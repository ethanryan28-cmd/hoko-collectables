# Christmas 2026 delivery cutoff — sealed imports

**Order by: Monday 30 November 2026** (used in captions, calendar and Shopify descriptions)

## How it's worked out
- Lead time Japan → Victoria → buyer: **21 days** — DEFAULT 21 days — 6 Oct dropship supply-model doc not found in repo, Google Drive or Notion (NOT CHECKED)
- AusPost Parcel Post send-by from VIC metro to NSW/ACT/QLD/SA/TAS: **Mon 21 Dec 2026** — https://auspost.com.au/sending/christmas-sending-dates (fetched 2026-10-13)
- Cutoff = AusPost send-by − full lead time = 21 Dec − 21 days = **Mon 30 Nov**.
  Conservative on purpose: it assumes the whole 21 days is used before the box is lodged in Victoria,
  so anything ordered by the cutoff is on hand before AusPost's last parcel date.
- Graded slabs are already in Victoria — normal AusPost dates apply, no import lead time.

## Per-state (order-by = AusPost send-by − 21 days)
| state | AusPost Parcel Post send-by (from VIC) | order sealed by |
|---|---|---|
| NSW | Mon 21 Dec | Mon 30 Nov |
| ACT | Mon 21 Dec | Mon 30 Nov |
| VIC | Tue 22 Dec | Tue 1 Dec |
| QLD | Mon 21 Dec | Mon 30 Nov |
| SA | Mon 21 Dec | Mon 30 Nov |
| TAS | Mon 21 Dec | Mon 30 Nov |
| WA | Fri 18 Dec | Fri 27 Nov |
| NT | Wed 16 Dec | Wed 25 Nov |

WA (Fri 27 Nov) and NT (Wed 25 Nov) are earlier than the headline date.
Shopify copy uses the headline date; mention WA/NT in DMs if asked.

## Conflict to check
The live Shipping & Returns page says Japanese sealed is "imported and dispatched tracked from Victoria
within 2–4 business days". If that's true for in-stock boxes, the real cutoff is later (≈ AusPost dates).
Update `christmas_cutoff` in config.json and re-run `run.py calendar` if the lead time changes.
