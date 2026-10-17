"""Public URLs for local clips: Instagram, Facebook (file_url) and TikTok need a URL the platform can fetch.
Clips go to Shopify Files (stagedUploadsCreate → upload → fileCreate → poll READY). Cached by path+size+mtime
in data/social-media-cache.json so a clip is only uploaded once."""

import json
import time
from pathlib import Path

from . import config as C


def _cache():
    try:
        return json.loads(C.MEDIA_CACHE_PATH.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def _save(c):
    C.MEDIA_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    C.MEDIA_CACHE_PATH.write_text(json.dumps(c, indent=1), encoding='utf-8')


def _key(p):
    st = p.stat()
    return f'{p.as_posix()}|{st.st_size}|{int(st.st_mtime)}'


def gql(http, query, variables):
    store, token = C.get('SHOPIFY_STORE'), C.get('SHOPIFY_ADMIN_TOKEN')
    j = http.post(f'https://{store}/admin/api/{C.SHOPIFY_API}/graphql.json',
                  json={'query': query, 'variables': variables},
                  headers={'X-Shopify-Access-Token': token, 'Content-Type': 'application/json'})
    if j.get('errors'):
        raise RuntimeError(f'Shopify GraphQL: {str(j["errors"])[:300]}')
    return j['data']


def public_url(http, media, sleep=time.sleep):
    p = (C.REPO / media) if not Path(media).is_absolute() else Path(media)
    if not p.exists():
        raise FileNotFoundError(f'media missing: {media} — render it on the PC (python -m tools.social render)')
    cache = _cache()
    k = _key(p)
    if k in cache:
        return cache[k]
    d = gql(http, """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
        stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }""",
            {'input': [{'filename': p.name, 'mimeType': 'video/mp4', 'resource': 'VIDEO',
                        'fileSize': str(p.stat().st_size), 'httpMethod': 'POST'}]})['stagedUploadsCreate']
    if d['userErrors']:
        raise RuntimeError(f'stagedUploadsCreate: {d["userErrors"]}')
    tgt = d['stagedTargets'][0]
    with open(p, 'rb') as fh:
        http.request('POST', tgt['url'], data={x['name']: x['value'] for x in tgt['parameters']},
                     files={'file': (p.name, fh, 'video/mp4')})
    d = gql(http, """mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){
        files{ id fileStatus } userErrors{ field message } } }""",
            {'files': [{'originalSource': tgt['resourceUrl'], 'contentType': 'VIDEO', 'alt': f'HOKO clip {p.stem}'}]})['fileCreate']
    if d['userErrors']:
        raise RuntimeError(f'fileCreate: {d["userErrors"]}')
    fid = d['files'][0]['id']
    for _ in range(60):
        n = gql(http, """query($id:ID!){ node(id:$id){ ... on Video { fileStatus sources{ url mimeType height } } } }""",
                {'id': fid})['node']
        if n['fileStatus'] == 'READY':
            url = max((s for s in n['sources'] if s['mimeType'] == 'video/mp4'), key=lambda s: s['height'])['url']
            cache[k] = url
            _save(cache)
            return url
        if n['fileStatus'] == 'FAILED':
            raise RuntimeError(f'Shopify video processing failed: {fid}')
        sleep(10)
    raise RuntimeError(f'Shopify video not READY after 10 min: {fid}')
