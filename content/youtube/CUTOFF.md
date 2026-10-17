# Christmas 2026 delivery cutoff — sealed imports

**Order by: Monday 7 December 2026** (used in captions, calendar and Shopify descriptions)

## How it's worked out
- Lead time Japan → Victoria → buyer: **14 days** — ASSUMPTION 17 Oct 2026: Urara order → DHL to Victoria → dispatch within 2–4 business days ≈ 14 days door to door (the old 21-day figure came from the retired "allow 2–3 weeks" line)
- AusPost Parcel Post send-by from VIC metro to NSW/ACT/QLD/SA/TAS: **Mon 21 Dec 2026** — https://auspost.com.au/sending/christmas-sending-dates (fetched 2026-10-13)
- Cutoff = AusPost send-by − full lead time = 21 Dec − 14 days = **Mon 7 Dec**.
  Conservative on purpose: it assumes the whole 14 days is used before the box is lodged in Victoria,
  so anything ordered by the cutoff is on hand before AusPost's last parcel date.
- Graded slabs are already in Victoria — normal AusPost dates apply, no import lead time.

## Per-state (order-by = AusPost send-by − 14 days)
| state | AusPost Parcel Post send-by (from VIC) | order sealed by |
|---|---|---|
| NSW | Mon 21 Dec | Mon 7 Dec |
| ACT | Mon 21 Dec | Mon 7 Dec |
| VIC | Tue 22 Dec | Tue 8 Dec |
| QLD | Mon 21 Dec | Mon 7 Dec |
| SA | Mon 21 Dec | Mon 7 Dec |
| TAS | Mon 21 Dec | Mon 7 Dec |
| WA | Fri 18 Dec | Fri 4 Dec |
| NT | Wed 16 Dec | Wed 2 Dec |

WA (Fri 4 Dec) and NT (Wed 2 Dec) are earlier than the headline date.
Shopify copy uses the headline date; mention WA/NT in DMs if asked.

## Conflict to check
The live Shipping & Returns page says Japanese sealed is "imported and dispatched tracked from Victoria
within 2–4 business days". If that's true for in-stock boxes, the real cutoff is later (≈ AusPost dates).
Update `christmas_cutoff` in config.json and re-run `run.py calendar` if the lead time changes.
