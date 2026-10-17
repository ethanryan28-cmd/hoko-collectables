# REPORT — 2026-10-19 · Copy hygiene (`claude/copy-hygiene-1019-n6reb3`)

Branch note: the harness pins this session to `claude/copy-hygiene-1019-n6reb3` (prompt said `claude/copy-hygiene-1019`).

## Pre-run: what the read found (640 ACTIVE, one bulk read)

- The old figures ("free over $30", "$12.50") are only on the **3 card bundles**. The singles paragraph on 612 products already carries $3 / $10.95 / free at $150, but adds **"Express Post is $19.50"** (not canon) and offers the $3 letter on $50+ cards and slabs.
- 24 Japanese sealed say "free on orders of $250 or more" (canon: "free on sealed orders of $250+"); 19 of them miss "once it lands" in the dispatch line. The English TMNT Commander deck adds "Express Post $19.50".
- Slab SEO descriptions: 6 say "free tracked postage". Only Bellsprout (PSA 9, $115) is under $150; the other 5 ($150+) are true as written and stay.
- "same-day": 0 hits.

## Step 1 examples (before the bulk run)

Only the postage sentences change; "We ship worldwide, tracked.", the dispatch sentence and "Combined postage applies automatically on multiple items." stay byte-identical.

**Single under $50** — Dark Knight's Greatsword 95 (10417121886486, $4.23)
- before: `Letter post $3 (untracked) or tracked parcel $10.95 — free tracked on orders of $150 or more. Express Post is $19.50.`
- after: `Postage within Australia: $3 untracked letter.`

**Slab** — Bellsprout 69 Topps Chrome PSA 9 (10655248122134, $115)
- body before: `Letter post $3 (untracked) or tracked parcel $10.95 — free tracked on orders of $150 or more. Express Post is $19.50.`
- body after: `Postage within Australia: $10.95 tracked, free tracked at $150+.`
- SEO description before: `… Ships double-boxed and tracked from Victoria, Australia — free tracked postage.` (157)
- SEO description after: `… Ships double-boxed and tracked from Victoria, Australia.` (the canon line would take it to 173 > 160, so the wrong claim is dropped rather than replaced)

**Sealed** — Pokémon Abyss Eye (M5) Japanese Booster Box (10734771765526, $190)
- before: `Dispatched tracked from Victoria within 2–4 business days. Postage within Australia: $15.25 tracked, free on orders of $250 or more.`
- after: `Dispatched tracked from Victoria within 2–4 business days once it lands. Postage within Australia: $15.25 tracked, free on sealed orders of $250+.`

(Single $50+, e.g. Roronoa Zoro Alt Art OP01 $299: the Express paragraph becomes `Postage within Australia: $10.95 tracked, free tracked at $150+.`)

Payload: 637 products (601 singles < $50, 5 singles $50+, 6 slabs, 25 sealed) + 3 bundles in step 2. Gate on every new string: 0.

## Step 3 examples (before the bulk run)

| ID | Before (len) | After (len) |
|---|---|---|
| 10417121886486 | Dark Knight's Greatsword 95 FINAL FANTASY \| HOKO Collectables (61) | Dark Knight's Greatsword 95 FINAL FANTASY NM \| HOKO (51) |
| 10505277505814 | Ran and Shaw 325 Avatar: The Last Airbender \| HOKO Collectables (63) | Ran and Shaw 325 Avatar: The Last Airbender NM \| HOKO (53) |
| 10543581004054 | Dreamroot Cascade Foil 254 Secrets of Strixhaven \| HOKO Collectables (68) | Dreamroot Cascade Foil 254 Secrets of Strixhaven NM \| HOKO (58) |
| 10655243436310 | Flamekin Village 149 Commander: Lorwyn Eclipsed \| HOKO Collectables (67) | Flamekin Village 149 Commander: Lorwyn Eclipsed NM \| HOKO (57) |
| 10668896026902 | Smoldering Marsh 168 Commander: Lorwyn Eclipsed \| HOKO Collectables (67) | Smoldering Marsh 168 Commander: Lorwyn Eclipsed NM \| HOKO (57) |

300 of 301 fit at 60 with the full set (0 needed set or condition trimmed). 1 to MANUAL: "Mass of Mysteries" (10543567470870), a real MTG card whose name trips the banned-word gate.

## Step 2 plan (bundles)

| ID | Title after | Tags removed |
|---|---|---|
| 10481579065622 | MTG Card Bundle — 50 Cards incl. 5 Rares + 2 Foils (unchanged) | `mystery-pack`, `hoko-mystery` |
| 10495484952854 | Pokémon Paradox Rift Card Bundle — 10 Near Mint Cards (unchanged) | `mystery-pack` |
| 10495496454422 | Multi-Game Card Bundle — 20+ Cards (was "Ultimate TCG M… Chaos Bundle …") | `mystery-pack` |

The MTG bundle is 50 cards, NM to LP, so the "10 Near Mint Cards" pattern would misdescribe it; its current title already passes the gate and is kept. Same for the multi-game bundle (20+ cards, condition not stated). SEO title + description added on all 3 (B2 pattern, ≤60 / 50–160, no `$`). The old MTG SEO description carried "$14.95" and "random"; replaced.

## RESULTS

| Step | Result | Detail |
|---|---|---|
| 1 Postage copy | **PASS — 637/637 read back** | Backup `reports/backups/2026-10-19-postage-before.csv`, payload `…-postage-payload.jsonl`, CSV `data/postage-copy-2026-10-19.csv` (642 rows incl. the 3 bundles). 601 singles < $50 → `$3 untracked letter`; 5 singles $50+ and 6 slabs → `$10.95 tracked, free tracked at $150+`; 25 sealed → `$15.25 tracked, free on sealed orders of $250+` (+ the 2–4 "once it lands" line on Japanese sealed). Express Post removed everywhere. Bellsprout SEO description: wrong "free tracked postage" claim dropped. 0 userErrors |
| 2 Bundles | **PASS — 3/3 read back** | Backup `…-bundles-before.csv`. Tags `mystery-pack` / `hoko-mystery` removed, "Mystery Chaos" title → "Multi-Game Card Bundle — 20+ Cards", SEO title + description on all 3, "every order tracked" removed (they ship untracked letter). All 3 still ACTIVE. Banned-word gate 0 |
| 3 SEO titles | **PASS — 300/300 read back** | Backup `…-seo-titles-before.csv`. 300 of 301 rebuilt as `<card> <set> <cond> \| HOKO`, max 60, 0 needed trimming. 1 MANUAL (below). SEO titles > 60 on the store now: 1 |
| 4 Articles | **PASS** | Gate 0 + 0 prices on the final bodies, then `isPublished: true` (published 2026-10-17 12:45 UTC). Read back published. `/blogs/news/aura-seeker-m7-whats-in-the-box-and-when-it-lands` 200 · `/blogs/news/the-dominance-of-god-op-18-pre-order-guide` 200 |
| 5 Gates | **PASS** | Repo banned-word gate 0 · 86 tests OK · `python -m tools.social check` PASS 60% · full-store read-back after all writes: 0 status, 0 price, 0 inventory, 0 handle diffs; 0 description, title or SEO changes outside the payloads |

**How it was written:** the connector refuses `bulkOperationRunMutation` (safety policy), so every write was `productUpdate` through `graphql_mutation`, as aliased calls of 6–79 products. Postage ran as 3 batches (250 / 250 / 136) one after another, then SEO as 2 batches (250 / 50), with Bellsprout and the bundles written singly first. Calls are pre-built from the payload files. 3 SEO calls got a retryable `upstream_error` and went through on the retry. The full read-back above is what counts.

Counts: 940 `productUpdate` writes (637 postage + 3 bundles + 300 SEO), 2 `articleUpdate` writes, 3 bulk reads. 0 price, inventory, status, order, discount or theme writes.

## NOT CHECKED

- The storefront render of the new copy (only the Admin read-back). Shopify caches can take a few minutes.
- eBay listing copy: eBay is 403 from the cloud. If the same "Express Post $19.50" block is in eBay descriptions, it's still there.
- The live-body banned-word check on the articles was done by reading them through the API (0 hits). The repo source copies also gate at 0.

## MANUAL

**Ethan (phone or PC):**
- **Mass of Mysteries** (10543567470870): a real MTG card name that trips the banned-word gate. Its SEO title (68 chars) was left as is. Keep the card name (recommended; the rule targets pack language) and I'll shorten it next run, or change the title wording.
- "Mystical Archive" (an MTG set) and "Chaos Warp" plus 2 other MTG card names: real names, not pack language, left as they are. The gate here matched `myster(y|ies)`, not `myst*`.
- The multi-game bundle's **URL handle still says `ultimate-tcg-mystery-chaos-bundle-…`**. Changing it needs a redirect. Your call.
- The multi-game bundle body still describes a **3-point condition scale** (NM / Played / Damaged), not NM · LP · MP · HP · DMG, and says "20 years in the hobby". Not changed.
- 612 singles keep "We ship worldwide, tracked." That's accurate, but the international rates (signature required, $25 / $35 / $40) aren't stated. Add them? Your call.
- 20 Japanese sealed SEO descriptions say "tracked from Victoria in 2–4 business days" without "once it lands". Not changed (the figures match canon).

**PC:** unchanged (see QUEUE): eBay order sync, platform keys, environment setup.

## COMPLETE
