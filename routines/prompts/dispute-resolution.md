# Dispute Resolution

**When to use:** When a buyer opens a case, requests a return, sends a threatening message, or leaves negative feedback.
**Applies to:** eBay and Shopify orders

---

## Inputs

Before generating a response, confirm:

- **Platform:** eBay / Shopify
- **Dispute type:** Item Not Received (INR) / Item Not As Described (INAD) / Return request / Negative feedback / Payment dispute
- **Order date:** [date]
- **Item:** [product name + grade/cert if slab]
- **Tracking status:** [delivered / in transit / no scan / lost]
- **Buyer message (paste it):** [paste buyer message]
- **Any photos sent by buyer?** Yes / No — if yes, describe what they show

---

## Case type: Item Not Received (INR)

**Step 1: Check tracking before responding**
- If tracking shows delivered: respond with tracking details and request buyer to check with neighbours or local post office
- If tracking shows in transit: respond acknowledging the delay and provide expected delivery window
- If tracking shows no movement for 7+ days: escalate to Australia Post lost item inquiry and offer resolution options

**Response — tracking shows delivered:**
```
Hi [BUYER_USERNAME],

Thanks for getting in touch. I can see from tracking that your parcel was delivered to [ADDRESS] on [DATE] at [TIME].

Could you check with any other household members, neighbours, or your building's parcel area? Sometimes parcels are left in unexpected spots.

If you still can't locate it after checking, please let me know and I'll lodge an investigation with Australia Post on my end.

Cheers,
Ethan — HOKO Collectables
```

**Response — tracking shows in transit / delayed:**
```
Hi [BUYER_USERNAME],

Sorry for the delay — it looks like your parcel is still in transit. The latest tracking update was [DATE] showing [LOCATION].

Australia Post delays do happen occasionally. I'd suggest giving it another [2-3 business days] and checking the tracking link again: [TRACKING_NUMBER]

If it still hasn't arrived after that, message me and I'll escalate it with Australia Post straight away.

Cheers,
Ethan — HOKO Collectables
```

**Response — tracking shows lost / no movement 10+ days:**
```
Hi [BUYER_USERNAME],

I'm sorry to hear your parcel hasn't arrived. After reviewing the tracking, it does appear there may be an issue with delivery.

I've lodged a lost item inquiry with Australia Post — they typically investigate within 5 business days.

In the meantime, I'd like to offer you the choice of:
a) A full refund if the item is confirmed lost
b) A replacement if I have the same item in stock

Please let me know which you'd prefer and I'll sort it out for you.

Cheers,
Ethan — HOKO Collectables
```

---

## Case type: Item Not As Described (INAD)

**Step 1: Request photo evidence (if not already provided)**
```
Hi [BUYER_USERNAME],

Thanks for letting me know — I'm sorry to hear the item wasn't as expected.

Could you please send me a photo of what you received so I can understand the issue? That'll help me sort this out for you as quickly as possible.

Cheers,
Ethan — HOKO Collectables
```

**Step 2: Assess the claim against the listing**
- Does the photo show something different from what was listed?
- Is the issue a genuine discrepancy (wrong grade, different item) or a subjective disagreement (buyer expected better condition)?
- Was the condition clearly described in the listing?

**If the claim is valid (genuine discrepancy):**
```
Hi [BUYER_USERNAME],

Thank you for the photo — I can see the issue and I apologise for the error.

I'll [issue a full refund / send the correct item] immediately. You don't need to return the item.

The refund will appear in your account within [3-5 business days] / I'll ship the correct item today with tracking.

Again, I'm sorry for the inconvenience.

Cheers,
Ethan — HOKO Collectables
```

**If the claim is not valid (item matches listing):**
```
Hi [BUYER_USERNAME],

Thank you for getting in touch. Looking at the photos alongside my original listing, the item appears to match the description — [specifically note the matching detail, e.g. grade, condition, photos in listing].

I want to make sure you're happy, so I'm happy to discuss this further. Could you let me know specifically what you believe differs from the listing?

Cheers,
Ethan — HOKO Collectables
```

---

## Case type: Return request

**HOKO return policy:**
- Accepts returns within 30 days for items not as described
- Does not accept change-of-mind returns (clearly stated in listings)
- All returns must include original packaging

**If return is valid (INAD):**
- Accept the return immediately
- Send a prepaid return label if the buyer is in Australia
- Issue refund once item is received and inspected

**If return is change-of-mind:**
```
Hi [BUYER_USERNAME],

Thanks for reaching out. As noted in our listing, we don't accept change-of-mind returns for this category — this is standard for graded cards and sealed collectables.

If there's something about the item that doesn't match the listing, I'm absolutely happy to look into that. Otherwise, I'd suggest reselling through eBay — graded cards generally hold their value well.

Let me know if there's anything else I can help with.

Cheers,
Ethan — HOKO Collectables
```

---

## Case type: Negative feedback

**Do NOT respond in anger or defensively.** Always respond publicly, calmly, and briefly.

**Template — genuine issue, resolved:**
```
We're sorry this wasn't the experience we aimed for. We resolved this directly with the buyer and regret any inconvenience caused.
```

**Template — postal delay (outside our control):**
```
Item shipped same-day with Express Post tracking. Delivery delay was with Australia Post. Happy to assist further.
```

**Template — buyer misread listing:**
```
The item matched the listing exactly. We're sorry if there was any confusion and welcome buyers to message us before purchase.
```

**Feedback revision request (only if buyer is genuinely happy after resolution):**
```
Hi [BUYER_USERNAME], glad we could sort that out for you. If you're happy with the outcome, would you be open to revising your feedback? No pressure at all. Cheers, Ethan
```

---

## Escalation — when eBay gets involved

If eBay escalates a case:
- Respond within 3 business days or eBay may close it in buyer's favour
- Provide: tracking information, listing screenshots, any photos, communication history
- For slabs: provide cert number — eBay can verify authenticity via PSA/BGS/CGC
- Accept that eBay almost always sides with buyers for INR cases with lost tracking
- If you lose a case via eBay, it still creates a defect — monitor in Seller Hub

---

## Tone reminders

- Never match a buyer's aggression — stay calm and professional at all times
- Short messages are better than long ones — buyers often skim
- Acknowledge the problem first before explaining or defending
- Offer a clear resolution path — do not leave buyers guessing
- Document every interaction (keep screenshots in your records)

---

## Related files

- `docs/ebay-reputation-guide.md` — defect rate targets and feedback management
- `routines/prompts/customer-review-request.md` — post-purchase follow-up (only send if no issues)
- `docs/packaging-guide.md` — prevent disputes before they start with better packing
