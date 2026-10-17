"""content/youtube/hoko/reel.py — no price in the on-screen hook, the voiceover or the pre-order card.

Ethan 17 Oct 2026: no prices anywhere in the video frame or voiceover. Runs every hook over the committed
sealed/source.csv + slabs/source.csv rows. No render, no network.
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
YT = REPO / 'content' / 'youtube'

try:
    sys.path.insert(0, str(YT))
    from hoko import reel
    from hoko.common import load_rows
except ImportError as e:   # numpy / Pillow missing
    reel = None
    _why = str(e)
finally:
    if sys.path and sys.path[0] == str(YT):
        sys.path.pop(0)


@unittest.skipIf(reel is None, 'reel.py deps not installed')
class NoPriceInReel(unittest.TestCase):
    def rows(self):
        return [('sealed', r) for r in load_rows('sealed')] + [('slab', r) for r in load_rows('slab')]

    def test_hook_text_has_no_dollar_for_every_kind_and_hook(self):
        n = 0
        for kind, row in self.rows():
            # every hook hook_text implements for this row (sealed h0 'gone' has no copy; h3/h4 need their column)
            if kind == 'slab':
                ks = range(len(reel.SLAB_HOOKS))
            else:
                ks = [1, 2] + ([3] if row.get('release_date') else []) + ([4] if row.get('chase') else [])
            for k in ks:
                hook, vo = reel.hook_text(row, kind, k)
                for text in (hook, vo):
                    self.assertNotIn('$', text, f'{kind} {row["id"]} h{k}: {text}')
                    self.assertNotIn('two fifty', text.lower(), f'{kind} {row["id"]} h{k}: {text}')
                n += 1
        self.assertGreater(n, 0)

    def test_preorder_body_has_no_dollar(self):
        pre = [r for k, r in self.rows() if k == 'sealed' and r.get('release_date')]
        self.assertTrue(pre)
        for row in pre:
            for line in reel.preorder_body(row):
                self.assertNotIn('$', line, f'{row["id"]}: {line}')


if __name__ == '__main__':
    unittest.main()
