"""run.py publish — post today's queued calendar item.

Instagram: Graph API Reels flow (media → poll → media_publish). IG needs a PUBLIC video URL, so the mp4 is
first uploaded to Shopify Files (Admin API staged upload) and the Shopify CDN URL is used.
YouTube Shorts: Data API v3 resumable upload, OAuth token cached in .secrets/ (gitignored).
TikTok: not automated — TODAY.md gets the reel path + caption for Ethan.
"""

import json
import os
import platform
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

from . import calendar_gen as cal
from .common import REPO, ROOT, ffprobe, today
from .http import Http, MockHttp

GRAPH = 'https://graph.facebook.com/v21.0'
SHOPIFY_API = '2025-01'
SECRETS = ROOT / '.secrets'
YT_TOKEN = SECRETS / 'yt_token.json'
YT_SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.force-ssl']
LOG = ROOT / 'publish.log'


def log(msg):
    line = f'{datetime.now():%Y-%m-%d %H:%M:%S} {msg}'
    print(line)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


# ---------------------------------------------------------------- Shopify Files (public URL for IG)

def shopify_env():
    store = os.environ.get('SHOPIFY_STORE')
    token = os.environ.get('SHOPIFY_ADMIN_TOKEN') or os.environ.get('SHOPIFY_TOKEN')
    return store, token


def shopify_gql(http, query, variables):
    store, token = shopify_env()
    j = http.post(f'https://{store or "MOCK-STORE.myshopify.com"}/admin/api/{SHOPIFY_API}/graphql.json',
                  json={'query': query, 'variables': variables},
                  headers={'X-Shopify-Access-Token': token or 'mock', 'Content-Type': 'application/json'})
    if j.get('errors'):
        raise RuntimeError(f'Shopify GraphQL: {j["errors"]}')
    return j['data']


def upload_to_shopify_files(http, mp4):
    mp4 = Path(mp4)
    size = mp4.stat().st_size if mp4.exists() else 0
    d = shopify_gql(http, """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
        stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }""",
                    {'input': [{'filename': mp4.name, 'mimeType': 'video/mp4', 'resource': 'VIDEO',
                                'fileSize': str(size), 'httpMethod': 'POST'}]})['stagedUploadsCreate']
    if d['userErrors']:
        raise RuntimeError(d['userErrors'])
    tgt = d['stagedTargets'][0]
    if not http.mocked:
        with open(mp4, 'rb') as fh:
            http.post(tgt['url'], data={p['name']: p['value'] for p in tgt['parameters']},
                      files={'file': (mp4.name, fh, 'video/mp4')})
    else:
        http.post(tgt['url'])
    d = shopify_gql(http, """mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){
        files{ id fileStatus } userErrors{ field message } } }""",
                    {'files': [{'originalSource': tgt['resourceUrl'], 'contentType': 'VIDEO',
                                'alt': f'HOKO reel {mp4.parent.name}/{mp4.stem}'}]})['fileCreate']
    if d['userErrors']:
        raise RuntimeError(d['userErrors'])
    fid = d['files'][0]['id']
    for _ in range(60):
        n = shopify_gql(http, """query($id:ID!){ node(id:$id){ ... on Video { id fileStatus
            sources{ url mimeType height width } } } }""", {'id': fid})['node']
        if n['fileStatus'] == 'READY':
            mp4s = [s for s in n['sources'] if s['mimeType'] == 'video/mp4']
            best = max(mp4s, key=lambda s: s['height'])
            return best['url']
        if n['fileStatus'] == 'FAILED':
            raise RuntimeError(f'Shopify video processing failed: {fid}')
        time.sleep(0 if http.mocked else 10)
    raise RuntimeError(f'Shopify video not READY after 10 min: {fid}')


# ---------------------------------------------------------------- Instagram

def post_instagram(http, video_url, caption):
    uid, tok = os.environ.get('IG_USER_ID', 'MOCK_IG_USER'), os.environ.get('IG_ACCESS_TOKEN', 'mock')
    c = http.post(f'{GRAPH}/{uid}/media', data={'media_type': 'REELS', 'video_url': video_url,
                                                'caption': caption[:2200], 'share_to_feed': 'true',
                                                'access_token': tok})
    cid = c['id']
    for _ in range(60):
        s = http.get(f'{GRAPH}/{cid}', params={'fields': 'status_code', 'access_token': tok})
        if s['status_code'] == 'FINISHED':
            break
        if s['status_code'] in ('ERROR', 'EXPIRED'):
            raise RuntimeError(f'IG container {cid}: {s}')
        time.sleep(0 if http.mocked else 10)
    else:
        raise RuntimeError(f'IG container {cid} not FINISHED after 10 min')
    p = http.post(f'{GRAPH}/{uid}/media_publish', data={'creation_id': cid, 'access_token': tok})
    return p['id']


# ---------------------------------------------------------------- YouTube

def youtube_client():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if YT_TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(YT_TOKEN), YT_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            cid, sec = os.environ.get('YT_OAUTH_CLIENT_ID'), os.environ.get('YT_OAUTH_CLIENT_SECRET')
            if not cid or not sec:
                raise RuntimeError('YT_OAUTH_CLIENT_ID / YT_OAUTH_CLIENT_SECRET missing in .env')
            flow = InstalledAppFlow.from_client_config(
                {'installed': {'client_id': cid, 'client_secret': sec,
                               'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                               'token_uri': 'https://oauth2.googleapis.com/token',
                               'redirect_uris': ['http://localhost']}}, YT_SCOPES)
            creds = flow.run_local_server(port=0)   # opens a browser once; token cached after
        SECRETS.mkdir(exist_ok=True)
        YT_TOKEN.write_text(creds.to_json())
    return build('youtube', 'v3', credentials=creds, cache_discovery=False)


def yt_metadata(caption):
    lines = [l_ for l_ in caption.splitlines()]
    hook = lines[0].strip()
    title = (hook[:100 - len(' #Shorts')] + ' #Shorts')
    tags = [t.lstrip('#') for t in lines[-1].split() if t.startswith('#')]
    return title, caption, tags


def post_youtube(mp4, caption, mocked=False):
    title, desc, tags = yt_metadata(caption)
    body = {'snippet': {'title': title, 'description': desc[:4900], 'tags': tags[:15], 'categoryId': '22'},
            'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}}
    if mocked:
        return 'MOCK_YT_' + Path(mp4).parent.name, body
    from googleapiclient.http import MediaFileUpload
    yt = youtube_client()
    req = yt.videos().insert(part='snippet,status', body=body,
                             media_body=MediaFileUpload(str(mp4), mimetype='video/mp4', resumable=True))
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    return resp['id'], body


# ---------------------------------------------------------------- TikTok (manual)

def write_today(row, reel, caption, results):
    (ROOT / 'TODAY.md').write_text(f"""# Today's post — {row['date']}

**{row['item']}**

## TikTok (manual)
1. Open TikTok → + → Upload → pick `{reel}`
   (on the PC: `{(ROOT / reel).resolve()}`)
2. Paste the caption below. Post.

```
{caption.strip()}
```

## Auto-posted
{chr(10).join(f'- {k}: {v}' for k, v in results.items())}
""", encoding='utf-8')


# ---------------------------------------------------------------- main

def run(dry_run=False, when=None):
    print('RETIRED 17 Oct 2026: tools/social is the only poster. Remove the task: schtasks /Delete /TN "HOKO publish" /F')
    when = date.fromisoformat(when) if when else today()
    due = cal.next_due(when)
    if not due:
        log(f'publish {when}: nothing queued for today')
        return None
    idx, row = due
    reel = ROOT / row['reel']
    caption = (ROOT / row['caption']).read_text(encoding='utf-8')
    if not reel.exists():
        log(f'publish {row["date"]}: reel missing, rendering {row["reel"]}')
        from . import reel as reelmod
        kind, pid, h = Path(row['reel']).parts[-3], Path(row['reel']).parts[-2], int(Path(row['reel']).stem[1:])
        r = next(x for x in reelmod.load_rows(kind) if x['id'] == pid)
        reelmod.render(r, kind, h, reel)
    info = ffprobe(reel)
    http = MockHttp() if dry_run else Http()
    results = {}

    store, stoken = shopify_env()
    ig_ready = dry_run or (os.environ.get('IG_USER_ID') and os.environ.get('IG_ACCESS_TOKEN') and store and stoken)
    if ig_ready:
        try:
            url = upload_to_shopify_files(http, reel)
            results['Instagram'] = 'posted media ' + post_instagram(http, url, caption) + f' (video {url})'
        except Exception as e:
            results['Instagram'] = f'ERROR {e}'
    else:
        results['Instagram'] = 'NOT CONFIGURED (IG_USER_ID / IG_ACCESS_TOKEN / SHOPIFY_STORE / SHOPIFY_ADMIN_TOKEN)'

    yt_ready = dry_run or YT_TOKEN.exists() or (os.environ.get('YT_OAUTH_CLIENT_ID') and os.environ.get('YT_OAUTH_CLIENT_SECRET'))
    if yt_ready:
        try:
            vid, _ = post_youtube(reel, caption, mocked=dry_run)
            results['YouTube'] = f'posted https://youtube.com/shorts/{vid}'
        except Exception as e:
            results['YouTube'] = f'ERROR {e}'
    else:
        results['YouTube'] = 'NOT CONFIGURED (YT_OAUTH_CLIENT_ID / YT_OAUTH_CLIENT_SECRET)'
    results['TikTok'] = 'manual — see TODAY.md'

    ok = [k for k in ('Instagram', 'YouTube') if results[k].startswith('posted')]
    if len(ok) == 2:
        status = 'posted'
    elif ok:
        status = 'partial:' + '+'.join(ok)
    else:
        status = 'queued'          # nothing went out → stays in the queue, rolls to next run
    if dry_run:
        status = status.replace('posted', 'posted-dryrun') if status != 'queued' else status
    if status != 'queued':
        cal.set_status(idx, status)
    write_today(row, row['reel'], caption, results)
    log(f'publish {row["date"]} [{info["width"]}x{info["height"]} {info["duration"]:.1f}s] → {status} | '
        + ' | '.join(f'{k}: {v}' for k, v in results.items()))
    if dry_run:
        log(f'dry-run HTTP calls: {len(http.calls)} → ' + ', '.join(f'{m} {u}' for m, u in http.calls))
    return status, results


# ---------------------------------------------------------------- Windows Task Scheduler

TASK_NAME = 'HOKO publish'


def register_task(print_only=False):
    cmd_file = ROOT / 'hoko-publish.cmd'
    tr = f'"{cmd_file}"'
    args = ['schtasks', '/Create', '/TN', TASK_NAME, '/TR', tr, '/SC', 'DAILY', '/ST', '18:30', '/F']
    print('Task command:', ' '.join(a if ' ' not in a else f'"{a}"' for a in args))
    if print_only:
        return
    if platform.system() != 'Windows':
        raise SystemExit('Not Windows — run this on the PC: python content\\youtube\\run.py schedule')
    subprocess.run(args, check=True)
    q = subprocess.run(['schtasks', '/Query', '/TN', TASK_NAME], capture_output=True, text=True)
    print(q.stdout or q.stderr)
