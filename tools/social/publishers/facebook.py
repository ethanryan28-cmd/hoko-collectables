"""Facebook Page video, scheduled natively with scheduled_publish_time (published=false).
Mirrors the Instagram slot. Video is passed by file_url (the clip hosted on Shopify Files)."""

from .. import config as C
from ..schedule import FB_MIN_LEAD, parse
from .base import PLACEHOLDER_URL, canon, is_https, need


def build(item, ctx):
    slot = parse(item['slot'])
    p = {'file_url': ctx.get('hosted_url') or PLACEHOLDER_URL, 'description': item['caption']}
    if ctx.get('late'):
        p['published'] = 'true'
    else:
        p['published'] = 'false'
        p['scheduled_publish_time'] = int(slot.timestamp())
    p['_page'] = C.get('FB_PAGE_ID') or '{FB_PAGE_ID}'
    return p


def validate(p, item, ctx):
    errs = need(p, 'file_url', 'description')
    if not is_https(p.get('file_url', '')):
        errs.append('file_url not https')
    if p.get('published') == 'false':
        lead = p['scheduled_publish_time'] - int(ctx['now'].timestamp())
        if lead < 600:
            errs.append(f'scheduled_publish_time only {lead}s ahead (needs ≥ 600)')
        if lead > 30 * 86400:
            errs.append('scheduled_publish_time more than 30 days ahead')
    if len(p.get('description', '')) > 63206:
        errs.append('description too long')
    errs += canon(p.get('description'))
    return errs


def send(item, p, http, ctx):
    data = {k: v for k, v in p.items() if not k.startswith('_')}
    data['access_token'] = C.get('META_PAGE_TOKEN')
    j = http.post(f'{C.GRAPH_VIDEO}/{C.get("FB_PAGE_ID")}/videos', data=data)
    return j['id']


def lead_ok(item, now):
    return parse(item['slot']) - now >= FB_MIN_LEAD
