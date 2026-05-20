# Shopify pivot punch list — sealed-only

5 fixes to bring hokocollectables.com in line with the sealed-only pivot. ~30 mins total via Shopify Connector for Claude (voice on phone). Every step uses the "show me first, don't execute yet" safety habit.

**Tick boxes from GitHub mobile as you go.**

---

## 1. Drop off-strategy items from main nav

Bulk lots on the live site are priced "100x Pokemon $18" / "100x MTG $22" — clearly bulk singles, off-strategy.

**If Mystery Packs is also singles-bundle stuff:**

- [ ] Voice: *"Remove 'Mystery Packs' and 'Bulk Lots' from the main navigation menu. Don't archive the products, just unlink from the menu."*

**If Mystery Packs is genuinely sealed booster packs (one random sealed pack):**

- [ ] Voice: *"Remove 'Bulk Lots' from the main navigation, but keep 'Mystery Packs'."*

---

## 2. Add "Sealed" and "Graded Slabs" to main nav

These are now the two pillar collections.

- [ ] Voice: *"Show me whether I have a 'Sealed' collection and a 'Graded Slabs' collection. If they exist, add both to the main nav. If they don't exist, list which products would belong in each — don't create the collections yet."*
- [ ] Review the products list, approve the collection creation if needed.
- [ ] Voice: *"Go ahead, create the collections and add them to the main nav after 'Shop'."*

---

## 3. Fix shipping-threshold mismatch

Site shows both "$50" and "$100" as free-shipping threshold depending where you look. Brand promise is **$100**.

- [ ] Voice: *"Find every place on the site that mentions 'free shipping over $50' or 'free shipping'. Show me the list. Don't change anything."*
- [ ] Review list.
- [ ] Voice: *"Update them all to: 'Free AU shipping on orders over $100'."*

---

## 4. Rewrite hero subheadline

**Current:**
> Pokemon, MTG, One Piece & Japanese Sealed. Honestly graded, packed properly, shipped tracked from Melbourne.

Problem: "sealed" buried at end, "graded" reads as singles condition.

**New:**
> Sealed boxes, ETBs & graded slabs. Pokémon, MTG, One Piece, Japanese imports. Honest grading. Same-day dispatch from Melbourne.

- [ ] Voice: *"Update the homepage hero subheadline to: 'Sealed boxes, ETBs & graded slabs. Pokémon, MTG, One Piece, Japanese imports. Honest grading. Same-day dispatch from Melbourne.'"*

---

## 5. Archive EVERYTHING currently on Shopify (clean slate)

**Updated decision (May 2026):** instead of triaging by price, **archive every active product** on the site. Cleanest possible move. Site keeps its hero / theme / collections / pages — only products go hidden. Reversible: any product can be unarchived later from Shopify admin if you change your mind.

Owner confirmed no sealed booster packs or accessories currently listed, so the threshold-review approach is unnecessary — the whole catalogue is off-strategy and goes.

### Path A: Shopify Connector (preferred, do from phone)

If Connector isn't set up yet:

1. On phone, open Safari (or Chrome) → `claude.ai/settings/connectors`
2. Find Shopify → Connect → OAuth into Shopify admin → approve
3. Pick `hokocollectables.myshopify.com`
4. ~5 min total

Then voice prompts:

- [ ] *"Show me every active product on hokocollectables. Don't change anything yet — give me the count and the first 20 names."*
- [ ] Sanity-check the list (just confirms the Connector is talking to the right store)
- [ ] *"Archive ALL active products. Don't delete — archive. Confirm with me before you start."*
- [ ] Approve confirmation prompt
- [ ] *"Show me how many products are still active. I expect 0."*

### Path B: Script (PC required, API token route)

When at PC:

```powershell
cd scripts/shopify
$env:SHOPIFY_STORE = "hokocollectables.myshopify.com"
$env:SHOPIFY_ADMIN_TOKEN = "shpat_..."

# Edit archive_cheap_singles.py: THRESHOLD_AUD = 99999.0
python archive_cheap_singles.py            # dry-run, writes candidates.csv
# Review CSV (should be everything active)
python archive_cheap_singles.py --execute
# Type 'archive' to confirm
```

### After archive

Catalogue is empty. Going forward, new listings only:

- **Slabs** from buybacks (commercial, for sale) — listed via Connector after each filming/photo session
- **Sealed product** from supplier orders — listed when shipments arrive
- **NEVER** the PC slabs (those are content fuel, not inventory)

The first new listings come from today's slab filming session (commercial slabs only — PC slabs stay off-Shopify).

---

## After this is done

Bigger lifts — *not* required for the pivot, do later when working capital is flowing:

- Add a hero image (good photo of Japanese sealed or a slab)
- Reviews widget (Loox or Judge.me)
- Founder story page
- Structured buyback intake form (replacing free-text "Sell Your Cards" form, mirroring `templates/collection-buyback-intake.md`)
- **Consignment intake page** (Phase 2 — when the consignment service formally launches)
- Sticky HOKO10 banner (currently only in footer signup)
