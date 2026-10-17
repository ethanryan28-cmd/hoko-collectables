"""Unit tests: queue rules, scheduling, captions canon, runner timing / idempotency / retries, dry-run.
Run: python -m unittest discover -s tools/social/tests -t .   (or: python -m pytest tools/social/tests)"""

import os
import tempfile
import unittest
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest import mock

from tools.social import captions as cap
from tools.social import config as C
from tools.social import queue_builder as qb
from tools.social import runner
from tools.social.assets import Asset, load as load_assets, strip_prices
from tools.social.http import Response
from tools.social.schedule import SLOTS, TIKTOK_PER_DAY, TZ, parse

START = date(2026, 10, 18)
ASSETS = load_assets(START)


def build(start=START, n=15, existing=None, assets=None):
    return qb.build(start=start, n_days=n, existing=existing, assets=ASSETS if assets is None else assets)


def entries(q, platform):
    for it in q['items']:
        if it['platform'] == platform:
            for e in (it.get('clips') or [it]):
                yield it, e


class TopupHotShare(unittest.TestCase):
    """Topup keeps past items; only today+ may count toward the hot share, or a hot-heavy past starves the new window."""

    def test_topup_window_meets_hot_share(self):
        hot = C.hot_config()
        for back in (1, 3, 7, 14):
            q0 = build(start=START - timedelta(days=back))
            q = build(start=START, existing=q0)
            for p, (h, n, s) in qb.hot_share(q, start=START).items():
                self.assertGreaterEqual(s, hot['share'], (back, p, h, n))


class QueueRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = build()

    def test_fourteen_days_every_platform(self):
        cov = qb.coverage(self.q)
        for p in SLOTS:
            self.assertGreaterEqual(cov.get(p, 0), 14, p)

    def test_no_violations(self):
        self.assertEqual(qb.violations(self.q), [])

    def test_no_clip_repeat_within_7_days_same_platform(self):
        hot = C.hot_config()
        for p in SLOTS:
            last = {}
            for it, e in sorted(entries(self.q, p), key=lambda x: x[0]['slot']):
                dt = parse(it['slot'])
                window = timedelta(days=hot['repeat_days']) if e.get('set_code') in hot['hot_sets'] else timedelta(days=7)
                if e['asset_id'] in last:
                    self.assertGreaterEqual(dt - last[e['asset_id']], window, (p, e['asset_id']))
                last[e['asset_id']] = dt

    def test_hot_sets_take_their_share_on_every_platform(self):
        hot = C.hot_config()
        self.assertEqual(hot['hot_sets'], ['M6a', 'EB-05', 'OP-18', 'M7', 'FB12'])
        share = qb.hot_share(self.q, start=START)
        for p, (h, n, s) in share.items():
            self.assertGreaterEqual(s, hot['share'], (p, h, n))
        # and every hot product is actually used somewhere
        used = {e.get('set_code') for it in self.q['items'] for e in (it.get('clips') or [it])}
        self.assertTrue(set(hot['hot_sets']) <= used, used)

    def test_bf_week_block(self):
        q = build(start=date(2026, 11, 20), n=11)
        self.assertEqual(qb.violations(q), [])
        for it in q['items']:
            day = it['slot'][:10]
            for e in (it.get('clips') or [it]):
                if not e.get('asset_id'):
                    continue
                link = e.get('link', '')
                self.assertTrue('/products/' in link or link.endswith('/collections/japan-direct-sealed'), (it['id'], link))
                text = e.get('caption', '')
                if it['platform'] == 'pinterest':
                    continue
                self.assertIn('BFDROP5', text, it['id'])
                self.assertEqual(cap.check(text), [], it['id'])
                if day < '2026-11-27':
                    self.assertIn('box drop list', text, it['id'])
        pins = [it for it in q['items'] if it['platform'] == 'pinterest']
        self.assertTrue(all('BFDROP5' in it['caption'] for it in pins))

    def test_bf_lines_only_in_bf_week(self):
        self.assertEqual(cap.bf_lines('2026-11-19'), [])
        self.assertEqual(cap.bf_lines('2026-12-01'), [])
        self.assertTrue(cap.bf_lines('2026-11-20'))
        self.assertTrue(cap.bf_lines('2026-11-30'))
        for d in ('2026-11-20', '2026-11-27'):
            for line in cap.bf_lines(d):
                self.assertEqual(cap.check(line), [], line)

    def test_slot_times_local(self):
        for p, times in SLOTS.items():
            got = Counter(parse(it['slot']).astimezone(TZ).strftime('%H:%M') for it in self.q['items'] if it['platform'] == p)
            self.assertEqual(set(got), set(times), p)
            for t in times:
                self.assertEqual(got[t], 15, (p, t))

    def test_offset_is_aedt_in_october(self):
        it = next(i for i in self.q['items'] if i['platform'] == 'instagram')
        self.assertTrue(it['slot'].endswith('+11:00'), it['slot'])

    def test_tiktok_three_clips_daily_at_7(self):
        packs = [i for i in self.q['items'] if i['platform'] == 'tiktok_queue']
        self.assertEqual(len(packs), 15)
        for p in packs:
            self.assertEqual(len(p['clips']), TIKTOK_PER_DAY)
            self.assertEqual(len({c['asset_id'] for c in p['clips']}), TIKTOK_PER_DAY)

    def test_facebook_mirrors_instagram(self):
        ig = {i['slot']: i['asset_id'] for i in self.q['items'] if i['platform'] == 'instagram'}
        fb = {i['slot']: i['asset_id'] for i in self.q['items'] if i['platform'] == 'facebook'}
        self.assertEqual(ig, fb)

    def test_one_product_per_platform_per_day(self):
        for p in ('youtube', 'instagram', 'pinterest', 'tiktok_queue'):
            seen = Counter()
            for it, e in entries(self.q, p):
                a = next(x for x in ASSETS if x.id == e['asset_id'])
                seen[(it['slot'][:10], a.product_id or a.id)] += 1
            self.assertLessEqual(max(seen.values()), 1, p)

    def test_only_eligible_assets(self):
        ok = {a.id for a in ASSETS if a.eligible}
        for it in self.q['items']:
            for e in (it.get('clips') or [it]):
                self.assertIn(e['asset_id'], ok)

    def test_pinterest_and_discord_use_images_linking_site(self):
        for it in self.q['items']:
            if it['platform'] in ('pinterest', 'discord'):
                self.assertTrue(it['image_url'].startswith('https://'))
                self.assertIn('hokocollectables.com/', it['link'])

    def test_japanese_sealed_weighted_heavier_in_november(self):
        nov = build(start=date(2026, 11, 2), n=14)
        dec = build(start=date(2026, 12, 7), n=14)
        byid = {a.id: a for a in ASSETS}

        def share(q):
            c = Counter(qb.category(byid[e['asset_id']]) for p in ('youtube', 'instagram', 'tiktok_queue')
                        for _, e in entries(q, p))
            return c['jp'] / sum(c.values())
        self.assertGreaterEqual(share(nov), 0.6)
        self.assertGreater(share(nov), share(dec))

    def test_beat_takes_first_video_slot_on_its_date(self):
        q = build(start=date(2026, 11, 20), n=10)
        for p in ('youtube', 'instagram'):
            first = min((i for i in q['items'] if i['platform'] == p and i['slot'].startswith('2026-11-27')),
                        key=lambda i: i['slot'])
            self.assertEqual(first['asset_id'], 'beat/2026-11-27')
        pack = next(i for i in q['items'] if i['platform'] == 'tiktok_queue' and i['slot'].startswith('2026-11-27'))
        self.assertEqual(pack['clips'][0]['asset_id'], 'beat/2026-11-27')

    def test_beat_on_draft_box_is_ineligible_and_skipped(self):
        # mark the 26 Nov beat's featured box DRAFT, whatever box the last render picked
        from tools.social import assets as A
        pid = next(a for a in ASSETS if a.id == 'beat/2026-11-26').product_id
        real = A.product_eligible
        with mock.patch.object(A, 'product_eligible',
                               side_effect=lambda r: (False, 'status DRAFT') if r and r.get('id') == pid else real(r)):
            assets = load_assets(START)
        beat = next(a for a in assets if a.id == 'beat/2026-11-26')
        self.assertFalse(beat.eligible)
        self.assertIn('featured box', beat.reason)
        q = build(start=date(2026, 11, 20), n=10, assets=assets)
        used = {e['asset_id'] for i in q['items'] for e in (i.get('clips') or [i]) if e.get('asset_id')}
        self.assertNotIn('beat/2026-11-26', used)
        self.assertIn('beat/2026-11-27', used)

    def test_topup_keeps_existing_and_extends(self):
        q1 = build(n=15)
        q2 = qb.build(start=START + timedelta(days=1), n_days=15, existing=q1, assets=ASSETS)
        old = {i['id']: i for i in q1['items'] if parse(i['slot']).date() >= START + timedelta(days=1)}
        new = {i['id']: i for i in q2['items']}
        for k, v in old.items():
            self.assertEqual(new[k], v)
        self.assertGreaterEqual(min(qb.coverage(q2).values()), 15)
        self.assertEqual(qb.violations({'items': q1['items'] + [i for i in q2['items'] if i['id'] not in old]}), [])

    def test_small_pool_reports_error_instead_of_repeating(self):
        few = [a for a in ASSETS if a.media_type == 'image'][:2] + [a for a in ASSETS if a.media_type == 'video'][:2]
        q = build(n=3, assets=few)
        self.assertTrue(any(i.get('error') for i in q['items'] if i['platform'] == 'pinterest'))
        self.assertEqual([v for v in qb.violations(q) if 'repeats' in v], [])


class Captions(unittest.TestCase):
    def test_every_caption_is_canon_clean(self):
        q = build()
        for it in q['items']:
            for e in (it.get('clips') or [it]):
                for f in ('caption', 'title', 'alt_text'):
                    self.assertEqual(cap.check(e.get(f, '')), [], (it['id'], f))

    def test_sign_off_on_every_caption(self):
        q = build()
        for it in q['items']:
            if it['platform'] in ('discord',):
                continue
            for e in (it.get('clips') or [it]):
                self.assertIn(cap.SIGN_OFF, e['caption'], it['id'])

    def test_check_catches_banned_and_prices(self):
        for bad in ('Catch us on What' + 'not', 'WHAT NOT tonight', 'myst' + 'ery pack drop', 'official store',
                    'officially licensed', 'Top ' + 'Rated seller', 'only $120', 'AUD 99', '50 dollars'):
            self.assertTrue(cap.check(bad), bad)
        self.assertEqual(cap.check('Collector first. Seller second. Victoria, Australia @hokocollectables'), [])
        self.assertTrue(cap.check('follow @someoneelse'))

    def test_strip_prices(self):
        self.assertEqual(strip_prices('Abyss Eye · no shrink — $120 on HOKO'), 'Abyss Eye · no shrink')
        self.assertEqual(strip_prices('Japanese sealed under $200'), 'Japanese sealed under')

    def test_youtube_title_limit(self):
        a = Asset(id='x', kind='tip', media_type='video', hook='A' * 150)
        t = cap.youtube_title(a)
        self.assertLessEqual(len(t), 100)
        self.assertTrue(t.endswith('#Shorts'))

    def test_buying_posts_carry_games_line(self):
        a = next(x for x in ASSETS if x.id == 'tip/buyback')
        self.assertIn(cap.GAMES_LINE, cap.caption(a, 'instagram', '2026-10-20'))


class FakeHttp:
    def __init__(self, fail=0):
        self.calls, self.fail = [], fail

    def request(self, method, url, **kw):
        self.calls.append((method, url.split('?')[0]))
        if self.fail:
            self.fail -= 1
            raise RuntimeError('boom 500')
        return Response(200, {'Location': 'https://upload.example/session'}, '{"id": "123"}')

    def get(self, url, **kw):
        return self.request('GET', url, **kw).json()

    def post(self, url, **kw):
        return self.request('POST', url, **kw).json()


class RunnerTiming(unittest.TestCase):
    def item(self, platform, slot):
        return {'id': f'{platform}:x', 'platform': platform, 'slot': slot.isoformat()}

    def test_actions(self):
        now = datetime(2026, 10, 18, 9, 0, tzinfo=TZ)
        A = runner.action
        self.assertEqual(A(self.item('youtube', now + timedelta(days=13)), now), 'send')
        self.assertEqual(A(self.item('youtube', now + timedelta(days=15)), now), 'wait')
        self.assertEqual(A(self.item('youtube', now + timedelta(minutes=2)), now), 'send-late')
        self.assertEqual(A(self.item('facebook', now + timedelta(hours=3)), now), 'send')
        self.assertEqual(A(self.item('facebook', now + timedelta(minutes=5)), now), 'send-late')
        self.assertEqual(A(self.item('instagram', now + timedelta(minutes=5)), now), 'wait')
        self.assertEqual(A(self.item('instagram', now - timedelta(minutes=5)), now), 'send')
        self.assertEqual(A(self.item('pinterest', now - timedelta(hours=7)), now), 'stale')


class RunnerLog(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = Path(self.tmp.name) / 'log.csv'
        q = build(n=2)
        self.q = {'items': [i for i in q['items'] if i['platform'] == 'discord']}
        self.now = parse(self.q['items'][0]['slot']) + timedelta(minutes=1)
        self.env = mock.patch.dict(os.environ, {'DISCORD_WEBHOOK_PICKUPS': 'https://discord.example/api/webhooks/1/x'})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_idempotent(self):
        h = FakeHttp()
        runner.run(now=self.now, http=h, queue=self.q, log_path=self.log, out=lambda *_: None)
        runner.run(now=self.now + timedelta(minutes=15), http=h, queue=self.q, log_path=self.log, out=lambda *_: None)
        self.assertEqual(len(h.calls), 1)
        rows = runner.read_log(self.log)
        self.assertEqual([r['status'] for r in rows], ['OK'])

    def test_two_retries_then_fail(self):
        h = FakeHttp(fail=99)
        for k in range(5):
            runner.run(now=self.now + timedelta(minutes=15 * k), http=h, queue=self.q, log_path=self.log, out=lambda *_: None)
        self.assertEqual([r['status'] for r in runner.read_log(self.log)], ['RETRY', 'RETRY', 'FAIL'])
        self.assertEqual(len(h.calls), 3)

    def test_retry_then_ok(self):
        h = FakeHttp(fail=1)
        for k in range(3):
            runner.run(now=self.now + timedelta(minutes=15 * k), http=h, queue=self.q, log_path=self.log, out=lambda *_: None)
        self.assertEqual([r['status'] for r in runner.read_log(self.log)], ['RETRY', 'OK'])

    def test_stale_is_skipped_not_posted(self):
        h = FakeHttp()
        runner.run(now=self.now + timedelta(hours=7), http=h, queue=self.q, log_path=self.log, out=lambda *_: None)
        self.assertEqual(h.calls, [])
        self.assertEqual(runner.read_log(self.log)[0]['status'], 'SKIP')

    def test_unconfigured_platform_waits(self):
        with mock.patch.dict(os.environ, {'DISCORD_WEBHOOK_URL': '', 'DISCORD_WEBHOOK_PICKUPS': ''}):
            h = FakeHttp()
            runner.run(now=self.now, http=h, queue=self.q, log_path=self.log, out=lambda *_: None)
        self.assertEqual(h.calls, [])
        self.assertEqual(runner.read_log(self.log), [])

    def test_log_never_contains_secret(self):
        h = FakeHttp(fail=1)
        runner.run(now=self.now, http=h, queue=self.q, log_path=self.log, out=lambda *_: None)
        self.assertNotIn('discord.example/api/webhooks/1/x', self.log.read_text())


class DryRun(unittest.TestCase):
    def test_every_platform_valid(self):
        q = build()
        now = datetime.combine(START, datetime.min.time(), tzinfo=TZ)
        rep = runner.dry_run(now=now, queue=q, out=lambda *_: None, write=False)
        for p in ('youtube', 'instagram', 'facebook', 'pinterest', 'discord', 'tiktok_queue', 'tiktok'):
            self.assertIn(p, rep['platforms'], p)
            self.assertGreater(rep['platforms'][p]['valid'], 0, p)
            self.assertEqual(rep['platforms'][p]['invalid'], 0, (p, rep['problems'][:5]))

    def test_youtube_publishat_in_past_is_invalid(self):
        from tools.social.publishers import youtube
        it = next(i for i in build(n=1)['items'] if i['platform'] == 'youtube')
        now = parse(it['slot']) + timedelta(hours=1)
        p = youtube.build(it, {'now': now, 'late': False})
        self.assertIn('publishAt is in the past', youtube.validate(p, it, {'now': now}))

    def test_facebook_needs_ten_minutes_lead(self):
        from tools.social.publishers import facebook
        it = next(i for i in build(n=1)['items'] if i['platform'] == 'facebook')
        now = parse(it['slot']) - timedelta(minutes=5)
        p = facebook.build(it, {'now': now, 'late': False, 'hosted_url': 'https://cdn.shopify.com/x.mp4'})
        self.assertTrue(any('600' in e for e in facebook.validate(p, it, {'now': now})))


if __name__ == '__main__':
    unittest.main()
