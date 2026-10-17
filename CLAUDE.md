# HOKO Collectables — Project Context (canon, 17 Oct 2026)

## Brand

- **Name:** HOKO Collectables · **Owner / GitHub:** ethanryan28-cmd · **Live site:** https://www.hokocollectables.com (Shopify)
- **Based:** Victoria, Australia. Write it exactly that way, never the capital city's name.
- **Selling since 2023.** Proof line: "Selling since 2023 · 1.5K sold, 100% positive on eBay" (re-check the eBay count before using a number).
- **Tagline:** *"Collector first. Seller second."*
- **Six games, always this order:** Magic · Pokémon · One Piece · Lorcana · Gundam · Dragon Ball Super
- **Socials:** Instagram `@hoko.collectables` · TikTok / YouTube / Pinterest `@hokocollectables` · Discord https://discord.gg/4eFCy5YPFU · eBay https://www.ebay.com.au/str/hokocollectables
- **Support:** support@hokocollectables.com · ABN 25 308 780 156
- **Voice:** collector-to-collector, honest, AU English, no hype. Honest grading: LP means LP.

## What HOKO sells

- **Singles are core.** List / post / ship singles across all six games every week. English and Japanese.
- **Japanese sealed is the push.** Booster boxes imported from Japan by HOKO (supplier Urara.Chii; copy says "imported from Japan by HOKO" or "direct from our Japanese distributor"). Line to use everywhere: **"Dispatched tracked from Victoria within 2–4 business days once it lands."**
- **Pre-orders** on the newest Japanese sets (live 17 Oct 2026: EB-05, OP-18, M7 Aura Seeker, FB12; M6a is the newest live Pokémon box). Pre-order line: **"Pre-order — dispatched tracked from Victoria once it lands."**
- **Newest sets only, every game:** supplier orders, pre-orders, content and homepage all point at the newest release per game; older boxes stay live untouched. The five newest are `hot_sets` in `content/youtube/config.json` and take ≥60% of the social queue.
- **Graded slabs:** PSA, BGS, CGC only. Every slab is one item; photograph the exact copy.
- **Buying:** sealed, PSA/BGS/CGC slabs ($100+ each) and premium singles ($25+), Australia-wide, 70–85% of eBay last-sold. Quote form on `/pages/sell-your-cards`. Consignment at 70% to the seller via `/pages/consign-your-cards`.

## Words that are banned in anything customer-facing

Never write: the name of the live-auction app HOKO left in 2026 (the W-word), eBay's seller-tier badge phrase ("Top R…"), "myst… pack" / repack language, **"official"**, **"same-day dispatch"**, the capital city's name (say Victoria), or **"1.4K"**. No prices in social captions. No handle changes.

## Operating lines (copy these verbatim)

- Dispatch: **"Dispatched within 1–3 business days"** (singles and slabs). Japanese sealed: the 2–4 business days line above.
- Condition scale: **NM · LP · MP · HP · DMG**.
- Postage (Australia):
  - singles under $50: **$3 untracked letter**
  - singles $50+ and slabs: **$10.95 tracked, free tracked at $150+**
  - sealed boxes: **$15.25 tracked, free on sealed orders of $250+**
- Postage (international, singles, signature required): **NZ / Asia-Pacific $25 · US / Canada / UK-EU $35 · rest of world $40**.
- Returns: **7 days, not-as-described only. Sealed and international orders are final sale.** Australian Consumer Law rights unaffected.
- Discount codes that exist (read from Shopify 17 Oct 2026, list them and nothing else):
  - `WELCOME10` — 10% off the discount-eligible collection, once per customer, active
  - `THANKS10` — 10% off the discount-eligible collection, active
  - `BFDROP5` — $5 off Japanese sealed, once per customer, scheduled 27–30 Nov 2026
  - Black Friday automatics, scheduled 27–30 Nov: 10% off singles under $100 (discount-eligible), free AU postage on orders $100+
  - The old welcome code ending in "10" that package inserts used to carry no longer exists; use `WELCOME10`.

## Channels

- **eBay is the source of truth** for inventory and prices. **Shopify is the premium storefront.** No outbound sync yet (eBay API keys pending); `tools/relist-reconcile.py` reconciles exports by hand.
- Package inserts in every eBay order carry the Shopify URL and the live welcome code.
- Social: `tools/social/` posts a 14-day queue to Instagram, Facebook, YouTube Shorts, Pinterest and Discord, and packages TikTok clips for the phone. Content comes from `content/youtube/`.

## Hard rules for agents

- **Pricing, discounts, promos, markdowns are Ethan's.** Never create, edit, schedule or delete one. Report, don't act. Prices are Ethan's — no agent price change without his number.
- **eBay offers:** capped at 5%, and only if Ethan sets them.
- **Never bulk relist** without reconciling against inventory. **Never end, relist or delete listings.**
- **Never touch payments, billing or banking.** Never change a marketplace category or a social handle.
- **Bulk Shopify content writes:** backup CSV to `reports/backups/` first · batches of 250, sequential · read every row back and compare before calling it done · a content job never writes price, inventory, status or order fields.
- **Themes:** publishing is Ethan's click. Stack theme edits into the open draft theme; never write to MAIN.
- Shopify connector habit for anything bulk-destructive: show one example first, then run.

## Run protocol

- Every CC prompt opens with **"Go."** and a from-Ethan line. Read `QUEUE.md` first.
- Work on a `claude/<topic>` branch. Don't open PRs unless asked.
- One report file per run (`REPORT-<ISO date>.md`): PASS/FAIL per step, failures with IDs and errors, **NOT CHECKED**, **MANUAL** (PC-only vs Ethan-only), then `## COMPLETE`. Update `QUEUE.md` (newest first).
- A failed gate is the only reason to stop an unattended run. A Shopify write refused by the permission guard is logged as MANUAL and the run continues.

## Repo map

- `index.html`, `style.css`, `app.js` — demo storefront only (hard-coded sandbox catalog, not the real shop).
- `content/youtube/` — content machine: reels, Shorts, calendar, cutoff. `config.json` holds lead time and the Christmas cutoff.
- `tools/social/` — auto-poster (see its README). `tools/relist-reconcile.py` — eBay/Shopify reconcile.
- `routines/` — scheduled prompts (daily, weekly) and reusable prompt templates. `templates/` — intake / listing templates.
- `docs/` — current guides. `docs/archive/` — pre-pivot material, not canon.
- `reports/` — run reports and `reports/backups/` (before-copies of every bulk write).

## Voice Intake Protocol

The owner often dumps raw voice transcripts (via Whisper Flow, Claude mobile, or phone dictation) instead of typing — speaking is ~3× faster than typing and lets him capture ideas while away from his PC.

When you receive a raw transcript-style dump (rambling, half-sentences, multiple topics mixed together, no formatting):

1. **Extract, don't invent.** Pull out only what he actually said. Never fabricate card names, prices, dates, or details he didn't mention.
2. **Categorise** the contents into any of these buckets that apply:
   - Listings to draft (eBay or Shopify)
   - Social posts (IG caption / TikTok script)
   - Customer DMs or replies to draft
   - Pricing or buyback decisions
   - Restock / inventory notes
   - To-dos / reminders
   - Strategic thoughts (file, don't action)
3. **Produce structured output** — one section per bucket, with concrete drafts where possible. Use the prompts in `routines/prompts/` (eBay listing, Shopify sealed, social caption, package insert) as templates.
4. **Ask only for truly missing info** — never block on details he can fill in later. If a price or condition isn't mentioned, leave a `[FILL IN: price]` placeholder and keep going.
5. **End with a tight to-do list** — what he should review/approve when he's back at his PC.

**Output destination (when in a Claude Code session with GitHub MCP):** create one GitHub issue per bucket, tagged `voice-dump`. Title format: `[voice-dump] <category> — <date>`. Body contains the structured drafts. Owner is on iPhone and reviews on the GitHub mobile app.

**Phone setup the owner uses:** iPhone with either (a) Whisper Flow for system-wide dictation, or (b) Claude.ai mobile / Claude Code web in Safari with native iOS dictation. Both produce raw transcripts that follow this protocol.

Match his tone in any drafts: collector-to-collector, honest, AU English, no marketing hype.

## Daily Routine

A scheduled Claude Code session runs `routines/daily.md` once per day. Output lands in `reports/YYYY-MM-DD.md` on `main`.

A scheduled Claude Code session also runs `routines/weekly.md` once per week (suggested: Monday 8am AEST). Output lands in `reports/YYYY-MM-week-N.md` on `main`.

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
