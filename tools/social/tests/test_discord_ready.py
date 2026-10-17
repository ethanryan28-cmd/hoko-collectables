"""Discord readiness: DISCORD_WEBHOOK_URL (old DISCORD_WEBHOOK_PICKUPS still read), dry-run preview of the next 3."""

import os
import re
import unittest
from datetime import datetime
from unittest import mock

from tools.social import config as C
from tools.social import runner
from tools.social.publishers import discord
from tools.social.schedule import TZ

NO_KEYS = {k: '' for k in C.KEYS}
HOOK = 'https://discord.example/api/webhooks/1/secret'
NOW = datetime(2026, 10, 18, 9, 0, tzinfo=TZ)


def item(day, n):
    return {'id': f'discord:{day}', 'platform': 'discord', 'slot': f'{day}T17:00:00+11:00', 'asset_id': f'product/{n}',
            'media_type': 'image', 'media': '', 'image_url': f'https://cdn.example/{n}.jpg',
            'link': f'https://www.hokocollectables.com/products/p{n}', 'name': f'Box {n}',
            'title': f'Box {n}: sealed Japanese booster box', 'caption': f'Line one {n}.\nLine two {n}.'}


ITEMS = [item('2026-10-17', 0), item('2026-10-18', 1), item('2026-10-19', 2), item('2026-10-20', 3),
         item('2026-10-21', 4)]


class Env(unittest.TestCase):
    def test_reads_webhook_url(self):
        with mock.patch.dict(os.environ, dict(NO_KEYS, DISCORD_WEBHOOK_URL=HOOK)):
            self.assertEqual(C.missing('discord'), [])
            self.assertTrue(runner.configured('discord'))

    def test_old_name_still_read(self):
        with mock.patch.dict(os.environ, dict(NO_KEYS, DISCORD_WEBHOOK_PICKUPS=HOOK)):
            self.assertEqual(C.get('DISCORD_WEBHOOK_URL'), HOOK)

    def test_new_name_wins(self):
        with mock.patch.dict(os.environ, dict(NO_KEYS, DISCORD_WEBHOOK_URL=HOOK, DISCORD_WEBHOOK_PICKUPS='https://old')):
            self.assertEqual(C.get('DISCORD_WEBHOOK_URL'), HOOK)

    def test_missing_reports_new_name(self):
        with mock.patch.dict(os.environ, NO_KEYS):
            self.assertEqual(C.missing('discord'), ['DISCORD_WEBHOOK_URL'])
            self.assertIn('discord: MISSING DISCORD_WEBHOOK_URL', C.platform_lines())


class Preview(unittest.TestCase):
    def test_not_configured_does_not_fail(self):
        with mock.patch.dict(os.environ, NO_KEYS):
            lines = discord.preview(ITEMS, NOW)
        self.assertEqual(lines[0], 'Discord next 3 · NOT CONFIGURED (DISCORD_WEBHOOK_URL missing)')

    def test_next_three_future_items_text_and_link(self):
        with mock.patch.dict(os.environ, dict(NO_KEYS, DISCORD_WEBHOOK_URL=HOOK)):
            lines = discord.preview(ITEMS, NOW)
        self.assertEqual(lines[0], 'Discord next 3 · would post')
        heads = [l for l in lines if l.startswith('- ')]
        self.assertEqual(heads, ['- 2026-10-18T17:00 · Box 1: sealed Japanese booster box',
                                 '- 2026-10-19T17:00 · Box 2: sealed Japanese booster box',
                                 '- 2026-10-20T17:00 · Box 3: sealed Japanese booster box'])
        self.assertIn('    Line two 2.', lines)
        self.assertIn('    link: https://www.hokocollectables.com/products/p3', lines)
        self.assertNotIn(HOOK, '\n'.join(lines))

    def test_dry_run_prints_preview_without_env(self):
        out = []
        with mock.patch.dict(os.environ, NO_KEYS):
            rep = runner.dry_run(now=NOW, queue={'items': ITEMS}, out=out.append, write=False)
        self.assertEqual(rep['platforms']['discord']['invalid'], 0)
        self.assertIn('Discord next 3 · NOT CONFIGURED (DISCORD_WEBHOOK_URL missing)', out)

    def test_real_queue_preview_has_no_price(self):
        with mock.patch.dict(os.environ, NO_KEYS):
            q = runner.load_queue()
            lines = discord.preview(q['items'], NOW) if q else []
        self.assertFalse([l for l in lines if re.search(r'\$\s?\d', l)])


if __name__ == '__main__':
    unittest.main()
