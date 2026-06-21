# Customer Review Request

**Trigger:** 3–5 days after dispatch confirmation (or after eBay feedback window opens)
**Use for:** eBay post-purchase follow-up (feedback request) and Shopify post-purchase (review request)

---

## Inputs

Before generating the message, confirm:

- **Platform:** eBay / Shopify
- **Product purchased:** [product name]
- **Order date:** [date]
- **Tracking shows:** Delivered / In transit / No tracking update
- **Any issues flagged by buyer?** Yes / No

> If buyer has flagged an issue — DO NOT send a review request. Go to dispute-resolution.md first.

---

## eBay — Feedback Request Message

Send via eBay's Message Centre (not feedback tool directly — buyers respond better to a personal message).

**Template:**

```
Hi [BUYER_USERNAME],

Hope your [PRODUCT_NAME] arrived safely and you're happy with it!

If everything went smoothly, I'd really appreciate it if you left feedback when you get a moment — it means a lot for a small Australian shop like ours.

If there's anything at all that wasn't right, please message me first and I'll sort it out for you.

Cheers,
Ethan
HOKO Collectables
```

**Tone notes:**
- Casual and direct — no corporate language
- One ask only — don't list all the ways they can leave feedback
- Make it easy to raise an issue — reduces risk of negative feedback
- Never ask for 5-star specifically (against eBay policy)

---

## Shopify — Review Request Message

Send via email or Shopify contact (adjust platform used as needed).

**Template:**

```
Hi [FIRST_NAME],

Just following up to make sure your [PRODUCT_NAME] arrived in good shape.

If you're happy with your purchase, a quick review on the site would be awesome — it genuinely helps other collectors find us.

And if anything wasn't right, just reply to this email and I'll fix it.

Cheers,
Ethan
HOKO Collectables
hokocollectables.com
```

**Tone notes:**
- Keep it short — buyers don't read long emails
- Don't include a review link unless your Shopify plan supports review apps with direct links
- Lead with the check-in, not the ask

---

## Timing guide

| Platform | When to send | Notes |
|----------|-------------|-------|
| eBay | 3–5 days after tracking shows delivered | Check tracking before sending — don't message if still in transit |
| Shopify | 5–7 days after dispatch | Allow time for Express Post delivery + a couple of days to open the package |
| Both | Never send if buyer has messaged about an issue | Resolve first, ask for review never (or only if buyer is happy after resolution) |

---

## When NOT to send

- Buyer has lodged a return, dispute, or "item not received"
- Tracking shows package is still in transit or delayed
- Buyer already left feedback (no need to follow up)
- International orders — add extra delivery buffer before sending

---

## Related files

- `routines/prompts/dispute-resolution.md` — if buyer has flagged an issue
- `docs/ebay-reputation-guide.md` — eBay feedback strategy and defect rate targets
- `docs/packaging-guide.md` — reducing the chance of issues that lead to negative feedback
