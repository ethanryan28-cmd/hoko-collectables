# QUEUE

Work queue for Claude Code runs. Newest first. Each entry: date · what · status · where the report is.

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
