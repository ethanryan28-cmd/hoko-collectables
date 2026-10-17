# Whatnot Setup Guide

Setup, configuration, and show-running guide for HOKO Collectables on Whatnot.

---

## Account setup

### Initial seller application
- Apply at whatnot.com/sell — approval is not instant; can take days to weeks
- You'll need: valid ID, ABN (Australian Business Number), bank account for payouts
- Category: Trading Cards / Collectables
- Profile photo: use the HOKO logo or a clean product photo
- Bio: keep it short — e.g. "HOKO Collectables | Melbourne AU | Sealed TCG + PSA/BGS/CGC Graded Slabs | Collector first, seller second."

### Verified seller status
- Whatnot verifies sellers over time based on show performance and no violations
- Aim for 5-star seller rating — respond to all buyer messages promptly

---

## Shipping configuration

**Domestic (Australia):**
- Whatnot handles shipping labels in supported countries — check current AU availability
- If self-managed: use Australia Post Express Post for all orders
- Include tracking for all domestic shipments — buyers expect it
- Package to the same standard as eBay orders (see `docs/packaging-guide.md`)

**International:**
- Disable international shipping unless you're confident with customs documentation
- If enabled: use Australia Post International Express with tracking
- Note: some Whatnot buyers are US-based — check if your show settings allow international bidders

**Shipping cutoffs:**
- Ship within 1 business day of show end
- Mark as shipped in Whatnot dashboard immediately after dropping off at post office

---

## Show setup — before going live

### Scheduling a show
1. Go to Seller Dashboard > Schedule Show
2. Set title: use format `[Category] | HOKO Collectables | [Date]`
   - Example: `Graded Slabs + Sealed | HOKO Collectables | 22 Jun`
3. Set start time: aim for 7-9pm AEST weeknights or weekend afternoons
4. Set show duration: 60-90 minutes for standard shows; 2+ hours for large lots
5. Write a show description — what you're selling, approximate lot count, any highlights

### Show categories and tags
- Primary category: Trading Cards
- Tags: Pokemon, MTG, graded cards, PSA, sealed, HOKO, Melbourne

### Lot preparation
- Enter all lots before going live — do not improvise lots during the show
- For each lot: clear photo, accurate title, starting bid, buy-it-now price (optional)
- Starting bids: minimum $5 for commons, scale up by value
- Slot high-value items mid-show (not first, not last) — audience is warmest in the middle

**Lot naming convention:**
```
[GRADE/TYPE] [CARD NAME] [SET] [YEAR] — e.g.:
PSA 9 Charizard Base Set 1st Ed 1999
BGS 9.5 Pikachu Ex Dragon 2004
SEALED Pokemon Twilight Masquerade ETB 2024
MTG Sealed Commander Precon 2024
```

---

## During the show

### Audio and video
- Use a phone mount or tripod — shaky camera puts people off
- Good lighting is critical — use the same setup as your listing photos (see `docs/photography-guide.md`)
- Lapel mic or a quiet room — background noise kills stream quality
- Test audio and video 10 minutes before going live

### Show flow
- Open with a 2-3 minute intro: who you are, what you're selling today, rough lot count
- Read out the cert number and grade for every slab lot — buyers want to verify
- Show front and back of every slab before starting the timer
- For sealed: show all sides of the box, including the seal
- Pace yourself — don't rush lots; buyers need time to bid

### Pinned messages (set before going live)
- "Welcome to HOKO Collectables! Melbourne AU | Sealed TCG + Graded Slabs"
- "Ships same or next business day | Express Post with tracking"
- "Buyback enquiries: DM us @hokocollectables"

### Handling bids and buy-it-now
- Acknowledge every bid by name: "Thank you [username]"
- Call out the current bid and who's winning regularly during the countdown
- If BIN is used: confirm the winner and move to the next lot promptly
- Do not extend lots repeatedly — it frustrates bidders

### Dealing with no-shows (buyers who win but don't pay)
- Whatnot handles payment at time of winning bid — you should not have cash no-shows
- If a buyer cancels: accept cancellation and relist the item in a future show
- Excessive no-show buyers can be reported to Whatnot support

---

## After the show

### Immediate post-show (same night)
- Export the show summary: total lots sold, total revenue
- Pack all sold items ready for dispatch next morning
- Note any items that didn't sell — consider repricing for next show or listing on eBay

### Dispatch (next business day)
- Ship all show items
- Mark as shipped in Whatnot dashboard
- For $200+ items: use signature on delivery if available

### Content (within 48 hours)
- Post a show recap to Instagram: highlights, top sellers, what's coming next
- Use `routines/prompts/convention-post-content.md` as a base — adapt for Whatnot show

---

## Show performance targets

| Metric | Target |
|--------|--------|
| Peak concurrent viewers | 10+ (grows over time) |
| Lot sell-through rate | > 80% of listed lots sold |
| Average lot price | Depends on mix — track monthly |
| Buyer satisfaction rating | 5.0 / 5.0 |
| Ships on time | 100% |

---

## Common issues and fixes

| Issue | Fix |
|-------|-----|
| Stream drops out | Pre-download Whatnot app update; use Wi-Fi, not mobile data |
| No bids on a lot | Lower starting price; re-describe; move to end of show |
| Buyer complains item not as described | Refer to lot photo and description; resolve via Whatnot dispute process |
| Payout delayed | Check Whatnot seller dashboard — payouts typically 1-3 business days after show |
| Item damaged in transit | Claim with Australia Post; Whatnot has a seller protection policy — check current terms |

---

## Related files

- `routines/prompts/whatnot-show.md` — show script and lot order prompt
- `routines/whatnot-show-prep.md` — pre-show checklist
- `routines/whatnot-singles-liquidation-show.md` — singles liquidation show format
- `docs/packaging-guide.md` — packing standards for show lots
- `docs/photography-guide.md` — lot photo standards
