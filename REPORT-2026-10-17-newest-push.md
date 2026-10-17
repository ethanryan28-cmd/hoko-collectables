# REPORT — 2026-10-17 newest push (`claude/newest-push-1017`)

Unattended run. Authorised: product copy writes, archiving one duplicate DRAFT, article publishing. Every write backed up to `reports/backups/` and read back. No price, discount, order or fulfilment changes.

## Summary

| Step | Result |
|---|---|
| 0 State | PASS — nothing already done; M6a confirmed ACTIVE $330 CONTINUE (backup `reports/backups/2026-10-17-m6a-activate.json`) |
| 1 M6a copy to canon | PASS |
| 2 OP-17 duplicate | PASS — kept 10734775730454, archived 15402647453974, 301 live |
| 3 Source without the PC token | PASS — gate met after two fixes (3 clips rendered, eligibility rule for CONTINUE boxes) |
| 4 Two articles | PASS — both published, both return 200 |
| 5 Wrap | PASS |

## Step 1 — M6a copy to canon (15398993723670)
- Before: older template (pre-order line, "small batches", "$15.25 added at checkout", no cutoff/authenticity/spot-a-fake). Backup `reports/backups/2026-10-17-m6a-copy-before.json`.
- After (`productUpdate`, read back): cutoff block (7 Dec), proof line, authenticity line, bullets — authentic print · outer shrink removed, inner packs factory sealed · **20 packs per box, 6 cards per pack** · "Import freight from Japan is included in the price. Dispatched tracked from Victoria within 2–4 business days once it lands. Postage within Australia: $15.25 tracked, free on orders of $250 or more." · origin Japan — spot-a-fake block (incl. the no-shrink line), guide link, returns paragraph.
- Tags: `label:NEEDS-COMP` removed (now `booster-box game:pokemon japanese jp-sealed latest-set moq-6 no-shrink pokemon route:urara-batch sealed set:M6a`). SEO description was null → set. Status, price, policy untouched.

## Step 2 — OP-17 duplicate
- Kept **10734775730454** `one-piece-tcg-op-17-sealed-japanese-booster-box` (cleaner handle, 3 images incl. the white-background packshot, canon copy, $200, SKU DS-URA-OP17-0049). DRAFT, unchanged.
- Archived **15402647453974** `one-piece-op-17-the-worlds-strongest-warriors-sealed-japanese-booster-box-pre-order` (no images, older copy, $175, SKU HOKO-JP-OP17). Backup `reports/backups/2026-10-17-op17-duplicate-archive-before.json`. Read back: ARCHIVED.
- 301: UrlRedirect 786389729558 `/products/one-piece-op-17-…-pre-order` → `/products/one-piece-tcg-op-17-sealed-japanese-booster-box`. Storefront returns 301 to the kept handle.

## Step 3 — Product source without the PC token
- `content/youtube/sealed/source.csv` rebuilt from the connector with the same columns as `run.py source` (query: ACTIVE `jp-sealed` + pre-order drafts with an image): **20 ACTIVE** (18 boxes + Mega Gengar starter deck + Fukuoka special box, incl. M5 sealed, OP-16, M6a) **+ 2 pre-order drafts** (OP-18, EB-05; M7/FB12 have no image so are skipped, as `run.py` would). Existing `release_date`, `chase`, `packs`, `reel_images` values preserved by product ID.
- `content/youtube/slabs/source.csv` rebuilt: 6 ACTIVE PSA/BGS slabs (unchanged set).
- New column **`policy`** (inventoryPolicy). `tools/social/assets.py::product_eligible` now treats 0 stock as unbuyable only when policy is DENY; CONTINUE boxes (M6a, M5 sealed, M5 NOS, OP-16, M6 NOS) are promotable. `content/youtube/hoko/source.py` now emits `policy` so the PC run matches.
- Latent bug fixed on the way: a BF/Xmas beat whose featured box is no longer in `source.csv` was treated as eligible; it is now ineligible (`not in sealed/source.csv`). The 26 Nov Inferno X beat stays out of the queue.
- Clips: the 3 newly ACTIVE boxes had no reel at all, so `run.py reel sealed <id> --hook 1` was run in the cloud for 15398993723670, 10734771765526, 10734775664918 (Piper fallback voice, ~11 s each; mp4s are gitignored, sidecar json/caption committed).
- Calendar statuses-only rebuild: 72 rows. Queue rebuilt (`python -m tools.social build`, nothing had been posted yet; before-copy in scratch): 165 items, 15 days on all 6 platforms, `check` PASS.
- **GATE:** every one of the 20 live boxes referenced within 14 days — **20/20**. M6a first slot **19 Oct** (within 3 days); M5 sealed 17 Oct; OP-16 19 Oct. Violations 0. Pre-order drafts referenced 0 times. Tests 43 passed. PASS.

## Step 4 — Articles (blog `news`, byline Ethan Ryan, published)
| Article | ID | URL |
|---|---|---|
| Pokémon 30th Celebration (M6a) Japanese Booster Box — Australia Buying Guide 2026 | 688481501462 | https://www.hokocollectables.com/blogs/news/pokemon-30th-celebration-m6a-japanese-booster-box-australia-buying-guide-2026 |
| One Piece Heroines Edition vol.2 (EB-05) — What to Expect, Release Date and Pre-order in Australia | 688481534230 | https://www.hokocollectables.com/blogs/news/one-piece-heroines-edition-vol-2-eb-05-release-date-pre-order-australia |

Both: SEO title/description via `global.title_tag` / `global.description_tag`, tags, summary, internal links to the spot-a-fake guide (`how-to-spot-fake-pokemon-cards`), Japanese-vs-English (`japanese-vs-english-pokemon-cards`), the 2026 JP boxes guide, the product and `japan-direct-sealed`. No prices in the body (the $250 free-postage threshold is the canon postage line, not a product price). Both read back `isPublished: true` and return HTTP 200. No card-level claims or pull rates were invented; M6a facts limited to set code, month, 20×6 counts; EB-05 facts from Bandai's product page (31 Oct, 6 cards, 75 + 2 DON!!, rarity split).

## Banned words
0 on everything touched. One grep hit is the Shopify CDN filename of the M6a packshot (`…-official-white.jpg`) inside `source.csv`, not copy.

## NOT CHECKED
- `run.py source` itself still not run in the cloud (no token); the CSVs were built from the connector with the same query logic.
- The 3 cloud clips use the Piper en_GB fallback voice.
- Whether Shopify's article `publishDate` matched local time (published immediately, 03:34Z).

## MANUAL
**PC only:** re-voice the 3 new clips in en-AU with `--force` if wanted; `run.py source` now writes the `policy` column.
**Ethan only:** nothing blocking.

## COMPLETE
