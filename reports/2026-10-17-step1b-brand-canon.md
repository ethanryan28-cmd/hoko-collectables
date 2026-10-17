# Step 1b — Brand canon (17 Oct audit) — 2026-10-17

**Draft theme:** `HOKO NEXT — 1b brand canon 17 Oct (draft)` (`gid://shopify/OnlineStoreTheme/190950736150`), duplicated from MAIN `HOKO NEXT — sold-out last` (`…/190759731478`). **Not published.**
Preview: Online Store → Themes → the draft → Preview.

> Note: pages, collections, articles, products, URL redirects and Shopify Email are **store-wide, not theme-scoped**. Those edits went live when made. Only the theme edits (items 5 and 6) wait on a publish.

---

## 1. Store default meta description — for Chrome (connector can't write it)

Online Store → Preferences → Homepage meta description.

**Before (live, read via API `shop.description`):**
> We buy card collections Australia-wide — send photos, get an itemised offer within 1–2 business days. Also stocking Magic, Pokémon, One Piece, Lorcana and Gundam singles. Honest grading, packed by hand in regional Victoria.

**After (paste this):**
> We buy card collections Australia-wide — send photos, get an itemised offer within 1–2 business days. Also stocking Magic, Pokémon, One Piece, Lorcana, Gundam and Dragon Ball Super singles plus Japanese sealed. Honest grading, packed by hand in Victoria, Australia.

Length: 246 chars. Google truncates around 155–160, so the snippet will cut off after "…within 1–2 business days." That's fine because the buy-offer leads.

---

## 2. /collections/japan-direct-sealed — DONE (live)

**Description before:**
> The newest sealed Japanese booster boxes, imported from Japan by HOKO in small batches and shipped tracked from Victoria once they land. Allow 2–3 weeks for delivery. Item origin: Japan.
> Collector first. Seller second.

**Description after:**
> The newest sealed Japanese booster boxes, imported from Japan by HOKO in small batches and shipped tracked from Victoria once they land. Dispatched tracked from Victoria within 2–4 business days once it lands. Item origin: Japan.
> Collector first. Seller second.

⚠ The swap reads a bit repetitive ("shipped tracked from Victoria once they land. Dispatched tracked from Victoria … once it lands."). Suggested tidy, not applied: drop "and shipped tracked from Victoria once they land" from sentence 1.

**Heat Wave Arena handle — already done before this session, so no change made:**
- Product: `Pokemon Heat Wave Arena (sv9a) Sealed Japanese Booster Box`
- Handle (current): `pokemon-heat-wave-arena-sv9a-sealed-japanese-booster-box`
- Redirect already exists: `/products/pokemon-hot-air-arena-sv9a-sealed-japanese-booster-box` → `/products/pokemon-heat-wave-arena-sv9a-sealed-japanese-booster-box` (`UrlRedirect/765811523862`)

---

## 3. /pages/want-list → /pages/sell-your-cards — DONE (live)

**Gap check (before merging):**

| want-list section | on sell-your-cards before? |
|---|---|
| Retro games bullet | ❌ missing, so merged in (below) |
| In-person meet line | ✅ "Meet in person — … bank branch or storage facility in Victoria. We don't do home pickups." |
| Quote form | ✅ template `page.sell-your-cards.liquid` renders section `hoko-seller-intake` |

**Merge into sell-your-cards. Added `What We Buy` bullet:**
> **Retro games & consoles** — GBA, DS, N64, SNES. Loose, CIB or sealed, authenticated before we quote.

**Also changed on sell-your-cards (link would have redirected back to itself):**
- Before: "…our working shown. See what we pay on our Buy Prices page and what we're chasing on our want list."
- After: "…our working shown. See what we pay on our Buy Prices page."

**want-list duplicate H1:**
- Before: body `<h1>We Buy Magic, Pokémon, One Piece, Lorcana, Gundam & Dragon Ball Super Collections — Australia-Wide</h1>`, plus the template's `<h1>We Buy Cards</h1>`, which made 2 H1s
- After: body heading demoted to `<h2>`. Only "We Buy Cards" remains as H1.

**301:**
- Shopify only fires a URL redirect when the old URL 404s, so `want-list` was **unpublished** (not deleted, body kept) and the redirect `/pages/want-list` → `/pages/sell-your-cards` was created (`UrlRedirect/786373181718`).

**Not carried over from want-list (judgement call, flag if you want them):** per-game "What We're After" chase lists (Prismatic Evolutions, OP-09/10, WOTC vintage, Reserved List…), contact list (email / IG / TikTok DM), and the 5-question FAQ. These are SEO-useful. Say the word and I'll merge them into sell-your-cards.

**Leftover links to /pages/want-list (they still work via the 301; not changed):**
- Main menu item **"We Buy Cards" → /pages/want-list**. It now duplicates the "Sell Your Cards" item right above it. Recommend deleting it.
- `/pages/buy-prices` body: "Check the want list for what we're chasing…"

---

## 4. /pages/sell-your-cards meta description — DONE (live)

- Before: "Get cash or store credit for your Pokémon, One Piece, Magic, Lorcana, Gundam and Dragon Ball Super cards, and retro games. HOKO Collectables buys collections Australia-wide."
- After: "Get cash or store credit for your Pokémon, One Piece, Magic, Lorcana, Gundam and Dragon Ball Super cards. HOKO Collectables buys collections Australia-wide."
- Retro is still a bullet on the page (see 3).

---

## 5. Proof line + 1.4K → 1.5K

**Live eBay count verified first:** ebay.com.au/str/hokocollectables shows "100% positive Feedback", "1.5K items sold" (17 Oct).

**Homepage eBay-feedback section (draft theme, `templates/index.json` → `hoko_ebay_reviews.settings.proof`):**
- Before: `1.4K sold, 100% positive on eBay`
- After: `Selling since 2023 · 1.5K sold, 100% positive on eBay`

**Every other 1.4K string:**

| Location | Before | After | Where |
|---|---|---|---|
| `sections/hoko-ebay-reviews.liquid` schema default | `1.4K sold, 100% positive on eBay` | `1.5K sold, 100% positive on eBay` | draft theme |
| `sections/hoko-hero-v3.liquid` hero proof list | `<li>1.4K sold, 100% positive on eBay</li>` | `<li>1.5K sold, 100% positive on eBay</li>` | draft theme |
| `snippets/hoko-product-trust.liquid` (every PDP) | `1.4K sold, 100% positive on eBay` | `1.5K sold, 100% positive on eBay` | draft theme |
| Page `consign-your-cards` | "…through our eBay store (1.4K sold, 100% positive)." | "…through our eBay store (1.5K sold, 100% positive)." | live |
| Page `about` (unpublished) | "Selling since 2023. 1.4K sold, 100% positive." | "Selling since 2023. 1.5K sold, 100% positive." | live (page is hidden) |

Articles and collections: 0 hits for "1.4K". Post-sweep theme grep (all sections, templates, snippets, blocks, layout, config): 0 hits.

Note: the hero already has a separate "Selling since 2023" bullet beside the eBay one, so the homepage now says "Selling since 2023" twice (hero + reviews section). That's harmless but you might want to drop one.

---

## 6. Footer Pinterest — DONE (draft theme)

The active footer is the custom section `hoko-footer-v3` (the theme's default footer blocks are disabled), so the link went into its social row after Discord:

- Before: Instagram · TikTok · YouTube · Discord · eBay · Email
- After: Instagram · TikTok · YouTube · Discord · **Pinterest** · eBay · Email
- Markup: `<a href="https://www.pinterest.com.au/hokocollectables/" class="hoko-footer__social-link" aria-label="Pinterest">` + inline SVG (the `hoko-icon` snippet has no Pinterest glyph). Discord unchanged.
- Side effect: the schema JSON in that file had 2 keys reordered (`settings` / `class`). This is functionally identical.

---

## 7. Condition scale + blog title — DONE (live)

**shipping-returns.** Inserted directly under the Returns intro paragraph, above the final-sale bullets:
- Before: `…refund, replacement, or store credit.</p>` → `<ul><li>Sealed product is final sale.…`
- After: `…refund, replacement, or store credit.</p>` → `<p>Condition scale: NM · LP · MP · HP · DMG</p>` → `<ul>…`

**Blog title stray space.** The only article title in the store with a space before "!" (`Article/683758125334`):
- Before: `Pokemon Card Condition Guide — NM vs LP vs MP vs HP vs Damaged Explained !`
- After: `Pokemon Card Condition Guide — NM vs LP vs MP vs HP vs Damaged Explained!`

---

## 8. Product types + legacy titles — DONE (live)

**"One Piece Single" → "One Piece Singles":** 62 products (41 active, 18 draft, 3 archived) retyped.
- Before: One Piece Single 62 / One Piece Singles 437
- After: One Piece Single **0** / One Piece Singles **499**
- Backup: `reports/backups/2026-10-17-one-piece-single-type.csv`

**Counts only, unchanged:**

| Type | All statuses | Active |
|---|---|---|
| Trading Card | 488 | 195 |
| Trading Card Single | 142 | 75 |

**Legacy suffix titles.** The actual suffix in the store is ` PKM NM AU Stock Tracked`. No title contains "…Tracked Pokémon".

- 15 titles carry "… NM AU Stock Tracked": 7 PKM (all ACTIVE), 8 MTG (`MTG NM AU Stock Tracked`, 6 archived + 1 draft, plus "Stock Up 24" which is a false match).
- Stripped ` PKM NM AU Stock Tracked` on the 7 ACTIVE ones. Backup first: `reports/backups/2026-10-17-legacy-suffix-titles.csv`.

| Before | After |
|---|---|
| Empoleon 037/172 Holo Rare Brilliant Stars PKM NM AU Stock Tracked | Empoleon 037/172 Holo Rare Brilliant Stars |
| Magmar 019/172 Common Brilliant Stars PKM NM AU Stock Tracked | Magmar 019/172 Common Brilliant Stars |
| Riolu 113/198 Common Scarlet & Violet PKM NM AU Stock Tracked | Riolu 113/198 Common Scarlet & Violet |
| Alcremie 071/172 Rare Brilliant Stars PKM NM AU Stock Tracked | Alcremie 071/172 Rare Brilliant Stars |
| Duskull 060/172 Common Brilliant Stars PKM NM AU Stock Tracked | Duskull 060/172 Common Brilliant Stars |
| Druddigon 113/172 Rare Brilliant Stars PKM NM AU Stock Tracked | Druddigon 113/172 Rare Brilliant Stars |
| Ultra Ball 150/172 Uncommon Brilliant Stars PKM NM AU Stock Tracked | Ultra Ball 150/172 Uncommon Brilliant Stars |

Handles were left alone (they still contain `pkm-nm-au-stock-tracked`), so no redirects were needed. The titles now have no game name. Other singles use "… Pokemon Near Mint". Optional: append " Pokemon Near Mint" for consistency.

---

## 9. Shopify Email

The Admin API doesn't expose Shopify Email campaigns or automations (`marketingActivities` returns empty), so this was checked against your Gmail inbox (you're on the list):

- **"Japanese sealed boxes are on the site": SENT.** It landed in ethan.ryan28@gmail.com on **10 Oct 2026, 13:48 AEDT** (02:48 UTC) from support@hokocollectables.com. Preheader: "Newest sets and best sellers, tracked from Victoria". It was a real send, not a `[Preview]`. Recipient count and open rate aren't visible from here: Marketing → Campaigns.
- **Welcome flow: built, live status unconfirmed.** Only `[Preview] Welcome to HOKO — your 10% off is here` exists (6 May 2026), plus 2 more `[Preview]` follow-ups ("What we're loving right now (and 1 chase card)", "Last chance — your 10% off ends tonight"). There have been no live welcome sends to you, but you subscribed long before May, so that proves nothing either way. Check Marketing → Automations → Welcome new subscribers: is it **Active**?

**BFDROP5 (already exists, scheduled):** $5.00 off, scoped to collection `japanese-sealed` (56 products), once per customer, any customer. Runs **Fri 27 Nov 00:00 → Mon 30 Nov 23:59 AEDT**. That matches the /pages/black-friday window (27–30 Nov).
⚠ "Early access" isn't enforced: the code isn't segment-limited and doesn't start before the public sale. Either send the email now-ish and accept that, or move `startsAt` earlier (e.g. Thu 26 Nov) to give the list a real head start.

### Draft: BF early-access box-drop email. **SUPERSEDED by `content/email/` (its postage line matches the live BF page)**

- **Subject:** Black Friday box drop — the list gets first look
- **Preview text:** $5 off Japanese sealed with code BFDROP5. Small batches.
- **Heading:** Black Friday box drop
- **Body:**

  You're on the HOKO list, so you hear about it first.

  From 12am Friday 27 November (AEDT), use **BFDROP5** at checkout for **$5 off Japanese sealed booster boxes**.

  - Code: BFDROP5, once per customer
  - Runs Friday 27 to Monday 30 November, ends 11:59pm AEDT
  - ~~Postage $15.25, free on sealed orders of $250 or more~~ (conflicts with the BF page: "$100+ ships free that weekend")

  These come in small batches. When a box sells out it stays out until the next shipment lands.

- **Button:** Shop Japanese Sealed → `https://www.hokocollectables.com/collections/japanese-sealed` (the collection the code applies to)
- **Sign-off:** Collector first. Seller second. — Ethan

Banned-word check on the draft: 0 hits.

---

## GATE — banned-word sweep (Whatnot, Top Rated, mystery pack, official)

Final gate results and the 12-article "official" rewrite table: see `REPORT-2026-10-17T1140+1100.md` (Step 2). Articles 0 · collections 0 · published pages 0 · active products 0. Residuals are only on the unpublished `whatnot-live` page and archived/draft products.

---

## Live vs draft summary

| Change | Scope |
|---|---|
| Theme: proof line, 1.5K ×3 files, Pinterest | **Draft only.** Publish when happy. |
| Collection, pages, redirect, articles, product types/titles | **Live now** |
| Store meta description | **Pending: Chrome** (string above) |
| BF email | **Draft text only.** Build + schedule in Shopify Email. |
