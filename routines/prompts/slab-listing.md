# Prompt: Graded Slab Listing (Shopify + eBay)

Use when: you've acquired a PSA, BGS, or CGC graded slab via buyback and need to list it on Shopify and/or eBay.

**Important:** Only PSA, BGS, and CGC slabs. No HGA, GMG, or unverified-grader slabs — ever.

---

## Inputs (fill in before running)

```
Card name: [e.g. Charizard, Pikachu Illustrator, Black Lotus]
Set / year: [e.g. Base Set 1999, Alpha 1993, 151 2023]
Variant: [e.g. Shadowless, 1st Edition, Holo, Non-Holo, None]
Language: [English / Japanese / Korean / Other]
Grader: [PSA / BGS / CGC]
Grade: [number, e.g. 9, 9.5, 10]
Cert number: [the grader's cert number on the label — verify on grader's website]
Game: [Pokemon TCG / Magic: The Gathering / Other]
Cost (what you paid): $[X] AUD
Current eBay sold comps: $[X] AUD (check eBay sold listings filtered by same grader + grade)
Target sell price: $[X] AUD (or type "calculate" to get a recommended price)
Channel(s): [Shopify / eBay / both]
Photos ready?: [yes / no — if no, note what's needed]
```

---

## What to produce

### 1. Shopify product listing

**Title** (follow seo-guide.md format):
```
[Card Name] [Set] [Year] [Grader] [Grade] | [Game] | [Variant if applicable] | HOKO Collectables
```

Example: `Charizard Base Set 1999 PSA 9 | Pokemon TCG | Shadowless Holo | HOKO Collectables`

**Description** (3-4 sentences, AU English, collector-to-collector tone):
- What the card is (set, variant, significance)
- Grade context (why this grade matters for this card — e.g. PSA 9 base set Charizard is strong because raw copies are risky)
- Grader credentials (PSA/BGS/CGC only — note cert can be verified at [grader website])
- Shipping (free AU shipping over $100, secure packaging, same-day dispatch)

**Meta description** (140-160 chars):
> [Grade] [Card name] [Set] — authenticated by [grader]. Secure packaging, same-day dispatch. Melbourne-based collector shop.

**Price recommendation** (if "calculate" was entered):
```
Reference: current eBay sold comps = $X
Target: price at market (not below, not over 10% above)
Shopify price = $[X] AUD
eBay price = same or $5-10 higher (accounts for eBay fees)
```

**Tags for Shopify:**
graded-slabs, [grader-lowercase], [grade], [game-slug], [card-name-slug], psa-graded (or bgs-graded / cgc-graded)

**Collection:** Graded Slabs

---

### 2. eBay listing

**Title** (80 chars max):
```
[Card Name] [Set] [Year] [Grader] [Grade] [Variant] [Game] TCG [Language]
```

Example: `Charizard Base Set 1999 PSA 9 Shadowless Holo Pokemon TCG English`

**Item specifics:**
- Card Name: [card name]
- Set: [set name]
- Year: [year]
- Language: [language]
- Grade: [grade]
- Grading Service: [PSA / BGS / CGC]
- Certification Number: [cert number]
- Type: Graded Card

**Description** (plain text, collector voice):
Note the cert number and direct buyers to verify at PSA/BGS/CGC website.
Include condition note (what the slab itself looks like — any case scratches? note them honestly).
Free AU shipping over $100, Express Post, same-day dispatch. Secure packaging (bubble wrap + rigid mailer).

**Price:** [Shopify price + $5-10 to account for eBay fees, or match market]

---

### 3. Cert verification step (do this before listing)

Before you list, verify the cert number is valid:
- **PSA:** https://www.psacard.com/cert/
- **BGS:** https://www.beckett.com/news/beckett-grading-services-cert-verification/
- **CGC:** https://www.cgccards.com/certlookup/

Paste the cert number and confirm the card matches what's on the label. This protects you from selling a tampered or counterfeit slab.

---

### 4. Photo checklist

For a slab, you need:
- [ ] Front of card (through slab, good lighting, no glare)
- [ ] Back of card (through slab)
- [ ] Label (clearly showing grader, grade, cert number, card name)
- [ ] Side view of slab (shows slab condition)
- [ ] Optional: 45-degree angle shot showing shine/holo

---

## Pricing rules (never override)

- Price at current eBay sold comps, not historical purchase price
- If replacement cost (what you'd pay to acquire the same slab today) is higher than comps, note it but still price at market
- Buyback cost is a sunk cost — don't subtract it from pricing decisions; the question is "what would I pay to get this again today?"
- Never list below current market to "move it quickly" — the moat is service + authenticity, not price
