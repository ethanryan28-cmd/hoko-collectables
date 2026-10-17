# REPORT 2026-10-18 · Phone ops (`claude/phone-ops-1018`)

Cloud only, PC down. Branch from `main` @ `bcc32cb`. **No Shopify writes**: four product reads only. No products, prices, discounts, inventory or captions changed. Not merged.

Ethan's rulings this run:
- Pre-orders stay ACTIVE at current prices; the brief is confirm-or-adjust.
- Discord stays product-drop photos.

| Step | Result | Detail |
|---|---|---|
| 1 phone-pack `--days` + toggle | **PASS** | `claude/phone-pack-2day` (`170240f`) merged in.<br>• `--days N`: day 1 = today (Victoria) or the next day with items; each day gets its own heading; `--date` combines with it.<br>• Log skips rows already logged for the same date + platform + asset_id.<br>• Save line under every heading: `PHONE_PACK_FILES_FIRST=1` switches it to the Files route.<br>• 7 tests. |
| 2 task prompt | **PASS** | `routines/prompts/phone-pack-task.md` opens with "Push works only after Ethan adds the repo to the task's sources in claude.ai."<br>• Steps: shallow clone (`GIT_LFS_SKIP_SMUDGE=1`) → `phone-pack --days 1` → push the log on `claude/phone-pack-log-<YYYYMMDD>` (a 403 becomes one line and the task carries on) → ONE SendUserMessage ending `NOT CHECKED:` → PushNotification "PHONE PACK <date> — N clips ready."<br>• The push runs before the message so the message can report it. |
| 3a Urara yen | **PASS (none listed)** | `download_file_content` xlsx export covered every tab and row.<br>• Grep for M7 / Hadou / Aura / Seeker / OP-18 / Dominance / EB-05 / Heroines / FB12 / Reach the God / Fusion: 0 hits.<br>• Sheet dated 17 Oct 2026. Newest rows: Pokémon M6a, One Piece OP-17 / EB-04 / PRB-02. No Dragon Ball rows.<br>• Kanade: no sheet in Drive. |
| 3b pricing brief | **PASS** | `data/preorder-pricing-2026-10-18.md` covers all four boxes:<br>• Shopify state, cost source, FX 0.009112, landed, fee, floor<br>• comp table with URLs (read 17 Oct), comp median<br>• one recommendation, margin table<br>• ends with the ETHAN DECIDES block.<br>No price written. |
| 4 Discord ready | **PASS** | The poster now reads `DISCORD_WEBHOOK_URL` (`config.ALIASES` still reads the old `DISCORD_WEBHOOK_PICKUPS`).<br>• `dry-run` prints the next 3 Discord items (title, caption, product link, photo; no price, no webhook URL) or `Discord next 3 · NOT CONFIGURED (DISCORD_WEBHOOK_URL missing)`, exit 0.<br>• README "Discord webhook on phone"; `install-tasks.ps1` key list updated.<br>• 8 tests in `test_discord_ready.py`. |
| 5a banned-word gate | **PASS** | 0 hits in new or changed files.<br>• The script reports 1 line, its own regex (self-match, already there on `main`).<br>• Banned words inside test fixtures are excluded by the gate, as before. |
| 5b tests | **PASS** | `python -m unittest discover -s tools -t .`: 86 OK (71 on main + 7 phone-pack + 8 Discord). |
| 5c `check` | **PASS** | 15 days on every platform; hot share 60% on every platform. |
| 5d `dry-run` | **PASS** | 0 invalid on every platform, 0 media missing, exit 0. |
| 5e QUEUE | **PASS** | New entry on top.<br>• New PHONE section (6 items).<br>• WAITING ON ETHAN: the "Prices for M7/OP-18/FB12" line is now "Confirm/adjust pre-order prices — see data/preorder-pricing-2026-10-18.md".<br>• Discord and publishing the theme moved from WAITING ON PC to PHONE. |

## Pricing brief: headline

| Box | Now | Comp median | Floor (Urara-pattern cost) | Rec |
|---|---|---|---|---|
| M7 | $190 ACTIVE | A$224.95 (only 1 AU domestic retailer) | $135 @ ¥11,200 | **$190 keep** |
| OP-18 | $200 ACTIVE | A$299.95 | $155 @ ¥13,200 | **$219 (+$19)**: still $1 under the cheapest AU store (DenDen $220) |
| FB12 | $165 ACTIVE | NOT CHECKED (<3 AU listings) | $140 @ ¥12,000 ASSUMPTION | **$165 keep** |
| EB-05 | $235 ACTIVE | A$250.00 | $145 @ ¥12,200 | **$235 keep** |

**Correction to the brief's label.** The cost stand-in is JP retail (RRP), ¥5,760–6,000 a box. Urara sells new boxes at about 2× RRP (OP-17 ¥13,200, EB-03 ¥12,200, M6 ¥11,200). So the stand-in floor reads **low**, not high. Each box therefore carries both lines:
- "RETAIL STAND-IN — floor reads low"
- a "Urara-pattern" line at the previous set's Urara price.

## NOT CHECKED
- Urara yen for M7 / OP-18 / FB12 / EB-05: not listed as of 17 Oct 2026.
- Kanade yen: no sheet.
- Freight: A$14 per box is an ASSUMPTION.
- GST registration status.
- eBay AU comps (403 from the cloud).
- AmiAmi, Cardrush, MTG Mate (403); Toyger, Card Merchant (no connection).
- M7 JP RRP: search snippet only. Hobby Search prices: from search results, product pages 403.
- FB12 AU comp median: fewer than 3 Japanese-box listings.
- The phone-pack prompt has not been run inside `trig_01QeakRTdC9hVqwinFfMP1CB`.
- A real Discord post (no webhook in this environment).
- Clock: the cloud clock read 17 Oct (~22:15 Victoria) when Shopify and the comps were read; files carry the 18 Oct run date as briefed.

## MANUAL

**Phone (Ethan)**
1. Add `ethanryan28-cmd/hoko-collectables` to the sources of the phone-pack task `trig_01QeakRTdC9hVqwinFfMP1CB`.
2. Add the same repo to the sources of the cloud-run poster task `trig_015SKsJWBRCz4Y549d2kHgeL`.
3. Paste `routines/prompts/phone-pack-task.md` into `trig_01QeakRTdC9hVqwinFfMP1CB`.
4. Create the Discord webhook and paste it as `DISCORD_WEBHOOK_URL` in the cloud-run task env.
5. Publish the draft theme.
6. Post the daily pack.

Also from the phone:
- Tick the ETHAN DECIDES block in the pricing brief. Any price change is Ethan's own edit.
- Merge `claude/phone-ops-1018`.

**PC-only**
- Platform keys: IG/FB, YouTube, Pinterest.
- `schtasks /Delete /TN "HOKO publish" /F`.
- Policies, meta description, BF email.
- Cloud setup-script line and network allowlist.

## COMPLETE
