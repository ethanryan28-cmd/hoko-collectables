# REPORT — 2026-10-17 consolidated run (`claude/consolidated-1017`)

Unattended run. Authorised writes this run: status, inventory-policy, tag, metafield, raise-to-floor price. Every Shopify write has a before-copy in `reports/backups/` and was read back. No price lowered. Discounts, orders, fulfilments, payments untouched.

## Summary

| Step | Result |
|---|---|
| 0 State | PASS — nothing in this prompt was already done; prior runs (`REPORT-2026-10-17-finish.md`, `reports/REPORT-2026-10-17T1140+1100.md`) only overlap on the 15 boxes and the pre-order drafts, which are inputs here |
| 1 Scope + routing | PASS with one input NOT CHECKED (eBay AU sold counts, see below) |
| 2 Social in the cloud | STEP2_RESULT |
| 3 Store hygiene | STEP3_RESULT |
| 4 Wrap | PASS — branch merged `--no-ff` into main |

## Step 0 — State

- Branch: `claude/consolidated-1017` from `main` @ fbf9eba (finish-1017 merge).
- Read: CLAUDE.md (canon, 17 Oct), QUEUE.md, both 17 Oct reports, `git log -30`, `git branch -r` (10 remote branches; `claude/finish-1017` and 7 older `claude/*` branches still exist remotely — git proxy refuses remote deletes).
- Already done → SKIPPED: nothing. The 15 zero-stock boxes were set DRAFT by `claude/jp-boxes-draft` (7ee760a) and are candidates here by design.

## Step 1 — Scope + routing (Pokémon + One Piece Japanese sealed)

### Inputs
- FX: 1 JPY = 0.009112 AUD (open.er-api.com, 17 Oct 00:02 UTC).
- Kanade: Drive sheet "Price List" (owner asuzuki0816, modified 7 Aug 2026) — Pokémon + One Piece tabs, per-box yen.
- Urara: "Urara.Chii List" sheet, price list dated 16 Oct 2026 — a box counts as listed only when Stock > 0 and Price > 0. No-outer-shrink products are matched to Urara's "No-Shurink" rows; Kanade has no no-shrink rows, so those boxes have no Kanade route.
- Fees: Shopify Payments AU 1.75% + $0.30 (ASSUMPTION: Basic plan domestic card rate).
- Single landed = (Kanade ¥ + ¥5,500 freight + ¥500 signature) × FX. Batch landed = Urara ¥ × FX + A$14. Floor = (landed + fee) × 1.10, rounded up to $5.

### Live set
- (i) Newest 3 released sets per game: Pokémon **M6a, M6, M5**; One Piece **OP-17, OP-16, OP-15** (ASSUMPTION: EB-03 Heroines treated as an extra booster, not a main set).
- (ii) Pre-orders M7 / OP-18 / FB12: daily gate has not made them ACTIVE (none on the Urara list) → excluded, stay DRAFT. FB12 is Dragon Ball, outside this step's scope anyway.
- (iii) Top-5 older sets by eBay AU sold count last 30 days: **NOT CHECKED.** `ebay.com.au` returns HTTP 403 to this container (curl with browser UA and WebFetch both; proxy status shows no explicit deny, eBay bot-blocks the egress). Without sold counts the trim could not be computed, so **no in-stock ACTIVE box was set DRAFT on missing data**; the 11 zero-stock DRAFT boxes outside (i) stayed DRAFT. Shopify's own last-30-day orders were checked as a proxy: 1 box sold (Abyss Eye M5 sealed, draft order #1434, 27 Sep); every other order in the window was a single.
- M6a (15398993723670) and OP-17 (15402647453974 pre-order, 10734775730454) are in the live set by (i) but are not candidates under 1a (not ACTIVE, not in the 15, not a named pre-order) → left DRAFT, flagged MANUAL.

### Routing table
ROUTING_TABLE

Per-box reasons for "none":
- M6 sealed: Kanade 20,980 yen → single floor $280 vs $150 list ($130 gap); Urara has 0 sealed stock (only no-shrink at 9,300). Stays DRAFT.
- OP-15: Kanade 15,980 yen → floor $225 vs $165 ($60 gap); Urara 0 stock. Stays DRAFT.
- M3 sealed (in stock ×2): Kanade floor $150 is $20 above $130 (outside the $15 raise window); Urara 0 stock. Kept ACTIVE/DENY, sells in-hand stock only, no restock route.
- M3 no-shrink (in stock ×2): no supplier lists it today. Kept ACTIVE/DENY, in-hand only.

### Writes (all read back, 0 userErrors)
- Backup: `reports/backups/2026-10-17-routing-before.json` (19 products: status, tags, variant, price, policy, qty).
- 15 × `productUpdate`: one `route:` tag each, metafield `hoko.supplier` = kanade|urara. Live-set boxes also → `status: ACTIVE` and `OOS-SUPPLIER` tag dropped: **M5 sealed (DRAFT→ACTIVE, kanade), OP-16 (DRAFT→ACTIVE, urara), M6 no-shrink (urara), M5 no-shrink (urara)**.
- 7 × `productVariantsBulkUpdate`: `inventoryPolicy: CONTINUE` on the 4 live-set boxes; raise-to-floor on **sv3a $235→$245, s12a $375→$390, M1S $165→$175** (each within $15 of its Kanade floor). No price lowered.
- Collection `japan-direct-sealed` (534554444054, sortOrder MANUAL): `collectionReorderProducts` → positions 0–17 = M6 NOS, M5 sealed, M5 NOS, OP-16, then in-stock boxes newest set first (sv9a, sv8a, sv8, M1L, M1S, M3, M3 NOS, OP-12, OP-11, OP-07, sv7, sv3a, s12a, Fukuoka box). Read back in that order. Pre-orders are DRAFT so not placed.
- Black Friday page (167154385174): backup `reports/backups/2026-10-17-black-friday-page-before-routing.html`; added tiles for M5 sealed ($190) and OP-16 ($180), updated the three raised prices. Read back (updatedAt 03:09Z).
- `content/youtube/config.json` `hot_sets` → M6a M6 M5 OP-17 OP-16 OP-15 + in-stock sets (sv9a sv8a sv8 M1L M1S M3 OP-12 OP-11 OP-07 sv7 sv3a s12a); previous list kept as `hot_sets_before_2026_10_17`.
- `data/routing-2026-10-17.csv` written (handle, route, price, both floors, margin each way, note).

### Gates
- Each live box has exactly one `route:` tag: PASS (4/4 live-set boxes; 15/15 routed boxes overall).
- Banned words in routing outputs (CSV, config, backup, BF page body): 0 hits. PASS.
- `availableForSale` on the storefront (`/products/<handle>.js`): M6 NOS, M5 sealed, M5 NOS, OP-16 all `true` at the expected prices; sv3a $245, s12a $390, M1S $175 confirmed live. PASS.

STEP2_SECTION

STEP3_SECTION

## NOT CHECKED
- eBay AU sold counts (ebay.com.au 403 from the cloud) — the top-5 trim in 1b.
- Kanade's actual current stock (the Price List sheet has prices only, last modified 7 Aug).
- Shopify Payments plan rate (assumed 1.75% + $0.30).
NOT_CHECKED_EXTRA

## MANUAL

**Ethan only**
- Decide the eBay sold-count trim by hand (or run this step from the PC where eBay is reachable): 11 zero-stock boxes stay DRAFT, 11 in-stock boxes stay ACTIVE until then.
- M6a (30th Celebration, 15398993723670) and OP-17 (15402647453974 / 10734775730454) are "newest sets" but were not candidates — list price + which supplier, then they can be routed.
- Kanade's Storm Emeralda price (20,980 yen) looks stale vs Urara no-shrink 9,300; confirm before ordering M6 singles.
- Pre-orders M7 / OP-18 / FB12 remain DRAFT until they appear on the Urara list.
MANUAL_ETHAN_EXTRA

**PC only**
MANUAL_PC_EXTRA

## COMPLETE
