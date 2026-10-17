# HOKO social auto-poster (`tools/social/`)

The poster queues 14 days of posts across Instagram, Facebook, YouTube Shorts, Pinterest and Discord, plus a daily TikTok
package sent to your phone, and then posts them on schedule. Its content comes from what's already in `content/`. It
replaces the old one-post-a-day `content/youtube/run.py publish` job.

> **The PC "HOKO publish" job is RETIRED (17 Oct 2026). `tools/social` is the only poster.** `run.py publish`,
> `run.py schedule` and `hoko-publish.cmd` stay in the repo but must not run. Remove the task on the PC:
> `schtasks /Delete /TN "HOKO publish" /F` (`install-tasks.ps1` only disables it).

| Platform | When (AEDT/AEST) | How |
|---|---|---|
| Instagram Reels | 12:15, 19:15 | Graph API. The clip is hosted on Shopify Files and published at the slot (no native scheduling). |
| Facebook Page | 12:15, 19:15 (mirrors IG) | `scheduled_publish_time`, scheduled 15 min–14 days ahead |
| YouTube Shorts | 11:00, 18:00 | Every Short due in the next 14 days is uploaded at once with `status.publishAt` |
| Pinterest | 10:00, 15:00, 20:00 | v5 image pins (product / collection photo) linking the product or collection page |
| Discord #pickups-and-drops | 17:00 | Webhook embed: photo, name, link |
| TikTok | 07:00 | 3 clips + captions sent to the #tiktok-queue webhook. You post from your phone. Direct posting via the Content Posting API is built but off (`TIKTOK_ENABLED=false`). |

## Commands (from the repo root)

```
python -m tools.social env        # one line per platform: set / MISSING <keys> (never prints values; --keys = per key)
python -m tools.social build      # rebuild content/social-queue.json, today + 14 days
python -m tools.social topup      # keep today+ items, add days up to 14 ahead  (--render: render missing clips)
python -m tools.social check      # gate: ≥14 days per platform, no 7-day repeats, no banned words / prices
python -m tools.social dry-run    # build + validate every payload, no network → data/social-dryrun.json
python -m tools.social run        # post / schedule what's due (the 15-minute task)
python -m tools.social render     # render clips the queue needs (PC: ffmpeg + content/youtube deps)
python -m tools.social cloud-run  # one unattended pass from Claude Code web (see Cloud below); --dry-run = JSON summary only
python -m tools.social phone-pack # today's TikTok clips + Instagram items as markdown for the phone (see Phone pack below)
python -m unittest discover -s tools/social/tests -t .
```

Windows (once): `powershell -ExecutionPolicy Bypass -File tools\social\install-tasks.ps1`. This creates
**HOKO Social Runner** (every 15 min) and **HOKO Social Topup** (23:00), disables the old **HOKO publish** job,
and sets the PC to never sleep on mains power.

## Env keys (User environment variables; nothing is stored in the repo)

`META_PAGE_TOKEN`, `IG_BUSINESS_ID`, `FB_PAGE_ID`, `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`,
`PINTEREST_TOKEN`, `PINTEREST_BOARD_ID`, `DISCORD_WEBHOOK_PICKUPS`, `DISCORD_WEBHOOK_TIKTOK_QUEUE`,
`TIKTOK_ENABLED` (default false), `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN`,
`SHOPIFY_STORE`, `SHOPIFY_ADMIN_TOKEN` (needs `write_files`, used to host clips for IG / FB / TikTok).
Optional: `TIKTOK_PRIVACY` (default `SELF_ONLY` until the TikTok app is audited), `DISCORD_MAX_UPLOAD_MB` (default 10).
A platform with missing keys is skipped and reported as `NOT CONFIGURED`. Add the keys later and it starts posting.

## Queue rules

- **Sources.** Product reels `content/youtube/reels/{sealed,slab}/<id>/h<k>`, tips, ranked roundups, BF/Christmas
  beat reels (pinned to their date). The poster also picks up `content/youtube/out/*/short_*` (Shorts cut from long-form),
  `content/carddrop/**` and `content/social-bank/**` (an mp4 with a sidecar `.json` of `hook/url/title/game`).
- **What gets promoted.** Only products that are ACTIVE, not `OOS-SUPPLIER`, and inventory > 0 (every live variant is set to DENY, so 0 means sold out). Draft pre-orders
  are left out until they are published. To refresh from Shopify: `python content/youtube/run.py source`.
- **Mix.** Japanese sealed takes about 70% through November (50% in December). Slabs take 20–30%, tips and buy-posts the rest.
- **No repeats.** The same clip or pin never goes to the same platform within 7 days, and each product appears at most once
  per platform per day.
- **Captions.** These are written by `captions.py` templates with no API calls. Every caption ends "Collector first.
  Seller second.", and none contains prices or any of the banned words in `captions.BANNED`.
  `check` enforces this. Edit any caption directly in `content/social-queue.json`; the runner posts the text it finds there.
- **Runner.** `data/social-post-log.csv` is the source of truth: OK / FAIL / SKIP mean done. A failed post is logged RETRY,
  retried on the next run, and marked FAIL after 2 retries. Anything more than 6 h past its slot is logged SKIP
  instead of going out late.

## Phone pack

`python -m tools.social phone-pack [--date YYYY-MM-DD]` prints the day's `tiktok_queue` clips and Instagram items as
markdown: platform + slot · name, the clip as a `raw.githubusercontent.com/.../main/<media>` mp4 URL (reels are
committed), the product link, and the caption verbatim in a code block. Day = today in Victoria; if it has no
TikTok / Instagram items, the next day that does. Every printed item is appended to `data/phone-pack-log.csv`
(`date,platform,asset_id,url`, header written if the file is new). A scheduled cloud task (07:10 daily) runs it.

## Cloud (Claude Code web, no PC)

`python -m tools.social cloud-run` is the whole poster in one pass for a scheduled Claude Code web session:
env check → top up the queue (any platform under 10 days queued → today + 14) → render missing clips here →
host clips on Shopify Files → post everything due, with a **7 h late window** (a slot that passed up to 7 h ago
still goes out, because a daily trigger cannot hit every 15-minute slot; `SOCIAL_LATE_WINDOW_HOURS` overrides) →
write `data/social-post-log.csv` (idempotency, header created if missing) and `data/social-runner.log` (transcript).
Those two files are **not** gitignored any more: the cloud run commits them to `main` at the end so the next run
knows what already went out. `data/social-media-cache.json` and `data/social-dryrun.json` stay ignored.

Keys are read from **environment variables only** (no `.env` is read in the cloud). Set them in the Claude Code web
environment config. A platform with a missing key is reported `NOT CONFIGURED` and skipped; the run never fails on it.

| Platform | Env vars (all required for that platform) | What setting them unlocks |
|---|---|---|
| Instagram Reels | `META_PAGE_TOKEN`, `IG_BUSINESS_ID` + Shopify Files hosting | Reels published at 12:15 / 19:15 via the Graph API |
| Facebook Page | `META_PAGE_TOKEN`, `FB_PAGE_ID` + Shopify Files hosting | Same clip scheduled natively (`scheduled_publish_time`), up to 14 days ahead |
| YouTube Shorts | `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` | Every Short due in the next 14 days uploaded at once with `publishAt` |
| Pinterest | `PINTEREST_TOKEN`, `PINTEREST_BOARD_ID` | Image pins at 10:00 / 15:00 / 20:00 linking product / collection pages |
| Discord #pickups-and-drops | `DISCORD_WEBHOOK_PICKUPS` | 17:00 product embed |
| TikTok phone pack | `DISCORD_WEBHOOK_TIKTOK_QUEUE` | 07:00 package of 3 clips + captions to #tiktok-queue (you post from the phone) |
| TikTok direct API (off by default) | `TIKTOK_ENABLED=true`, `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN` + Shopify Files hosting; optional `TIKTOK_PRIVACY` | Direct posting via the Content Posting API (SELF_ONLY until the app is audited) |
| Shopify Files hosting | `SHOPIFY_STORE` (xxxx.myshopify.com), `SHOPIFY_ADMIN_TOKEN` (Admin API, `write_files`) | Public URLs for clips, needed by Instagram, Facebook and the TikTok API. Also lets `content/youtube/run.py source` refresh the product list |

Optional: `SOCIAL_LATE_WINDOW_HOURS` (default 7), `DISCORD_MAX_UPLOAD_MB` (default 10), `HOKO_PIPER_MODEL` (path to a
Piper `.onnx` voice; cloud-run downloads `en_GB-alan-medium` to `content/youtube/.cache/piper/` when unset).

**Rendering in the cloud.** The en-AU edge-tts voice verifies against the session proxy's CA bundle when `SSL_CERT_FILE` /
`REQUESTS_CA_BUNDLE` (or `/root/.ccr/ca-bundle.crt`) is set and uses `HTTPS_PROXY` (see `content/youtube/hoko/tts.py`;
verification is never disabled). If edge-tts still cannot reach Microsoft, cloud-run renders the clip with the Piper
fallback voice and logs `fallback voice` per clip.
Beat-matched captions need faster-whisper; without it the script's words are spaced evenly over the voiceover.
Needs `ffmpeg` on PATH plus `pip install edge-tts piper-tts faster-whisper pillow numpy requests` in the environment (add
them to the environment's setup script). Shorts cut from long-form, CardDrop and social-bank clips need their source
video and are reported `cannot_render`; render those on the PC.
Reels are committed; cloud-run only renders what's missing.

**Schedule it (one-time, in Claude Code web):** open the environment → Triggers → Add scheduled trigger, daily (a
second one later in the day catches the evening slots), source this repo on `main`, with this prompt:

```
Go. From Ethan: run the social poster.
Read CLAUDE.md. On a claude/social-cloud-<date> branch run `python -m tools.social cloud-run`, paste its JSON summary
into reports/REPORT-<ISO date>.md with PASS/FAIL per platform (NOT CONFIGURED is not a failure), then commit
data/social-post-log.csv, data/social-runner.log and the report to main. Never create, edit or delete a discount,
price or listing. If `invalid.count` is not 0, stop and report.
```

**Check it without posting:**

```
python -m tools.social env                 # which platforms are set / MISSING which keys
python -m tools.social cloud-run --dry-run # JSON: platforms, queue_days_per_platform, invalid, rendered, hosted,
                                           #       would_post, late_window_hours — no renders, uploads or posts
```
