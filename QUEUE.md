# QUEUE

Work queue for Claude Code runs. Newest first. Each entry: date · what · status · where the report is.

## 2026-10-13 · HOKO content machine (`content/youtube/`)
- **Status:** built. Report → `content/youtube/REPORT.md`
- Reel engine, Shorts cutter + packager, 14 Oct → 24 Dec calendar, IG/YT auto-publish, comment queue
- **Ethan to do (MANUAL):**
  1. Fill `content/youtube/.env` from `.env.example` (IG, YT OAuth, Shopify Admin token)
  2. `python content/youtube/run.py cutoff` → check the example → `--apply` (Shopify write was blocked in the cloud run)
  3. `python content/youtube/run.py schedule` on the PC (registers "HOKO publish", 6:30pm daily)
  4. `python content/youtube/run.py reel sealed all --force` + `reel slab all --force` on the PC to re-voice reels in en-AU (cloud run used a fallback voice)
  5. Create the $5-off BF box code in Shopify (not created — by design)
