"""run.py comments — pull YouTube comment threads on the last 10 uploads → comments/queue.md.

Each comment gets a drafted reply in Ethan's voice (casual Aussie collector, short, not salesy unless
they asked about buying) and an `APPROVE [ ]` box. Tick it (`[x]`), edit the draft if you like, then
`run.py comments --post` posts ONLY ticked replies and marks them POSTED. Nothing posts automatically.
"""

import re
from datetime import datetime

from .common import ROOT

QUEUE = ROOT / 'comments' / 'queue.md'

BUY = re.compile(r'\b(price|how much|cost|available|still got|still have|for sale|sell|buy|ship|postage|'
                 r'shipping|link|where.*get|stock|pre-?order|restock)\b', re.I)
PRAISE = re.compile(r'(🔥|💯|😍|🤩|\b(sick|insane|love|nice|awesome|beautiful|clean|fire|mint|great|cool|banger)\b)', re.I)
PULL = re.compile(r'\b(pull(ed)?|hit|chase|opened|rip(ped)?|box break)\b', re.I)
GRADE = re.compile(r'\b(psa|bgs|cgc|tag|grade|graded|grading|slab|centering|surface)\b', re.I)


def draft_reply(text, author):
    name = (author or '').lstrip('@').split()[0] if author else ''
    hi = f'{name}' if name and len(name) <= 20 else 'mate'
    if BUY.search(text):
        return (f"Cheers {hi}! Yep — it's up on hokocollectables.com, ships tracked from Victoria. "
                f"Flick us a DM if you've got questions.")
    if '?' in text and GRADE.search(text):
        return f"Good q {hi} — [FILL IN: answer]. Might do a proper video on grading this one."
    if '?' in text:
        return f"Good question {hi} — [FILL IN: answer]."
    if PULL.search(text):
        return f"Haha love it {hi}. What's the best thing you've pulled from it?"
    if PRAISE.search(text):
        return f"Cheers {hi}, appreciate it 🤙"
    return f"Cheers for watching {hi} 🤙"


# ---------------------------------------------------------------- fetch

def _mock_threads():
    """Shaped like commentThreads.list items (snippet + replies)."""
    def t(tid, vid, author, text, likes, owner_replied=False):
        item = {'id': tid, 'snippet': {'videoId': vid, 'canReply': True, 'totalReplyCount': int(owner_replied),
                'topLevelComment': {'snippet': {'authorDisplayName': author, 'textOriginal': text,
                                                'likeCount': likes, 'publishedAt': '2026-10-12T09:00:00Z',
                                                'authorChannelId': {'value': 'UCviewer'}}}}}
        if owner_replied:
            item['replies'] = {'comments': [{'snippet': {'authorChannelId': {'value': 'UCHOKO'}}}]}
        return item
    vids = {'vid001': 'Abyss Eye box opening #Shorts', 'vid002': 'PSA 10 Pikachu — what\'s it worth? #Shorts'}
    threads = [
        t('Ugx1', 'vid001', '@mattcollects', 'How much for the box? Do you ship to WA?', 12),
        t('Ugx2', 'vid001', '@pokefan_au', 'Is Abyss Eye better value than Nihil Zero for pulls?', 30),
        t('Ugx3', 'vid002', '@slabhunter', 'Would you crack it and resub to BGS?', 22),
        t('Ugx4', 'vid002', '@jess', 'That centering is insane 🔥', 5),
        t('Ugx5', 'vid001', '@tom', 'pulled the SAR from this set last week!', 3),
        t('Ugx6', 'vid002', '@already', 'Great vid', 1, owner_replied=True),
    ]
    return vids, threads, 'UCHOKO'


def _live_threads():
    from .publish import youtube_client
    yt = youtube_client()
    ch = yt.channels().list(part='id,contentDetails', mine=True).execute()['items'][0]
    me, uploads = ch['id'], ch['contentDetails']['relatedPlaylists']['uploads']
    items = yt.playlistItems().list(part='snippet,contentDetails', playlistId=uploads, maxResults=10).execute()['items']
    vids = {i['contentDetails']['videoId']: i['snippet']['title'] for i in items}
    threads = []
    for vid in vids:
        try:
            r = yt.commentThreads().list(part='snippet,replies', videoId=vid, maxResults=50,
                                         order='relevance', textFormat='plainText').execute()
            threads += r.get('items', [])
        except Exception as e:   # comments disabled etc.
            print(f'  skip {vid}: {e.__class__.__name__}')
    return vids, threads, me


# ---------------------------------------------------------------- queue.md

ENTRY_RE = re.compile(r'<!-- thread:(?P<id>[^ ]+) -->\n(?P<body>.*?)(?=\n<!-- thread:|\n## |\Z)', re.S)


def existing_ids():
    return set(re.findall(r'<!-- thread:([^ ]+) -->', QUEUE.read_text(encoding='utf-8'))) if QUEUE.exists() else set()


def pull(dry_run=False):
    vids, threads, me = _mock_threads() if dry_run else _live_threads()
    seen = existing_ids()
    new, questions = [], []
    for th in threads:
        s = th['snippet']
        top = s['topLevelComment']['snippet']
        if top.get('authorChannelId', {}).get('value') == me or not s.get('canReply', True):
            continue
        replies = th.get('replies', {}).get('comments', [])
        if any(r['snippet'].get('authorChannelId', {}).get('value') == me for r in replies):
            continue
        text = top['textOriginal'].strip()
        if '?' in text:
            questions.append((top.get('likeCount', 0), text, vids.get(s['videoId'], s['videoId'])))
        if th['id'] in seen:
            continue
        new.append((th['id'], vids.get(s['videoId'], s['videoId']), top['authorDisplayName'], text,
                    top.get('likeCount', 0), draft_reply(text, top['authorDisplayName'])))

    out = [] if QUEUE.exists() else ['# YouTube comment queue\n',
                                    'Tick `APPROVE [x]` (edit the draft first if needed), then run '
                                    '`python content/youtube/run.py comments --post`. Only ticked replies post.\n']
    if new:
        out.append(f'\n## Pulled {datetime.now():%Y-%m-%d %H:%M}{" (DRY-RUN / mocked)" if dry_run else ""}\n')
        for tid, vt, au, tx, likes, dr in new:
            quoted = tx.replace('\n', '\n> ')
            out.append(f'\n<!-- thread:{tid} -->\n**{vt}** · {au} · 👍 {likes}\n> {quoted}\n\n'
                       f'Reply: {dr}\n\nAPPROVE [ ]\n')
    questions.sort(reverse=True)
    if questions:
        out.append('\n### Next-topic suggestions (top questions by likes)\n')
        for likes, tx, vt in questions[:3]:
            out.append(f'- "{tx}" — {vt} (👍 {likes})\n')
    QUEUE.parent.mkdir(exist_ok=True)
    with open(QUEUE, 'a', encoding='utf-8') as f:
        f.write(''.join(out))
    print(f'comments: {len(new)} new thread(s) → {QUEUE.relative_to(ROOT)}; top questions: {min(3, len(questions))}')
    return new, questions[:3]


def post_approved(dry_run=False):
    text = QUEUE.read_text(encoding='utf-8')
    todo = []
    for m in ENTRY_RE.finditer(text):
        body = m.group('body')
        if re.search(r'APPROVE \[[xX]\]', body) and 'POSTED' not in body:
            reply = re.search(r'^Reply: (.+)$', body, re.M).group(1).strip()
            if '[FILL IN' in reply:
                print(f'  skip {m.group("id")}: draft still has [FILL IN]')
                continue
            todo.append((m.group('id'), reply))
    yt = None if dry_run else __import__('hoko.publish', fromlist=['x']).youtube_client()
    for tid, reply in todo:
        if dry_run:
            cid = f'MOCK_{tid}'
        else:
            cid = yt.comments().insert(part='snippet', body={'snippet': {'parentId': tid,
                                                                         'textOriginal': reply}}).execute()['id']
        text = re.sub(rf'(<!-- thread:{re.escape(tid)} -->.*?)APPROVE \[[xX]\]',
                      lambda mm: mm.group(1) + f'APPROVE [x] POSTED {datetime.now():%Y-%m-%d} ({cid})',
                      text, count=1, flags=re.S)
        print(f'  posted reply to {tid}')
    QUEUE.write_text(text, encoding='utf-8')
    print(f'comments --post: {len(todo)} reply(ies) posted')
    return todo


def run(post=False, dry_run=False):
    return post_approved(dry_run) if post else pull(dry_run)
