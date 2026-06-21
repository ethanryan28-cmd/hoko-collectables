#!/usr/bin/env python3
"""
check_inventory.py — Read-only inventory audit for HOKO Collectables Shopify store.

Finds active product variants with zero inventory that are still published
(visible to buyers). Prints a report and saves a CSV.

This is a READ-ONLY script — it makes no changes to the store.

Usage:
  python check_inventory.py
  python check_inventory.py --min-price 50   # only flag items priced above $50
  python check_inventory.py --csv-out out.csv

Required environment variables (or set directly below):
  SHOPIFY_STORE_URL  e.g. hoko-collectables.myshopify.com
  SHOPIFY_API_TOKEN  your Admin API access token (read-only scopes are sufficient)
"""

import os
import csv
import sys
import argparse
import requests
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
STORE_URL = os.getenv("SHOPIFY_STORE_URL", "hoko-collectables.myshopify.com")
API_TOKEN = os.getenv("SHOPIFY_API_TOKEN", "")
API_VERSION = "2024-01"
DEFAULT_CSV_OUT = f"inventory-check-{datetime.now().strftime('%Y%m%d')}.csv"


def get_headers():
    return {
        "X-Shopify-Access-Token": API_TOKEN,
        "Content-Type": "application/json",
    }


def fetch_active_products():
    """Fetch all active (published) products with their variants."""
    products = []
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products.json"
    params = {"status": "active", "limit": 250}

    while url:
        resp = requests.get(url, headers=get_headers(), params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        products.extend(data.get("products", []))

        # Handle pagination via Link header
        link = resp.headers.get("Link", "")
        next_url = None
        if "rel=\"next\"" in link:
            for part in link.split(","):
                if "rel=\"next\"" in part:
                    next_url = part.strip().split(";")[0].strip("<>").strip()
        url = next_url
        params = {}  # params only needed for first request

    return products


def get_inventory_levels(inventory_item_ids):
    """Fetch inventory levels for a batch of inventory item IDs."""
    if not inventory_item_ids:
        return {}

    ids_str = ",".join(str(i) for i in inventory_item_ids)
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/inventory_levels.json"
    params = {"inventory_item_ids": ids_str, "limit": 250}
    resp = requests.get(url, headers=get_headers(), params=params, timeout=15)
    resp.raise_for_status()

    levels = {}
    for level in resp.json().get("inventory_levels", []):
        iid = level["inventory_item_id"]
        qty = level.get("available", 0) or 0
        levels[iid] = levels.get(iid, 0) + qty  # sum across locations

    return levels


def main():
    parser = argparse.ArgumentParser(description="Check for zero-inventory active Shopify variants.")
    parser.add_argument("--min-price", type=float, default=0,
                        help="Only flag variants priced at or above this amount (default: 0 = all)")
    parser.add_argument("--csv-out", default=DEFAULT_CSV_OUT,
                        help="Output CSV filename")
    args = parser.parse_args()

    if not API_TOKEN:
        print("ERROR: SHOPIFY_API_TOKEN is not set. Exiting.")
        sys.exit(1)

    print(f"Fetching active products from {STORE_URL}...")
    products = fetch_active_products()
    print(f"Found {len(products)} active products.")

    # Collect all variants
    all_variants = []
    for product in products:
        for variant in product.get("variants", []):
            price = float(variant.get("price", 0) or 0)
            if price < args.min_price:
                continue
            all_variants.append({
                "product_id": product["id"],
                "product_title": product["title"],
                "variant_id": variant["id"],
                "variant_title": variant.get("title", "Default"),
                "sku": variant.get("sku", ""),
                "price": price,
                "inventory_item_id": variant.get("inventory_item_id"),
                "inventory_management": variant.get("inventory_management", ""),
            })

    print(f"Checking inventory for {len(all_variants)} variants...")

    # Fetch inventory in batches of 50 (API limit)
    BATCH_SIZE = 50
    inventory_map = {}
    tracked_items = [v for v in all_variants if v["inventory_management"] == "shopify"]
    item_ids = [v["inventory_item_id"] for v in tracked_items if v["inventory_item_id"]]

    for i in range(0, len(item_ids), BATCH_SIZE):
        batch = item_ids[i:i + BATCH_SIZE]
        batch_levels = get_inventory_levels(batch)
        inventory_map.update(batch_levels)

    # Find zero-inventory variants
    zero_stock = []
    for v in all_variants:
        inv_id = v["inventory_item_id"]
        if v["inventory_management"] != "shopify":
            continue  # not tracked by Shopify
        qty = inventory_map.get(inv_id, 0)
        if qty <= 0:
            zero_stock.append({**v, "available_qty": qty})

    # Report
    print(f"\n=== ZERO-INVENTORY ACTIVE VARIANTS ===")
    if not zero_stock:
        print("None found. All tracked active variants have stock.")
    else:
        print(f"Found {len(zero_stock)} variant(s) with zero (or negative) inventory:\n")
        for item in zero_stock:
            print(f"  [{item['sku'] or 'no-sku'}] {item['product_title']} — {item['variant_title']} | Price: ${item['price']:.2f} | Qty: {item['available_qty']}")

        # Write CSV
        fieldnames = ["product_id", "product_title", "variant_id", "variant_title", "sku", "price", "available_qty"]
        with open(args.csv_out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in zero_stock:
                writer.writerow({k: item[k] for k in fieldnames})
        print(f"\nSaved to: {args.csv_out}")

    print(f"\nDone. {len(zero_stock)} zero-stock variants out of {len(all_variants)} checked.")

    if zero_stock:
        sys.exit(1)  # non-zero exit if issues found (useful for CI/scripts)


if __name__ == "__main__":
    main()
