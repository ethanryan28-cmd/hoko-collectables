# Google Search Console Setup — HOKO Collectables

> One-time setup. Takes about 10 minutes. Free. Shows exactly which search terms are bringing people to your Shopify store.  
> Reference: docs/seo-guide.md for what to do with the data once it's flowing.

---

## Why bother

Without Search Console, you're guessing what keywords are working. With it, you can see:
- Which search terms people type to find hokocollectables.com
- Which pages rank (and for what queries)
- How many clicks vs impressions you're getting per keyword
- Any indexing errors Google has found

It's the single most useful free SEO tool available, and it takes one afternoon to set up.

---

## Step 1 — Add your property

1. Go to https://search.google.com/search-console
2. Sign in with a Google account (use the business Google account if you have one, otherwise personal is fine)
3. Click **Add property** → choose **Domain** → enter `hokocollectables.com`
4. You'll be asked to verify ownership

---

## Step 2 — Verify via Shopify (easiest method)

Google gives you a DNS TXT record to add. The quickest way to do this with Shopify:

1. Copy the TXT record value Google gives you (looks like: `google-site-verification=xxxxxxxxxxxxxxxx`)
2. In Shopify admin: **Online Store → Domains → Manage → hokocollectables.com → DNS settings**
3. Add a new TXT record with the value Google gave you
4. Back in Search Console, click **Verify**
5. DNS changes can take a few minutes to propagate — if it fails, wait 10 minutes and try again

**Alternative if DNS doesn't work:** Download the HTML verification file Google offers and upload it to your Shopify theme's root via **Online Store → Themes → Edit code** — paste the file in the root directory.

---

## Step 3 — Submit your sitemap

Once verified:
1. In Search Console left sidebar → **Sitemaps**
2. Enter: `sitemap.xml` and click Submit
3. Shopify auto-generates a sitemap at `https://hokocollectables.com/sitemap.xml` — this tells Google all your pages

If you've recently added products, resubmitting the sitemap speeds up indexing.

---

## Step 4 — What to check monthly (during weekly.md SEO step)

Once data starts flowing (usually 2-4 weeks after setup):

**Performance → Search results:**
- Filter by **Queries** — these are the actual keywords people searched
- Sort by **Clicks** descending — top keywords driving traffic
- Look for keywords with high **Impressions but low Clicks** — these are ranking but not getting clicked. Fix: improve title/meta description
- Cross-reference with docs/seo-guide.md keyword tracking table — update actual positions

**Coverage → Pages:**
- Check for any **Error** pages — these are indexed pages Google can't access. Fix them.
- Check **Excluded** section — if important product pages are excluded, investigate why

**Enhancement → Core Web Vitals:**
- Flag any pages marked as "Poor" — these hurt rankings. Usually a theme/image optimisation issue.

---

## Step 5 — Connect to Google Analytics (optional but recommended)

If you want traffic data (not just search data):
1. Set up Google Analytics 4 at https://analytics.google.com
2. In Shopify admin: **Online Store → Preferences → Google Analytics** → paste your G-XXXXXXXX tag
3. In Search Console, link to your Analytics property: **Settings → Associations → Link Google Analytics**

This lets you see which search terms lead to actual purchases, not just visits.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Verification failed | Wait 10-15 min for DNS propagation, try again |
| Sitemap shows 0 pages submitted | Check that `hokocollectables.com/sitemap.xml` loads in browser |
| No data showing after 2 weeks | Check domain is verified; check sitemap is submitted; check store isn't password-protected |
| Important pages not indexed | Submit them manually via URL Inspection tool in Search Console |

---

## Time investment

- **Setup:** ~10 minutes once
- **Monthly review:** 5-10 minutes as part of the weekly SEO audit (routines/weekly.md Step 5)
- **Payoff:** Knowing exactly which keywords to double down on and which pages need fixing
