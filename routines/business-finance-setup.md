# Business finance setup — HOKO Collectables (AU)

Minimum viable financial infrastructure for a Melbourne TCG sole trader / ABN business. Owner asked: bank account + safety finances. This doc captures the operational setup — **not financial advice**. Real tax / structure decisions go through a registered accountant.

---

## ⚠️ Active fix plan — HOKO current state (May 2026)

**Diagnosis (from owner check-in):**
- Has a CBA Business account but it's effectively unused
- Shopify + eBay payouts currently land in **personal CBA account**, not business
- All business expenses (suppliers, postage, fees) flow through the **same personal account**
- No tax bucket, no restock bucket, no float — single-balance setup
- "Cash is bullshit imo" mindset → all revenue gets reinvested into Pokemon, no reserves held

This is the most common (and most dangerous) cashflow pattern for an early-stage TCG sole trader. Tax time will be brutal without a fix, and you can't see what's actually profitable when personal and business money are in the same balance.

### The 4 fixes — do today, ~30 min total

Tick boxes from GitHub mobile as you go.

#### Fix 1 — Move payout destinations to the business CBA account (15 min)

- [ ] **Shopify:** Settings → Payments → edit payout bank details → swap in **business CBA BSB + account number**
- [ ] **eBay:** Seller Hub → Payments → Payout bank account → change to business CBA
- [ ] **PayPal / Stripe** (if linked anywhere for sales): point to business CBA

From this point, every dollar of revenue lands in the business account. Personal account stops receiving HOKO money entirely.

#### Fix 2 — Open 3 NetBank Saver sub-accounts under business operating (10 min)

Inside the CBA app, link 3 new NetBank Saver accounts to the business operating account. Name them exactly:

- [ ] **Tax** (untouchable — for BAS + income tax)
- [ ] **Restock** (buying sealed from suppliers)
- [ ] **Float** (business emergency buffer)

NetBank Savers are free, earn interest, and show as sub-accounts in the CBA app.

#### Fix 3 — Set up scheduled weekly transfers (5 min)

CBA doesn't do auto-percentage splits like Up does — you'll use **fixed weekly transfers** from business operating into the 3 savers.

**Tuned amounts** (based on most recent 30-day eBay performance: $730.74 gross / $563.51 net = ~$170/week gross):

| To | Amount/week | Monthly | % of net |
|---|---|---|---|
| → Tax | **$35** | $140 | ~25% |
| → Restock | **$50** | $200 | ~35% |
| → Float | **$15** | $60 | ~10% |
| Stays in Operating | **$30** | $120 | ~21% |

- [ ] Set up the 3 scheduled transfers (CBA app → Transfers → Recurring)
- [ ] Pick a day right after Shopify usually pays out (e.g. Tuesdays or Fridays)

**Important context (May 2026):** owner's 90-day total was $4,712, but most-recent 30 days dropped to $730 — a 37.6% decline. The pivot to sealed-only + slabs (higher AOV than current cheap-singles mix) is designed to reverse this. As monthly revenue climbs back toward $1,500+ and beyond, scale these transfer amounts up proportionally.

**Trigger to revisit amounts:** any month where eBay gross exceeds $1,000, or after a Whatnot stream lands, bump transfers up.

#### Fix 4 — Move business expenses to come from the business account (10 min)

- [ ] **Shopify monthly subscription** → update billing card to business account
- [ ] **eBay store fees** → update payment method
- [ ] **Postage** (Sendle / Australia Post / Aramex) → update billing
- [ ] **Supplier payments** → use business account for wires / BPAY / cards
- [ ] **Whatnot fees** (when streaming) → business account

From here: personal account = personal life only. Business account = HOKO only. No mixing.

### After the 4 fixes are done

- [ ] **Engage an accountant** ($500-1500/yr in Melbourne) to confirm the actual tax % for your bracket + structure (sole trader vs Pty Ltd)
- [ ] **Personal emergency fund** — separate goal, target 2 months living expenses (~$4-6k) in a CBA NetBank Saver linked to your personal account
- [ ] **Revisit transfer amounts every 2-3 months** as revenue grows

### One-off cash events (Whatnot streams, large buybacks, lot sales)

**Don't apply the weekly auto-split to one-off cash events.** They distort the maths because:

- The weekly transfers assume steady revenue
- A $3k Whatnot stream is ~8 weeks of normal revenue arriving at once
- Auto-splitting would over-allocate to tax (you owe tax on *profit*, not gross sales)

**When a large event lands** (e.g. Whatnot stream payout, big collection sale):

| Bucket | Allocation for one-off events | Why |
|---|---|---|
| → Tax | ~25% | Still taxable income, but only on profit portion |
| → Restock | 50-60% | Rebuild inventory at supplier rates (the main reason for the event) |
| → Float | 10-15% | Rebuild emergency buffer |
| → Operating | 10-15% | Covers several months of fees + your living |

Handle these manually after the payout clears. Ping Claude with the real number for an exact split.

### The mindset piece — why the buckets matter

"Cash is bullshit, I just reinvest into Pokemon" is exactly why the bucket method exists. **The architecture replaces the willpower.**

If all the money lives in one balance, you spend it all on Pokemon — that's how brains work, no shame. The Tax bucket existing in a separate account means **when tax day arrives, the money is already there**, not staring at a $2000 bill you can't pay.

You don't need self-discipline if the money's not in your spending account.

### What changes immediately

- Tax time stops being a panic event
- You can see real business profitability (revenue − expenses − tax buffer = actual margin)
- Personal and business stop bleeding into each other
- When the accountant asks "what's your FY26 business income", you answer in 30 sec instead of 3 hours of bank statement reconciliation
- The Pokemon spend is finally bounded — you can only buy from the Restock bucket, not the whole pile

---

## The 4-account method (general framework)

Every dollar of revenue auto-splits across four accounts the moment it lands. No in-the-moment decisions about "is this business or personal."

| Account | Purpose | Target % of revenue |
|---|---|---|
| **1. Operating (OPEX)** | Day-to-day business expenses — Shopify fees, postage, supplies, packaging | ~15-20% |
| **2. Tax Savings** | Untouchable until BAS + income tax due | ~25-30% |
| **3. Restock / Inventory** | Buying sealed from suppliers, replenishment | ~30-40% |
| **4. Owner's Wage** | Transferred to personal account weekly/fortnightly | ~15-20% |

Total = 100%. Adjust the split as the business matures — early stage skews toward restock + tax, later stages can shift more to owner's wage.

---

## AU bank account recommendations

### HOKO's current bank: CBA Business Transaction Account

- Big 4 traditional bank, useful if business lending is on the roadmap
- More fees than neobanks but solid for an established business
- Does NOT support auto-percentage splits natively — use scheduled fixed-amount transfers (see Fix 3 above)
- Supports multiple NetBank Saver sub-accounts (free, app-visible)

### Alternative if you ever switch: Up Business

- Free for sole traders
- App-first, fast onboarding (no branch visit)
- **Unlimited "Savers" with auto-percentage splits** — does the bucket method natively without manual transfers
- Owned by Bendigo Bank, AU government guaranteed deposits
- Only consider switching once HOKO is past the daily-cashflow-crunch phase — switching banks during an active business is friction you don't need right now

### Personal high-interest savings (for emergency fund)

Any of these work — pick whichever ecosystem you're already in:

- **CBA NetBank Saver** (same bank as your business — easiest)
- **ING Savings Maximiser** (typically highest rate, conditions apply)

---

## General week-1 checklist (for new HOKO-like businesses)

This is the generic checklist for any AU TCG sole trader starting from scratch. HOKO's specific fix plan is in the "Active fix plan" section above.

- [ ] Open business bank account (Up or CBA) — 15 min online
- [ ] Inside the business account, create the 4 named savers / sub-accounts (OPEX, Tax, Restock, Wage)
- [ ] Set up automated split rule (Up) or scheduled fixed transfers (CBA): every payout that lands → distribute across the 4 buckets on the % allocation above
- [ ] Update Shopify Payments + eBay payout destinations to the business account
- [ ] Find + engage an accountant in Melbourne (Google "small business accountant Melbourne sole trader" / ask in TCG seller groups for recommendations)
- [ ] Open / fund personal emergency fund — target 2 months living expenses (~$4-6k)

---

## What the accountant handles (so you don't have to)

- ATO compliance + annual tax return
- BAS filings (if GST-registered)
- Whether to stay sole trader or incorporate as Pty Ltd (changes at certain revenue / liability points)
- Confirming the real tax %s for the buckets above based on your actual bracket
- Bookkeeping recommendations (Xero, MYOB, etc.)
- Quarterly check-ins on cashflow + reserves

Budget: $500-1500/year for a small-business accountant. Saves multiples of that in mistakes / missed deductions / late lodgement penalties.

---

## The single principle to never break

**Don't touch the tax savings account.** Ever. Not for restock when you find a great deal. Not for a personal cash crunch. Not for a friend's loan.

The tax savings account is the line between a sustainable business and a chronic cash crisis. Sellers who raid it for restock end up owing the ATO money they don't have, then the cycle becomes: raid restock → can't buy → revenue drops → still owe ATO → worse cash crunch. Unwinnable.

Set it up. Auto-transfer. Forget it exists until BAS or tax return time.

---

## Disclaimer

This is operational setup guidance, not regulated financial advice. Specific tax %s, business structure decisions, and superannuation handling depend on individual circumstances and must be confirmed with a registered tax agent or accountant.
