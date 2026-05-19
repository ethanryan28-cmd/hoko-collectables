# HOKO Collectables — Project Context

## Brand

- **Name:** HOKO Collectables
- **Owner / GitHub:** ethanryan28-cmd
- **Live site:** https://www.hokocollectables.com (Shopify)
- **Based:** Melbourne, Australia (founded 2024)
- **Socials:** Instagram & TikTok — `@hokocollectables`
- **Motto:** *"Collector first. Seller second."*
- **Positioning:** Collector-run (~20 yrs hobby experience), honest grading (LP means LP), transparent buybacks, careful packing, same-day dispatch.
- **Active promos:** `HOKO10` (10% off first order), free AU shipping over $100, VIP loyalty with restock early-access, 48-hr collection-quote turnaround.

## Product Domain

The live business is **TCG-focused**:

- Pokémon TCG singles
- Magic: The Gathering
- One Piece TCG
- Dragon Ball Super
- Japanese sealed product
- Mystery packs & bulk lots
- Collection buyback service

**Not** the broad figures/vintage/comics/sports-memorabilia mix shown in this repo's demo catalog.

## Sales Channels

- **eBay** — live
- **Shopify** (hokocollectables.com) — live
- **Whatnot** — planned next channel (live-stream selling)

The full operational plan / assets live on the owner's PC, not in this repo.

## This Repo

`hoko-collectables` (this repo) is a **demo / portfolio storefront** — single-page static site (`index.html` + `style.css` + `app.js`). Its 32-item hard-coded `PRODUCTS` catalog (Darth Vader figure, Millennium Falcon, Jordan rookie, etc.) does **not** reflect the real shop's TCG-singles inventory. Treat it as a sandbox unless the owner says otherwise.

### Tech state

- Vanilla JS, no build step, no framework.
- No `package.json`, no linter, no tests, no CI.
- State (`cart`, `wishlist`) persisted in `localStorage`; countdown in `sessionStorage`.
- Known bugs spotted during review (not yet fixed):
  - `app.js:322` — `$(btn).forEach(...)` uses single-element selector; this whole wishlist re-style branch throws.
  - `app.js:459` and `app.js:514` — unescaped apostrophes inside single-quoted strings (`'We'll'`, `'We're'`) → syntax errors.
  - `JSON.parse(localStorage.getItem(...))` at `app.js:55-56` is unguarded; malformed storage breaks the whole app.
  - `productCardHTML` interpolates product fields directly into HTML — safe today (hard-coded data) but an XSS surface once products come from a backend.

## Working Notes

- Use `claude/<topic>` branches (e.g. `claude/analyze-test-coverage-bF8y1`).
- Don't open PRs unless explicitly asked.
- Voice when writing copy for the brand: approachable, community-focused, trust-forward — match the "collector first" tone, not generic e-commerce hype.
