# QUEUE

Work queue for Claude Code runs. Newest first. Each entry: date · what · status · where the report is.

## 2026-10-18 · Social poster cloud-run 07:11 (`claude/social-cloud-2026-10-18-0711`)
- **Status:** ran, merged. Report → `reports/social/REPORT-2026-10-18T0711+1100.md`
- All 8 platforms NOT CONFIGURED (no env keys in the cloud environment). 0 posted, 0 FAIL, 0 SKIP (queue starts 18 Oct; 57 due in the 14-day FB/YT windows). Queue 15 days/platform, 0 invalid, 0 clips missing. PyPI still unreachable (piper-tts / edge-tts not installable) — no render was needed.
- **Ethan to do:** set the platform env vars; add `edge-tts piper-tts` to the environment setup script.

## 2026-10-19 · Copy-hygiene follow-up: banned-word allowlist, Mass of Mysteries SEO, bundle handle + 301, condition scale (`claude/copy-hygiene-followup-1019`)
- **Status:** built, merged. Report → `REPORT-2026-10-19-copy-hygiene-followup.md`
- `tools/banned_words.py` + allowlist (Mass of Mysteries, Mystical Archive, Chaos Warp; case-sensitive whole phrase), the repo gate uses it, 5 tests. 2 real misses reworded (`index.html` demo, content-strategy doc).
- Mass of Mysteries SEO title 68 → 58. Multi-game bundle handle → `multi-game-card-bundle-20-cards`, 301 from the old URL (old 301, new 200), condition paragraph → NM · LP · MP · HP · DMG. Store diff: exactly those 3 fields.
- Topup hot-share fix (past items no longer count toward the share), 1 test; queue topped up, check PASS 60%. 92 tests OK.

## 2026-10-19 · Copy hygiene: postage copy (637), bundles retitle/retag (3), SEO titles (300), M7 + OP-18 published (`claude/copy-hygiene-1019-n6reb3`)
- **Status:** built, merged. Report → `REPORT-2026-10-19-copy-hygiene.md`
- Postage: the old "$12.50 / free over $30" was only on the 3 bundles. 612 singles carried "Express Post is $19.50" and offered the letter on $50+ cards; now canon by kind (601 < $50 letter · 11 $50+ / slabs tracked · 25 sealed). Read back 637/637. CSV `data/postage-copy-2026-10-19.csv`.
- Bundles: `mystery-pack` / `hoko-mystery` tags gone, "Mystery Chaos" → "Multi-Game Card Bundle — 20+ Cards", SEO set, still ACTIVE (3/3).
- SEO titles: 300/301 → `<card> <set> <cond> | HOKO` ≤ 60, read back 300/300. 1 left: Mass of Mysteries (card name trips the gate).
- Articles 688483762454 (M7) + 688483795222 (OP-18) published, both 200.
- `bulkOperationRunMutation` is blocked by the connector, so bulk writes go as aliased `productUpdate` calls.
- **Ethan to do:** Mass of Mysteries SEO title; bundle handle still says mystery-chaos (redirect?); multi-game bundle's 3-point condition scale.

## 2026-10-19 · Overnight: listing sweep, SEO fill (6), M7 + OP-18 draft articles, reads (`claude/overnight-1018`)
- **Status:** built, merged. Report → `REPORT-2026-10-19-overnight.md`
- Sweep of 640 ACTIVE products → `data/listing-quality-2026-10-19.csv`: 279 pass all; 301 SEO titles > 60, 89 with < 3 tags, 3 sealed without barcode, 0 missing image/type/collection.
- SEO title on 6 slabs (read back 6/6, nothing else changed); 3 `mystery-pack` bundles skipped. Articles 688483762454 (M7) + 688483795222 (OP-18) are DRAFT.
- Social check PASS 60%, queue to 31 Oct, no topup. 54 open UNFULFILLED orders, all eBay, back to June. 0 abandoned checkouts in 24 h. Discounts match canon. Pre-orders 190/219/165/235.
- **Ethan to do:** publish the 2 drafts (PHONE); rule on the 3 mystery-tagged bundles; eBay order sync (PC).

## 2026-10-18 · Pre-order prices: OP-18 $200 → $219, BF tile, merges (`claude/preorder-prices-1018`)
- **Status:** built, merged (with `claude/phone-ops-1018`). Report → `REPORT-2026-10-18-preorder-prices.md`
- Ethan's call 18 Oct: OP-18 → **$219** (variant 67686723518742, price only; read back 219.00, storefront 21900). M7 $190 / FB12 $165 / EB-05 $235 kept, no write. Brief ticked + "Decided 18 Oct 2026 by Ethan".
- BF page tile OP-18 $200 → $219 (backup `reports/backups/2026-10-18-bf-page-before.json`, storefront tiles read back $330/$235/$219/$190/$165). Captions with OP-18 $200: 0.
- Banned-word gate script excluded itself (it matched its own regex line). 86 tests OK, check PASS 60%.
- **Ethan to do:** PC `run.py source` refreshes `sealed/source.csv` (still 200.0 for OP-18; calendar.md history rows say $200).

## 2026-10-18 · Phone ops: phone-pack 2-day merged in, Discord ready, pre-order pricing brief (`claude/phone-ops-1018`)
- **Status:** built, merged 18 Oct (preorder-prices run). Report → `REPORT-2026-10-18-phone-ops.md`
- `claude/phone-pack-2day` merged into this branch (`--days`, log dedupe, save-line env toggle, `routines/prompts/phone-pack-task.md`); prompt now opens with "Push works only after Ethan adds the repo to the task's sources in claude.ai."
- Discord: poster reads `DISCORD_WEBHOOK_URL` (old `DISCORD_WEBHOOK_PICKUPS` still read); `dry-run` prints the next 3 Discord items (product-drop photos, no clips, no price) or NOT CONFIGURED. README "Discord webhook on phone". 86 tests OK.
- `data/preorder-pricing-2026-10-18.md`: Urara full export, none of M7 / OP-18 / FB12 / EB-05 listed; JP RRP stand-in reads LOW (Urara runs ~2× RRP). Recs: M7 $190 keep · OP-18 $219 (+$19) · FB12 $165 keep · EB-05 $235 keep. No price written.

## 2026-10-17 · Phone pack 2-day + task prompt (`claude/phone-pack-2day`)
- **Status:** built, folded into `claude/phone-ops-1018` (not on main yet). Report → `REPORT-2026-10-17-phone-pack-2day.md`
- `phone-pack --days N` (each day its own heading, log dedupes date+platform+asset) · save line under each heading, env `PHONE_PACK_FILES_FIRST=1` flips it to the Files route · task prompt `routines/prompts/phone-pack-task.md` for `trig_01QeakRTdC9hVqwinFfMP1CB`.

## 2026-10-18 · Close-out: discount canon, `phone-pack`, QUEUE tidy (`claude/hoko-close-out-1018-6c8z6p`)
- **Status:** built, merged. Report → `REPORT-2026-10-18-close-out.md`
- CLAUDE.md free-postage line = the live automatic ("Black Friday: Free AU postage", every AU order, no minimum); `local-setup/CLAUDE.md.template` = copy of CLAUDE.md; email Checks bullet marked done.
- New `python -m tools.social phone-pack [--date]`: today's (Victoria) TikTok + Instagram items as markdown with raw.githubusercontent mp4 URLs, logged to `data/phone-pack-log.csv`. 10 tests, 66 OK. Scheduled task `trig_01QeakRTdC9hVqwinFfMP1CB` (07:10) calls it.
- Repo banned-word gate now a script (`scripts/banned-word-gate.sh`), 0 hits (5 demo/doc lines reworded). check PASS 60%.
- **Ethan to do:** see WAITING ON PC / WAITING ON ETHAN below.

## PHONE (Ethan can do these from the phone)
1. Add repo `ethanryan28-cmd/hoko-collectables` to the phone-pack task's sources (`trig_01QeakRTdC9hVqwinFfMP1CB`, claude.ai).
2. Add the same repo to the cloud-run poster task's sources (`trig_015SKsJWBRCz4Y549d2kHgeL`, claude.ai).
3. Paste `routines/prompts/phone-pack-task.md` (between the `---8<---` lines) into `trig_01QeakRTdC9hVqwinFfMP1CB`.
4. Discord app → Server Settings → Integrations → Webhooks → New Webhook → Copy URL → paste as `DISCORD_WEBHOOK_URL` in the cloud-run task env.
5. Publish the draft theme (Shopify app, Ethan's click).
6. Post the daily pack (07:10 message: save each mp4, paste caption, post).

## WAITING ON PC
- Platform keys (IG/FB, YouTube, Pinterest). Discord moved to PHONE. Chrome task `trig_01Adhr9RC9iZHFwUnMvX7zVj` runs when the PC is on.
- Cloud environment: setup-script line `pip install edge-tts piper-tts` + network allowlist (list in the MANUAL of `REPORT-2026-10-17-bf-media-2.md`).
- `schtasks /Delete /TN "HOKO publish" /F` (PC publisher retired).
- eBay→Shopify fulfilment sync stopped ~10 Oct (#1472+ show UNFULFILLED though shipped) — check eBay channel order-sync. (19 Oct read: 54 open UNFULFILLED eBay orders, incl. 39 from Jun–Aug.)
- Policies (paste blocks, `REPORT-2026-10-17-consolidated.md`) · meta description (Chrome) · BF email.

## WAITING ON ETHAN (not PC)
- ~~3 card bundles tagged `mystery-pack`~~ retitled/retagged 19 Oct; ~~handle + 301, condition scale, Mass of Mysteries SEO~~ done 19 Oct (follow-up).
- eBay relist (reconcile first with `tools/relist-reconcile.py`; never bulk relist).

## DONE 17 Oct (struck in the entries below)
- ~~BF free-postage automatic~~ → "Black Friday: Free AU postage", every AU order, no minimum · ~~M6a ACTIVE~~ · ~~We Buy Cards menu item~~ · ~~`run.py cutoff --apply`~~ · ~~$5 BF code~~ = `BFDROP5` · ~~cloud-run poster scheduled task~~ `trig_015SKsJWBRCz4Y549d2kHgeL` (4×/day) · ~~test orders #1058 / #1434~~ archived · ~~phone-pack scheduled task~~ `trig_01QeakRTdC9hVqwinFfMP1CB` (07:10)

## 2026-10-18 · No price frames: strip prices from frame + voice, re-render 75, captions/ rebuilt, PC publisher retired (`claude/no-price-frames`)
- **Status:** built, merged. Report → `REPORT-2026-10-18-no-price-frames.md`
- `reel.py`: hooks, voiceover, pre-order card, gold price slot (now `SEALED · JAPANESE` / grader+grade), roundup labels (set code) and postage strip carry no figure. `calendar_gen.py`: roundup/beat captions de-priced, `under-200` roundup retitled, buyback tip drops `$100+`. 2 new tests, 56 OK.
- 75/75 clips re-rendered in William (incl. 4 drafted-product clips that only had sidecars), 93.8 MB, 0 `$` in sidecars, 36 clips frame-checked. captions/ rebuilt: only `$5 off boxes` left (15 files, ruling 4). check PASS 60%, dry-run 0 invalid / 0 missing.
- `run.py publish` / `hoko-publish.cmd` / "HOKO publish" marked RETIRED in both READMEs; `publish.run()` prints a retired line.
- **Ethan to do:** PC `schtasks /Delete /TN "HOKO publish" /F`; ~~BF automatic edit~~ (done 17 Oct); platform keys; env setup + allowlist; optional: BF beat on-screen `$5 off`.

## 2026-10-17 · BF media tidy: run-2 fold-in, cloud docs, caption prices out (`claude/bf-media-tidy-1017-1tsocy`)
- **Status:** built, merged. Report → `REPORT-2026-10-17-bf-media-tidy.md`
- Merged `claude/bf-media-render-queue-376p0p` (report + QUEUE only). `cloud_run.py` docstring + dry-run log line now describe the tts.py proxy-CA path (no logic change).
- `reel.caption_text`: price + postage figure out (incl. priced hooks). 61 `reels/**/*.caption.txt` rewritten without rendering, 0 with `$N`, backup in `reports/backups/2026-10-17-bf-media-tidy-captions/`. Nothing reads those files. 0 mp4/json touched. 54 tests OK, check PASS 60%, dry-run 0 invalid / 0 missing.
- `due_unconfigured` 29 on FB/YT = native 14-day scheduling, not a bug.
- Pre-order clips show the price on screen (`preorder_body`), left for Ethan. `captions/<date>.txt` (read by PC `run.py publish`) still carry prices, needing a no-render calendar rebuild.
- **Ethan to do:** on-screen price ruling; captions/ rebuild yes/no; ~~BF automatic edit~~ (done 17 Oct); platform keys; env setup + allowlist.

## 2026-10-17 · Social poster cloud-run 20:13 (`claude/social-cloud-2026-10-17-2012`)
- **Status:** ran, merged. Report → `reports/social/REPORT-2026-10-17T2013+1100.md`
- All 8 platforms NOT CONFIGURED (no env keys in the cloud environment). 0 posted, 0 FAIL, 3 SKIP (stale 11:00 / 12:15 slots). Queue 15 days/platform, 0 invalid, 0 clips missing. PyPI still unreachable (edge-tts / piper-tts not installable) — no render was needed.
- **Ethan to do:** set the platform env vars; add `edge-tts piper-tts` to the environment setup script.

## 2026-10-17 · BF media 2, run 2: resume check — already merged, verified (`claude/bf-media-render-queue-376p0p`)
- **Status:** verified, nothing redone. Report → `REPORT-2026-10-17-bf-media-2.md` (## Run 2)
- main `e967b58`, 71 mp4s / 86.5 MB on origin/main, 54 tests OK.

## 2026-10-17 · BF media 2: live William gate, 71 clips rendered + committed, merged (`claude/bf-media-1017`)
- **Status:** built, merged. Reports → `REPORT-2026-10-17-bf-media.md` (tts fix, stopped at gate) + `REPORT-2026-10-17-bf-media-2.md` (this run)
- Network open this session (PyPI 200, Bing reachable). The branch's `tts.py` proxy-CA fix rendered live (`edge-tts:en-AU-WilliamMultilingualNeural`, verification on, no sitecustomize). 54 tests OK.
- 71/71 mp4s rendered in William (45 sealed incl. EB-05/M7/FB12 h3 forced, 12 slab, 4 tips, 4 roundups, 6 BF beats). ffprobe PASS 1080×1920, audio, 8–20 s, no "$" spoken. **86.5 MB committed**, mp4s now in git. 30 sidecars piper → William.
- Queue: check PASS 60% hot everywhere, dry-run 0 invalid / **0 missing media** (was 30), all platforms NOT CONFIGURED.
- **Ethan to do:** ~~BF free-shipping automatic edit~~ (done 17 Oct); platform keys; env setup line + network allowlist (in the report MANUAL).

## 2026-10-17 · BF media: tts.py proxy-CA fix, un-ignore reels mp4s, re-render + keep (`claude/bf-media-1017`)
- **Status:** built, **NOT merged** — stopped at the Step 1 live-render gate. Report → `REPORT-2026-10-17-bf-media.md`
- Cloud run with every render host policy-denied (403 at the proxy): PyPI, `speech.platform.bing.com`, `huggingface.co`. No edge-tts / piper / faster-whisper installable, so **0 clips rendered, 0 MB committed**; the 38 bf-render mp4s are still gone.
- Done + tested: `content/youtube/hoko/tts.py` trusts `SSL_CERT_FILE` / `REQUESTS_CA_BUNDLE` / `/root/.ccr/ca-bundle.crt` via a verifying `ssl.create_default_context(cafile=…)` handed to edge-tts' connector **and** its per-request context (edge-tts 7.x overrides the connector), `proxy=$HTTPS_PROXY`; no env var → unchanged PC path. 7 new unit tests, 54 OK. `content/youtube/.gitignore` now keeps `reels/**/*.mp4` (out/, wav, cache, inbox still ignored). README Cloud line added.
- Queue: check PASS 15 days / 60% hot on all 6, 0 invalid, **missing media 30** (the unrendered clips), all platforms NOT CONFIGURED.
- **Ethan to do:** merge the branch or re-run with network (prompt line in the report MANUAL); PC render + push the mp4s meanwhile; ~~BF automatic edit~~ (done 17 Oct) + platform keys still pending.

## 2026-10-17 · BF render: 38 clips in en-AU, queue check, BF automatic re-read (`claude/bf-render-1017-idka4q`)
- **Status:** built, merged. Report → `REPORT-2026-10-17-bf-render.md`
- Cloud run, PyPI reachable this time: edge-tts William worked through the proxy CA (session-only sitecustomize, no repo code change). 38/38 clips rendered + ffprobe PASS (1080×1920, audio, 8–20 s, no "$" spoken): EB-05/M7/FB12 h3 (`stale_render` cleared), the 27 the queue listed missing, 6 BF beats (text unchanged, none said $100). mp4s are gitignored, so only sidecars are committed.
- Queue: topup kept all 165 items, check PASS, 60% hot on every platform, 0 invalid, 0 missing media, all platforms NOT CONFIGURED; 47 tests OK. `source.csv` not refreshed (no token): committed rows already right.
- BF free-shipping automatic read live: still "$100+, all products, AU". CLAUDE.md line now says so explicitly.
- **Ethan to do:** ~~change that automatic to Japanese Sealed / no minimum~~ (done 17 Oct: every AU order, no minimum); PC: `run.py source` + `tools.social render` (mp4s are local-only); decide on the 3-line `tts.py` proxy fix.

## 2026-10-17 · BF lock-in: M7 + FB12 live, newest-set links, BF page/collection, social queue 60% newest (`claude/bf-lockin-1017`)
- **Status:** built, merged. Report → `REPORT-2026-10-17-bf-lockin.md`
- M7 + FB12 ACTIVE, CONTINUE, 7/7 channels. FB12 = Bandai JP pack art; **M7 = HOKO placeholder card (no publisher art exists yet)** — swap when pokemon-card.com publishes. 24/24 ACTIVE jp-sealed on all 7 channels.
- M6a + EB-05 guides link the other four newest; 2026 guide has a "Newest releases" list; 0 dead links across 41 articles. BF page = 5 newest tiles + collection link, no postage figure; `japan-direct-sealed` sorted M6a, EB-05, OP-18, M7, FB12 first.
- Social: `hot_sets` = the 5, builder pushes them to ≥60% (2-day hot repeat), BF-week block 20–30 Nov built in (BFDROP5 + box drop list, product/collection links only), check PASS, 47 tests. All platforms NOT CONFIGURED. CLAUDE.md: newest-sets rule + prices-are-Ethan's line.
- 07:27 Ethan ruled: free postage on ALL sealed, no minimum; M7 stays live with the placeholder. Page/email/captions reworded (`claude/bf-postage-1017`).
- **Ethan to do:** ~~edit the scheduled BF free-shipping automatic (all orders $100+ → Japanese Sealed collection, no minimum)~~ (done 17 Oct: every AU order, no minimum); social keys + piper in the env setup; PC re-render of EB-05/M7/FB12 h3 clips.

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
- **Ethan to do:** ~~flip M6a to ACTIVE if wanted~~ (ACTIVE); merge the duplicate OP-17 listings; confirm EB-05 price when Urara lists it.

## 2026-10-17 · Consolidated run: JP sealed routing, social cloud-run, store hygiene (`claude/consolidated-1017`)
- **Status:** built. Report → `REPORT-2026-10-17-consolidated.md`
- Routing: M5 sealed + OP-16 back ACTIVE (CONTINUE), 15 boxes tagged `route:kanade-single` / `route:urara-batch` + metafield `hoko.supplier`, 3 raise-to-floor prices, `japan-direct-sealed` re-sorted, BF page tiles, `data/routing-2026-10-17.csv`, `hot_sets` updated. eBay sold-count trim NOT CHECKED (eBay 403 from the cloud) — no in-stock box drafted.
- Social: `python -m tools.social cloud-run` + `env`, README Cloud section, 43 tests, queue topped to 15 days/platform; run log + CSV now committed.
- Hygiene: policy diffs + paste blocks (connector lacks `write_legal_policies`), discount-eligible clean, 0 customer orders stuck, abandoned checkouts read.
- **Ethan to do:** see MANUAL in the report (env vars + ~~trigger~~ (cloud-run trigger `trig_015SKsJWBRCz4Y549d2kHgeL`, 4×/day), ~~test orders #1058/#1434~~ (archived), paste policies, eBay trim, M6a/OP-17 pricing)

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
  2. ~~`python content/youtube/run.py cutoff` → check the example → `--apply` (Shopify write was blocked in the cloud run)~~ (done)
  3. `python content/youtube/run.py schedule` on the PC (registers "HOKO publish", 6:30pm daily)
  4. `python content/youtube/run.py reel sealed all --force` + `reel slab all --force` on the PC to re-voice reels in en-AU (cloud run used a fallback voice)
  5. ~~Create the $5-off BF box code in Shopify (not created — by design)~~ (done: `BFDROP5`)
