"""Caption writer — templates written for HOKO in-session, filled from asset metadata. No API calls.

Canon: "Collector first. Seller second." · games Magic · Pokémon · One Piece · Lorcana · Gundam · Dragon Ball Super ·
"Victoria, Australia" · never any of the BANNED words below · no prices · handles unchanged.
"""

import hashlib
import re

from .assets import GAME_NAMES

SIGN_OFF = 'Collector first. Seller second.'
GAMES_LINE = 'Magic · Pokémon · One Piece · Lorcana · Gundam · Dragon Ball Super'
WHERE = 'Victoria, Australia'
HANDLE = '@hokocollectables'

BANNED = [r'what\s*not', r'mystery\s*packs?', r'official', r'top\s*rated']
BANNED_RE = re.compile('|'.join(BANNED), re.I)
PRICE_RE = re.compile(r'\$\s?\d|\bA?UD\s?\d|\d+\s?(?:dollars|bucks)\b|\bAUD\b', re.I)

TAGS = {
    'pokemon': ['#pokemontcg', '#japanesepokemon', '#pokemoncollector', '#pokemonaustralia'],
    'onepiece': ['#onepiecetcg', '#onepiececardgame', '#onepiececollector', '#onepieceaustralia'],
    'dbs': ['#dragonballsuper', '#dbsfusionworld', '#dbscardgame'],
    'mtg': ['#mtg', '#magicthegathering', '#mtgaustralia'],
}
TAGS_SEALED = ['#sealedproduct', '#boosterbox', '#japanesesealed']
TAGS_SLAB = ['#psa', '#gradedcards', '#slabs']
TAGS_BASE = ['#tcgaustralia', '#tcgcollector', '#hokocollectables']

# --- body lines (rotated deterministically per asset+platform+date) --------------------------------------
SEALED_LINES = [
    'Factory sealed Japanese {what}, imported from Japan by HOKO.',
    'Sealed Japanese box, checked in hand before it ships.',
    'Japanese sealed, packed carefully and sent tracked from {where}.',
    'Straight from our Japanese supplier to your shelf. Sealed, tracked, packed by hand.',
]
NO_SHRINK_LINE = 'No outer film on this one: box seals intact, packs untouched.'
SLAB_LINES = [
    '{grader} {grade}. One copy, the exact slab in the photos.',
    'Graded by {grader}, {grade}. We only stock PSA, BGS and CGC.',
    'The slab you see is the slab you get: {grader} {grade}.',
]
TIP_LINES = {
    'spot-a-fake': 'Clean printed shrink, one seal, matching set codes. If something looks off, DM us a photo before you buy.',
    'no-outer-shrink': '"No outer shrink" means the outer film is gone but the box seals and every pack are untouched.',
    'verified-graders': 'PSA, BGS and CGC only. Every slab we sell or buy comes from a grader you can verify.',
    'buyback': 'Selling sealed or PSA / BGS / CGC slabs? One wide photo plus a typed list gets you a quote within 48 hours.',
}
ROUNDUP_LINES = {
    'mega-era': 'Every Mega-era Japanese box we have right now, cheapest first.',
    'one-piece': 'One Piece Japanese boxes on the shelf right now.',
    'under-200': 'Japanese sealed that won\'t blow the budget. Full list on the site.',
    'preorders': 'Pre-orders landing before Christmas, dispatched tracked from Victoria once they land.',
}
CTA = {
    'instagram': 'Link in bio → hokocollectables.com',
    'facebook': 'Shop it here: {url}',
    'youtube': 'Shop: {url}',
    'tiktok': 'Link in bio → hokocollectables.com',
    'pinterest': 'Shop at hokocollectables.com',
    'discord': '',
}


def _pick(options, *seed):
    h = int(hashlib.sha1('|'.join(map(str, seed)).encode()).hexdigest(), 16)
    return options[h % len(options)]


def _tags(asset, n=10):
    tags = []
    if is_slab(asset):
        tags += TAGS_SLAB
    elif asset.jp_sealed or asset.kind in ('sealed', 'roundup', 'beat'):
        tags += TAGS_SEALED
    tags += TAGS.get(asset.game, TAGS['pokemon'])
    tags += TAGS_BASE
    seen, out = set(), []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out[:n]


def is_sealed(asset):
    return asset.kind == 'sealed' or (asset.kind == 'product' and asset.extra.get('source') == 'sealed')


def is_slab(asset):
    return asset.kind == 'slab' or (asset.kind == 'product' and asset.extra.get('source') == 'slab')


def headline(asset):
    if is_sealed(asset):
        game = GAME_NAMES.get(asset.game, 'Pokémon')
        what = 'starter deck' if 'deck' in asset.name.lower() else 'booster box'
        return f'{asset.name}: sealed Japanese {game} {what}'
    if is_slab(asset):
        g = f'{asset.extra.get("grader", "")} {asset.extra.get("grade", "")}'.strip()
        return f'{asset.name} · {g}' if g and g not in asset.name else asset.name
    return asset.hook or asset.name


def body(asset, platform, day):
    k = asset.kind
    if is_sealed(asset):
        what = 'starter deck' if 'deck' in asset.name.lower() else 'booster box'
        lines = [_pick(SEALED_LINES, asset.id, platform, day).format(where=WHERE, what=what)]
        if asset.extra.get('no_shrink'):
            lines.append(NO_SHRINK_LINE)
        lines.append('Dispatched tracked from Victoria within 2–4 business days.')
        return lines
    if is_slab(asset):
        return [_pick(SLAB_LINES, asset.id, platform, day).format(grader=asset.extra.get('grader') or 'PSA',
                                                                  grade=asset.extra.get('grade') or ''),
                'Sleeved, double-boxed and sent tracked from Victoria.']
    if k == 'tip':
        return [TIP_LINES.get(asset.extra.get('tip'), asset.hook)]
    if k == 'roundup':
        return [ROUNDUP_LINES.get(asset.extra.get('roundup'), asset.hook), 'All imported from Japan by HOKO.']
    if k == 'beat':
        return [asset.extra.get('voiceover', asset.hook).replace(' Link in bio.', '')]
    if k == 'collection':
        cid = asset.extra.get('collection')
        if cid == 'sell-your-cards':
            return ['We buy sealed and PSA / BGS / CGC slabs Australia-wide. Itemised offer within 1–2 business days.',
                    GAMES_LINE + '.']
        if cid == 'graded-slabs':
            return ['PSA, BGS and CGC slabs only. Every one photographed, every one the exact copy you get.']
        return ['Newest Japanese booster boxes, imported from Japan by HOKO in small batches.',
                'Dispatched tracked from Victoria within 2–4 business days.']
    return [asset.hook] if asset.hook else []


def caption(asset, platform, day, cta=True, tags=True, games=None):
    if games is None:   # buying posts name every game we buy and stock
        games = asset.extra.get('tip') == 'buyback' or asset.extra.get('collection') == 'sell-your-cards'
    head = headline(asset)
    parts = [head, '']
    parts += body(asset, platform, day)
    if games:
        parts += ['', GAMES_LINE]
    c = CTA.get(platform, '')
    if cta and c:
        parts += ['', c.format(url=asset.url)]
    parts += ['', SIGN_OFF]
    if tags:
        parts += ['', ' '.join(_tags(asset))]
    text = '\n'.join(parts).strip()
    return re.sub(r'\n{3,}', '\n\n', text)


def youtube_title(asset):
    t = headline(asset)
    suffix = ' #Shorts'
    return (t[:100 - len(suffix)].rstrip() + suffix)


def pinterest_fields(asset, day):
    title = headline(asset)[:100]
    desc = ' '.join(body(asset, 'pinterest', day) + [SIGN_OFF, f'Packed by hand in {WHERE}.'])
    return title, desc[:500], f'{asset.name} — HOKO Collectables'[:500]


def check(text):
    """Return list of canon problems in a caption (empty = clean)."""
    problems = []
    for m in BANNED_RE.finditer(text or ''):
        problems.append(f'banned word: {m.group(0)!r}')
    for m in PRICE_RE.finditer(text or ''):
        problems.append(f'price: {m.group(0)!r}')
    if re.search(r'@(?!hokocollectables\b)[\w.]+', text or ''):
        problems.append('foreign handle')
    return problems
