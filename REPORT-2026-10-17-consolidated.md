# REPORT — 2026-10-17 consolidated run (`claude/consolidated-1017`)

Unattended run. Authorised writes this run: status, inventory-policy, tag, metafield, raise-to-floor price. Every Shopify write has a before-copy in `reports/backups/` and was read back. No price lowered. Discounts, orders, fulfilments, payments untouched.

## Summary

| Step | Result |
|---|---|
| 0 State | PASS — nothing in this prompt was already done; prior runs (`REPORT-2026-10-17-finish.md`, `reports/REPORT-2026-10-17T1140+1100.md`) only overlap on the 15 boxes and the pre-order drafts, which are inputs here |
| 1 Scope + routing | PASS with one input NOT CHECKED (eBay AU sold counts, see below) |
| 2 Social in the cloud | PASS — all 5 gates (43 tests, dry-run invalid 0, 1 clip rendered in the cloud with the Piper fallback voice, 0 DRAFT/0-stock refs, 15 days on 6 platforms). `run.py source` NOT RUN (no Shopify token in this environment); every platform NOT CONFIGURED (no keys yet) |
| 3 Store hygiene | PASS (reads) / MANUAL (policy writes) — `shopPolicyUpdate` refused: token lacks `write_legal_policies`; Contact, Shipping and a full AU Privacy policy are paste blocks below. Discount-eligible has no live sealed/pre-order/slab; 0 customer orders stuck; 9 abandoned checkouts, none over $50 |
| 4 Wrap | PASS — branch merged `--no-ff` into main |

## Step 0 — State

- Branch: `claude/consolidated-1017` from `main` @ fbf9eba (finish-1017 merge).
- Read: CLAUDE.md (canon, 17 Oct), QUEUE.md, both 17 Oct reports, `git log -30`, `git branch -r` (10 remote branches; `claude/finish-1017` and 7 older `claude/*` branches still exist remotely — git proxy refuses remote deletes).
- Already done → SKIPPED: nothing. The 15 zero-stock boxes were set DRAFT by `claude/jp-boxes-draft` (7ee760a) and are candidates here by design.

## Step 1 — Scope + routing (Pokémon + One Piece Japanese sealed)

### Inputs
- FX: 1 JPY = 0.009112 AUD (open.er-api.com, 17 Oct 00:02 UTC).
- Kanade: Drive sheet "Price List" (owner asuzuki0816, modified 7 Aug 2026) — Pokémon + One Piece tabs, per-box yen.
- Urara: "Urara.Chii List" sheet, price list dated 16 Oct 2026 — a box counts as listed only when Stock > 0 and Price > 0. No-outer-shrink products are matched to Urara's "No-Shurink" rows; Kanade has no no-shrink rows, so those boxes have no Kanade route.
- Fees: Shopify Payments AU 1.75% + $0.30 (ASSUMPTION: Basic plan domestic card rate).
- Single landed = (Kanade ¥ + ¥5,500 freight + ¥500 signature) × FX. Batch landed = Urara ¥ × FX + A$14. Floor = (landed + fee) × 1.10, rounded up to $5.

### Live set
- (i) Newest 3 released sets per game: Pokémon **M6a, M6, M5**; One Piece **OP-17, OP-16, OP-15** (ASSUMPTION: EB-03 Heroines treated as an extra booster, not a main set).
- (ii) Pre-orders M7 / OP-18 / FB12: daily gate has not made them ACTIVE (none on the Urara list) → excluded, stay DRAFT. FB12 is Dragon Ball, outside this step's scope anyway.
- (iii) Top-5 older sets by eBay AU sold count last 30 days: **NOT CHECKED.** `ebay.com.au` returns HTTP 403 to this container (curl with browser UA and WebFetch both; proxy status shows no explicit deny, eBay bot-blocks the egress). Without sold counts the trim could not be computed, so **no in-stock ACTIVE box was set DRAFT on missing data**; the 11 zero-stock DRAFT boxes outside (i) stayed DRAFT. Shopify's own last-30-day orders were checked as a proxy: 1 box sold (Abyss Eye M5 sealed, draft order #1434, 27 Sep); every other order in the window was a single.
- M6a (15398993723670) and OP-17 (15402647453974 pre-order, 10734775730454) are in the live set by (i) but are not candidates under 1a (not ACTIVE, not in the 15, not a named pre-order) → left DRAFT, flagged MANUAL.

### Routing table
| Set | Box | Before | After | Inv | Price | Kanade ¥ | Urara ¥ | Single floor | Batch floor | Margin single | Margin batch | Route |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M6 | `pokemon-storm-emeralda-m6-sealed-japanese-booster-box` | DRAFT | DRAFT | 0 | $150 | 20980 | — | $280 | — | $-98.77 | — | none — Kanade floor $280 is $130 above price; Urara: 0 stock / not listed |
| M6 | `pokemon-storm-emeralda-m6-japanese-booster-box-no-outer-shrink` | ACTIVE | ACTIVE | 1 | $180 | — | 9300 | — | $115 | — | $77.81 | route:urara-batch |
| M5 | `pokemon-abyss-eye-m5-sealed-japanese-booster-box` | DRAFT | ACTIVE | 0 | $190 | 8880 | — | $155 | — | $50.79 | — | route:kanade-single |
| M5 | `pokemon-abyss-eye-m5-japanese-booster-box-no-outer-shrink` | ACTIVE | ACTIVE | 2 | $120 | — | 9000 | — | $110 | — | $21.59 | route:urara-batch |
| OP-16 | `one-piece-tcg-op-16-sealed-japanese-booster-box` | DRAFT | ACTIVE | 0 | $180 | 13580 | 10300 | $205 | $125 | $-1.86 | $68.7 | route:urara-batch |
| OP-15 | `one-piece-tcg-op-15-sealed-japanese-booster-box-1` | DRAFT | DRAFT | 0 | $165 | 15980 | — | $225 | — | $-38.47 | — | none — Kanade floor $225 is $60 above price; Urara: 0 stock / not listed |
| sv9a | `pokemon-heat-wave-arena-sv9a-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $285 | 21580 | 19000 | $285 | $215 | $28.4 | $92.58 | route:kanade-single |
| M1L | `pokemon-mega-brave-m1l-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $175 | 13780 | 9400 | $205 | $115 | $-8.6 | $71.98 | route:urara-batch |
| M3 | `pokemon-nihil-zero-m3-japanese-booster-box-no-outer-shrink` | ACTIVE | ACTIVE | 2 | $115 | — | — | — | — | — | — | none — in-hand stock kept ACTIVE, no restock route; Kanade: not listed; Urara: 0 stock / not listed |
| M3 | `pokemon-nihil-zero-m3-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $130 | 8580 | — | $150 | — | $-5.43 | — | none — in-hand stock kept ACTIVE, no restock route; Kanade floor $150 is $20 above price; Urara: 0 stock / not listed |
| OP-07 | `one-piece-tcg-op-07-500-years-in-the-future-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 1 | $250 | 21080 | 18000 | $280 | $200 | $-1.43 | $67.31 | route:urara-batch |
| OP-11 | `one-piece-tcg-op-11-a-fist-of-divine-speed-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 1 | $470 | 41980 | 39000 | $495 | $415 | $24.28 | $92.11 | route:urara-batch |
| OP-12 | `one-piece-tcg-op-12-legacy-of-the-master-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $240 | 19780 | 18800 | $265 | $210 | $0.59 | $50.19 | route:urara-batch |
| sv3a | `pokemon-raging-surf-sv3a-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $235 → $245 | 17580 | 14500 | $245 | $165 | $25.55 | $94.29 | route:kanade-single |
| sv7 | `pokemon-stellar-miracle-sv7-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $210 | 14080 | 12200 | $210 | $145 | $23.06 | $80.86 | route:kanade-single |
| sv8 | `pokemon-super-electric-breaker-sv8-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $390 | 34580 | 33000 | $420 | $355 | $13.11 | $68.18 | route:urara-batch |
| sv8a | `pokemon-terastal-festival-ex-sv8a-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $280 | 20980 | — | $280 | — | $28.96 | — | route:kanade-single |
| s12a | `pokemon-vstar-universe-s12a-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $375 → $390 | 32080 | 28500 | $390 | $310 | $35.89 | $109.18 | route:kanade-single |
| M1S | `pokemon-mega-symphonia-m1s-sealed-japanese-booster-box` | ACTIVE | ACTIVE | 2 | $165 → $175 | 10980 | — | $175 | — | $16.92 | — | route:kanade-single |

Per-box reasons for "none":
- M6 sealed: Kanade 20,980 yen → single floor $280 vs $150 list ($130 gap); Urara has 0 sealed stock (only no-shrink at 9,300). Stays DRAFT.
- OP-15: Kanade 15,980 yen → floor $225 vs $165 ($60 gap); Urara 0 stock. Stays DRAFT.
- M3 sealed (in stock ×2): Kanade floor $150 is $20 above $130 (outside the $15 raise window); Urara 0 stock. Kept ACTIVE/DENY, sells in-hand stock only, no restock route.
- M3 no-shrink (in stock ×2): no supplier lists it today. Kept ACTIVE/DENY, in-hand only.

### Writes (all read back, 0 userErrors)
- Backup: `reports/backups/2026-10-17-routing-before.json` (19 products: status, tags, variant, price, policy, qty).
- 15 × `productUpdate`: one `route:` tag each, metafield `hoko.supplier` = kanade|urara. Live-set boxes also → `status: ACTIVE` and `OOS-SUPPLIER` tag dropped: **M5 sealed (DRAFT→ACTIVE, kanade), OP-16 (DRAFT→ACTIVE, urara), M6 no-shrink (urara), M5 no-shrink (urara)**.
- 7 × `productVariantsBulkUpdate`: `inventoryPolicy: CONTINUE` on the 4 live-set boxes; raise-to-floor on **sv3a $235→$245, s12a $375→$390, M1S $165→$175** (each within $15 of its Kanade floor). No price lowered.
- Collection `japan-direct-sealed` (534554444054, sortOrder MANUAL): `collectionReorderProducts` → positions 0–17 = M6 NOS, M5 sealed, M5 NOS, OP-16, then in-stock boxes newest set first (sv9a, sv8a, sv8, M1L, M1S, M3, M3 NOS, OP-12, OP-11, OP-07, sv7, sv3a, s12a, Fukuoka box). Read back in that order. Pre-orders are DRAFT so not placed.
- Black Friday page (167154385174): backup `reports/backups/2026-10-17-black-friday-page-before-routing.html`; added tiles for M5 sealed ($190) and OP-16 ($180), updated the three raised prices. Read back (updatedAt 03:09Z).
- `content/youtube/config.json` `hot_sets` → M6a M6 M5 OP-17 OP-16 OP-15 + in-stock sets (sv9a sv8a sv8 M1L M1S M3 OP-12 OP-11 OP-07 sv7 sv3a s12a); previous list kept as `hot_sets_before_2026_10_17`.
- `data/routing-2026-10-17.csv` written (handle, route, price, both floors, margin each way, note).

### Gates
- Each live box has exactly one `route:` tag: PASS (4/4 live-set boxes; 15/15 routed boxes overall).
- Banned words in routing outputs (CSV, config, backup, BF page body): 0 hits. PASS.
- `availableForSale` on the storefront (`/products/<handle>.js`): M6 NOS, M5 sealed, M5 NOS, OP-16 all `true` at the expected prices; sv3a $245, s12a $390, M1S $175 confirmed live. PASS.

## Step 2 — Social in the cloud

### Gates

| Gate | Result | Evidence |
|---|---|---|
| Tests pass | **PASS** | `python -m pytest tools/social/tests -q` → **43 passed** (35 existing + 8 new in `test_cloud_run.py`) |
| `cloud-run --dry-run` invalid == 0 | **PASS** | `"invalid": {"count": 0, "list": []}`; exit code 0 |
| At least one clip rendered in the cloud | **PASS** | `cloud_run.render([...sealed/10734771798294/h1.mp4], limit=1)` → `rendered content/youtube/reels/sealed/10734771798294/h1.mp4 [piper:en_GB-alan-medium] — fallback voice` in 20.9 s. ffprobe: video 1080x1920 + audio, 11.07 s, 1.29 MB. Sidecar `h1.json` now says `"tts": "piper:en_GB-alan-medium"` |
| No queue item on a DRAFT / 0-stock product; no 23 Nov beat | **PASS** | Script over `content/social-queue.json` vs `reports/shopify-inventory-2026-10-17.csv`: 165 items, 161 product refs, 23 distinct products, all `['ACTIVE']` with available ≥ 1; DRAFT/0-stock/unknown refs = 0; refs to `2026-11-23` = 0 (beats on disk: 11-01, 11-20, 11-24, 11-26, 11-27; the 30 Nov cutoff beat is in `beats()` but not rendered/needed yet) |
| 14+ days queued per platform | **PASS** | `check` → `{'tiktok_queue': 15, 'pinterest': 15, 'youtube': 15, 'instagram': 15, 'facebook': 15, 'discord': 15}` PASS, before and after topup |

### Files added

- `tools/social/cloud_run.py` — the `cloud-run` pass: env status → topup (any platform < 10 days → today + 14) → render missing clips via `content/youtube/run.py` (`reel <kind> <id> --hook k` per product clip, `calendar` for tips/roundups/beats) with the Piper fallback voice (downloaded to `content/youtube/.cache/piper/`, gitignored) and a `fallback voice` log line per clip → host due IG/FB/TikTok clips on Shopify Files (`hosting.public_url`) → `runner.run` with a 7 h late window → `data/social-post-log.csv` + `data/social-runner.log` (created with header if missing). `--dry-run` skips renders/uploads/posts and prints one JSON summary (keys: `platforms`, `queue_days_per_platform`, `invalid{count,list}`, `rendered`, `hosted`, `would_post`, `late_window_hours` + `due_unconfigured`, `missing_media`, `cannot_render`, `posted`, `log`, `post_log`). Transcript goes to stderr + the runner log; stdout is the JSON only. Exit 1 only when `invalid.count > 0`.
- `tools/social/tests/test_cloud_run.py` — 8 tests: dry-run summary shape with no keys, configured platform → `would_post`, `SOCIAL_LATE_WINDOW_HOURS` override, 7 h window vs the PC runner's 6 h, live run posts inside the window / SKIPs outside (Pinterest same-day slots, fake HTTP), live run with no keys posts nothing and does not fail, hosting NOT CONFIGURED, `env` output (all MISSING / set, never prints a value, `--keys`), .gitignore change, render plan grouping, dry render.
- `data/social-post-log.csv` (header row only) and `data/social-runner.log` (transcripts of the two dry-runs) — now untracked-but-committable.

### Files changed

- `tools/social/__main__.py` — `cloud-run` subcommand (`--dry-run`, `--render-limit N`, `--no-render`); `env` now prints one line per platform (`<platform>: set` / `<platform>: MISSING A, B`), `env --keys` keeps the old per-key table. Exit 0 always for `env`.
- `tools/social/config.py` — `RUNNER_LOG_PATH`, `NEEDS['shopify_files']`, `PLATFORM_ORDER`, `missing()` treats `TIKTOK_ENABLED` as a required key for the TikTok API platform, `platform_lines()`.
- `tools/social/runner.py` — `action(item, now, grace=LATE_GRACE)` and `run(..., grace=LATE_GRACE)`; SKIP reason names the window used. PC behaviour unchanged (6 h).
- `tools/social/README.md` — commands table + new **Cloud** section (env var per platform and what it unlocks, cloud rendering notes, trigger prompt text, dry-run command).
- `.gitignore` — removed `data/social-post-log.csv` and `data/social-runner.log`; `data/social-media-cache.json`, `data/social-dryrun.json`, `__pycache__/`, `.pytest_cache/` stay ignored.
- `content/youtube/hoko/tts.py` — `piper_model()`: uses `HOKO_PIPER_MODEL` or the default `content/youtube/.cache/piper/en_GB-alan-medium.onnx`. Edge (en-AU) is still tried first.
- `content/youtube/hoko/reel.py` — `word_times` falls back to `even_words` (script words spaced evenly over 90 % of the voiceover) when `faster_whisper` is not installed. Beat-matched captions still happen on the PC.
- `content/youtube/calendar.md`, `CUTOFF.md`, `content/youtube/captions/*.txt` (33 files) — regenerated by the statuses-only rebuild (see commands).
- `content/youtube/reels/sealed/10734771798294/h1.json` — re-rendered metadata (duration 11.01 → 11.05, same Piper voice).

Not mine: `reports/backups/2026-10-17-shop-policies-before.json` (another step's untracked file; left alone).

### Decisions made (no questions asked)

- **Fallback voice = Piper `en_GB-alan-medium`.** edge-tts (en-AU William) fails from this container: aiohttp/certifi rejects the proxy CA (`CERTIFICATE_VERIFY_FAILED`), also with `SSL_CERT_FILE` set. Every reel rendered earlier on the PC already recorded `piper:en_GB-alan-medium`, so the cloud voice matches the existing clips. Logged per clip as `fallback voice`.
- **Deps installed in the container for the gate:** `pip install edge-tts piper-tts` (not in the repo; add to the environment setup script). ffmpeg/ffprobe, Pillow 12.3, numpy 2.5, requests were already present. faster-whisper is **not** installed — hence the even-spacing caption fallback instead of a 1 GB+ model install.
- **Late window 7 h** as a constant (`LATE_WINDOW_HOURS`), overridable with `SOCIAL_LATE_WINDOW_HOURS`. The PC runner keeps 6 h.
- **Topup threshold 10 days**, extends to today + 14 using `queue_builder.build(existing=…)` (keeps every existing future item). Dry-run also tops up (a queue write is not a post).
- **Hosting** reuses `hosting.public_url` unchanged (Shopify Files staged upload, cached in `data/social-media-cache.json`). cloud-run pre-hosts due IG/FB clips so the summary can list them; the runner then hits the cache.
- **Shorts / CardDrop / social-bank clips** cannot be rendered in the cloud (need the source video) → `cannot_render` in the summary (0 today).
- Platform list for `env`/`platforms`: instagram, facebook, youtube, pinterest, discord, tiktok_queue, tiktok (API, off), shopify_files.

### Commands run (trimmed)

```
$ python content/youtube/run.py source
RuntimeError: POST https://mock-store.myshopify.com/admin/api/2025-01/graphql.json → 404
→ NOT RUN: SHOPIFY_STORE / SHOPIFY_ADMIN_TOKEN are not set in this environment (no .env in the cloud). source.csv left as committed.

$ python3 -c "import sys; sys.path.insert(0,'content/youtube'); from hoko import calendar_gen; calendar_gen.build(render_beats=False)"
calendar.md: 72 rows, 72 missing reels      (12 rows blocked:draft-product — M7 / OP-18 / FB12 pre-order drafts; calendar re-ordered vs the committed one because it is rebuilt from current config/source)

$ python -m tools.social check
days per platform {'tiktok_queue': 15, 'pinterest': 15, 'youtube': 15, 'instagram': 15, 'facebook': 15, 'discord': 15}
PASS
$ python -m tools.social topup            # hot_sets come from content/youtube/config.json via the asset pool
165 items · days per platform {... all 15}
$ python -m tools.social check            # after topup
PASS

$ python3 -c "from tools.social import cloud_run; cloud_run.render(['content/youtube/reels/sealed/10734771798294/h1.mp4'], print, limit=1)"
deps missing: []
downloading fallback voice en_GB-alan-medium → content/youtube/.cache/piper
→ run.py reel sealed 10734771798294 --hook 1
rendered content/youtube/reels/sealed/10734771798294/h1.mp4 [piper:en_GB-alan-medium] — fallback voice
real 0m20.9s · ffprobe: video 1080x1920, audio, 11.066667 s

$ python -m tools.social cloud-run --dry-run      (rc=0)
{"mode": "dry-run", "now": "2026-10-17T14:11:05+11:00",
 "platforms": {instagram, facebook, youtube, pinterest, discord, tiktok_queue, tiktok, shopify_files: "NOT CONFIGURED"},
 "queue_days_per_platform": {"tiktok_queue": 15, "pinterest": 15, "youtube": 15, "instagram": 15, "facebook": 15, "discord": 15},
 "invalid": {"count": 0, "list": []},
 "rendered": [45 clips that would be rendered], "hosted": [], "would_post": 0,
 "due_unconfigured": {"facebook": 29, "instagram": 1, "pinterest": 1, "youtube": 29},
 "missing_media": 45, "cannot_render": [], "late_window_hours": 7.0}

$ python -m tools.social env                      (rc=0)
instagram: MISSING META_PAGE_TOKEN, IG_BUSINESS_ID, SHOPIFY_STORE, SHOPIFY_ADMIN_TOKEN
facebook: MISSING META_PAGE_TOKEN, FB_PAGE_ID, SHOPIFY_STORE, SHOPIFY_ADMIN_TOKEN
youtube: MISSING YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
pinterest: MISSING PINTEREST_TOKEN, PINTEREST_BOARD_ID
discord: MISSING DISCORD_WEBHOOK_PICKUPS
tiktok_queue: MISSING DISCORD_WEBHOOK_TIKTOK_QUEUE
tiktok: MISSING TIKTOK_ENABLED, TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REFRESH_TOKEN, SHOPIFY_STORE, SHOPIFY_ADMIN_TOKEN
shopify_files: MISSING SHOPIFY_STORE, SHOPIFY_ADMIN_TOKEN

$ python -m pytest tools/social/tests -q
43 passed in 0.72s
```

### NOT CHECKED

- A **live** `python -m tools.social cloud-run` from the CLI: the permission classifier refused the command in this session (flagged as a commit-like action). The same code path was exercised by `cloud_run.run()` in the live-mode tests (fake HTTP, posts inside the 7 h window, SKIP outside, no keys → nothing posts) and by the real one-clip render above.
- Real posting / Shopify Files upload: no platform keys exist in this environment; every platform reports NOT CONFIGURED.
- `run.py source` against Shopify (no token) — source.csv is the 17 Oct committed copy.

### MANUAL

**Ethan-only**
- Add the env vars to the Claude Code web environment (table in `tools/social/README.md` → Cloud). Nothing posts until then.
- Create the scheduled trigger (prompt text is in the README Cloud section). Consider two daily firings (morning + evening) so the 7 h window covers every slot.
- Add `pip install pillow numpy requests piper-tts edge-tts` (+ ffmpeg) to the environment setup script so cloud renders work without a manual install.
- Commit of this branch (per the run protocol, the parent run commits).

**PC-only**
- Beat-matched captions (faster-whisper) and Shorts / CardDrop / social-bank renders.
- Re-render any clip with the en-AU edge-tts voice if the Piper voice is not wanted (`run.py reel <kind> <id> --force`).


## Step 3 — Store hygiene

Read-only run against Shopify Admin GraphQL (MCP). Only write attempted: `shopPolicyUpdate` — **refused by Shopify (`Access denied… Required access: write_legal_policies`)**. No discounts, orders, fulfilments, products, prices or inventory touched.

### 3a. Shop policies

Backup of all five live policy bodies (as read 17 Oct 2026): `/home/user/hoko-collectables/reports/backups/2026-10-17-shop-policies-before.json`.

| Policy | ID | Last updated | Verdict vs canon |
|---|---|---|---|
| Refund | gid://shopify/ShopPolicy/50504663318 | 2026-10-03 | **ON CANON.** 7 days · not-as-described only (no change-of-mind) · sealed and international final sale · ACL unaffected · support email. No banned words. Only nit: says "within 7 days of delivery" — fine. No change needed. |
| Shipping | gid://shopify/ShopPolicy/50504728854 | 2026-10-11 | **OFF CANON — international singles rates.** Live text lists weight-tiered rates (NZ $18/$22 · Asia-Pac $21/$27 · Canada $23.50/$30 · US $29/$36 · UK/EU $28.50/$36 · RoW $34.50/$44). Canon is flat: **NZ / Asia-Pacific $25 · US / Canada / UK-EU $35 · rest of world $40**, signature required. AU tiers, dispatch lines and "Victoria" are all correct. Also says "free on orders over $150" (canon: "free tracked at $150+") and lacks the pre-order line. Replacement below. |
| Privacy | gid://shopify/ShopPolicy/50324734230 | 2026-10-03 | **OFF CANON — wrong jurisdiction.** Shopify's generic US/EEA template (GDPR, "sale/share", EDPB). No Privacy Act 1988 / APPs, no OAIC, no named pixels, no retention periods. Contact block (ABN, Victoria, support email) is correct. Replacement below. |
| Terms of service | gid://shopify/ShopPolicy/50504696086 | 2026-10-04 | **PASS with notes.** Governing law Victoria, Australia; contact block correct (email, Victoria, ABN); no banned words. Still Shopify's template: refers to "U.S. and foreign patent" law, "federal and state" law, "state or province", and has a blanket warranty disclaimer with no ACL carve-out. Not blocking; a one-paragraph ACL clause would be the only canon-relevant fix. Not rewritten. |
| Contact information | gid://shopify/ShopPolicy/50504761622 | 2026-10-04 | **OFF CANON — incomplete.** Has name, support email, Instagram, 1–2 business day reply line. Missing ABN 25 308 780 156, "Victoria, Australia", and the other channels (TikTok/YouTube/Pinterest @hokocollectables, Discord, eBay). Carries leftover ChatGPT `data-start`/`data-end` attributes. Replacement below. |

Banned-word scan of all five bodies: none of the live-auction W-word, the eBay seller-tier badge phrase, "mystery pack", "official", the same-day promise, the old sold-count figure, "HOKO10", or the capital city's name. Clean.

#### Write attempt
`shopPolicyUpdate(shopPolicy:{type:CONTACT_INFORMATION, body:…})` →
`Access denied for shopPolicyUpdate field. Required access: write_legal_policies access scope.`
The MCP token has no `write_legal_policies`; shipping and privacy would fail on the same scope so were not re-attempted. **MANUAL (Ethan-only):** Shopify admin → Settings → Policies → paste the blocks below. Nothing was changed on the store; read-back not applicable.

#### Paste block — Contact information
```html
<p><strong>HOKO Collectables</strong><br>Victoria, Australia<br>ABN 25 308 780 156</p>
<p>Email: <a href="mailto:support@hokocollectables.com">support@hokocollectables.com</a><br>We reply within 1–2 business days, Monday to Friday. Email is the fastest way to reach us about an order, a card's condition, or selling us your cards.</p>
<p>Instagram: @hoko.collectables<br>TikTok, YouTube and Pinterest: @hokocollectables<br>Discord: <a href="https://discord.gg/4eFCy5YPFU">discord.gg/4eFCy5YPFU</a><br>eBay: <a href="https://www.ebay.com.au/str/hokocollectables">ebay.com.au/str/hokocollectables</a></p>
<p>Collector first. Seller second.</p>
```

#### Paste block — Shipping policy
```html
<h2>Shipping</h2>
<p>Everything is dispatched from Victoria, Australia.</p>
<h3>Dispatch times</h3>
<ul>
<li>Singles and graded slabs: dispatched within 1–3 business days.</li>
<li>Japanese sealed (booster boxes imported from Japan by HOKO): dispatched tracked from Victoria within 2–4 business days once it lands.</li>
<li>Pre-orders: pre-order — dispatched tracked from Victoria once it lands. Release dates are set by the publisher and can move; we'll email you if they do.</li>
</ul>
<h3>Postage within Australia</h3>
<ul>
<li>Singles under $50: $3 untracked letter.</li>
<li>Singles $50 and over, and graded slabs: $10.95 tracked, free tracked at $150+.</li>
<li>Sealed boxes: $15.25 tracked, free on sealed orders of $250+.</li>
<li>Express Post $19.50 where offered at checkout.</li>
</ul>
<p>Untracked letters travel at your risk — Australia Post can't trace them, so we can't replace a letter that goes missing. If it matters, choose tracked.</p>
<h3>International (Australia Post, tracked, signature on delivery)</h3>
<ul>
<li>Singles and graded slabs: New Zealand and Asia-Pacific $25 · United States, Canada, UK and Europe $35 · rest of world $40. Signature on delivery is required on every international order.</li>
<li>Sealed product, flat rate per order: New Zealand $55 · Asia-Pacific $75 · United States and Canada $100 · UK and Europe $100 · rest of world $120.</li>
<li>Import duties and taxes in your country are your responsibility.</li>
<li>International orders are final sale.</li>
</ul>
<p>Questions: <a href="mailto:support@hokocollectables.com">support@hokocollectables.com</a></p>
```

Notes on the shipping draft: AU tiers and both dispatch lines are verbatim canon. International singles use the canon flat rates. The sealed-international flat rates (NZ $55 / Asia-Pac $75 / US-Canada $100 / UK-EU $100 / RoW $120) and Express Post $19.50 are carried over from the live delivery profiles — Ethan should confirm they still match checkout before pasting. The draft's shipping rates must match the actual Shopify shipping profiles or the policy will mis-state what checkout charges; the policy was not compared to the live profiles in this step (NOT CHECKED).

#### Paste block — Privacy policy (Privacy Act 1988 / APPs)
```html
<p>Last updated: 17 October 2026</p>
<p>HOKO Collectables (ABN 25 308 780 156, Victoria, Australia) runs www.hokocollectables.com. This policy explains what personal information we collect when you browse or buy from us, how we use it, who we share it with, and how you can get at it or complain. We are bound by the Privacy Act 1988 (Cth) and the Australian Privacy Principles (APPs), and we try to follow them even where the Act's small-business exemption might otherwise apply.</p>

<h2>1. What we collect</h2>
<ul>
<li><strong>Order and contact details:</strong> name, email, phone number, billing and shipping address, what you bought, what you paid, and any notes you leave on the order.</li>
<li><strong>Payment details:</strong> handled by our payment processors, not by us. We see the payment method type, the last four digits of a card and the payment status. We never see or store a full card number.</li>
<li><strong>Account details</strong> if you create one: login email, saved addresses and order history.</li>
<li><strong>Messages:</strong> emails, Discord or social DMs, and anything you send through our sell-your-cards or consignment forms (including photos of cards).</li>
<li><strong>Device and browsing data:</strong> IP address, browser and device type, pages viewed, items added to cart, referring site, collected automatically through cookies and similar tools (see section 4).</li>
</ul>
<p>We don't ask for sensitive information (health, religion, etc.) and we don't need it. Please don't send it to us.</p>

<h2>2. Why we collect it</h2>
<ul>
<li>To take your order, charge you, post it and send tracking.</li>
<li>To answer questions, sort out returns and handle not-as-described claims.</li>
<li>To quote on and buy or consign cards you offer us.</li>
<li>To send marketing email through Shopify Email, but only if you opt in at checkout or via our sign-up form. Every email has an unsubscribe link.</li>
<li>To understand how the store is used and to measure advertising (section 4).</li>
<li>To prevent fraud and meet our legal obligations, including Australian tax record-keeping.</li>
</ul>

<h2>3. Who we share it with</h2>
<ul>
<li><strong>Shopify Inc.</strong> hosts the store, checkout and customer database and processes your data on our behalf. Shopify stores data on servers in the United States and Canada. Shopify's own privacy policy is at shopify.com/legal/privacy.</li>
<li><strong>Payment processors</strong> (card, PayPal and similar) receive what they need to take your payment and run fraud checks.</li>
<li><strong>Australia Post</strong> and any other carrier receives your name, address and phone number to deliver your parcel.</li>
<li><strong>Advertising and analytics platforms:</strong> Meta (Facebook and Instagram) pixel, TikTok pixel, Pinterest tag and Google Analytics 4 receive browsing and purchase events as described in section 4.</li>
<li><strong>Grading companies</strong> (PSA, BGS, CGC) if you use our grading submission service: we pass on only what the submission needs.</li>
<li><strong>Government and law enforcement</strong> where the law requires it.</li>
</ul>
<p>We don't sell your personal information and we don't give it to other sellers or data brokers.</p>

<h2>4. Cookies, pixels and analytics</h2>
<p>Our site uses cookies and tracking pixels. Shopify sets cookies it needs to run the cart and checkout; these can't be turned off without breaking the store. On top of that we use:</p>
<ul>
<li><strong>Google Analytics 4</strong> to count visits, see which pages and products people look at, and where traffic comes from.</li>
<li><strong>Meta pixel, TikTok pixel and Pinterest tag</strong> to measure whether our posts and ads led to a sale, and to show our products to people who've visited the site before.</li>
<li><strong>Shopify's own analytics and customer-events tools</strong>, which feed the same information to Shopify.</li>
</ul>
<p>These tools collect your IP address, device identifiers, pages viewed, products viewed, cart adds and purchases, and may match this to an account you hold with that platform. You can control cookies in your browser, opt out of ad personalisation in your Meta, TikTok, Pinterest and Google account settings, and manage Shopify-level data sharing at privacy.shopify.com or our data-sharing opt-out page.</p>

<h2>5. Overseas disclosure</h2>
<p>Because the store runs on Shopify, your personal information is held on Shopify's servers in the United States and Canada. The advertising and analytics platforms above also process data in the United States and other countries where they operate. Payment processors may process data overseas too. By placing an order you agree to these transfers. We only use providers with their own published privacy commitments, but once information is overseas it is covered by the laws of that country rather than Australian law.</p>

<h2>6. How long we keep it</h2>
<ul>
<li>Order records (who bought what, when, for how much, and where it was sent) are kept for at least five years after the sale, as Australian tax law requires, and then deleted or de-identified.</li>
<li>Support emails and buy/consign quotes are kept for two years after the last message, then deleted.</li>
<li>Marketing subscription data is kept until you unsubscribe, then removed from the send list.</li>
<li>Analytics data is retained according to each platform's settings; we set Google Analytics 4 to its shortest retention option.</li>
</ul>

<h2>7. Security</h2>
<p>Checkout runs over HTTPS and payments are handled by PCI-compliant processors. Access to the Shopify admin is limited to the owner and protected with two-factor authentication. No system is perfectly secure; if we learn of a data breach that is likely to cause you serious harm we will notify you and the Office of the Australian Information Commissioner (OAIC) as the Notifiable Data Breaches scheme requires.</p>

<h2>8. Access, correction and deletion</h2>
<p>You can ask us at any time for a copy of the personal information we hold about you, ask us to correct it, or ask us to delete it. Email <a href="mailto:support@hokocollectables.com">support@hokocollectables.com</a> from the address on your order and we'll respond within 30 days. We may need to keep order records for tax purposes even after a deletion request; we'll tell you if so. If you have an account you can also update your details and addresses yourself after logging in.</p>

<h2>9. Complaints</h2>
<p>If you think we've mishandled your personal information, email support@hokocollectables.com with "Privacy complaint" in the subject line. We'll acknowledge it within 7 days and aim to resolve it within 30. If you're not happy with our answer you can complain to the Office of the Australian Information Commissioner at <a href="https://www.oaic.gov.au">www.oaic.gov.au</a> or on 1300 363 992.</p>

<h2>10. Children</h2>
<p>The store is for adults. We don't knowingly collect personal information from anyone under 18. If you think a minor has given us their details, email us and we'll remove them.</p>

<h2>11. Changes</h2>
<p>We'll update this page when our practices change and put the new date at the top. Material changes will be flagged on the site.</p>

<h2>12. Contact</h2>
<p>HOKO Collectables<br>ABN 25 308 780 156<br>Victoria, Australia<br><a href="mailto:support@hokocollectables.com">support@hokocollectables.com</a></p>
```

Privacy draft assumptions to confirm before pasting: GA4 retention set to the shortest option; 2FA on the Shopify admin; Meta pixel, TikTok pixel and Pinterest tag are actually installed (named because the brief said so, not verified on the storefront). If any aren't installed, delete that line rather than leave a false statement.

### 3b. Discount-eligible collection (READ ONLY)

`discount-eligible` = gid://shopify/Collection/532514177302 "Discount Eligible", smart collection, **6,160 products**. Rules (ALL must match): variant price < 100 · title NOT CONTAINS "Sealed" · NOT "Booster Box" · NOT "Booster Case" · NOT "Booster Pack" · NOT "— Japanese".

Method note: `collection_id:` combined with `tag:` returns 0 in Shopify product search (index quirk), but `collection_id:` + `status:` / `product_type:` works and sums to 6,160. Candidate lists were therefore pulled store-wide by tag/title/type and each product's membership checked with `inCollection(id:…)`. `title:*Japanese*` wildcard search was used for titles (146 hits store-wide).

#### By status
| Status | Count |
|---|---|
| ACTIVE | 605 |
| DRAFT | 4,562 |
| ARCHIVED | 992 |
| **Total** | **6,160** (sum 6,159 — one product changed status mid-read) |

#### By productType (all statuses / active only)
| productType | All | Active |
|---|---|---|
| Pokemon Single | 2,394 | 20 |
| Magic: The Gathering Single | 1,700 | 263 |
| One Piece Singles | 489 | 38 |
| Trading Card | 479 | 195 |
| Trading Card Single | 141 | 75 |
| Dragon Ball Super Single | 95 | 1 |
| Lorcana Single | 95 | 10 |
| Singles | 26 | 0 |
| Card Lot | 12 | 0 |
| Subscription Box | 7 | 0 |
| Bulk Lot | 3 | 0 |
| Card Bundle | 3 | 3 |
| Graded Trading Card - PSA | 1 | 0 |
| Trading Card Single - MTG | 1 | 0 |
| Trading Card Single - Pokemon | 1 | 0 |
| (blank productType) | 713 | 0 |
| Accessories, Grading Service, One Piece TCG, Other Product, Sealed Booster Box, Sealed Product, Sealed Trading Cards - Booster Box | 0 | 0 |

Takeaway: the title rules keep every real Japanese booster box / pack / case out of the collection (all 100+ `jp-sealed`/`booster-box` products checked return `inCollection: false`, including the active M3, M1S, M5, M6, OP-07/11/12/16, sv7/sv8/sv8a/sv3a/s12a boxes and the three [PRE-ORDER] drafts). Active graded slabs are out too — but only because they're priced ≥ $100 (see risk below).

#### Products in the collection that match the Japanese-sealed / pre-order / slab / repack indicators

**Japanese sealed indicators (tags `japanese`+`jp-sealed`) — all ARCHIVED, all "mystery box" subscriptions:**
| Product ID | Title | Status |
|---|---|---|
| gid://shopify/Product/10462213964054 | HOKO Japanese Pokemon Mystery Box — Bronze | ARCHIVED |
| gid://shopify/Product/10462225170710 | HOKO Japanese Pokemon Mystery Box — Silver | ARCHIVED |
| gid://shopify/Product/10462226514198 | HOKO Japanese Pokemon Mystery Box — Gold | ARCHIVED |

**Pre-order indicator (tag `pre-order`):**
| Product ID | Title | Status |
|---|---|---|
| gid://shopify/Product/10437759140118 | Boa Marigold OP07-052 500 Years in the Future Pre-Release Cards One Piece NM | ARCHIVED (single mis-tagged pre-order) |

**Graded slab indicators (type `Graded Trading Card - PSA` / tags `slab`, `psa`, `graded`):**
| Product ID | Title | Status |
|---|---|---|
| gid://shopify/Product/10443831410966 | Bellsprout 69 Topps Chrome T.v. Pokemon PSA 9 | ARCHIVED (tag duplicate-archived) |
| gid://shopify/Product/10493850779926 | HOKO Silver Mystery Box — Monthly Subscription (tag graded, mystery-pack) | ARCHIVED |
| gid://shopify/Product/10493851599126 | HOKO Gold Mystery Box — Monthly Subscription (tag graded, mystery-pack) | ARCHIVED |

**Repack / "mystery" language in collection (banned customer-facing word) — report only:**
| Product ID | Title | Status |
|---|---|---|
| gid://shopify/Product/10495496454422 | Ultimate TCG Mystery Chaos Bundle — 20+ Cards Multi-Game \| HOKO Collectables (Card Bundle, tag mystery-pack) | **ACTIVE — live and discount-eligible** |
| gid://shopify/Product/10530148417814 | The HOKO Monthly Box — Subscription (tag mystery) | DRAFT |
| gid://shopify/Product/10437782864150 | Rip & Ship — Mystery Card Pack (You Pick the Set) | ARCHIVED |
| gid://shopify/Product/10493849993494 | HOKO Bronze Mystery Box — Monthly Subscription | ARCHIVED |
| gid://shopify/Product/10499888677142 | HOKO 16-Card Mystery Chaos Bundle — Pokemon, MTG, Dragon Ball Multi-TCG | ARCHIVED |
| gid://shopify/Product/10502685458710 | HOKO 16-Card Mystery Chaos Bundle — Pokemon, MTG, Dragon Ball Multi-TCG | ARCHIVED |
("Mystery Garden" and "Might Solve a Mystery" are card names — fine.)

**Japanese singles in the collection (tag `japanese`/`pokemon-japanese` or title contains "Japanese") — 65 products, 0 ACTIVE, no action needed; listed for completeness:**

DRAFT (Pokemon Single / Singles, tag japanese): 10534845514006 Ivysaur 167/165 · 10534845546774 Machoke 177/165 · 10534845579542 Roaring Moon ex 218/187 · 10534845612310 Meloetta ex 170/086 · 10534845645078 Keldeo ex 169/086 · 10534861668630 Oddish (Master Ball) 043/165 · 10534861734166 Geodude (MB) 074/165 · 10534861799702 Rhyhorn (MB) 111/165 · 10534861832470 Cycling Road 165/165 · 10534861865238 Doduo 142/190 · 10534861898006 Magnemite (MB) 081/165 · 10534861930774 Pidgeotto (MB) 017/165 · 10534861996310 Clefable (MB) 036/165 · 10534862553366 Zapdos ex 194/165 · 10534862586134 Dragonair 182/165 · 10534862618902 Omanyte 180/165 · 10534862651670 Nidoking 174/165 · 10534862684438 Mr. Mime 179/165 · 10534862749974 Raging Bolt ex 222/187 · 10534862782742 Caterpie 172/165 · 10534862815510 Genesect ex 172/086 · 10534862848278 Iron Crown ex 214/187 · 10534862881046 Palafin ex 207/187 · 10655228100886 Vaporeon 134/165.

DRAFT (type "Trading Card", tag pokemon-japanese — stub-titled duplicates of the above): 10543510520086 Keldeo ex · 10543510552854 Mega Lopunny EX 114/080 · 10543510585622 Roaring Moon ex · 10543510618390 Meloetta ex · 10543510651158 Palafin ex · 10543510749462 Iron Crown ex · 10543510782230 Raging Bolt ex · 10543510814998 Caterpie · 10543510847766 Machoke · 10543510880534 Mr. Mime · 10543510913302 Nidoking · 10543510946070 Giovanni's Charisma 197/165 · 10543510978838 Daisy's Help 198/165 · 10543511011606 Zapdos ex · 10543511044374 Omanyte · 10543511077142 Ivysaur · 10543511109910 Dragonair · 10543511175446 Clefable (MB) · 10543511208214 Pidgeotto (MB) · 10543511240982 Magnemite (MB) · 10543511273750 Doduo · 10543511372054 Cycling Road · 10543511470358 Rhyhorn (MB) · 10543511601430 Oddish (MB) · 10543511634198 Rigid Band (MB) 159/165 · 10543511666966 Mega Charizard X EX 013/080 · 10543536341270 Jynx ex 193/165.

ARCHIVED: 10543510683926 Genesect ex (dup) · 10543511142678 Poliwhirl 176/165 · 10543511568662 Geodude (MB) (dup) · 10416947790102 Team Rocket's Meowth 109/098 · 10416947921174 Skeledirge EX 324/190 · 10416947953942 Frigibax 233/190 · 10416948117782 Forretress EX 320/190 · 10416948248854 Abomasnow 200/190 · 10416948379926 Tornadus 078/086 · 10416948412694 Lugia V 079/098 · 10416948543766 Kadabra 254/190 · 10416948576534 Eevee 125/187 · 10416948707606 Varoom 114/187.

#### Risks worth a decision (report, don't act)
1. **Slabs are only excluded by price.** The ACTIVE slabs (10655248122134 Bellsprout PSA 9, 10655248220438 Magikarp PSA 9, 10655248613654 Detective Pikachu BGS 9, 10655248711958 Nico Robin BGS 9.5, 10655248777494 Nami BGS 10, 10655248810262 Pikachu 27 PSA 10, and DRAFT 10655248154902 / 10655248679190) are typed "Pokemon Single"/"One Piece Singles" with tag `graded` only — no `slab`/`psa`/`bgs` tag, and the collection has no slab rule. Any slab priced under $100 becomes WELCOME10/THANKS10-eligible automatically. Suggest a `tag NOT EQUALS graded` rule (Ethan's call).
2. **Ultimate TCG Mystery Chaos Bundle (10495496454422) is ACTIVE, discount-eligible, and uses banned repack language** in title and tag `mystery-pack`.
3. No pre-order or Japanese-sealed title rule gap found: "[PRE-ORDER]" boxes are kept out by "Sealed"/"Booster Box" in their titles, not by a pre-order rule. A pre-order *single* (e.g. a promo) would slip in.

### 3c. Online Store orders paid + unfulfilled (READ ONLY)

Query `financial_status:paid AND fulfillment_status:unfulfilled` → **64 orders**. 62 are eBay-sourced (sourceName `ebay`, channel `ebay-au` "eBay", tags eBay/eBay-AU) — Marketplace Connect mirrors eBay orders in but never marks them fulfilled; excluded. `fulfillment_status:unshipped OR partial` (eBay excluded) returned the same two orders.

| Order | ID | Created (AEST) | Processed | Total | Customer | Line items | Source / channel | Days since paid | Business days (Mon–Fri AEST) | Flag |
|---|---|---|---|---|---|---|---|---|---|---|
| #1058 | gid://shopify/Order/7073331347734 | 2026-03-09 22:28 | 2026-03-09T12:28:59Z | A$15.23 | ethan | Hero FINAL FANTASY Magic: The Gathering NM Foil ×1 | web / Online Store | 221 | 159 | **> 3 business days** — looks like Ethan's own test order (customer first name "ethan", $15.23). |
| #1434 | gid://shopify/Order/18911228297494 | 2026-09-27 19:48 | 2026-09-27T09:48:38Z | A$145.00 | ethan | Pokemon Abyss Eye (M5) Sealed Japanese Booster Box ×1 | shopify_draft_order, tag `TEST-DS`, no channel | 19 | 15 | **> 3 business days** — tagged TEST-DS, draft order; drop-ship test. |

No genuine customer Online Store order is sitting unfulfilled. **MANUAL (Ethan):** mark #1058 and #1434 fulfilled or archive them so they stop polluting the unfulfilled count.

### 3d. Abandoned checkouts, last 14 days (READ ONLY)

`abandonedCheckouts(query:"created_at:>=2026-10-03")` → **9 checkouts, total A$344.15**, none recovered (`completedAt` null on all), no discount codes used.

Over A$50: **none.** (Largest is A$47.61.)

All nine, for context:
| Created (UTC) | Value | Line items |
|---|---|---|
| 2026-10-15 09:52:33 | A$47.61 | Pokémon Paradox Rift Card Bundle — 10 Near Mint Cards ×1 |
| 2026-10-15 09:52:04 | A$47.61 | same |
| 2026-10-15 09:52:03 | A$47.61 | same |
| 2026-10-15 09:51:34 | A$47.61 | same |
| 2026-10-15 09:51:03 | A$47.61 | same |
| 2026-10-15 06:04:04 | A$7.00 | Magic the Gathering Land Card set 10 Units of Island (random arts) ×1 |
| 2026-10-06 09:14:33 | A$32.97 | Fennekin 025/195 Common Silver Tempest Pokemon Reverse Holo Near Mint ×1 |
| 2026-10-04 15:43:03 | A$33.06 | same |
| 2026-10-04 10:24:03 | A$33.07 | same |

Products in 3+ abandoned checkouts:
| Product | Checkouts |
|---|---|
| Pokémon Paradox Rift Card Bundle — 10 Near Mint Cards | 5 (all within 90 seconds on 15 Oct — one shopper retrying checkout, or a bot; treat as 1 real intent) |
| Fennekin 025/195 Common Silver Tempest Pokemon Reverse Holo Near Mint | 3 (4–6 Oct, totals ~A$33 for a common reverse holo — postage is most of that; same shopper bounced three times, likely postage shock on a sub-$5 card) |

### Result

- 3a Shop policies: **PASS (audit) / MANUAL (writes)** — backup saved; refund and terms on canon; shipping, privacy, contact off canon with replacements drafted; `shopPolicyUpdate` refused (`write_legal_policies` missing).
- 3b Discount-eligible collection: **PASS** — 6,160 products; no live Japanese sealed, pre-order box or slab inside; 1 ACTIVE repack-language bundle and 7 ARCHIVED/DRAFT mystery-box products inside; slab exclusion relies on price only.
- 3c Paid + unfulfilled Online Store orders: **PASS** — 2 found, both Ethan's own test orders (#1058 221 days, #1434 19 days), no customer order outstanding.
- 3d Abandoned checkouts: **PASS** — 9 / A$344.15 / none over A$50.

#### NOT CHECKED
- Shipping policy vs the live delivery profiles (rates actually charged at checkout) — token/time; policy draft carries live-profile figures from CLAUDE.md, confirm before pasting.
- Whether Meta pixel, TikTok pixel, Pinterest tag and GA4 are actually installed on the storefront (privacy draft names them per brief).
- The 62 eBay-sourced paid+unfulfilled mirror orders (out of scope; eBay Seller Hub is source of truth).
- Terms of service was not rewritten (judged on canon for the checked items).

#### MANUAL
- **Ethan-only:** paste the three replacement policies (Contact, Shipping, Privacy) in Shopify admin → Settings → Policies; or grant the MCP app `write_legal_policies` and re-run 3a.
- **Ethan-only:** fulfil/archive test orders #1058 and #1434.
- **Ethan's call (pricing/collection rule):** add a `graded`-tag exclusion to the Discount Eligible smart collection; decide on the ACTIVE "Ultimate TCG Mystery Chaos Bundle" (banned repack wording, discount-eligible).
- **Ethan's call:** optional ACL carve-out paragraph in Terms of service.


## NOT CHECKED
- eBay AU sold counts (ebay.com.au 403 from the cloud) — the top-5 trim in 1b.
- Kanade's actual current stock (the Price List sheet has prices only, last modified 7 Aug).
- Shopify Payments plan rate (assumed 1.75% + $0.30).
- Live `python -m tools.social cloud-run` (permission classifier refused the CLI call; live path covered by tests + the real render). Real posting and Shopify Files upload (no keys here).
- Shipping policy vs the live delivery profiles at checkout; whether the Meta/TikTok/Pinterest/GA4 pixels are actually installed; Terms of Service not rewritten (still Shopify US template wording, no ACL carve-out).

## MANUAL

**Ethan only**
- Decide the eBay sold-count trim by hand (or run this step from the PC where eBay is reachable): 11 zero-stock boxes stay DRAFT, 11 in-stock boxes stay ACTIVE until then.
- M6a (30th Celebration, 15398993723670) and OP-17 (15402647453974 / 10734775730454) are "newest sets" but were not candidates — list price + which supplier, then they can be routed.
- Kanade's Storm Emeralda price (20,980 yen) looks stale vs Urara no-shrink 9,300; confirm before ordering M6 singles.
- Pre-orders M7 / OP-18 / FB12 remain DRAFT until they appear on the Urara list.
- Paste the three policy replacements (Contact, Shipping, Privacy) in Settings → Policies, or grant the connector `write_legal_policies`. Terms of Service also needs an ACL sentence.
- Decide on slabs under $100 in `discount-eligible` (price-only rule, no slab exclusion) and on the live "Ultimate TCG Mystery Chaos Bundle" (10495496454422): repack wording, discount-eligible.
- Fulfil or archive your two test orders #1058 and #1434 (only non-eBay paid+unfulfilled orders).
- Add the social env vars to the Claude Code web environment, create the `cloud-run` scheduled trigger (prompt in `tools/social/README.md` → Cloud), add `pip install pillow numpy requests piper-tts edge-tts` + ffmpeg to the environment setup script.
- 11 Nov–7 Dec BF/Xmas reels and the one cloud-rendered clip use the Piper fallback voice; re-render on the PC in en-AU with `--force` if you want your voice match.

**PC only**
- `python content/youtube/run.py source` (needs the Shopify token), then calendar rebuild.
- Beat-matched captions need faster-whisper (cloud used even spacing). Shorts / CardDrop / social-bank renders.
- eBay sold-count trim for 1b (eBay unreachable from the cloud).

## COMPLETE
