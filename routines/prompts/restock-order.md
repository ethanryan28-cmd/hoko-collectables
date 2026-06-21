# Prompt: Restock Order Summary

Use when: you're about to contact a supplier to restock, or you've just done a stocktake and want to plan the next order. Run this to generate a structured order summary you can review before sending.

---

## Inputs (fill in before running)

```
Date: [DD/MM/YYYY]
Supplier: [name or alias — e.g. AU Wholesaler A, JP Importer B]
Budget ceiling for this order: $[X] AUD
Current stock status (list what's low or sold out):
  - [Product name]: [qty remaining] — [notes, e.g. "selling fast", "held off — price spike"]
  - [Product name]: [qty remaining] — [notes]
  - ...
Upcoming set releases in next 60 days (if any): [set name, release date]
Any customer requests or pre-order interest?: [yes — [product] / no]
Shipping lead time from this supplier: [e.g. 3-5 days / 2-3 weeks for JP orders]
```

---

## What to produce

### 1. Priority order list

Rank by: sell-through velocity + margin + upcoming demand. Format:

| Priority | Product | Qty to order | Est. cost | Reason |
|----------|---------|--------------|-----------|--------|
| 1 | [product] | [qty] | $[X] | [sold out / low stock / upcoming release demand] |
| 2 | ... | ... | ... | ... |

**Total estimated order cost:** $[X]
**Within budget?** [yes / no — if no, flag which items to cut first]

### 2. Items to hold off on

List any products that should NOT be restocked this cycle and why:
- [Product]: [reason — e.g. market price dropped, slow sell-through, supplier OOS]

### 3. Supplier message draft

A short message to send to the supplier — professional, to the point:

> Hi [supplier name/alias],
>
> Looking to restock the following — can you confirm availability and current pricing?
>
> [Item 1] — [qty]
> [Item 2] — [qty]
> [Item 3] — [qty]
>
> Prefer [payment method if known]. Let me know lead time and I'll confirm.
>
> Cheers,
> Ethan — HOKO Collectables

### 4. Pricing check reminder

Before confirming the order, check replacement cost on each item:
- [ ] Check eBay sold listings for current market price
- [ ] Compare to current Shopify list price — if market moved, update price before or immediately after restock
- [ ] Apply the replacement cost pricing rule: reprice at new cost + margin, not original purchase price

### 5. Post-order checklist

- [ ] Confirm order in writing (email/message)
- [ ] Note expected delivery date in calendar
- [ ] Prep listings in advance (draft Shopify + eBay listings so you can go live the day stock arrives)
- [ ] Update sku-watchlist.json with new quantities and updated prices when stock lands
- [ ] Post "restock incoming" social content the day before or day of arrival

---

## Pricing rules (apply to every restock)

- **Never order at a price where you can't make margin** — if current market price is at or below your cost + fees, skip the restock until market recovers
- **Replacement cost pricing:** if your new cost is higher than what you paid last time, reprice existing stock too (don't sell remaining stock at old price if it would be below replacement cost)
- **Budget discipline:** if order total exceeds ceiling, cut lower-priority items — don't go over budget on a single supplier order
