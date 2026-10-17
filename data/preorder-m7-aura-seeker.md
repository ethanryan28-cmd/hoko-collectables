# Pre-order spec: Pokémon M7 Aura Seeker (Japanese) — 17 Oct 2026

## Product

| Field | Value |
|---|---|
| Set | **Aura Seeker** (M7), Mega Evolution series. Japanese trademark name **Hadou Seeker (ハドウシーカー)**. Star card reported as Mega Lucario Z ex. |
| Release (JP) | **27 Nov 2026**. This date is reported but not yet confirmed by The Pokémon Company. |
| Shopify | **DRAFT already existed** (created 11 Oct): `gid://shopify/Product/15417947455766`, handle `pre-order-pokemon-hadou-seeker-m7-sealed-japanese-booster-box`, SKU `PRE-URA-M7-BOX`, qty 6 (tag `moq-6`), policy DENY, supplier metafield `Urara.Chii`. No duplicate was created. |
| Price | **$190.00. Unchanged.** |
| Edited today (draft only, still DRAFT) | Title `[PRE-ORDER] Pokemon Hadou Seeker (M7)…` → `[PRE-ORDER] Pokemon Aura Seeker (M7) Sealed Japanese Booster Box`. The description now leads with **"Pre-order — dispatched tracked from Victoria once it lands"**, 1.4K → 1.5K, and the Hadou Seeker name added. The release line was changed from "within 2–4 business days of Japanese release" to "once it lands". SEO title/description updated. Handle is unchanged, so the content-machine links still work. |

## Landed cost (Urara.Chii)

**M7 is not on the Urara.Chii price list yet.** The sheet "Urara.Chii List", Pricelist_Pokemon, dated 16 Oct 2026, starts at M6a.
**[FILL IN: Urara M7 yen quote]** once it appears, then re-run the maths below.

FX: 1 JPY = **0.009145 AUD** (open.er-api.com, 16 Oct 2026 00:02 UTC).

Calibration against what HOKO already prices off the same list (yen × FX = goods cost, before freight):

| Box | Urara ¥ (16 Oct) | Goods A$ | HOKO price | Price ÷ goods |
|---|---|---|---|---|
| Abyss Eye M5 · no shrink | 9,000 | 82.31 | 120 | 1.46× |
| Storm Emeralda M6 · no shrink | 9,300 | 85.05 | 180 | 2.12× |
| Ninja Spinner M4 · no shrink | 8,000 | 73.16 | (not listed) | — |
| Mega Gengar starter deck | 3,500 | 32.01 | 70 | 2.19× |
| Pokémon Center Fukuoka box | 14,000 | 128.03 | 230 | 1.80× |

### Cost model per box (assumptions marked)

- Goods = Urara ¥ × 0.009145
- Freight JP → VIC: **A$14.00/box (ASSUMPTION)**. No freight figure exists in the repo, Drive, Notion or Gmail. This is a placeholder for a 6-box carton by EMS/air of roughly A$84. Replace it with the real invoice figure.
- Card fees: Shopify Payments AU domestic 1.75% + A$0.30 = **A$3.63** at $190.
- GST: **not modelled (NOT CHECKED: HOKO's GST registration status).** If registered, 1/11 of the $190 (A$17.27) comes off every scenario below, and the breakeven drops to ~¥16,960.
- Customer pays postage ($15.25 tracked) unless the order is $250+. Free post on a single $190 box doesn't apply.

**Breakeven Urara price at $190:** (190 − 3.63 − 14.00) ÷ 0.009145 = **¥18,849**.

| Urara M7 quote (scenario) | Landed A$ (goods + freight) | Fees | Margin per box at $190 | Margin % |
|---|---|---|---|---|
| ¥14,000 | 142.03 | 3.63 | **+44.34** | 23% |
| ¥15,500 | 155.75 | 3.63 | **+30.62** | 16% |
| ¥17,000 | 169.47 | 3.63 | **+16.90** | 9% |
| ¥18,000 (JP retail pre-order price, see comps) | 178.61 | 3.63 | **+7.76** | 4% |

**GATE (margin positive): PASS, conditional.** Margin is positive for any Urara quote up to ¥18,849. A wholesale quote above the JP *retail* pre-order price (¥18,000) is unlikely, but it's not verified until Urara lists M7.
If the quote lands above ~¥16,500, margin falls under 10%. At that point principle 1 (replacement cost) says reprice to market (≈$199–219, see comps) before the 6 sell through.

## Comp check (17 Oct 2026)

| Seller | Where | Listing | Price |
|---|---|---|---|
| FUDAKURA (JP → AU wholesale) | fudakura-australia.com/index.php?p=product&id=aura-seeker-booster-box | "Aura Seeker (Hadou Seeker) Booster Box", pre-order, releases Nov 2026 | **A$184.57 single**, A$176.17 (6–17), A$166.44 (18–35), A$157.78 (36+). Wholesale, shipping extra (free over A$3,000) |
| Krystal Kollectz (AU) | krystalkollectz.com/products/japanese-aura-seeker-m7-pokemon-booster-box | "Japanese \| Aura Seeker M7 - Pokémon Booster Box \| PRE-ORDER" | listed, **price not set (A$0.00)** |
| PokeNinJapan (JP retailer) | pokeninjapan.store/products/pre-order-box-aura-seeker-japanese-pokemon-card-booster-box | "Pre-order {M7 BOX} Aura Seeker" | **¥18,000** (≈ A$164.61) + intl shipping |
| Pokebox (AU) | pokebox.com.au (search "aura seeker") | no M7 listing yet. Reference Mega boxes: MEGA Dream ex $164.95, Storm Emerald $139.95, Mega Brave (no shrink) $109.95 | — |
| GD Games (AU) | gdgames.com.au | no M7 listing found (Mega Dream ex box page exists) | — |

**Read:** an AU reseller buying one box from the cheapest wholesale source pays ~A$185 plus shipping. HOKO at **$190 delivered-to-Victoria** is at market, not under it (principle 2), and leaves room if Urara comes in at or below ~¥17,000.
**Recommendation:** hold $190 (no change made). Reprice only after the Urara M7 quote, per the table above.

## Copy (live on the draft)

- Lead line: **Pre-order — dispatched tracked from Victoria once it lands.**
- No "direct from Japan" escalation beyond the existing "direct from our Japanese distributor". That line was already on every Urara product.

## To publish (Ethan)

1. Get the Urara M7 yen quote and fill in `[FILL IN]` above. Confirm margin > 0 with the real freight figure.
2. Add a product photo (Shopify → product → Media). The content machine swaps the text-card reel for it: `python content/youtube/run.py reel sealed 15417947455766 --force`.
3. Set status ACTIVE. Then `python content/youtube/run.py source` and `python -m tools.social topup`, which puts it in the social queue. The pre-order roundup unblocks too.

Sources: [PokeNinJapan M7 pre-order](https://www.pokeninjapan.store/products/pre-order-box-aura-seeker-japanese-pokemon-card-booster-box) · [Krystal Kollectz M7](https://krystalkollectz.com/products/japanese-aura-seeker-m7-pokemon-booster-box) · [FUDAKURA Aura Seeker](https://fudakura-australia.com/) · [Pokebox Japanese boxes](https://www.pokebox.com.au/collections/japanese-pokemon-tcg-booster-boxes) · [GD Games Japanese](https://www.gdgames.com.au/collections/japanese-pokemon-tcg) · [Samurai Sword Tokyo release calendar](https://samuraiswordtokyo.com/pages/release-calendar) · Urara.Chii List (Google Sheet, 16 Oct 2026) · open.er-api.com JPY rates (16 Oct 2026)
