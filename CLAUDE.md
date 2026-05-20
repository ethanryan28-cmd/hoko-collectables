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

The live business is **TCG sealed + graded**. As of May 2026 HOKO pivoted to strictly sealed product and graded slabs — no new singles sourcing, no more eBay/FB lot-splitting.

**In scope (new sourcing + buybacks):**

- Pokémon TCG sealed (boxes, ETBs, booster packs, decks, promos)
- Magic: The Gathering sealed
- One Piece TCG sealed
- Dragon Ball Super sealed
- Japanese sealed product (Pokémon, One Piece, DBS, etc.)
- Graded slabs — PSA, BGS, CGC only (modern + vintage)
- Collection buyback service — **sealed + verified-grader slabs only**

**Out of scope (sell-through, do not replenish):**

- Loose singles (English or Japanese) — existing Shopify/eBay inventory sells through naturally over the coming months. No new singles added.
- Mystery packs / bulk single lots — out.
- Slabs from unverified graders (HGA, GMG, etc.) — out.

**Not** the broad figures/vintage/comics/sports-memorabilia mix shown in this repo's demo catalog.

## Sales Channels

Post sealed-only pivot:

- **Shopify** (hokocollectables.com) — primary brand storefront. Sealed product + graded slabs going forward. Existing premium singles allowed to sell through naturally.
- **eBay** — kept, pivoted to sealed + graded. Captures search-driven sealed buyers who don't shop Shopify by default. Bridge to Shopify via package inserts (HOKO10 + URL on every parcel) remains the core acquisition flow.
- **Whatnot** — planned live-stream channel. Sealed pack-rip / box-break shows make obvious sense as the live format.

The full operational plan / assets live on the owner's PC, not in this repo.

## Sourcing

All new sourcing is **sealed product + verified-grader slabs only**. No more lot-buying, no more single-card splits.

- **Japanese / Korean / Chinese sealed:** mix of direct-from-Asia imports and AU-based wholesale partners — varies per SKU. **Default copy phrasing is the safe generic:** *"sourced through our regional supplier network"* or *"imported via our wholesale partners."* Only escalate to *"direct from Japan"* (or similar) when the owner has confirmed that specific SKU is direct-import. When in doubt, ask before writing.
- **English sealed:** AU-based wholesalers + direct supplier relationships, plus opportunistic sealed lots from collection buybacks. Same default copy phrasing applies.
- **Graded slabs:** primarily acquired via collection buybacks. Always verify grader (PSA / BGS / CGC only).
- **Lot-buying on eBay / FB Marketplace is no longer the strategy.** Margin profile is now consistent (supplier-bought, predictable) — apply replacement-cost pricing (see Brand & Pricing Strategy §1).

## Brand & Pricing Strategy

Four operating principles (PokeNE, May 2026) — apply whenever pricing, restocking, or buying.

### 1. Price at replacement cost, not historical cost

When ~30-40% sold through on any SKU, check the *current* supplier or lot replacement cost before running out. If replacement rose, raise the price on remaining stock to match. Profit must cover restock, not just original purchase.

- **Asian sealed:** check supplier rate at 30% sell-through; reprice if it moved.
- **English sealed:** check wholesaler / distributor price today; reprice if the market moved.
- **Graded slabs (buyback-sourced):** check current TCGPlayer + eBay sold comps; reprice if the comp range moved.

The $20 profit on a $100 box vanishes the moment the next box costs $120.

### 2. Price at market, never undercut

HOKO10 is for customer acquisition; day-to-day pricing is at market. The moat is honest grading + same-day dispatch + buybacks + trust — not lowest price. Undercutting trains customers to expect prices that can't scale, and bigger sellers can always go lower on volume.

### 3. Collection buybacks: rigid, professional, copy-paste

Pay 75-80% of fair market value. Use a fixed intake email template every time (never freeball negotiate). Set non-negotiable rules:

- **What you buy:** factory-sealed TCG + PSA/BGS/CGC slabs valued at AUD $100+ each. No loose singles, binders, bulk, damaged sealed, slabs under $100, or unverified-grader slabs.
- **Where you meet:** local bank branch or nominated storage facility, business hours only. No home pickups, no after-hours.
- **Photo + list required** before any quote (one wide collection photo + typed inventory).
- **Quote validity:** 48 hours.
- **Payment:** bank transfer on the day. No PayPal, no cash, no instalments.

The intake email template lives at `templates/collection-buyback-intake.md` — copy-paste every time, customise only the recipient's name. Being stern signals legit operation; sellers of valuable collections prefer rigid rules.

### 3a. Consignment (future revenue pillar)

Directional intent — full launch in Phase 2 (months 4-6 of the content plan).

HOKO will offer **consignment** alongside buybacks as a second option for sellers:

- **Buyback:** outright purchase at 75-80% of FMV, paid on the day.
- **Consignment:** HOKO lists the item on its channels (Shopify, Whatnot, eBay), takes a **15-20% commission** when it sells, consignor gets paid out after the sale clears.

**Scope:** sealed product + PSA/BGS/CGC slabs $100+ only. Same constraints as buyback. No loose singles, no unverified-grader slabs.

**Why it fits:**
- Inventory flows in without HOKO laying out capital (solves the cashflow problem)
- Higher margin per hour worked (no purchase-to-list time cost)
- Two-offer pitch to sellers ("cash now at 75-80%, or wait + get 80-85% via consignment")
- Reinforces *"Collector first"* — helping collectors monetise on their own timeline

**Casual cases now, formal launch in Phase 2.** If a seller DMs with a collection that fits sealed + slabs and wants top dollar, offer consignment as the alternative. Single-page contract per item. Don't market it yet — formal launch (intake form, tracking system, marketing) waits until Whatnot + Shopify flow is proven so consignors trust HOKO to move their stuff.

**Phase 2 deliverables (not yet written):**
- `templates/consignment-agreement.md` — single-page contract template
- `templates/consignment-intake-email.md` — parallel to buyback intake
- Tracking spreadsheet schema (consignor / item / list price / sale price / commission / payout status)
- Commission structure decision (flat 20% vs sliding scale by item value)

### 4. Be platform-agnostic — own the brand

eBay, TCGPlayer, Whatnot, conventions are channels, not the business. If a customer answers "where'd you buy that?" with the platform name instead of "HOKO Collectables", that's a marketing bottleneck. Every parcel, caption, stream, and DM reinforces the brand so the audience follows when channels change.

Levers already in place: package inserts (HOKO10 + hokocollectables.com on every eBay order), motto in copy ("Collector first. Seller second."), consistent handle `@hokocollectables`, owner's regional voice in all customer comms.

## Tooling owner uses

- **CardUploader** — bulk-upload tool for Shopify; owner has adapted/"flipped" the same data flow to push listings to eBay too (saves duplicate data entry).
- **Shopify Connector for Claude (no-code)** — owner's primary path for running the store by voice from iPhone. Enabled in claude.ai → Connectors → Shopify. Gives Claude live-store write access (archive, edit products, bulk price updates, Smart Collections, Metafields).
- Local Claude Code on Windows for ops + content gen (folder: `claude\hoko-collectables\`).
- Cloud Claude Code (this repo) for repo work + scheduled daily routine.

### Shopify Connector — known limits + safety habits

- **No local image uploads** — images must be passed as public URLs. For new products with photos on the owner's phone/PC, upload to Shopify Files first or use a CDN, then reference the URL.
- **Bulk-destructive actions** (price changes, archives, deletes): always ask Claude to *"show me one example first, don't execute yet."* Approve the dry-run, then say *"go ahead."* This pattern prevents catalogue-wide mistakes.
- **Claude Code + Shopify plugin** exists as a deeper path (theme edits, SEO audits, conversion reports, AOV bundle analysis). Owner is not using it yet — only add when a specific need surfaces.

## Catalogue strategy (post sealed-only pivot)

- **Shopify** — sealed product + PSA/BGS/CGC slabs **only**. As of the sealed-only pivot, **all singles get archived** (not just cheap ones) — the site goes 100% sealed + slabs immediately, not via slow sell-through. Existing singles inventory moves via the Whatnot liquidation stream + eBay sell-through.
- **eBay** — sealed + slabs. The bridge (HOKO10 + Shopify URL insert in every parcel) remains the acquisition flow. Existing singles sell through then the channel is sealed-only.
- **Whatnot** — sealed pack-rip / box-break shows when owner goes live.
- **Bridge:** package inserts in every eBay order push HOKO10 + Shopify URL.
- **Pivot helper:** preferred path is voice-driven via Shopify Connector (*"Show me every product that is NOT a sealed box, ETB, pack, deck, sealed accessory, or graded slab. Don't change anything."* → review → *"Archive all of them."*). The legacy `scripts/shopify/archive_cheap_singles.py` script remains in the repo for the narrower sub-$30 use case but is **not** the primary tool for the all-singles archive.

## This Repo

`hoko-collectables` (this repo) is a **demo / portfolio storefront** — single-page static site (`index.html` + `style.css` + `app.js`). Its 32-item hard-coded `PRODUCTS` catalog (Darth Vader figure, Millennium Falcon, Jordan rookie, etc.) does **not** reflect the real shop's TCG sealed + slab inventory. Treat it as a sandbox unless the owner says otherwise.

### Tech state

- Vanilla JS, no build step, no framework.
- No `package.json`, no linter, no tests, no CI.
- State (`cart`, `wishlist`) persisted in `localStorage`; countdown in `sessionStorage`.
- Known bugs spotted during review (not yet fixed):
  - `app.js:322` — `$(btn).forEach(...)` uses single-element selector; this whole wishlist re-style branch throws.
  - `app.js:459` and `app.js:514` — unescaped apostrophes inside single-quoted strings (`'We'll'`, `'We're'`) → syntax errors.
  - `JSON.parse(localStorage.getItem(...))` at `app.js:55-56` is unguarded; malformed storage breaks the whole app.
  - `productCardHTML` interpolates product fields directly into HTML — safe today (hard-coded data) but an XSS surface once products come from a backend.

## Content Strategy

Target: **~3 IG/TikTok posts per day**, ~30 seconds of owner time per post, via 3 daily phone photos + voice-dumped context.

### 5 content pillars (rotate)

| Pillar | What it looks like | Weekly target |
|---|---|---|
| **The Pull** | Pack opens, hits | 2x |
| **The Drop** | Restocks (especially Japanese sealed), new arrivals | 2x |
| **The Story** | Packing, sourcing, behind-the-scenes | 2x |
| **The Tip** | Grading / fakes / collecting advice | 1x |
| **The Hit-list** | Market commentary, trending sets | 1x |

### Daily workflow

1. 3 phone photos.
2. Voice-dump 30s of context per photo into Claude mobile.
3. Claude returns per photo: IG caption + hashtags, TikTok hook, story idea, suggested pillar.
4. Owner schedules via Meta Business Suite / TikTok Studio.

**Hard rule:** never post on owner's behalf. Always hand drafts back for approval.

## Working Notes

- Use `claude/<topic>` branches (e.g. `claude/analyze-test-coverage-bF8y1`).
- Don't open PRs unless explicitly asked.
- Voice when writing copy for the brand: approachable, community-focused, trust-forward — match the "collector first" tone, not generic e-commerce hype.

## Voice Intake Protocol

The owner often dumps raw voice transcripts (via Whisper Flow, Claude mobile, or phone dictation) instead of typing — speaking is ~3× faster than typing and lets him capture ideas while away from his PC.

When you receive a raw transcript-style dump (rambling, half-sentences, multiple topics mixed together, no formatting):

1. **Extract, don't invent.** Pull out only what he actually said. Never fabricate card names, prices, dates, or details he didn't mention.
2. **Categorise** the contents into any of these buckets that apply:
   - Listings to draft (eBay or Shopify)
   - Social posts (IG caption / TikTok script)
   - Whatnot show ideas / prep
   - Customer DMs or replies to draft
   - Pricing or buyback decisions
   - Restock / inventory notes
   - To-dos / reminders
   - Strategic thoughts (file, don't action)
3. **Produce structured output** — one section per bucket, with concrete drafts where possible. Use the Reference Prompts above (eBay listing, Shopify sealed, social caption, Whatnot show, package insert) as templates.
4. **Ask only for truly missing info** — never block on details he can fill in later. If a price or condition isn't mentioned, leave a `[FILL IN: price]` placeholder and keep going.
5. **End with a tight to-do list** — what he should review/approve when he's back at his PC.

**Output destination (when in a Claude Code session with GitHub MCP):** create one GitHub issue per bucket, tagged `voice-dump`. Title format: `[voice-dump] <category> — <date>`. Body contains the structured drafts. Owner is on iPhone and reviews on the GitHub mobile app.

**Phone setup the owner uses:** iPhone with either (a) Whisper Flow for system-wide dictation, or (b) Claude.ai mobile / Claude Code web in Safari with native iOS dictation. Both produce raw transcripts that follow this protocol.

Match his tone in any drafts: collector-to-collector, honest, AU English, no marketing hype.

## Daily Routine

A scheduled Claude Code session runs `routines/daily.md` once per day. Output lands in `reports/YYYY-MM-DD.md` on `main`.

Sub-routines:
1. Brand & SEO scan (WebSearch — works today)
2. Competitor pricing (needs `routines/sku-watchlist.json` populated)
3. Sales/inventory snapshot (needs Shopify + eBay env vars — see step 3 of routine)
4. Listing freshness (sitemap probe — works today; eBay portion needs creds)

### Web UI setup (one-time, owner does this)

1. Open environment in https://claude.ai/code → Triggers → **Add scheduled trigger**
2. Schedule: daily at 8:00 AM AEST (or preferred time)
3. Source: this repo, branch `main`
4. Prompt: `Read and execute routines/daily.md`
5. Environment variables (under env config, not in repo): `SHOPIFY_STORE`, `SHOPIFY_ADMIN_TOKEN`, `EBAY_APP_ID`, `EBAY_CERT_ID`, `EBAY_DEV_ID`, `EBAY_USER_TOKEN`
6. Network policy: needs outbound to `hokocollectables.com`, eBay APIs, Google (for WebSearch)

Docs: https://code.claude.com/docs/en/claude-code-on-the-web
