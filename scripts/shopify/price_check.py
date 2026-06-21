"""
price_check.py -- Read-only Shopify price audit for HOKO Collectables

Fetches all active Shopify products and flags any priced below a threshold.
Use this as a safety net to catch listings accidentally priced too low.

READ-ONLY: this script makes no changes to your store.

Setup (Windows, one-time):
  winget install Python.Python.3.12
  pip install requests

Run:
  # Set credentials for this PowerShell session only
  $env:SHOPIFY_STORE = "hokocollectables.myshopify.com"
  $env:SHOPIFY_ADMIN_TOKEN = "shpat_xxxxxxxxxxxxxxxxxxxx"

  python price_check.py

  # Optional: custom threshold (default: $50 AUD)
  python price_check.py --threshold 100

Output: prints flagged products and saves price_check_results_TIMESTAMP.csv

Note: requires read_products scope. See archive_cheap_singles.py for token setup.
"""

import os
import sys
import csv
import argparse
import requests
from datetime import datetime

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

STORE = os.environ.get("SHOPIFY_STORE", "")
TOKEN = os.environ.get("SHOPIFY_ADMIN_TOKEN", "")
API_VERSION = "2024-01"

def api_url(endpoint: str) -> str:
    return f"https://{STORE}/admin/api/{API_VERSION}/{endpoint}"

HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json",
}

# ---------------------------------------------------------------------------
# Fetch products (paginated)
# ---------------------------------------------------------------------------

def fetch_active_products() -> list:
    products = []
    url = api_url("products.json")
    params = {"status": "active", "limit": 250, "fields": "id,title,variants,product_type"}

    while url:
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()
        products.extend(data.get("products", []))

        link_header = resp.headers.get("Link", "")
        next_url = None
        for part in link_header.split(","):
            part = part.strip()
            if 'rel="next"' in part:
                next_url = part.split(";")[0].strip().strip("<>")
        url = next_url
        params = {}

    return products

# ---------------------------------------------------------------------------
# Price audit
# ---------------------------------------------------------------------------

def audit_prices(products: list, threshold: float) -> list:
    flagged = []
    for product in products:
        for variant in product.get("variants", []):
            price = float(variant.get("price", 0))
            if price < threshold and price > 0:
                flagged.append({
                    "product_id": product["id"],
                    "title": product["title"],
                    "variant_id": variant["id"],
                    "sku": variant.get("sku", ""),
                    "price_aud": price,
                    "product_type": product.get("product_type", ""),
                })
    return sorted(flagged, key=lambda x: x["price_aud"])

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_results(flagged: list, threshold: float) -> None:
    if not flagged:
        print(f"\n OK  No active products found priced below AUD ${threshold:.2f}")
        return
    print(f"\n WARN  {len(flagged)} variant(s) priced below AUD ${threshold:.2f}:\n")
    print(f"{'Price':>10}  {'SKU':<20}  {'Title'}")
    print("-" * 80)
    for item in flagged:
        print(f"AUD {item['price_aud']:>7.2f}  {item['sku']:<20}  {item['title']}")

def save_csv(flagged: list) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"price_check_results_{ts}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["price_aud","sku","title","product_type","product_id","variant_id"])
        writer.writeheader()
        writer.writerows(flagged)
    return filename

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="HOKO Collectables -- read-only price audit")
    parser.add_argument("--threshold", type=float, default=50.0,
                        help="Flag products priced below this AUD amount (default: 50.0)")
    args = parser.parse_args()

    if not STORE or not TOKEN:
        print("Error: set SHOPIFY_STORE and SHOPIFY_ADMIN_TOKEN environment variables.")
        sys.exit(1)

    print(f"Fetching active products from {STORE}...")
    products = fetch_active_products()
    print(f"Found {len(products)} active products.")

    flagged = audit_prices(products, args.threshold)
    print_results(flagged, args.threshold)

    if flagged:
        csv_file = save_csv(flagged)
        print(f"\nResults saved to: {csv_file}")
        print("\nReview the list. If any are priced incorrectly, update in Shopify admin.")
        print("Pricing rule: replacement cost + margin, not historical purchase price.")
        sys.exit(1)

if __name__ == "__main__":
    main()
