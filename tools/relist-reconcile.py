#!/usr/bin/env python3
"""Relist reconcile: which ended-unsold eBay listings are safe to relist? Read-only. Never relists, never
changes a price. Produces two CSVs for Ethan to act on by hand in Seller Hub.

  python tools/relist-reconcile.py --unsold unsold.csv --active active.csv --orders orders.csv \
      --shopify inventory.csv [--out-dir data/relist] [--since 2026-09-01]

Inputs (Seller Hub / Shopify exports; header row is auto-detected, preamble lines are skipped):
  --unsold   eBay Seller Hub → Listings → Unsold → Download (Item number, Title, Custom label (SKU), price, End date)
  --active   eBay Seller Hub → Listings → Active → Download
  --orders   eBay Seller Hub → Orders → Download (Item number, Item title, Custom label, Sale date, Quantity)
  --shopify  Shopify → Products → Inventory → Export (SKU, Available)  — or Products → Export (Variant SKU,
             Variant Inventory Qty, Status)

Output:
  relist-confirmed.csv  item_number, sku, title, price (as exported — unchanged), quantity, shopify_available,
                        ended, matched_by
  relist-excluded.csv   same + reason (one of REASONS)
"""

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

REASONS = {
    'ALREADY_ACTIVE': 'same SKU / item / title is live on eBay now',
    'SOLD_SINCE': 'sold on eBay after (or without) this listing ending',
    'NO_SHOPIFY_STOCK': 'Shopify available ≤ 0',
    'NOT_IN_SHOPIFY': 'SKU not found in the Shopify export (and no title match)',
    'SHOPIFY_NOT_ACTIVE': 'Shopify product is draft / archived',
    'OUT_OF_SCOPE': 'mystery / bulk lot or unverified grader (HGA, GMG, …) — not relisted post-pivot',
    'BANNED_WORDS': 'title has Whatnot / mystery pack / official / Top Rated',
    'DUPLICATE': 'older duplicate of another unsold row for the same item',
    'NO_PRICE': 'no price in the unsold export',
}

ALIASES = {
    'item': ['item number', 'item id', 'itemid', 'item no', 'listing id'],
    'title': ['title', 'item title', 'listing title'],
    'sku': ['custom label (sku)', 'custom label', 'sku', 'variant sku'],
    'price': ['current price', 'start price', 'price', 'buy it now price', 'sold for'],
    'qty': ['available quantity', 'quantity available', 'quantity', 'qty'],
    'ended': ['end date', 'end time', 'ended', 'date ended'],
    'sold_date': ['sale date', 'sold date', 'paid on date', 'order date', 'sold on'],
    'available': ['available', 'variant inventory qty', 'on hand', 'inventory', 'quantity'],
    'status': ['status', 'product status'],
}

OUT_OF_SCOPE_RE = re.compile(r'\b(mystery|bulk lot|card lot|lot of \d+|grab bag|repack|hga|gmg|ace grading|tag grading)\b', re.I)
BANNED_RE = re.compile(r'what\s*not|mystery\s*pack|official|top\s*rated', re.I)
DATE_FORMATS = ('%Y-%m-%d', '%d-%b-%y', '%d-%b-%Y', '%b-%d-%y', '%b %d, %Y', '%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d %H:%M:%S',
                '%b-%d-%y %H:%M:%S', '%d %b %Y', '%m/%d/%Y')


def norm_title(t):
    return re.sub(r'[^a-z0-9]+', ' ', (t or '').lower()).strip()


def norm_sku(s):
    return (s or '').strip().upper()


def parse_date(s):
    s = (s or '').strip()
    s = re.sub(r'\s+(AEST|AEDT|PST|PDT|GMT|UTC)$', '', s)
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            continue
    m = re.match(r'(\d{4}-\d{2}-\d{2})', s)
    return datetime.strptime(m.group(1), '%Y-%m-%d') if m else None


def parse_money(s):
    s = (s or '').replace(',', '')
    m = re.search(r'\d+(?:\.\d+)?', s)
    return float(m.group(0)) if m else None


def read_csv(path, must_have):
    """Read a CSV whose header may follow preamble lines; returns list of dicts with lower-cased keys."""
    raw = Path(path).read_text(encoding='utf-8-sig', errors='replace').splitlines()
    start = 0
    for i, line in enumerate(raw[:50]):
        low = line.lower()
        if any(a in low for a in must_have):
            start = i
            break
    rows = list(csv.DictReader(raw[start:]))
    return [{(k or '').strip().lower(): (v or '').strip() for k, v in r.items()} for r in rows
            if any((v or '').strip() for v in r.values())]


def col(row, key):
    for a in ALIASES[key]:
        if a in row and row[a] != '':
            return row[a]
    return ''


def reconcile(unsold, active, orders, shopify, since=None):
    act_items = {col(r, 'item') for r in active if col(r, 'item')}
    act_skus = {norm_sku(col(r, 'sku')) for r in active if col(r, 'sku')}
    act_titles = {norm_title(col(r, 'title')) for r in active if col(r, 'title')}

    sold = []      # (item, sku, title, date)
    for r in orders:
        sold.append((col(r, 'item'), norm_sku(col(r, 'sku')), norm_title(col(r, 'title')), parse_date(col(r, 'sold_date'))))

    shop_by_sku, shop_by_title = {}, {}
    for r in shopify:
        sku = norm_sku(col(r, 'sku'))
        avail = col(r, 'available')
        try:
            n = int(float(avail)) if avail != '' else 0
        except ValueError:
            n = 0
        status = (col(r, 'status') or 'active').lower()
        rec = {'available': n, 'status': status}
        if sku:
            prev = shop_by_sku.get(sku)
            shop_by_sku[sku] = rec if not prev else {'available': prev['available'] + n, 'status': prev['status'] if prev['status'] == 'active' else status}
        t = norm_title(col(r, 'title'))
        if t:
            shop_by_title.setdefault(t, rec)

    # newest unsold row per item key wins
    keyed = {}
    for r in unsold:
        key = col(r, 'item') or norm_sku(col(r, 'sku')) or norm_title(col(r, 'title'))
        keyed.setdefault(key, []).append(r)

    confirmed, excluded = [], []
    for key, rows in keyed.items():
        rows.sort(key=lambda r: parse_date(col(r, 'ended')) or datetime.min, reverse=True)
        for dup in rows[1:]:
            excluded.append(out_row(dup, None, '', 'DUPLICATE'))
        r = rows[0]
        item, sku, title = col(r, 'item'), norm_sku(col(r, 'sku')), col(r, 'title')
        nt = norm_title(title)
        ended = parse_date(col(r, 'ended'))
        if since and ended and ended < since:
            continue
        reason, shop, matched = None, None, ''
        if sku and sku in shop_by_sku:
            shop, matched = shop_by_sku[sku], 'sku'
        elif nt in shop_by_title:
            shop, matched = shop_by_title[nt], 'title'

        if BANNED_RE.search(title):
            reason = 'BANNED_WORDS'
        elif OUT_OF_SCOPE_RE.search(title):
            reason = 'OUT_OF_SCOPE'
        elif item in act_items or (sku and sku in act_skus) or nt in act_titles:
            reason = 'ALREADY_ACTIVE'
        elif any((item and s[0] == item) or (sku and s[1] == sku) or (nt and s[2] == nt) for s in sold
                 if not ended or not s[3] or s[3] >= ended or s[0] == item):
            reason = 'SOLD_SINCE'
        elif shop is None:
            reason = 'NOT_IN_SHOPIFY'
        elif shop['status'] not in ('active', ''):
            reason = 'SHOPIFY_NOT_ACTIVE'
        elif shop['available'] <= 0:
            reason = 'NO_SHOPIFY_STOCK'
        elif parse_money(col(r, 'price')) is None:
            reason = 'NO_PRICE'
        row = out_row(r, shop, matched, reason)
        (excluded if reason else confirmed).append(row)
    return confirmed, excluded


def out_row(r, shop, matched, reason):
    qty_raw = col(r, 'qty')
    try:
        qty = int(float(qty_raw)) if qty_raw else 1
    except ValueError:
        qty = 1
    avail = shop['available'] if shop else ''
    if shop:
        qty = max(0, min(qty or 1, shop['available']))
    d = {'item_number': col(r, 'item'), 'sku': col(r, 'sku'), 'title': col(r, 'title'),
         'price': col(r, 'price'), 'quantity': qty, 'shopify_available': avail, 'ended': col(r, 'ended'),
         'matched_by': matched}
    if reason:
        d['reason'] = reason
        d['reason_detail'] = REASONS[reason]
    return d


def write(path, rows, extra=()):
    fields = ['item_number', 'sku', 'title', 'price', 'quantity', 'shopify_available', 'ended', 'matched_by', *extra]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in fields})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unsold', required=True)
    ap.add_argument('--active', required=True)
    ap.add_argument('--orders', required=True)
    ap.add_argument('--shopify', required=True)
    ap.add_argument('--out-dir', default='data/relist')
    ap.add_argument('--since', help='only consider listings that ended on/after YYYY-MM-DD')
    a = ap.parse_args(argv)
    unsold = read_csv(a.unsold, ['item number', 'title'])
    active = read_csv(a.active, ['item number', 'title'])
    orders = read_csv(a.orders, ['order number', 'item number', 'sales record'])
    shopify = read_csv(a.shopify, ['sku', 'handle'])
    since = datetime.strptime(a.since, '%Y-%m-%d') if a.since else None
    confirmed, excluded = reconcile(unsold, active, orders, shopify, since)
    out = Path(a.out_dir)
    write(out / 'relist-confirmed.csv', confirmed)
    write(out / 'relist-excluded.csv', excluded, extra=('reason', 'reason_detail'))
    from collections import Counter
    print(f'unsold {len(unsold)} · confirmed {len(confirmed)} · excluded {len(excluded)} '
          + ' '.join(f'{k}={v}' for k, v in Counter(r['reason'] for r in excluded).most_common()))
    print(f'→ {out / "relist-confirmed.csv"}  {out / "relist-excluded.csv"}  (nothing was relisted; prices as exported)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
