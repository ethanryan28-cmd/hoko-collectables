# Prompt Templates

Reusable prompts for HOKO Collectables content generation. Copy any of these into your local Claude session, fill in the inputs, and run.

## How to use

**In local Claude Code on your PC:**

```powershell
cd C:\path\to\claude\hoko-collectables
claude
```

Then either:

- `Read routines/prompts/ebay-listing.md and use it for: Charizard Base Set 1st Ed, LP, ungraded, $750 AUD`
- Or copy the template, fill in the inputs, paste back

## Templates

| File | Use when |
|------|----------|
| `ebay-listing.md` | New eBay listing for a single, sealed item, or lot |
| `shopify-sealed.md` | New sealed product page on Shopify |
| `social-caption.md` | Instagram / TikTok post — also gives TikTok script |
| `whatnot-show.md` | Going live — show title, run-of-show, lot list, pinned messages |
| `package-insert.md` | The card going in the box — converts eBay buyers to Shopify |
| `voice-dump-processor.md` | Raw voice transcript dump — categorises and drafts structured output across all content buckets |
| `buyback-dm-reply.md` | Incoming DM/email from a seller offering a collection — drafts a compliant reply that enforces buyback rules |
| `youtube-optimiser.md` | YouTube video upload — generates SEO title, description, tags, and thumbnail brief |
| `pricing-update.md` | Repricing a SKU at replacement cost — new list price calc, Shopify Connector command, eBay update note |

## Channel strategy these support

- **eBay** — sealed product + graded slabs, customer acquisition via search
- **Shopify** — primary brand storefront, sealed + slabs
- **Whatnot** — live pack-rip / box-break shows
- **YouTube** — long-form content (unboxings, collection reviews, grading reveals)
- **Package insert** is the bridge: eBay buyers get a HOKO10 + Shopify pitch in every parcel

## Post–May 2026 pivot note

All prompts reflect the sealed-product + verified-grader slab focus. In-scope: Pokémon, MTG, One Piece, Dragon Ball Super sealed; PSA/BGS/CGC slabs. Out of scope: loose singles, mystery packs, HGA/GMG/unverified-grader slabs.
