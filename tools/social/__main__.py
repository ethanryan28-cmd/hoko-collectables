"""python -m tools.social <command>

  env        one line per platform: '<platform>: set' or '<platform>: MISSING KEY, KEY' (values never printed)
             --keys lists every key instead
  cloud-run  one unattended pass from Claude Code web: env → topup → render missing clips (fallback voice) →
             host → post with a 7 h late window → data/social-post-log.csv + data/social-runner.log
             --dry-run prints a JSON summary and makes no renders / uploads / posts
  build      rebuild content/social-queue.json from today, 14 days ahead (keeps nothing)
  topup      keep today+ items, append days up to 14 ahead (daily "HOKO Social Topup", 23:00)
  run        post / schedule what is due (every 15 min, "HOKO Social Runner"); --dry-run = validate only
  dry-run    validate every future payload for every platform → data/social-dryrun.json
  check      queue gate: ≥14 days per platform, no repeats (7 d; hot sets 2 d), hot-set share ≥ target, no banned words / prices
  phone-pack today's tiktok_queue clips + instagram items as markdown for the phone (Victoria day; next day
             with items if today has none) → stdout + data/phone-pack-log.csv. --date YYYY-MM-DD overrides today
  render     render any clip the next 14 days need (PC only: ffmpeg + content/youtube deps)
"""

import argparse
import subprocess
import sys
from datetime import date

from . import config as C


def main(argv=None):
    ap = argparse.ArgumentParser(prog='python -m tools.social')
    sub = ap.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('env')
    e.add_argument('--keys', action='store_true', help='one line per env key instead of per platform')
    b = sub.add_parser('build')
    b.add_argument('--start', help='YYYY-MM-DD (default today, Victoria)')
    t = sub.add_parser('topup')
    t.add_argument('--render', action='store_true', help='then render missing clips (PC)')
    r = sub.add_parser('run')
    r.add_argument('--dry-run', action='store_true')
    sub.add_parser('dry-run')
    sub.add_parser('check')
    sub.add_parser('render')
    pp = sub.add_parser('phone-pack')
    pp.add_argument('--date', help='YYYY-MM-DD (default today, Victoria)')
    cr = sub.add_parser('cloud-run')
    cr.add_argument('--dry-run', action='store_true', help='no renders / uploads / posts; print JSON summary')
    cr.add_argument('--render-limit', type=int, default=None, help='render at most N missing clips this pass')
    cr.add_argument('--no-render', action='store_true', help='skip rendering (report missing clips only)')
    a = ap.parse_args(argv)

    if a.cmd == 'env':
        print('\n'.join(C.env_report() if a.keys else C.platform_lines()))
        return 0
    if a.cmd == 'phone-pack':
        from . import phone_pack
        return phone_pack.main(a)
    if a.cmd == 'cloud-run':
        from . import cloud_run
        return cloud_run.main(a)
    from . import queue_builder as qb
    from .schedule import now
    today = now().date()
    if a.cmd == 'build':
        q = qb.build(start=date.fromisoformat(a.start) if a.start else today)
        qb.save_queue(q)
        print(f'{len(q["items"])} items → {C.QUEUE_PATH.relative_to(C.REPO)} · days per platform {qb.coverage(q)}')
        return 0
    if a.cmd == 'topup':
        q = qb.topup(start=today)
        print(f'{len(q["items"])} items · days per platform {qb.coverage(q)}')
        if a.render:
            return render(q)
        return 0
    if a.cmd == 'check':
        q = qb.load_queue()
        cov = {p: d for p, d in qb.coverage(q).items()}
        v = qb.violations(q)
        short = [p for p in ('youtube', 'instagram', 'facebook', 'pinterest', 'discord', 'tiktok_queue') if cov.get(p, 0) < 14]
        print(f'days per platform {cov}')
        hot = C.hot_config()
        hs = qb.hot_share(q, start=today)
        print(f'hot sets {hot["hot_sets"]} share target {hot["share"]:.0%} · '
              + ' · '.join(f'{p} {h}/{n} ({s:.0%})' for p, (h, n, s) in hs.items()))
        under = [p for p, (h, n, s) in hs.items() if p != 'all' and n and s < hot['share']] if hot['hot_sets'] else []
        for x in v:
            print('  ✗', x)
        ok = not v and not short and not under
        print('PASS' if ok else f'FAIL (short: {short}, violations: {len(v)}, hot share under target: {under})')
        return 0 if ok else 1
    if a.cmd in ('dry-run',) or (a.cmd == 'run' and a.dry_run):
        from . import runner
        rep = runner.dry_run()
        bad = sum(r['invalid'] for r in rep['platforms'].values())
        return 1 if bad else 0
    if a.cmd == 'run':
        from . import runner
        runner.run()
        return 0
    if a.cmd == 'render':
        return render(qb.load_queue())
    return 2


def render(q):
    """Render missing clips via the content machine (PC only)."""
    missing = {it['media'] for it in q['items'] if it.get('media_type') == 'video' and it.get('media')
               and not (C.REPO / it['media']).exists()}
    missing |= {c['media'] for it in q['items'] for c in it.get('clips', []) if not (C.REPO / c['media']).exists()}
    if not missing:
        print('all clips present')
        return 0
    print(f'{len(missing)} clip(s) missing — rendering via content/youtube/run.py')
    run = [sys.executable, str(C.YT_CONTENT / 'run.py')]
    cmds = []
    if any('/reels/sealed/' in m for m in missing):
        cmds.append(run + ['reel', 'sealed', 'all'])
    if any('/reels/slab/' in m for m in missing):
        cmds.append(run + ['reel', 'slab', 'all'])
    if any(x in m for m in missing for x in ('/reels/tips/', '/reels/roundups/', '/reels/beats/')):
        cmds.append(run + ['calendar'])
    rc = 0
    for c in cmds:
        print('→', ' '.join(c[1:]))
        rc |= subprocess.call(c)
    return rc


if __name__ == '__main__':
    sys.exit(main())
