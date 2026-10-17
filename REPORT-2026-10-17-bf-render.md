# REPORT — 2026-10-17 BF render (`claude/bf-render-1017-idka4q`)

Unattended **cloud** run (no `.env`, Linux container), brief pasted by Ethan as the session's opening message. Branch is the session's designated `claude/bf-render-1017-idka4q` (the harness pins it; brief said `claude/bf-render-1017`). Authorised and used: clip renders + sidecar rewrites under `content/youtube/reels`, social queue topup, CLAUDE.md edit, backups. **0 Shopify writes. No price, discount, inventory, order, fulfilment or product-status change.** Shopify read: discounts only.

## Summary

| Step | Result |
|---|---|
| 0 State | PASS — read CLAUDE.md, QUEUE.md, `REPORT-2026-10-17-bf-lockin.md` (answered OPEN QUESTION: free postage on all sealed, no minimum; M7 stays live with the placeholder), git log -10. Location: **cloud**. Unlike the 17:12 / bf-lockin runs, **PyPI was reachable this session**: `edge-tts` + `faster-whisper` installed, piper already present, `en_GB-alan-medium` voice downloaded. Nothing skipped as already done |
| 1 Source refresh | **MANUAL (PC)** — no Shopify token in the cloud, `run.py source` not run. Committed `sealed/source.csv` checked instead: the 5 newest are ACTIVE at $330 / $235 / $200 / $190 / $165, M7 image = `m7-aura-seeker-preorder-placeholder.png` (`image_source` hoko-placeholder), FB12 = `FB12_jp.png`. Diff vs `reports/backups/2026-10-17-bf-lockin-sealed-source-before.csv`: only OP-18 + EB-05 DRAFT→ACTIVE and M7 + FB12 rows added; **0 other rows changed**. File not rewritten this run |
| 2 Renders | **PASS — 38/38 clips, all en-AU William (edge-tts), 0 fallback voice** |
| 3 Queue | PASS — topup kept all 165 items (queue byte-identical), check PASS 15 days/platform, 60% hot on every platform, 0 violations; dry-run 0 invalid, **0 missing media**; cloud-run dry-run: all 8 NOT CONFIGURED (expected); 47 tests OK |
| 4 Canon | PASS — automatic read live, still "$100+ all products"; CLAUDE.md line made explicit; change to the automatic → MANUAL (Ethan) |
| 5 Gates + wrap | PASS (table below) |

## Step 2 — how edge-tts was made to work in the cloud

edge-tts failed with `CERTIFICATE_VERIFY_FAILED` (it pins `certifi.where()`, and aiohttp ignores `HTTPS_PROXY`). Fixed **without touching repo code or disabling TLS**: a session-only `sitecustomize.py` on `PYTHONPATH` points certifi at the session proxy CA bundle and defaults `edge_tts.Communicate(proxy=$HTTPS_PROXY)`. Every clip then rendered with `en-AU-WilliamMultilingualNeural`; piper was never needed. Word timings via faster-whisper `base` (beat-matched captions, not the even-spacing fallback).

## Step 2 — per-clip render table

a) brief clips: EB-05 h3 (new), M7 h3 + FB12 h3 (`stale_render` cleared — the renderer rewrites the sidecar without it), `--force`. b) the 27 clips the queue listed as missing (sealed/slab rendered per id + hook rather than `reel … all`, so ~50 unqueued hooks were not rendered for nothing; tips/roundups via `python -m tools.social render` → `run.py calendar`). c) BF beats: none says "$100" (11/20, 11/24, 11/26 "Free postage on every sealed box, the twenty seventh to the thirtieth of November"; 11/27 "Free postage on every sealed box until Monday") — **text left as-is**; `run.py calendar` rendered their mp4s with the same voiceover text (they had no mp4 in this checkout). `calendar.md`, `captions/`, `CUTOFF.md` came out byte-identical — nothing to revert.

Gate per clip: ffprobe 1080×1920, audio stream present, 8–20 s, voiceover has no "$".

| Clip | Voice | Duration | Resolution | Audio | Gate |
|---|---|---|---|---|---|
| `reels/beats/2026-11-01.mp4` | en-AU-WilliamMultilingualNeural | 10.74s | 1080x1920 | audio | PASS |
| `reels/beats/2026-11-20.mp4` | en-AU-WilliamMultilingualNeural | 10.78s | 1080x1920 | audio | PASS |
| `reels/beats/2026-11-24.mp4` | en-AU-WilliamMultilingualNeural | 10.74s | 1080x1920 | audio | PASS |
| `reels/beats/2026-11-26.mp4` | en-AU-WilliamMultilingualNeural | 10.63s | 1080x1920 | audio | PASS |
| `reels/beats/2026-11-27.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/beats/2026-11-30.mp4` | en-AU-WilliamMultilingualNeural | 11.74s | 1080x1920 | audio | PASS |
| `reels/roundups/mega-era.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/roundups/one-piece.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/roundups/preorders.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/roundups/under-200.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/sealed/10734773862678/h2.mp4` | en-AU-WilliamMultilingualNeural | 9.51s | 1080x1920 | audio | PASS |
| `reels/sealed/10734773895446/h2.mp4` | en-AU-WilliamMultilingualNeural | 9.27s | 1080x1920 | audio | PASS |
| `reels/sealed/10734775501078/h1.mp4` | en-AU-WilliamMultilingualNeural | 8.77s | 1080x1920 | audio | PASS |
| `reels/sealed/10734775501078/h2.mp4` | en-AU-WilliamMultilingualNeural | 9.18s | 1080x1920 | audio | PASS |
| `reels/sealed/10734778482966/h2.mp4` | en-AU-WilliamMultilingualNeural | 8.84s | 1080x1920 | audio | PASS |
| `reels/sealed/10734779564310/h1.mp4` | en-AU-WilliamMultilingualNeural | 8.87s | 1080x1920 | audio | PASS |
| `reels/sealed/15398993723670/h1.mp4` | en-AU-WilliamMultilingualNeural | 9.70s | 1080x1920 | audio | PASS |
| `reels/sealed/15413124268310/h1.mp4` | en-AU-WilliamMultilingualNeural | 8.60s | 1080x1920 | audio | PASS |
| `reels/sealed/15413357543702/h1.mp4` | en-AU-WilliamMultilingualNeural | 9.13s | 1080x1920 | audio | PASS |
| `reels/sealed/15417946865942/h3.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/sealed/15417947291926/h3.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/sealed/15417947455766/h3.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/sealed/15431829848342/h3.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/slab/10655248122134/h0.mp4` | en-AU-WilliamMultilingualNeural | 9.87s | 1080x1920 | audio | PASS |
| `reels/slab/10655248122134/h1.mp4` | en-AU-WilliamMultilingualNeural | 8.00s | 1080x1920 | audio | PASS |
| `reels/slab/10655248220438/h0.mp4` | en-AU-WilliamMultilingualNeural | 11.30s | 1080x1920 | audio | PASS |
| `reels/slab/10655248220438/h1.mp4` | en-AU-WilliamMultilingualNeural | 8.00s | 1080x1920 | audio | PASS |
| `reels/slab/10655248613654/h1.mp4` | en-AU-WilliamMultilingualNeural | 8.00s | 1080x1920 | audio | PASS |
| `reels/slab/10655248711958/h0.mp4` | en-AU-WilliamMultilingualNeural | 10.70s | 1080x1920 | audio | PASS |
| `reels/slab/10655248711958/h1.mp4` | en-AU-WilliamMultilingualNeural | 8.00s | 1080x1920 | audio | PASS |
| `reels/slab/10655248777494/h0.mp4` | en-AU-WilliamMultilingualNeural | 9.87s | 1080x1920 | audio | PASS |
| `reels/slab/10655248777494/h1.mp4` | en-AU-WilliamMultilingualNeural | 8.00s | 1080x1920 | audio | PASS |
| `reels/slab/10655248810262/h0.mp4` | en-AU-WilliamMultilingualNeural | 8.84s | 1080x1920 | audio | PASS |
| `reels/slab/10655248810262/h1.mp4` | en-AU-WilliamMultilingualNeural | 8.00s | 1080x1920 | audio | PASS |
| `reels/tips/buyback.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/tips/no-outer-shrink.mp4` | en-AU-WilliamMultilingualNeural | 10.77s | 1080x1920 | audio | PASS |
| `reels/tips/spot-a-fake.mp4` | en-AU-WilliamMultilingualNeural | 11.80s | 1080x1920 | audio | PASS |
| `reels/tips/verified-graders.mp4` | en-AU-WilliamMultilingualNeural | 11.67s | 1080x1920 | audio | PASS |

Voiceover changes vs the committed sidecars (text only — everything else is tts/duration):
- `roundups/one-piece`: now leads with "The Dominance of God" (OP-18 now ACTIVE).
- `roundups/preorders`: now lists all four pre-orders incl. "Aura Seeker, 27 November. Reach the God, 12 December."
- M7 h3 sidecar: same text, JSON now escapes é (`é`).
- Every other sidecar: voiceover unchanged; `tts` piper/older → `edge-tts:en-AU-WilliamMultilingualNeural`.

**mp4s are gitignored** (`content/youtube/.gitignore`: `*.mp4`, by design "reproducible"), so the committed result is the sidecars + captions. The mp4s exist in this container only. The PC (or a cloud-run) still needs to render them locally before posting — see MANUAL.

## Step 3 — queue hot share per platform (after topup)

| Platform | Hot (M6a, EB-05, OP-18, M7, FB12) / total | Share |
|---|---|---|
| instagram | 18 / 30 | 60% |
| facebook | 18 / 30 | 60% |
| youtube | 18 / 30 | 60% |
| tiktok_queue | 27 / 45 | 60% |
| pinterest | 27 / 45 | 60% |
| discord | 9 / 15 | 60% |
| **all** | **117 / 195** | **60%** |

Topup added nothing (queue already reached 31 Oct, 15 days per platform) — `content/social-queue.json` is byte-identical to the before-copy `reports/backups/2026-10-17-bf-render-social-queue-before.json`. dry-run: valid 14/29/29/43/42/14/28, invalid 0, media missing 0 on every platform. cloud-run `--dry-run --no-render`: instagram, facebook, youtube, pinterest, discord, tiktok_queue, tiktok, shopify_files all NOT CONFIGURED; invalid 0, would_post 0, missing_media 0, cannot_render []. Tests: `Ran 47 tests … OK`.

## Step 4 — CLAUDE.md "Black Friday automatics" line

Live read (Admin GraphQL, discounts only), `gid://shopify/DiscountAutomaticNode/1736998125846`: **"Black Friday: Free AU postage on orders $100+"**, SCHEDULED 2026-11-26T13:00Z → 2026-11-30T12:59:59Z, summary "Free shipping on all products • Minimum purchase of $100.00 • For Australia", minimum subtotal 100.0 AUD, countries [AU]. Ethan has **not** changed it yet. Not edited.

- Before: `Black Friday automatics, scheduled 27–30 Nov: 10% off singles under $100 (discount-eligible), free AU postage on orders $100+`
- After: `Black Friday automatics, scheduled 27–30 Nov: 10% off singles under $100 (discount-eligible), free AU postage on orders $100+ (all products, AU only — re-read 17 Oct 2026; Ethan's ruling is free postage on every Japanese sealed box, no minimum — the automatic is still to be changed to that by Ethan)`

Same read: the 10%-singles automatic and BFDROP5 are SCHEDULED with the same window, unchanged.

## Gates

| Gate | Result |
|---|---|
| source.csv 5 newest ACTIVE | PASS (committed file; live refresh MANUAL) |
| every rendered clip passes ffprobe + no "$" in voiceover | PASS — 38/38 |
| social check PASS + 60% | PASS — 60% on all 6 platforms |
| 47 tests OK | PASS |
| 0 banned words on everything touched | PASS — grep over all 52 changed/new files. Hits excluded as allowed: CLAUDE.md line 25 (the banned-word list itself), the M6a CDN filename (`…-sealed-box-<o-word>-white.jpg`) and the IANA time-zone string in the queue before-copy. 0 hits in sidecars, captions, this report |

## Findings (not actioned)
- `content/youtube/reels/**/h*.caption.txt` (legacy content-machine captions, rewritten on each render) carry a price and "free AU post on sealed orders $250+", e.g. M7 "$190 — free AU post…". CLAUDE.md says no prices in social captions. The social poster builds its own captions (price gate) and does not post these files, so nothing customer-facing breaks. Worth a one-line fix in `reel.caption_text` on a later run if those files are used anywhere.
- The pre-order on-screen card (`reel.preorder_body`) shows the price + "free AU post $250+" in the video frame. Allowed by the current gate (voiceover only). Raising it in case "no prices in social" should cover the frame too.
- `content/youtube/hoko/tts.py` does not pass the proxy/CA to edge-tts, so a cloud-run without this run's sitecustomize falls back to piper (en_GB). Fix is about 3 lines (`proxy=os.environ.get('HTTPS_PROXY')` + an SSL context from `SSL_CERT_FILE`). Repo code was outside this brief's scope, so not changed.
- cloud-run dry-run reports `due_unconfigured` facebook 29 / youtube 29 (vs 1 on the others). Expected? Nothing posts while NOT CONFIGURED; not investigated.

## NOT CHECKED
- `run.py source` against the live store (no token in the cloud). The 5 newest were confirmed via the committed CSV only; this run read discounts only from Shopify, not products.
- Watching/listening to the clips: checked by ffprobe + sidecar text only, not by eye or ear.
- Live posting (no platform keys).

## MANUAL

**Ethan only**
- Shopify admin → Discounts → "Black Friday: Free AU postage on orders $100+" → applies to collection *Japanese Sealed*, no minimum purchase, dates unchanged 27–30 Nov (rename the title to match). Until then the live automatic still covers every sealed box (cheapest $115 ≥ $100), so the copy is true either way. After the change, tell the next run to rewrite the CLAUDE.md line to "free AU postage on every Japanese sealed box, no minimum".
- Social platform keys (list in `REPORT-2026-10-17-bf-lockin.md` MANUAL); environment setup script: `pip install edge-tts faster-whisper piper-tts pillow numpy requests` so renders don't depend on PyPI at run time.
- Decide whether to ship the `tts.py` proxy fix so cloud-run renders in the en-AU voice (see Findings).

**PC only**
- `python content/youtube/run.py source` → confirm the 5 newest come back ACTIVE at $330/$235/$200/$190/$165 with the M7 placeholder / `FB12_jp.png` images.
- Render the mp4s locally (gitignored, so they don't come down with the pull): `python -m tools.social render` (PC edge-tts gives the same William voice), plus `python content/youtube/run.py reel sealed 15431829848342 --hook 3 --force` (and the same for 15417947455766, 15417947291926) if the PC still holds the old M7/FB12 h3 mp4s.

## COMPLETE
