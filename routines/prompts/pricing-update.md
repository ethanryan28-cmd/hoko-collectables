# Prompt: Pricing Update (Replacement Cost Check)

Use when: you have new supplier quotes, just checked eBay comps, or have hit the 30-40% sell-through trigger on a SKU and want to reprice at current replacement cost.

---

## Inputs (fill in before running)

```
SKU or product name: [e.g. Pokemon 151 Booster Box English]
Current list price: $[X] AUD
New replacement cost (what it would cost to restock today): $[X] AUD
Target margin %: [e.g. 20%]
Selling channel(s): [Shopify / eBay / both]
Units remaining in stock: [number]
Free shipping threshold to maintain: $100 AUD
```

---

## What to produce

1. **New recommended list price** — calculated as:
   `New replacement cost / (1 - platform_fee_decimal) + postage_absorbed` then rounded to nearest $5
   - Shopify platform fee: 1.75% + $0.30
   - eBay platform fee: 13.4%
   - Postage absorbed (if free shipping applies): add ~$15-20 depending on weight

2. **Margin check** — confirm the new price covers:
   - New replacement cost
   - Platform fees
   - Postage cost (if absorbing)
   - Target margin %
   Show the maths.

3. **Price change recommendation** — one clear sentence:
   > "Raise list price from $X to $Y on [channel]. This gives [Z]% margin after platform fees and postage."

4. **Shopify Connector command** (ready to paste into Claude with Shopify Connector enabled):
   > "Update the price of [product name] to $Y.00 AUD. Show me the product first before making any changes."

5. **eBay update note** (if eBay is in scope):
   > "Log in to eBay, find [product name] listing, edit price to $Y.00. [Optional: also update quantity if stock is low.]"

---

## Pricing rules to enforce (never override)

- **Never price below replacement cost** — even if the market dipped, HOKO does not subsidise buyers from its margin
- **Never undercut market** — if new price is above current market, note it but still recommend the replacement-cost price; the moat is service not price
- **HOKO10** is for acquisition only; day-to-day pricing is at market (not HOKO10-discounted cost)
- **Buyback rates** (75-80% of FMV) are separate and not affected by this repricing exercise

---

## Example output

**Input:**
- SKU: Pokemon 151 Booster Box English
- Current list price: $180 AUD
- New replacement cost: $145 AUD
- Target margin: 20%
- Channel: Shopify (absorbing $15 postage)

**Output:**
```
Break-even = $145 / (1 - 0.0175) + $15 = $147.59 + $15 = $162.59
Target 20% margin = $162.59 x 1.20 = $195.11 → round to $195

Recommendation: Raise from $180 to $195 on Shopify.
Margin at $195: ($195 - $145 - $3.41 - $15) / $195 = $31.59 / $195 = 16.2%
(Note: 20% target not quite reached at $195 — raise to $200 for 18.4% margin, or hold at $195 if market resistance expected above that.)

Shopify Connector command:
"Update the price of Pokemon Scarlet & Violet 151 Booster Box (English) to $195.00 AUD. Show me the product first before making any changes."
```
