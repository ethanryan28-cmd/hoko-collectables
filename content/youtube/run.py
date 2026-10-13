#!/usr/bin/env python3
"""HOKO content machine — one entry point. See README.md for one line per command.

Run from anywhere: python content/youtube/run.py <command> ...
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hoko.common import load_env  # noqa: E402


def main():
    load_env()
    ap = argparse.ArgumentParser(prog='run.py')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('source', help='Refresh sealed/source.csv + slabs/source.csv from the Shopify Admin API')

    p = sub.add_parser('reel', help='Build reels: reel <sealed|slab> <id|handle|all>')
    p.add_argument('kind', choices=['sealed', 'slab'])
    p.add_argument('which', nargs='?', default='all')
    p.add_argument('--force', action='store_true', help='re-render even if the mp4 exists')
    p.add_argument('--hook', type=int, action='append', help='only this hook index (repeatable)')

    p = sub.add_parser('shorts', help='Cut inbox/*.mp4 long-form into vertical Shorts')
    p.add_argument('--model', default='small', help='faster-whisper model size')

    p = sub.add_parser('package', help='3 titles + 3 thumbnails for a long-form video')
    p.add_argument('video', help='inbox file name or path')

    p = sub.add_parser('calendar', help='Rebuild calendar.md (14 Oct → 24 Dec), CUTOFF.md, dated captions')

    p = sub.add_parser('publish', help="Post today's queued calendar item to Instagram + YouTube Shorts")
    p.add_argument('--dry-run', action='store_true', help='mock API calls (no network); still updates calendar')
    p.add_argument('--date', help='pretend today is YYYY-MM-DD')

    p = sub.add_parser('comments', help='Pull YouTube comments → comments/queue.md with drafted replies')
    p.add_argument('--post', action='store_true', help='post only replies ticked APPROVE [x]')
    p.add_argument('--dry-run', action='store_true', help='use mocked API responses')

    p = sub.add_parser('cutoff', help='Add the Christmas cutoff line to sealed product + collection descriptions')
    p.add_argument('--apply', action='store_true', help='write (default: dry run, shows one example)')
    p.add_argument('--remove', action='store_true', help='strip the cutoff line again')

    p = sub.add_parser('schedule', help='Register Windows Task Scheduler job "HOKO publish" (18:30 daily)')
    p.add_argument('--print', action='store_true', help='only print the schtasks command')

    a = ap.parse_args()

    if a.cmd == 'source':
        from hoko import source
        source.refresh()
    elif a.cmd == 'reel':
        from hoko import reel
        built = reel.build(a.kind, a.which, force=a.force, hooks=a.hook)
        print(f'{len(built)} reel(s) ready')
    elif a.cmd == 'shorts':
        from hoko import shorts
        shorts.run_inbox(model=a.model)
    elif a.cmd == 'package':
        from hoko import shorts
        shorts.package(a.video)
    elif a.cmd == 'calendar':
        from hoko import calendar_gen
        calendar_gen.build()
    elif a.cmd == 'publish':
        from hoko import publish
        publish.run(dry_run=a.dry_run, when=a.date)
    elif a.cmd == 'comments':
        from hoko import comments
        comments.run(post=a.post, dry_run=a.dry_run)
    elif a.cmd == 'cutoff':
        from hoko import shopify_cutoff
        shopify_cutoff.run(apply=a.apply, remove=a.remove)
    elif a.cmd == 'schedule':
        from hoko import publish
        publish.register_task(print_only=a.print)


if __name__ == '__main__':
    main()
