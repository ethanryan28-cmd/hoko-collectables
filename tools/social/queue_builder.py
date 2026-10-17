"""Builds content/social-queue.json: every platform, every slot, HORIZON days ahead.

Rules
- Slots from schedule.SLOTS (Australia/Melbourne). Facebook mirrors Instagram (same clip, same caption body).
- No clip/asset repeats on the same platform within 7 days (NO_REPEAT).
- Category mix per platform follows schedule.season_weights (Japanese sealed heavier through November):
  each slot takes the category furthest below its target share.
- Within a category: least-recently-used product on that platform first, then least-recently-used asset.
- A product is used at most once per platform per day.
- Pinned beat reels (BF / Christmas) take the first video slot of their date on IG / YT / TikTok.
- Newest-set push (17 Oct 2026): assets of a set in config `hot_sets` must take >= `social_hot_share` (0.6) of the
  slots on every platform. While a platform is under its share the hot pool is tried first (least-recently-used
  product, then asset), with a shorter repeat window (`social_hot_repeat_days`, default 2) because the five newest
  boxes only have one or two clips each. Non-hot assets keep the 7-day rule.
- Topup keeps every existing item from today on (already-scheduled YT/FB uploads must not change) and only
  appends missing days; history (incl. older items) feeds the 7-day rule.
"""

import hashlib
import json
from datetime import date, timedelta

from . import captions as cap
from .assets import is_hot, load as load_assets
from .config import BF_WEEK, QUEUE_PATH, TZ_NAME, hot_config
from .schedule import (SLOTS, TIKTOK_PER_DAY, days, local_date, parse, season_weights, slot_dt)

HORIZON = 15            # today + 14 full days
NO_REPEAT = timedelta(days=7)
ORDER = ['youtube', 'instagram', 'tiktok_queue', 'pinterest', 'discord']   # facebook is derived from instagram


def category(a):
    if a.kind == 'slab' or a.extra.get('source') == 'slab' or a.extra.get('collection') == 'graded-slabs':
        return 'slab'
    if a.jp_sealed:
        return 'jp'
    return 'other'


def bf_week_ok(a, day):
    """20–30 Nov: every post links a product page or /collections/japan-direct-sealed (brief, 17 Oct 2026)."""
    iso = str(day)
    if not (BF_WEEK[0] <= iso <= BF_WEEK[1]):
        return True
    return '/products/' in (a.url or '') or (a.url or '').rstrip('/').endswith('/collections/japan-direct-sealed')


def pool_for(platform, assets, day=None):
    if day is not None:
        assets = [a for a in assets if bf_week_ok(a, day)]
    if platform in ('youtube', 'instagram', 'tiktok_queue'):
        return [a for a in assets if a.eligible and a.media_type == 'video' and a.kind != 'beat']
    if platform == 'pinterest':
        return [a for a in assets if a.eligible and a.media_type == 'image']
    if platform == 'discord':
        return [a for a in assets if a.eligible and a.kind == 'product']
    return []


def _h(*x):
    return int(hashlib.sha1('|'.join(map(str, x)).encode()).hexdigest()[:8], 16)


class History:
    def __init__(self):
        self.uses = {}        # (platform, asset_id) -> [dt]
        self.puses = {}       # (platform, product_key) -> [dt]
        self.cats = {}        # platform -> {cat: n}
        self.hot = {}         # platform -> [n_hot, n_total]

    def add(self, platform, a_id, pkey, cat, dt, hot=False, share=True):
        self.uses.setdefault((platform, a_id), []).append(dt)
        self.puses.setdefault((platform, pkey), []).append(dt)
        c = self.cats.setdefault(platform, {})
        c[cat] = c.get(cat, 0) + 1
        if not share:  # past items still block repeats, but the hot share is measured from today, as check does
            return
        h = self.hot.setdefault(platform, [0, 0])
        h[0] += int(bool(hot))
        h[1] += 1

    def hot_share(self, platform):
        n_hot, n = self.hot.get(platform, [0, 0])
        return n_hot / n if n else 0.0

    def last(self, platform, a_id, dt):
        prev = [d for d in self.uses.get((platform, a_id), []) if d <= dt]
        return max(prev) if prev else None

    def plast(self, platform, pkey, dt):
        prev = [d for d in self.puses.get((platform, pkey), []) if d <= dt]
        return max(prev) if prev else None

    def blocked(self, platform, a_id, dt, window=NO_REPEAT):
        return any(abs(dt - d) < window for d in self.uses.get((platform, a_id), []))


def pkey(a):
    return a.product_id or a.id


def _lru_sort(platform, dt, hist, cands):
    epoch = parse('2000-01-01T00:00:00+10:00')
    cands.sort(key=lambda a: (hist.plast(platform, pkey(a), dt) or epoch,
                              hist.last(platform, a.id, dt) or epoch,
                              _h(a.id, platform, dt.date())))
    return cands


def choose(platform, dt, pool, hist, used_today, hot=None):
    hot = hot if hot is not None else hot_config()
    hot_sets = hot['hot_sets']
    # newest-set push: while this platform is under its hot share, try the hot pool first
    if hot_sets and hist.hot_share(platform) < hot['share']:
        window = timedelta(days=hot['repeat_days'])
        cands = [a for a in pool if is_hot(a, hot_sets) and not hist.blocked(platform, a.id, dt, window)
                 and pkey(a) not in used_today]
        if cands:
            a = _lru_sort(platform, dt, hist, cands)[0]
            return a, category(a)
    weights = season_weights(local_date(dt))
    counts = hist.cats.get(platform, {})
    total = sum(counts.values()) + 1
    order = sorted(weights, key=lambda c: -(weights[c] * total - counts.get(c, 0)))
    for cat in order:
        cands = [a for a in pool if category(a) == cat and not hist.blocked(platform, a.id, dt)
                 and pkey(a) not in used_today]
        if not cands:
            continue
        return _lru_sort(platform, dt, hist, cands)[0], cat
    return None, None


def _item(platform, dt, a, day):
    it = {'id': f'{platform}:{dt.strftime("%Y-%m-%dT%H:%M")}', 'platform': platform, 'slot': dt.isoformat(),
          'asset_id': a.id, 'kind': a.kind, 'media_type': a.media_type, 'media': a.media,
          'image_url': a.image_url, 'link': a.url, 'product_id': a.product_id, 'name': a.name,
          'set_code': a.set_code}
    if platform == 'youtube':
        it['title'] = cap.youtube_title(a)
        it['caption'] = cap.caption(a, 'youtube', day)
    elif platform == 'instagram':
        it['caption'] = cap.caption(a, 'instagram', day)
    elif platform == 'pinterest':
        it['title'], it['caption'], it['alt_text'] = cap.pinterest_fields(a, day)
    elif platform == 'discord':
        it['title'] = cap.headline(a)
        it['caption'] = '\n'.join(cap.body(a, 'discord', day) + cap.bf_lines(day))
    return it


def _clip(a, day):
    return {'asset_id': a.id, 'kind': a.kind, 'media': a.media, 'link': a.url, 'name': a.name,
            'set_code': a.set_code, 'caption': cap.caption(a, 'tiktok', day, tags=True)}


def build(start=None, n_days=HORIZON, existing=None, assets=None):
    start = start or date.today()
    assets = assets if assets is not None else load_assets(start)
    by_id = {a.id: a for a in assets}
    hot = hot_config()
    hs = hot['hot_sets']
    hist = History()
    keep = []
    have_days = {}

    for it in (existing or {}).get('items', []):
        dt = parse(it['slot'])
        clips = it.get('clips') or ([{'asset_id': it['asset_id']}] if it.get('asset_id') else [])
        for c in clips:
            ca = by_id.get(c['asset_id'])
            hist.add(it['platform'], c['asset_id'], pkey(ca) if ca else c['asset_id'],
                     category(ca) if ca else 'other', dt, hot=bool(ca) and is_hot(ca, hs), share=local_date(dt) >= start)
        if local_date(dt) >= start:
            keep.append(it)
            have_days.setdefault(it['platform'], set()).add(local_date(dt))

    beats = {a.pin_date: a for a in assets if a.kind == 'beat' and a.eligible}
    items = list(keep)
    for day in days(start, n_days):
        iso = day.isoformat()
        for platform in ORDER:
            if day in have_days.get(platform, set()):
                continue
            pool = pool_for(platform, assets, day)
            used_today = set()
            for k, hhmm in enumerate(SLOTS[platform]):
                dt = slot_dt(day, hhmm)
                if platform == 'tiktok_queue':
                    clips = []
                    if iso in beats:
                        b = beats[iso]
                        clips.append(_clip(b, iso))
                        hist.add(platform, b.id, pkey(b), category(b), dt, hot=is_hot(b, hs))
                    while len(clips) < TIKTOK_PER_DAY:
                        a, cat = choose(platform, dt, pool, hist, used_today, hot)
                        if not a:
                            break
                        used_today.add(pkey(a))
                        hist.add(platform, a.id, pkey(a), cat, dt, hot=is_hot(a, hs))
                        clips.append(_clip(a, iso))
                    items.append({'id': f'tiktok_queue:{dt.strftime("%Y-%m-%dT%H:%M")}', 'platform': platform,
                                  'slot': dt.isoformat(), 'clips': clips})
                    continue
                if k == 0 and iso in beats and platform in ('youtube', 'instagram'):
                    a, cat = beats[iso], category(beats[iso])
                else:
                    a, cat = choose(platform, dt, pool, hist, used_today, hot)
                if not a:
                    items.append({'id': f'{platform}:{dt.strftime("%Y-%m-%dT%H:%M")}', 'platform': platform,
                                  'slot': dt.isoformat(), 'error': 'no eligible asset (7-day rule exhausted)'})
                    continue
                used_today.add(pkey(a))
                hist.add(platform, a.id, pkey(a), cat, dt, hot=is_hot(a, hs))
                it = _item(platform, dt, a, iso)
                items.append(it)
                if platform == 'instagram' and day not in have_days.get('facebook', set()):
                    fb = dict(it, id=f'facebook:{dt.strftime("%Y-%m-%dT%H:%M")}', platform='facebook',
                              mirror_of=it['id'], caption=cap.caption(a, 'facebook', iso))
                    items.append(fb)
                    hist.add('facebook', a.id, pkey(a), cat, dt, hot=is_hot(a, hs))

    items.sort(key=lambda i: (i['slot'], ORDER.index(i['platform']) if i['platform'] in ORDER else 9))
    return {'generated_at': date.today().isoformat(), 'tz': TZ_NAME, 'start': start.isoformat(),
            'horizon_days': n_days, 'items': items}


def load_queue(path=QUEUE_PATH):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8'))


def save_queue(q, path=QUEUE_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(q, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def topup(start=None, path=QUEUE_PATH):
    q = build(start=start, existing=load_queue(path))
    save_queue(q, path)
    return q


def coverage(q):
    """platform -> number of distinct dates with at least one valid item."""
    cov = {}
    for it in q['items']:
        if it.get('error') or (it['platform'] == 'tiktok_queue' and not it.get('clips')):
            continue
        cov.setdefault(it['platform'], set()).add(parse(it['slot']).date())
    return {p: len(d) for p, d in cov.items()}


def violations(q):
    """Rule check over the whole queue: same asset on the same platform within 7 days, banned words, prices."""
    out = []
    seen = {}
    hot = hot_config()
    hot_window = timedelta(days=hot['repeat_days'])
    for it in sorted(q['items'], key=lambda i: i['slot']):
        dt = parse(it['slot'])
        entries = it.get('clips') or [it]
        for e in entries:
            if not e.get('asset_id'):
                continue
            key = (it['platform'], e['asset_id'])
            is_h = bool(e.get('set_code')) and e['set_code'] in hot['hot_sets']
            window = hot_window if is_h else NO_REPEAT
            for prev in seen.get(key, []):
                if dt - prev < window:
                    out.append(f'{it["id"]}: {e["asset_id"]} repeats within {window.days} days ({prev.isoformat()})')
            seen.setdefault(key, []).append(dt)
            for field in ('caption', 'title', 'alt_text'):
                for p in cap.check(e.get(field)):
                    out.append(f'{it["id"]} {field}: {p}')
        if it.get('error'):
            out.append(f'{it["id"]}: {it["error"]}')
    return out


def hot_share(q, start=None, n_days=HORIZON):
    """platform -> (hot, total, share) over the window start..start+n_days; 'all' = aggregate."""
    hot = hot_config()
    hs = set(hot['hot_sets'])
    start = start or date.today()
    end = start + timedelta(days=n_days)
    counts = {}
    for it in q['items']:
        d = local_date(parse(it['slot']))
        if not (start <= d < end) or it.get('error'):
            continue
        for e in (it.get('clips') or [it]):
            if not e.get('asset_id'):
                continue
            c = counts.setdefault(it['platform'], [0, 0])
            c[0] += int(bool(e.get('set_code')) and e['set_code'] in hs)
            c[1] += 1
    allc = [sum(c[0] for c in counts.values()), sum(c[1] for c in counts.values())]
    counts['all'] = allc
    return {p: (c[0], c[1], round(c[0] / c[1], 3) if c[1] else 0.0) for p, c in counts.items()}
