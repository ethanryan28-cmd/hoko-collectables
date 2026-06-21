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

Or export them in your shell before running.

---

## Scripts

### archive_cheap_singles.py

Archives active Shopify listings below a price floor.

**Use case:** Clean up old single card listings after the May 2026 pivot to sealed + slabs only.

```bash
python archive_cheap_singles.py --dry-run
python archive_cheap_singles.py --threshold 10
python archive_cheap_singles.py --threshold 25 --confirm
```

---

### check_inventory.py

Read-only audit for zero-stock active variants.

**Use case:** Weekly inventory hygiene check before restocking or repricing.

```bash
python check_inventory.py
python check_inventory.py --output zero_stock.csv
python check_inventory.py --type 'Graded Card'
```

---

### list_active_products.py

Read-only export of all active Shopify products to CSV.

**Use case:** Cross-reference with eBay listings, repricing runs, stock audits.

```bash
python list_active_products.py
python list_active_products.py --output active_products.csv
python list_active_products.py --type 'Graded Card'
python list_active_products.py --type 'Sealed TCG'
```

**CSV output columns:** product_id, product_title, product_type, vendor, status,
variant_id, sku, price, inventory_quantity, created_at, updated_at

---

### price_check.py

Read-only audit of current Shopify prices vs a reference CSV.

**Use case:** Spot pricing anomalies before a price update run.

```bash
python price_check.py --file prices.csv
python price_check.py --file prices.csv --output discrepancies.csv
```

---

### update_prices.py

Bulk price updater. Reads a CSV and updates variant prices via the Shopify Admin API.

**Use case:** Apply monthly repricing across the full catalogue in one run.

```bash
python update_prices.py --file prices.csv --dry-run
python update_prices.py --file prices.csv
python update_prices.py --file prices.csv --floor 5 --ceiling 2000
```

**CSV format:** `sku,price`

---

## Notes

- All write operations prompt for confirmation unless `--force` is passed
- Dry run mode is available on all write scripts — use it first
- API rate limit: 2 requests/second (scripts handle this automatically)
- Do not commit `.env` files or API tokens
- Test on a staging store first if making large bulk changes
