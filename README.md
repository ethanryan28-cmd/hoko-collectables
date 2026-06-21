# HOKO Collectables

> **Collector first. Seller second.**
> Melbourne-based TCG sealed product + graded slab shop. Founded 2024 by Ethan, ~20 years collecting experience.
> Live store: [hokocollectables.com](https://www.hokocollectables.com)

---

## About This Repo

This repository is a **demo / sandbox storefront** and also contains the **operational docs and automation routines** that run the real business.

The 32-item hard-coded demo catalogue (action figures, vintage toys, comics, sports memorabilia) does **not** reflect the real HOKO shop inventory. The live business is TCG sealed product + PSA/BGS/CGC graded slabs only.

---

## The Real Business (post May 2026 pivot)

HOKO now sells strictly:

- Pokemon TCG sealed: booster boxes, ETBs, packs, Japanese imports
- Magic: The Gathering sealed
- One Piece TCG sealed (English + Japanese)
- Dragon Ball Super TCG sealed
- Graded slabs: PSA, BGS, CGC only (modern + vintage)

Out of scope: loose singles, mystery packs, HGA/GMG slabs.

Buyback service: 75-80% FMV for sealed + PSA/BGS/CGC slabs $100+. Bank transfer on the day. Quote within 48 hours.

---

## Operational Docs

| File | Purpose |
|------|--------|
| CLAUDE.md | Full project context, brand rules, working instructions |
| routines/daily.md | Scheduled daily routine (brand scan, competitor pricing, listing freshness) |
| routines/sku-watchlist.json | SKU watchlist with market price targets |
| routines/shopify-prices.json | Current Shopify price snapshot for daily comparison |
| routines/consignment-tracking-schema.md | Phase 2 consignment tracking schema |
| routines/content-strategy-multichannel.md | Multi-channel content strategy |
| templates/collection-buyback-intake.md | Buyback intake email template |
| templates/consignment-agreement.md | Phase 2 consignment contract |
| templates/consignment-intake-email.md | Phase 2 consignment intake email |
| reports/ | Daily routine reports, one file per day |

---

## Demo Site Features

- Product Catalogue: 32 demo items with badges
- Shopping Cart: persisted in localStorage
- Wishlist: heart toggle, persisted in localStorage
- Category Filtering, Sort Options, Live Search
- Load More Pagination (batches of 8)
- Countdown Timer (session-based)
- Scroll-Reveal Animations (Intersection Observer)
- Hero Parallax (mousemove)
- Newsletter and Contact Forms with toast feedback
- Responsive Design: mobile-first

---

## Project Structure

hoko-collectables/
├── index.html          # Demo single-page storefront
├── style.css           # Dark-theme design system
├── app.js              # Cart, search, animations
├── CLAUDE.md           # Project context + Claude working rules
├── routines/           # Operational docs + automation
├── templates/          # Customer-facing document templates
├── scripts/            # Utility scripts (Shopify, eBay)
└── reports/            # Auto-generated daily reports

---

## Design System

| Token | Value | Usage |
|-------|-------|-------|
| --primary | #c0392b | Buttons, accents, badges |
| --dark | #1a1a2e | Page background |
| --card-bg | #1e2240 | Product and category cards |
| --font-serif | Playfair Display | Headings |
| --font-sans | Inter | Body + UI |

---

## Running the Demo Locally

git clone https://github.com/ethanryan28-cmd/hoko-collectables.git
cd hoko-collectables
open index.html

Or: python -m http.server 8000

---

## Sales Channels

| Channel | Purpose |
|---------|--------|
| hokocollectables.com | Primary Shopify storefront |
| eBay | Search-driven sealed + slab buyers |
| Whatnot | Planned live-stream box-break shows |
| Instagram / TikTok | @hokocollectables content |
| YouTube | @HokoCollectables pack opens |

---

(c) 2026 HOKO Collectables. All rights reserved.
