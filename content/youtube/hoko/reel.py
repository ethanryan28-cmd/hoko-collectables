"""Reel engine: 1080x1920 8-12s product reels from existing Shopify photos.

Ken Burns over product images, light sweep on slabs, big captions, 2s end card, en-AU voiceover.
Output per hook variant: reels/<sealed|slab>/<product_id>/h<k>.mp4 (+ h<k>.caption.txt, h<k>.json)
"""

import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import tts
from .common import (dshort, FONT_BLACK, FONT_BOLD, FPS, H, ROOT, SITE, W, config, fetch_image, flags, game_label,
                     load_rows, price_str, product_kind, rel, set_name, short_title)

REELS = ROOT / 'reels'
GOLD = (242, 193, 78)
END_CARD_S = 2.0

# ---------------------------------------------------------------- hooks

SEALED_HOOKS = ['gone', 'pull', 'still', 'preorder']
SLAB_HOOKS = ['worth', 'trigger']


def is_preorder(row):
    return bool(flags(row) & {'pre-order', 'preorder', 'label:PRE-ORDER'}) or 'PRE-ORDER' in row['title'].upper()


def eligible_hooks(row, kind):
    """Only hooks that are true for this item (no fake scarcity, no fake pre-orders)."""
    if kind == 'slab':
        return [0, 1]
    out = []
    inv = int(float(row.get('inventory') or 0))
    if 1 <= inv <= 2 and not is_preorder(row):
        out.append(0)
    out += [1, 2]
    if is_preorder(row) and row.get('release_date'):
        out.append(3)
    return out


def slab_short(row):
    words = []
    for w_ in row['card'].split():
        if any(c.isdigit() for c in w_) or w_ in {'Alt', 'Art', 'Topps', 'Black', 'SR', 'R'}:
            break
        words.append(w_)
    return ' '.join(words) or row['card']


def hook_text(row, kind, k):
    """(on-screen hook, voiceover script)."""
    p = price_str(row['price'])
    if kind == 'slab':
        g = f"{row['grader']} {row['grade']}"
        name = slab_short(row)
        if k == 0:
            return (f"{g} {name} — what's it worth?",
                    f"{g} {name}. What's it worth? We've got it at {p}. Link in bio.")
        return (f"Would you pull the trigger at {p}?",
                f"Would you pull the trigger at {p}? {g} {name}. On HOKO now. Link in bio.")
    s = set_name(row)
    kd = product_kind(row)
    if k == 0:
        n = int(float(row['inventory']))
        return ("This box is about to be gone",
                f"This box is about to be gone. {s}, sealed Japanese {kd}. Only {n} left at {p}. Link in bio.")
    if k == 1:
        inv = int(float(row.get('inventory') or 0))
        where = 'in Victoria now' if inv > 0 else 'imported to order'
        return (f"{s} — sealed Japanese {kd}, {where}",
                f"{s}. Sealed Japanese {kd}, {where}. {p} on HOKO. Link in bio.")
    if k == 2:
        return (f"Would you pay {p} for {s}?",
                f"Would you pay {p} for a sealed {s} {kd}? Tell us below. Link in bio.")
    month = row['release_date'][:7]
    from datetime import date
    mname = date.fromisoformat(month + '-01').strftime('%B')
    return (f"Pre-order — lands {mname}",
            f"Pre-order now. {s} lands in {mname}. {p} on HOKO. Link in bio.")


# ---------------------------------------------------------------- captions

def hashtags(row, kind):
    g = row.get('game')
    if kind == 'slab':
        base = ['#gradedcards', '#slabs', '#thehobby', f"#{row['grader'].lower()}",
                f"#{row['grader'].lower()}{row['grade'].replace('.', '')}"]
        base += ['#pokemontcg', '#pokemoncards', '#pokemoncollector', '#pokemonaustralia'] if g == 'pokemon' else \
                ['#onepiecetcg', '#onepiececardgame', '#opcg', '#onepieceaustralia']
    else:
        base = ['#sealedproduct', '#boosterbox', '#tcgcollector']
        base += ['#pokemontcg', '#japanesepokemon', '#pokemonjapan', '#pokemoncollector', '#pokemonaustralia'] \
            if g == 'pokemon' else ['#onepiecetcg', '#onepiececardgame', '#onepiecejapanese', '#onepieceaustralia']
    base += ['#tcgaustralia', '#melbournecollectors', '#aussiecollector', '#hokocollectables']
    seen = []
    for t in base:
        if t not in seen:
            seen.append(t)
    return seen[:15]


def caption_text(row, kind, k, when=None):
    """Caption for posting date `when` (date or None = pre-November base copy)."""
    from datetime import date
    cfg = config()
    hook, _ = hook_text(row, kind, k)
    p = price_str(row['price'])
    lines = [hook, '']
    if kind == 'slab':
        label = f" {row['grade_label']}" if row.get('grade_label') else ''
        lines += [f"{row['card']} — {row['grader']} {row['grade']}{label}.",
                  'Verified grader (PSA / BGS / CGC only). Ships from Victoria.',
                  f'{p} — tracked post, free on orders $150+.']
    else:
        extra = ' (no outer shrink)' if 'no-shrink' in flags(row) else ''
        lines += [f"{short_title(row)} — sealed Japanese {game_label(row)} {product_kind(row)}{extra}.",
                  'Imported via our wholesale partners. Packed carefully, tracked from Victoria.',
                  f'{p} — free AU post on sealed orders $250+.']
    lines.append(f"Grab it at hokocollectables.com → {row['url']}")
    if when is not None:
        cutoff = date.fromisoformat(cfg['christmas_cutoff'])
        if date(when.year, 11, 1) <= when <= date(when.year, 11, 30) and kind == 'sealed':
            lines.append(f"Join the BF box drop list — $5 off boxes {cfg.get('bf_list_url') or '{{BF_LIST_URL}}'}")
        if kind == 'sealed' and when.month in (11, 12):
            if when <= cutoff:
                lines.append(f"Christmas delivery: order by {dshort(cutoff)}.")
            else:
                lines.append('Slabs ship in 1–3 days if you need it under the tree.')
        if kind == 'slab' and when.month == 12:
            lines.append('Slabs ship from Victoria in 1–3 business days — AusPost Christmas send-by dates apply.')
    lines += ['', 'Collector first. Seller second.', '', ' '.join(hashtags(row, kind))]
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------- drawing helpers

def font(size, black=True):
    return ImageFont.truetype(str(FONT_BLACK if black else FONT_BOLD), size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_layer(text, size, y, color=(255, 255, 255), black=True, max_w=960, stroke=10, box=None):
    """RGBA full-frame layer with centred, wrapped, stroked text. Shrinks to fit 3 lines."""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    while True:
        f = font(size, black)
        lines = wrap(d, text, f, max_w)
        if len(lines) <= 3 or size < 50:
            break
        size -= 6
    lh = int(size * 1.12)
    total = lh * len(lines)
    if box:
        widest = max(d.textlength(l_, font=f) for l_ in lines)
        pad = 34
        d.rounded_rectangle([W / 2 - widest / 2 - pad, y - pad * 0.6, W / 2 + widest / 2 + pad, y + total + pad * 0.4],
                            radius=28, fill=box)
    for i, l_ in enumerate(lines):
        tw = d.textlength(l_, font=f)
        d.text(((W - tw) / 2, y + i * lh), l_, font=f, fill=color,
               stroke_width=0 if box else stroke, stroke_fill=(0, 0, 0))
    return layer


def cover(img, w, h):
    r = max(w / img.width, h / img.height)
    im = img.resize((math.ceil(img.width * r), math.ceil(img.height * r)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))


def end_card():
    im = Image.new('RGB', (W, H), (12, 12, 14))
    d = ImageDraw.Draw(im)
    for txt, size, y, col, blk in [('HOKO', 210, 690, (255, 255, 255), True),
                                   ('Collectables', 110, 910, (255, 255, 255), True),
                                   ('hokocollectables.com', 64, 1100, GOLD, False),
                                   ('Collector first. Seller second.', 44, 1210, (200, 200, 200), False)]:
        f = font(size, blk)
        tw = d.textlength(txt, font=f)
        d.text(((W - tw) / 2, y), txt, font=f, fill=col)
    d.rectangle([W / 2 - 90, 1060, W / 2 + 90, 1066], fill=GOLD)
    return im


# ---------------------------------------------------------------- render

class Slide:
    """One product photo: blurred cover background + Ken Burns foreground."""

    BOX = (940, 940)   # foreground area
    CY = 1000           # foreground centre y

    def __init__(self, path, seed, box=None, cy=None):
        self.BOX = box or self.BOX
        self.CY = cy or self.CY
        src = Image.open(path)
        src = src.convert('RGBA') if src.mode in ('P', 'LA', 'RGBA') else src.convert('RGB')
        if src.mode == 'RGBA':
            bgw = Image.new('RGB', src.size, (245, 245, 245))
            bgw.paste(src, mask=src.split()[3])
            src = bgw
        self.bg = cover(src, W, H).filter(ImageFilter.GaussianBlur(38))
        self.bg = Image.blend(self.bg, Image.new('RGB', (W, H), (0, 0, 0)), 0.55)
        r = min(self.BOX[0] / src.width, self.BOX[1] / src.height)
        self.base = src.resize((int(src.width * r * 1.12), int(src.height * r * 1.12)), Image.LANCZOS)
        self.fw, self.fh = int(src.width * r), int(src.height * r)
        self.dir = 1 if seed % 2 else -1
        self.yy, self.xx = np.mgrid[0:self.fh, 0:self.fw].astype(np.float32)
        shadow = Image.new('RGBA', (self.fw + 60, self.fh + 60), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle([30, 40, self.fw + 30, self.fh + 40], 24, fill=(0, 0, 0, 150))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        self.x0, self.y0 = (W - self.fw) // 2, self.CY - self.fh // 2
        self.bg.paste(shadow, (self.x0 - 30, self.y0 - 30), shadow)

    def frame(self, t, sweep):
        """t in [0,1] across this slide's life; sweep True adds the slab light sweep."""
        z = 1.0 + 0.10 * ease(t)
        bw, bh = self.base.size
        cw, ch = bw / (z * 1.12), bh / (z * 1.12)
        cx = bw / 2 + self.dir * (bw - cw) * 0.35 * (ease(t) - 0.5)
        cy = bh / 2 - (bh - ch) * 0.25 * (ease(t) - 0.5)
        crop = self.base.resize((self.fw, self.fh), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
        if sweep:
            pos = (-0.4 + 1.8 * ((t * 1.3) % 1.0)) * (self.fw + 0.5 * self.fh)
            band = np.exp(-(((self.xx + 0.5 * self.yy) - pos) / (self.fw * 0.09)) ** 2) * 0.45
            arr = np.asarray(crop, dtype=np.float32)
            arr = arr + (255 - arr) * band[..., None]
            crop = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
        out = self.bg.copy()
        out.paste(crop, (self.x0, self.y0))
        return out


def render(row, kind, k, out_mp4, force=False, override=None, body=None, tag=None):
    """override=(on-screen hook, voiceover) for beat / tip reels; body = list of on-screen lines that
    replace the price block in the second half; tag overrides the top pill."""
    out_mp4 = Path(out_mp4)
    meta_p = out_mp4.with_suffix('.json')
    if out_mp4.exists() and meta_p.exists() and not force:
        if not override:   # captions are cheap — keep them in sync with current copy rules
            out_mp4.with_name(out_mp4.stem + '.caption.txt').write_text(caption_text(row, kind, k), encoding='utf-8')
        return json.loads(meta_p.read_text())
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    hook, vo = override or hook_text(row, kind, k)
    vo_base = out_mp4.with_name(out_mp4.stem + '.vo')
    engine = tts.synth(vo, vo_base)
    vo_wav = vo_base.with_suffix('.wav')
    vo_len = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                   str(vo_wav)], capture_output=True, text=True).stdout)
    max_content = 9.8 - 0.6
    tempo = 1.0
    if vo_len > max_content:
        tempo = min(1.35, vo_len / max_content)
        vo_len = vo_len / tempo
    content = max(6.0, min(9.8, vo_len + 0.6))
    total = round(content + END_CARD_S, 2)

    imgs = [fetch_image(u) for u in row['reel_images'].split('|') if u][:3]
    slides = [Slide(p, i + int(row['id'][-3:]), box=(720, 720) if body else None, cy=800 if body else None)
              for i, p in enumerate(imgs)]
    p = price_str(row['price'])
    tag = tag or (f"{row['grader']} {row['grade']}" if kind == 'slab' else f"JAPANESE SEALED · {game_label(row).upper()}")
    sub = row['card'] if kind == 'slab' else short_title(row)
    post = 'Tracked post · free $150+' if kind == 'slab' else 'Free AU post on sealed $250+'
    L_tag = text_layer(tag, 46, 120, color=(15, 15, 15), black=True, box=(*GOLD, 255))
    L_hook = text_layer(hook.upper(), 92, 215)
    L_price = text_layer(p, 180, 1470, color=GOLD, stroke=12)
    L_sub = text_layer(sub, 52, 1690, black=False, stroke=7)
    L_post = text_layer(post, 46, 250, black=False, box=(0, 0, 0, 190))
    L_body = None
    if body:
        L_body = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        y = 1260
        for i, line in enumerate(body):
            L_body.alpha_composite(text_layer(line, 66 if i == 0 else 52, y, color=GOLD if i == 0 else (255, 255, 255),
                                              black=(i == 0), stroke=8))
            y += 150 if i == 0 else 118
    endc = end_card()

    hook_end = content * 0.48
    n = int(round(total * FPS))
    cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-i', str(vo_wav), '-filter_complex',
           f'[1:a]atempo={tempo:.3f},adelay=300|300,apad,atrim=0:{total},afade=t=out:st={content - 0.25}:d=0.25[a]',
           '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '128k', '-ar', '48000', '-t', f'{total}', '-movflags', '+faststart', str(out_mp4)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    seg = content / len(slides)
    xf = 0.35
    for i in range(n):
        t = i / FPS
        if t >= content:
            fr = endc if t >= content + 0.2 else Image.blend(prev, endc, (t - content) / 0.2)
        else:
            si = min(int(t / seg), len(slides) - 1)
            local = (t - si * seg) / seg
            fr = slides[si].frame(local, kind == 'slab')
            if si + 1 < len(slides) and t > (si + 1) * seg - xf:
                a = (t - ((si + 1) * seg - xf)) / xf
                fr = Image.blend(fr, slides[si + 1].frame(0, kind == 'slab'), a)
            fr = fr.convert('RGBA')
            fr.alpha_composite(L_tag)
            if t < hook_end:
                a = min(1, t / 0.25)
                fr.alpha_composite(_fade(L_hook, a))
            else:
                a = min(1, (t - hook_end) / 0.25)
                if L_body is not None:
                    fr.alpha_composite(_fade(L_body, a))
                else:
                    fr.alpha_composite(_fade(L_post, a))
                    fr.alpha_composite(_fade(L_price, a))
                    fr.alpha_composite(_fade(L_sub, a))
            fr = fr.convert('RGB')
            prev = fr
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f'ffmpeg failed for {out_mp4}')
    vo_wav.unlink(missing_ok=True)
    meta = {'product_id': row['id'], 'kind': kind, 'hook_index': k, 'hook': hook, 'voiceover': vo,
            'tts': engine, 'duration': total, 'url': row['url'], 'title': row['title'], 'reel': rel(out_mp4)}
    meta_p.write_text(json.dumps(meta, indent=2))
    if not override:
        out_mp4.with_name(out_mp4.stem + '.caption.txt').write_text(caption_text(row, kind, k), encoding='utf-8')
    return meta


_fade_cache = {}


def _fade(layer, a):
    if a >= 1:
        return layer
    key = (id(layer), round(a, 2))
    if key not in _fade_cache:
        l2 = layer.copy()
        l2.putalpha(l2.getchannel('A').point(lambda v: int(v * a)))
        _fade_cache[key] = l2
    return _fade_cache[key]


def reel_path(kind, pid, k):
    return REELS / kind / str(pid) / f'h{k}.mp4'


def promotable(row, kind):
    return kind == 'slab' or 'OOS-SUPPLIER' not in flags(row)


def build(kind, which='all', force=False, hooks=None, log=print):
    rows = load_rows(kind)
    if which != 'all':
        rows = [r for r in rows if r['id'] == which or r['handle'] == which]
        if not rows:
            raise SystemExit(f'No {kind} row with id/handle {which}')
    else:
        rows = [r for r in rows if promotable(r, kind)]
    built = []
    for r in rows:
        for k in (hooks if hooks is not None else eligible_hooks(r, kind)):
            if k not in eligible_hooks(r, kind):
                continue
            m = render(r, kind, k, reel_path(kind, r['id'], k), force=force)
            log(f"  {kind} {r['id']} h{k} {m['duration']}s [{m['tts']}] {m['reel']}")
            built.append(m)
    return built
