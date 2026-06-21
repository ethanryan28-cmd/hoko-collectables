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
# Dry run — shows what would be archived
python archive_cheap_singles.py --dry-run

# Archive listings under $10
python archive_cheap_singles.py --threshold 10

# Archive listings under $25 with confirmation prompt
python archive_cheap_singles.py --threshold 25 --confirm
```

---

### price_check.py

Read-only audit of current Shopify prices vs a reference CSV.

**Use case:** Spot pricing anomalies before a price update run.

```bash
# Compare all active listings to reference prices
python price_check.py --file prices.csv

# Export discrepancies only
python price_check.py --file prices.csv --output discrepancies.csv
```

---

### update_prices.py

Bulk price updater. Reads a CSV and updates variant prices via the Shopify Admin API.

**Use case:** Apply monthly repricing across the full catalogue in one run.

```bash
# Dry run — shows what would change, no writes
python update_prices.py --file prices.csv --dry-run

# Apply updates (writes to Shopify)
python update_prices.py --file prices.csv

# Apply updates with floor/ceiling safety check
python update_prices.py --file prices.csv --floor 5 --ceiling 2000
```

**CSV format:**

```
sku,price
PSA-10-CHARZRDVMAX-EN,249.00
SLD-PTG-SV01ETB-EN,89.00
```

---

### check_inventory.py

Read-only audit for zero-stock active variants. Identifies listings that are live but have
no inventory, which can lead to customer disappointment or overselling.

**Use case:** Weekly inventory hygiene check before restocking or repricing.

```bash
# Print zero-stock active variants to console
python check_inventory.py

# Export results to CSV
python check_inventory.py --output zero_stock.csv

# Filter by product type
python check_inventory.py --type 'Graded Card'
```

---

## Notes

- All write operations prompt for confirmation unless `--force` is passed
- Dry run mode is available on all write scripts — use it first
- API rate limit: 2 requests/second (scripts handle this automatically)
- Do not commit `.env` files or API tokens
- Test on a staging store first if making large bulk changes
