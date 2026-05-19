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

## 5. Hide bulk lots from featured collections

Search results lead with cheap bulk lots — tanks brand perception. Don't archive yet (the `archive_cheap_singles.py` script does that later). Just unfeature.

- [ ] Voice: *"Show me which products under AUD $30 are currently in 'New Arrivals' or 'Featured'. Don't change anything."*
- [ ] Review list.
- [ ] Voice: *"Remove those from 'New Arrivals' and 'Featured' — don't archive, just unfeature."*

---

## After this is done

Bigger lifts — *not* required for the pivot, do later when working capital is flowing:

- Add a hero image (good photo of Japanese sealed or a slab)
- Reviews widget (Loox or Judge.me)
- Founder story page
- Structured buyback intake form (replacing free-text "Sell Your Cards" form, mirroring `templates/collection-buyback-intake.md`)
- Sticky HOKO10 banner (currently only in footer signup)
