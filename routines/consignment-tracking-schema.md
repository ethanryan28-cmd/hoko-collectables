————————–———# HOKO Consignment Tracking Schema

> Phase 2 operational doc. Do not market consignment until Whatnot + Shopify flow is proven.
> For casual inbound consignment cases only until formal launch.

---

## Purpose

Single source of truth for all active and closed consignment items. One row per item. Maintained in a spreadsheet (Google Sheets recommended) or exported as CSV to this repo periodically.

---

## Column Schema

| Column | Field Name | Type | Notes |
|--------|-----------|------|-------|
| A | consignment_id | Text | Unique ID. Format: CONS-YYYY-NNN (e.g. CONS-2026-001) |
| B | consignor_name | Text | Full name of the item owner |
| C | consignor_email | Text | Primary contact email |
| D | consignor_phone | Text | Mobile number (AU format) |
| E | item_description | Text | Full item name — set name, grade, grader, cert number if slab |
| F | item_category | Enum | sealed-pokemon / sealed-mtg / sealed-onepiece / sealed-dbs / slab-psa / slab-bgs / slab-cgc |
| G | grader | Enum | PSA / BGS / CGC / N/A (for sealed) |
| H | grade | Number | Numeric grade (e.g. 9, 9.5, 10). Leave blank for sealed. |
| I | cert_number | Text | Grading cert / population report number. Leave blank for sealed. |
| J | agreed_list_price_aud | Currency | Agreed listing price in AUD (inc. GST) |
| K | commission_rate_pct | Number | HOKO commission percent (typically 20). Enter as integer. |
| L | consignor_payout_aud | Currency | Auto-calculated: agreed_list_price_aud * (1 - commission_rate_pct/100) |
| M | channels | Text | Where listed: Shopify / eBay / Whatnot / combination |
| N | date_received | Date | YYYY-MM-DD date item physically received by HOKO |
| O | contract_signed | Boolean | TRUE / FALSE single-page consignment agreement signed and filed |
| P | shopify_product_url | URL | Full Shopify product URL once listed. Leave blank until live. |
| Q | ebay_listing_url | URL | Full eBay listing URL once listed. Leave blank until live. |
| R | date_listed | Date | YYYY-MM-DD date first listed on any channel |
| S | date_sold | Date | YYYY-MM-DD date item sold. Leave blank until sold. |
| T | sale_price_aud | Currency | Actual sale price (may differ from list price if negotiated) |
| U | actual_payout_aud | Currency | Auto-calculated: sale_price_aud * (1 - commission_rate_pct/100) |
| V | platform_fee_aud | Currency | eBay/Whatnot/Shopify payment fee deducted (estimate if needed) |
| W | net_hoko_revenue_aud | Currency | Auto-calculated: sale_price_aud - actual_payout_aud - platform_fee_aud |
| X | payout_date | Date | YYYY-MM-DD date HOKO paid consignor. Leave blank until paid. |
| Y | payout_method | Enum | bank-transfer (standard) / other |
| Z | status | Enum | intake / listed / sold-unpaid / paid-closed / returned |
| AA | notes | Text | Free-form notes (condition issues, owner comms, special instructions) |

---

## Status Definitions

| Status | Meaning |
|--------|---------|
| intake | Agreement signed, item received, not yet listed |
| listed | Live on at least one channel, awaiting sale |
| sold-unpaid | Item sold, payout not yet made to consignor |
| paid-closed | Sale complete, consignor paid, case closed |
| returned | Item returned to consignor unsold |

---

## Rules

- Minimum item value: AUD $100 per item at agreed list price. No exceptions.
- Accepted categories: factory-sealed TCG product + PSA/BGS/CGC slabs only. No loose singles, no HGA/GMG.
- Commission: 20% flat (negotiable only for items $1,000+ at owner discretion).
- Contract required: do not accept physical possession without a signed templates/consignment-agreement.md.
- Payout: bank transfer only, within 5 business days of sale clearing.
- Listing period: default 90 days. If unsold, consignor may request return or agree to extend/reprice.

---

## Related Files

- templates/consignment-agreement.md
- templates/consignment-intake-email.md
- templates/collection-buyback-intake.md
