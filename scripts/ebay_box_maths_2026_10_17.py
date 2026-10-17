"""eBay box maths for the 2026-10-17 organic-2 run. Read + compute only: writes nothing to eBay or Shopify.

Inputs:
- the 20 ACTIVE jp-sealed products (live connector read 17 Oct 2026; Shopify price, stock, policy)
- supplier yen from data/routing-2026-10-17.csv (Urara ¥ first, Kanade ¥ if no Urara row), plus the
  Urara.Chii List "Pricelist_Other" tab (16 Oct 2026) for the starter deck and the Fukuoka box
- FX 1 JPY = 0.009112 AUD (open.er-api.com, 17 Oct 2026 00:02 UTC)

`python scripts/ebay_box_maths_2026_10_17.py` writes data/ebay-box-maths-2026-10-17.csv and prints the report table.
"""
import csv
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROUTING = ROOT / "data/routing-2026-10-17.csv"
OUT = ROOT / "data/ebay-box-maths-2026-10-17.csv"

FX = 0.009112
FX_SOURCE = "open.er-api.com 2026-10-17 00:02 UTC"
FREIGHT_YEN = 6500 / 12          # bulk freight, ¥6,500 shared by 12 boxes
FVF = 0.135
PER_ORDER = 0.30
POST = 15.25
PACKAGING = 1.50
FIXED = PER_ORDER + POST + PACKAGING

# (product_id, short name, Shopify price now, stock, policy) from the connector, 17 Oct 2026
ACTIVE = [
    ("15398993723670", "30th Celebration (M6a) no-shrink", 330, 0, "CONTINUE"),
    ("10734779138326", "Storm Emeralda (M6) no-shrink", 180, 1, "CONTINUE"),
    ("10734771765526", "Abyss Eye (M5) sealed", 190, 0, "CONTINUE"),
    ("10734771798294", "Abyss Eye (M5) no-shrink", 120, 2, "CONTINUE"),
    ("15413124170006", "Nihil Zero (M3) sealed", 130, 2, "DENY"),
    ("10734773895446", "Nihil Zero (M3) no-shrink", 115, 2, "DENY"),
    ("15413124268310", "Mega Symphonia (M1S)", 175, 2, "DENY"),
    ("10734773731606", "Mega Brave (M1L)", 175, 2, "DENY"),
    ("10734773633302", "Heat Wave Arena (sv9a)", 285, 2, "DENY"),
    ("10734779433238", "Terastal Festival ex (sv8a)", 280, 2, "DENY"),
    ("10734779171094", "Super Electric Breaker (sv8)", 390, 2, "DENY"),
    ("10734779072790", "Stellar Miracle (sv7)", 210, 2, "DENY"),
    ("10734778482966", "Raging Surf (sv3a)", 245, 2, "DENY"),
    ("10734779564310", "VSTAR Universe (s12a)", 390, 2, "DENY"),
    ("10734775664918", "OP-16", 180, 0, "CONTINUE"),
    ("10734775501078", "OP-12 Legacy of the Master", 240, 2, "DENY"),
    ("10734775435542", "OP-11 A Fist of Divine Speed", 470, 1, "DENY"),
    ("10734775370006", "OP-07 500 Years in the Future", 250, 1, "DENY"),
    ("10734773862678", "Mega Gengar starter deck", 70, 1, "DENY"),
    ("15413357543702", "Pokemon Center Fukuoka special box", 230, 2, "DENY"),
]

# Not in the routing CSV: read from the Urara.Chii List (16 Oct 2026), or a flagged proxy.
EXTRA_YEN = {
    "10734773862678": (3500, "Urara 16 Oct (Pricelist_Other: Mega Gengar Starter Deck, stock 20)"),
    "15413357543702": (14000, "Urara 16 Oct (Pricelist_Other: Pokemon Center Fukuoka, price listed, stock '-')"),
    "10734773895446": (8580, "PROXY: no no-shrink price at Urara or Kanade; uses Kanade M3 sealed ¥8,580 (upper bound)"),
}


def up5(x):
    return math.ceil(x / 5) * 5


def ebay_net(price):
    return price * (1 - FVF) - FIXED


def price_for_net(target):
    return (target + FIXED) / (1 - FVF)


def supplier_yen():
    out = {}
    with ROUTING.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["urara_yen"]:
                out[r["product_id"]] = (int(r["urara_yen"]), "Urara (routing CSV)")
            elif r["kanade_yen"]:
                out[r["product_id"]] = (int(r["kanade_yen"]), "Kanade (routing CSV; no Urara row)")
    out.update(EXTRA_YEN)
    return out


def rows():
    yen = supplier_yen()
    for pid, name, shop_price, stock, policy in ACTIVE:
        y, src = yen.get(pid, (None, "MISSING"))
        landed = (y + FREIGHT_YEN) * FX if y is not None else None
        r = {"product_id": pid, "box": name, "stock": stock, "policy": policy,
             "supplier_yen": y if y is not None else "", "yen_source": src,
             "freight_yen_per_box": round(FREIGHT_YEN, 2), "fx_jpy_aud": FX, "fx_source": FX_SOURCE,
             "landed_bulk_aud": round(landed, 2) if landed is not None else ""}
        if landed is None:
            yield r
            continue
        net = ebay_net(shop_price)
        p10, p18 = price_for_net(landed * 1.10), price_for_net(landed * 1.18)
        r.update({
            "gst_10pct_aud_flag": round(landed * 0.10, 2),
            "consignment_of_12_over_1000": "Y" if landed * 12 > 1000 else "N",
            "shopify_price_now": shop_price,
            "ebay_price_now": "NOT CHECKED",
            "ebay_price_used": shop_price,
            "ebay_price_source": "Shopify stand-in (no eBay active-listings export in the cloud)",
            "ebay_net_at_price": round(net, 2),
            "margin_at_shopify_price_aud": round(net - landed, 2),
            "margin_at_shopify_price_pct": round((net - landed) / landed * 100, 1),
            "breakeven_ebay_price": round(price_for_net(landed), 2),
            "ebay_price_plus10": round(p10, 2),
            "ebay_price_plus18": round(p18, 2),
            "ebay_price_plus10_up5": up5(p10),
            "ebay_price_plus18_up5": up5(p18),
            "shopify_price_clears_plus10_on_ebay": "Y" if shop_price >= p10 else "N",
            "ebay_last_sold": "NOT CHECKED (ebay.com.au 403 from the cloud)",
        })
        yield r


def main():
    data = sorted(rows(), key=lambda r: r.get("margin_at_shopify_price_aud", -1e9), reverse=True)
    fields = list(dict.fromkeys(k for r in data for k in r))
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(data)
    blank = [r["box"] for r in data if r["landed_bulk_aud"] == ""]
    print(f"{len(data)} rows → {OUT.relative_to(ROOT)}; blank landed: {blank or 'none'}")
    print("| # | Box | Yen (source) | Landed bulk | GST 10% flag | Shopify | eBay net @ Shopify | Margin $ | Margin % "
          "| Breakeven | +10% | +18% | Shopify clears +10%? |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(data, 1):
        src = r["yen_source"].split(" ")[0].rstrip(":")
        print(f"| {i} | {r['box']} | ¥{r['supplier_yen']:,} ({src}) | ${r['landed_bulk_aud']:.2f} | "
              f"${r['gst_10pct_aud_flag']:.2f} | ${r['shopify_price_now']} | ${r['ebay_net_at_price']:.2f} | "
              f"${r['margin_at_shopify_price_aud']:.2f} | {r['margin_at_shopify_price_pct']}% | "
              f"${r['breakeven_ebay_price']:.2f} | ${r['ebay_price_plus10']:.2f} | ${r['ebay_price_plus18']:.2f} | "
              f"{r['shopify_price_clears_plus10_on_ebay']} |")


if __name__ == "__main__":
    main()
