# SKU Generator

**Trigger:** When adding a new product to Shopify, eBay, or any platform that requires a consistent SKU.
**Use for:** Generating a standardised SKU code for graded slabs and sealed TCG product.

---

## SKU format

### Graded slabs

```
[GRADER]-[GRADE]-[CERT_LAST6]-[GAME_CODE]-[CARD_CODE]
```

| Component | Format | Example |
|-----------|--------|---------|
| GRADER | PSA / BGS / CGC | PSA |
| GRADE | numeric with decimal if needed | 9 / 9.5 / 10 |
| CERT_LAST6 | last 6 digits of cert number | 234567 |
| GAME_CODE | 2-3 letter game code (see below) | PKM / MTG / OP / DBS |
| CARD_CODE | up to 6 chars: set code + card number or abbrev | BS001 / EX147 / OP1001 |

**Examples:**
- `PSA-9-234567-PKM-BS004` — PSA 9 Charizard Base Set #4
- `BGS-9.5-987654-PKM-EXD045` — BGS 9.5 Ex Dragon #45
- `CGC-10-112233-MTG-RAV012` — CGC 10 Ravnica card #12

---

### Sealed product

```
SEALED-[GAME_CODE]-[SET_CODE]-[FORMAT_CODE]
```

| Component | Format | Example |
|-----------|--------|---------|
| GAME_CODE | PKM / MTG / OP / DBS | PKM |
| SET_CODE | abbreviation of set name (4-6 chars) | SV8 / TM / BRS |
| FORMAT_CODE | BOX / ETB / PACK / TIN / BUND | ETB |

**Examples:**
- `SEALED-PKM-SV8-BOX` — Pokemon Scarlet & Violet 8 Booster Box
- `SEALED-PKM-TM-ETB` — Pokemon Twilight Masquerade ETB
- `SEALED-MTG-MKM-BOX` — Magic: The Gathering Murders at Karlov Manor Booster Box
- `SEALED-OP-OP09-BOX` — One Piece OP09 Booster Box

---

## Game codes

| Code | Game |
|------|------|
| PKM | Pokemon |
| MTG | Magic: The Gathering |
| OP | One Piece Card Game |
| DBS | Dragon Ball Super Card Game |
| YGO | Yu-Gi-Oh (not currently in scope) |

---

## Format codes (sealed only)

| Code | Product type |
|------|-------------|
| BOX | Booster Box |
| ETB | Elite Trainer Box |
| PACK | Individual booster pack |
| TIN | Collector tin |
| BUND | Bundle (Paldean Fates-style bundle) |
| CMD | Commander precon deck (MTG) |
| COLL | Collection box / special set |

---

## Inputs to provide when generating

For slabs:
- Grader (PSA/BGS/CGC)
- Grade
- Cert number
- Card name
- Set name
- Card number in set

For sealed:
- Game
- Set name
- Product type (booster box, ETB, pack etc.)
- Language (JP/EN/KR) — append JP or KR suffix if not EN: `SEALED-PKM-SV8-BOX-JP`

---

## Outputs

Generate:
1. **SKU** — the code itself
2. **Shopify title suggestion** — product title in listing format
3. **Short description** — 1-line blurb for internal records

---

## Rules

- SKUs must be **unique** — check existing SKUs before generating
- Use **uppercase only** for all components
- No spaces — use hyphens only
- Max 30 characters total for the SKU
- For BGS sub-grades: use the overall grade in the SKU (not individual sub-grades)
- If cert number is fewer than 6 digits, zero-pad from the left: `00X` → `000012`

---

## Related files

- `routines/sku-watchlist.json` — current active SKU list
- `routines/prompts/slab-listing.md` — full listing prompt (uses SKU as input)
- `routines/prompts/shopify-sealed.md` — sealed listing prompt
