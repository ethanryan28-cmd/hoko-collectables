# HOKO content machine — run report (13 Oct 2026)

| Step | Result | Notes |
|---|---|---|
| 0 State check | **PASS** | sealed/source.csv 32 rows, slabs/source.csv 6 rows, every row ≥1 image. All tools import. |
| 1 Reel engine | **PASS** | 67 product reels (55 sealed, 12 slab) + 6 beat + 4 tip reels = 77; all 1080x1920, 8–12s, with audio |
| 2 Shorts + package | **PASS** | 90s testsrc + spoken track → 1 short (1080x1920, 36.1s, audio), 3 titles, 3 thumbs 1280x720. Test outputs deleted |
| 3 Calendar | **PASS** | 72 rows (14 Oct → 24 Dec, one a day), 0 missing reels, 0 missing captions. One Tip reel a week; hot sets take 3 of 4 sealed slots |
| 4 Auto-publish | **PASS (dry-run)** · scheduler **NOT CHECKED** | Mocked IG + Shopify Files + YT run changed `queued` → `posted-dryrun`; queue.md produced. The Windows task can't exist in a Linux cloud container. Run `run.py schedule` on the PC |
| 5 Shopify wiring | **BLOCKED → MANUAL** | Shopify writes were denied by this session's permission guard. Nothing on the live store was changed. Ready to run: `run.py cutoff` (dry run) then `--apply` |
| 6 Wire-up | **PASS** | .env.example, .gitignore, README.md, QUEUE.md, commit "hoko content machine" |

## SKIPPED (already built)
Nothing. There was no QUEUE.md, no `content/youtube/`, and no earlier REPORT.md. Not rebuilt: the existing Shopify "Black Friday" page with its box-drop signup form (created 12 Oct) is reused as the BF list URL instead of creating a duplicate.

## Counts
- Reels: **77** (sealed 55 · slab 12 · BF/Christmas beats 6 · tips 4). 19 promotable sealed boxes (13 skipped as `OOS-SUPPLIER`) × 2–3 true hooks; 6 slabs × 2 hooks.
- Calendar rows: **72** — 9 Tip, 6 pinned beats, the rest 2 sealed : 1 slab. Hot sets (`hot_sets` in config.json) take 3 of every 4 sealed slots; older sets get 1–2 posts each.
- Source CSVs: sealed 32 (all live Japanese sealed) · slabs 6 (PSA/BGS — no CGC/TAG in stock). One title match, "Paladin Elizabeth Taggerdy", is an MTG single and was excluded.

## LEAD TIME + CUTOFF
- **Lead time: 21 days.** The default was used because the 6 Oct dropship supply-model doc wasn't found in the repo, Google Drive or Notion (**NOT CHECKED**). The collection copy says "Allow 2–3 weeks", which is consistent with this.
- **AusPost** Parcel Post send-by from VIC metro: NSW/ACT/QLD/SA/TAS Mon 21 Dec, VIC Tue 22 Dec, WA Fri 18 Dec, NT Wed 16 Dec. Source: https://auspost.com.au/sending/christmas-sending-dates (fetched 13 Oct).
- **Cutoff: Monday 30 November 2026** = 21 Dec − 21 days. It is conservative because it assumes the full lead time is used before lodgement. WA is 27 Nov and NT is 25 Nov (see CUTOFF.md).
- Christmas-cutoff reel is pinned to 23 Nov (cutoff − 7). It is also in CUTOFF.md and config.json.
- ⚠ **Conflict:** sealed product descriptions and the Shipping page say "dispatched tracked from Victoria within 2–4 business days", but the collection says "Allow 2–3 weeks". If boxes are actually on hand, the real cutoff is about 18–21 Dec. Change `christmas_cutoff` in config.json and re-run `calendar`.

## FORMULA
**DEFAULTS.** `content/youtube/retrospecs-breakdown.md` doesn't exist. Reels use the hook in the first ~48%, then price + postage, then a 2s end card, with an 8–12s total.

## Live URLs
- Buy prices: https://www.hokocollectables.com/pages/buy-prices (200 ✓)
- Sell your cards: https://www.hokocollectables.com/pages/sell-your-cards (200 ✓)
- BF list: https://www.hokocollectables.com/pages/black-friday#bf-early-access (200 ✓, form present). This is the real URL in every November caption, not `{{BF_LIST_URL}}`.

## NOT CHECKED
- Live IG / YouTube posting. No keys were available; only mocked responses were exercised.
- Live comment pull/post (mocked only).
- Windows Task Scheduler job "HOKO publish". Not possible on Linux.
- Shopify Files video upload against the real API (mocked).
- 21-day lead time (source doc missing).
- en-AU voice. edge-tts is blocked in this sandbox (its WebSocket returns 403 at the proxy), so all 73 reels use the Piper fallback voice (`en_GB-alan`). Each reel's `.json` records this.
- Slab photos come from Shopify. The 3 `s1600` files are eBay-origin. There's no eBay integration in this repo. Front-facing shots were picked by eye; card-back photos are excluded via `reel_images`.

## MANUAL (Ethan)
1. **Shopify cutoff line (blocked here):** `python content/youtube/run.py cutoff` shows one example. Then `--apply` updates 32 sealed products + the "Japanese Sealed — Newest Releases" collection (backup written first; `--remove` after Christmas). A pre-run backup is in `shopify-backup/`.
2. **$5 BF box code.** Create it in Shopify. Not created, as instructed. The BF page already promises it ("emailed to the list before 27 November").
3. `.env` from `.env.example`, then `run.py schedule` on the PC. The first YT run opens a browser once for OAuth.
4. Re-voice in en-AU on the PC: `run.py reel sealed all --force` and `run.py reel slab all --force`, then `run.py calendar`. Alternatively, just let `publish` render as it goes; mp4s are gitignored.
5. **BF shipping wording.** The brief said "free AU post on all sealed 27–30 Nov". The live BF page says "every Australian order of $100 or more ships free". The cheapest sealed item (Mega Gengar deck, $70) is under $100, so copy says "every sealed box" (all boxes are $115+). Align the page or the copy.
6. **Pre-orders** (OP-18, FB12, M7) are DRAFT with no images, so they're not in the CSV or the calendar. Publish them with photos, then `run.py source` + `calendar`.
7. **Scarcity hook** ("This box is about to be gone · only N left") is used only where Shopify inventory is 1–2. Check those counts are real stock, not a drop-ship placeholder, before posting.

## Paths
- Engine: `content/youtube/run.py`, `content/youtube/hoko/*.py`
- Reels: `content/youtube/reels/{sealed,slab}/<product_id>/h<k>.mp4` (+ `.caption.txt`, `.json`), `reels/beats/<date>.mp4`
- Calendar: `content/youtube/calendar.md`, dated captions `content/youtube/captions/YYYY-MM-DD.txt`, `CUTOFF.md`, `config.json`
- Publish: `hoko/publish.py`, `hoko-publish.cmd`, `TODAY.md` (written per run), `publish.log`
- Comments: `comments/queue.md` (created on first `run.py comments`)

## Second pass (same day) — content review
Looked at the reels as a viewer, not a gate. Changed:
- Dropped the bait hook "What you can pull from X" (showed a box, never a pull) → "[Set] — sealed Japanese box, in Victoria now / imported to order".
- Dropped "Still $X on HOKO" (reads as unsold) → "Would you pay $X for [set]?" (invites comments).
- BF / Christmas beat reels now carry their own on-screen lines ($5 off · join at link in bio · dates) instead of a price block.
- Added 4 Tip reels (spot a fake JP box · no outer shrink · why PSA/BGS/CGC only · how we buy collections), copy lifted from your live product descriptions. One runs every 7th day.
- December captions no longer say "lands after Christmas"; they point sealed to early-Jan and slabs to under-the-tree.
Still thin: it's product photos only. A 30s phone clip of a pack rip or a packing table would lift every reel. Drop clips in `inbox/` and `run.py shorts` cuts them.

## COMPLETE
