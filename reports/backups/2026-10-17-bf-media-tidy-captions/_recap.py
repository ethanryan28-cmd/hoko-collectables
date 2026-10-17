"""Rewrite reels/**/h<k>.caption.txt from the sidecar json + source.csv with the new caption_text. No render."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, 'content/youtube')
from hoko import reel
from hoko.common import load_rows, product_kind
rows = {k: {r['id']: r for r in load_rows(k)} for k in ('sealed', 'slab')}
PRICE = re.compile(r'^\$[0-9].*(free AU post on sealed orders|tracked post, free on orders).*$\n', re.M)
HOOK2 = re.compile(r'^(.+) for \$[0-9][0-9,.]* — free AU post over \$250$', re.M)
done = {'source': 0, 'strip': 0}
for cap in sorted(reel.REELS.glob('*/*/h*.caption.txt')):
    meta = json.loads(cap.with_name(cap.name.replace('.caption.txt', '.json')).read_text(encoding='utf-8'))
    kind, pid, k = meta['kind'], meta['product_id'], int(meta['hook_index'])
    row = rows[kind].get(pid)
    if row:
        new = reel.caption_text(row, kind, k); done['source'] += 1
    else:   # product dropped from source.csv — remove the price line only, same result as caption_text
        new = PRICE.sub('', cap.read_text(encoding='utf-8')); done['strip'] += 1
        new = HOOK2.sub(lambda m: f"{m.group(1)} — sealed Japanese {product_kind(meta)}", new)
    cap.write_text(new, encoding='utf-8')
print(done)
