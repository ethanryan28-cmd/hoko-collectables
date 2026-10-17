# QUEUE

Work queue for Claude Code runs. Newest first. Each entry: date · what · status · where the report is.

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
