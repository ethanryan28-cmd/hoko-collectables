# HOKO content machine

Reels from existing Shopify photos → BF/Christmas calendar → auto-publish to Instagram + YouTube Shorts.
Legit growth only: no bots, no bought engagement, nothing posts a reply without an approval tick.

Setup (once, on the PC): `pip install faster-whisper edge-tts google-api-python-client google-auth-oauthlib requests pillow numpy` + ffmpeg on PATH, copy `.env.example` → `.env` and fill it in.

| Command (run from repo root) | What it does |
|---|---|
| `python content/youtube/run.py source` | Refresh `sealed/source.csv` + `slabs/source.csv` from Shopify (read-only) |
| `python content/youtube/run.py reel sealed all` | Build every hook variant for every promotable sealed box → `reels/sealed/<id>/h<k>.mp4` + caption |
| `python content/youtube/run.py reel slab <id>` | Same for one slab (`all` for every slab); `--force` re-renders, `--hook N` picks one hook |
| `python content/youtube/run.py shorts` | `inbox/*.mp4` long-form → 3–5 vertical Shorts with burned captions → `out/<video>/short_N.mp4/.json` |
| `python content/youtube/run.py package <video>` | 3 title variants + 3 thumbnails (1280x720) → `out/<video>/package/` |
| `python content/youtube/run.py calendar` | Rebuild `calendar.md` (14 Oct → 24 Dec), `CUTOFF.md`, dated captions, BF/Christmas beat reels |
| `python content/youtube/run.py publish` | Post today's queued row to IG + YT Shorts, mark it posted, write `TODAY.md` for TikTok (`--dry-run` mocks APIs) |
| `python content/youtube/run.py comments` | Pull comments on last 10 YT videos → `comments/queue.md` with drafted replies + `APPROVE [ ]` |
| `python content/youtube/run.py comments --post` | Post only the replies you ticked `[x]` (drafts with `[FILL IN]` are skipped) |
| `python content/youtube/run.py cutoff` | Dry-run: show the Christmas-cutoff line on one sealed product; `--apply` writes all + collection; `--remove` after Christmas |
| `python content/youtube/run.py schedule` | Register Windows Task Scheduler job **HOKO publish**, daily 6:30pm, via `hoko-publish.cmd` |

Notes
- Voice: edge-tts `en-AU-WilliamMultilingualNeural`. If edge-tts can't connect it falls back to Piper (`HOKO_PIPER_MODEL`). Each reel's `.json` records which voice it used.
- `*.mp4` is gitignored. `publish` renders a missing reel on the fly, so a fresh clone works.
- First YouTube run opens a browser once for OAuth; the token is cached in `.secrets/` (gitignored).
- Settings (cutoff, lead time, BF list URL) live in `config.json`; change them and re-run `calendar`.
