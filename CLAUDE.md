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

## Tooling owner uses

- **CardUploader** — bulk-upload tool for Shopify; owner has adapted/"flipped" the same data flow to push listings to eBay too (saves duplicate data entry).
- Local Claude Code on Windows for ops + content gen (folder: `claude\hoko-collectables\`).
- Cloud Claude Code (this repo) for repo work + scheduled daily routine.

## Catalogue strategy (in progress)

- **Shopify** — sealed product + premium / graded singles (kept for margin & brand).
- **eBay** — cheap singles only; primary acquisition channel.
- **Whatnot** — on-demand live streaming when owner chooses to go live.
- **Bridge:** package inserts in every eBay order push HOKO10 + Shopify URL.
- Migration helper: `scripts/shopify/archive_cheap_singles.py` archives Shopify products under AUD $30 (reversible, dry-run by default).

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
