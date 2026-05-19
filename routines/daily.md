# Daily Routine — HOKO Collectables

You are a scheduled Claude Code session running for HOKO Collectables. Read `CLAUDE.md` first for brand context, then execute the four sub-routines below.

**Rules**
- Be concise. Bullet points, not prose.
- Run independent steps in parallel.
- If a step can't run (missing credentials, site down), say so and move on — never fail the whole routine.
- Write one combined report to `reports/YYYY-MM-DD.md`. Commit and push to `main`. If anything is actionable (stock-out, bad review, broken listing), also open a GitHub issue labelled `daily-alert`.
- Keep the final report under one page.

---

## 1. Brand & SEO scan

Use `WebSearch` for each of these queries and note anything new vs the previous day's report:

- `"Hoko Collectables"` — general mentions, news, reviews
- `"Hoko Collectables" site:reddit.com` — community chatter
- `"Hoko Collectables" site:youtube.com` — video mentions / unboxings
- `"Hoko Collectables" review` — sentiment
- `Pokemon singles Australia` — where do we rank?
- `One Piece TCG Australia` — same

Flag:
- New negative reviews or complaints
- New competitor activity in AU TCG space
- Ranking drops on key queries

---

## 2. Competitor pricing

Read `routines/sku-watchlist.json` for the SKUs to monitor. If the file is missing or empty, note that and skip with a one-line "owner to populate watchlist" message.

For each SKU:
- `WebFetch` eBay completed/sold-listings page
- Report median sold price (AUD) over last 30 days
- Compare to Shopify price from `routines/shopify-prices.json` if present
- Flag any SKU where Shopify price is >15% above or below market median

---

## 3. Sales / inventory snapshot

Requires environment variables (set in Claude Code environment config, not in repo):

- `SHOPIFY_STORE` — e.g. `hokocollectables.myshopify.com`
- `SHOPIFY_ADMIN_TOKEN` — Shopify Admin API access token
- `EBAY_APP_ID`, `EBAY_CERT_ID`, `EBAY_DEV_ID`, `EBAY_USER_TOKEN`

**If any required var is unset:** print `Credentials not configured — skipping.` and move on. Do not fail.

**If set:**
- Pull Shopify orders from last 24h via Admin API (`/admin/api/2024-10/orders.json?status=any&created_at_min=...`)
- Pull eBay sales from last 24h via Trading API or Sell API
- Report: total revenue (AUD), unit count, top 5 SKUs by units sold
- Pull current inventory levels; flag SKUs at 0 or below threshold (default 2 units)

---

## 4. Listing freshness check

- `WebFetch` `https://www.hokocollectables.com/sitemap.xml`
- Sample 10 product URLs at random
- For each: confirm HTTP 200, page has a title, price, and at least one image reference
- Flag any 404, redirect loop, or missing core element

Once eBay creds are configured (step 3):
- List active eBay listings ending in next 24h with zero bids/watchers — candidates for relist or price adjustment

---

## Report format

```markdown
# HOKO Daily Report — YYYY-MM-DD

## Headlines
- 1–3 bullets — the things owner should see first

## Brand & SEO
...

## Competitor pricing
...

## Sales & inventory
...

## Listing freshness
...

## Actions opened
- #123 Stock-out: <SKU>
- #124 Stale listing: <eBay item id>
```
