"""Tests for tools/relist-reconcile.py with synthetic Seller Hub / Shopify exports (no live data)."""

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('relist', Path(__file__).resolve().parents[1] / 'relist-reconcile.py')
rr = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rr)

UNSOLD = '''"Seller Hub - Unsold listings report"
"Downloaded 17-Oct-26"

Item number,Title,Custom label (SKU),Current price,Available quantity,End date
111,Pikachu 27 Black Star Promo PSA 10,SLAB-PIKA27,AU $599.00,1,10-Oct-26
222,Abyss Eye M5 Japanese Booster Box No Shrink,DS-URA-M5-0004,AU $120.00,2,11-Oct-26
333,Charizard Base Set HGA 9,SLAB-CHAR,AU $450.00,1,12-Oct-26
444,MTG Myst'''+'''ery Pack 10 NM Cards,MYS-1,AU $15.00,5,12-Oct-26
555,Nami Alt Art BGS 10,SLAB-NAMI,AU $499.00,1,13-Oct-26
666,Riolu 113/198 Common Scarlet & Violet,poke000-236,AU $3.00,1,13-Oct-26
777,OP-12 Legacy of the Master Japanese Booster Box,DS-URA-OP12-0044,AU $240.00,1,14-Oct-26
777,OP-12 Legacy of the Master Japanese Booster Box,DS-URA-OP12-0044,AU $240.00,1,01-Oct-26
888,Magikarp Art Rare PSA 9,SLAB-MAGI,AU $450.00,1,14-Oct-26
'''
ACTIVE = '''Item number,Title,Custom label (SKU),Current price,Available quantity
999,Abyss Eye M5 Japanese Booster Box No Shrink,DS-URA-M5-0004,AU $120.00,2
'''
ORDERS = '''Sales record number,Order number,Item number,Item title,Custom label,Quantity,Sale date
1,05-1,555,Nami Alt Art BGS 10,SLAB-NAMI,1,15-Oct-26
'''
SHOPIFY = '''Handle,Title,SKU,Location,Available,On hand
pika,Pikachu 27 Black Star Promo PSA 10,SLAB-PIKA27,Victoria,1,1
abyss,Abyss Eye,DS-URA-M5-0004,Victoria,2,2
nami,Nami,SLAB-NAMI,Victoria,1,1
riolu,Riolu,POKE000-236,Victoria,0,0
op12,OP-12,DS-URA-OP12-0044,Victoria,2,2
'''


class Reconcile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        for name, body in (('u.csv', UNSOLD), ('a.csv', ACTIVE), ('o.csv', ORDERS), ('s.csv', SHOPIFY)):
            (d / name).write_text(body, encoding='utf-8')
        self.d = d
        rr.main(['--unsold', str(d / 'u.csv'), '--active', str(d / 'a.csv'), '--orders', str(d / 'o.csv'),
                 '--shopify', str(d / 's.csv'), '--out-dir', str(d / 'out')])
        self.conf = list(csv.DictReader(open(d / 'out' / 'relist-confirmed.csv', encoding='utf-8')))
        self.excl = list(csv.DictReader(open(d / 'out' / 'relist-excluded.csv', encoding='utf-8')))

    def tearDown(self):
        self.tmp.cleanup()

    def reason(self, item):
        return sorted(r['reason'] for r in self.excl if r['item_number'] == item)

    def test_confirmed(self):
        self.assertEqual(sorted(r['item_number'] for r in self.conf), ['111', '777'])

    def test_prices_unchanged(self):
        p = {r['item_number']: r['price'] for r in self.conf}
        self.assertEqual(p['111'], 'AU $599.00')
        self.assertEqual(p['777'], 'AU $240.00')

    def test_reasons(self):
        self.assertEqual(self.reason('222'), ['ALREADY_ACTIVE'])
        self.assertEqual(self.reason('333'), ['OUT_OF_SCOPE'])
        self.assertEqual(self.reason('444'), ['BANNED_WORDS'])
        self.assertEqual(self.reason('555'), ['SOLD_SINCE'])
        self.assertEqual(self.reason('666'), ['NO_SHOPIFY_STOCK'])
        self.assertEqual(self.reason('777'), ['DUPLICATE'])
        self.assertEqual(self.reason('888'), ['NOT_IN_SHOPIFY'])

    def test_quantity_capped_by_shopify(self):
        q = {r['item_number']: int(r['quantity']) for r in self.conf}
        self.assertEqual(q['777'], 1)

    def test_every_unsold_row_accounted_for(self):
        self.assertEqual(len(self.conf) + len(self.excl), 9)


if __name__ == '__main__':
    unittest.main()
