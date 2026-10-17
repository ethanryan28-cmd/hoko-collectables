"""phone-pack tests: day selection (Melbourne, fall-forward), raw.githubusercontent URL building, CSV log,
--days, log dedupe, save-line env toggle."""

import csv
import io
import os
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
            self.assertEqual(len(rows), 1 + 3)              # header once, 3 rows; the re-run is deduped
            self.assertEqual(rows[1], ['2026-10-20', 'tiktok_queue', 'a/1', UrlBuilding.BASE + 'content/x/1.mp4'])


def run(days=None, date_='2026-10-19', log=None, env=None):
    buf = io.StringIO()
    a = SimpleNamespace(date=date_) if days is None else SimpleNamespace(date=date_, days=days)
    with mock.patch('tools.social.queue_builder.load_queue', return_value={'items': ITEMS}), \
            mock.patch.dict(os.environ, env or {}, clear=False), redirect_stdout(buf):
        if env is None:
            os.environ.pop('PHONE_PACK_FILES_FIRST', None)
        rc = pp.main(a, log_path=log)
    return rc, buf.getvalue()


def log_rows(log):
    return list(csv.reader(log.open(encoding='utf-8')))[1:]


class Days(unittest.TestCase):
    def test_days_2_prints_two_headings_and_logs_both(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / 'log.csv'
            rc, md = run(days=2, log=log)
            self.assertEqual(rc, 0)
            self.assertEqual([l for l in md.splitlines() if l.startswith('# ')],
                             ['# HOKO phone pack · 2026-10-20', '# HOKO phone pack · 2026-10-22'])
            self.assertIn('## Instagram 10:30 · Four', md)
            self.assertEqual(sorted({r[0] for r in log_rows(log)}), ['2026-10-20', '2026-10-22'])
            self.assertEqual(len(log_rows(log)), 4)

    def test_days_1_matches_default(self):
        with tempfile.TemporaryDirectory() as d:
            _, md1 = run(days=1, log=Path(d) / 'a.csv')
            _, md0 = run(log=Path(d) / 'b.csv')
            self.assertEqual(md1, md0)
            self.assertEqual(md1.count('# HOKO phone pack'), 1)
            self.assertEqual(log_rows(Path(d) / 'a.csv'), log_rows(Path(d) / 'b.csv'))

    def test_date_plus_days_starts_from_date(self):
        with tempfile.TemporaryDirectory() as d:
            _, md = run(days=5, date_='2026-10-21', log=Path(d) / 'l.csv')
            self.assertEqual([l for l in md.splitlines() if l.startswith('# ')], ['# HOKO phone pack · 2026-10-22'])

    def test_rerun_prints_but_does_not_reappend(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / 'log.csv'
            _, first = run(days=2, log=log)
            _, second = run(days=2, log=log)
            self.assertEqual(first, second)
            self.assertEqual(len(log_rows(log)), 4)
            # a new day on the third run appends only the new rows
            run(days=1, date_='2026-10-20', log=log)
            self.assertEqual(len(log_rows(log)), 4)


class SaveLine(unittest.TestCase):
    def test_default_line(self):
        with tempfile.TemporaryDirectory() as d:
            _, md = run(log=Path(d) / 'l.csv')
            self.assertIn('# HOKO phone pack · 2026-10-20\n\nTap mp4 → share → Save Video → post.\n', md)
            self.assertNotIn('Files', md)

    def test_files_first_env(self):
        with tempfile.TemporaryDirectory() as d:
            _, md = run(log=Path(d) / 'l.csv', env={'PHONE_PACK_FILES_FIRST': '1'})
            self.assertIn('# HOKO phone pack · 2026-10-20\n\nTap mp4 → Files → Share → Save Video → post.\n', md)

    def test_other_env_value_keeps_default(self):
        with tempfile.TemporaryDirectory() as d:
            _, md = run(log=Path(d) / 'l.csv', env={'PHONE_PACK_FILES_FIRST': '0'})
            self.assertIn('Tap mp4 → share → Save Video → post.', md)


if __name__ == '__main__':
    unittest.main()
