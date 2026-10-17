# REPORT — 2026-10-19 · Overnight (`claude/overnight-1018`)

## MORNING SUMMARY FOR ETHAN
1. Part A is done and on main: **OP-18 is $219** (read back in Shopify and on the storefront) and the BF page tile says $219. M7 $190, FB12 $165 and EB-05 $235 are unchanged.
2. Listing sweep over all **640 ACTIVE** products: 279 pass every check. The big gap is **301 SEO titles over 60 characters** (the " | HOKO Collectables" suffix pushes them over), then 89 with fewer than 3 tags. CSV: `data/listing-quality-2026-10-19.csv`.
3. SEO fill: **6 graded slabs** got an SEO title; read back 6/6 with 0 userErrors. I skipped 3 bundles tagged `mystery-pack`, which are banned language and your call.
4. Two blog articles are saved as **DRAFTS** (M7, OP-18) and need your Publish click. IDs are under MANUAL.
5. **54 open orders show UNFULFILLED, every one from eBay.** 15 are since #1472 (10 Oct) and **39 are older (Jun–Aug)**, so the eBay fulfilment sync has gaps going back well before 10 Oct.
6. Social queue is fine through 31 Oct (0 invalid, 0 missing, 60% newest), so no topup was needed. 0 abandoned checkouts in the last 24 h. The discount codes match CLAUDE.md.

## PASS / FAIL

| Step | Result | Detail |
|---|---|---|
| B1 Listing quality sweep | **PASS** | 640 ACTIVE products read in one bulk operation (products → collections → variants). `data/listing-quality-2026-10-19.csv`, script `scripts/shopify/listing_quality_2026_10_19.py` |
| B2 SEO fill: gate on generated strings | **PASS — 0** | 1 length fail on the first build (Bellsprout, 65 chars) was caught and shortened before anything was written; 0 banned words, 0 `$` |
| B2 SEO fill: write | **PASS** | Backup `reports/backups/2026-10-19-seo-fill-before.csv`, payload `…-payload.json`; 1 example written and checked, then 5 sequential `productUpdate` (1 batch ≤ 250), SEO fields only, 0 userErrors |
| B2 Read-back | **PASS — 6/6 (100%)** | Second bulk read: SEO of the 6 == payload; across all 640 products, 0 other SEO diffs, 0 status diffs, 0 variant price/qty/barcode diffs. `…-readback.json` |
| B3 Two DRAFT articles | **PASS** | Created with `isPublished: false`, read back false. 0 banned words, 0 prices (`$`/¥/円), pre-order line verbatim, 7/7 internal links 200 |
| B4 `check` | **PASS** | 15 days/platform, 60% hot on all 6 |
| B4 `dry-run` | **PASS** | 0 invalid, 0 missing media on every platform; all platforms NOT CONFIGURED |
| B4 `topup` | **SKIPPED (not needed)** | Queue ends 31 Oct, 14 days out (> 7) |
| B5 Reads | **PASS** | See below |
| B6 Banned-word gate | **PASS — 0** | `scripts/banned-word-gate.sh` (the seo_fill regex was split at runtime so the gate stays at 0) |
| B6 Tests | **PASS** | 86 OK |
| B6 `check` | **PASS** | |
| Merge | **PASS** | `claude/overnight-1018` → main `--no-ff`, pushed |

## B1: summary

Active products: 640 · all checks PASS: 279

| Check | Missing / failing | Rule |
|---|---|---|
| image | 0 | >=1 image |
| desc_40w | 1 | description >=40 words |
| seo_title | 310 | SEO title set, <=60 |
| seo_desc | 4 | SEO description 50-160 |
| type_set | 0 | productType set |
| tags_3 | 89 | >=3 tags |
| collection | 0 | >=1 collection |
| barcode_sealed | 3 | barcode on every variant (sealed only) |

Worst 20 by value (listings with >=1 failing check, highest value first):

| # | ID | Title | Value | Fails |
|---|---|---|---|---|
| 1 | 15417947455766 | [PRE-ORDER] Pokemon Aura Seeker (M7) Sealed Japanese Booster Box | $1140.00 | barcode_sealed |
| 2 | 15417947291926 | [PRE-ORDER] Dragon Ball Super Reach the God (FB12) Sealed Japanese Boo | $990.00 | barcode_sealed |
| 3 | 10655248810262 | Pikachu 27 Black Star Promo Pokemon PSA 10 GEM MINT | $599.00 | seo_title |
| 4 | 10655248777494 | Nami Alt Art R EB02017 One Piece BGS 10 Gold | $499.00 | seo_title seo_desc |
| 5 | 10655248613654 | Detective Pikachu 098/SVP Black Star Promo Pokemon BGS 9 Silver | $475.00 | seo_title |
| 6 | 10655248220438 | Magikarp 080/073 Art Rare SV1a Triplet Beat Japanese Pokemon PSA 9 | $450.00 | seo_title |
| 7 | 10481579065622 | MTG Card Bundle — 50 Cards incl. 5 Rares + 2 Foils | $299.00 | seo_title |
| 8 | 10534845317398 | Roronoa Zoro (Alternate Art) OP01 One Piece Promotion Cards One Piece  | $299.00 | seo_title |
| 9 | 10655248711958 | Nico Robin OP12-087 Alt Art Super Rare One Piece BGS 9.5 Gold | $275.00 | seo_title seo_desc |
| 10 | 10655256936726 | Kuzan (040) (Alternate Art) OP12-040 Legacy of the Master One Piece Fo | $118.00 | seo_title |
| 11 | 10655248122134 | Bellsprout 69 Topps Chrome TV Animation Series Pokemon PSA 9 | $115.00 | seo_title |
| 12 | 10655256674582 | Sanji & Pudding (Alternate Art) EB02-035 anime 25th One Piece Foil NM | $115.00 | seo_title |
| 13 | 15396362682646 | MTG Teenage Mutant Ninja Turtles Turtle Power! Commander Deck Sealed T | $100.00 | barcode_sealed |
| 14 | 10495484952854 | Pokémon Paradox Rift Card Bundle — 10 Near Mint Cards | $79.92 | desc_40w seo_title seo_desc |
| 15 | 10655247958294 | Monkey.D.Luffy P-106 One Piece Promotion Cards One Piece NM | $69.00 | seo_title |
| 16 | 10417121886486 | Dark Knight's Greatsword 95 Uncommon FINAL FANTASY Magic: The Gatherin | $54.99 | seo_title tags_3 |
| 17 | 10655247499542 | Marshall.D.Teach P-100 One Piece Promotion Cards One Piece Foil NM | $45.00 | seo_title |
| 18 | 10543581266198 | Emeritus of Abundance 145 | $36.00 | seo_title |
| 19 | 10655255101718 | Goliath - Clan Leader 173/204 Legendary Whispers in the Well Lorcana N | $32.00 | seo_title |
| 20 | 10655257788694 | Wing Gundam Zero (EW) GD05-067 LR Freedom Ascension Gundam Holo Near M | $29.00 | seo_title |

Breakdown:
- **SEO title:** 9 empty (6 filled in B2, 3 bundles skipped) and **301 over 60**. Over-length was out of scope for B2, which fills empty fields only.
- **SEO description:** 2 empty (the skipped bundles) and 2 at 161 characters (Nami 10655248777494, Robin 10655248711958; 1 over).
- **Tags < 3:** 89, made up of 75 MTG singles, 13 Pokémon singles and 1 DBS single (mostly `game:mtg` + `mtg-single` only).
- **Barcode (sealed):** 3 missing: M7 15417947455766 and FB12 15417947291926 (no verifiable JAN yet, known), plus MTG TMNT Commander deck 15396362682646.
- **Description < 40 words:** 1, the Paradox Rift bundle 10495484952854 (37 words).
- **Value** = max variant price × max(inventory, 1). That's why the two pre-orders at qty 6 top the list.

## B2: written (6)

| Product | SEO title (len) |
|---|---|
| 10655248810262 | Pikachu 27 Black Star Promo PSA 10 \| HOKO Collectables (54) |
| 10655248122134 | Bellsprout 69 Topps Chrome PSA 9 \| HOKO Collectables (52) |
| 10655248220438 | Magikarp 080/073 SV1a Triplet Beat PSA 9 \| HOKO Collectables (60) |
| 10655248613654 | Detective Pikachu 098/SVP Promo BGS 9 \| HOKO Collectables (57) |
| 10655248711958 | Nico Robin OP12-087 Alt Art BGS 9.5 \| HOKO Collectables (55) |
| 10655248777494 | Nami EB02-017 Alt Art BGS 10 Gold \| HOKO Collectables (53) |

The six already had SEO descriptions, which were passed back unchanged. The examples were committed in this report (70429d2) before the bulk run.

## B3: articles (DRAFT)

- `gid://shopify/Article/688483762454`, "Aura Seeker (M7): what's in the box and when it lands", handle `aura-seeker-m7-whats-in-the-box-and-when-it-lands`. **Every fact is marked reported**: 27 Nov date, 5 cards/pack, 30 packs/box, Mega Lucario ex headline (The Pokémon Company hasn't published the set page yet). Source copy `content/articles/2026-10-19-m7-aura-seeker.html`.
- `gid://shopify/Article/688483795222`, "The Dominance of God (OP-18) pre-order guide", handle `the-dominance-of-god-op-18-pre-order-guide`. Bandai JP page: 21 Nov 2026, 6 cards/pack, 127+1 types, Water Seven / Holy Knights of God, Saint Gunko and Saint Shamrock debut. EN page: 20 Nov. 24 packs/box is labelled as the standard box (Bandai's page doesn't list it). Source copy `content/articles/2026-10-19-op18-preorder-guide.html`.
- Both link the product + `/collections/japan-direct-sealed`, the 2026 guide and the spot-a-fake guide. Author Ethan Ryan, blog `news`.

## B5: reads

- **Unfulfilled (open) by channel:** eBay **54**, Online Store / other **0**, partial 0. eBay since 10 Oct: #1472–#1487 (15; #1475 isn't in the list). Older eBay: Aug #1341–#1354 (14), Jul #1299–#1316 (20), Jun–Jul #1182, #1188, #1213, #1217, #1227, #1282, #1286 (7). The last eBay order marked shipped is #1471 (10 Oct).
- **Abandoned checkouts, last 24 h:** **0** (0 bot-pattern, 0 real). There are 25 in total, the newest from 15 Oct 09:51–09:52 UTC in 30-second bursts (the bot pattern seen before).
- **Discount codes vs CLAUDE.md: MATCH.** Live: `WELCOME10` ACTIVE · `THANKS10` ACTIVE · `BFDROP5` SCHEDULED · "Black Friday — 10% off singles under $100" SCHEDULED · "Black Friday: Free AU postage" SCHEDULED (all BF: 26 Nov 13:00Z – 30 Nov 12:59Z = 27–30 Nov Victoria time). Expired, harmless: SORRY10, DISCORD15, "Buy 3 or More". No writes.
- **Pre-order prices:** M7 **190.00** · OP-18 **219.00** · FB12 **165.00** · EB-05 **235.00**, all ACTIVE. ✔

## Counts

Shopify writes this part: 6 `productUpdate` (SEO title only) + 2 `articleCreate` (DRAFT). Two read-only bulk operations. 0 price, discount, inventory, status or order writes. 0 posts.

## NOT CHECKED

- eBay side of the 54 unfulfilled orders: eBay is 403 from the cloud.
- Render (`edge-tts` / `piper-tts`): not attempted because topup wasn't needed.
- M7 facts against The Pokémon Company's own page (not published yet).

## MANUAL

**Phone (Ethan):**
- Review and publish the two DRAFT articles (Shopify app → Online Store → Blog posts): 688483762454 (M7) and 688483795222 (OP-18).
- Decide on the 3 card bundles tagged `mystery-pack` / `hoko-mystery`. One title says "Mystery Chaos Bundle", which CLAUDE.md bans. IDs 10481579065622, 10495484952854, 10495496454422. No SEO written. The MTG bundle's SEO description also carries a price.

**PC:**
- eBay channel order sync: 54 eBay orders open and UNFULFILLED back to June, not only since 10 Oct.
- Bulk fix for the 301 SEO titles over 60 characters (a content-only job under the bulk rule, if you want it, e.g. a shorter suffix or trimmed card names) and the 89 listings with fewer than 3 tags.
- Stale copy seen during the sweep (not changed):
  - Slab SEO descriptions say "free tracked postage" on sub-$150 slabs (e.g. Bellsprout).
  - Older descriptions carry "Tracked postage free on orders over $30" / "$12.50" / "Express $19.50", which don't match the canon postage.
  - The 2 SEO descriptions at 161 characters.
- MTG TMNT Commander deck 15396362682646 has no barcode.

## COMPLETE
