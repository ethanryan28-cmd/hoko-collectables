"""cloud-run tests: dry-run summary shape, 7 h late window, NOT CONFIGURED handling, `env` output, .gitignore."""

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest import mock

from tools.social import __main__ as cli
from tools.social import cloud_run, config as C, queue_builder as qb, runner
from tools.social.assets import load as load_assets
from tools.social.http import Response
from tools.social.schedule import LATE_GRACE, TZ, parse

START = date(2026, 10, 18)
ASSETS = load_assets(START)
NO_KEYS = {k: '' for k in C.KEYS}      # '' counts as unset for config.get
WEBHOOK = 'https://discord.example/api/webhooks/42/secret-token-value'


def build(n=15):
    return qb.build(start=START, n_days=n, assets=ASSETS)


class FakeHttp:
    def __init__(self):
        self.calls = []

    def request(self, method, url, **kw):
        self.calls.append((method, url.split('?')[0]))
        return Response(200, {}, '{"id": "777"}')

    def get(self, url, **kw):
        return self.request('GET', url, **kw).json()

    def post(self, url, **kw):
        return self.request('POST', url, **kw).json()


class Paths:
    """Temp CSV / runner log / queue so tests never touch data/ or content/social-queue.json."""

    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.csv, self.log, self.queue = d / 'post-log.csv', d / 'runner.log', d / 'queue.json'

    def kw(self):
        return dict(csv_path=self.csv, log_path=self.log, queue_path=self.queue, do_render=False, out=None)


class DryRunSummary(unittest.TestCase):
    def setUp(self):
        self.p = Paths()
        self.q = build()
        self.now = datetime.combine(START, datetime.min.time(), tzinfo=TZ) + timedelta(hours=12, minutes=30)

    def tearDown(self):
        self.p.tmp.cleanup()

    def test_shape_and_values_with_no_keys(self):
        with mock.patch.dict(os.environ, NO_KEYS):
            s = cloud_run.run(dry_run=True, now=self.now, queue=self.q, **self.p.kw())
        for k in ('platforms', 'queue_days_per_platform', 'invalid', 'rendered', 'hosted', 'would_post', 'late_window_hours'):
            self.assertIn(k, s)
        self.assertEqual(set(s['platforms']), set(C.PLATFORM_ORDER))
        self.assertTrue(all(v == 'NOT CONFIGURED' for v in s['platforms'].values()))
        self.assertEqual(s['late_window_hours'], 7)
        self.assertEqual(s['invalid']['count'], 0, s['invalid']['list'][:5])
        self.assertEqual(s['invalid']['count'], len(s['invalid']['list']))
        self.assertIsInstance(s['rendered'], list)
        self.assertEqual(s['hosted'], [])
        self.assertEqual(s['would_post'], 0)        # nothing configured → nothing would post
        self.assertGreater(sum(s['due_unconfigured'].values()), 0)   # …but items are due at 12:30
        for p in ('youtube', 'instagram', 'facebook', 'pinterest', 'discord', 'tiktok_queue'):
            self.assertGreaterEqual(s['queue_days_per_platform'][p], 14)
        json.dumps(s, default=str)                   # serialisable
        self.assertTrue(self.p.csv.exists() and self.p.log.exists())
        self.assertEqual(self.p.csv.read_text().strip(), ','.join(runner.LOG_FIELDS))   # header only, no posts

    def test_configured_platform_counts_as_would_post(self):
        with mock.patch.dict(os.environ, dict(NO_KEYS, DISCORD_WEBHOOK_PICKUPS=WEBHOOK)):
            s = cloud_run.run(dry_run=True, now=self.now.replace(hour=17, minute=5), queue=self.q, **self.p.kw())
        self.assertEqual(s['platforms']['discord'], 'configured')
        self.assertEqual(s['would_post'], 1)
        self.assertNotIn('secret-token-value', self.p.log.read_text())

    def test_late_window_env_override(self):
        with mock.patch.dict(os.environ, dict(NO_KEYS, SOCIAL_LATE_WINDOW_HOURS='3')):
            s = cloud_run.run(dry_run=True, now=self.now, queue=self.q, **self.p.kw())
        self.assertEqual(s['late_window_hours'], 3)


class LateWindow(unittest.TestCase):
    def item(self, platform, slot):
        return {'id': f'{platform}:x', 'platform': platform, 'slot': slot.isoformat()}

    def test_seven_hour_window(self):
        now = datetime(2026, 10, 18, 20, 0, tzinfo=TZ)
        g = cloud_run.late_window()
        self.assertEqual(g, timedelta(hours=7))
        self.assertEqual(runner.action(self.item('discord', now - timedelta(hours=6, minutes=30)), now, g), 'send')
        self.assertEqual(runner.action(self.item('discord', now - timedelta(hours=7, minutes=30)), now, g), 'stale')
        # PC runner keeps its 6 h default
        self.assertEqual(runner.action(self.item('discord', now - timedelta(hours=6, minutes=30)), now), 'stale')
        self.assertEqual(LATE_GRACE, timedelta(hours=6))

    def test_live_run_posts_inside_window_skips_outside(self):
        p = Paths()
        try:
            q = build(n=2)
            day = START.isoformat()
            a, b, c = [i for i in q['items'] if i['platform'] == 'pinterest' and i['slot'].startswith(day)]  # 10:00 15:00 20:00
            now = parse(b['slot']) + timedelta(hours=6, minutes=50)   # a is 11 h 50 past (stale), b 6 h 50 (late window), c due
            h = FakeHttp()
            with mock.patch.dict(os.environ, dict(NO_KEYS, PINTEREST_TOKEN='pin-secret', PINTEREST_BOARD_ID='b1')):
                s = cloud_run.run(now=now, queue={'items': [a, b, c]}, http=h, **p.kw())
            self.assertEqual(len(h.calls), 2)
            rows = {r['item_id']: r['status'] for r in runner.read_log(p.csv)}
            self.assertEqual((rows[a['id']], rows[b['id']], rows[c['id']]), ('SKIP', 'OK', 'OK'))
            self.assertEqual(s['posted']['pinterest'], {'OK': 2, 'SKIP': 1})
            self.assertNotIn('pin-secret', p.csv.read_text() + p.log.read_text())
        finally:
            p.tmp.cleanup()


class NotConfigured(unittest.TestCase):
    def test_live_run_with_no_keys_posts_nothing_and_does_not_fail(self):
        p = Paths()
        try:
            q = build(n=2)
            now = parse(q['items'][0]['slot']) + timedelta(minutes=1)
            h = FakeHttp()
            with mock.patch.dict(os.environ, NO_KEYS):
                s = cloud_run.run(now=now, queue=q, http=h, **p.kw())
            self.assertEqual(h.calls, [])
            self.assertEqual(s['would_post'], 0)
            self.assertTrue(all(v == 'NOT CONFIGURED' for v in s['platforms'].values()))
            self.assertTrue(all('NOT CONFIGURED' in k for k in s['posted']), s['posted'])
            self.assertEqual([r for r in runner.read_log(p.csv) if r['status'] == 'OK'], [])
            self.assertIn('discord: NOT CONFIGURED', p.log.read_text())
        finally:
            p.tmp.cleanup()

    def test_hosting_not_configured_hosts_nothing(self):
        it = {'id': 'instagram:x', 'platform': 'instagram', 'media': 'content/youtube/reels/sealed/1/h1.mp4'}
        lines = []
        with mock.patch.dict(os.environ, NO_KEYS):
            self.assertEqual(cloud_run.host([it], None, lines.append), [])
        self.assertTrue(any('hosting NOT CONFIGURED' in x for x in lines))


class EnvCommand(unittest.TestCase):
    def run_cli(self, argv, env):
        buf = io.StringIO()
        with mock.patch.dict(os.environ, env), redirect_stdout(buf):
            rc = cli.main(argv)
        return rc, buf.getvalue()

    def test_all_missing(self):
        rc, out = self.run_cli(['env'], NO_KEYS)
        self.assertEqual(rc, 0)
        lines = out.strip().splitlines()
        self.assertEqual([l.split(':')[0] for l in lines], C.PLATFORM_ORDER)
        self.assertIn('instagram: MISSING META_PAGE_TOKEN, IG_BUSINESS_ID, SHOPIFY_STORE, SHOPIFY_ADMIN_TOKEN', lines)
        self.assertIn('tiktok_queue: MISSING DISCORD_WEBHOOK_TIKTOK_QUEUE', lines)
        self.assertIn('shopify_files: MISSING SHOPIFY_STORE, SHOPIFY_ADMIN_TOKEN', lines)
        self.assertTrue(lines[-2].startswith('tiktok: MISSING TIKTOK_ENABLED, TIKTOK_CLIENT_KEY'))

    def test_set_and_never_prints_values(self):
        env = dict(NO_KEYS, DISCORD_WEBHOOK_PICKUPS=WEBHOOK, SHOPIFY_STORE='x.myshopify.com', SHOPIFY_ADMIN_TOKEN='shpat_secret')
        rc, out = self.run_cli(['env'], env)
        self.assertEqual(rc, 0)
        self.assertIn('discord: set', out)
        self.assertIn('shopify_files: set', out)
        self.assertIn('instagram: MISSING META_PAGE_TOKEN, IG_BUSINESS_ID', out)
        for secret in (WEBHOOK, 'shpat_secret', 'x.myshopify.com'):
            self.assertNotIn(secret, out)
        rc, out = self.run_cli(['env', '--keys'], env)
        self.assertEqual(rc, 0)
        self.assertNotIn('shpat_secret', out)


class GitIgnore(unittest.TestCase):
    def test_cloud_logs_are_committable_others_still_ignored(self):
        lines = [l.strip() for l in (C.REPO / '.gitignore').read_text(encoding='utf-8').splitlines()]
        self.assertNotIn('data/social-post-log.csv', lines)
        self.assertNotIn('data/social-runner.log', lines)
        self.assertNotIn('data/', lines)
        self.assertIn('data/social-media-cache.json', lines)
        self.assertIn('data/social-dryrun.json', lines)


class RenderPlan(unittest.TestCase):
    def test_plan_groups_commands(self):
        missing = ['content/youtube/reels/sealed/123/h1.mp4', 'content/youtube/reels/slab/9/h0.mp4',
                   'content/youtube/reels/tips/buyback.mp4', 'content/youtube/reels/beats/2026-11-27.mp4',
                   'content/youtube/out/vid/short_1.mp4']
        cmds, cannot = cloud_run.render_plan(missing)
        self.assertEqual(cannot, ['content/youtube/out/vid/short_1.mp4'])
        self.assertEqual([c[0][1:] for c in cmds], [['reel', 'sealed', '123', '--hook', '1'],
                                                   ['reel', 'slab', '9', '--hook', '0'], ['calendar']])
        self.assertEqual(cmds[2][1], missing[2:4])

    def test_dry_render_lists_without_rendering(self):
        lines = []
        rendered, cannot = cloud_run.render(['content/youtube/reels/sealed/123/h1.mp4'], lines.append, dry=True)
        self.assertEqual(rendered, ['content/youtube/reels/sealed/123/h1.mp4'])
        self.assertTrue(any('would render' in x for x in lines))


if __name__ == '__main__':
    unittest.main()
