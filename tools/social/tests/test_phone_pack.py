"""phone-pack tests: day selection (Melbourne, fall-forward), raw.githubusercontent URL building, CSV log."""

import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools.social import phone_pack as pp


def item(platform, slot, **kw):
    it = {'platform': platform, 'slot': slot}
    if platform == 'tiktok_queue':
        it['clips'] = kw.pop('clips', [{'asset_id': 'a/1', 'media': 'content/x/1.mp4', 'name': 'One',
                                        'link': 'https://l/1', 'caption': 'cap one'}])
    it.update(kw)
    return it


ITEMS = [
    item('pinterest', '2026-10-18T10:00:00+11:00'),
    item('tiktok_queue', '2026-10-20T07:00:00+11:00'),
    item('instagram', '2026-10-20T19:15:00+11:00', asset_id='b/2', media_type='video', media='content/x/2.mp4',
         name='Two', link='https://l/2', caption='cap two\nline 2'),
    item('instagram', '2026-10-20T12:15:00+11:00', asset_id='b/3', media_type='video', media='content/x/3.mp4',
         name='Three', link='https://l/3', caption='cap three'),
    # 23:30 UTC on the 21st is 10:30 on the 22nd in Melbourne
    item('instagram', '2026-10-21T23:30:00+00:00', asset_id='b/4', media_type='image', image_url='https://img/4.jpg',
         name='Four', link='https://l/4', caption='cap four'),
]


class DateSelection(unittest.TestCase):
    def test_today_with_items(self):
        self.assertEqual(pp.pick_day(ITEMS, date(2026, 10, 20)), date(2026, 10, 20))

    def test_falls_forward_to_next_day_with_items(self):
        # the 18th only has pinterest; the 19th has nothing
        self.assertEqual(pp.pick_day(ITEMS, date(2026, 10, 18)), date(2026, 10, 20))

    def test_melbourne_day_not_utc(self):
        self.assertEqual(pp.pick_day(ITEMS, date(2026, 10, 21)), date(2026, 10, 22))

    def test_nothing_ahead(self):
        self.assertIsNone(pp.pick_day(ITEMS, date(2026, 10, 23)))

    def test_entries_slot_order_and_shape(self):
        rows = pp.entries(ITEMS, date(2026, 10, 20))
        self.assertEqual([(r['platform'], r['slot']) for r in rows],
                         [('tiktok_queue', '07:00'), ('instagram', '12:15'), ('instagram', '19:15')])
        self.assertEqual(rows[2]['caption'], 'cap two\nline 2')


class UrlBuilding(unittest.TestCase):
    BASE = 'https://raw.githubusercontent.com/ethanryan28-cmd/hoko-collectables/main/'

    def test_repo_relative(self):
        self.assertEqual(pp.raw_url('content/youtube/reels/tips/buyback.mp4'),
                         self.BASE + 'content/youtube/reels/tips/buyback.mp4')

    def test_leading_dot_slash_and_backslashes(self):
        self.assertEqual(pp.raw_url('./content\\x\\1.mp4'), self.BASE + 'content/x/1.mp4')
        self.assertEqual(pp.raw_url('/content/x/1.mp4'), self.BASE + 'content/x/1.mp4')

    def test_empty(self):
        self.assertEqual(pp.raw_url(''), '')

    def test_image_item_uses_image_url(self):
        rows = pp.entries(ITEMS, date(2026, 10, 22))
        self.assertEqual(rows[0]['url'], 'https://img/4.jpg')


class MainAndLog(unittest.TestCase):
    def test_markdown_and_csv(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / 'phone-pack-log.csv'
            buf = io.StringIO()
            with mock.patch('tools.social.queue_builder.load_queue', return_value={'items': ITEMS}), redirect_stdout(buf):
                for _ in range(2):
                    self.assertEqual(pp.main(SimpleNamespace(date='2026-10-19'), log_path=log), 0)
            md = buf.getvalue()
            self.assertIn('# HOKO phone pack · 2026-10-20', md)
            self.assertIn('## Instagram 12:15 · Three', md)
            self.assertIn('```\ncap two\nline 2\n```', md)
            self.assertIn(UrlBuilding.BASE + 'content/x/1.mp4', md)
            rows = list(csv.reader(log.open(encoding='utf-8')))
            self.assertEqual(rows[0], pp.LOG_HEADER)
            self.assertEqual(len(rows), 1 + 3 * 2)          # header once, then 3 rows per run
            self.assertEqual(rows[1], ['2026-10-20', 'tiktok_queue', 'a/1', UrlBuilding.BASE + 'content/x/1.mp4'])


if __name__ == '__main__':
    unittest.main()
