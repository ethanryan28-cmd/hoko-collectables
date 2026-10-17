"""Pre-order placeholder product image for a box whose publisher has not released art yet.

Same look as content/youtube/hoko/reel.py CardSlide (dark card, gold outline, set code,
PRE-ORDER). Never borrows another product's photo. Swap for the publisher art when it exists.

Usage: python scripts/preorder_placeholder_image.py M7 "Pokémon Aura Seeker" "Japanese Booster Box" out.png
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_BLACK = ROOT / 'content/youtube/assets/fonts/InterDisplay-Black.otf'
FONT_BOLD = ROOT / 'content/youtube/assets/fonts/InterDisplay-Bold.otf'
GOLD = (242, 193, 78)
S = 1200


def font(size, black=True):
    return ImageFont.truetype(str(FONT_BLACK if black else FONT_BOLD), size)


def centred(d, text, size, y, fill, black=True):
    f = font(size, black)
    tw = d.textlength(text, font=f)
    d.text(((S - tw) / 2, y), text, font=f, fill=fill)


def build(code, name, kind, out):
    im = Image.new('RGB', (S, S), (14, 14, 18))
    d = ImageDraw.Draw(im)
    for y in range(0, S, 4):
        v = int(14 + 22 * (1 - abs(y - 560) / 700))
        d.line([(0, y), (S, y + 4)], fill=(v, v, v + 6), width=4)
    d.rounded_rectangle([150, 170, 1050, 820], 40, outline=GOLD, width=8, fill=(24, 24, 30))
    centred(d, code, 200 if len(code) <= 4 else 140, 300, GOLD)
    centred(d, 'PRE-ORDER', 48, 600, (255, 255, 255), black=False)
    centred(d, name, 56, 890, (255, 255, 255))
    centred(d, kind, 40, 970, (200, 200, 200), black=False)
    centred(d, 'Art to follow once the publisher releases it', 30, 1060, (150, 150, 150), black=False)
    centred(d, 'HOKO Collectables', 30, 1120, GOLD, black=False)
    im.save(out, 'PNG', optimize=True)
    return out


if __name__ == '__main__':
    code, name, kind, out = sys.argv[1:5]
    print(build(code, name, kind, Path(out)))
