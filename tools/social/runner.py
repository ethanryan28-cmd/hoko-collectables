"""Runner — called every 15 min ("HOKO Social Runner"). Idempotent via data/social-post-log.csv.

Per item, the latest log row decides: OK / FAIL / SKIP = done; RETRY = try again next run.
A failure is logged RETRY twice, then FAIL on the third failed attempt (2 retries then FAIL).

When an item is acted on:
  youtube      every item slotted within the next 14 days is uploaded at once, scheduled with publishAt
  facebook     scheduled natively (scheduled_publish_time) once its slot is 15 min – 14 days ahead
  instagram, pinterest, discord, tiktok_queue (and tiktok when TIKTOK_ENABLED=true)
               published when the slot has arrived (no native scheduling)
  any item more than 6 h past its slot and never sent is logged SKIP (stale), never posted late.
Platforms with missing env keys are left pending (reported as NOT CONFIGURED), so adding keys later just works.

Dry run: builds + validates every queue item's payload, no network, no log writes → data/social-dryrun.json.
"""

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

from . import config as C
from . import hosting
from .http import Http
from .publishers import discord, facebook, instagram, pinterest, tiktok, youtube
from .publishers.base import PLACEHOLDER_URL
from .queue_builder import load_queue
from .schedule import FB_HORIZON, FB_MIN_LEAD, LATE_GRACE, YT_HORIZON, now as now_tz, parse

LOG_FIELDS = ['ts', 'item_id', 'platform', 'slot', 'asset_id', 'attempt', 'status', 'remote_id', 'error']
MAX_ATTEMPTS = 3
PUB = {'youtube': youtube, 'facebook': facebook, 'instagram': instagram, 'pinterest': pinterest, 'discord': discord}


# ------------------------------------------------------------------ log

def read_log(path=None):
    path = Path(path or C.LOG_PATH)
    if not path.exists():
        return []
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def append_log(row, path=None):
    path = Path(path or C.LOG_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, '') for k in LOG_FIELDS})


def state(log_rows):
    """item_id -> (last status, attempts so far)."""
    st = {}
    for r in log_rows:
        prev = st.get(r['item_id'], ('', 0))
        attempts = prev[1] + (1 if r['status'] in ('OK', 'RETRY', 'FAIL') else 0)
        st[r['item_id']] = (r['status'], attempts)
    return st


# ------------------------------------------------------------------ timing

def action(item, now):
    """'send' | 'send-late' | 'wait' | 'stale' for this item at `now`."""
    slot = parse(item['slot'])
    p = item['platform']
    if now > slot + LATE_GRACE:
        return 'stale'
    if p == 'youtube':
        if slot - now > YT_HORIZON:
            return 'wait'
        return 'send' if slot - now > timedelta(minutes=5) else 'send-late'
    if p == 'facebook':
        if slot - now > FB_HORIZON:
            return 'wait'
        return 'send' if slot - now >= FB_MIN_LEAD else 'send-late'
    return 'send' if now >= slot else 'wait'


def expand(items):
    """TikTok API items (one per clip) are derived from each tiktok_queue package when TIKTOK_ENABLED."""
    out = list(items)
    if C.tiktok_enabled():
        for it in items:
            if it['platform'] == 'tiktok_queue':
                for n, c in enumerate(it.get('clips', []), 1):
                    out.append(dict(c, id=f'tiktok:{it["slot"][:16]}:{n}', platform='tiktok', slot=it['slot']))
    return out


# ------------------------------------------------------------------ payloads

def payload(item, ctx):
    p = item['platform']
    if p == 'tiktok_queue':
        pl = discord.build_pack(item, ctx)
        return pl, discord.validate_pack(pl, item, ctx)
    if p == 'tiktok':
        pl = tiktok.build(item, ctx)
        return pl, tiktok.validate(pl, item, ctx)
    mod = PUB[p]
    pl = mod.build(item, ctx)
    return pl, mod.validate(pl, item, ctx)


def send(item, pl, http, ctx):
    p = item['platform']
    if p == 'tiktok_queue':
        return discord.send_pack(item, pl, http, ctx)
    if p == 'tiktok':
        return tiktok.send(item, pl, http, ctx)
    return PUB[p].send(item, pl, http, ctx)


def configured(platform):
    if platform == 'tiktok':
        return C.tiktok_enabled() and not C.missing('tiktok')
    return not C.missing(platform)


# ------------------------------------------------------------------ run

def run(now=None, http=None, queue=None, log_path=None, out=print):
    now = now or now_tz()
    http = http or Http()
    q = queue or load_queue()
    if not q:
        out('no content/social-queue.json — run: python -m tools.social build')
        return {}
    st = state(read_log(log_path))
    summary = {}
    ctx_shared = {}
    for it in expand(q['items']):
        if it.get('error'):
            continue
        p = it['platform']
        last, attempts = st.get(it['id'], ('', 0))
        if last in ('OK', 'FAIL', 'SKIP'):
            continue
        act = action(it, now)
        if act == 'wait':
            continue
        base = {'ts': now.isoformat(timespec='seconds'), 'item_id': it['id'], 'platform': p, 'slot': it['slot'],
                'asset_id': it.get('asset_id') or ','.join(c['asset_id'] for c in it.get('clips', []))}
        if act == 'stale':
            append_log(dict(base, status='SKIP', error='stale: slot passed by more than 6h'), log_path)
            summary[p] = summary.get(p, []) + ['SKIP']
            continue
        if not configured(p):
            summary.setdefault(f'{p} NOT CONFIGURED', []).append(it['id'])
            continue
        attempt = attempts + 1
        try:
            ctx = dict(ctx_shared, now=now, late=(act == 'send-late'))
            if p in ('instagram', 'facebook'):
                ctx['hosted_url'] = hosting.public_url(http, it['media'])
            pl, errs = payload(it, ctx)
            if errs:
                raise ValueError('invalid payload: ' + '; '.join(errs))
            rid = send(it, pl, http, ctx)
            ctx_shared.update({k: v for k, v in ctx.items() if k == 'yt_token'})
            append_log(dict(base, attempt=attempt, status='OK', remote_id=rid), log_path)
            summary[p] = summary.get(p, []) + ['OK']
        except Exception as e:   # noqa: BLE001 — every failure is logged, never raised
            status = 'FAIL' if attempt >= MAX_ATTEMPTS else 'RETRY'
            append_log(dict(base, attempt=attempt, status=status, error=str(e)[:500]), log_path)
            summary[p] = summary.get(p, []) + [status]
    for k, v in summary.items():
        out(f'{k}: {len(v)} ' + (', '.join(f'{s}×{v.count(s)}' for s in sorted(set(v))) if 'NOT CONFIGURED' not in k else ''))
    return summary


def dry_run(now=None, queue=None, out=print, write=True):
    """Build + validate every future queue item for every platform. No network, no log writes."""
    now = now or now_tz()
    q = queue or load_queue()
    if not q:
        raise SystemExit('no content/social-queue.json — run: python -m tools.social build')
    report = {'now': now.isoformat(), 'platforms': {}, 'problems': [], 'samples': {}}
    items = list(q['items'])
    for it in items:      # TikTok API payloads are validated even while TIKTOK_ENABLED=false
        if it['platform'] == 'tiktok_queue':
            for n, c in enumerate(it.get('clips', []), 1):
                items.append(dict(c, id=f'tiktok:{it["slot"][:16]}:{n}', platform='tiktok', slot=it['slot']))
    for it in items:
        p = it['platform']
        rep = report['platforms'].setdefault(p, {'valid': 0, 'invalid': 0, 'past': 0, 'media_present': 0, 'media_missing': 0})
        if it.get('error'):
            rep['invalid'] += 1
            report['problems'].append(f'{it["id"]}: {it["error"]}')
            continue
        slot = parse(it['slot'])
        if slot <= now:
            rep['past'] += 1
            continue
        # act at the moment the runner would: YT/FB ahead of time (now), the rest at the slot
        act_now = now if p in ('youtube', 'facebook') else slot
        ctx = {'now': act_now, 'late': False, 'hosted_url': PLACEHOLDER_URL, 'size': 1}
        pl, errs = payload(it, ctx)
        if p == 'tiktok_queue':
            medias = [c['media'] for c in it.get('clips', [])]
        elif p in ('youtube', 'instagram', 'facebook', 'tiktok'):
            medias = [it['media']]
        else:
            medias = []
        for m in medias:
            rep['media_present' if (C.REPO / m).exists() else 'media_missing'] += 1
        if errs:
            rep['invalid'] += 1
            report['problems'].append(f'{it["id"]}: ' + '; '.join(errs))
        else:
            rep['valid'] += 1
            report['samples'].setdefault(p, {'item': it['id'], 'payload': pl})
    for p, r in sorted(report['platforms'].items()):
        out(f'{p:<13} valid {r["valid"]:>3}  invalid {r["invalid"]:>2}  past {r["past"]:>2}  '
            f'media present {r["media_present"]:>3} / missing {r["media_missing"]:>3}')
    for pr in report['problems'][:50]:
        out('  ✗ ' + pr)
    if write:
        C.DRYRUN_PATH.parent.mkdir(parents=True, exist_ok=True)
        C.DRYRUN_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
        out(f'→ {C.DRYRUN_PATH.relative_to(C.REPO)}')
    return report
