"""cloud-run — one unattended pass of the poster from a Claude Code web session (no PC, no .env).

    python -m tools.social cloud-run [--dry-run] [--render-limit N] [--no-render]

What one pass does, in order:
  1. env       every key is read from the environment only. A platform with missing keys is reported
               NOT CONFIGURED and skipped; it never fails the run.
  2. topup     if any platform has fewer than MIN_QUEUED_DAYS queued, the queue is topped up to today + 14.
  3. render    clips the queue needs that are not on disk are rendered here via content/youtube/run.py
               (reel <kind> <id> --hook k, or `calendar` for tips / roundups / beats). The en-AU edge-tts voice
               cannot connect from the cloud, so the Piper voice is downloaded to content/youtube/.cache/piper/
               and every clip rendered with it is logged "fallback voice". Clips cut from source video
               (shorts / carddrop / social-bank) cannot be rendered here and are reported.
  4. host      clips due now for Instagram / Facebook (and TikTok API when enabled) are uploaded to Shopify
               Files (tools/social/hosting.py; needs SHOPIFY_STORE + SHOPIFY_ADMIN_TOKEN).
  5. post      runner.run with a 7 h late window (LATE_WINDOW_HOURS, env SOCIAL_LATE_WINDOW_HOURS): a slot that
               passed up to 7 h ago still goes out, because a daily cloud trigger cannot hit every 15-minute slot.
  6. log       data/social-post-log.csv (idempotency) + data/social-runner.log (this transcript). Both are
               committed to main at the end of each cloud run; they are created with headers if missing.

--dry-run does all of it except real renders, uploads and posts, and prints one JSON summary:
  platforms {name: configured|NOT CONFIGURED}, queue_days_per_platform, invalid {count, list}, rendered,
  hosted, would_post, late_window_hours (+ due_unconfigured, missing_media, cannot_render for context).
"""

import csv
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

from . import config as C
from . import hosting
from . import queue_builder as qb
from . import runner
from .schedule import PLATFORMS, now as now_tz

LATE_WINDOW_HOURS = 7          # default; env SOCIAL_LATE_WINDOW_HOURS overrides
MIN_QUEUED_DAYS = 10           # top up when any platform has fewer days queued than this
PIPER_VOICE = 'en_GB-alan-medium'
PIPER_DIR = C.YT_CONTENT / '.cache' / 'piper'
AU_VOICE_PREFIX = 'edge-tts:en-AU'
RUN_PY = C.YT_CONTENT / 'run.py'
REEL_RE = re.compile(r'content/youtube/reels/(sealed|slab)/(\d+)/h(\d+)\.mp4$')
CALENDAR_RE = re.compile(r'content/youtube/reels/(tips|roundups|beats)/[^/]+\.mp4$')


def late_window():
    try:
        hours = float(C.get('SOCIAL_LATE_WINDOW_HOURS', LATE_WINDOW_HOURS))
    except ValueError:
        hours = LATE_WINDOW_HOURS
    return timedelta(hours=hours)


class Log:
    """print + append to data/social-runner.log (one timestamped line each). Never receives secrets: callers
    pass messages built from key names, paths and ids only."""

    def __init__(self, path=None, echo=print):
        self.path = Path(path or C.RUNNER_LOG_PATH)
        self.echo = echo
        self.lines = []

    def __call__(self, msg):
        for line in str(msg).splitlines() or ['']:
            stamped = f'{now_tz().isoformat(timespec="seconds")} {line}'
            self.lines.append(stamped)
            if self.echo:
                self.echo(line)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(stamped + '\n')


def ensure_files(csv_path=None, log_path=None):
    """Create data/social-post-log.csv (header row) and data/social-runner.log if missing."""
    csv_path = Path(csv_path or C.LOG_PATH)
    log_path = Path(log_path or C.RUNNER_LOG_PATH)
    for p in (csv_path, log_path):
        p.parent.mkdir(parents=True, exist_ok=True)
    if not csv_path.exists():
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            csv.DictWriter(f, fieldnames=runner.LOG_FIELDS).writeheader()
    if not log_path.exists():
        log_path.touch()


def platform_status():
    return {p: 'configured' if not C.missing(p) else 'NOT CONFIGURED' for p in C.PLATFORM_ORDER}


# ------------------------------------------------------------------ media

def _medias(item):
    if item.get('error'):
        return []
    if item['platform'] == 'tiktok_queue':
        return [c['media'] for c in item.get('clips', []) if c.get('media')]
    if item.get('media_type') == 'video' and item.get('media'):
        return [item['media']]
    return []


def missing_media(q, now, grace):
    """Repo-relative mp4 paths the queue still needs (items not already stale), in slot order, deduped."""
    out, seen = [], set()
    for it in sorted(q['items'], key=lambda i: i['slot']):
        if runner.action(it, now, grace) == 'stale':
            continue
        for m in _medias(it):
            if m not in seen and not (C.REPO / m).exists():
                seen.add(m)
                out.append(m)
    return out


def render_plan(missing):
    """(commands, cannot) — one `reel <kind> <id> --hook k` per product clip, one `calendar` for the rest."""
    cmds, cannot, calendar = [], [], []
    for m in missing:
        mm = REEL_RE.search(m)
        if mm:
            kind, pid, k = mm.groups()
            cmds.append(([str(RUN_PY), 'reel', kind, pid, '--hook', k], [m]))
        elif CALENDAR_RE.search(m):
            calendar.append(m)
        else:
            cannot.append(m)
    if calendar:
        cmds.append(([str(RUN_PY), 'calendar'], calendar))
    return cmds, cannot


def render_deps():
    """List of what is missing for a cloud render (empty = can render)."""
    probs = []
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            probs.append(f'{tool} not on PATH')
    for mod in ('PIL', 'numpy', 'requests'):
        try:
            __import__(mod)
        except ImportError:
            probs.append(f'python module {mod} missing')
    try:
        __import__('piper')
    except ImportError:
        try:
            __import__('edge_tts')
        except ImportError:
            probs.append('no TTS engine (pip install piper-tts, or edge-tts)')
    return probs


def ensure_voice(log):
    """Make sure a Piper fallback voice exists and HOKO_PIPER_MODEL points at it. Returns the path or None."""
    m = C.get('HOKO_PIPER_MODEL')
    if m and Path(m).exists():
        return Path(m)
    onnx = PIPER_DIR / f'{PIPER_VOICE}.onnx'
    if not onnx.exists():
        try:
            __import__('piper')
        except ImportError:
            log('fallback voice unavailable: piper-tts not installed')
            return None
        PIPER_DIR.mkdir(parents=True, exist_ok=True)
        log(f'downloading fallback voice {PIPER_VOICE} → {PIPER_DIR.relative_to(C.REPO)}')
        r = subprocess.run([sys.executable, '-m', 'piper.download_voices', PIPER_VOICE, '--data-dir', str(PIPER_DIR)],
                           capture_output=True, text=True)
        if r.returncode != 0 or not onnx.exists():
            log(f'fallback voice download failed (rc {r.returncode}): {(r.stderr or r.stdout)[-300:]}')
            return None
    os.environ['HOKO_PIPER_MODEL'] = str(onnx)
    return onnx


def voice_used(media):
    """Engine recorded in the clip's sidecar json ('edge-tts:en-AU-…' or 'piper:en_GB-alan-medium')."""
    try:
        return json.loads((C.REPO / media).with_suffix('.json').read_text(encoding='utf-8')).get('tts', '')
    except (OSError, ValueError):
        return ''


def render(missing, log, limit=None, dry=False):
    """Render missing clips in the cloud. Returns (rendered paths, cannot-render paths)."""
    cmds, cannot = render_plan(missing)
    for m in cannot:
        log(f'cannot render here (needs the source video): {m}')
    if not cmds:
        return [], cannot
    if dry:
        planned = [m for _, ms in cmds for m in ms]
        log(f'dry-run: would render {len(planned)} clip(s) with the fallback voice')
        return planned[:limit] if limit else planned, cannot
    probs = render_deps()
    if probs:
        log('render skipped — ' + '; '.join(probs))
        return [], cannot + [m for _, ms in cmds for m in ms]
    ensure_voice(log)
    rendered, done = [], 0
    for cmd, medias in cmds:
        if limit is not None and done >= limit:
            break
        log('→ run.py ' + ' '.join(cmd[1:]))
        r = subprocess.run([sys.executable] + cmd, cwd=str(C.REPO), capture_output=True, text=True)
        if r.returncode != 0:
            log(f'render failed (rc {r.returncode}): {(r.stderr or r.stdout)[-400:]}')
        for m in medias:
            if (C.REPO / m).exists():
                v = voice_used(m)
                tag = '' if v.startswith(AU_VOICE_PREFIX) else ' — fallback voice'
                log(f'rendered {m} [{v or "voice unknown"}]{tag}')
                rendered.append(m)
                done += 1
    return rendered, cannot


# ------------------------------------------------------------------ hosting + posting

def due(q, now, grace, log_rows):
    """Items whose slot has arrived (send / send-late) and that are not already OK / FAIL / SKIP in the log."""
    st = runner.state(log_rows)
    out = []
    for it in runner.expand(q['items']):
        if it.get('error') or st.get(it['id'], ('', 0))[0] in ('OK', 'FAIL', 'SKIP'):
            continue
        if runner.action(it, now, grace) in ('send', 'send-late'):
            out.append(it)
    return out


def host(items, http, log, dry=False):
    """Upload clips due for IG / FB (and TikTok API when enabled) to Shopify Files. Returns hosted media paths."""
    need = []
    for it in items:
        if it['platform'] in ('instagram', 'facebook', 'tiktok') and it.get('media') and it['media'] not in need:
            need.append(it['media'])
    if not need:
        return []
    if C.missing('shopify_files'):
        log(f'hosting NOT CONFIGURED — {len(need)} clip(s) stay local')
        return []
    hosted = []
    for m in need:
        if not (C.REPO / m).exists():
            log(f'host skipped, media missing: {m}')
            continue
        if dry:
            hosted.append(m)
            continue
        try:
            hosting.public_url(http, m)
            hosted.append(m)
            log(f'hosted {m}')
        except Exception as e:   # noqa: BLE001 — logged, the runner will log RETRY for the item
            log(f'host failed {m}: {str(e)[:200]}')
    return hosted


# ------------------------------------------------------------------ one pass

def run(dry_run=False, now=None, queue=None, queue_path=qb.QUEUE_PATH, csv_path=None, log_path=None,
        http=None, render_limit=None, do_render=True, out=print):
    now = now or now_tz()
    grace = late_window()
    ensure_files(csv_path, log_path)
    log = Log(log_path, echo=out)
    log(f'cloud-run {"DRY-RUN " if dry_run else ""}start · late window {grace.total_seconds() / 3600:g} h')

    status = platform_status()
    for p, s in status.items():
        log(f'{p}: {s}')

    today = now.date()
    q = queue or qb.load_queue(queue_path)
    if q is None:
        log('no queue — building today + 14')
        q = qb.topup(start=today, path=queue_path)
    cov = qb.coverage(q)
    short = [p for p in PLATFORMS if cov.get(p, 0) < MIN_QUEUED_DAYS]
    if short:
        log(f'topup: {short} below {MIN_QUEUED_DAYS} days → extending to today + {qb.HORIZON - 1}')
        q = qb.build(start=today, existing=q)
        qb.save_queue(q, queue_path)
        cov = qb.coverage(q)
    log(f'queue days per platform {cov}')

    problems = list(qb.violations(q))
    rep = runner.dry_run(now=now, queue=q, out=lambda *_: None, write=not dry_run)
    problems += [x for x in rep['problems'] if x not in problems]
    log(f'invalid payloads / rule violations: {len(problems)}')
    for x in problems[:20]:
        log('  ✗ ' + x)

    missing = missing_media(q, now, grace)
    log(f'clips missing on disk: {len(missing)}')
    rendered, cannot = ([], missing) if not do_render else render(missing, log, limit=render_limit, dry=dry_run)

    log_rows = runner.read_log(csv_path)
    due_items = due(q, now, grace, log_rows)
    configured = [it for it in due_items if runner.configured(it['platform'])]
    unconfigured = [it for it in due_items if not runner.configured(it['platform'])]
    http = http or (runner.Http() if not dry_run else None)
    hosted = host(configured, http, log, dry=dry_run)
    log(f'due now: {len(due_items)} · on configured platforms: {len(configured)} · hosted: {len(hosted)}')

    posted = {}
    if not dry_run:
        posted = runner.run(now=now, http=http, queue=q, log_path=csv_path, out=log, grace=grace)
    summary = {
        'mode': 'dry-run' if dry_run else 'live',
        'now': now.isoformat(timespec='seconds'),
        'platforms': status,
        'queue_days_per_platform': cov,
        'invalid': {'count': len(problems), 'list': problems},
        'rendered': rendered,
        'hosted': hosted,
        'would_post': len(configured),
        'due_unconfigured': {p: sum(1 for it in unconfigured if it['platform'] == p)
                             for p in sorted({it['platform'] for it in unconfigured})},
        'missing_media': len(missing),
        'cannot_render': cannot,
        'late_window_hours': grace.total_seconds() / 3600,
        'posted': {k: (v if 'NOT CONFIGURED' in k else dict((s, v.count(s)) for s in sorted(set(v))))
                   for k, v in posted.items()},
        'log': str(Path(log_path or C.RUNNER_LOG_PATH)),
        'post_log': str(Path(csv_path or C.LOG_PATH)),
    }
    log('cloud-run end')
    return summary


def main(args):
    # transcript → stderr (and data/social-runner.log); the JSON summary alone → stdout
    s = run(dry_run=args.dry_run, render_limit=args.render_limit, do_render=not args.no_render,
            out=lambda m: print(m, file=sys.stderr))
    print(json.dumps(s, ensure_ascii=False, indent=1, default=str))
    return 1 if s['invalid']['count'] else 0
