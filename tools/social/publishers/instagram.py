"""Instagram Reels via the Graph API: create container (video_url on Shopify Files) → poll → media_publish.
The Graph API has no native scheduling for Reels, so the runner publishes at the slot time."""

import time

from .. import config as C
from .base import PLACEHOLDER_URL, canon, is_https, need


def build(item, ctx):
    return {'media_type': 'REELS', 'video_url': ctx.get('hosted_url') or PLACEHOLDER_URL,
            'caption': item['caption'], 'share_to_feed': 'true',
            '_ig': C.get('IG_BUSINESS_ID') or '{IG_BUSINESS_ID}'}


def validate(p, item, ctx):
    errs = need(p, 'media_type', 'video_url', 'caption')
    if not is_https(p.get('video_url', '')):
        errs.append('video_url not https')
    c = p.get('caption', '')
    if len(c) > 2200:
        errs.append(f'caption {len(c)} > 2200')
    if c.count('#') > 30:
        errs.append('more than 30 hashtags')
    if c.count('@') > 20:
        errs.append('more than 20 mentions')
    errs += canon(c)
    return errs


def send(item, p, http, ctx, sleep=time.sleep):
    ig, tok = C.get('IG_BUSINESS_ID'), C.get('META_PAGE_TOKEN')
    data = {k: v for k, v in p.items() if not k.startswith('_')}
    data['access_token'] = tok
    cid = http.post(f'{C.GRAPH}/{ig}/media', data=data)['id']
    for _ in range(60):
        s = http.get(f'{C.GRAPH}/{cid}', params={'fields': 'status_code', 'access_token': tok})
        if s.get('status_code') == 'FINISHED':
            break
        if s.get('status_code') in ('ERROR', 'EXPIRED'):
            raise RuntimeError(f'IG container {cid}: {s.get("status_code")}')
        sleep(10)
    else:
        raise RuntimeError(f'IG container {cid} not FINISHED after 10 min')
    return http.post(f'{C.GRAPH}/{ig}/media_publish', data={'creation_id': cid, 'access_token': tok})['id']
