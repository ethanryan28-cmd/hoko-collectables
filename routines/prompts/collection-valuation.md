# Collection Valuation — Buyback Prompt

Use this prompt when a seller has submitted a list of cards they want to sell.
This generates a structured valuation summary and offer range for Ethan to review.

**Never send the AI output directly to the seller.** Always review and apply your own
judgement before making any offer. Final offer must follow the buyback policy (75-80% FMV).

---

## Inputs to Gather Before Running

| Input | Notes |
|---|---|
| Card list | Name, set, grade, grader (e.g. Charizard VMAX, Brilliant Stars, PSA 10) |
| Grading company | PSA / BGS / CGC only — reject HGA, GMG, unverified |
| Seller's asking price (if stated) | Optional — include if they've named a figure |
| Condition of slabs | Any scratches, cracks, tampering noted? |
| Urgency | Is the seller in a hurry or happy to wait? |

---

## The Prompt

```
You are helping Ethan from HOKO Collectables assess a buyback enquiry.
HOKO buys PSA, BGS, and CGC graded slabs only. No HGA, GMG, or unverified graders.
HOKO pays 75-80% of fair market value. FMV is based on recent sold listings on eBay AU,
eBay US (converted), and TCGPlayer (for MTG).

For each card below, provide:
1. Card name, set, grade, grader
2. Estimated FMV range (AUD) based on recent sold comps
3. HOKO offer range at 75-80% of FMV
4. Any flags (e.g. low liquidity, price volatility, grader concerns)
5. Recommended action: BUY / PASS / QUERY

Cards to value:
[PASTE CARD LIST HERE]

At the end, provide:
- Total estimated FMV of the collection
- Total HOKO offer range (75-80% of total FMV)
- Overall recommendation: proceed, negotiate, or pass
- Any items to exclude (wrong grader, low value, damaged slab)

Important rules:
- Do not fabricate sold prices — if you cannot find comps, flag as 'QUERY — no recent data'
- PSA 10 and BGS 9.5+ command a significant premium — factor this in
- If a card is under $100 FMV, HOKO policy is to pass (minimum $100 per slab)
- Be conservative on estimates — it's better to underpromise and overpay than overpromise
```

---

## How to Use

1. Receive card list from seller (DM, email, or WhatsApp)
2. Check each card: PSA/BGS/CGC only, $100+ FMV only
3. Paste the list into the prompt above
4. Run the prompt
5. Review the output — check each card's FMV estimate against eBay sold listings yourself
6. If proceeding, use the output as a reference to make your offer (48-hour turnaround)
7. If passing on any cards, note the reason so you can explain to the seller

---

## What to Do With the Output

The output is a draft valuation. Before making any offer:

- Cross-check 2-3 sold listings per card on eBay AU (last 30 days)
- Apply 75-80% to your own FMV estimate (not the AI's estimate blindly)
- Exclude any slabs that don't meet policy (wrong grader, under $100, damaged slab)
- Write your offer as a single total figure or itemised — whichever is cleaner for the seller

---

## What NOT to Include in Your Offer

- Any price negotiation in DMs — redirect to formal intake if needed
- Offers above 80% FMV — this is the hard cap
- Offers on HGA, GMG, or unverified grader slabs — HOKO does not buy these
- Offers on cards under $100 FMV — not worth the admin
- Consignment offers — Phase 2 only, not yet launched

---

## Turnaround

HOKO policy: 48-hour quote turnaround from when the full card list is received.
If you need more time, let the seller know — don't go quiet.

---

## Meeting Logistics

All buyback transactions at:
- A bank branch (seller's or HOKO's)
- A storage facility

Never meet at a private address. Payment: bank transfer on the day, no cash.
