"""run.py source — rebuild sealed/source.csv + slabs/source.csv from the Shopify Admin API (read-only).

sealed: every ACTIVE Japanese sealed product (product type "Sealed Product", tag japanese) plus pre-orders
        (tag preorder / pre-order) once they have at least one image.
slabs:  every ACTIVE product with PSA / BGS / CGC / TAG + a grade in the title.
Rows without an image are skipped and reported (reels need a photo). Slab reels use the first image
(slab front) unless `reel_images` is hand-edited in the CSV.
"""

import csv
import re

from .common import ROOT
from .http import Http
from .publish import shopify_gql

Q = """query($q:String!,$after:String){ products(first:100, query:$q, after:$after){
  pageInfo{ hasNextPage endCursor }
  nodes{ id handle title status productType tags onlineStoreUrl totalInventory publishedAt
         priceRangeV2{ minVariantPrice{ amount } } images(first:4){ nodes{ url } }
         metafields(first:10, namespace:"custom"){ nodes{ key value } } } } }"""

SLAB_RE = re.compile(r'\b(PSA|BGS|CGC|TAG)\s+(\d+(?:\.\d)?)\s*(.*)$')
KEEP_FLAGS = {'OOS-SUPPLIER', 'newest-drop', 'no-shrink', 'pre-order', 'preorder', 'ds-active', 'label:PRE-ORDER'}


def products(http, q):
    out, after = [], None
    while True:
        d = shopify_gql(http, Q, {'q': q, 'after': after})['products']
        out += d['nodes']
        if not d['pageInfo']['hasNextPage']:
            return out
        after = d['pageInfo']['endCursor']


def write(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def refresh():
    http = Http()
    sealed, skipped = [], []
    q = ("product_type:'Sealed Product' AND tag:japanese AND (status:active OR "
         "(status:draft AND (tag:preorder OR tag:pre-order)))")
    for n in products(http, q):
        ims = [i['url'] for i in n['images']['nodes']]
        mf = {m['key']: m['value'] for m in n['metafields']['nodes']}
        is_pre = any(t in n['tags'] for t in ('preorder', 'pre-order', 'label:PRE-ORDER'))
        if not ims and not (is_pre and mf.get('release_date')):
            skipped.append(n['title'])   # pre-orders with a release date get a text-card reel instead
            continue
        sealed.append(dict(
            id=n['id'].split('/')[-1], handle=n['handle'], title=n['title'], set_code=mf.get('set_code', ''),
            game=next((t.split(':')[1] for t in n['tags'] if t.startswith('game:')), ''),
            price=n['priceRangeV2']['minVariantPrice']['amount'], inventory=n['totalInventory'], status=n['status'],
            release_date=mf.get('release_date', ''), listed_at=(n['publishedAt'] or '')[:10],
            url=n['onlineStoreUrl'] or f"https://www.hokocollectables.com/products/{n['handle']}",
            flags='|'.join(t for t in n['tags'] if t in KEEP_FLAGS), images='|'.join(ims),
            image_source='shopify' if ims else 'none (no photo yet)',
            reel_images='|'.join(ims)))
    slabs = []
    for n in products(http, 'status:active AND (title:*PSA* OR title:*BGS* OR title:*CGC* OR title:*TAG*)'):
        m = SLAB_RE.search(n['title'])
        ims = [i['url'] for i in n['images']['nodes']]
        if not m or not ims:
            continue
        card = re.sub(r'\s+(Pokemon|One Piece)$', '', n['title'][:m.start()].strip())
        slabs.append(dict(
            id=n['id'].split('/')[-1], handle=n['handle'], title=n['title'], card=card, grader=m.group(1),
            grade=m.group(2), grade_label=m.group(3).strip(),
            game='pokemon' if 'Pokemon' in n['title'] else 'onepiece', price=n['priceRangeV2']['minVariantPrice']['amount'],
            inventory=n['totalInventory'], status=n['status'], release_date='',
            url=n['onlineStoreUrl'] or f"https://www.hokocollectables.com/products/{n['handle']}",
            images='|'.join(ims), image_source='shopify', reel_images=ims[0]))
    write(ROOT / 'sealed' / 'source.csv', sealed)
    write(ROOT / 'slabs' / 'source.csv', slabs)
    print(f'sealed: {len(sealed)} rows · slabs: {len(slabs)} rows · skipped (no image): {len(skipped)}')
    for t in skipped:
        print('  no image:', t)
