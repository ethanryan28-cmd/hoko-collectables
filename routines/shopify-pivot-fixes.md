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

## 5. Archive sub-$50 products from Shopify

**Updated decision (May 2026):** archive everything under AUD $50 via the script. Catches most cheap singles + low-end accessories. Premium singles ($50+) stay listed and sell through naturally. Existing singles inventory moves via the Whatnot liquidation stream + eBay sell-through.

**Primary path: run the script.**

```powershell
cd scripts/shopify
$env:SHOPIFY_STORE = "hokocollectables.myshopify.com"
$env:SHOPIFY_ADMIN_TOKEN = "shpat_..."

# Step 1 — dry-run, writes candidates.csv. No changes made.
python archive_cheap_singles.py
```

- [ ] Set up Shopify Admin API token (one-time, see `scripts/shopify/README.md`)
- [ ] Run dry-run — produces `candidates.csv`
- [ ] **Open `candidates.csv` in Excel** — review every row
  - Critically: spot-check for **cheap sealed product** (individual booster packs at $5-8, sealed accessories) that you want to keep listed. The price filter catches these too.
  - If anything in the list shouldn't be archived, take note for the next step.
- [ ] If a few items shouldn't be archived: either temporarily raise their price to $50+ in Shopify so they fall outside the filter, or skip the script and manually archive everything else via Shopify Connector instead
- [ ] When CSV looks right: `python archive_cheap_singles.py --execute` and type `archive` to confirm
- [ ] After archive: confirm via Shopify Admin → Products → Status = Active filter → should show only sealed + slabs (with premium singles still active by design until they sell through)

**Reversibility:** archived products stay in Shopify admin. Products → filter Status = Archived → open product → Unarchive.

**Alternative path** (voice-driven, by product type instead of price): use the Shopify Connector — *"Show me every product that is NOT a sealed box, ETB, pack, deck, sealed accessory, or graded slab. Don't change anything yet."* Useful for a deeper purge later that catches premium singles ($50+) too.

---

## After this is done

Bigger lifts — *not* required for the pivot, do later when working capital is flowing:

- Add a hero image (good photo of Japanese sealed or a slab)
- Reviews widget (Loox or Judge.me)
- Founder story page
- Structured buyback intake form (replacing free-text "Sell Your Cards" form, mirroring `templates/collection-buyback-intake.md`)
- **Consignment intake page** (Phase 2 — when the consignment service formally launches)
- Sticky HOKO10 banner (currently only in footer signup)
