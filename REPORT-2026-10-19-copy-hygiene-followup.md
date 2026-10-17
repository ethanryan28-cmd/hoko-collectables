# REPORT — 2026-10-19 · Copy hygiene follow-up (`claude/copy-hygiene-followup-1019`)

## RESULTS

| Item | Result | Detail |
|---|---|---|
| 1a Allowlist | **PASS** | New `tools/banned_words.py`: one term list (CLAUDE.md) + `ALLOWLIST` = "Mass of Mysteries", "Mystical Archive", "Chaos Warp". Names are blanked case-sensitively as whole phrases before the check. `scripts/banned-word-gate.sh` now pipes its `git grep` candidates through the module. 5 tests in `tools/tests/test_banned_words.py`: the 3 names pass (alone and in real titles); "mystery pack", "mystery box", "chaos pack", "Mystery Pack" and the old bundle title fail; lower-case "mass of mysteries", "Chaos Warping pack" and "Chaos Warp mystery pack" fail |
| 1b Mass of Mysteries SEO | **PASS — read back** | 10543567470870: `Mass of Mysteries (Borderless) Commander: Lorwyn \| HOKO Collectables` (68) → `Mass of Mysteries (Borderless) Commander: Lorwyn NM \| HOKO` (58). SEO description passed back unchanged |
| 2 Handle + 301 | **PASS** | 10495496454422 handle `ultimate-tcg-mystery-chaos-bundle-20-cards-multi-game-hoko-collectables` → `multi-game-card-bundle-20-cards` (slug was free; `redirectNewHandle: false`). Then `urlRedirectCreate` gid://shopify/UrlRedirect/786439733526. GET old → **301** to `/products/multi-game-card-bundle-20-cards`; GET new → **200**. Still ACTIVE |
| 3 Condition scale | **PASS — read back** | Same product: only the Condition Grading paragraph changed (read-back = old body with that one `<p>` swapped). The MTG bundle has no scale wording to copy (it says "Near Mint to Lightly Played"), so the new line uses the CLAUDE.md scale: `HOKO grades on the store scale <strong>NM · LP · MP · HP · DMG</strong> (Near Mint, Lightly Played, Moderately Played, Heavily Played, Damaged). Cards scanned individually; we err toward the lower grade.` |
| 4 Checks | **PASS** | Banned-word check 0 · 92 tests OK · `check` PASS 60% on all 6 · dry-run 0 invalid / 0 missing |

**Redirect pair:** `/products/ultimate-tcg-mystery-chaos-bundle-20-cards-multi-game-hoko-collectables` → `/products/multi-game-card-bundle-20-cards` (301)

**Full-store diff** (640 ACTIVE, bulk read before vs after): exactly 3 fields changed. Those are the bundle's handle, the bundle's description and Mass of Mysteries' SEO. 0 price, 0 inventory, 0 status changes, 0 other handle changes, 0 title/tag changes. Before-copies: `reports/backups/2026-10-19-followup-before.json`.

Shopify writes: 3 `productUpdate` (1 aliased call for 1b + 3, 1 for the handle) + 1 `urlRedirectCreate`. 0 payments, billing, price, discount, order or shipping-rate writes. "We ship worldwide, tracked" untouched.

## Also changed (found by the wider check)

- The old repo check only matched "myst… pack", so the new term list caught 2 real misses. Both are reworded:
  - `index.html:279` (demo storefront): "5 mystery items" → "5 hand-picked items".
  - `routines/content-strategy-multichannel.md:126`: "mystery box" removed from the show-format rotation.
- `re-pack` is now matched on a word boundary, so "pre-pack photos" (dispatch guide) no longer trips it. The check now excludes QUEUE.md, `data/*.csv` (store exports and run logs: real handles like `chaos-warp-221-…` are lower-case slugs) and the dated run scripts `scripts/shopify/*_2026_*.py` (they hold old gate regexes).
- **`check` failed at first, unrelated to this diff.** The clock rolled to 18 Oct in Victoria, which dropped a day from the window and put tiktok, pinterest and discord under 60%. `topup` refilled the window but left Discord at 8/15. The root cause: `queue_builder.build` counted past items toward the hot share, while `check` counts today onward. Fix: past items still block repeats but no longer count toward the share (`History.add(share=…)`). New test `TopupHotShare` failed before the fix and passes after. Re-ran `topup` from main's queue: Discord 9/15, all 60%.

## NOT CHECKED

- Google's view of the redirect (only the storefront GET).
- Whether any external links or eBay inserts point at the old bundle URL. The 301 covers them either way.

## MANUAL

- None for this run. The PC and Ethan items in QUEUE.md are unchanged.

## COMPLETE
