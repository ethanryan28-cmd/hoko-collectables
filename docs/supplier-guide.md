# Supplier Guide

How HOKO Collectables sources sealed TCG product and graded slabs. This is an internal reference — not customer-facing.

---

## Sourcing principles

- **Price at replacement cost** — what matters is what it would cost to replace the item today, not what you paid
- **Quality over volume** — better to have fewer, better items than a lot of low-margin filler
- **Never source what you can't sell** — only buy sealed and PSA/BGS/CGC slabs in categories you understand
- **Default sourcing copy:** "sourced through our regional supplier network" — only say 'direct from Japan' when Ethan has explicitly confirmed this for a specific SKU

---

## Supplier types

| Type | Pros | Cons | Best for |
|------|------|------|---------|
| Australian distributors | GST-registered, fast shipping, reliable | Higher price, limited allocation | Sealed Pok\u00e9mon, MTG, One Piece |
| Japanese wholesalers / importers | Lower cost, access to JP-exclusive product | Longer lead time, currency risk, customs | JP sealed, vintage product |
| Card show / convention dealers | Can negotiate, inspect before buying | Inconsistent, time-limited | Slabs, vintage sealed |
| Private sellers / buybacks | Best margins if priced right | Variable quality, more vetting needed | Individual slabs |
| Online marketplaces (eBay, TCGPlayer) | Wide selection | Retail pricing, no bulk discount | Fill gaps only |

---

## What to ask a new supplier

Before placing a first order, confirm:

1. **ABN / GST registration** — are they registered? Get a tax invoice with GST shown
2. **Minimum order quantity (MOQ)** — what's the smallest order they'll take?
3. **Pricing structure** — is it per unit, per case, tiered? Ask for a price list
4. **Payment terms** — upfront, 30-day net, deposit? Australian suppliers often require upfront
5. **Lead time** — how long from order to delivery?
6. **Stock availability** — do they hold stock or is it pre-order / allocation?
7. **Returns / damaged stock policy** — what happens if a box arrives damaged?
8. **Exclusivity / allocation** — for high-demand sets, ask how allocation works

---

## Red flags — avoid these suppliers

- Cannot provide a tax invoice with ABN
- No physical address or Australian presence
- Prices that are suspiciously low (undercut every competitor by 30%+) — could be counterfeit
- Reselling factory-second or refurbished sealed product without disclosure
- Offering 'exclusive' product that doesn't exist on any distributor list
- Pressure to place large orders before you've verified quality
- No clear returns policy for damaged goods
- Product arrives in generic/unmarked packaging with no documentation

---

## Authenticity checks — sealed product

Before listing any sealed product, verify:

- **Shrink wrap:** tight, even, no bubbles or peeling edges (sign of resealing)
- **Holo seal sticker** (where applicable): present, centred, not wrinkled
- **Box artwork:** matches official reference photos — check The Pok\u00e9mon Company / Wizards release details
- **Weight:** booster boxes should feel consistent — obviously light boxes are a red flag
- **Language:** confirm JP/EN/KR etc. matches what you were sold
- **Set symbol / set code:** verify against official set release list

If in doubt — do not list. Pull the item and verify before selling.

---

## Authenticity checks — slabs

All slabs must be PSA, BGS, or CGC only. Before purchasing:

- **Verify cert number** at PSA Set Registry / BGS Certification / CGC Registry before agreeing to purchase
- **Check for tampering:** case edges should be tight with no gaps; label should be flat and centred
- **Grade label:** confirm the grade shown matches what's on the registry
- **Population report:** check pop for context on the grade's rarity — relevant to pricing
- **Reject HGA, GMG, and any unrecognised graders** — HOKO does not buy or sell these

---

## Negotiation tips

- **Know your replacement cost before you negotiate** — if you don't know the market, you'll overpay
- **Lead with volume** — ask 'what's the price if I take X units?' before accepting the standard price
- **Don't reveal your resale price** — suppliers who know your margin will push for more
- **Build the relationship first** — first order at standard price; ask for better terms after you've proven you pay on time
- **Get everything in writing** — price, quantity, delivery date, condition, returns policy
- **Walk away if the numbers don't work** — a bad deal sourced cheaply is still a bad deal

---

## Pricing a new stock order

Before placing an order, run the numbers:

1. **Market price check:** what is the item selling for on eBay sold listings right now?
2. **Fee deduction:** subtract platform fees (see `docs/platform-fees.md`)
3. **Postage cost:** subtract your packaging and postage cost
4. **Target margin:** minimum 20% net on sealed; minimum 25% net on slabs
5. **Maximum buy price:** market price minus fees minus postage minus target margin = max you should pay per unit

If the supplier price is above your maximum buy price — don't order.

---

## Related files

- `docs/platform-fees.md` — fee tables and minimum viable price formula
- `routines/prompts/restock-order.md` — supplier order prompt
- `routines/prompts/pricing-update.md` — repricing when replacement cost changes
- `CLAUDE.md` — sourcing copy rules (never claim 'direct from Japan' without confirmation)
