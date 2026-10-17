"""Phone pack: today's tiktok_queue clips + Instagram items as markdown, for posting from the phone.

Day = today in Victoria (tz Australia/Melbourne); if that day has no tiktok_queue / instagram items, the next day that does.
Clip URLs point at raw.githubusercontent.com on main (mp4s are committed). Each printed item is appended to
data/phone-pack-log.csv (date, platform, asset_id, url).
"""

import csv
from datetime import date

from . import config as C
from .schedule import TZ, local_date, now, parse

RAW_BASE = 'https://raw.githubusercontent.com/ethanryan28-cmd/hoko-collectables/main/'
PLATFORMS = ('tiktok_queue', 'instagram')
LOG_PATH = C.DATA / 'phone-pack-log.csv'
LOG_HEADER = ['date', 'platform', 'asset_id', 'url']


def raw_url(media):
    """Repo-relative media path → raw.githubusercontent.com URL on main."""
    if not media:
        return ''
    m = media.replace('\\', '/')
    while m.startswith(('./', '/')):
        m = m[2:] if m.startswith('./') else m[1:]
    return RAW_BASE + m


def _day(it):
    return local_date(parse(it['slot']))


def pick_day(items, today):
    """`today` if it has tiktok_queue / instagram items, else the next day that does, else None."""
    days = sorted({_day(it) for it in items if it.get('platform') in PLATFORMS and _day(it) >= today})
    return days[0] if days else None


def entries(items, day):
    """Flat list of dicts (platform, slot, asset_id, name, url, link, caption) for `day`, slot order."""
    out = []
    for it in sorted((i for i in items if i.get('platform') in PLATFORMS and _day(i) == day), key=lambda i: i['slot']):
        slot = parse(it['slot']).astimezone(TZ).strftime('%H:%M')
        rows = it['clips'] if it['platform'] == 'tiktok_queue' else [it]
        for n, c in enumerate(rows, 1):
            url = raw_url(c.get('media', '')) if c.get('media_type', 'video') == 'video' else c.get('image_url', '')
            out.append({'platform': it['platform'], 'slot': slot, 'n': n if len(rows) > 1 else 0,
                        'asset_id': c.get('asset_id', ''), 'name': c.get('name', ''), 'url': url,
                        'link': c.get('link', ''), 'caption': c.get('caption', '')})
    return out


def markdown(day, rows):
    lines = [f'# HOKO phone pack · {day.isoformat()}', '']
    if not rows:
        return '\n'.join(lines + ['Nothing queued for tiktok_queue or instagram.', ''])
    for r in rows:
        tag = 'TikTok' if r['platform'] == 'tiktok_queue' else 'Instagram'
        head = f'## {tag} {r["slot"]}' + (f' #{r["n"]}' if r['n'] else '') + f' · {r["name"]}'
        lines += [head, '', f'- Clip: {r["url"]}', f'- Product: {r["link"]}', '', '```', r['caption'], '```', '']
    return '\n'.join(lines)


def log(day, rows, path=None):
    path = path or LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists() or path.stat().st_size == 0
    with open(path, 'a', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(LOG_HEADER)
        for r in rows:
            w.writerow([day.isoformat(), r['platform'], r['asset_id'], r['url']])


def main(a, out=print, log_path=None):
    from . import queue_builder as qb
    items = qb.load_queue()['items']
    today = date.fromisoformat(a.date) if getattr(a, 'date', None) else now().date()
    day = pick_day(items, today)
    if day is None:
        out(f'# HOKO phone pack · {today.isoformat()}\n\nNo tiktok_queue or instagram items from {today} on.')
        return 1
    rows = entries(items, day)
    out(markdown(day, rows))
    log(day, rows, log_path)
    return 0
