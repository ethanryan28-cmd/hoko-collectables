# REPORT — 2026-10-17 pre-orders run (`claude/preorders-1017`)

Unattended run. Authorised: product creation (DRAFT only), tag/metafield writes, raise-to-floor prices on Japanese sealed. Every write backed up to `reports/backups/` and read back. No price lowered; discounts, orders, fulfilments untouched. Status writes were not in scope this run, so nothing changed status.

## Summary

| Step | Result |
|---|---|
| 0 State | PASS — nothing already done |
| 1 Route M6a / OP-17 | PASS — M6a routed (Urara batch); both OP-17 listings stay DRAFT, no supplier clears the floor |
| 2 Pre-orders for what's coming | PASS — 1 release in the 90-day window had no product (EB-05); created as DRAFT $235 |
| 3 Gates | PASS — 2 boxes were missing the cutoff line and were fixed; banned words 0; check/topup PASS; 43 tests pass. `run.py source` NOT RUN (no Shopify token in this environment) |
| 4 Wrap | PASS — merged `--no-ff` into main |

## Step 0 — State
Branch from main @ 2e0b597. Read CLAUDE.md, QUEUE.md, `REPORT-2026-10-17-consolidated.md`, `data/routing-2026-10-17.csv` (19 rows), `git log -20`. FX 1 JPY = 0.009112 AUD (open.er-api.com, 17 Oct). Nothing in this prompt was already done.

## Step 1 — Route the two left out

Same method as the consolidated run: single landed = (Kanade ¥ + ¥6,000) × FX; batch landed = Urara ¥ × FX + A$14; floor = (landed + 1.75% + $0.30) × 1.10 rounded up to $5; raise only within $15. Backup: `reports/backups/2026-10-17-routing-m6a-op17-before.json`.

| Box | Status | Price | Kanade ¥ | Urara ¥ | Single floor | Batch floor | Margin (batch) | Result |
|---|---|---|---|---|---|---|---|---|
| M6a 30th Celebration — No Outer Shrink (15398993723670) | DRAFT | $330 | none (no no-shrink row; sealed lots 39,980–44,980 dated Sept) | 25,000 (No-Shurink, stock 27) | — | $275 | $82.12 | **`route:urara-batch`**, `hoko.supplier` = urara, `no-shrink` tag added. Read back. Stays DRAFT (status write not authorised this run). |
| OP-17 (10734775730454) | DRAFT | $200 | case only: 379,800 / 12 = 31,650 | 0 stock | $390 | — | — | stays DRAFT: Kanade floor $190 above price; Urara not stocking |
| OP-17 pre-order duplicate (15402647453974) | DRAFT | $175 | 31,650 | 0 stock | $390 | — | — | stays DRAFT, same reason; duplicate listing of the same box |

Other live-set DRAFT boxes with no route tag: M6 sealed and OP-15 were already assessed in the consolidated run (no supplier clears the floor) and are unchanged. EB-03 Heroines (15410264736022) is not in the live set by the newest-3 definition; for reference its floors would be $320 single / $145 batch against a $155 list.

Rows appended to `data/routing-2026-10-17.csv` (now 22 data rows).

## Step 2 — Pre-orders for what's coming (next 90 days, to 15 Jan 2027)

Sources: samuraiswordtokyo.com release calendar and One Piece schedule article, onepiece-cardgame.com product pages (EB-05, OP-18), Japanese Pokémon schedule roundups (snkrdunk, torecamap, tcgpro, pokecottage, billsarchive via search).

| Game | Set | JP release | Shopify product | Action |
|---|---|---|---|---|
| One Piece | EB-05 Heroines Edition vol.2 (extra booster) | 31 Oct 2026 (publisher page) | none | **Created** DRAFT 15431829848342 |
| One Piece | OP-18 The Dominance of God | 21 Nov 2026 (publisher page) | 15417946865942 draft | left alone |
| Pokémon | M7 Aura Seeker | 27 Nov 2026 (reported, not yet confirmed) | 15417947455766 draft | left alone |
| Pokémon | MEGA×MEGA Parade high class pack | Feb 2027 (reported) | none | outside window, no publisher date → not created |
| One Piece | Heroines Precious Box | 31 Oct 2026 | none | authorised-shops box set, not a booster box → not created |

No Japanese Pokémon booster box is scheduled for December 2026 in any source found.

### EB-05 pre-order created
- Title `[PRE-ORDER] One Piece Heroines Edition vol.2 (EB-05) Sealed Japanese Booster Box`, handle `pre-order-one-piece-heroines-edition-vol-2-eb-05-sealed-japanese-booster-box`, type Sealed Product, vendor Bandai, tags `jp-sealed game:onepiece set:EB-05 preorder label:PRE-ORDER booster-box extra-booster japanese onepiece sealed`.
- Copy: cutoff line (release is before 1 Dec), pre-order line, proof line, authenticity line, 24 packs × 6 cards, release date, postage, 7-day not-as-described, sealed + international final sale, ACL sentence. SEO title/description set.
- Price **$235**: median of Australian pre-order listings for the Japanese box — japan-figure.com (en-au store) $267.00 and eBay AU item 318941719127 ≈ A$197.62 (US$138 converted) → $232.31 → rounded up to $5. Gameology ($279.95) and Games Portal ($495) list "EB-05 Booster Box" with no language and the English release date, so they were treated as English edition and excluded. Neither Urara nor Kanade lists EB-05 yet; the daily pre-order gate re-prices and activates it when one does.
- Image: Bandai's pack art from the EB-05 product page (MediaImage 47000266899734, READY). Bandai has not published a box packshot yet (the box slot on their page is a placeholder) — swap when it appears.
- SKU `PRE-OP-EB05-BOX`, inventory policy DENY, qty 0, DRAFT.
- Added to `japan-direct-sealed` (56 products now) and moved to position 0. M7 and OP-18 drafts are not in that collection and were left alone.
- Recorded in `data/preorders-2026-10-17.csv` (set · date · source · product ID · price basis · image source).

## Step 3 — Gates
- **Cutoff line on every ACTIVE jp-sealed box:** 19 ACTIVE products tagged `jp-sealed` read back. 17 carried the 7 Dec block; **M5 sealed (10734771765526) and OP-16 (10734775664918) did not** (they were DRAFT when the block was applied earlier today). Backup `reports/backups/2026-10-17-xmas-cutoff-m5-op16-before.json`, block prepended via `productUpdate`, read back: 19/19 now carry `Christmas delivery cutoff: order by Monday 7 December 2026`. PASS.
- **Banned words on everything touched** (EB-05 copy, routing CSV, pre-orders CSV, backups, QUEUE, this report): 0. PASS.
- `python content/youtube/run.py source`: **NOT RUN** — SHOPIFY_STORE / SHOPIFY_ADMIN_TOKEN are not set in this environment (falls back to mock-store → 404).
- Calendar statuses-only rebuild (`calendar_gen.build(render_beats=False)`): 72 rows. `python -m tools.social check` PASS (15 days × 6 platforms) → `topup` (165 items, no change) → `check` PASS. The EB-05 draft is not in the queue (DRAFT products are ineligible). PASS.
- Tests: `python -m pytest tools/social/tests -q` → 43 passed. PASS.

## NOT CHECKED
- `run.py source` (no Shopify token in the cloud environment).
- Whether Gameology / Games Portal EB-05 listings are English or Japanese (pages rate-limited; judged English from the 30 Oct date and absence of "Japanese" in the title).
- M7's 27 Nov date is reported by third parties, not yet confirmed by Pokémon Japan.
- Kanade stock (price list has prices only).

## MANUAL
**Ethan only**
- M6a no-shrink is routed and margin-positive at $330 via Urara; flip to ACTIVE + CONTINUE if you want it live (status writes were out of scope here).
- Two OP-17 listings exist (10734775730454 at $200, 15402647453974 pre-order at $175). Merge or delete one.
- EB-05 at $235 is a web-median placeholder; confirm when Urara/Kanade list it. Swap the pack-art image for Bandai's box packshot when published.
- Set the Shopify token in the cloud environment so `run.py source` can run.

**PC only**
- `python content/youtube/run.py source` then calendar rebuild.

## COMPLETE
