"""calendar.md: one post per day 14 Oct → 24 Dec, queue-ordered, 2 sealed : 1 slab, plus fixed beats.

Queue semantics: rows are a queue, not fixed dates. `publish` always posts the FIRST row still
`queued` whose date <= today, so a missed day rolls forward instead of being skipped. Fixed beats
(BF / Christmas) are pinned (`pin` column) — publish skips a pinned row until its date.

Also writes CUTOFF.md and a dated caption per row in captions/YYYY-MM-DD.txt.
"""

import os
import re
from pathlib import Path
from datetime import date, timedelta

from . import reel
from .common import ROOT, SITE, config, dshort, dlong, set_name, flags, load_rows, price_str, rel, set_name, short_title

CAL = Path(os.environ.get('HOKO_CALENDAR') or ROOT / 'calendar.md')   # override for dry-run tests
CAPS = ROOT / 'captions'
HEADER = '| date | item | reel | caption | platforms | status | pin |'
SEP = '|---|---|---|---|---|---|---|'
PLATFORMS = 'IG, YT, TT(manual)'

# Release order, newest first (Pokémon JP M-series > SV; One Piece by set number).
# Used only for ordering the queue — not printed as a release date.
SET_RANK = ['M7', 'M6', 'M5', 'M4', 'M3', 'M2a', 'M2', 'M1S', 'M1L', 'sv10', 'sv9a', 'sv9', 'sv8a', 'sv8', 'sv7',
            'sv3a', 'sv3', 's12a',
            'OP-18', 'OP-17', 'OP-16', 'OP-15', 'OP-14', 'OP-13', 'PRB-02', 'OP-12', 'EB-04', 'OP-11', 'OP-10',
            'OP-07']


def rank(row):
    if reel.is_preorder(row):
        return -1
    sc = row.get('set_code', '')
    if 'newest-drop' in flags(row):
        return 0
    return SET_RANK.index(sc) + 1 if sc in SET_RANK else len(SET_RANK) + 1


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += timedelta(days=1)


def beats(cfg):
    """Fixed-date posts: {date: (label, kind_hint)}."""
    y = 2026
    cutoff = date.fromisoformat(cfg['christmas_cutoff'])
    return {
        date(y, 11, 1): 'BF box drop list open',
        date(y, 11, 20): 'BF countdown — 7 days',
        date(y, 11, 24): 'BF countdown — 3 days',
        date(y, 11, 26): 'BF countdown — tomorrow',
        date(y, 11, 27): "It's live — BF: free AU post on every sealed box 27–30 Nov",
        cutoff - timedelta(days=7): f'Christmas cutoff reel — order sealed by {dshort(cutoff)}',
    }


def beat_hook(label, cfg):
    """(on-screen hook, voiceover, body lines, tag) for a beat reel."""
    cutoff = date.fromisoformat(cfg['christmas_cutoff'])
    if label.startswith('BF box drop list'):
        return ('BF box drop list is open',
                'The Black Friday box drop list is open. Five dollars off any Japanese box, and you hear first on '
                'the twenty seventh. Link in bio.',
                ['$5 off boxes', 'Join at the link in bio', 'List hears first · 27 Nov'], 'BLACK FRIDAY')
    if label.startswith('BF countdown'):
        n = label.split('— ')[1]
        return (f'Black Friday: {n}',
                f'Black Friday, {n}. Free postage on every sealed box, the twenty seventh to the thirtieth of '
                f'November. Link in bio.',
                ['Free AU post on every box', '27 – 30 Nov', 'List: $5 off · link in bio'], 'BLACK FRIDAY')
    if label.startswith("It's live"):
        return ("It's live", "It's live. Black Friday at HOKO. Free postage on every sealed box until Monday. "
                "List members, your five dollar code is in your inbox. Link in bio.",
                ['Free AU post on every box', 'Until Mon 30 Nov', 'hokocollectables.com'], 'BLACK FRIDAY')
    return (f'Christmas cutoff: order sealed by {dshort(cutoff)}',
            f'Christmas cutoff. Order sealed boxes by {cutoff:%A} the {_ord(cutoff.day)} of {cutoff:%B} '
            f'to have them for Christmas. Slabs ship in one to three days. Link in bio.',
            [f'Sealed: order by {dshort(cutoff)}', 'Slabs: ship in 1–3 days', 'hokocollectables.com'], 'CHRISTMAS')


def _ord(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


# Tip reels: text over a blurred product photo, copy taken from the live product descriptions / policies.
TIPS = [
    ('spot-a-fake', 'How to spot a fake Japanese box',
     'How to spot a fake Japanese box. Printed shrink, one clean seal. Clear wrap or a double seam is a red flag. '
     'Not sure? Send us a photo before you open it.',
     ['Printed shrink, one clean seal', 'Clear wrap / double seam = red flag', 'Same set code on every pack',
      'Unsure? DM a photo first']),
    ('no-outer-shrink', 'What "no outer shrink" means',
     'What does no outer shrink mean? The box is still factory sealed, the printed film is just removed. '
     'Same packs, lower price.',
     ['Box is still factory sealed', 'Outer film removed, packs untouched', 'Same product, lower price']),
    ('verified-graders', 'Why we only buy PSA, BGS and CGC',
     'Why only PSA, BGS and CGC? The cert checks online and the pop reports are public. '
     'If you cannot verify it, walk away.',
     ['Cert checks online', 'Public pop reports', "Can't verify it? Walk away"]),
    ('buyback', 'Selling a collection? Here is how we buy',
     'Selling a collection? We buy sealed and PSA, BGS or CGC slabs. One photo and a list '
     'gets you a quote in forty eight hours. Link in bio.',
     ['Sealed + graded slabs', 'One photo + a list → quote in 48 hrs', 'Bank transfer on the day']),
]


# Roundup reels: ranked multi-product lists (honest, useful, and they sell boxes). One a week.
def roundups(cfg):
    rows = load_rows('sealed')
    live = [r for r in rows if r['status'] == 'ACTIVE' and 'OOS-SUPPLIER' not in flags(r)
            and int(float(r['inventory'] or 0)) > 0]
    by_price = lambda rs: sorted(rs, key=lambda r: float(r['price']))
    pre = [r for r in rows if reel.is_preorder(r) and r.get('release_date')
           and r['release_date'] <= cfg['calendar_end']]
    out = [
        ('mega-era', 'Every Mega-era box in stock, cheapest first', 'IN STOCK NOW',
         by_price([r for r in live if r['game'] == 'pokemon' and r.get('set_code', '').startswith('M')])[:4]),
        ('one-piece', 'One Piece JP boxes in stock right now', 'IN STOCK NOW',
         by_price([r for r in live if r['game'] == 'onepiece'])[:4]),
        ('under-200', 'Cheapest Japanese sealed in stock', 'IN STOCK NOW',
         by_price([r for r in live if float(r['price']) < 200])[:4]),
        ('preorders', 'Pre-orders landing before Christmas', 'PRE-ORDER',
         sorted(pre, key=lambda r: r['release_date'])[:4]),
    ]
    return [r for r in out if r[3]]


# spoken opener where it differs from the on-screen title
SPOKEN_HOOK = {'under-200': 'The cheapest Japanese sealed in stock right now'}


def roundup_vo(hook, items, pre=False):
    # no prices in the voiceover, the frame or the caption (Ethan 17 Oct 2026)
    parts = []
    for it in items:
        name = set_name(it)
        if pre:
            rd = date.fromisoformat(it['release_date'])
            parts.append(f'{name}, {rd.day} {rd:%B}')
        else:
            parts.append(name)
    return f'{hook}. ' + '. '.join(parts) + '. Link in bio.'


def roundup_caption(hook, items, pre=False):
    lines = [hook, '']
    for i, it in enumerate(items, 1):
        extra = f' · JP release {dshort(date.fromisoformat(it["release_date"]))}' if pre else ''
        lines.append(f'{i}. {short_title(it)}{extra}\n   {it["url"]}')
    lines += ['', 'All sealed, all tracked from Victoria. Free AU post on sealed boxes.',
              '', 'Collector first. Seller second.', '',
              ' '.join(reel.hashtags(items[0], 'sealed'))]
    return '\n'.join(lines) + '\n'


def tip_caption(tip, row):
    key, hook, vo, body = tip
    tags = ' '.join(reel.hashtags(row, 'sealed')[:-4] + ['#tcgtips', '#collectortips', '#tcgaustralia',
                                                         '#hokocollectables'])
    extra = {'buyback': f"\n\nSell to HOKO: {SITE}/pages/sell-your-cards",
             'verified-graders': f"\n\nSlabs in stock: {SITE}/collections/graded-slabs"}.get(key, '')
    return f"{hook}\n\n" + '\n'.join(f'• {b}' for b in body) + extra + \
        f"\n\nCollector first. Seller second.\n\n{tags}\n"


def beat_caption(label, row, cfg):
    cutoff = date.fromisoformat(cfg['christmas_cutoff'])
    url = cfg.get('bf_list_url') or '{{BF_LIST_URL}}'
    s = short_title(row)
    tags = ' '.join(reel.hashtags(row, 'sealed'))
    co = dshort(cutoff)
    if label.startswith('BF box drop list'):
        body = (f"BF box drop list is open.\n\nJoin the BF box drop list — $5 off boxes {url}\n"
                f"List members hear first when the Black Friday boxes go up on 27 Nov.\n\n"
                f"Featured: {s}. {row['url']}")
    elif label.startswith('BF countdown'):
        n = label.split('— ')[1]
        body = (f"Black Friday: {n}.\n\nFree AU post on every sealed box, 27–30 Nov.\n"
                f"Join the BF box drop list — $5 off boxes {url}\n\nFeatured: {s}. {row['url']}")
    elif label.startswith("It's live"):
        body = (f"It's live. Black Friday at HOKO.\n\nFree AU post on every sealed box, 27–30 Nov.\n"
                f"Christmas delivery on sealed imports: order by {co}.\n\n{s}. {row['url']}")
    else:
        body = (f"Christmas cutoff: order sealed by {co}.\n\nJapanese sealed is imported to order — "
                f"after {co} we can't promise it lands before Christmas.\n"
                f"Slabs ship from Victoria in 1–3 business days.\n\n{s}. {row['url']}")
    return f"{body}\n\nCollector first. Seller second.\n\n{tags}\n"


def build(log=print, render_beats=True):
    cfg = config()
    start, end = date.fromisoformat(cfg['calendar_start']), date.fromisoformat(cfg['calendar_end'])
    sealed = sorted([r for r in load_rows('sealed') if reel.promotable(r, 'sealed')], key=rank)
    hot = [r for r in sealed if r.get('set_code') in cfg['hot_sets'] or 'newest-drop' in flags(r)]
    filler = [r for r in sealed if r not in hot]
    # hot sets (Mega era, VSTAR, Terastal, newest One Piece) take `hot_share` slots per filler slot
    def weighted():
        hi, fi, n = 0, 0, 0
        while True:
            if filler and n % (cfg['hot_share'] + 1) == cfg['hot_share']:
                yield filler[fi % len(filler)]
                fi += 1
            else:
                yield hot[hi % len(hot)]
                hi += 1
            n += 1
    sealed = weighted()
    slabs = sorted(load_rows('slab'), key=lambda r: -float(r['price']))

    # rotation queues of (row, hook) — every item once per pass, hook index advances per pass
    def cycle(rows, kind):
        passes = 0
        while True:
            for r in rows:
                hooks = reel.eligible_hooks(r, kind)
                yield r, hooks[passes % len(hooks)]
            passes += 1

    def cycle_weighted(gen, kind):
        seen = {}
        for r in gen:
            hooks = reel.eligible_hooks(r, kind)
            k = seen.get(r['id'], 0)
            seen[r['id']] = k + 1
            yield r, hooks[k % len(hooks)]

    sq, lq = cycle_weighted(sealed, 'sealed'), cycle(slabs, 'slab')
    fixed = beats(cfg)
    CAPS.mkdir(exist_ok=True)
    rows_out, missing = [], []
    cutoff = date.fromisoformat(cfg['christmas_cutoff'])
    rups = roundups(cfg)
    i, tip_i, rup_i = 0, 0, 0
    for d in daterange(start, end):
        if d in fixed:
            label = fixed[d]
            r, k = next(sq)   # beats feature a sealed box
            kind, item, pin = 'sealed', f'**{label}** · {short_title(r)} {price_str(r["price"])}', 'yes'
            cap = beat_caption(label, r, cfg)
        elif (d - start).days % 7 == 3 and rups:
            key, rhook, rtag, items = rups[rup_i % len(rups)]
            rup_i += 1
            r, k, kind, pin = items[0], 1, 'roundup', ''
            item = f'**Roundup: {rhook}**'
            cap = roundup_caption(rhook, items, pre=(key == 'preorders'))
            rup = (key, rhook, rtag, items)
        elif (d - start).days % 7 == 6:
            # one Tip reel a week (CLAUDE.md pillar "The Tip") — text over a product photo
            tip = TIPS[tip_i % len(TIPS)]
            tip_i += 1
            r, k = next(sq)
            kind, item, pin = 'tip', f'**Tip: {tip[1]}**', ''
            cap = tip_caption(tip, r)
        else:
            pattern = ['sealed', 'sealed', 'slab']
            kind = pattern[i % len(pattern)]
            i += 1
            r, k = next(sq) if kind == 'sealed' else next(lq)
            while kind == 'sealed' and reel.is_preorder(r) and r.get('release_date') and \
                    date.fromisoformat(r['release_date']) < d:
                r, k = next(sq)   # pre-order already released — skip until `run.py source` re-tags it
            item = (f'{short_title(r)} {price_str(r["price"])}' if kind == 'sealed'
                    else f'{r["card"]} {r["grader"]} {r["grade"]} {price_str(r["price"])}')
            item += f' · h{k}'
            pin = ''
            cap = reel.caption_text(r, kind, k, when=d)
        rp = reel.reel_path(kind, r['id'], k)
        if pin:
            rp = reel.REELS / 'beats' / f'{d.isoformat()}.mp4'
            if render_beats:
                hook, vo, body, tag = beat_hook(fixed[d], cfg)
                m = reel.render(r, 'sealed', k, rp, override=(hook, vo), body=body, tag=tag)
                log(f"  beat {d} {m['duration']}s {m['reel']}")
        elif kind == 'roundup':
            rp = reel.REELS / 'roundups' / f'{rup[0]}.mp4'
            if render_beats:
                m = reel.render(r, 'sealed', k, rp, override=(rup[1], roundup_vo(SPOKEN_HOOK.get(rup[0], rup[1]), rup[3], rup[0] == 'preorders')),
                                tag=rup[2], items=rup[3])
                log(f"  roundup {rup[0]} {m['duration']}s {m['reel']}")
        elif kind == 'tip':
            rp = reel.REELS / 'tips' / f'{tip[0]}.mp4'
            if render_beats:
                m = reel.render(r, 'sealed', k, rp, override=(tip[1], tip[2]), body=tip[3], tag='THE TIP')
                log(f"  tip {tip[0]} {m['duration']}s {m['reel']}")
        if not rp.exists():
            missing.append(rel(rp))
        cp = CAPS / f'{d.isoformat()}.txt'
        cp.write_text(cap, encoding='utf-8')
        drafts = [x for x in (rup[3] if kind == 'roundup' else [r]) if x.get('status', 'ACTIVE') != 'ACTIVE']
        status = 'blocked:draft-product' if drafts else 'queued'
        rows_out.append(f'| {d.isoformat()} | {item} | {rel(rp)} | {rel(cp)} | {PLATFORMS} | {status} | {pin} |')

    # keep status of rows already posted
    old = {}
    if CAL.exists():
        for line in CAL.read_text(encoding='utf-8').splitlines():
            c = parse_row(line)
            if c and c['status'].split(':')[0] in ('posted', 'posted-dryrun', 'partial', 'missed'):
                old[c['date']] = line
    rows_out = [old.get(parse_row(l)['date'], l) for l in rows_out]

    cutoff = date.fromisoformat(cfg['christmas_cutoff'])
    head = f"""# HOKO content calendar — {start.day} {start:%b} → {end.day} {end:%b %Y}

One post per day, queue-ordered: `run.py publish` posts the first `queued` row dated today or earlier,
so a missed day rolls forward. Rows with `pin = yes` are fixed beats and wait for their date.
Mix: 2 sealed : 1 slab. Hot sets (`hot_sets` in config.json — Mega era, VSTAR, Terastal, newest One Piece) take 3 of every 4 sealed slots; older sets fill the rest. OOS-SUPPLIER boxes are left out.

- **Christmas cutoff (sealed imports):** order by **{dlong(cutoff)}** — see CUTOFF.md
- **BF:** list opens 1 Nov · countdown 20 / 24 / 26 Nov · live 27 Nov (free AU post on every sealed box 27–30 Nov)
- **TikTok** is manual — `publish` writes TODAY.md with the reel + caption.
- `blocked:draft-product` = the Shopify product is still a draft (no public page to link). Publish it in Shopify,
  then `run.py source` + `run.py calendar` and the row goes back to `queued`. `publish` skips blocked rows.
- Regenerate: `python content/youtube/run.py calendar` (keeps posted rows).

{HEADER}
{SEP}
"""
    CAL.write_text(head + '\n'.join(rows_out) + '\n', encoding='utf-8')
    write_cutoff(cfg)
    log(f'calendar.md: {len(rows_out)} rows, {len(missing)} missing reels')
    return rows_out, missing


def write_cutoff(cfg):
    lt = cfg['lead_time_days']
    cutoff = date.fromisoformat(cfg['christmas_cutoff'])
    dl = cfg['auspost_deadlines_from_vic']
    lines = '\n'.join(f'| {s} | {dshort(date.fromisoformat(v))} | '
                      f'{dshort(date.fromisoformat(v) - timedelta(days=lt))} |' for s, v in dl.items())
    (ROOT / 'CUTOFF.md').write_text(f"""# Christmas 2026 delivery cutoff — sealed imports

**Order by: {dlong(cutoff)}** (used in captions, calendar and Shopify descriptions)

## How it's worked out
- Lead time Japan → Victoria → buyer: **{lt} days** — {cfg['lead_time_source']}
- AusPost Parcel Post send-by from VIC metro to NSW/ACT/QLD/SA/TAS: **Mon 21 Dec 2026** — {cfg['auspost_source']}
- Cutoff = AusPost send-by − full lead time = 21 Dec − {lt} days = **{dshort(cutoff)}**.
  Conservative on purpose: it assumes the whole {lt} days is used before the box is lodged in Victoria,
  so anything ordered by the cutoff is on hand before AusPost's last parcel date.
- Graded slabs are already in Victoria — normal AusPost dates apply, no import lead time.

## Per-state (order-by = AusPost send-by − {lt} days)
| state | AusPost Parcel Post send-by (from VIC) | order sealed by |
|---|---|---|
{lines}

WA ({dshort(date.fromisoformat(dl['WA']) - timedelta(days=lt))}) and NT ({dshort(date.fromisoformat(dl['NT']) - timedelta(days=lt))}) are earlier than the headline date.
Shopify copy uses the headline date; mention WA/NT in DMs if asked.

## Conflict to check
The live Shipping & Returns page says Japanese sealed is "imported and dispatched tracked from Victoria
within 2–4 business days". If that's true for in-stock boxes, the real cutoff is later (≈ AusPost dates).
Update `christmas_cutoff` in config.json and re-run `run.py calendar` if the lead time changes.
""", encoding='utf-8')


ROW_RE = re.compile(r'^\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)\|$')


def parse_row(line):
    m = ROW_RE.match(line.strip())
    if not m:
        return None
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) < 7:
        return None
    return dict(zip(['date', 'item', 'reel', 'caption', 'platforms', 'status', 'pin'], cells))


def read():
    return [(i, parse_row(l)) for i, l in enumerate(CAL.read_text(encoding='utf-8').splitlines()) if parse_row(l)]


def next_due(when):
    """What to post on `when`.

    1. A pinned beat dated `when` wins.
    2. Pinned beats whose date has passed unposted are marked `missed` (stale BF countdowns etc.).
    3. Otherwise the first queued, unpinned row dated <= `when` (missed days roll forward).
    """
    rows = read()
    for i, r in rows:
        if r['status'] == 'queued' and r['pin'] == 'yes' and date.fromisoformat(r['date']) == when:
            return i, r
    for i, r in rows:
        if r['status'] == 'queued' and r['pin'] == 'yes' and date.fromisoformat(r['date']) < when:
            set_status(i, 'missed')
    rows = read()
    for i, r in rows:
        if r['status'] == 'queued' and r['pin'] != 'yes' and date.fromisoformat(r['date']) <= when:
            return i, r
    # today's row is blocked (draft product) → pull the next queued row forward so the day isn't lost
    if any(r['status'].startswith('blocked') and date.fromisoformat(r['date']) <= when for _, r in rows):
        for i, r in rows:
            if r['status'] == 'queued' and r['pin'] != 'yes':
                return i, r
    return None


def set_status(line_idx, status):
    lines = CAL.read_text(encoding='utf-8').splitlines()
    cells = [c.strip() for c in lines[line_idx].strip().strip('|').split('|')]
    cells[5] = status
    lines[line_idx] = '| ' + ' | '.join(cells) + ' |'
    CAL.write_text('\n'.join(lines) + '\n', encoding='utf-8')
