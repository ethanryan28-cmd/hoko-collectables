"""
HOKO Collectables — Shopify cheap-singles archiver.

Finds every active product whose entire price range is under AUD $30, then
optionally archives them. Safe by default — dry-run produces a CSV you review
before any change is made. Archiving requires a typed 'archive' confirmation.

Strategy (post May 2026 pivot to sealed-only):
HOKO no longer sources new singles. Existing premium singles are allowed to
sell through naturally on Shopify, but cheap singles (under AUD $30) drag the
brand toward "discount bin" perception. This script archives them in bulk so
the Shopify catalogue presents as sealed + graded only. Reversible — archived
products can be reactivated from Shopify admin at any time.

Usage (PowerShell on Windows):
    $env:SHOPIFY_STORE = "hokocollectables.myshopify.com"
    $env:SHOPIFY_ADMIN_TOKEN = "shpat_xxxxxxxxxxxxxxxxxxxx"

    # Step 1 — dry run, writes candidates.csv. No changes made.
    python archive_cheap_singles.py

    # Step 2 — review candidates.csv. If happy, run with --execute.
    python archive_cheap_singles.py --execute

Dependencies: pip install requests
"""

import argparse
import csv
import os
import sys
import time

import requests

THRESHOLD_AUD = 30.0
API_VERSION = "2024-10"  # bump to latest Shopify API version when convenient
PAGE_SIZE = 100
RATE_LIMIT_SLEEP = 0.5

STORE = os.environ.get("SHOPIFY_STORE")
TOKEN = os.environ.get("SHOPIFY_ADMIN_TOKEN")

if not STORE or not TOKEN:
    sys.exit("Set SHOPIFY_STORE and SHOPIFY_ADMIN_TOKEN environment variables first.")

ENDPOINT = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json",
}

LIST_QUERY = """
query Products($first: Int!, $after: String) {
  products(first: $first, after: $after, query: "status:active") {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        title
        handle
        status
        totalInventory
        priceRangeV2 {
          maxVariantPrice { amount currencyCode }
          minVariantPrice { amount currencyCode }
        }
      }
    }
  }
}
"""

ARCHIVE_MUTATION = """
mutation ArchiveProduct($input: ProductInput!) {
  productUpdate(input: $input) {
    product { id status }
    userErrors { field message }
  }
}
"""


def gql(query, variables):
    response = requests.post(
        ENDPOINT, headers=HEADERS, json={"query": query, "variables": variables}, timeout=30
    )
    response.raise_for_status()
    body = response.json()
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]


def find_candidates():
    after = None
    while True:
        data = gql(LIST_QUERY, {"first": PAGE_SIZE, "after": after})
        page = data["products"]
        for edge in page["edges"]:
            product = edge["node"]
            price_range = product["priceRangeV2"]
            max_price = float(price_range["maxVariantPrice"]["amount"])
            currency = price_range["maxVariantPrice"]["currencyCode"]
            if currency != "AUD":
                continue
            if max_price < THRESHOLD_AUD:
                yield product
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
        time.sleep(RATE_LIMIT_SLEEP)


def write_csv(candidates, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "handle", "max_price_aud", "min_price_aud", "inventory"])
        for product in candidates:
            price_range = product["priceRangeV2"]
            writer.writerow([
                product["id"],
                product["title"],
                product["handle"],
                price_range["maxVariantPrice"]["amount"],
                price_range["minVariantPrice"]["amount"],
                product.get("totalInventory") or 0,
            ])


def archive_all(candidates):
    archived = 0
    for product in candidates:
        result = gql(ARCHIVE_MUTATION, {"input": {"id": product["id"], "status": "ARCHIVED"}})
        errors = result["productUpdate"]["userErrors"]
        if errors:
            print(f"  ERROR  {product['handle']}: {errors}")
        else:
            archived += 1
            print(f"  archived: {product['title']}")
        time.sleep(RATE_LIMIT_SLEEP)
    return archived


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually archive products. Without this flag, runs as dry-run.",
    )
    args = parser.parse_args()

    print(f"Scanning {STORE} for active products under AUD ${THRESHOLD_AUD:.2f}...")
    candidates = list(find_candidates())
    print(f"Found {len(candidates)} candidates.")

    csv_path = "candidates.csv"
    write_csv(candidates, csv_path)
    print(f"Wrote {csv_path}.")

    if not args.execute:
        print("\nDry-run complete. Review candidates.csv, then re-run with --execute.")
        return

    confirm = input(
        f"\nAbout to ARCHIVE {len(candidates)} products. Type 'archive' to confirm: "
    )
    if confirm.strip().lower() != "archive":
        print("Aborted — no changes made.")
        return

    archived = archive_all(candidates)
    print(f"\nDone. Archived {archived}/{len(candidates)}.")


if __name__ == "__main__":
    main()
