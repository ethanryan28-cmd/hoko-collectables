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
    if is_preorder(row):
        return [3] if row.get('release_date') else [1]
    out = [1, 2]
    if row.get('chase'):
        out.insert(0, 4)        # "What's in [set]?" — only when Ethan has filled the chase column
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
            return (f"{g} {row['card']}",
                    f"{g} {row['card']}. {p}, tracked from Victoria. Link in bio.")
        return (f"One in stock — {g} {name}, {p}",
                f"One in stock. {g} {name}, {p}. Link in bio.")
    s = set_name(row)
    kd = product_kind(row)
    if k == 1:
        inv = int(float(row.get('inventory') or 0))
        where = 'in Victoria now' if inv > 0 else 'imported to order'
        return (f"{s} — sealed Japanese {kd}, {where}",
                f"{s}. Sealed Japanese {kd}, {where}. {p} on HOKO. Link in bio.")
    if k == 2:
        if row.get('packs'):
            n_packs, n_cards = row['packs'].lower().split('x')
            return (f"{s} — {n_packs} packs, {n_cards} cards a pack",
                    f"{s}. {n_packs} packs, {n_cards} cards a pack, factory sealed. {p} on HOKO. Link in bio.")
        return (f"{s} for {p} — free AU post over $250",
                f"{s}, {p}. Free Australian postage when your sealed order is over two fifty. Link in bio.")
    if k == 4:
        return (f"What's in {s}?",
                f"What's in {s}? {row['chase']}. Sealed {kd}, {p} on HOKO. Link in bio.")
    from datetime import date
    rd = date.fromisoformat(row['release_date'])
    return (f"Pre-order — lands {rd:%B}",
            f"Pre-order open. {s}, {game_label(row)}. Japan release {rd.day} {rd:%B}, ships from Victoria "
            f"a few days after. {p} on HOKO. Link in bio.")


def preorder_body(row):
    from datetime import date
    rd = date.fromisoformat(row['release_date'])
    return [f'{set_name(row)} ({row["set_code"]})', f'JP release {dshort(rd)}', 'Ships from Victoria 2–4 days after',
            f'{price_str(row["price"])} · free AU post $250+']


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
    base += ['#tcgaustralia', '#victoriacollectors', '#aussiecollector', '#hokocollectables']
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
        extra = ' (outer film removed, packs untouched)' if 'no-shrink' in flags(row) else ''
        if k == 4:
            extra += f". Chase: {row['chase']}"
        if k == 3:
            from datetime import date
            rd = date.fromisoformat(row['release_date'])
            extra += f". Pre-order: Japan release {dshort(rd)}, ships tracked from Victoria 2–4 business days after"
        lines += [f"{short_title(row)} — sealed Japanese {game_label(row)} {product_kind(row)}{extra}.",
                  'Imported direct from our Japanese distributor. Packed carefully, tracked from Victoria.',
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

class CardSlide:
    """No photo yet (pre-orders): dark card with the set code, slow drift. Never borrows another product's photo."""

    def __init__(self, label, seed):
        self.bg = Image.new('RGB', (W, H), (14, 14, 18))
        d = ImageDraw.Draw(self.bg)
        for y in range(0, H, 4):
            v = int(14 + 22 * (1 - abs(y - 900) / 1100))
            d.line([(0, y), (W, y + 4)], fill=(v, v, v + 6), width=4)
        card = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([170, 560, 910, 1180], 40, outline=GOLD, width=8, fill=(24, 24, 30, 255))
        f = font(170 if len(label) <= 4 else 120)
        tw = cd.textlength(label, font=f)
        cd.text(((W - tw) / 2, 760), label, font=f, fill=GOLD)
        f2 = font(44, False)
        tw = cd.textlength('PRE-ORDER', font=f2)
        cd.text(((W - tw) / 2, 1030), 'PRE-ORDER', font=f2, fill=(255, 255, 255))
        self.card = card
        self.dir = 1 if seed % 2 else -1

    def frame(self, t, sweep):
        out = self.bg.copy()
        dx = int(self.dir * 30 * (ease(t) - 0.5))
        out.paste(self.card, (dx, int(-20 * ease(t))), self.card)
        return out


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


_whisper = None


def align_to_script(heard, script):
    """Whisper mishears names ('Nihil Zero' → 'Nile'). Keep its timings, show the script's words.
    Matched words take their heard timing; the rest are interpolated between neighbours."""
    import difflib
    norm = lambda w: re.sub(r'[^a-z0-9$]', '', w.lower())
    sw = script.split()
    hw = [h[2] for h in heard]
    times = [None] * len(sw)
    sm = difflib.SequenceMatcher(a=[norm(w) for w in sw], b=[norm(w) for w in hw], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for di in range(i2 - i1):
                times[i1 + di] = (heard[j1 + di][0], heard[j1 + di][1])
        elif tag == 'replace' and (i2 - i1) == (j2 - j1):
            for di in range(i2 - i1):
                times[i1 + di] = (heard[j1 + di][0], heard[j1 + di][1])
    # interpolate gaps
    known = [i for i, t in enumerate(times) if t]
    if not known:
        return []
    out = []
    for i, w in enumerate(sw):
        if times[i]:
            out.append((times[i][0], times[i][1], w))
            continue
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        a = times[prev][1] if prev is not None else heard[0][0]
        b = times[nxt][0] if nxt is not None else heard[-1][1]
        span = (b - a) / ((nxt if nxt is not None else len(sw)) - (prev if prev is not None else -1))
        k = i - (prev if prev is not None else -1)
        out.append((a + span * (k - 1), a + span * k, w))
    return out


def word_times(wav, tempo, delay=0.3, script=None):
    """[(start, end, word)] in reel seconds, from faster-whisper on the voiceover (works for any TTS voice)."""
    global _whisper
    import numpy as np
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(wav), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel('base', device='auto', compute_type='int8')
    segs, _ = _whisper.transcribe(audio, word_timestamps=True, language='en')
    out = []
    for sg in segs:
        for w_ in sg.words or []:
            out.append((w_.start / tempo + delay, w_.end / tempo + delay, w_.word.strip()))
    return align_to_script(out, script) if script else out


def caption_layers(words, y=1385):
    """One layer per word: its 3-word phrase in a dark pill, the spoken word in gold."""
    layers = []
    f = font(58)
    # phrase-aware chunks: ≤3 words, break after punctuation
    phrase_of, cur = [], []
    for idx, w in enumerate(words):
        cur.append(idx)
        if len(cur) == 3 or w[2][-1:] in '.,?!:' or idx == len(words) - 1:
            for j in cur:
                phrase_of.append([words[j2] for j2 in cur])
            cur = []
    for i, (a, b, w_) in enumerate(words):
        phrase = phrase_of[i]
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        widths = [d.textlength(p[2].upper(), font=f) for p in phrase]
        gap = 22
        total = sum(widths) + gap * (len(phrase) - 1)
        x = (W - total) / 2
        d.rounded_rectangle([x - 30, y - 16, x + total + 30, y + 78], 22, fill=(0, 0, 0, 200))
        for (aa, bb, ww), wd in zip(phrase, widths):
            col = GOLD if (aa, bb, ww) == (a, b, w_) else (255, 255, 255)
            d.text((x, y), ww.upper(), font=f, fill=col)
            x += wd + gap
        layers.append((a, layer))
    return layers


def caption_at(layers, t):
    cur = None
    for a, layer in layers:
        if a <= t:
            cur = layer
        else:
            break
    return cur


def render(row, kind, k, out_mp4, force=False, override=None, body=None, tag=None, items=None):
    """override=(on-screen hook, voiceover) for beat / tip reels; body = list of on-screen lines that
    replace the price block in the second half; tag overrides the top pill."""
    out_mp4 = Path(out_mp4)
    meta_p = out_mp4.with_suffix('.json')
    if out_mp4.exists() and meta_p.exists() and not force:
        if not override:   # captions are cheap — keep them in sync with current copy rules
            out_mp4.with_name(out_mp4.stem + '.caption.txt').write_text(caption_text(row, kind, k), encoding='utf-8')
        return json.loads(meta_p.read_text())
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    _fade_cache.clear()   # per-reel cache; without this memory grows ~0.5 GB per reel until the OS kills us
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

    if kind == 'sealed' and k == 3 and not body:
        body = preorder_body(row)
    words = [] if items else word_times(vo_wav, tempo, script=vo)
    L_words = caption_layers(words, y=1235 if body else 1385)
    item_layers = []
    if items:
        # roundup: one slide per product, ranked label under each
        slides = []
        for i, it in enumerate(items):
            im = next((u for u in it['reel_images'].split('|') if u), None)
            slides.append(Slide(fetch_image(im), i, box=(760, 760), cy=880) if im
                          else CardSlide(it.get('set_code') or 'NEW', i))
            lab = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            lab.alpha_composite(text_layer(f'#{i + 1}  {short_title(it)}', 60, 1490, black=True, stroke=8))
            lab.alpha_composite(text_layer(price_str(it['price']), 130, 1590, color=GOLD, stroke=11))
            item_layers.append(lab)
    else:
        imgs = [fetch_image(u) for u in row['reel_images'].split('|') if u][:3]
        if imgs:
            slides = [Slide(p, i + int(row['id'][-3:]), box=(660, 660) if body else (860, 860), cy=880 if body else 930)
                      for i, p in enumerate(imgs)]
        else:
            slides = [CardSlide(row.get('set_code') or 'NEW', int(row['id'][-3:]))]
    p = price_str(row['price'])
    tag = tag or (f"{row['grader']} {row['grade']}" if kind == 'slab' else f"JAPANESE SEALED · {game_label(row).upper()}")
    sub = row['card'] if kind == 'slab' else short_title(row)
    post = 'Tracked post · free $150+' if kind == 'slab' else 'Free AU post on sealed $250+'
    L_tag = text_layer(tag, 46, 120, color=(15, 15, 15), black=True, box=(*GOLD, 255))
    L_hook = text_layer(hook.upper(), 92, 215)
    L_price = text_layer(p, 170, 1500, color=GOLD, stroke=12)
    L_sub = text_layer(sub, 50, 1715, black=False, stroke=7)
    L_post = text_layer(post, 46, 250, black=False, box=(0, 0, 0, 190))
    L_body = None
    if body:
        L_body = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        y = 1340
        for i, line in enumerate(body):
            L_body.alpha_composite(text_layer(line, 66 if i == 0 else 52, y, color=GOLD if i == 0 else (255, 255, 255),
                                              black=(i == 0), stroke=8))
            y += 140 if i == 0 else 112
    endc = end_card()

    hook_end = 1.3 if items else content * 0.48
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
            if items:
                fr.alpha_composite(_fade(L_hook, min(1, t / 0.25)) if t < hook_end else item_layers[si])
            elif t < hook_end:
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
            cap = caption_at(L_words, t)
            if cap is not None and (not items or t >= hook_end):
                fr.alpha_composite(cap)
            fr = fr.convert('RGB')
            prev = fr
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f'ffmpeg failed for {out_mp4}')
    vo_wav.unlink(missing_ok=True)
    meta = {'product_id': row['id'], 'kind': kind, 'hook_index': k, 'hook': hook, 'voiceover': vo,
            'tts': engine, 'duration': total, 'url': row['url'], 'title': row['title'], 'reel': rel(out_mp4),
            'words': len(words)}
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
