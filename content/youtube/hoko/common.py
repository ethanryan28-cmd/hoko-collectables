"""Shared paths, config, CSV loading and small helpers for the HOKO content machine."""

import csv
import hashlib
import json
import os
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # content/youtube
REPO = ROOT.parent.parent                              # repo root
CACHE = ROOT / '.cache'
FONT_BLACK = ROOT / 'assets' / 'fonts' / 'InterDisplay-Black.otf'
FONT_BOLD = ROOT / 'assets' / 'fonts' / 'InterDisplay-Bold.otf'
CONFIG_PATH = ROOT / 'config.json'

SITE = 'https://www.hokocollectables.com'
W, H = 1080, 1920
FPS = 30


def load_env():
    """Load content/youtube/.env then repo-root .env into os.environ (no overwrite)."""
    for p in (ROOT / '.env', REPO / '.env'):
        if not p.exists():
            continue
        for line in p.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def config():
    return json.loads(CONFIG_PATH.read_text(encoding='utf-8'))


def load_rows(kind):
    """kind: 'sealed' or 'slab'. Returns list of dicts from <kind>/source.csv."""
    folder = 'sealed' if kind == 'sealed' else 'slabs'
    with open(ROOT / folder / 'source.csv', newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def flags(row):
    return set(filter(None, row.get('flags', '').split('|')))


def price_str(p):
    v = float(p)
    return f'${v:,.0f}' if v == int(v) else f'${v:,.2f}'


def short_title(row):
    """'Pokemon Abyss Eye (M5) Sealed Japanese Booster Box' -> 'Abyss Eye (M5)'."""
    t = re.sub(r'^\[PRE-ORDER\]\s*', '', row['title'])
    t = re.sub(r'^(Pokemon|Pokémon|One Piece TCG|One Piece|Dragon Ball Super)\s+', '', t)
    t = re.sub(r'\s+(Sealed\s+)?Japanese.*$', '', t)
    t = re.sub(r'\s+Sealed$', '', t)
    t = t.strip().rstrip('—').strip()
    if t.startswith('Center '):
        t = 'Pokémon ' + t
    if 'no-shrink' in flags(row):
        t += ' · no shrink'
    return t


def set_name(row):
    """Set name without the code: 'Abyss Eye (M5)' -> 'Abyss Eye'; 'OP-07 500 Years...' -> '500 Years in the Future'."""
    s = re.sub(r'\s*\([^)]*\)', '', short_title(row)).strip()
    s = re.sub(r'^(OP|EB|PRB|FB)-?\d+\s*', '', s).strip()
    return s or row.get('set_code') or short_title(row)


def product_kind(row):
    t = row['title'].lower()
    if 'starter deck' in t:
        return 'starter deck'
    if 'special box' in t:
        return 'special box'
    if 'premium boost' in t:
        return 'premium booster box'
    if 'extra booster' in t:
        return 'extra booster box'
    return 'booster box'


def game_label(row):
    return {'pokemon': 'Pokémon', 'onepiece': 'One Piece', 'dbs': 'Dragon Ball Super',
            'mtg': 'Magic'}.get(row.get('game', ''), 'TCG')


def fetch_image(url):
    """Download (once) to .cache/img and return the local path."""
    import requests
    CACHE.joinpath('img').mkdir(parents=True, exist_ok=True)
    p = CACHE / 'img' / (hashlib.md5(url.encode()).hexdigest()[:16] + '.img')
    if not p.exists() or p.stat().st_size == 0:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        p.write_bytes(r.content)
    return p


def ffprobe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                          'stream=codec_type,width,height:format=duration', '-of', 'json', str(path)],
                         capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    v = next((s for s in j['streams'] if s['codec_type'] == 'video'), {})
    return {'width': v.get('width'), 'height': v.get('height'),
            'duration': float(j['format']['duration']),
            'audio': any(s['codec_type'] == 'audio' for s in j['streams'])}


def today():
    override = os.environ.get('HOKO_TODAY')   # for dry-runs / tests
    return date.fromisoformat(override) if override else date.today()


def rel(p):
    return Path(p).resolve().relative_to(ROOT).as_posix()


def dshort(d):
    """Mon 30 Nov (portable — no %-d)."""
    return f'{d:%a} {d.day} {d:%b}'


def dlong(d):
    return f'{d:%A} {d.day} {d:%B %Y}'
