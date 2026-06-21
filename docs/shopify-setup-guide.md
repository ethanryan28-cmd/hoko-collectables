# Shopify Setup Guide

Reference guide for HOKO Collectables' Shopify store configuration.
Covers product setup, collections, shipping, and store settings.

---

## Store Basics

- **Platform:** Shopify (Basic or Shopify plan)
- **Currency:** AUD
- **Timezone:** Melbourne (AEST/AEDT)
- **Primary market:** Australia
- **Tax:** GST inclusive pricing (10%) — display prices include GST

---

## Product Setup

### Product Types

All products fall into one of two categories post-May 2026 pivot:

| Category | Type Tag | Examples |
|---|---|---|
| Graded slab | `Graded Card` | PSA 10 Charizard, BGS 9.5 Lugia |
| Sealed TCG | `Sealed TCG` | ETBs, booster boxes, UPC |

### Product Title Format

**Slabs:** `[Game] [Card Name] [Set] [Grade] [Grader]`
Example: `Pokemon Charizard VMAX Brilliant Stars PSA 10`

**Sealed:** `[Game] [Product Type] [Set Name]`
Example: `Pokemon Elite Trainer Box Scarlet & Violet Base`

### Variants

- Slabs: Single variant (no options needed)
- Sealed: Variants for language if applicable (EN / JP)
- Never use size/colour variants for collectables

### SKU Format

See `routines/prompts/sku-generator.md` for the full SKU format.

Quick reference:
- Slabs: `[GRADER]-[GRADE]-[CARDCODE]-[LANG]` e.g. `PSA-10-CHARZRDVMAX-EN`
- Sealed: `SLD-[GAMECODE]-[SETCODE]-[LANG]` e.g. `SLD-PTG-SV01ETB-EN`

---

## Collections

Maintain these collections in Shopify:

| Collection | What Goes In |
|---|---|
| Pokemon — Graded | All PSA/BGS/CGC Pokemon slabs |
| MTG — Graded | All PSA/BGS/CGC MTG slabs |
| One Piece — Graded | All PSA/BGS/CGC One Piece slabs |
| Dragon Ball — Graded | All PSA/BGS/CGC Dragon Ball slabs |
| Pokemon — Sealed | All sealed Pokemon product |
| MTG — Sealed | All sealed MTG product |
| One Piece — Sealed | All sealed One Piece product |
| Dragon Ball — Sealed | All sealed Dragon Ball product |
| New Arrivals | Auto-collection: products created in last 30 days |

---

## Pricing Rules

- Price at replacement cost (not purchase price)
- Never undercut the current market — moat is service, not price
- Include GST in the displayed price
- Use `update_prices.py` for bulk repricing (see `scripts/shopify/README.md`)
- Minimum viable price: replacement cost + 15% buffer

---

## Shipping Settings

### Domestic (Australia)

| Order Value | Shipping Method | Rate |
|---|---|---|
| Under $100 | Australia Post tracked | Actual cost or flat $10 |
| $100–$500 | Australia Post Express + signature | Actual cost or flat $15 |
| $500+ | Australia Post Express + signature + insurance | Actual cost |

See `docs/insurance-guide.md` for shipping value thresholds and cover details.

### International

International shipping is available at buyer's risk above $200. Clearly state in listings.

---

## Inventory Management

- Track inventory for all products: ON
- Continue selling when out of stock: OFF (never oversell)
- Use `check_inventory.py` weekly to audit zero-stock active listings
- Archive listings when stock is 0 and restock is not imminent

---

## Apps to Keep

| App | Purpose |
|---|---|
| Klaviyo | Email marketing and newsletters |
| Judge.me or Stamped | Product reviews |
| Metafields Guru | Custom product fields (cert numbers, grade detail) |

---

## Monthly Checklist

- [ ] Run `check_inventory.py` — archive any zero-stock active listings
- [ ] Run `price_check.py` against current market prices
- [ ] Run `update_prices.py` if repricing is needed
- [ ] Review New Arrivals collection — remove items older than 30 days
- [ ] Check all product images are still correct and high quality
- [ ] Confirm all SKUs are correctly formatted
