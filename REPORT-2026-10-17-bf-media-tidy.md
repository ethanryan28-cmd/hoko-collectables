# REPORT — 2026-10-17 BF media tidy (`claude/bf-media-tidy-1017-1tsocy`)

Unattended **cloud** run. Ethan pasted the brief as the session's opening message. Authorised: merging `claude/bf-media-render-queue-376p0p`, plus edits to `cloud_run.py` (docstring and log text only), the `reel.py` caption text, the social README and QUEUE.md. **0 Shopify writes, 0 Shopify reads.** No price, discount, listing, inventory, order or theme change. No mp4 or sidecar `.json` was touched.

Branch note: the harness assigned `claude/bf-media-tidy-1017-1tsocy` (the brief said `claude/bf-media-tidy-1017`). The work went there, cut from `origin/main` `e967b58`.

## Summary

| Step | Result |
|---|---|
| 0 Read + branch | **PASS.** Read CLAUDE.md, QUEUE.md, bf-media Findings and bf-media-2. origin/main `e967b58`. Nothing from Steps 1–3 was already on main |
| 1 Fold in run-2 verification | **PASS.** `fb5e120` merged `--no-ff`. `git diff origin/main --stat` shows only `QUEUE.md` (+4) and `REPORT-2026-10-17-bf-media-2.md` (+9) |
| 2 Stale cloud docs | **PASS.** `cloud_run.py` docstring now says edge-tts trusts the proxy CA via `hoko/tts.py` (SSL_CERT_FILE / REQUESTS_CA_BUNDLE / `/root/.ccr/ca-bundle.crt`) and Piper is used only if Bing is still unreachable. Also fixed the dry-run log literal "would render N clip(s) with the fallback voice", which now reads "(en-AU edge-tts, Piper fallback)". The diff covers 1 docstring block and 1 log f-string, no logic. 54 tests OK |
| 3 Caption price lines | **PASS.** Nothing reads `.caption.txt`. `caption_text` changed and 61 files rewritten with no render. The gate `grep '\$[0-9]'` finds 0 files. 0 mp4 and 0 json modified. 54 tests OK |
| 4 due_unconfigured 29/29 | **PASS, by design.** No code change. The explanation is below |
| 5 Gates + wrap | **PASS.** Results under Gates |

## Step 3 — captions

**Readers of `*.caption.txt`:** none. `grep -rn "caption.txt"` across `tools/`, `content/youtube/hoko`, `run.py`, `routines/` and the whole repo outside `reels/` finds:
- the 2 writers in `reel.py` (`render()`: new clip + the "captions are cheap, keep in sync" re-write on every non-forced run),
- the `reel.py` module docstring,
- `content/youtube/REPORT.md` (docs).

The social queue (`tools/social/queue_builder.py`) builds its own captions with `tools/social/captions.py`, which never uses these files. The TikTok phone pack takes its captions from the queue, not from these files.

**Code change (`content/youtube/hoko/reel.py` `caption_text`):**
- Dropped the sealed line `"{price} — free AU post on sealed orders $250+."` and the slab line `"{price} — tracked post, free on orders $150+."`.
- The hook line itself carried a price in 26 files: slab hooks h1+ (`"One in stock — PSA 10 Pikachu, $599"`) and sealed h2 without a packs field (`"Abyss Eye for $190 — free AU post over $250"`). The caption now strips it: slab → `"One in stock — PSA 10 Pikachu"`, sealed h2 → `"Abyss Eye — sealed Japanese booster box"`. `hook_text` is **not** changed, so the on-screen hook and the sidecars stay as rendered.
- Kept: hook, product line, distributor/grader line, pre-order date line, `Grab it at hokocollectables.com → <url>`, tagline, hashtags. The dated BF/Christmas lines (only added when `when` is set, i.e. calendar captions) are unchanged.

**Rewrite:** a backup of all 61 files went to `reports/backups/2026-10-17-bf-media-tidy-captions/` and was compared byte-for-byte before writing. The script is saved alongside as `_recap.py`. It loads `sealed/source.csv` and `slabs/source.csv` and calls the new `caption_text` (57 files). The 4 files of the 2 products dropped from source.csv (`10734771896598`, `10734773666070`) are not in source.csv, so the script strips those lines by regex instead, taking the product kind from the sidecar title. The first attempt's backup copy failed (`cpio` not installed). The files were restored from git (they are tracked) and the backup was redone and verified before the rewrite.

**Read-back:** 61 files, +26 −87. Every removed line is a price/postage line or a priced hook, and every added line is the de-priced hook. **0 other lines changed.**

**Pre-order on-screen price card (Findings #2): YES**, the price is in the video frame for pre-order clips. `reel.preorder_body(row)` line 4 is `f'{price_str(row["price"])} · free AU post $250+'`, drawn by `render()` when `kind == 'sealed' and k == 3`. Separately, `render()` draws the big gold `L_price` (`price_str(row['price'])`) on sealed/slab clips. The h2 sealed and h1+ slab **on-screen hooks** (`hook_text`) also carry the price. Not touched: Ethan's call.

## Step 4 — why facebook / youtube show due_unconfigured 29

`cloud_run.due()` counts an item when `runner.action(item, now, grace)` returns `send` or `send-late`. In `tools/social/runner.py:68`:
- **youtube:** `send` whenever the slot is ≤ `YT_HORIZON` (14 days) ahead. The runner uploads everything in the next 14 days at once with `publishAt`.
- **facebook:** `send` whenever the slot is between `FB_MIN_LEAD` (15 min) and `FB_HORIZON` (14 days) ahead. FB schedules natively with `scheduled_publish_time`.
- **instagram, pinterest, discord, tiktok_queue:** `send` only once `now >= slot` (no native scheduling), so only the 1–2 slots in today's window count.

The queue holds ~15 days per platform, so nearly every future FB/YT slot (29 each) counts as "due now" for native scheduling. **Not a bug.** One consequence for when keys are added: the first configured cloud-run will host all ~29 FB clips in Shopify Files in one pass (`host()` uploads every due IG/FB clip). That is intended, but the first run will be slow. `data/social-runner.log` was reverted with `git checkout`.

## Gates

| Gate | Result |
|---|---|
| `python -m unittest discover -s tools/social/tests -t .` | **54 tests OK** |
| `python -m tools.social check` | **PASS**: 15 days on all 6, 60% hot on every platform (all 117/195), 0 violations printed |
| `python -m tools.social dry-run` | **0 invalid**, **missing 0** on every platform |
| `cloud-run --dry-run --no-render` | 0 invalid, missing_media 0, cannot_render [] |
| Banned words on changed text files | **0.** The list and method are under Wrap |
| mp4 / sidecar json modified | **0** (`git status` shows only `.caption.txt`, `reel.py`, `cloud_run.py`, report, QUEUE, backups) |
| `grep -rln '\$[0-9]' content/youtube/reels/ --include='*.caption.txt'` | **0 files** |

## Findings (not actioned)
1. **`content/youtube/captions/YYYY-MM-DD.txt` still carry prices (65 files) and they DO have a reader.** `calendar_gen.py` writes them from the same `caption_text` (with `when=d`), and `calendar.md` points at them. The PC-only `run.py publish` (`hoko/publish.py`, Windows "HOKO publish" task) posts them to IG and YouTube. The `caption_text` fix only reaches them when the calendar is rebuilt. `run.py calendar` calls `calendar_gen.build()` with `render_beats=True`, which renders the beats/tips/roundups. A no-render rebuild would be `python -c "from hoko import calendar_gen; calendar_gen.build(render_beats=False)"` from `content/youtube/`. It rewrites `calendar.md`, `CUTOFF.md` and all dated captions, so it is left for a brief that authorises it. Also check whether the PC publish task is still scheduled. If `tools/social` replaced it, it should be removed.
2. The calendar-only BF line `"Join the BF box drop list — $5 off boxes …"` puts a dollar figure in calendar captions. It is a discount amount, not a product price, and was not touched. Ethan's call.
3. The sealed h2 on-screen hook and voiceover still say "free AU post over $250" / "over two fifty", and `preorder_body` says "free AU post $250+". Ethan's ruling (bf-lockin 07:27) is free postage on all sealed, no minimum. Changing these needs a re-render, so it goes with the Findings #2 decision.

## NOT CHECKED
- Any render, ffprobe or voice: nothing was rendered.
- Live posting (no platform keys). Shopify was not read.
- Whether the PC "HOKO publish" scheduled task is still active.

## MANUAL

**Ethan only**
- BF free-shipping automatic still to be edited (all orders $100+ → Japanese Sealed collection, no minimum, 27–30 Nov). Unchanged.
- Platform keys (list in `REPORT-2026-10-17-bf-lockin.md` MANUAL).
- Environment setup line `pip install edge-tts piper-tts faster-whisper pillow numpy requests` + `ffmpeg`, and network allowlist `pypi.org`, `files.pythonhosted.org`, `speech.platform.bing.com`, `huggingface.co`.
- **Ruling:** does the on-screen price stay in clips? This covers the pre-order card (`preorder_body`), the big gold price (`L_price`), the sealed h2 / slab h1+ hooks, and the "$250+" postage figure in them (Findings 3).
- **Ruling:** rebuild `captions/*.txt` without rendering (Findings 1), yes/no.

**PC only**
- Check Task Scheduler for "HOKO publish". It posts `captions/<date>.txt`, which still carry prices.

## Wrap
- Banned-word scan on changed text files (`reel.py`, `cloud_run.py`, 61 captions, report, QUEUE). Checked: every term on the CLAUDE.md banned list (8 terms). Result: 0 hits.
- Commits on `claude/bf-media-tidy-1017-1tsocy`: the merge of `fb5e120`, then the tidy commit (code + captions + backups + this report + QUEUE). Pushed, merged `--no-ff` into `main`, pushed. `git ls-remote` was checked against local main.

## COMPLETE
