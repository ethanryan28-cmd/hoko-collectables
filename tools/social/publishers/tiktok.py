"""TikTok Content Posting API (direct post, FILE_UPLOAD). OFF unless TIKTOK_ENABLED=true.
Un-audited TikTok apps can only post SELF_ONLY (private); set TIKTOK_PRIVACY=PUBLIC_TO_EVERYONE after audit.
The default path is the #tiktok-queue Discord package (publishers/discord.py)."""

from .. import config as C
from .base import canon

TOKEN_URL = 'https://open.tiktokapis.com/v2/oauth/token/'
INIT_URL = 'https://open.tiktokapis.com/v2/post/publish/video/init/'


def build(clip, ctx):
    size = ctx.get('size', 0)
    return {'post_info': {'title': clip['caption'][:2200], 'privacy_level': C.get('TIKTOK_PRIVACY', 'SELF_ONLY'),
                          'disable_duet': False, 'disable_comment': False, 'disable_stitch': False},
            'source_info': {'source': 'FILE_UPLOAD', 'video_size': size, 'chunk_size': size, 'total_chunk_count': 1},
            '_media': clip['media']}


def validate(p, clip, ctx):
    errs = []
    if p['post_info']['privacy_level'] not in ('SELF_ONLY', 'MUTUAL_FOLLOW_FRIENDS', 'FOLLOWER_OF_CREATOR', 'PUBLIC_TO_EVERYONE'):
        errs.append('bad privacy_level')
    if len(p['post_info']['title']) > 2200:
        errs.append('title > 2200')
    if not str(p['_media']).endswith('.mp4'):
        errs.append('media not mp4')
    errs += canon(p['post_info']['title'])
    return errs


def send(clip, p, http, ctx):
    media = C.REPO / p['_media']
    if not media.exists():
        raise FileNotFoundError(f'media missing: {p["_media"]}')
    size = media.stat().st_size
    p = build(clip, dict(ctx, size=size))
    tok = http.post(TOKEN_URL, data={'client_key': C.get('TIKTOK_CLIENT_KEY'), 'client_secret': C.get('TIKTOK_CLIENT_SECRET'),
                                     'grant_type': 'refresh_token', 'refresh_token': C.get('TIKTOK_REFRESH_TOKEN')},
                    headers={'Content-Type': 'application/x-www-form-urlencoded'})['access_token']
    body = {k: v for k, v in p.items() if not k.startswith('_')}
    j = http.post(INIT_URL, json=body, headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json; charset=UTF-8'})
    data = j['data']
    with open(media, 'rb') as fh:
        http.request('PUT', data['upload_url'], data=fh,
                     headers={'Content-Type': 'video/mp4', 'Content-Length': str(size),
                              'Content-Range': f'bytes 0-{size - 1}/{size}'})
    return data['publish_id']
