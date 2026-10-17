# Pre-order pricing brief — 18 Oct 2026

Confirm-or-adjust, not a gate. All four stay ACTIVE at their current prices until Ethan ticks a box below.
**No price was written.** Shopify was read only.

Data read 17 Oct 2026, ~21:00–22:15 Victoria time (the cloud clock); filed under the 18 Oct run.

## Inputs

| Input | Value | Source |
|---|---|---|
| FX | 1 JPY = **A$0.009112** | open.er-api.com, updated 17 Oct 2026 00:02 UTC |
| Freight JP → VIC | **A$14.00 / box (ASSUMPTION)** | same placeholder as the routing sheet; replace with a real invoice figure |
| Card fee | 1.75% + A$0.30 on the selling price | Shopify Payments AU domestic |
| Landed | cost ¥ × FX + 14 | |
| Floor | (landed + fee) × 1.10, rounded up to $5 | fee taken on the floor price itself: floor = 1.10 × (landed + 0.30) ÷ (1 − 1.10 × 0.0175) |
| GST | not modelled | NOT CHECKED (registration status) |

### Supplier cost (Urara / Kanade)

- **Urara: none of the four is listed** (sheet "Urara.Chii List", dated 17 Oct 2026). This time the full sheet was exported (xlsx, every tab, every row), so the 10-row preview limit doesn't apply. Grep for M7 / Hadou / Aura / Seeker / OP-18 / OP18 / Dominance / EB-05 / EB05 / Heroine / FB12 / FB-12 / Reach the God / Fusion returned 0 hits. The Pokémon tab tops out at M6a, the One Piece tab at OP-17 / EB-04 / PRB-02, and there's no Dragon Ball tab or row. → **NOT CHECKED (Urara: not listed as of 17 Oct 2026).**
- **Kanade:** no Kanade sheet in Drive. → **NOT CHECKED.**
- **Stand-in = JP retail pre-order price** (Bandai / Pokémon box RRP), labelled **RETAIL STAND-IN** on every line it feeds.

> **⚠ Direction of the stand-in.** The brief asked for the label "floor reads high", but the evidence says it reads **low**.
> JP retail for these boxes is ¥5,760–6,000. Urara sells *new* sets at roughly 2× JP retail:
>
> | Box | Urara ¥ (17 Oct) | Stock |
> |---|---|---|
> | OP-17 | ¥13,200 | 52 |
> | OP-16 | ¥10,300 | 8 |
> | EB-03 | ¥12,200 | 4 |
> | M6 | ¥11,200 | 50 |
> | M6a 30th Celebration | ¥26,000 | 128 |
>
> So every line below also shows a **"Urara-pattern" scenario** at the previous set's Urara price. Treat that as the realistic cost until Urara lists the box.

Formula check: at the current price, breakeven ¥ = (price − fee − 14) ÷ 0.009112.

## Current Shopify state (read only)

| Box | Product | Status | Price | Inventory |
|---|---|---|---|---|
| M7 Aura Seeker | `gid://shopify/Product/15417947455766` · SKU PRE-URA-M7-BOX | ACTIVE | **$190.00** | 6 |
| OP-18 The Dominance of God | `gid://shopify/Product/15417946865942` · SKU PRE-URA-OP18-BOX | ACTIVE | **$200.00** | 6 |
| FB12 Reach the God | `gid://shopify/Product/15417947291926` · SKU PRE-URA-FB12-BOX | ACTIVE | **$165.00** | 6 |
| EB-05 Heroines Edition vol.2 | `gid://shopify/Product/15431829848342` · SKU PRE-OP-EB05-BOX | ACTIVE | **$235.00** | 0 |

## Comps: excluded across all four

- **Probably English or unlabelled.** Titles don't say Japanese and they use the English set blurb:
  - Gameology: OP-18 $259.95, EB-05 $279.95, FB12 $279.95
  - Collectible Madness: $215 each
  - Good Games: OP-18 $399, EB-05 $429, FB12 $259
  - Let's Play Games: OP-18 $214.99
- **Other exclusions:**
  - Nippon Figures (USD)
  - KrystalKollectz M7 (A$0.00 placeholder)
  - PokeNinJapan ¥1 / ¥18,000 / ¥20,000 placeholders (the pages say so)
- **Unreachable from the cloud:** AmiAmi, Cardrush, MTG Mate (403), Toyger, Card Merchant (no connection), eBay AU (403).
- **japan-figure.com** is Japan-based (Minami Ward address) and sells to AU in AUD. It's flagged JP-based in every table.

---

## 1. Pokémon M7 Aura Seeker (ハドウシーカー) — now $190, ACTIVE

**Cost:**
- RETAIL STAND-IN ¥6,000, reported JP RRP from a gamenv.net search snippet (page 403).
- Urara-pattern ¥11,200 (M6 box).

| Line | Cost ¥ | Landed | Fee @ unrounded floor | Floor |
|---|---|---|---|---|
| RETAIL STAND-IN — floor reads low (see ⚠) | 6,000 | 68.67 | 1.65 | **$80** |
| Urara-pattern (M6 ¥11,200) | 11,200 | 116.05 | 2.58 | **$135** |

**Comps (read 17 Oct 2026):**

| Seller | Country | URL | Price |
|---|---|---|---|
| Good Deals Games | AU | https://www.gdgames.com.au/products/aura-seeker-booster-box-japanese-pokemon-tcg | A$224.95, pre-order (sold out) |
| Fudakura Australia | JP → AU wholesale | https://fudakura-australia.com/index.php?p=product&id=aura-seeker-booster-box | A$184.57 single, ex GST, MOQ 6 |
| Japan Figure | JP-based, AUD | https://japan-figure.com/en-au/products/pokemon-card-game-mega-aura-seeker-expansion-pack-box | A$397.00, pre-order |
| PokeNinJapan | JP | https://www.pokeninjapan.store/products/pre-order-box-aura-seeker-japanese-pokemon-card-booster-box | ¥18,000 placeholder ("cannot purchase at this price") |
| JP RRP | JP | gamenv.net (snippet, page 403) | ¥6,000 / box |

**Comp median: A$224.95** (184.57 / 224.95 / 397.00). **Short:** only one AU domestic retailer lists a Japanese M7 box. Searched with no listing: pokebox, cardrealmaus, dendenhobby, trainertown, groovycollectables, collectiblemadness, gameology, goodgames.

**Recommended: $190 (keep).** It sits just above the wholesale single price and $35 under the only AU retail listing. Margin stays positive up to ¥18,917, so even the realistic Urara-pattern cost leaves 37%.

Margin at $190 (fee $3.62):

| Urara ¥ (scenario) | Landed | Margin | Margin % |
|---|---|---|---|
| 6,000 (RETAIL STAND-IN) | 68.67 | 117.70 | 61.9% |
| 9,000 | 96.01 | 90.37 | 47.6% |
| 11,200 (Urara-pattern, M6) | 116.05 | 70.32 | 37.0% |
| 14,000 | 141.57 | 44.81 | 23.6% |
| 18,000 | 178.02 | 8.36 | 4.4% |

---

## 2. One Piece OP-18 The Dominance of God — now $200, ACTIVE

**Cost:**
- RETAIL STAND-IN ¥5,760 (24 packs × ¥240). Hobby Search lists ¥5,781.
- Urara-pattern ¥13,200 (OP-17).

| Line | Cost ¥ | Landed | Fee @ unrounded floor | Floor |
|---|---|---|---|---|
| RETAIL STAND-IN — floor reads low (see ⚠) | 5,760 | 66.49 | 1.61 | **$75** |
| Urara-pattern (OP-17 ¥13,200) | 13,200 | 134.28 | 2.94 | **$155** |

**Comps (read 17 Oct 2026):**

| Seller | Country | URL | Price |
|---|---|---|---|
| Card Realm AUS | AU | https://cardrealmaus.com/products/bandai-one-piece-card-game-op-18-japanese-booster-box-24-packs-pre-order | A$299.95, pre-order |
| DenDenHOBBY AU | AU | https://dendenhobby.com.au/products/pre-order-one-piece-card-game-booster-op-18-japanese-version-box-of-24-packs | A$220.00, pre-order (unavailable) |
| Japan Figure | JP-based, AUD | https://japan-figure.com/en-au/products/bandai-one-piece-tcg-op-18-the-dominion-of-god-japanese-booster-box | A$388.00, pre-order |
| Trainer Town | AU | https://trainertown.com.au/products/one-piece-tcg-op-18-booster-box-sealed-case-japanese | A$1,499.95 / case of 12 (≈A$125 a box), sold out |
| Hobby Search | JP | https://www.1999.co.jp/11464772 | ¥5,781, pre-order (from search results; product page 403) |

**Comp median: A$299.95** for box listings (220.00 / 299.95 / 388.00). With Trainer Town's per-box case figure it's A$259.98.

**Recommended: $219 (change, +$19).**
- HOKO is the cheapest Japanese OP-18 box in AU by $20. $219 still undercuts the lowest domestic retailer (DenDen $220) and matches the old OP-16 pre-order price.
- At the Urara-pattern cost it lifts margin from 31.0% to 36.8%.

Margin at $200 now (fee $3.80) and at $219 (fee $4.13):

| Urara ¥ (scenario) | Landed | Margin @ $200 | Margin @ $219 |
|---|---|---|---|
| 5,760 (RETAIL STAND-IN) | 66.49 | 129.71 (64.9%) | 148.38 (67.8%) |
| 10,300 (OP-16) | 107.85 | 88.35 (44.2%) | 107.01 (48.9%) |
| 13,200 (Urara-pattern, OP-17) | 134.28 | 61.92 (31.0%) | 80.59 (36.8%) |
| 16,000 | 159.79 | 36.41 (18.2%) | 55.08 (25.1%) |
| 18,000 | 178.02 | 18.18 (9.1%) | 36.85 (16.8%) |

Breakeven at $200: ¥19,996.

---

## 3. Dragon Ball Super Fusion World FB12 Reach the God — now $165, ACTIVE

JP release 12 Dec 2026.

**Cost:**
- RETAIL STAND-IN ¥5,781 (Hobby Search; RRP ¥5,760).
- No Urara Dragon Ball history at all, so the Urara-pattern line uses ¥12,000 as an **ASSUMPTION** (≈2× RRP, the One Piece ratio).

| Line | Cost ¥ | Landed | Fee @ unrounded floor | Floor |
|---|---|---|---|---|
| RETAIL STAND-IN — floor reads low (see ⚠) | 5,781 | 66.68 | 1.61 | **$80** |
| Urara-pattern ASSUMPTION (2× RRP) | 12,000 | 123.34 | 2.73 | **$140** |

**Comps (read 17 Oct 2026):**

| Seller | Country | URL | Price |
|---|---|---|---|
| Japan Figure | JP-based, AUD | https://japan-figure.com/en-au/products/bandai-dragon-ball-super-card-game-reach-the-god-24-pack-box | A$290.00, pre-order |
| Trainer Town | AU | https://trainertown.com.au/products/dragon-ball-tcg-reach-the-god-fb12-booster-box-sealed-case-japanese | A$1,499.95 / case (count not stated; ≈A$125 a box if 12), sold out |
| Hobby Search | JP | https://www.1999.co.jp/11432046 | ¥5,781, pre-order (search results; product page 403) |
| Jump Ichiban | JP (export) | https://jumpichiban.com/en-jp/products/dragon-ball-super-card-game-fusion-world-reach-the-god-fb12-box-or-booster | ¥24,900, pre-order (export markup) |

**Comp median: NOT CHECKED, fewer than 3 AU box listings** (one AU-facing box price, A$290, plus one case listing). Searched with no Japanese FB12 box: pokebox, cardrealmaus, dendenhobby, gdgames, krystalkollectz, groovycollectables, trainertown (box).

**Recommended: $165 (keep).**
- There's no AU Japanese-box market to price against.
- $165 clears the assumed Urara-pattern floor ($140).
- The English box sells for $259–280 at local stores, so the price isn't leaving money on the table relative to buyers' alternatives.
- Revisit when Urara lists FB12.

Margin at $165 (fee $3.19):

| Urara ¥ (scenario) | Landed | Margin | Margin % |
|---|---|---|---|
| 5,781 (RETAIL STAND-IN) | 66.68 | 95.14 | 57.7% |
| 9,000 | 96.01 | 65.80 | 39.9% |
| 12,000 (ASSUMPTION, 2× RRP) | 123.34 | 38.47 | 23.3% |
| 15,000 | 150.68 | 11.13 | 6.7% |

Breakeven at $165: ¥16,222.

---

## 4. One Piece EB-05 Heroines Edition vol.2 — now $235, ACTIVE

JP release 31 Oct 2026.

**Cost:**
- RETAIL STAND-IN ¥5,760 (Bandai event price via Samurai Sword Tokyo; Amazon.co.jp snippet ¥5,782).
- Urara-pattern ¥12,200 (EB-03).

| Line | Cost ¥ | Landed | Fee @ unrounded floor | Floor |
|---|---|---|---|---|
| RETAIL STAND-IN — floor reads low (see ⚠) | 5,760 | 66.49 | 1.61 | **$75** |
| Urara-pattern (EB-03 ¥12,200) | 12,200 | 125.17 | 2.76 | **$145** |

**Comps (read 17 Oct 2026):**

| Seller | Country | URL | Price |
|---|---|---|---|
| PokeBox | AU | https://www.pokebox.com.au/products/one-piece-card-game-eb-05-heroines-edition-vol-2-booster-box-japanese | A$229.99, pre-order (available) |
| DenDenHOBBY AU | AU | https://dendenhobby.com.au/products/pre-order-one-piece-card-game-extra-booster-eb-05-japanese-version-box-of-24-packs-1 | A$250.00, pre-order (unavailable) |
| Japan Figure | JP-based, AUD | https://japan-figure.com/en-au/products/bandai-one-piece-card-game-heroines-extra-booster-pack-vol-2-box | A$267.00, pre-order |
| Trainer Town | AU | https://trainertown.com.au/products/one-piece-tcg-eb-05-booster-box-sealed-case-japanese | A$1,499.95 / case of 12 (≈A$125 a box), sold out |
| Amazon.co.jp | JP | https://www.amazon.co.jp/-/en/Bandai-Piece-Booster-Heroines-EB-05/dp/B0HB3JQ6P4 | ¥5,782 (snippet only; page 503) |

**Comp median: A$250.00** (229.99 / 250.00 / 267.00). With Trainer Town's per-box case figure it's A$240.00.

**Recommended: $235 (keep).** It's $15 under the median and $5 over PokeBox, the one AU store that can actually take an order today. Margin stays above 40% even at the Urara-pattern cost.

Margin at $235 (fee $4.41):

| Urara ¥ (scenario) | Landed | Margin | Margin % |
|---|---|---|---|
| 5,760 (RETAIL STAND-IN) | 66.49 | 164.10 | 69.8% |
| 9,000 | 96.01 | 134.58 | 57.3% |
| 12,200 (Urara-pattern, EB-03) | 125.17 | 105.42 | 44.9% |
| 15,000 | 150.68 | 79.91 | 34.0% |
| 18,000 | 178.02 | 52.57 | 22.4% |

Breakeven at $235: ¥23,769.

---

## NOT CHECKED

- Urara yen for all four: not listed as of 17 Oct 2026.
- Kanade yen: no sheet.
- Freight: A$14 is an assumption.
- GST status.
- eBay AU comps (403).
- AmiAmi / Cardrush / MTG Mate / Toyger / Card Merchant: unreachable.
- M7 JP RRP: snippet only.
- FB12 AU median: fewer than 3 listings.
- Hobby Search prices are read from search results (product pages 403).

ETHAN DECIDES:
- M7 · now $190 · rec $190 · [ ] keep [ ] change
- OP-18 · now $200 · rec $219 · [ ] keep [ ] change
- FB12 · now $165 · rec $165 · [ ] keep [ ] change
- EB-05 · now $235 · rec $235 · [ ] keep [ ] change
