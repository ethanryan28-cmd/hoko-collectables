# Platform Fees Reference — HOKO Collectables

> Quick reference for calculating net margin before pricing. Verify rates periodically — platforms change fees.  
> All rates are approximate as of mid-2026. AU GST (10%) is included where noted.

---

## 1. eBay Australia

| Fee | Rate | Notes |
|-----|------|-------|
| Final Value Fee (most categories) | 13.4% of total sale (item + postage) | Includes GST. Applies to TCG cards, sealed product |
| Final Value Fee (Cards: Sports/Pokemon etc.) | 13.4% | Same as above for TCG categories |
| PayPal / Managed Payments | Included in eBay managed payments | eBay Managed Payments replaced PayPal — no separate PayPal fee |
| eBay Store (Basic) | ~AUD $22/month | Reduces listing fees; worth it at >40 active listings |
| Promoted Listings Standard | 1-20% additional (you set) | Only charged on sale. Optional. |

**Net calculation (no promoted listings, no store):**
```
Net = Sale Price x (1 - 0.134) - Postage Cost
```

**Example — $200 sealed box, $15 postage:**
```
Sale = $200
eBay fee = $200 x 13.4% = $26.80
Postage = $15
Net = $200 - $26.80 - $15 = $158.20
```

---

## 2. Shopify

| Fee | Rate | Notes |
|-----|------|-------|
| Shopify Basic Plan | ~AUD $56/month | Standard plan most small shops start on |
| Transaction fee (Basic) | 2.0% | Charged if NOT using Shopify Payments |
| Transaction fee (Shopify Payments) | 0% | No transaction fee with Shopify Payments |
| Shopify Payments processing | 1.75% + 30c (AUS cards) | Visa/Mastercard domestic |
| Shopify Payments — Amex | 1.75% + 30c | Same rate for Amex domestic |
| Shopify Payments — international | 2.95% + 30c | For international cards |

**Net calculation (Shopify Payments, domestic card):**
```
Net = Sale Price x (1 - 0.0175) - $0.30 - Postage Cost
```

**Example — $200 sealed box, free shipping (you absorb $15 postage):**
```
Sale = $200
Shopify Payments = $200 x 1.75% + $0.30 = $3.50 + $0.30 = $3.80
Postage = $15
Net = $200 - $3.80 - $15 = $181.20
```

**Shopify vs eBay on same $200 item (absorbing $15 postage):**
- eBay: $200 - $26.80 - $15 = $158.20 net
- Shopify: $200 - $3.80 - $15 = $181.20 net
- **Shopify advantage: +$23/order** — this is why every eBay parcel has a HOKO10 + Shopify URL insert.

---

## 3. Whatnot

| Fee | Rate | Notes |
|-----|------|-------|
| Seller commission | 8% of sale price | Current standard rate |
| Payment processing | Included in Whatnot fee | No separate processing charge |
| Shipping | Buyer pays (you set flat rate) | Whatnot generates label — you pay, buyer reimburses |

**Net calculation:**
```
Net = Lot Price x (1 - 0.08) - Postage Cost
```

**Example — $50 lot:**
```
Sale = $50 | Whatnot fee = $4 | Postage = $10 | Net = $36
```

Note: Whatnot is best for moving volume at live events, not maximising per-unit margin. Audience-building compounds over time.

---

## 4. Margin Cheat Sheet

| Sale Price | eBay Net (fee only, excl. postage) | Shopify Net (fee only, excl. postage) | Whatnot Net (fee only, excl. postage) |
|-----------|-------------------------------------|---------------------------------------|---------------------------------------|
| $50 | $43.30 | $49.00 | $46.00 |
| $100 | $86.60 | $98.25 | $92.00 |
| $150 | $129.90 | $147.08 | $138.00 |
| $200 | $173.20 | $196.20 | $184.00 |
| $300 | $259.80 | $294.45 | $276.00 |
| $500 | $433.00 | $490.95 | $460.00 |

---

## 5. Postage Costs (Australia Post, approximate)

| Weight | Express Post satchel | Parcel Post (regular) |
|--------|---------------------|-----------------------|
| Up to 500g | ~$10 | ~$8 |
| Up to 1kg | ~$13 | ~$10 |
| Up to 3kg | ~$15-18 | ~$12-14 |
| 3-5kg (booster box) | ~$20-25 | ~$15-18 |

**HOKO default:** Express Post on all orders. Free AU shipping over $100 is a brand differentiator — price it into product margin, don't absorb it as loss.

**Free shipping maths:** If average order is $180 and postage costs $15, the promo costs $15/$180 = 8.3% of order value. Still cheaper than eBay's fee overhead.

---

## 6. Minimum Viable Price Formula

```
Minimum list price = Replacement cost / (1 - platform_fee) + postage_absorbed
```

**Example — box costs $120 to replace, selling on Shopify, absorbing $15 postage, targeting 20% margin:**
```
Break-even = $120 / (1 - 0.0175) + $15 = $122.20 + $15 = $137.20
Target 20% margin = $137.20 x 1.20 = $164.64 → list at $165
```

---

## 7. Review Cadence

- eBay FVF rates: check every 6 months (eBay AU typically adjusts in July).
- Shopify Payments rates: check in Shopify admin → Settings → Payments.
- Whatnot commission: check in your Whatnot seller dashboard.
