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
