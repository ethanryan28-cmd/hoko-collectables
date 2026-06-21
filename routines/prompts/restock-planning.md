# Restock Planning — Prompt

Use this prompt to plan a restock run from suppliers.
Run it monthly or when stock falls below minimum levels.

---

## Inputs to Gather Before Running

| Input | Example |
|---|---|
| Current stock summary | 3 ETBs, 2 PSA 10 slabs |
| Recent sell-through | 5 ETBs, 3 slabs in last 30 days |
| Available budget | $2,000 AUD |
| Current market prices | SV ETB ~$70, PSA 10 Charizard ~$300 |
| Supplier availability | Japan stock confirmed, local TBA |
| Games in demand | Pokemon, One Piece |
| Upcoming events | Melbourne Card Show in 3 weeks |

---

## The Prompt

```
You are helping Ethan from HOKO Collectables plan a restock run.
HOKO sells PSA/BGS/CGC graded slabs and sealed TCG product (Pokemon, MTG, One Piece, Dragon Ball Super).
HOKO prices at replacement cost and never undercuts the market.

Plan a restock order based on the following:

Current stock: [SUMMARY]
Recent sell-through (last 30 days): [SUMMARY]
Budget: [AMOUNT AUD]
Market prices: [KEY PRICES]
Supplier availability: [NOTES]
Games in demand: [LIST]
Upcoming events: [LIST OR NONE]

Output:
1. RESTOCK PRIORITY LIST (top 5-10 items, ranked by sell-through and demand)
2. ESTIMATED COST per item (at replacement cost)
3. TOTAL ESTIMATED SPEND (within budget)
4. SUPPLIER RECOMMENDATION per item (which type of supplier to approach)
5. TIMING NOTE (order now vs wait — based on market conditions)

Rules:
- Only recommend PSA, BGS, CGC graded slabs — no HGA, GMG, unverified graders
- Only recommend sealed product HOKO currently carries (Pokemon, MTG, One Piece, Dragon Ball Super)
- Do not recommend singles or loose cards
- Price estimates should reflect current AUD replacement cost, not historical cost
- Flag any items where market is volatile or prices are unclear
```

---

## Restock Priorities

When deciding what to restock, consider:

**High priority:**
- Items with 0 stock that have had recent enquiries
- Items that sell within 7 days of listing
- Core Pokemon sealed (ETBs, booster boxes) — always in demand

**Medium priority:**
- Items with 1-2 units left
- Seasonal items (pre-event stock, new set releases)

**Low priority:**
- Slow-moving lines (30+ days on shelf)
- Items where market price has dropped significantly

---

## Budget Allocation Guide

| Category | Suggested Allocation |
|---|---|
| Pokemon sealed | 50-60% |
| MTG sealed | 10-20% |
| One Piece sealed | 10-15% |
| Dragon Ball sealed | 5-10% |
| Graded slabs (buyback) | Remaining |

Adjust based on what's actually selling that month.

---

## Sourcing Reminder

See `docs/supplier-guide.md` for supplier evaluation criteria.
Default sourcing copy: "sourced through our regional supplier network".
Only use "direct from Japan" if Ethan has confirmed for the specific SKU.
