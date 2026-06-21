# Shopify Scripts

Python scripts for managing HOKO Collectables' Shopify store via the Admin REST API.
All scripts are read-safe by default and require explicit flags for write operations.

---

## Setup

### Requirements

- Python 3.9+
- `requests` library: `pip install requests`
- Shopify Admin API token with appropriate scopes

### Environment Variables

Create a `.env` file in this folder (never commit it):

```
SHOPIFY_STORE=your-store.myshopify.com
SHOPIFY_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxx
```

---

## Scripts

### archive_cheap_singles.py
Archives active Shopify listings below a price floor. Use after the May 2026 pivot.
```bash
python archive_cheap_singles.py --dry-run
python archive_cheap_singles.py --threshold 10
```

### check_inventory.py
Read-only audit for zero-stock active variants.
```bash
python check_inventory.py
python check_inventory.py --output zero_stock.csv
```

### export_sold_orders.py
Read-only export of shipped Shopify orders to CSV. For GST reconciliation and sales analysis.
```bash
python export_sold_orders.py --days 30
python export_sold_orders.py --from 2026-05-01 --to 2026-05-31
python export_sold_orders.py --output may_orders.csv
```

### list_active_products.py
Read-only export of all active Shopify products to CSV.
```bash
python list_active_products.py
python list_active_products.py --type "Graded Card"
```

### price_check.py
Read-only price audit vs a reference CSV.
```bash
python price_check.py --file prices.csv
python price_check.py --file prices.csv --output discrepancies.csv
```

### update_prices.py
Bulk price updater. Always dry-run first.
```bash
python update_prices.py --file prices.csv --dry-run
python update_prices.py --file prices.csv
python update_prices.py --file prices.csv --floor 5 --ceiling 2000
```
CSV format: `sku,price`

---

## Notes

- Never commit `.env` files or API tokens
- Dry run mode available on write scripts — always use it first
- API rate limit handled automatically (2 req/sec)
- Test on staging store before large bulk operations
