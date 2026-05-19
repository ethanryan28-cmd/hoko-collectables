# Shopify scripts

Scripts for managing HOKO Collectables' Shopify catalogue. All scripts default to dry-run.

## `archive_cheap_singles.py`

Finds active Shopify products priced under AUD $30 and archives them (reversible). Strategy: keep premium singles + sealed on Shopify, push cheap singles to eBay-only.

### Setup (Windows, one-time)

1. **Install Python** if you don't have it:
   ```powershell
   winget install Python.Python.3.12
   ```
2. **Install the one dependency:**
   ```powershell
   pip install requests
   ```
3. **Get a Shopify Admin API access token:**
   - Shopify admin → Settings → Apps and sales channels → Develop apps → Create an app → name it `HOKO Scripts`
   - Configure scopes: `read_products`, `write_products`
   - Install app → reveal Admin API access token (starts with `shpat_...`)
   - **Treat this token like a password — never commit it to git.**

### Run it

```powershell
cd C:\path\to\claude\hoko-collectables\scripts\shopify

# Set credentials for this PowerShell session only
$env:SHOPIFY_STORE = "hokocollectables.myshopify.com"
$env:SHOPIFY_ADMIN_TOKEN = "shpat_xxxxxxxxxxxxxxxxxxxx"

# Step 1 — dry-run. Writes candidates.csv. No changes made.
python archive_cheap_singles.py

# Step 2 — open candidates.csv in Excel. Review the list.
# Spot-check: are any premium products in there by mistake?
# If happy:
python archive_cheap_singles.py --execute
# Type 'archive' at the prompt to confirm.
```

### Reversing

Archived products stay in admin — to bring one back:
- Shopify admin → Products → filter Status = Archived
- Open the product → Unarchive (top-right)

### Tweaking the threshold

Edit `THRESHOLD_AUD` near the top of `archive_cheap_singles.py`.
