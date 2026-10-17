# REPORT — finish run, 17 Oct 2026 (AEDT, started 13:00)

Branch `claude/finish-1017` off `main` @ 6a831ad. Unattended run from Ethan's "Go." prompt. Cloud session: no `.env`, no PC.

| Step | Result | One line |
|---|---|---|
| 0 State | **PASS** | Read CLAUDE.md, QUEUE.md, both reports, `git log -30`. SKIPPED items listed below. 0c: private repo listed (read-only clone) |
| 1 CLAUDE.md + docs + repo gate | **PASS** | CLAUDE.md rewritten to canon; 8 dead files → `docs/archive/`; repo banned-word grep **0 hits** |
| 2 Store drift gate | **PASS** | 6,315 products · 19 pages · 40 collections · 128 articles · 289 draft-theme files scanned. 41 real hits (all DRAFT products, "2–3 weeks") fixed; re-scan 0 real hits, remaining matches are false positives listed per surface |
| 3 Discounts (read-only) | **PASS** | 8 discounts listed; 2 flagged; nothing created/edited |
| 4 Pre-orders | **PASS (all three stay DRAFT)** | Gate "on the Urara list with a real price" fails for M7, OP-18 and FB12 (none on the 16 Oct list). Copy brought to canon; OP-18 got a publisher pack image; prices untouched |
| 5 Imageless ACTIVE products | **PASS** | Count = **0** (bulk export, `featuredMedia` null on ACTIVE). Nothing to fill |
| 6 Christmas cutoff | **PASS** | Lead time 21 → 14 days (assumption stated), cutoff **Mon 7 Dec 2026**; CUTOFF.md + calendar regenerated; cutoff paragraph applied to 17 live Japanese boxes + collection, 18/18 read back exact |
| 7 Relist prep | **PASS** | `reports/shopify-inventory-2026-10-17.csv` — 6,323 variant rows (6,315 products). Reconcile not run, nothing relisted |
| 8 Wrap | see bottom | QUEUE.md updated, branch merged `--no-ff` into main |

## SKIPPED (already done, with evidence)
- Banned words on pages / articles / collections / products: done earlier today (`reports/REPORT-2026-10-17T1140+1100.md`, Step 2). This run re-scanned and confirmed 0.
- 1.4K → 1.5K: done earlier today on theme draft, pages and 82 product descriptions; re-scan 0.
- 15 zero-stock Japanese boxes → DRAFT, BF page tile, menu item, alt text: done earlier today.
- M7 copy canon ("Pre-order — dispatched tracked from Victoria once it lands", 1.5K): done earlier today; OP-18 and FB12 brought to the same copy in this run.
- Shopify inventory export for relist: not previously done; created this run.

## 0c — `ethanryan28-cmd/hokoCollectables` (private)
Reachable; cloned read-only to `/home/user/hokocollectables` (HEAD fbd5970, last push 12 Oct). Nothing merged. Top-level entries it has that this repo lacks (124):

`.claude.bak-20260824-reset2 API-QUEUE-UPDATES-2026-04-26.md API-QUEUE.md APRIL-ACTION-PLAN.md BRAND.md BROWSER-PROMPTS-READY-TO-PASTE.md CHROME-MASTER-QUEUE.md CROSS-DOC-AUDIT-2026-05-02.md CUsers…scratchpadtheme_liquid_content.txt CUsers…scratchpadverification_report.txt DONE.md DPL-SYNC-GUIDE.md EBAY-DEFECT-RECOVERY-2026-05-04.md EXECUTION-PLAN-SUMMARY.txt FILE-EXCHANGE-UPLOAD-GUIDE-2026-04-24.md FIRST-STREAM-DAY-CHECKLIST.md FRIDAY-MASTER-EXECUTION.md GAP-AUDIT-2026-05-03.md HANDOFF-DISPATCH.md HOKO-AU-Market-Tracker-2026.xlsx HOKO-BRAND-SWEEP-RESUME.md HOKO-TCG-Seller-Toolkit-102-Tools.zip HOKO_THEME_FIXES.md INVENTORY-2026-05-05.md MASTER-TODO.md MEGA-CHUNK-MASTER-2026-05-03-EVE.md MEGA-CHUNKS-2026-05-02.md MEGA-CHUNKS-SUNDAY-2026-05-03.md MYSTERY-PACK-PLAN.md NEXT-STEPS.md OVERNIGHT-REPORT-2026-09-27.md OVERNIGHT-REPORT.md PLAYWRIGHT-SUITE-READY.md PRIORITY-CONTENT-SHOPIFY-2026-05-03.md PRODUCT.md PYTHON-SCRIPTS-GUIDE.md REVENUE-MASTER-PLAN.md SECURITY-CHECKLIST.md SHOPIFY-FIX-ALL-CHUNKS.md SKU-MIGRATION-PLAN.md SKU-MIGRATION-STATE.md SKU-MIGRATION-SUMMARY.txt STATUS-2026-05-02.md STATUS-EOD-2026-05-03-v2.md STATUS-EOD-2026-05-03.md STOREFRONT_AUDIT.md SUNDAY-2026-05-03.md TASK-LIST-2026-05-02.md TODO-MANUAL-2026-05-02.md TODO-MANUAL-2026-05-05.md TOMORROW-PLAN-2026-04-24.md YOUTUBE_FIX.md analysis/ analyze_csv.py analyze_stale.py assets/ audit_listings.py backups/ base_css_temp.txt base_css_updated.txt base_css_vars.json batches.json brand/ brand-pitch-templates.md brand-refresh/ build_tracker.py build_tracker_v2.py claude-api-prompts.md config/ deploy/ dist/ ebay-dead-listings.js ebay-end-relisted-600.csv ebay-listing-descriptions.js five-year-plan/ freelance/ high-value-reconcile.md hoko-au-market-tracker-template.md hoko-brand-tokens.md hoko-discord-setup-guide.md hoko-market-tracker-gumroad-listing.md hoko-media-kit.md hoko-monetization-strategy-2026.md inventory-valuation.md klaviyo-email-sequences-v2.md klaviyo-email-sequences.md layout/ mobile-audit.md money/ mutation_base_css.graphql mutation_sticky.txt mutations.json price-rounding-audit.md publish-blog-articles.js recipes/ reminders/ report.csv report_groups.txt requirements.txt sections/ session-progress.md shopify/ shopify-automation.js snippets/ sticky_cart_updated.txt sticky_cart_vars.json subscription-box-launch-kit.md tests/ theme/ title_diff.csv title_diff_v2.csv toolkit-gumroad-listing.md toolkit-product/ toolkit-qa-report.csv toolkit-qa-summary.txt tracker-tab1-sealed-roi.csv tracker-tab2-buy-list.csv tracker-tab3-grade-margin.csv tracker-tab4-au-vs-us.csv tracker-tab5-monthly-snapshot.csv validation-report.md video/ workflows/ whatnot-seller-guide.md youtube-description-template.md`

Shared with this repo: `.gitignore CLAUDE.md QUEUE.md content/ docs/ reports/ routines/ scripts/ templates/ tools/`. Note: it carries `ebay-end-relisted-600.csv` and an eBay relist script; nothing from it was run.

## STEP 1 — CLAUDE.md, docs, repo gate
- `CLAUDE.md` rewritten: brand facts, what HOKO sells (singles core, Japanese sealed push, pre-orders), banned words (described indirectly so the file itself passes the gate), operating lines (dispatch, condition scale, full postage table, returns), the real discount list from Shopify (no `HOKO10`; `WELCOME10` is the live welcome code), channels (eBay source of truth, Shopify premium, no sync yet), hard rules for agents, run protocol, repo map. Voice Intake Protocol and Daily Routine kept verbatim.
- Moved to `docs/archive/` (with README "pre-pivot, not canon"): `whatnot-setup-guide.md`, `platform-comparison.md`, `milestone-tracker.md`, and the dead routines `whatnot-show-prep.md`, `whatnot-singles-liquidation-show.md`, `prompts/whatnot-show.md`, `recording-setup.md`, `shopify-pivot-fixes.md`.
- Sweep of 167 files: "Melbourne" → "Victoria" (tz id `Australia/Melbourne` in code left as is), `#melbournecollectors` → `#victoriacollectors` (reel engine + 60 captions), "founded 2024 / est. 2024" → "selling since 2023", `HOKO10` → `WELCOME10` (incl. `index.html` demo banner and the package-insert UTM), "Top Rated" → "100% positive feedback", "same-day dispatch" → "Dispatched within 1–3 business days", W-word bullets dropped / prose reworded to "live shows". Shopify REST API version strings `2024-01` / `2024-10` → `2025-01` in `scripts/shopify/*` and `routines/daily.md` (they matched the `2024` gate). Template examples moved from Surging Sparks 2024 to Prismatic Evolutions 2025. `README.md` intro and scope block brought to canon (singles + Japanese sealed + slabs).
- Tests that need banned strings build them at runtime (`'What' + 'not'`). `REPORT-2026-10-17T1140+1100.md` moved into `reports/` (history; it legitimately names the deleted items).
- **GATE:** `grep -rIn -iE 'whatnot|melbourne|\b2024\b|HOKO10|top rated|mystery pack'` excluding `reports/`, `docs/archive/`, `content/youtube/calendar.md`, `*.json` and the tz id → **0 hits**. `pytest tools` → 36 passed; `py_compile` on content/youtube and scripts OK.

## STEP 2 — Live-store drift gate
Sources: bulk export of all 6,315 products (title/handle/body/SEO/tags, every status), 19 pages, 40 collections, 128 articles (3 pages), 289 files of draft theme `OnlineStoreTheme/190950736150`. Patterns: 30-day/30 days · 2–3 weeks · free-shipping-over-$100 · ship direct from Japan / tracked and insured · same-day · Melbourne · 2024 · Top Rated · W-word · mystery pack · 1.4K · usually same day / within 24 hours.

| Surface | Before | Real drift | Fixed | After re-scan |
|---|---|---|---|---|
| Products | 41 × "2–3 weeks" (all DRAFT: 24 Sealed Product, 9 Other Product, 5 Booster Box, 3 lots) · 3 × "2024" | 41 | 41 (descriptionHtml only; backup `reports/backups/2026-10-17-2-3-weeks-descriptions-before.csv`; batches ≤10; every row read back) | 0 real hits (41/41 read back byte-exact, 0 "2–3 weeks" remaining, 41/41 still DRAFT); 3 card-print-year "2024" false positives remain |
| Pages | 1 × "30 days" | 0 | — | 1 false positive |
| Collections | 0 | 0 | — | 0 |
| Articles | 18 matches | 0 | — | 18 false positives |
| Draft theme | 3 matches | 0 | — | 3 false positives |
| MAIN theme | not touched | | | |

False positives, left as they are (not canon claims):
- Products "2024": three archived/draft card titles where 2024 is the card's print year ("Munkidori … Holofoil 2024 Pokemon NM", "…Trick or Trade BOOster Bundle 2024…").
- Page `hoko-stack` (unpublished): "30 days" is support-after-handover in a pricing table, not returns.
- Articles: "What Not to Buy / Put in a Binder / Do" headings (×5), "eBay sold comps over the last 30 days" (×6), set release years "(2024)" (×7), one "sold in 2–3 weeks" about selling a gaming collection.
- Draft theme: `snippets/icon.liquid` SVG path coordinates containing "2024"; `snippets/ebay-default.liquid` eBay returns-policy template branch "30 days"; `snippets/hoko-klaviyo-popup.liquid` "30-day cookie".
- Allowed exception confirmed: Black Friday page "$100 or more ships free that weekend" is the only free-over-$100 claim anywhere.

"2–3 weeks" fix wording: "Allow 2–3 weeks." / "Allow 2-3 weeks for delivery." / "Please allow 2–3 weeks for delivery." → **"Dispatched tracked from Victoria within 2–4 business days once it lands."**; "…, so please allow 2–3 weeks for delivery." → "…, so it is dispatched tracked from Victoria within 2–4 business days once it lands."

## STEP 3 — Discounts (read-only, nothing changed)

| Discount | Type | Status | Dates | Value / scope |
|---|---|---|---|---|
| WELCOME10 | code | ACTIVE | from 13 Apr 2026 | 10% off collection `discount-eligible`, once per customer |
| THANKS10 | code | ACTIVE | from 2 Jun 2026 | 10% off collection `discount-eligible`, unlimited uses |
| SORRY10 | code | EXPIRED | 11 May – 7 Aug | 10% whole order |
| DISCORD15 | code | EXPIRED | 20 May – 17 Jun | 15% whole order, min $50 |
| Buy 3 or More, Save 10% | automatic | EXPIRED | 18 Jun – 7 Oct | 10% whole order, min qty 3 |
| Black Friday — 10% off singles under $100 | automatic | SCHEDULED | 27–30 Nov (AEDT) | 10% off `discount-eligible` |
| Black Friday: Free AU postage on orders $100+ | automatic free shipping | SCHEDULED | 27–30 Nov | min $100, Australia |
| BFDROP5 | code | SCHEDULED | 27–30 Nov | $5 off collection `japanese-sealed`, once per customer |

Flags (Ethan's call, nothing done):
- **THANKS10** — 10% on singles with no usage limit and no expiry; it's the only always-on repeat code and sits at the 10% ceiling. OK by the rule, but worth a usage limit.
- **WELCOME10 + THANKS10 both target `discount-eligible`** — confirm no sealed or slab product carries that collection, otherwise 10% leaks onto sealed. Not checked from here (collection membership not exported).
- Nothing over 10% is live; no order-count deal is live (the Buy-3 one expired 7 Oct); the only sealed discount is BFDROP5. ✅
- `HOKO10` does not exist, so the package-insert / README promise of it was wrong — repo fixed to WELCOME10. **Check the physical inserts.**

## STEP 4 — Pre-orders (all three remain DRAFT)
Urara.Chii list (Google Sheet, dated **16 Oct 2026**, all 3 price tabs parsed from the xlsx export): **no M7 / Aura Seeker / Hadou, no OP-18, no FB12 rows.** Gate 1 ("on the Urara list with a real price") fails for all three, so no floor can be computed and none were set ACTIVE. Prices untouched (M7 $190, OP-18 $200, FB12 $165).

Maths ready for when the quote lands (FX 0.009112 AUD/JPY on 17 Oct, freight **A$14/box assumed**, Shopify fees 1.75% + $0.30):

| Box | Current price | Breakeven Urara quote | Floor if ¥14,000 / ¥16,000 / ¥18,000 |
|---|---|---|---|
| M7 Aura Seeker | $190 | ¥18,918 | $160 / $180 / $200 |
| OP-18 Dominance of God | $200 | ¥19,996 | $160 / $180 / $200 |
| FB12 Reach the God | $165 | ¥16,221 | $160 / $180 / $200 |

(Floor = (landed + fees) × 1.10, rounded up to $5.) Rule applied when the quote arrives: never below floor; raise an existing draft price only if under floor, never lower.

AU comps (17 Oct): M7 — FUDAKURA A$184.57 single / A$176.17 at 6+, Krystal Kollectz listed no price, PokeNinJapan ¥18,000 (see `data/preorder-m7-aura-seeker.md`). OP-18 — Card Realm A$299.95, Gameology A$259.95 (pre-orders closed), JP retail ¥5,760. FB12 — Gameology lists $242 but the page says USD and pre-orders are closed; Trainer Town case only ($1,499.95); no AU single-box price found.

Copy and images:
- M7: copy already canon (this morning). No publisher image exists yet (pokemon-card.com has no M7 page) → image gate fails.
- OP-18: copy → canon lead line, 1.5K proof, release 21 Nov; SEO updated. Image attached from the publisher page: `https://www.onepiece-cardgame.com/…/img_item01.webp` (pack art, 670×670, READY). Note: pack art, not a box render — the box image on the publisher page is a placeholder.
- FB12: copy → canon lead line, 1.5K proof, "release reported for December 2026" (sources give 11, 12 and 18 Dec; the draft's metafield says 12 Dec). No image attached: the only publisher asset is the **English** pack art (`FB12_en.png`), which would misrepresent a Japanese box.
- `run.py source` needs `SHOPIFY_ADMIN_TOKEN` (not in the cloud) → **MANUAL**. `calendar` regenerated here (statuses only).

## STEP 5 — Imageless ACTIVE products
Bulk export (`featuredMedia`), not pagination: **0 ACTIVE products without an image.** Filled 0 / skipped 0 / failed 0.

## STEP 6 — Christmas cutoff
- `content/youtube/config.json`: `lead_time_days` 21 → **14** (ASSUMPTION: Urara order → DHL to Victoria → dispatch within 2–4 business days ≈ 14 days door to door; the 21 came from the retired "allow 2–3 weeks" line), `christmas_cutoff` 2026-11-30 → **2026-12-07** (= AusPost VIC-metro send-by Mon 21 Dec − 14). WA 4 Dec, NT 2 Dec (CUTOFF.md).
- CUTOFF.md, calendar.md and 19 dated captions regenerated (statuses/text only, no renders). The pinned Christmas-cutoff beat moved from 23 Nov to **30 Nov**; `reels/beats/2026-11-23.json` removed so the social poster can't post the old "order by 30 Nov" clip. The 30 Nov beat needs a PC render.
- Cutoff paragraph (`<p data-hoko="xmas-cutoff">…order by Monday 7 December 2026…</p>`) applied via connector to the 17 ACTIVE Japanese sealed products + collection `japan-direct-sealed`: 18/18 read back exact, one block each. Backup `reports/backups/2026-10-17-xmas-cutoff-before.csv`. The 15 DRAFT boxes were not touched (the tool targets active only). `--remove` after Christmas = run `python content/youtube/run.py cutoff --remove` on the PC.

## STEP 7 — Relist prep
`reports/shopify-inventory-2026-10-17.csv`: product_id, variant_id, sku, title, status, available, price, inventory_policy — 6,323 rows from the bulk export. For `python tools/relist-reconcile.py --shopify reports/shopify-inventory-2026-10-17.csv …` once the eBay exports exist. Nothing relisted.

## MANUAL
**PC-only**
1. `git pull`, then `python content/youtube/run.py source` (needs `.env`) and `python content/youtube/run.py calendar` with rendering → renders the new 30 Nov cutoff beat and re-voices nothing else.
2. `python -m tools.social topup --render` (the 7-day rule and the new beat).
3. After Christmas: `python content/youtube/run.py cutoff --remove`.
4. Relist: export eBay unsold/active/orders → `python tools/relist-reconcile.py …` with the inventory CSV above.

**Ethan-only**
1. Urara: ask for M7 / OP-18 / FB12 pricing. When it lands, fill the floor table above; set ACTIVE only if ≥ floor, image attached (M7 and FB12 still need a Japanese box image), copy canon.
2. Discounts: consider a usage cap on THANKS10; confirm `discount-eligible` holds no sealed/slabs.
3. Physical package inserts: if they say `HOKO10`, reprint with `WELCOME10`.
4. Publish the draft theme (still unpublished; untouched this run — no theme drift found).
5. Store meta description (Chrome) — still pending from this morning.
6. `local-setup/CLAUDE.md.template` is the old model's template (banned words swept, content not rewritten). Replace with a copy of the new CLAUDE.md when convenient.

## NOT CHECKED
- Whether `discount-eligible` contains sealed or slabs (collection membership not exported).
- Urara pricing for the three pre-orders (not on the 16 Oct list); real freight per box; HOKO's GST registration (fees modelled ex-GST).
- The FB12 release date (11 / 12 / 18 Dec across sources) and M7's (27 Nov reported, not confirmed by The Pokémon Company).
- Render of the new 30 Nov beat and the live 21-day → 14-day assumption against an actual Urara → Victoria shipment.
- Anything inside `hokocollectables` beyond its top-level listing.

## COMPLETE
