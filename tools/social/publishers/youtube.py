"""YouTube Shorts — Data API v3 resumable upload, scheduled with status.publishAt (privacy private until then).
OAuth via refresh token (YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN); no browser on the PC."""

from datetime import timezone
from pathlib import Path

from .. import config as C
from .base import canon, need

TOKEN_URL = 'https://oauth2.googleapis.com/token'
UPLOAD_URL = 'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status'


def _tags(caption):
    last = (caption or '').strip().splitlines()[-1] if caption else ''
    return [t.lstrip('#') for t in last.split() if t.startswith('#')][:15]


def build(item, ctx):
    from ..schedule import parse
    slot = parse(item['slot'])
    status = {'selfDeclaredMadeForKids': False}
    if ctx.get('late'):
        status['privacyStatus'] = 'public'
    else:
        status['privacyStatus'] = 'private'
        status['publishAt'] = slot.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return {'snippet': {'title': item['title'], 'description': item['caption'][:4900],
                        'tags': _tags(item['caption']), 'categoryId': '22', 'defaultLanguage': 'en-AU'},
            'status': status, '_media': item['media']}


def validate(p, item, ctx):
    errs = need(p['snippet'], 'title', 'description')
    t = p['snippet'].get('title', '')
    if len(t) > 100:
        errs.append(f'title {len(t)} > 100 chars')
    if '<' in t or '>' in t:
        errs.append('title has < or >')
    if len(p['snippet'].get('description', '')) > 5000:
        errs.append('description > 5000')
    if p['status'].get('publishAt'):
        if p['status'].get('privacyStatus') != 'private':
            errs.append('publishAt requires privacyStatus=private')
        from datetime import datetime
        pa = datetime.strptime(p['status']['publishAt'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        if pa <= ctx['now']:
            errs.append('publishAt is in the past')
    if not str(p.get('_media', '')).endswith('.mp4'):
        errs.append('media is not an mp4')
    errs += canon(t, p['snippet'].get('description'))
    return errs


def access_token(http):
    j = http.post(TOKEN_URL, data={'client_id': C.get('YT_CLIENT_ID'), 'client_secret': C.get('YT_CLIENT_SECRET'),
                                   'refresh_token': C.get('YT_REFRESH_TOKEN'), 'grant_type': 'refresh_token'})
    return j['access_token']


def send(item, p, http, ctx):
    media = C.REPO / p['_media']
    if not media.exists():
        raise FileNotFoundError(f'media missing: {p["_media"]}')
    tok = ctx.get('yt_token') or access_token(http)
    ctx['yt_token'] = tok
    body = {k: v for k, v in p.items() if not k.startswith('_')}
    size = media.stat().st_size
    r = http.request('POST', UPLOAD_URL, json=body,
                     headers={'Authorization': f'Bearer {tok}', 'X-Upload-Content-Type': 'video/mp4',
                              'X-Upload-Content-Length': str(size)})
    loc = r.headers.get('Location') or r.headers.get('location')
    if not loc:
        raise RuntimeError('YouTube resumable session: no Location header')
    with open(media, 'rb') as fh:
        j = http.request('PUT', loc, data=fh, headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'video/mp4',
                                                         'Content-Length': str(size)}).json()
    return j['id']
