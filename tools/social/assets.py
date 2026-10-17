"""Inventory of postable assets, built from what content/ already holds. No rendering, no network.

Clip assets (video, for IG / FB / YT / TikTok):
  content/youtube/reels/{sealed,slab}/<product_id>/h<k>.json   product reels (one per hook)
  content/youtube/reels/{tips,roundups,beats}/*.json            tip / ranked-roundup / BF + Christmas beat reels
  content/youtube/out/<video>/short_<n>.json                     Shorts cut from long-form (run.py shorts)
  content/carddrop/**/*.json, content/social-bank/**/*.json      CardDrop renders / social bank (sidecar json next to the mp4)
Image assets (for Pinterest + Discord): one per promotable product (first reel image) + key collection pages.

The .mp4 files are gitignored; `media` is the path the PC renders them to. The runner refuses to post
a clip whose mp4 is missing (topup renders them first on the PC).
"""

import csv
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

from .config import CONTENT, REPO, SITE, YT_CONTENT

GAME_NAMES = {'pokemon': 'Pokémon', 'onepiece': 'One Piece', 'dbs': 'Dragon Ball Super', 'mtg': 'Magic',
              'magic': 'Magic', 'lorcana': 'Lorcana', 'gundam': 'Gundam'}

TIP_LINKS = {
    'buyback': f'{SITE}/pages/sell-your-cards',
    'verified-graders': f'{SITE}/collections/graded-slabs',
    'spot-a-fake': f'{SITE}/collections/japan-direct-sealed',
    'no-outer-shrink': f'{SITE}/collections/japan-direct-sealed',
}
ROUNDUP_NAMES = {
    'mega-era': 'Every Mega-era Japanese box in stock',
    'one-piece': 'One Piece Japanese boxes in stock right now',
    'under-200': 'Japanese sealed boxes on a budget',
    'preorders': 'Pre-orders landing before Christmas',
}
ROUNDUP_LINKS = {
    'mega-era': f'{SITE}/collections/japan-direct-sealed',
    'one-piece': f'{SITE}/collections/japan-direct-sealed',
    'under-200': f'{SITE}/collections/japan-direct-sealed',
    'preorders': f'{SITE}/collections/japan-direct-sealed',
}
COLLECTION_PINS = [
    # (id, title, link, source product id for the image, game)
    ('japan-direct-sealed', 'Japanese sealed booster boxes', f'{SITE}/collections/japan-direct-sealed', None, 'pokemon'),
    ('graded-slabs', 'PSA, BGS and CGC graded slabs', f'{SITE}/collections/graded-slabs', 'slab', 'pokemon'),
    ('sell-your-cards', 'Sell your cards to HOKO', f'{SITE}/pages/sell-your-cards', None, 'pokemon'),
]


@dataclass
class Asset:
    id: str                    # stable, e.g. 'sealed/10734771798294/h1', 'pin/product/10734771798294'
    kind: str                  # sealed | slab | tip | roundup | beat | short | carddrop | bank | product | collection
    media_type: str            # video | image
    media: str = ''            # repo-relative mp4 path (video)
    image_url: str = ''        # public image (image assets; also cover for video)
    product_id: str = ''
    url: str = ''              # product / collection / page link
    name: str = ''             # short display name, e.g. 'Abyss Eye (M5) · no shrink'
    hook: str = ''             # on-screen hook, prices stripped
    game: str = 'pokemon'
    set_code: str = ''
    jp_sealed: bool = False
    eligible: bool = True
    reason: str = ''           # why not eligible
    pin_date: str = ''         # beats: only on this date
    extra: dict = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


PRICE_RE = re.compile(r'\s*(?:[—\-–·,]\s*)?(?:from\s+)?\$\s?\d[\d,]*(?:\.\d+)?\+?(?:\s*on HOKO)?', re.I)


def strip_prices(s):
    s = PRICE_RE.sub('', s or '')
    return re.sub(r'\s{2,}', ' ', s).strip(' ·—-,')


def short_name(title):
    t = re.sub(r'^\[PRE-ORDER\]\s*', '', title or '')
    t = re.sub(r'^(Pokemon|Pokémon|One Piece TCG|One Piece|Dragon Ball Super)\s+', '', t)
    no_shrink = 'No Outer Shrink' in t
    t = re.sub(r'\s*—\s*No Outer Shrink', '', t)
    t = re.sub(r'\s*—\s*Japanese$', '', t)
    t = re.sub(r'\s*(Sealed\s+)?Japanese\s+.*$', '', t).strip()
    t = re.sub(r'\s+Sealed$', '', t)
    return t + (' · no shrink' if no_shrink else '')


def _rows(folder):
    p = YT_CONTENT / folder / 'source.csv'
    if not p.exists():
        return {}
    with open(p, newline='', encoding='utf-8') as f:
        return {r['id']: r for r in csv.DictReader(f)}


def _flags(row):
    return set(filter(None, (row.get('flags') or '').split('|')))


def product_eligible(row):
    """Promotable = ACTIVE, not supplier-out-of-stock, and buyable: inventory > 0, or inventoryPolicy CONTINUE
    (import-to-order boxes in the live set sell at 0 stock since 17 Oct 2026)."""
    if not row:
        return False, 'no source row'
    if row.get('status') != 'ACTIVE':
        return False, f'status {row.get("status")}'
    fl = _flags(row)
    if 'OOS-SUPPLIER' in fl:
        return False, 'OOS-SUPPLIER'
    try:
        inv = int(float(row.get('inventory') or 0))
    except ValueError:
        inv = 0
    if inv <= 0 and (row.get('policy') or 'DENY').upper() != 'CONTINUE':   # DENY at 0 stock = sold out
        return False, 'inventory 0'
    return True, ''


def _first_image(row):
    imgs = (row.get('reel_images') or row.get('images') or '').split('|')
    return imgs[0] if imgs and imgs[0] else ''


def _read(p):
    try:
        return json.loads(Path(p).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def load(today=None):
    today = today or date.today()
    sealed, slabs = _rows('sealed'), _rows('slabs')
    out = []
    reels = YT_CONTENT / 'reels'

    for kind, rows in (('sealed', sealed), ('slab', slabs)):
        for j in sorted((reels / kind).glob('*/h*.json')):
            meta = _read(j)
            pid = j.parent.name
            row = rows.get(pid)
            ok, why = product_eligible(row)
            title = (row or {}).get('title') or meta.get('title', '')
            out.append(Asset(
                id=f'{kind}/{pid}/{j.stem}', kind=kind, media_type='video',
                media=str(j.with_suffix('.mp4').relative_to(REPO)).replace('\\', '/'),
                image_url=_first_image(row or {}), product_id=pid,
                url=(row or {}).get('url') or meta.get('url', ''),
                name=short_name(title) if kind == 'sealed' else ((row or {}).get('card') or title),
                hook=strip_prices(meta.get('hook', '')),
                game=(row or {}).get('game') or 'pokemon', set_code=(row or {}).get('set_code', ''),
                jp_sealed=kind == 'sealed', eligible=ok, reason=why,
                extra={'grader': (row or {}).get('grader', ''), 'grade': (row or {}).get('grade', ''),
                       'no_shrink': 'no-shrink' in _flags(row or {})}))

    for j in sorted((reels / 'tips').glob('*.json')):
        meta = _read(j)
        out.append(Asset(id=f'tip/{j.stem}', kind='tip', media_type='video',
                         media=str(j.with_suffix('.mp4').relative_to(REPO)).replace('\\', '/'),
                         url=TIP_LINKS.get(j.stem, f'{SITE}/collections/japan-direct-sealed'),
                         name=strip_prices(meta.get('hook', j.stem)), hook=strip_prices(meta.get('hook', '')),
                         game='pokemon', extra={'tip': j.stem}))

    preorders_live = any(r.get('status') == 'ACTIVE' and 'preorder' in _flags(r) for r in sealed.values())
    for j in sorted((reels / 'roundups').glob('*.json')):
        meta = _read(j)
        ok = j.stem != 'preorders' or preorders_live
        out.append(Asset(id=f'roundup/{j.stem}', kind='roundup', media_type='video',
                         media=str(j.with_suffix('.mp4').relative_to(REPO)).replace('\\', '/'),
                         url=ROUNDUP_LINKS.get(j.stem, f'{SITE}/collections/japan-direct-sealed'),
                         name=ROUNDUP_NAMES.get(j.stem, strip_prices(meta.get('hook', j.stem))),
                         hook=ROUNDUP_NAMES.get(j.stem, strip_prices(meta.get('hook', ''))),
                         game='onepiece' if j.stem == 'one-piece' else 'pokemon', jp_sealed=True,
                         eligible=ok, reason='' if ok else 'pre-order products still DRAFT',
                         extra={'roundup': j.stem}))

    for j in sorted((reels / 'beats').glob('*.json')):
        meta = _read(j)
        d = j.stem
        bf = d <= '2026-11-30' and 'cutoff' not in meta.get('voiceover', '').lower() and 'christmas' not in meta.get('voiceover', '').lower()
        # a beat is rendered around one featured box; if that box is no longer buyable the clip is stale
        feat = sealed.get(str(meta.get('product_id', '')))
        ok, why = product_eligible(feat) if feat else (False, 'not in sealed/source.csv (DRAFT or removed)')
        out.append(Asset(id=f'beat/{d}', kind='beat', media_type='video',
                         media=str(j.with_suffix('.mp4').relative_to(REPO)).replace('\\', '/'),
                         url=f'{SITE}/collections/japan-direct-sealed',   # every post links a product or the collection (17 Oct)
                         name=strip_prices(meta.get('hook', '')), hook=strip_prices(meta.get('hook', '')),
                         game='pokemon', jp_sealed=True, pin_date=d, product_id=str(meta.get('product_id', '')),
                         eligible=ok, reason='' if ok else f'featured box {why}; re-render with run.py calendar',
                         extra={'voiceover': strip_prices(meta.get('voiceover', '')), 'bf': bf}))

    # Shorts cut from long-form, CardDrop renders, social bank — sidecar json with hook/url/title/game
    for kind, pattern in (('short', 'youtube/out/*/short_*.json'), ('carddrop', 'carddrop/**/*.json'),
                          ('bank', 'social-bank/**/*.json')):
        for j in sorted(CONTENT.glob(pattern)):
            meta = _read(j)
            mp4 = j.with_suffix('.mp4')
            out.append(Asset(id=f'{kind}/{j.relative_to(CONTENT).with_suffix("")}'.replace('\\', '/'), kind=kind,
                             media_type='video', media=str(mp4.relative_to(REPO)).replace('\\', '/'),
                             url=meta.get('url') or f'{SITE}/collections/japan-direct-sealed',
                             name=strip_prices(meta.get('title') or meta.get('hook') or j.stem),
                             hook=strip_prices(meta.get('hook') or meta.get('title') or ''),
                             game=meta.get('game', 'pokemon'), jp_sealed=bool(meta.get('jp_sealed'))))

    # image assets: one per promotable product + collection pages
    for kind, rows in (('sealed', sealed), ('slab', slabs)):
        for pid, row in rows.items():
            ok, why = product_eligible(row)
            img = _first_image(row)
            if not img:
                ok, why = False, 'no image'
            out.append(Asset(id=f'product/{pid}', kind='product', media_type='image', image_url=img,
                             product_id=pid, url=row.get('url', ''),
                             name=short_name(row['title']) if kind == 'sealed' else (row.get('card') or row['title']),
                             game=row.get('game') or 'pokemon', set_code=row.get('set_code', ''),
                             jp_sealed=kind == 'sealed', eligible=ok, reason=why,
                             extra={'source': kind, 'grader': row.get('grader', ''), 'grade': row.get('grade', ''),
                                    'no_shrink': 'no-shrink' in _flags(row)}))
    first_ok = {k: next((_first_image(r) for r in rows.values() if product_eligible(r)[0] and _first_image(r)), '')
                for k, rows in (('sealed', sealed), ('slab', slabs))}
    for cid, title, link, src, game in COLLECTION_PINS:
        img = first_ok['slab' if src == 'slab' else 'sealed']
        out.append(Asset(id=f'collection/{cid}', kind='collection', media_type='image', image_url=img, url=link,
                         name=title, game=game, jp_sealed=cid == 'japan-direct-sealed', eligible=bool(img),
                         reason='' if img else 'no image', extra={'collection': cid}))
    return out


def by_id(assets):
    return {a.id: a for a in assets}


def is_hot(asset, hot_sets):
    """Newest-set push: product assets of a set in hot_sets (video reels, image pins, discord embeds)."""
    return bool(asset.set_code) and asset.set_code in set(hot_sets)
