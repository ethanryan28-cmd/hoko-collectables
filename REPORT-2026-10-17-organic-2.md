# REPORT — 2026-10-17 organic-2, run 2 (`claude/organic-2-1017-9a79lu`)

Unattended cloud run, brief pasted by Ethan. Authorised: article-body, barcode, SEO and sales-channel-publication writes, with backup and byte-exact read-back. No price, status, discount, inventory, order or fulfilment field touched. eBay step: read and compute only.

Goal: every link on the Japanese-sealed content path resolves to a buyable box; the social poster is ready to fire when its keys land; Ethan gets the eBay price table to reprice the boxes with one word.

**Shopify writes this run: 0.** Steps 1–6 were done and merged earlier today (run 1, `claude/organic-2-1017-h3c9kj`, merged at 586648d). Per STEP 0 they were skipped as done and **re-verified against the live store**. Step 7 (eBay maths) is new. Run 1's full detail stays in git history (`git show 4c3e3d1:REPORT-2026-10-17-organic-2.md`).

Branch: the session's assigned branch is `claude/organic-2-1017-9a79lu` (the brief said `claude/organic-2-1017`, the same topic). It started at origin/main 254e979.

## Summary

| Step | Result |
|---|---|
| 0 State | PASS — read CLAUDE.md, QUEUE.md, `REPORT-2026-10-17-organic.md`, run 1's report, `data/jan-2026-10-17.csv`, `data/routing-2026-10-17.csv`, `git log -10`. Steps 1–6 done in run 1 → skipped, re-verified live |
| 1 2026 guide stock list | PASS (done in run 1, no write) — live body unchanged since run 1's read-back (updatedAt 05:31:11Z). 14 Pokémon + 4 One Piece, all linking ACTIVE products; range $115–$470 still matches the live min/max of the 18 listed boxes |
| 2 Japanese cards guide | PASS (done in run 1, no write) — the per-box bullet is live, the $60–120 / pull-rate bullet is gone (updatedAt 05:41:30Z, run 1's read-back) |
| 3 Dead-link sweep | PASS with 1 accepted link — no published article in the 4 tags has changed since run 1 (latest updatedAt 05:41:30Z). Re-read the 6 JP-sealed articles: 1 DRAFT link (EB-05 guide → EB-05 pre-order draft), which Ethan accepted in run 1 |
| 4 Channels | PASS — 20/20 ACTIVE jp-sealed on all 7 channels (re-read via `resourcePublicationsV2`), 0 gaps, 0 publish writes |
| 5 Social poster | PASS — `env` all MISSING; `dry-run` 0 invalid; `cloud-run --dry-run --no-render` every platform NOT CONFIGURED, 0 invalid payloads, would_post 0; Discord-only test passes |
| 6 JAN retry | PASS (no write) — FB12 and M7 still blank; looked again, logged in `data/jan-2026-10-17.csv` |
| 7 eBay maths | PASS — `data/ebay-box-maths-2026-10-17.csv`, 20 rows, 0 blank landed cost. eBay price now and last-sold: **NOT CHECKED** |
| 8 Gates | 7 PASS, 1 FAIL that Ethan already accepted (the EB-05 link) — see below |
| 9 Wrap | QUEUE.md updated, committed, merged `--no-ff` into main, pushed |

## Step 1 — 2026 guide (688213655830): links before → after

Run 1: 7 links → 21 links (collection ×2, then M6a, M6 no-shrink, M5, M5 no-shrink, M3, M3 no-shrink, M1S, M1L, sv9a, sv8a, sv8, sv7, sv3a, s12a, OP-16, OP-12, OP-11, OP-07). This run: 21 → 21. Every linked product is still ACTIVE with stock > 0 or policy CONTINUE. The live min/max of the 18 listed boxes is $115 (M3 no-shrink) / $470 (OP-11), so the sentence is unchanged.

## Step 2 — Japanese cards guide (683629674774): links before → after

2 → 2 (collection, M1S). Live bullet: "Japanese booster boxes hold fewer cards than English boxes, so compare them per box, not per pack". No price figures, no pull-rate claim.

## Step 3 — Dead links

Scope: the 40 published articles tagged `japanese` / `sealed` / `one-piece` / `pokemon` (re-listed: none updated since run 1). The 6 JP-sealed articles were read again:

| Article id | Article | Product/collection links | Not ACTIVE |
|---|---|---|---|
| 688213655830 | 2026 booster box guide | 21 | 0 |
| 683629674774 | Japanese cards guide | 2 | 0 |
| 683583242518 | Spot-a-fake guide | 2 (collection, M3 sealed) | 0 |
| 683583308054 | Japanese vs English | 2 (collection, sv8a) | 0 |
| 688481501462 | M6a buying guide | 2 (M6a, collection) | 0 |
| 688481534230 | EB-05 guide | 3 (collection, EB-05, OP-12) | **1**: `/products/pre-order-one-piece-heroines-edition-vol-2-eb-05-sealed-japanese-booster-box` → 15431829848342 DRAFT |

Run 1's dead-link table (`data/deadlinks-2026-10-17-organic-2.csv`) still holds: OP-17 10734775730454 and OP-13 10734775566614 removed, M6a repointed, EB-05 left (no ACTIVE equivalent; Ethan accepted it). No new dead links.

## Step 4 — Channel matrix

| Product | Online Store | Google & YouTube | Pinterest | Shop | FB & IG | TikTok | Microsoft |
|---|---|---|---|---|---|---|---|
| 20 ACTIVE jp-sealed (ids in `reports/channels-2026-10-17-organic-2.csv`) | 20 | 20 | 20 | 20 | 20 | 20 | 20 |

0 gaps, `publishablePublish` not called. Drafts not touched.

## Step 5 — Social poster

- `python -m tools.social env`: instagram, facebook, youtube, pinterest, discord, tiktok_queue, tiktok and shopify_files all MISSING (names in MANUAL).
- `python -m tools.social dry-run`: 0 invalid on all 7 platforms. Valid: discord 14, facebook 29, instagram 29, pinterest 43, tiktok 42, tiktok_queue 14, youtube 29.
- `python -m tools.social cloud-run --dry-run --no-render`: every platform NOT CONFIGURED, "invalid payloads / rule violations: 0", would_post 0. `data/social-runner.log` restored afterwards, so nothing changed.
- Discord-only: `NotConfigured.test_discord_only_posts_discord_and_nothing_else` passes. It sets only `DISCORD_WEBHOOK_PICKUPS`, uses a fake HTTP client and no network: Discord posts, everything else stays NOT CONFIGURED.
- Clips: 49 queued mp4s are gitignored, so they aren't in this container (media missing 29/29/42). cloud-run renders them at run time, and the session-start hook installs the render deps.

## Step 6 — JAN result

| Product | Result | Where I looked this run |
|---|---|---|
| FB12 · 15417947291926 | blank | kakaku S0001046479 [BOX] page still prints no JAN (4582770078718 appears only in a toysprime image path). Run 1's two box listings with conflicting JANs are unresolved |
| M7 · 15417947455766 | blank | web search for ハドウシーカー BOX JAN: no listing. Run 1 checked amiami, hlj, kakaku and pokemoncenter-online with nothing found |

Barcode fields not written. Notes appended to both rows of `data/jan-2026-10-17.csv`.

## Step 7 — eBay maths (read + compute only)

Inputs:
- **FX:** 1 JPY = **0.009112 AUD** (open.er-api.com, 17 Oct 2026 00:02 UTC).
- **Supplier yen:** `data/routing-2026-10-17.csv`. Urara ¥ where Urara has a row, otherwise Kanade ¥ (M5 sealed, M3 sealed, M1S, sv8a). I re-read the Urara.Chii List (16 Oct): its Pokémon prices match the CSV. Not in the CSV: the Mega Gengar deck is ¥3,500 and the Fukuoka box ¥14,000 (Urara Pricelist_Other; Fukuoka shows a price but stock "-"). **Nihil Zero (M3) no-shrink has no supplier price anywhere** (Urara "Munikisu Zero No-Shurink" is "-", and Kanade has no no-shrink rows), so it uses Kanade's M3 sealed ¥8,580 as a **PROXY**, flagged in the CSV. This is an upper bound, which overstates that box's cost.
- **Landed (bulk):** (supplier ¥ + ¥6,500 ÷ 12) × FX.
- **GST:** a 10% column, flagged and **not applied**. `consignment_of_12_over_1000` is Y for 17 of 20 boxes, meaning a 12-box consignment of that box would cross A$1,000.
- **eBay price now:** **NOT CHECKED.** There's no eBay active-listings export in `data/` or anywhere in the cloud (Drive has only 2023–24 eBay files). The Shopify price stands in.
- **eBay net** = price × (1 − 13.5%) − $0.30 − $15.25 post − $1.50 packaging. Breakeven = (landed + $17.05) ÷ 0.865. The +10% and +18% prices give net = landed × 1.10 / 1.18 (the CSV also has rounded-up-to-$5 versions).
- **eBay last-sold comps:** **NOT CHECKED.** ebay.com.au returned 403 on one try, so nothing is estimated.

Sorted by margin at the Shopify price, best first. Margin = eBay net at the Shopify price − bulk landed.

| # | Box | Yen (source) | Landed bulk | GST 10% flag | Shopify | eBay net @ Shopify | Margin $ | Margin % | Breakeven | +10% | +18% | Shopify clears +10%? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Abyss Eye (M5) sealed | ¥8,880 (Kanade) | $85.85 | $8.59 | $190 | $147.30 | $61.45 | 71.6% | $118.96 | $128.88 | $136.82 | Y |
| 2 | Raging Surf (sv3a) | ¥14,500 (Urara) | $137.06 | $13.71 | $245 | $194.88 | $57.82 | 42.2% | $178.16 | $194.01 | $206.68 | Y |
| 3 | VSTAR Universe (s12a) | ¥28,500 (Urara) | $264.63 | $26.46 | $390 | $320.30 | $55.67 | 21.0% | $325.64 | $356.23 | $380.71 | Y |
| 4 | Heat Wave Arena (sv9a) | ¥19,000 (Urara) | $178.06 | $17.81 | $285 | $229.47 | $51.41 | 28.9% | $225.56 | $246.15 | $262.62 | Y |
| 5 | Pokemon Center Fukuoka special box | ¥14,000 (Urara) | $132.50 | $13.25 | $230 | $181.90 | $49.40 | 37.3% | $172.89 | $188.21 | $200.47 | Y |
| 6 | Storm Emeralda (M6) no-shrink | ¥9,300 (Urara) | $89.68 | $8.97 | $180 | $138.65 | $48.97 | 54.6% | $123.38 | $133.75 | $142.05 | Y |
| 7 | Stellar Miracle (sv7) | ¥12,200 (Urara) | $116.10 | $11.61 | $210 | $164.60 | $48.50 | 41.8% | $153.93 | $167.36 | $178.09 | Y |
| 8 | Mega Brave (M1L) | ¥9,400 (Urara) | $90.59 | $9.06 | $175 | $134.32 | $43.74 | 48.3% | $124.44 | $134.91 | $143.29 | Y |
| 9 | OP-16 | ¥10,300 (Urara) | $98.79 | $9.88 | $180 | $138.65 | $39.86 | 40.3% | $133.92 | $145.34 | $154.48 | Y |
| 10 | 30th Celebration (M6a) no-shrink | ¥25,000 (Urara) | $232.74 | $23.27 | $330 | $268.40 | $35.66 | 15.3% | $288.77 | $315.68 | $337.20 | Y |
| 11 | OP-07 500 Years in the Future | ¥18,000 (Urara) | $168.95 | $16.90 | $250 | $199.20 | $30.25 | 17.9% | $215.03 | $234.56 | $250.19 | Y |
| 12 | Mega Symphonia (M1S) | ¥10,980 (Kanade) | $104.99 | $10.50 | $175 | $134.32 | $29.34 | 27.9% | $141.08 | $153.22 | $162.93 | Y |
| 13 | OP-11 A Fist of Divine Speed | ¥39,000 (Urara) | $360.30 | $36.03 | $470 | $389.50 | $29.20 | 8.1% | $436.25 | $477.90 | $511.22 | N |
| 14 | Terastal Festival ex (sv8a) | ¥20,980 (Kanade) | $196.11 | $19.61 | $280 | $225.15 | $29.04 | 14.8% | $246.42 | $269.09 | $287.23 | Y |
| 15 | Super Electric Breaker (sv8) | ¥33,000 (Urara) | $305.63 | $30.56 | $390 | $320.30 | $14.67 | 4.8% | $373.04 | $408.38 | $436.64 | N |
| 16 | OP-12 Legacy of the Master | ¥18,800 (Urara) | $176.24 | $17.62 | $240 | $190.55 | $14.31 | 8.1% | $223.46 | $243.83 | $260.13 | N |
| 17 | Nihil Zero (M3) sealed | ¥8,580 (Kanade) | $83.12 | $8.31 | $130 | $95.40 | $12.28 | 14.8% | $115.80 | $125.41 | $133.10 | Y |
| 18 | Mega Gengar starter deck | ¥3,500 (Urara) | $36.83 | $3.68 | $70 | $43.50 | $6.67 | 18.1% | $62.29 | $66.54 | $69.95 | Y |
| 19 | Abyss Eye (M5) no-shrink | ¥9,000 (Urara) | $86.94 | $8.69 | $120 | $86.75 | $-0.19 | -0.2% | $120.22 | $130.28 | $138.32 | N |
| 20 | Nihil Zero (M3) no-shrink | ¥8,580 (PROXY) | $83.12 | $8.31 | $115 | $82.42 | $-0.69 | -0.8% | $115.80 | $125.41 | $133.10 | N |

Shopify price clears +10% on eBay: 15 Y, 5 N (OP-11, sv8, OP-12, M5 no-shrink, M3 no-shrink). No recommendation: Ethan picks the rule.

## Step 8 — Gates

| Gate | Result |
|---|---|
| 0 DRAFT/ARCHIVED product links in the 6 JP-sealed articles | **FAIL — 1, accepted by Ethan in run 1**: 688481534230 → 15431829848342 (EB-05 pre-order, DRAFT). It clears when the pre-order is published (a status write, not in scope). Not treated as a stop because Ethan pre-approved this exact link |
| 20/20 ACTIVE boxes on all 7 channels | PASS — 20 × 7 |
| 0 banned words on everything touched | PASS — this report, `QUEUE.md`, `data/ebay-box-maths-2026-10-17.csv`, `data/jan-2026-10-17.csv`, `scripts/ebay_box_maths_2026_10_17.py` (grep gate) |
| `python -m tools.social check` PASS, queue untouched | PASS — 15 days on all 6 queued platforms; `content/social-queue.json` md5 `50f9ac76…` before and after |
| dry-run 0 errors | PASS — 0 invalid; cloud-run dry-run 0 invalid payloads |
| 43 tests OK | PASS — 44 OK (the 43 plus run 1's Discord-only test) |
| Edited articles read back as before + stated edit only | PASS — no article written this run. Run 1's two edits are still live (updatedAt unchanged since their MATCH read-back) |
| ebay-box-maths CSV: 20 rows, no blank landed cost | PASS — 20 rows, 0 blank. 1 PROXY landed cost (Nihil Zero M3 no-shrink, 10734773895446), flagged |

## NOT CHECKED
- eBay price now for every box: no eBay active-listings export is reachable from the cloud. The Shopify price stands in.
- eBay last-sold comps: ebay.com.au 403.
- Supplier price for Nihil Zero (M3) no-shrink: neither supplier lists one. A proxy is used and flagged.
- Storefront HTTP (the shell proxy blocks hokocollectables.com). Links were checked by Admin API handle → status.
- Live posting (no keys).

## MANUAL

**Ethan only:**
- **eBay repricing rule:** pick one (for example breakeven / +10% / +18%, rounded up to $5) from `data/ebay-box-maths-2026-10-17.csv`. For real eBay columns, drop an eBay active-listings export (Seller Hub → Listings → Active → Download) into `data/`. The next run fills the eBay-now column from it (the script currently uses the Shopify stand-in).
- EB-05 pre-order (15431829848342): publishing it is your click, and it clears the last DRAFT link.
- Social keys. One line per key. Put them in **claude.ai/code → this environment → Environment variables** for cloud-run, and/or Windows *User* environment variables for the PC runner. Never in the repo.
  - `DISCORD_WEBHOOK_PICKUPS`: Discord → HOKO server → #pickups-and-drops → Edit Channel → Integrations → Webhooks → New Webhook → Copy Webhook URL
  - `DISCORD_WEBHOOK_TIKTOK_QUEUE`: same steps on #tiktok-queue
  - `PINTEREST_TOKEN`: developers.pinterest.com → My apps → (create app) → Generate access token, scopes `pins:write`, `boards:read`
  - `PINTEREST_BOARD_ID`: with that token, `GET https://api.pinterest.com/v5/boards` → `id` of the board to pin to (or the number in the board's edit URL)
  - `META_PAGE_TOKEN`: developers.facebook.com → your app → Tools → Graph API Explorer → user token with `pages_show_list, pages_read_engagement, pages_manage_posts, instagram_basic, instagram_content_publish` → extend in Access Token Debugger → `GET /me/accounts` → the HOKO Page's `access_token` (or Meta Business Suite → Settings → Users → System users → Generate token, never expires)
  - `FB_PAGE_ID`: Facebook Page → About → Page transparency → Page ID (also the `id` in `/me/accounts`)
  - `IG_BUSINESS_ID`: Graph API Explorer → `GET /<FB_PAGE_ID>?fields=instagram_business_account` → its `id` (IG must be a professional account linked to the Page)
  - `YT_CLIENT_ID`: console.cloud.google.com → APIs & Services → Library → enable YouTube Data API v3 → Credentials → Create credentials → OAuth client ID (Desktop app) → Client ID
  - `YT_CLIENT_SECRET`: same Credentials page → that OAuth client → Client secret
  - `YT_REFRESH_TOKEN`: developers.google.com/oauthplayground → gear → "Use your own OAuth credentials" (the two above) → scope `https://www.googleapis.com/auth/youtube.upload` → Authorize as the HOKO channel → Exchange code → Refresh token
  - `SHOPIFY_STORE`: `dgcrmf-sh.myshopify.com` (Shopify admin → Settings → Domains shows it)
  - `SHOPIFY_ADMIN_TOKEN`: Shopify admin → Settings → Apps and sales channels → Develop apps → Create app → Admin API scopes `write_files` (+ `read_products`) → Install → Reveal token once
  - `TIKTOK_ENABLED`: leave unset / `false` (phone pack via Discord is the TikTok path)
  - `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN`: only if you turn the API on later. developers.tiktok.com → Manage apps → app → Content Posting API (`video.publish`)


**PC only:** last-sold comps (eBay blocks the cloud). Clip render if cloud-run can't render.

## COMPLETE
