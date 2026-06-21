# Grading Submission Prompt

**Trigger:** When preparing a batch of cards for PSA, BGS, or CGC submission.
**Use for:** Reviewing submission viability, tier selection, packaging standards, and tracking.

---

## Inputs

- **Grading company:** PSA / BGS / CGC
- **Submission tier:** [see tier guide below]
- **Cards to submit (list each):**
  - Card name, set, edition (1st ed/unlimited/shadowless etc.)
  - Estimated raw grade (your assessment)
  - Current raw market price
  - Estimated graded value at target grade
- **Total card count:** [number]
- **Current submission promo/discount?** Yes / No

---

## Tier selection guide

### PSA tiers (as of 2025 — check psacard.com for current pricing)

| Tier | Turnaround | Best for |
|------|-----------|---------|
| Value | ~100 business days | Low-value cards where you can wait |
| Economy | ~50 business days | Mid-value cards |
| Regular | ~20 business days | Higher value cards |
| Express | ~10 business days | High-value or time-sensitive |
| Super Express | ~5 business days | Very high value, need fast turnaround |

> **Rule of thumb:** Grading fee should be no more than 10-15% of expected graded sale price.

### BGS tiers
- Economy / Standard / Express / Premium Express
- BGS is worth the premium when quad 10s or Pristines are likely — pop report matters

### CGC tiers
- Economy / Standard / Express / Walkthrough
- CGC is cost-effective for bulk lower-value cards; less premium than PSA for most sets

---

## Viability check — run this for each card

For each card, calculate:

```
Expected graded value (at target grade) = [check recent eBay sold]
Minus: Grading fee = [tier fee]
Minus: Platform fees on sale = [approx 12-15% of graded value]
Minus: Postage to grader = [pro-rata per card]
Minus: Return postage = [pro-rata per card]
= Net profit vs buying the card graded directly
```

**Only submit if:** Net profit from grading > cost of buying it already graded at that grade.
If a PSA 10 of the card is available to buy for less than your all-in cost, don't grade — buy it.

---

## Pre-submission card assessment

Before including a card in the submission, check:

**Centering:**
- Front: left/right within 55/45 or better; top/bottom within 55/45 or better
- Back: similar tolerances
- Significant off-center kills a 10 chance immediately

**Corners:**
- Examine all 4 corners under bright light at a low angle
- Fraying, nicking, or whitening = significant deduction

**Edges:**
- Run a finger along all 4 edges — rough or chipped edges = deduction

**Surface:**
- Check for scratches, print lines, indentations, stains
- Clean cards with a soft microfibre cloth before submission — never use fingers

**Honest self-grade before submitting:**
- PSA 10: virtually perfect
- PSA 9: minor imperfections only (slight centering, minor surface issue)
- PSA 8: noticeable imperfections but clean overall
- Don't submit cards you'd realistically grade below 8 unless pop report makes a 7 or lower valuable

---

## Packaging for submission

Follow the grading company's current packaging guidelines — these change. As of 2025:

**Card sleeves:**
- Place each card in a clean penny sleeve first
- Then into a semi-rigid card saver or top loader
- Never use team bags as the only protection

**Labelling:**
- Attach the submission form label to each card saver/top loader
- PSA requires specific label placement — check current instructions

**Box packing:**
- Pack cards snugly — they should not shift in transit
- Use bubble wrap around the stack
- Ship in a rigid box (not a padded envelope)
- Use a tracked, insured shipping service (Australia Post Express with insurance for high-value submissions)

---

## Submission tracking

After submitting:
- Log in the tracking spreadsheet (or `routines/sku-watchlist.json`): card name, cert number (once returned), tier, submission date
- Check submission status online weekly
- Note expected return date and set a calendar reminder
- When returned: verify each cert number against what you submitted before listing

---

## Outputs to generate from this prompt

1. **Submission viability table** — for each card: raw estimate, target grade, expected graded value, all-in cost, net verdict (submit / skip)
2. **Submission summary** — total card count, total estimated fees, expected total return window
3. **Packaging checklist** — step-by-step packing instructions for the specific grader
4. **Tracking entry** — CSV-ready row for each card to add to your tracking spreadsheet

---

## Related files

- `routines/sku-watchlist.json` — active SKU and slab tracking
- `routines/prompts/sku-generator.md` — generate SKU for returned slabs
- `routines/prompts/slab-listing.md` — list returned slabs once graded
- `docs/photography-guide.md` — photograph returned slabs before listing
