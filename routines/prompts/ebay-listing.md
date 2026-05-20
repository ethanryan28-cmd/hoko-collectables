# eBay Listing Generator — HOKO Collectables

Generate an eBay AU listing for a TCG item.

## Inputs (fill these in)

- **Card / item:**
- **Set / product line:**
- **Condition (HOKO honest grading):** NM / LP / MP / HP / DMG  —  or  Sealed / Loose
- **Graded?** ungraded / PSA 9 / PSA 10 / BGS 9.5 / CGC 10 / other
- **Price (AUD):**
- **Quantity:**
- **Special notes:** 1st edition / signed / misprint / foil / holo / promo / etc.
- **Photos available:** yes / no

## Output

1. **Title** — max 80 chars, packed with terms AU TCG buyers actually search (set, card name, condition, year if relevant, key descriptors). No ALL CAPS. No emojis.
2. **Item specifics** — Brand, Set, Card Number, Card Name, Rarity, Language, Condition, Graded, Year, Features. Use eBay-AU standard values.
3. **Description** (mobile-readable, light HTML):
   - One-line hook
   - Bullet list: what you're buying, condition described honestly, packaging
   - Trust block: *"Collector-run from Melbourne. Honest grading — LP means LP. Tracked dispatch within 24 hrs."*
   - Cross-sell: *"Browse our full Pokémon / MTG / OPCG range and save 10% on your first order at hokocollectables.com with code HOKO10."*
4. **Suggested eBay AU category path**
5. **Suggested price logic** if I didn't pin one (use sold-comp reasoning)

Tone: collector-to-collector, honest, no hype words ("RARE!!", "AMAZING!!") unless genuinely warranted.
