"""
export_sold_orders.py — Read-only script to export shipped Shopify orders to CSV.

Usage:
    python export_sold_orders.py                        # last 30 days
    python export_sold_orders.py --days 90
    python export_sold_orders.py --from 2026-05-01 --to 2026-05-31
    python export_sold_orders.py --output may_orders.csv

Requires: SHOPIFY_STORE and SHOPIFY_TOKEN environment variables.
"""

import os, csv, sys, time, argparse, re, requests
from datetime import datetime, timedelta


def get_env():
    s, t = os.getenv("SHOPIFY_STORE"), os.getenv("SHOPIFY_TOKEN")
    if not s or not t:
        print("Error: SHOPIFY_STORE and SHOPIFY_TOKEN required.")
        sys.exit(1)
    return s, t


def fetch_orders(store, token, min_dt=None, max_dt=None):
    headers = {"X-Shopify-Access-Token": token}
    url = f"https://{store}/admin/api/2024-01/orders.json"
    params = {"status": "any", "fulfillment_status": "shipped", "limit": 250}
    if min_dt: params["created_at_min"] = min_dt
    if max_dt: params["created_at_max"] = max_dt
    orders, pi = [], None
    while True:
        if pi: params = {"page_info": pi, "limit": 250}
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 429: time.sleep(2); continue
        if r.status_code != 200: print(f"Error: {r.status_code}"); sys.exit(1)
        orders.extend(r.json().get("orders", []))
        link = r.headers.get("Link", "")
        if "next" not in link: break
        m = re.search(r"page_info=([^&>]+)", link)
        pi = m.group(1) if m else None
        if not pi: break
        time.sleep(0.5)
    return orders


def flatten(orders):
    rows = []
    for o in orders:
        c = o.get("customer", {})
        nm = (c.get("first_name","") + " " + c.get("last_name","")).strip()
        for i in o.get("line_items", []):
            rows.append({
                "order_number": o["order_number"],
                "created_at": o["created_at"],
                "financial_status": o["financial_status"],
                "customer": nm,
                "email": o.get("email",""),
                "sku": i.get("sku",""),
                "product": i["title"],
                "qty": i["quantity"],
                "price": i["price"],
                "line_total": str(float(i["price"]) * int(i["quantity"])),
                "order_total": o["total_price"],
                "discount": o["total_discounts"],
                "currency": o["currency"],
            })
    return rows


def main():
    p = argparse.ArgumentParser(description="Export Shopify orders to CSV")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--from", dest="date_from", default=None)
    p.add_argument("--to", dest="date_to", default=None)
    p.add_argument("--output", default=None)
    args = p.parse_args()
    store, token = get_env()
    min_dt, max_dt = None, None
    if args.date_from:
        min_dt = f"{args.date_from}T00:00:00Z"
        if args.date_to: max_dt = f"{args.date_to}T23:59:59Z"
    else:
        min_dt = (datetime.utcnow() - timedelta(days=args.days)).strftime("%Y-%m-%dT00:00:00Z")
    print(f"Fetching orders (from {min_dt})...")
    orders = fetch_orders(store, token, min_dt, max_dt)
    rows = flatten(orders)
    print(f"Found {len(orders)} orders, {len(rows)} line items")
    if not rows: print("No orders found."); return
    out = args.output or f'orders_{datetime.now().strftime("%Y%m%d")}.csv'
    fields = ["order_number","created_at","financial_status","customer","email",
              "sku","product","qty","price","line_total","order_total","discount","currency"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    print(f"Exported {len(rows)} rows to: {out}")


if __name__ == "__main__": main()
