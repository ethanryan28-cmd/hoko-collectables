# HOKO social auto-poster (`tools/social/`)

The poster queues 14 days of posts across Instagram, Facebook, YouTube Shorts, Pinterest and Discord, plus a daily TikTok
package sent to your phone, and then posts them on schedule. Its content comes from what's already in `content/`. It
replaces the old one-post-a-day `content/youtube/run.py publish` job.

| Platform | When (Melbourne) | How |
|---|---|---|
| Instagram Reels | 12:15, 19:15 | Graph API. The clip is hosted on Shopify Files and published at the slot (no native scheduling). |
| Facebook Page | 12:15, 19:15 (mirrors IG) | `scheduled_publish_time`, scheduled 15 min–14 days ahead |
| YouTube Shorts | 11:00, 18:00 | Every Short due in the next 14 days is uploaded at once with `status.publishAt` |
| Pinterest | 10:00, 15:00, 20:00 | v5 image pins (product / collection photo) linking the product or collection page |
| Discord #pickups-and-drops | 17:00 | Webhook embed: photo, name, link |
| TikTok | 07:00 | 3 clips + captions sent to the #tiktok-queue webhook. You post from your phone. Direct posting via the Content Posting API is built but off (`TIKTOK_ENABLED=false`). |

## Commands (from the repo root)

```
python -m tools.social env        # which keys are set / MISSING (never prints values)
python -m tools.social build      # rebuild content/social-queue.json, today + 14 days
python -m tools.social topup      # keep today+ items, add days up to 14 ahead  (--render: render missing clips)
python -m tools.social check      # gate: ≥14 days per platform, no 7-day repeats, no banned words / prices
python -m tools.social dry-run    # build + validate every payload, no network → data/social-dryrun.json
python -m tools.social run        # post / schedule what's due (the 15-minute task)
python -m tools.social render     # render clips the queue needs (PC: ffmpeg + content/youtube deps)
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
  Seller second.", and none contains prices, Whatnot, "mystery pack", "official" or "Top Rated".
  `check` enforces this. Edit any caption directly in `content/social-queue.json`; the runner posts the text it finds there.
- **Runner.** `data/social-post-log.csv` is the source of truth: OK / FAIL / SKIP mean done. A failed post is logged RETRY,
  retried on the next run, and marked FAIL after 2 retries. Anything more than 6 h past its slot is logged SKIP
  instead of going out late.
