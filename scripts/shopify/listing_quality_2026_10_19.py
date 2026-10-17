"""Listing quality sweep, 2026-10-19 overnight run (read only).

Input: a bulk-operation JSONL of every ACTIVE product (products → collections, variants), downloaded from the
connector's bulkOperationRunQuery. Output: data/listing-quality-2026-10-19.csv and a markdown summary on stdout.

    python scripts/shopify/listing_quality_2026_10_19.py <active.jsonl>

Checks per product: >=1 image, description >=40 words, SEO title present and <=60, SEO description present and
50-160, productType set, >=3 tags, >=1 collection, barcode on every variant if sealed.
Value = max variant price x max(total inventory, 1).
"""
import collections
import csv
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/listing-quality-2026-10-19.csv"
CHECKS = ["image", "desc_40w", "seo_title", "seo_desc", "type_set", "tags_3", "collection", "barcode_sealed"]


def load(path):
    products, cols, variants = {}, collections.defaultdict(list), collections.defaultdict(list)
    for line in open(path, encoding="utf-8"):
        o = json.loads(line)
        parent = o.get("__parentId")
        if parent is None:
            products[o["id"]] = o
        elif "/Collection/" in o["id"]:
            cols[parent].append(o)
        else:
            variants[parent].append(o)
    return products, cols, variants


def words(desc_html):
    text = html.unescape(re.sub(r"<[^>]+>", " ", desc_html or ""))
    return len(text.split())


def is_sealed(p):
    tags = {t.lower() for t in p["tags"]}
    return "sealed" in tags or "jp-sealed" in tags or "sealed" in (p["productType"] or "").lower()


def sweep(path):
    products, cols, variants = load(path)
    rows = []
    for pid, p in products.items():
        seo_t, seo_d = p["seo"]["title"] or "", p["seo"]["description"] or ""
        vs = variants[pid]
        sealed = is_sealed(p)
        price = max((float(v["price"]) for v in vs), default=0.0)
        r = {
            "id": pid.rsplit("/", 1)[1],
            "title": p["title"],
            "handle": p["handle"],
            "product_type": p["productType"],
            "sealed": "Y" if sealed else "",
            "price_max": f"{price:.2f}",
            "inventory": p["totalInventory"],
            "value": f"{price * max(p['totalInventory'] or 0, 1):.2f}",
            "images": p["mediaCount"]["count"],
            "desc_words": words(p["descriptionHtml"]),
            "seo_title_len": len(seo_t),
            "seo_desc_len": len(seo_d),
            "tags": len(p["tags"]),
            "collections": len(cols[pid]),
            "barcodes_missing": sum(1 for v in vs if not (v.get("barcode") or "").strip()) if sealed else 0,
        }
        ok = {
            "image": r["images"] >= 1,
            "desc_40w": r["desc_words"] >= 40,
            "seo_title": 0 < r["seo_title_len"] <= 60,
            "seo_desc": 50 <= r["seo_desc_len"] <= 160,
            "type_set": bool((p["productType"] or "").strip()),
            "tags_3": r["tags"] >= 3,
            "collection": r["collections"] >= 1,
            "barcode_sealed": (not sealed) or r["barcodes_missing"] == 0,
        }
        for c in CHECKS:
            r[c] = "PASS" if ok[c] else "FAIL"
        r["fails"] = sum(1 for c in CHECKS if not ok[c])
        r["failed_checks"] = " ".join(c for c in CHECKS if not ok[c])
        rows.append(r)
    rows.sort(key=lambda r: (-r["fails"], -float(r["value"])))
    return rows


def main(path):
    rows = sweep(path)
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    n = len(rows)
    print(f"Active products: {n} · all checks PASS: {sum(1 for r in rows if r['fails'] == 0)}\n")
    print("| Check | Missing / failing | Rule |\n|---|---|---|")
    rules = {"image": ">=1 image", "desc_40w": "description >=40 words", "seo_title": "SEO title set, <=60",
             "seo_desc": "SEO description 50-160", "type_set": "productType set", "tags_3": ">=3 tags",
             "collection": ">=1 collection", "barcode_sealed": "barcode on every variant (sealed only)"}
    for c in CHECKS:
        print(f"| {c} | {sum(1 for r in rows if r[c] == 'FAIL')} | {rules[c]} |")
    bad = sorted((r for r in rows if r["fails"]), key=lambda r: -float(r["value"]))[:20]
    print("\nWorst 20 by value (listings with >=1 failing check, highest value first):\n")
    print("| # | ID | Title | Value | Fails |\n|---|---|---|---|---|")
    for i, r in enumerate(bad, 1):
        print(f"| {i} | {r['id']} | {r['title'][:70]} | ${r['value']} | {r['failed_checks']} |")


if __name__ == "__main__":
    main(sys.argv[1])
