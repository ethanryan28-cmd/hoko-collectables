"""
list_active_products.py

Read-only script that fetches all active Shopify products and exports them to a CSV.
Useful for cross-referencing with eBay listings, repricing runs, and stock audits.

Usage:
    python list_active_products.py
    python list_active_products.py --output active_products.csv
    python list_active_products.py --type 'Graded Card'
    python list_active_products.py --type 'Sealed TCG'
"""

import os
import csv
import sys
import time
import argparse
import requests
from datetime import datetime


def get_env():
    store = os.getenv('SHOPIFY_STORE')
    token = os.getenv('SHOPIFY_TOKEN')
    if not store or not token:
        print('Error: SHOPIFY_STORE and SHOPIFY_TOKEN environment variables required.')
        print('Set them in your .env file or export them before running.')
        sys.exit(1)
    return store, token


def fetch_active_products(store, token, product_type=None):
    """Fetch all active products from Shopify, handling pagination."""
    headers = {'X-Shopify-Access-Token': token}
    base_url = f'https://{store}/admin/api/2024-01/products.json'
    params = {
        'status': 'active',
        'limit': 250,
    }
    if product_type:
        params['product_type'] = product_type

    products = []
    page_info = None

    while True:
        if page_info:
            params['page_info'] = page_info
            params.pop('status', None)
            params.pop('product_type', None)

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 429:
            print('Rate limited — waiting 2 seconds...')
            time.sleep(2)
            continue

        if response.status_code != 200:
            print(f'Error {response.status_code}: {response.text}')
            sys.exit(1)

        data = response.json()
        batch = data.get('products', [])
        products.extend(batch)

        link_header = response.headers.get('Link', '')
        if 'rel="next"' in link_header:
            import re
            match = re.search(r'page_info=([^&>]+)', link_header)
            page_info = match.group(1) if match else None
            if not page_info:
                break
        else:
            break

        time.sleep(0.5)

    return products


def flatten_products(products):
    """Flatten products to one row per variant."""
    rows = []
    for product in products:
        for variant in product.get('variants', []):
            rows.append({
                'product_id': product['id'],
                'product_title': product['title'],
                'product_type': product.get('product_type', ''),
                'vendor': product.get('vendor', ''),
                'status': product.get('status', ''),
                'variant_id': variant['id'],
                'sku': variant.get('sku', ''),
                'price': variant.get('price', ''),
                'inventory_quantity': variant.get('inventory_quantity', 0),
                'created_at': product.get('created_at', ''),
                'updated_at': product.get('updated_at', ''),
            })
    return rows


def main():
    parser = argparse.ArgumentParser(description='List active Shopify products')
    parser.add_argument('--output', default=None,
                        help='Output CSV filename (default: active_products_YYYYMMDD.csv)')
    parser.add_argument('--type', default=None, dest='product_type',
                        help='Filter by product type (e.g. "Graded Card", "Sealed TCG")')
    args = parser.parse_args()

    store, token = get_env()

    print(f'Fetching active products from {store}...')
    if args.product_type:
        print(f'Filtering by type: {args.product_type}')

    products = fetch_active_products(store, token, args.product_type)
    rows = flatten_products(products)

    print(f'Found {len(products)} products ({len(rows)} variants)')

    if not rows:
        print('No active products found.')
        return

    output_file = args.output or f'active_products_{datetime.now().strftime("%Y%m%d")}.csv'

    fieldnames = ['product_id', 'product_title', 'product_type', 'vendor', 'status',
                  'variant_id', 'sku', 'price', 'inventory_quantity', 'created_at', 'updated_at']

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'Exported to: {output_file}')


if __name__ == '__main__':
    main()
