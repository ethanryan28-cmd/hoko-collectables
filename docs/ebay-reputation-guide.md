# eBay Reputation Guide

How HOKO Collectables protects and grows its eBay seller reputation. Updated for 2026.

---

## Why reputation matters

eBay's algorithm heavily weights seller metrics when ranking listings. A seller with Top Rated status and high feedback gets significantly more visibility than an identical listing from a lower-rated seller. For a small shop like HOKO, this is a meaningful competitive advantage — especially in the graded slab and sealed TCG categories where buyers have multiple options.

---

## Key metrics and targets

| Metric | eBay threshold | HOKO target | Check frequency |
|--------|--------------|-------------|-----------------|
| Transaction defect rate | < 2% | < 0.5% | Monthly |
| Cases closed without seller resolution | < 0.3% | 0% | Monthly |
| Late shipment rate | < 10% | < 2% | Monthly |
| Tracking uploaded on time | > 95% | 100% | Weekly |
| Positive feedback % | n/a (shown to buyers) | > 99% | Monthly |

> Check these in **Seller Hub > Performance > Service metrics** monthly.

---

## Top Rated Seller requirements (Australia)

To qualify for eBay Top Rated Seller (TRS) status:

- Active eBay member for at least 90 days
- Minimum 100 transactions and $1,000 AUD in sales in the past 12 months
- Transaction defect rate ≤ 0.5%
- Cases closed without seller resolution ≤ 0.3%
- Late shipment rate ≤ 3%
- Tracking uploaded within handling time on ≥ 95% of transactions

TRS gives you:
- Top Rated badge on listings (builds buyer trust)
- Improved search placement
- Access to Top Rated Plus listings (extra discount + badge on listing)

---

## Defect rate — what causes it

A defect is recorded when:
1. A transaction is cancelled by the seller (avoid this entirely)
2. A buyer opens a case for "item not received" or "item not as described" and it is closed without seller resolution (i.e., eBay intervenes in buyer's favour)

**How to avoid defects:**
- Never cancel an order once confirmed — only cancel if buyer requests it
- Respond to all "item not received" cases within 3 business days
- For INR cases: check tracking first; if genuinely lost, offer refund or replacement immediately — do not let eBay close it
- For INAD cases: see `routines/prompts/dispute-resolution.md` for resolution process

---

## Feedback management

### Building positive feedback
- Send post-purchase follow-up messages (see `routines/prompts/customer-review-request.md`)
- Include a HOKO10 insert in every package — it creates goodwill
- Pack well — damaged arrivals are the #1 cause of negative feedback for collectables
- Ship same day or next day — buyers notice and mention it in feedback

### Responding to negative feedback
- Always respond to negative feedback publicly — calmly and professionally
- Do not argue or be defensive — future buyers read these responses
- If the negative was clearly unjustified (e.g., buyer left negative for a postal delay), state the facts briefly
- Example response: *"Sorry to hear the parcel was delayed — this was outside our control. We shipped same-day with tracking and offered a resolution immediately. Happy to help further."*
- You can request feedback revision if the issue was resolved to buyer's satisfaction (eBay allows one revision request per feedback)

### Feedback revision request — when to use
- Buyer left negative or neutral feedback but issue was resolved
- Do not use it as a pressure tactic — only reach out if buyer is genuinely satisfied
- Message: *"Hi [username], glad we were able to sort that out for you. Would you be open to revising your feedback? No pressure at all — just helps a small Aussie shop like ours. Cheers, Ethan"*

---

## Handling disputes — quick guide

| Dispute type | First step | Target resolution |
|-------------|-----------|-------------------|
| Item Not Received (INR) | Check tracking; if delivered, send tracking proof | Within 3 days |
| Item Not As Described (INAD) | Acknowledge, ask for photo proof | Within 3 days |
| Return request | Accept if within policy; arrange return label if needed | Within 3 days |
| Negative feedback | Respond publicly, calmly | Within 24 hours |
| Payment dispute (chargeback) | Respond with tracking + order details | Immediately |

> For full dispute handling process: `routines/prompts/dispute-resolution.md`

---

## Shipping — staying on time

Late shipment rate is easy to keep clean with a simple habit:

- Set handling time to **1 business day** in all listings
- Ship every weekday — batch any weekend orders for Monday dispatch
- Upload tracking **on the same day you ship** — eBay records tracking upload time, not delivery time
- Use Australia Post Express Post with MyPost Business for all domestic — tracked and eligible for next-day in metro areas

---

## Listing accuracy — preventing INAD claims

Most INAD claims happen because the listing didn't match what arrived. For HOKO specifically:

- **Slabs:** Always state the exact PSA/BGS/CGC grade, cert number, and card name. Include front + back slab photos.
- **Sealed:** Note any visible box damage (dents, seam pulls) in the listing. If it's factory sealed and pristine, say so.
- **Condition photos:** Show the actual item, not stock photos. This is non-negotiable for high-value items.
- Never list a slab as a grade higher than what's shown on the cert.

---

## Monthly seller health checklist

Run this at the same time as the monthly review (see `routines/prompts/end-of-month-review.md`):

- [ ] Check transaction defect rate in Seller Hub — target < 0.5%
- [ ] Check late shipment rate — target < 2%
- [ ] Check tracking upload compliance — target 100%
- [ ] Review any open cases or returns — resolve if outstanding
- [ ] Read any new feedback (positive and negative) — respond to negatives within 24h
- [ ] Check if TRS status is active — if lost, review which metric dropped
- [ ] Review listing accuracy on top 5 active listings — update photos or condition notes if needed

---

## Related files

- `routines/prompts/dispute-resolution.md` — full dispute handling process
- `routines/prompts/customer-review-request.md` — post-purchase review request
- `docs/packaging-guide.md` — prevent damage in transit (main cause of INAD)
- `routines/prompts/ebay-listing.md` — listing accuracy standards
