#!/usr/bin/env python3
"""
update_prices.py — Bulk price updater for HOKO Collectables Shopify store.

Reads a CSV file of product variant IDs and new prices, then updates them via
the Shopify Admin API. Always run with --dry-run first.

CSV format (no header row needed, but headers are ignored if present):
  variant_id, new_price
  e.g.:
  39012345678901, 149.99
  39012345678902, 89.00

Usage:
  python update_prices.py --csv prices.csv --dry-run   # preview only
  python update_prices.py --csv prices.csv             # apply updates

Required environment variables (or set directly below):
  SHOPIFY_STORE_URL  e.g. hoko-collectables.myshopify.com
  SHOPIFY_API_TOKEN  your Admin API access token
"""

import os
import csv
import sys
import argparse
import requests
from time import sleep

# ---------------------------------------------------------------------------
# Configuration — override via environment variables or edit directly
# ---------------------------------------------------------------------------
STORE_URL = os.getenv("SHOPIFY_STORE_URL", "hoko-collectables.myshopify.com")
API_TOKEN = os.getenv("SHOPIFY_API_TOKEN", "")
API_VERSION = "2024-01"
MIN_PRICE = 1.00   # Safety floor — reject updates below this price
MAX_PRICE = 9999.00  # Safety ceiling — reject updates above this price
RATE_LIMIT_DELAY = 0.5  # Seconds between API calls (stay under Shopify rate limit)


def get_headers():
    return {
        "X-Shopify-Access-Token": API_TOKEN,
        "Content-Type": "application/json",
    }


def validate_price(price_str):
    """Parse and validate a price string. Returns float or raises ValueError."""
    try:
        price = float(price_str)
    except ValueError:
        raise ValueError(f"Invalid price value: {price_str!r}")
    if price < MIN_PRICE:
        raise ValueError(f"Price {price} is below minimum allowed ({MIN_PRICE})")
    if price > MAX_PRICE:
        raise ValueError(f"Price {price} exceeds maximum allowed ({MAX_PRICE})")
    return round(price, 2)


def load_csv(filepath):
    """Load variant_id / new_price pairs from CSV. Skips header if present."""
    updates = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row_num, row in enumerate(reader, start=1):
            if not row or len(row) < 2:
                print(f"  [SKIP] Row {row_num}: too few columns — {row}")
                continue
            variant_id_str, price_str = row[0].strip(), row[1].strip()
            # Skip header row if present
            if variant_id_str.lower() in ("variant_id", "id", "sku"):
                continue
            try:
                variant_id = int(variant_id_str)
                price = validate_price(price_str)
                updates.append({"variant_id": variant_id, "new_price": price})
            except ValueError as e:
                print(f"  [ERROR] Row {row_num}: {e} — skipping")
    return updates


def get_variant_info(variant_id):
    """Fetch current price and title for a variant."""
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/variants/{variant_id}.json"
    resp = requests.get(url, headers=get_headers(), timeout=10)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    v = resp.json().get("variant", {})
    return {
        "id": v.get("id"),
        "title": v.get("title", "Unknown"),
        "product_id": v.get("product_id"),
        "current_price": v.get("price", "0.00"),
    }


def update_variant_price(variant_id, new_price):
    """Update the price for a single variant. Returns True on success."""
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/variants/{variant_id}.json"
    payload = {"variant": {"id": variant_id, "price": str(new_price)}}
    resp = requests.put(url, json=payload, headers=get_headers(), timeout=10)
    resp.raise_for_status()
    return True


def main():
    parser = argparse.ArgumentParser(description="Bulk update Shopify variant prices.")
    parser.add_argument("--csv", required=True, help="Path to CSV file with variant_id, new_price")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying them")
    args = parser.parse_args()

    if not API_TOKEN:
        print("ERROR: SHOPIFY_API_TOKEN is not set. Exiting.")
        sys.exit(1)

    if args.dry_run:
        print("=== DRY RUN — no prices will be changed ===")
    else:
        print("=== LIVE RUN — prices WILL be updated ===")

    print(f"Loading CSV: {args.csv}")
    updates = load_csv(args.csv)
    print(f"Found {len(updates)} valid rows.\n")

    if not updates:
        print("Nothing to do. Exiting.")
        sys.exit(0)

    success_count = 0
    error_count = 0

    for item in updates:
        variant_id = item["variant_id"]
        new_price = item["new_price"]

        # Fetch current info
        try:
            info = get_variant_info(variant_id)
        except Exception as e:
            print(f"  [ERROR] Variant {variant_id}: could not fetch info — {e}")
            error_count += 1
            continue

        if info is None:
            print(f"  [NOT FOUND] Variant {variant_id}: does not exist — skipping")
            error_count += 1
            continue

        current_price = info["current_price"]
        title = info["title"]
        print(f"  Variant {variant_id} ({title}): ${current_price} -> ${new_price:.2f}", end="")

        if args.dry_run:
            print(" [DRY RUN — not applied]")
            success_count += 1
        else:
            try:
                update_variant_price(variant_id, new_price)
                print(" [UPDATED]")
                success_count += 1
            except Exception as e:
                print(f" [ERROR: {e}]")
                error_count += 1

        sleep(RATE_LIMIT_DELAY)

    print(f"\nDone. {success_count} succeeded, {error_count} errors.")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
