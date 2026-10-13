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
from .common import ROOT, config, dshort, dlong, flags, load_rows, price_str, rel, set_name, short_title

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
    """(on-screen hook, voiceover) for a beat reel."""
    cutoff = date.fromisoformat(cfg['christmas_cutoff'])
    if label.startswith('BF box drop list'):
        return ('BF box drop list is open',
                'The Black Friday box drop list is open. Join for five dollars off boxes. Link in bio.')
    if label.startswith('BF countdown'):
        n = label.split('— ')[1]
        return (f'Black Friday: {n}',
                f'Black Friday, {n}. Free postage on every sealed box, the twenty seventh to the thirtieth of '
                f'November. Link in bio.')
    if label.startswith("It's live"):
        return ("It's live — free post on every sealed box",
                "It's live. Black Friday at HOKO. Free postage on every sealed box until Monday. Link in bio.")
    return (f'Christmas cutoff: order sealed by {dshort(cutoff)}',
            f'Christmas cutoff. Order sealed boxes by {cutoff:%A} the {cutoff.day}{'th' if 10 <= cutoff.day % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(cutoff.day % 10, 'th')} of {cutoff:%B} '
            f'to have them for Christmas. Link in bio.')


def beat_caption(label, row, cfg):
    cutoff = date.fromisoformat(cfg['christmas_cutoff'])
    url = cfg.get('bf_list_url') or '{{BF_LIST_URL}}'
    s, p = short_title(row), price_str(row['price'])
    tags = ' '.join(reel.hashtags(row, 'sealed'))
    co = dshort(cutoff)
    if label.startswith('BF box drop list'):
        body = (f"BF box drop list is open.\n\nJoin the BF box drop list — $5 off boxes {url}\n"
                f"List members hear first when the Black Friday boxes go up on 27 Nov.\n\n"
                f"Featured: {s} — {p}. {row['url']}")
    elif label.startswith('BF countdown'):
        n = label.split('— ')[1]
        body = (f"Black Friday: {n}.\n\nFree AU post on every sealed box, 27–30 Nov.\n"
                f"Join the BF box drop list — $5 off boxes {url}\n\nFeatured: {s} — {p}. {row['url']}")
    elif label.startswith("It's live"):
        body = (f"It's live. Black Friday at HOKO.\n\nFree AU post on every sealed box, 27–30 Nov.\n"
                f"Christmas delivery on sealed imports: order by {co}.\n\n{s} — {p}. {row['url']}")
    else:
        body = (f"Christmas cutoff: order sealed by {co}.\n\nJapanese sealed is imported to order — "
                f"after {co} we can't promise it lands before Christmas.\n"
                f"Slabs ship from Victoria in 1–3 business days.\n\n{s} — {p}. {row['url']}")
    return f"{body}\n\nCollector first. Seller second.\n\n{tags}\n"


def build(log=print, render_beats=True):
    cfg = config()
    start, end = date.fromisoformat(cfg['calendar_start']), date.fromisoformat(cfg['calendar_end'])
    sealed = sorted([r for r in load_rows('sealed') if reel.promotable(r, 'sealed')], key=rank)
    slabs = sorted(load_rows('slab'), key=lambda r: -float(r['price']))

    # rotation queues of (row, hook) — every item once per pass, hook index advances per pass
    def cycle(rows, kind):
        passes = 0
        while True:
            for r in rows:
                hooks = reel.eligible_hooks(r, kind)
                yield r, hooks[passes % len(hooks)]
            passes += 1

    sq, lq = cycle(sealed, 'sealed'), cycle(slabs, 'slab')
    fixed = beats(cfg)
    CAPS.mkdir(exist_ok=True)
    rows_out, missing = [], []
    pattern = ['sealed', 'sealed', 'slab']
    i = 0
    for d in daterange(start, end):
        if d in fixed:
            label = fixed[d]
            r, k = next(sq)   # beats feature a sealed box
            kind, item, pin = 'sealed', f'**{label}** · {short_title(r)} {price_str(r["price"])}', 'yes'
            cap = beat_caption(label, r, cfg)
        else:
            kind = pattern[i % 3]
            i += 1
            r, k = next(sq) if kind == 'sealed' else next(lq)
            item = (f'{short_title(r)} {price_str(r["price"])}' if kind == 'sealed'
                    else f'{r["card"]} {r["grader"]} {r["grade"]} {price_str(r["price"])}')
            item += f' · h{k}'
            pin = ''
            cap = reel.caption_text(r, kind, k, when=d)
        rp = reel.reel_path(kind, r['id'], k)
        if pin:
            rp = reel.REELS / 'beats' / f'{d.isoformat()}.mp4'
            if render_beats:
                m = reel.render(r, 'sealed', k, rp, override=beat_hook(fixed[d], cfg))
                log(f"  beat {d} {m['duration']}s {m['reel']}")
        if not rp.exists():
            missing.append(rel(rp))
        cp = CAPS / f'{d.isoformat()}.txt'
        cp.write_text(cap, encoding='utf-8')
        rows_out.append(f'| {d.isoformat()} | {item} | {rel(rp)} | {rel(cp)} | {PLATFORMS} | queued | {pin} |')

    # keep status of rows already posted
    old = {}
    if CAL.exists():
        for line in CAL.read_text(encoding='utf-8').splitlines():
            c = parse_row(line)
            if c and c['status'] != 'queued':
                old[c['date']] = line
    rows_out = [old.get(parse_row(l)['date'], l) for l in rows_out]

    cutoff = date.fromisoformat(cfg['christmas_cutoff'])
    head = f"""# HOKO content calendar — {start.day} {start:%b} → {end.day} {end:%b %Y}

One post per day, queue-ordered: `run.py publish` posts the first `queued` row dated today or earlier,
so a missed day rolls forward. Rows with `pin = yes` are fixed beats and wait for their date.
Mix: 2 sealed : 1 slab, newest sets first. Sealed items tagged OOS-SUPPLIER are left out.

- **Christmas cutoff (sealed imports):** order by **{dlong(cutoff)}** — see CUTOFF.md
- **BF:** list opens 1 Nov · countdown 20 / 24 / 26 Nov · live 27 Nov (free AU post on every sealed box 27–30 Nov)
- **TikTok** is manual — `publish` writes TODAY.md with the reel + caption.
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
    for i, r in read():
        if r['status'] == 'queued' and r['pin'] != 'yes' and date.fromisoformat(r['date']) <= when:
            return i, r
    return None


def set_status(line_idx, status):
    lines = CAL.read_text(encoding='utf-8').splitlines()
    cells = [c.strip() for c in lines[line_idx].strip().strip('|').split('|')]
    cells[5] = status
    lines[line_idx] = '| ' + ' | '.join(cells) + ' |'
    CAL.write_text('\n'.join(lines) + '\n', encoding='utf-8')
