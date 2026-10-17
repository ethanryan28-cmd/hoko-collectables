# QUEUE

Work queue for Claude Code runs. Newest first. Each entry: date · what · status · where the report is.

## 2026-10-17 · BF media 2, run 2: resume check — already merged, verified (`claude/bf-media-render-queue-376p0p`)
- **Status:** verified, nothing redone. Report → `REPORT-2026-10-17-bf-media-2.md` (## Run 2)
- main `e967b58`, 71 mp4s / 86.5 MB on origin/main, 54 tests OK.

## 2026-10-17 · BF media 2: live William gate, 71 clips rendered + committed, merged (`claude/bf-media-1017`)
- **Status:** built, merged. Reports → `REPORT-2026-10-17-bf-media.md` (tts fix, stopped at gate) + `REPORT-2026-10-17-bf-media-2.md` (this run)
- Network open this session (PyPI 200, Bing reachable). The branch's `tts.py` proxy-CA fix rendered live (`edge-tts:en-AU-WilliamMultilingualNeural`, verification on, no sitecustomize). 54 tests OK.
- 71/71 mp4s rendered in William (45 sealed incl. EB-05/M7/FB12 h3 forced, 12 slab, 4 tips, 4 roundups, 6 BF beats). ffprobe PASS 1080×1920, audio, 8–20 s, no "$" spoken. **86.5 MB committed**, mp4s now in git. 30 sidecars piper → William.
- Queue: check PASS 60% hot everywhere, dry-run 0 invalid / **0 missing media** (was 30), all platforms NOT CONFIGURED.
- **Ethan to do:** BF free-shipping automatic edit; platform keys; env setup line + network allowlist (in the report MANUAL).

## 2026-10-17 · BF media: tts.py proxy-CA fix, un-ignore reels mp4s, re-render + keep (`claude/bf-media-1017`)
- **Status:** built, **NOT merged** — stopped at the Step 1 live-render gate. Report → `REPORT-2026-10-17-bf-media.md`
- Cloud run with every render host policy-denied (403 at the proxy): PyPI, `speech.platform.bing.com`, `huggingface.co`. No edge-tts / piper / faster-whisper installable, so **0 clips rendered, 0 MB committed**; the 38 bf-render mp4s are still gone.
- Done + tested: `content/youtube/hoko/tts.py` trusts `SSL_CERT_FILE` / `REQUESTS_CA_BUNDLE` / `/root/.ccr/ca-bundle.crt` via a verifying `ssl.create_default_context(cafile=…)` handed to edge-tts' connector **and** its per-request context (edge-tts 7.x overrides the connector), `proxy=$HTTPS_PROXY`; no env var → unchanged PC path. 7 new unit tests, 54 OK. `content/youtube/.gitignore` now keeps `reels/**/*.mp4` (out/, wav, cache, inbox still ignored). README Cloud line added.
- Queue: check PASS 15 days / 60% hot on all 6, 0 invalid, **missing media 30** (the unrendered clips), all platforms NOT CONFIGURED.
- **Ethan to do:** merge the branch or re-run with network (prompt line in the report MANUAL); PC render + push the mp4s meanwhile; BF automatic edit + platform keys still pending.

## 2026-10-17 · BF render: 38 clips in en-AU, queue check, BF automatic re-read (`claude/bf-render-1017-idka4q`)
- **Status:** built, merged. Report → `REPORT-2026-10-17-bf-render.md`
- Cloud run, PyPI reachable this time: edge-tts William worked through the proxy CA (session-only sitecustomize, no repo code change). 38/38 clips rendered + ffprobe PASS (1080×1920, audio, 8–20 s, no "$" spoken): EB-05/M7/FB12 h3 (`stale_render` cleared), the 27 the queue listed missing, 6 BF beats (text unchanged, none said $100). mp4s are gitignored, so only sidecars are committed.
- Queue: topup kept all 165 items, check PASS, 60% hot on every platform, 0 invalid, 0 missing media, all platforms NOT CONFIGURED; 47 tests OK. `source.csv` not refreshed (no token): committed rows already right.
- BF free-shipping automatic read live: still "$100+, all products, AU". CLAUDE.md line now says so explicitly.
- **Ethan to do:** change that automatic to Japanese Sealed / no minimum; PC: `run.py source` + `tools.social render` (mp4s are local-only); decide on the 3-line `tts.py` proxy fix.

## 2026-10-17 · BF lock-in: M7 + FB12 live, newest-set links, BF page/collection, social queue 60% newest (`claude/bf-lockin-1017`)
- **Status:** built, merged. Report → `REPORT-2026-10-17-bf-lockin.md`
- M7 + FB12 ACTIVE, CONTINUE, 7/7 channels. FB12 = Bandai JP pack art; **M7 = HOKO placeholder card (no publisher art exists yet)** — swap when pokemon-card.com publishes. 24/24 ACTIVE jp-sealed on all 7 channels.
- M6a + EB-05 guides link the other four newest; 2026 guide has a "Newest releases" list; 0 dead links across 41 articles. BF page = 5 newest tiles + collection link, no postage figure; `japan-direct-sealed` sorted M6a, EB-05, OP-18, M7, FB12 first.
- Social: `hot_sets` = the 5, builder pushes them to ≥60% (2-day hot repeat), BF-week block 20–30 Nov built in (BFDROP5 + box drop list, product/collection links only), check PASS, 47 tests. All platforms NOT CONFIGURED. CLAUDE.md: newest-sets rule + prices-are-Ethan's line.
- 07:27 Ethan ruled: free postage on ALL sealed, no minimum; M7 stays live with the placeholder. Page/email/captions reworded (`claude/bf-postage-1017`).
- **Ethan to do:** edit the scheduled BF free-shipping automatic (all orders $100+ → Japanese Sealed collection, no minimum); social keys + piper in the env setup; PC re-render of EB-05/M7/FB12 h3 clips.

## 2026-10-17 · Organic-2 run 2: re-verify + eBay box maths (`claude/organic-2-1017-9a79lu`)
- **Status:** built, merged. Report → `REPORT-2026-10-17-organic-2.md`
- Steps 1–6 skipped as done (run 1), re-verified live: 2026 guide + JP cards guide unchanged, 6 JP-sealed articles 1 DRAFT link (EB-05, accepted), 20/20 × 7 channels, social env/dry-run/check PASS, 44 tests OK. FB12/M7 JAN still blank.
- eBay maths: `data/ebay-box-maths-2026-10-17.csv`, 20 rows, bulk landed at ¥6,500/12 freight, FX 0.009112. eBay price now + last-sold NOT CHECKED (no export, 403) → Shopify stand-in. Nihil Zero M3 no-shrink cost is a flagged proxy. 0 Shopify writes.
- **Ethan to do:** pick the eBay repricing rule; drop an eBay active-listings export in `data/` for real eBay columns.

## 2026-10-17 · Social poster cloud-run 17:12 (`claude/social-cloud-2026-10-17-1711`)
- **Status:** ran, merged. Report → `reports/social/REPORT-2026-10-17T1712+1100.md`
- All 8 platforms NOT CONFIGURED (no env keys in the cloud environment). 0 posted, 0 FAIL, 2 SKIP (stale 07:00 / 10:00 slots). Queue 15 days/platform, 0 invalid. 49 clips unrendered — `piper-tts` could not be installed (PyPI unreachable from the sandbox).
- **Ethan to do:** set the platform env vars + add `piper-tts` to the environment setup script (or render on the PC).

## 2026-10-17 · Organic-2: JP-sealed links, channels, social readiness, JAN retry (`claude/organic-2-1017-h3c9kj`)
- **Status:** built, merged. EB-05 guide → DRAFT pre-order link accepted by Ethan. Report → `REPORT-2026-10-17-organic-2.md`
- 2026 guide stock list rebuilt from live: 14 Pokémon + 4 One Piece boxes, OP-17/OP-13 out, M6a → product, range $115–$470. JP cards guide: price/pull-rate bullet replaced with the per-box line; the separate pull-rate bullet removed (follow-up). Both read back byte-exact.
- Dead-link sweep: 40 articles, 3 DRAFT links → 1 left (EB-05, no ACTIVE equivalent). `data/deadlinks-2026-10-17-organic-2.csv`
- Channels: 20/20 ACTIVE jp-sealed on all 7, no writes. Social: env all MISSING, dry-run 0 invalid, Discord-only test added (44 tests OK). FB12/M7 JAN still blank.
- **Ethan to do:** social keys + clip render (MANUAL in the report); EB-05 link goes live when the pre-order is published.

## 2026-10-17 · Organic run: JANs, product + collection SEO, article internal links (`claude/organic-1017`)
- **Status:** built. Report → `REPORT-2026-10-17-organic.md`
- JAN barcode on all 20 live Japanese boxes + EB-05 (13 written, 8 already present and re-verified; OP-18 bonus) — sources per row in `data/jan-2026-10-17.csv`. FB12 / M7 drafts blank (no verifiable JAN yet).
- SEO title ≤ 60 / description ≤ 155 / main-image alt on the 21 + the three other pre-order drafts; `japan-direct-sealed` collection SEO set.
- 5 JP-sealed articles got one internal-link sentence each (collection + a live box; M6a ↔ EB-05 guides cross-linked). Backups in `reports/backups/2026-10-17-organic-*`.
- **Ethan to do:** nothing blocking. Optional: fix the 2026 guide's stock list (links OP-17/OP-13 drafts, calls M6a a pre-order) — see report findings.

## 2026-10-17 · Newest push: M6a copy to canon, OP-17 duplicate archived, source from connector, two articles (`claude/newest-push-1017`)
- **Status:** built. Report → `REPORT-2026-10-17-newest-push.md`
- M6a (15398993723670) description rebuilt on the M5 template (cutoff, proof, authenticity, spot-a-fake, returns; no-shrink + 20-pack lines kept), `label:NEEDS-COMP` dropped, SEO description added.
- OP-17: kept 10734775730454, archived 15402647453974, 301 from the old handle.
- `content/youtube/sealed/source.csv` + `slabs/source.csv` rebuilt from the connector (20 ACTIVE boxes + 2 pre-order drafts; 6 slabs); new `policy` column so CONTINUE boxes at 0 stock are promotable; 3 clips rendered in the cloud; queue rebuilt — all 20 live boxes in 14 days, M6a on 19 Oct.
- Articles published: M6a buying guide, EB-05 release/pre-order guide.
- **Ethan to do:** re-voice the 3 cloud clips in en-AU on the PC if wanted; `run.py source` on the PC now emits `policy`.

## 2026-10-17 · Pre-orders run: M6a/OP-17 routing, EB-05 pre-order draft, cutoff gate (`claude/preorders-1017`)
- **Status:** built. Report → `REPORT-2026-10-17-preorders.md`
- M6a no-shrink routed `route:urara-batch` (stays DRAFT, status write not in scope); OP-17 ×2 stay DRAFT (Kanade case-only floor $390 vs $200/$175, Urara 0 stock). Rows appended to `data/routing-2026-10-17.csv`.
- 90-day release scan: only EB-05 Heroines vol.2 (31 Oct) had no product → DRAFT pre-order 15431829848342 at $235 (median of AU Japanese-box pre-orders), top of `japan-direct-sealed`. M7 / OP-18 untouched. `data/preorders-2026-10-17.csv`.
- Cutoff gate: M5 sealed + OP-16 were missing the 7 Dec line → added (backup in `reports/backups/`). All 19 ACTIVE jp-sealed now carry it.
- **Ethan to do:** flip M6a to ACTIVE if wanted; merge the duplicate OP-17 listings; confirm EB-05 price when Urara lists it.

## 2026-10-17 · Consolidated run: JP sealed routing, social cloud-run, store hygiene (`claude/consolidated-1017`)
- **Status:** built. Report → `REPORT-2026-10-17-consolidated.md`
- Routing: M5 sealed + OP-16 back ACTIVE (CONTINUE), 15 boxes tagged `route:kanade-single` / `route:urara-batch` + metafield `hoko.supplier`, 3 raise-to-floor prices, `japan-direct-sealed` re-sorted, BF page tiles, `data/routing-2026-10-17.csv`, `hot_sets` updated. eBay sold-count trim NOT CHECKED (eBay 403 from the cloud) — no in-stock box drafted.
- Social: `python -m tools.social cloud-run` + `env`, README Cloud section, 43 tests, queue topped to 15 days/platform; run log + CSV now committed.
- Hygiene: policy diffs + paste blocks (connector lacks `write_legal_policies`), discount-eligible clean, 0 customer orders stuck, abandoned checkouts read.
- **Ethan to do:** see MANUAL in the report (env vars + trigger, paste policies, eBay trim, M6a/OP-17 pricing)

## 2026-10-17 · Finish run: CLAUDE.md canon rewrite, store drift gate, pre-order gates, 14-day cutoff (`claude/finish-1017`)
- **Status:** built. Report → `REPORT-2026-10-17-finish.md`
- CLAUDE.md rewritten to canon; dead live-show / sealed-only docs → `docs/archive/`; repo banned-word gate 0; live-store drift scan + fixes; discounts read-only; M7 / OP-18 / FB12 kept DRAFT (not on the Urara list yet); lead time 21 → 14 days, cutoff Mon 7 Dec; `reports/shopify-inventory-2026-10-17.csv`
- **Ethan to do:** see MANUAL in the report

## 2026-10-17 · Social auto-poster + brand canon + M7 + relist + BF email (`ethan/social-autoposter`)
- **Status:** built. Report → `reports/REPORT-2026-10-17T1140+1100.md`
- `tools/social/` (14-day queue → IG/FB/YT/Pinterest/Discord + TikTok phone pack), brand canon sweep live + draft theme, M7 spec, `tools/relist-reconcile.py`, `content/email/bf-early-access.*`
- **Ethan to do:** see MANUAL in the report (env keys → render → dry-run → install-tasks.ps1; publish the draft theme; meta description in Chrome)

## 2026-10-13 · HOKO content machine (`content/youtube/`)
- **Status:** built. Report → `content/youtube/REPORT.md`
- Reel engine, Shorts cutter + packager, 14 Oct → 24 Dec calendar, IG/YT auto-publish, comment queue
- **Ethan to do (MANUAL):**
  1. Fill `content/youtube/.env` from `.env.example` (IG, YT OAuth, Shopify Admin token)
  2. `python content/youtube/run.py cutoff` → check the example → `--apply` (Shopify write was blocked in the cloud run)
  3. `python content/youtube/run.py schedule` on the PC (registers "HOKO publish", 6:30pm daily)
  4. `python content/youtube/run.py reel sealed all --force` + `reel slab all --force` on the PC to re-voice reels in en-AU (cloud run used a fallback voice)
  5. Create the $5-off BF box code in Shopify (not created — by design)
