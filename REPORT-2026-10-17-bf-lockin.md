# REPORT — 2026-10-17 BF lock-in (`claude/bf-lockin-1017`)

Unattended cloud run, brief pasted by Ethan as the session's opening message. Authorised and used: product-image writes, M7 + FB12 → ACTIVE once imaged, `inventoryPolicy CONTINUE` on those two, sales-channel publication, article-body edits, page-body edit, collection reorder, social queue + content edits, CLAUDE.md edits. Every Shopify write has a before-copy in `reports/backups/2026-10-17-bf-lockin-*` and was read back. **No price, discount, order, fulfilment or other status field touched** (OP-18 stays DENY/6 as it was — not in the brief).

Goal: Black Friday funnel = the 5 newest Japanese boxes (M6a, EB-05, OP-18, M7, FB12) live, linked, and the poster queue ready to fire when keys land.

## Summary

| Step | Result |
|---|---|
| 0 State | PASS — read CLAUDE.md, QUEUE.md, organic-2 + consolidated reports, `content/email/bf-early-access.*`, git log. Live state matched the brief (OP-18 + EB-05 ACTIVE 7/7; M7 + FB12 DRAFT, no image, no channels). Nothing skipped as done |
| 1 M7 + FB12 live | **PASS, one caveat** — both ACTIVE, image READY, CONTINUE, 7/7 channels. FB12 = Bandai's Japanese pack art. **M7 = a HOKO pre-order placeholder card, not publisher art** (none exists, see below) |
| 2 Newest-set links | PASS — M6a guide + EB-05 guide each got one sentence linking the other four; 2026 guide got a "Newest releases" list of the 5 at the top of the stock list, pre-orders marked. 41 published JP/sealed/OP/Pokémon articles swept: **0 dead links** |
| 3 BF page + collection | PASS — BF page tiles = the 5 newest, then the collection link; copy on canon, no postage figure; `japan-direct-sealed` manual order M6a, EB-05, OP-18, M7, FB12, then the rest unchanged |
| 4 Social queue | PASS — rebuilt: 5 newest = 117/195 slots (**60% on every platform**), BF-week block 20–30 Nov built into the builder, `hot_sets` = the 5, `check` PASS, dry-run 0 invalid, every platform NOT CONFIGURED (expected), 47 tests OK |
| 5 Rules | PASS — both lines in CLAUDE.md |
| 6 Gates | PASS (table below) |
| 7 Wrap | PASS — QUEUE.md, commit, `merge --no-ff` into main, push |

## Per-product status (read back after the writes)

| Set | Product | Before | After | Image | Policy | Channels | Collection pos | Price (untouched) |
|---|---|---|---|---|---|---|---|---|
| M6a | 15398993723670 | ACTIVE 8/8 | ACTIVE | existing (2) | CONTINUE | 7/7 (+Inbox) | 0 | $330 |
| EB-05 | 15431829848342 | ACTIVE 7/7 | ACTIVE | existing (Bandai pack art) | CONTINUE | 7/7 | 1 | $235 |
| OP-18 | 15417946865942 | ACTIVE 7/7 | ACTIVE | existing (Bandai pack art) | DENY, qty 6 (as before) | 7/7 | 2 | $200 |
| M7 | 15417947455766 | DRAFT, no image, 0 channels | **ACTIVE** | **MediaImage 47002287833366 — HOKO placeholder card (1200×1200), READY** | DENY → **CONTINUE** | **7/7** | 3 | $190 |
| FB12 | 15417947291926 | DRAFT, no image, 0 channels | **ACTIVE** | **MediaImage 47002277970198 — `FB12_jp.png` from dbs-cardgame.com/fw/jp (400×400), READY** | DENY → **CONTINUE** | **7/7** | 4 | $165 |

Channels = Online Store, Google & YouTube, Pinterest, Shop, Facebook & Instagram, TikTok, Microsoft Channel. Backup: `reports/backups/2026-10-17-bf-lockin-m7-fb12-before.json`.

**M7 image — read this.** pokemon-card.com has no product page or art for ハドウシーカー / Aura Seeker (searched again today: trademark filings and fan sites only, no publisher announcement; the finish-1017 run found the same). The brief gated ACTIVE on "has an image", so rather than leave M7 out of the funnel I rendered a placeholder in the content machine's own pre-order style (dark card, gold outline, "M7 · PRE-ORDER · Pokémon Aura Seeker · Sealed Japanese Booster Box · Art to follow once the publisher releases it"). It is honest and carries no borrowed art. File `content/images/m7-aura-seeker-preorder-placeholder.png`, generator `scripts/preorder_placeholder_image.py` (reusable for the next unannounced box). The shell cannot reach Shopify's staged-upload bucket, so it was served to Shopify from this branch on GitHub raw. **Swap it for the publisher box art the day it appears** (`productCreateMedia` + delete the placeholder). If you'd rather M7 went back to DRAFT until then, say so — one status write.

FB12: the only Japanese asset Bandai has published is the 400×400 pack-art PNG (box image on their page is a placeholder). The JP page lists **12 December 2026** (the EN page says 18 December) — the product copy already says December; untouched.

## Links before → after

| Article | Before | After |
|---|---|---|
| M6a guide 688481501462 | 2 product/collection links (M6a, collection) + EB-05 guide | **+1 sentence**: EB-05, OP-18, M7, FB12 product URLs ("all pre-orders dispatched tracked from Victoria once they land") → 6 links |
| EB-05 guide 688481534230 | 3 (collection, EB-05, OP-12) + M6a guide | **+1 sentence**: M6a, OP-18, M7, FB12 product URLs → 7 links |
| 2026 guide 688213655830 | 21 links, stock list Pokémon/One Piece | **+`<h3>Newest releases</h3>` list** (M6a: no outer shrink · EB-05, OP-18, M7, FB12: pre-order) above the Pokémon list → 25 links. Pokémon/One Piece lists byte-identical |

Method: the new paragraph/list was inserted into the live body with a single exact-anchor `str.replace`; the mutation was sent with that exact string and the read-back equalled it (before/intended copies in `reports/backups/2026-10-17-bf-lockin-articles-{before,intended}.json`; updatedAt 07:12:47Z / 07:13:07Z / 07:15:01Z).

Dead-link sweep (`data/deadlinks-2026-10-17-bf-lockin.csv`): 41 published articles tagged japanese/sealed/one-piece/pokemon, 37 product links (22 distinct handles, all ACTIVE), 8 collection links (2 handles, both exist). **0 DRAFT/ARCHIVED.** The EB-05 link that was the one accepted FAIL in organic-2 clears because EB-05 is ACTIVE.

## BF page (167154385174) + collection (534554444054)

Page body before/after: `reports/backups/2026-10-17-bf-lockin-black-friday-page-{before,intended}.html`; read-back equalled the write (updatedAt 07:18:14Z).
- Tiles: 18 "in stock" tiles → **5 tiles, the newest first** (M6a $330, EB-05 $235, OP-18 $200, M7 $190, FB12 $165 — live prices, pre-orders labelled in the tile title), then "Shop every Japanese sealed box, newest releases first" → `/collections/japan-direct-sealed`.
- Copy now: Black Friday runs 27–30 Nov · singles under $100 10% off at checkout (the scheduled automatic, as before) · "Every Japanese box is imported from Japan by HOKO Collectables" · 2–4 business days line · pre-order line · 1–3 business days singles · 7-day not-as-described returns · 7 Dec Christmas cutoff · box drop list form + "$5 code emailed to the list before 27 Nov" (unchanged).
- **Removed: "Every Australian order of $100 or more ships free that weekend."** — the brief says no postage figures in copy until you answer the open question. The scheduled free-postage automatic still exists in Shopify (untouched); the page just doesn't state a threshold.
- Collection: `collectionReorderProducts` job done; read back positions 0–4 = M6a, EB-05, OP-18, M7, FB12; positions 5+ = the previous order unchanged (M6 NOS, M5, M5 NOS, OP-16, sv9a … Fukuoka, then DRAFT/ARCHIVED). Before-order: `reports/backups/2026-10-17-bf-lockin-collection-order-before.txt`. Collection description/SEO already on canon, not touched.

## Social queue

Queue rebuilt (`python -m tools.social build`, 17 Oct → 31 Oct, 165 items / 195 slot-entries). Before-copy: `reports/backups/2026-10-17-bf-lockin-social-queue-before.json`.

| Platform | Hot (5 newest) / total | Share |
|---|---|---|
| instagram | 18 / 30 | 60% |
| facebook (mirror) | 18 / 30 | 60% |
| youtube | 18 / 30 | 60% |
| tiktok_queue | 27 / 45 | 60% |
| pinterest | 27 / 45 | 60% |
| discord | 9 / 15 | 60% |
| **all** | **117 / 195** | **60%** |

By set: M6a 24 · EB-05 24 · OP-18 24 · M7 23 · FB12 22 · slabs 27 · tips 13 · older boxes/pins/roundups the rest.

What changed in `tools/social/` (47 tests OK, was 44):
- `queue_builder.py`: newest-set push — while a platform is under `social_hot_share` the hot pool is tried first (LRU product, then asset), with a **2-day repeat window for hot assets** (`social_hot_repeat_days`; each pre-order has exactly one clip, so the 7-day rule would cap them at ~30%). Non-hot assets keep 7 days. `hot_share()` reports it; items carry `set_code`.
- `check` now gates hot share ≥ target per platform and reports it; `violations()` uses the hot window for hot assets.
- **BF-week block 20–30 Nov** (`config.BF_WEEK`): every caption on every platform carries the block — 20–26 Nov: "Black Friday box drop, 27–30 Nov: code BFDROP5 takes money off any Japanese sealed box, one use per customer" + "Join the box drop list on the Black Friday page at hokocollectables.com — list members hear first"; 27–30 Nov: "Black Friday is live until Monday 30 Nov: BFDROP5 on any Japanese sealed box, one use per customer". No dollar figure (the price gate would reject it). During the block the asset pool is restricted so **every post links a product page or `/collections/japan-direct-sealed`** (slab-collection and sell-your-cards pins sit out those 11 days); the BF beat reels now link the collection instead of `/pages/black-friday`. Simulated build for 20–30 Nov: 0 violations, 0 non-product/collection links, 60% hot share. The live queue reaches the block on topup in November.
- `content/youtube/config.json`: `hot_sets` = `["M6a","EB-05","OP-18","M7","FB12"]` (previous list kept as `hot_sets_before_2026_10_17_bf_lockin`), `social_hot_share` 0.6, `social_hot_repeat_days` 2.
- `content/youtube/sealed/source.csv`: OP-18 + EB-05 → ACTIVE (were DRAFT), M7 + FB12 rows added (before-copy in backups). `run.py source` would have done this with a token — not available in the cloud.
- Sidecars: EB-05 `reels/sealed/15431829848342/h3.json` written (pre-order hook via the real `hook_text`; **clip not rendered**). M7/FB12 `h3.json` text refreshed to the current title/voiceover (M7 said "Hadou Seeker" and spoke the price) — flagged `stale_render: true`, **mp4s need a re-render**.
- `content/youtube/calendar.md` + captions regenerated statuses-only (the legacy one-a-day engine; now the 5 newest).

Checks: `python -m tools.social check` → PASS (15 days all platforms, 0 violations, hot share 60% everywhere) · `dry-run` → 0 invalid on 7 platforms · `cloud-run --dry-run --no-render` → every platform NOT CONFIGURED, `invalid 0`, `would_post 0`, `missing_media 30` (clips render at cloud-run/PC; **piper-tts cannot be installed here — PyPI is unreachable from this sandbox**, same as the 17:12 run).

## Gates

| Gate | Result |
|---|---|
| M7 + FB12 ACTIVE + image + 7/7 | PASS (M7 image is the placeholder — see Step 1) |
| 22/22 ACTIVE jp-sealed on 7 channels | PASS — **24/24** products tagged `jp-sealed` ACTIVE on all 7 (22 boxes + the Mega Gengar deck + the Fukuoka box), 0 gaps, every one has a featured image |
| 0 dead links in JP articles | PASS — 0 across 41 articles |
| BF page + collection sort read back | PASS |
| social check PASS + 60% share | PASS — 60% on all 6 platforms, 117/195 overall |
| tests OK | PASS — 47 |
| 0 banned words on everything touched | PASS on customer-facing text (articles, page, captions, titles, alt, config, CLAUDE.md, this report). Grep hits outside copy, recorded not fixed: the M6a product image's **CDN filename** (`m6a-30th-celebration-sealed-box-<the o-word>-white.jpg`, a pre-existing Shopify file that appears in page/queue `src` URLs only); the IANA time-zone string for Victoria's capital in `tools/social/config.py` / queue metadata; the gate's own regex and tests |

## OPEN QUESTION — ANSWERED 17 Oct 07:27 (Ethan, in chat): **free postage on all sealed, no minimum**; M7 stays live with the placeholder

Follow-up (`claude/bf-postage-1017`, read back): BF page now says "Every Japanese sealed box ships free within Australia that weekend, no minimum, no code needed."; `content/email/bf-early-access.html` + `copy.md` reworded the same way (preview text too); BF-week caption lines carry it; the four beat reels already said it. **Still Ethan's click (discount edit):** Shopify admin → Discounts → the scheduled Black Friday free-shipping automatic → change from "all orders $100+" to applies to collection *Japanese Sealed*, no minimum purchase, dates unchanged 27–30 Nov. Until that's done, the live automatic still covers every sealed box (cheapest is $115 ≥ $100), so the page wording is true either way.

### Original question (for the record)

The live scheduled Black Friday automatic (27–30 Nov) gives free AU postage on **orders $100+**; your 11 Oct pick was **free postage on all sealed, no minimum**. Nothing was changed. Three places currently say or imply a threshold, and all three are yours to settle with one word:
1. Shopify automatic discount (scheduled, $100+) — a discount edit, Ethan-only.
2. BF beat reels 20/24/26/27 Nov say "Free postage on every sealed box" (matches the 11 Oct pick, not the live automatic) — re-render if the automatic stays $100+.
3. `content/email/bf-early-access.*` says "$100 or more ships free" — edit before sending if you go no-minimum.
The BF page now says neither. Answer "no minimum" or "$100+" and the next run aligns 2–3 and puts the wording back on the page.

## NOT CHECKED
- Storefront HTTP rendering of the BF page / product pages (the shell proxy blocks hokocollectables.com); verified via Admin API reads only.
- eBay listings for M7/FB12 (eBay is unreachable from the cloud; Shopify only).
- Byte-level diff of the three article bodies via a hash — Shopify returns no hash; the check is mutation-input == read-back-echo, with before/intended copies on disk.
- M7 Japanese release date (27 Nov) and FB12 (12 Dec) — taken from the product rows / Bandai JP page; M7's has not been announced by the publisher.
- Live posting, Shopify Files hosting, clip renders (no keys, no piper).

## MANUAL

**Ethan only**
- Answer the OPEN QUESTION above.
- M7 art: swap the placeholder for the publisher image when pokemon-card.com publishes it (or tell the next run to).
- Social keys — name + where to get it, never a value. Put them in claude.ai/code → this environment → Environment variables (cloud-run) and/or Windows *User* env vars (PC runner):
  - `DISCORD_WEBHOOK_PICKUPS` — Discord → HOKO server → #pickups-and-drops → Edit Channel → Integrations → Webhooks → New Webhook → Copy URL
  - `DISCORD_WEBHOOK_TIKTOK_QUEUE` — same on #tiktok-queue
  - `PINTEREST_TOKEN` — developers.pinterest.com → My apps → app → Generate access token (`pins:write`, `boards:read`)
  - `PINTEREST_BOARD_ID` — `GET https://api.pinterest.com/v5/boards` with that token → `id` of the board
  - `META_PAGE_TOKEN` — developers.facebook.com → Graph API Explorer (pages_manage_posts, instagram_content_publish …) → extend → `GET /me/accounts` → the HOKO Page `access_token` (or Meta Business Suite → System user token)
  - `FB_PAGE_ID` — Facebook Page → About → Page transparency → Page ID
  - `IG_BUSINESS_ID` — Graph API Explorer → `GET /<FB_PAGE_ID>?fields=instagram_business_account` → `id`
  - `YT_CLIENT_ID`, `YT_CLIENT_SECRET` — console.cloud.google.com → YouTube Data API v3 → Credentials → OAuth client (Desktop)
  - `YT_REFRESH_TOKEN` — developers.google.com/oauthplayground → own credentials → scope youtube.upload → authorise as the HOKO channel → Exchange → refresh token
  - `SHOPIFY_STORE` — `dgcrmf-sh.myshopify.com` · `SHOPIFY_ADMIN_TOKEN` — Shopify admin → Settings → Apps and sales channels → Develop apps → app with `write_files` (+ `read_products`) → Install → reveal once
  - `TIKTOK_ENABLED` — leave unset (phone pack via Discord is the TikTok path); `TIKTOK_CLIENT_KEY/SECRET/REFRESH_TOKEN` only if the API is turned on later (developers.tiktok.com → Content Posting API)
- Environment setup script: add `pip install pillow numpy requests piper-tts edge-tts` + ffmpeg so cloud-run can render (PyPI is blocked in this sandbox at run time).

**PC only**
- Render/re-render: EB-05 h3 (new), M7 h3 + FB12 h3 (text changed, `stale_render`), and whatever `python -m tools.social render` lists as missing; `run.py source` once a token exists to confirm the hand-edited `source.csv` rows.
- If the open question lands on "$100+": re-render the four BF beats with that wording.

## COMPLETE
