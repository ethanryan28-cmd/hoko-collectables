# HOKO Weekly Routine

Run once per week (suggested: Monday morning AEST). Deeper audit than the daily routine.
Output: append a weekly section to the current month's notes or open GitHub issues for anything actionable.

Same rules as daily.md:
- Be concise. Bullet points, not prose.
- If a step can't run (missing credentials, site down): say so and move on.
- Never fail the whole routine for one missing step.
- Open GitHub issues labelled "weekly-review" for anything actionable.

---

## Step 1 - Competitor deep scan

1. Run Google searches for each major competitor from the latest daily report.
2. Check their store for: new sealed sets added this week, price changes on SKUs in routines/sku-watchlist.json, any promotions or bundles.
3. Flag: if a competitor drops below HOKO's price on a watchlist SKU, note it. Do not undercut - note for owner awareness only.
4. Check if any new AU TCG sealed competitors have appeared (new eBay stores, Reddit mentions).

Competitors to watch: PokéBox AU, TrainerHub, The Wandering Collector, Collectable Cartel, JToys, Ronin Games, Pocket Games AU, Alpha Gaming.

---

## Step 2 - YouTube channel audit

1. Fetch @HokoCollectables YouTube channel.
2. Note: total video count, subscriber count, most recent upload date and title, view counts on last 3 uploads.
3. Flag: are video titles searchable? (include set name + "Australia" + "booster box")
4. Flag: thumbnails - do they include text overlay with set name?
5. Recommend one specific title/thumbnail improvement if needed.

---

## Step 3 - eBay feedback + reputation check

1. Fetch HOKO eBay feedback (last 30 days).
2. Note: total feedback count, positive %, any negative/neutral feedback this week.
3. Flag: any negative feedback requires owner review immediately.

---

## Step 4 - Shopify catalogue health

Requires SHOPIFY_STORE and SHOPIFY_ADMIN_TOKEN env vars.
If not set: skip and note "Credentials not configured - skipping Shopify check."

If set:
1. Pull all active products.
2. Check for: products with no description, no images, price = $0 or > $10,000, 0 inventory still "active".
3. Flag any anomalies.

---

## Step 5 - SEO ranking check

1. Search Google for:
   - "pokemon TCG sealed australia" - is HOKO on page 1?
   - "one piece TCG sealed australia" - same
   - "graded pokemon card australia" - same
   - "[most recent new sealed set] australia buy" - is HOKO indexed?
2. Note positions (or "not page 1") for each query.
3. Flag: if HOKO drops off any query it was previously ranking on, escalate.

---

## Step 6 - Social media snapshot

1. Check Instagram @hokocollectables: follower count, posts last 7 days (target: 10+ posts), any DMs that look like buyback/consignment inquiries.
2. Check TikTok @hokocollectables: follower count, videos posted this week, any high-view videos (>1,000 views).
3. Flag: if no posts in last 7 days, note as inactive.

---

## Step 7 - Buyback + consignment pipeline review

1. Are there any open buyback quotes (sent but not yet accepted)?
2. Are there any active consignment items (listed, awaiting sale)? Reference routines/consignment-tracking-schema.md.
3. Any consignment items over 90 days unsold? Flag for owner to contact consignor.
4. Any payout due (sold-unpaid status)? Flag immediately.

---

## Step 8 - SKU watchlist update

1. For each SKU in routines/sku-watchlist.json: re-run eBay AU sold listing search for last 7 days.
2. Update market price if moved >5% since last update.
3. Commit updated sku-watchlist.json to main: "Weekly SKU watchlist update YYYY-MM-DD"

---

## Report format

Save to reports/YYYY-MM-week-N.md (e.g. reports/2026-06-week-4.md). Commit to main.

# HOKO Weekly Review - YYYY-MM-DD

## Headlines (1-3 bullets)
## Competitor scan
## YouTube audit
## eBay reputation
## Shopify catalogue health
## SEO rankings
## Social media snapshot
## Buyback/consignment pipeline
## SKU watchlist changes
## Issues opened

Open GitHub issues labelled "weekly-review" for anything requiring owner action.
