"""Discord webhooks.
- pickups:   17:00 product drop → #pickups-and-drops (embed with photo + link).
- tiktok_queue: 07:00 package → #tiktok-queue: a header message, then one message per clip with the mp4
  attached and its caption in a code block, so Ethan can save + paste from his phone.
"""

import json
from pathlib import Path

from .. import config as C
from .base import canon, is_https, need

ORANGE = 0xFF6B2B
MAX_MB = float(C.get('DISCORD_MAX_UPLOAD_MB', '10') or 10)   # 10 MB on un-boosted servers


def build(item, ctx):
    return {'username': 'HOKO Collectables', 'allowed_mentions': {'parse': []},
            'content': '',
            'embeds': [{'title': item['title'][:256], 'url': item['link'], 'description': item['caption'][:4000],
                        'color': ORANGE, 'image': {'url': item['image_url']},
                        'footer': {'text': 'Collector first. Seller second. · Victoria, Australia'}}]}


def validate(p, item, ctx):
    e = p['embeds'][0]
    errs = need(e, 'title', 'url', 'description')
    if not is_https(e.get('url', '')):
        errs.append('embed url not https')
    if not is_https(e.get('image', {}).get('url', '')):
        errs.append('embed image not https')
    errs += canon(e.get('title'), e.get('description'))
    return errs


def send(item, p, http, ctx):
    r = http.request('POST', C.get('DISCORD_WEBHOOK_PICKUPS') + '?wait=true', json=p)
    return str(r.json().get('id', 'ok'))


# ---- #tiktok-queue package -------------------------------------------------------------------------------

def build_pack(item, ctx):
    day = item['slot'][:10]
    msgs = [{'username': 'HOKO TikTok queue', 'allowed_mentions': {'parse': []},
             'content': f'**TikTok queue — {day}** · {len(item["clips"])} clips. Save each video, paste its caption, post.'}]
    for n, c in enumerate(item['clips'], 1):
        msgs.append({'username': 'HOKO TikTok queue', 'allowed_mentions': {'parse': []},
                     'content': f'**{n}/{len(item["clips"])} · {c["name"]}**\n```\n{c["caption"]}\n```'[:2000],
                     '_file': c['media']})
    return {'messages': msgs}


def validate_pack(p, item, ctx):
    errs = []
    if len(p['messages']) < 2:
        errs.append('no clips in package')
    for m in p['messages']:
        if len(m['content']) > 2000:
            errs.append('message > 2000 chars')
        if m.get('_file') and not str(m['_file']).endswith('.mp4'):
            errs.append(f'{m["_file"]} is not an mp4')
        errs += canon(m['content'])
    return errs


def send_pack(item, p, http, ctx):
    hook = C.get('DISCORD_WEBHOOK_TIKTOK_QUEUE') + '?wait=true'
    for m in p['messages']:      # check every file before posting anything
        f = m.get('_file')
        if f:
            fp = C.REPO / f
            if not fp.exists():
                raise FileNotFoundError(f'media missing: {f}')
            if fp.stat().st_size > MAX_MB * 1024 * 1024:
                raise RuntimeError(f'{f} is {fp.stat().st_size / 1e6:.1f} MB > Discord limit {MAX_MB} MB')
    ids = []
    for m in p['messages']:
        body = {k: v for k, v in m.items() if not k.startswith('_')}
        f = m.get('_file')
        if f:
            fp = C.REPO / f
            with open(fp, 'rb') as fh:
                r = http.request('POST', hook, data={'payload_json': json.dumps(body)},
                                 files={'files[0]': (Path(f).name, fh, 'video/mp4')})
        else:
            r = http.request('POST', hook, json=body)
        ids.append(str(r.json().get('id', 'ok')))
    return ','.join(ids)
