"""Pinterest API v5 — image pins (product / collection photo from the Shopify CDN) linking the product or
collection page. Published at the slot time by the runner."""

from .. import config as C
from .base import canon, is_https, need

PINS_URL = 'https://api.pinterest.com/v5/pins'


def build(item, ctx):
    return {'board_id': C.get('PINTEREST_BOARD_ID') or '{PINTEREST_BOARD_ID}', 'title': item['title'],
            'description': item['caption'], 'link': item['link'], 'alt_text': item.get('alt_text', ''),
            'media_source': {'source_type': 'image_url', 'url': item['image_url']}}


def validate(p, item, ctx):
    errs = need(p, 'board_id', 'title', 'description', 'link')
    if len(p.get('title', '')) > 100:
        errs.append('title > 100')
    if len(p.get('description', '')) > 500:
        errs.append('description > 500')
    if len(p.get('alt_text', '')) > 500:
        errs.append('alt_text > 500')
    if not is_https(p.get('link', '')) or 'hokocollectables.com' not in p.get('link', ''):
        errs.append('link must be an https hokocollectables.com page')
    if not is_https(p['media_source'].get('url', '')):
        errs.append('image url not https')
    errs += canon(p.get('title'), p.get('description'), p.get('alt_text'))
    return errs


def send(item, p, http, ctx):
    j = http.post(PINS_URL, json=p, headers={'Authorization': f'Bearer {C.get("PINTEREST_TOKEN")}',
                                               'Content-Type': 'application/json'})
    return j['id']
