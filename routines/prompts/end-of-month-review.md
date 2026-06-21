# End of Month Review

**Trigger:** Last day of each month (or first working day of next month)
**Time required:** ~45-60 minutes
**Where to run:** Claude Code or as a prompted review session

This prompt generates a structured monthly business health review for HOKO Collectables.
Fill in the inputs below, then paste this whole file (including inputs) to get your review outputs.

---

## Inputs

Fill these in before running:

```
Month reviewed: [e.g. May 2026]
Revenue target for the month: $[amount]
Actual revenue for the month: $[amount]
  - eBay revenue: $[amount]
  - Shopify revenue: $[amount]
  - Whatnot revenue: $[amount]

Number of orders shipped: [count]
Number of buyback transactions completed: [count]
Buyback total paid out: $[amount]

Stock movement:
  - New stock acquired this month: [describe briefly]
  - Top 3 sellers by revenue: [list]
  - Slowest movers (in stock 30+ days): [list]

eBay metrics:
  - Feedback received this month: [count positive / count negative]
  - Any open cases or disputes?: [yes/no — if yes, describe]
  - Current TRS status: [active/at risk/lost]

Content:
  - Instagram posts this month: [count]
  - Best-performing post (by reach/engagement): [describe]
  - Videos posted (YouTube/Reels): [count]

Any major incidents, issues, or wins to flag: [describe or 'none']
```

---

## Outputs to generate

Using the inputs above, generate:

### 1. Revenue summary
- Actual vs target: AUD, and as a percentage over/under
- Platform breakdown: which channel performed best
- Month-on-month comparison (if prior month data is available in session)
- Simple commentary — what drove the result (a specific sale, slow period, restocking, etc.)

### 2. Inventory health
- Top sellers: what moved and why (if known)
- Slow movers: items 30+ days old, recommended action (price adjustment, feature in content, pull from listing)
- Buyback summary: deals completed, amount paid out, any patterns
- Stock gap assessment: categories or grades that are currently low or missing

### 3. eBay account health
- Feedback summary: ratio, any negatives and status of response
- TRS status and whether any metrics need attention
- Disputes: status of any open cases, actions needed
- Recommendation: any listing changes needed based on this month's issues

### 4. Content performance
- Post count vs goal (target from content-strategy-multichannel.md)
- Best performer: what worked and why
- Gaps: content types or themes that weren't covered
- One actionable improvement for next month

### 5. Priorities for next month
Generate a prioritised list of 5-7 actions for the coming month, e.g.:
- Restock specific categories
- Content themes to push
- Operational improvements
- Any events, card shows, or releases to prepare for
- Outstanding admin tasks

Format as a numbered list, most important first.

### 6. One-paragraph monthly snapshot
A short (100-150 word) summary of the month that could be saved as a record.
Tone: honest and direct — written by the owner for themselves, not for marketing.
Include: revenue result, standout win, standout challenge, overall mood on where the business is at.

---

## Tone notes

- This is an internal review — write it like a business owner talking to themselves
- Be honest about underperformance — don't soften bad months
- Keep recommendations specific and actionable — no vague advice
- Reference other HOKO files where relevant (e.g. 'see restock-order.md to execute the priority restock')

---

## Related files

- `routines/monthly.md` — monthly operational tasks (broader checklist)
- `routines/prompts/restock-order.md` — if restock is needed based on review
- `docs/ebay-reputation-guide.md` — if eBay metrics need attention
- `routines/prompts/pricing-update.md` — if slow movers need repricing
- `routines/prompts/content-strategy-multichannel.md` — content targets to compare against
