"""run.py cutoff — add "Christmas delivery cutoff: order by <date>" to every live Japanese sealed product
description and the Japanese sealed collection. No price / discount / shipping changes.

Default is a dry run that prints ONE example and the count (CLAUDE.md habit: show one first).
`--apply` writes. Idempotent: an existing cutoff paragraph is replaced, never duplicated.
`--remove` strips the paragraph again (use after Christmas).
Needs SHOPIFY_STORE + SHOPIFY_ADMIN_TOKEN (or SHOPIFY_TOKEN) in .env. Backup is written first.
"""

import json
import re
from datetime import date, datetime

from .common import ROOT, config, dlong
from .http import Http
from .publish import shopify_gql

COLLECTION_HANDLE = 'japan-direct-sealed'
BLOCK_RE = re.compile(r'<p data-hoko="xmas-cutoff">.*?</p>\n?', re.S)


def block(cutoff):
    return (f'<p data-hoko="xmas-cutoff"><strong>Christmas delivery cutoff: order by {dlong(cutoff)}.</strong> '
            'Japanese sealed is imported to order — orders after this date may not arrive before Christmas.</p>\n')


def with_block(html, cutoff, remove=False):
    html = BLOCK_RE.sub('', html or '')
    return html if remove else block(cutoff) + html


def fetch(http):
    d = shopify_gql(http, """query{ products(first:100, query:"product_type:'Sealed Product' AND status:active AND tag:japanese"){
        nodes{ id handle title descriptionHtml } }
        collectionByHandle(handle:"%s"){ id title descriptionHtml } }""" % COLLECTION_HANDLE, {})
    return d['products']['nodes'], d['collectionByHandle']


def run(apply=False, remove=False):
    http = Http()
    cutoff = date.fromisoformat(config()['christmas_cutoff'])
    products, coll = fetch(http)
    backup = ROOT / 'shopify-backup' / f'sealed-descriptions-{datetime.now():%Y%m%d-%H%M}.json'
    backup.parent.mkdir(exist_ok=True)
    backup.write_text(json.dumps({'products': products, 'collection': coll}, indent=1, ensure_ascii=False),
                      encoding='utf-8')
    ex = products[0]
    print(f'{len(products)} live Japanese sealed products + collection "{coll["title"]}". Backup: {backup.name}')
    print(f'\nExample — {ex["title"]}\n--- new description starts with ---\n'
          f'{with_block(ex["descriptionHtml"], cutoff, remove)[:400]}\n')
    if not apply:
        print('Dry run only. Re-run with --apply to write all of them.')
        return 0
    n = 0
    for p in products:
        r = shopify_gql(http, """mutation($p: ProductUpdateInput!){ productUpdate(product: $p){
            product{ id } userErrors{ field message } } }""",
                        {'p': {'id': p['id'], 'descriptionHtml': with_block(p['descriptionHtml'], cutoff, remove)}})
        errs = r['productUpdate']['userErrors']
        print(('  ok   ' if not errs else f'  FAIL {errs} ') + p['handle'])
        n += not errs
    r = shopify_gql(http, """mutation($c: CollectionInput!){ collectionUpdate(input: $c){
        collection{ id } userErrors{ field message } } }""",
                    {'c': {'id': coll['id'], 'descriptionHtml': with_block(coll['descriptionHtml'], cutoff, remove)}})
    print('  collection:', r['collectionUpdate']['userErrors'] or 'ok')
    print(f'{n}/{len(products)} products updated')
    return n
