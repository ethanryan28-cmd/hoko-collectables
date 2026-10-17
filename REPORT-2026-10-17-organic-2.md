# REPORT — 2026-10-17 organic-2 (`claude/organic-2-1017-h3c9kj`)

Unattended cloud run. Authorised: article-body, barcode, SEO and sales-channel-publication writes. Backup before every write, byte-exact read-back after. No price, status, discount, inventory, order or fulfilment field touched.

Goal: every link on the Japanese-sealed content path resolves to a buyable box, and the social poster is ready to fire the second its keys land.

## Summary

| Step | Result |
|---|---|
| 0 State | PASS — CLAUDE.md, QUEUE.md, `REPORT-2026-10-17-organic.md`, `data/jan-2026-10-17.csv`, git log read. Nothing in this brief was already done (the organic run only *flagged* the 2026 guide list and the $60–120 bullet) |
| 1 2026 guide stock list | PASS — rebuilt from live data: 14 Pokémon + 4 One Piece boxes, OP-17/OP-13 gone, M6a → product page, "pre-order" removed, range $150–$330 → **$115–$470**. Read-back byte-exact |
| 2 Japanese cards guide | PASS — one bullet out, one in. Read-back byte-exact |
| 3 Dead-link sweep | PASS with one listed link — 40 articles, 19 links, 3 hit DRAFT; 2 fixed (by step 1), 1 has no ACTIVE equivalent (EB-05 guide → its own DRAFT pre-order) and is listed, not guessed |
| 4 Channels | PASS — 20/20 ACTIVE jp-sealed already on all 7 channels; 0 gaps, 0 publish writes. 4 pre-order drafts untouched |
| 5 Social poster | PASS — `env`: every platform MISSING (names below); `dry-run` 0 invalid / 0 problems; cloud-run `--dry-run` every platform NOT CONFIGURED, would_post 0; new Discord-only unit test passes with no network |
| 6 JAN retry | JAN_RESULT_SUMMARY |
| 7 Gates | GATE_SUMMARY |
| 8 Wrap | WRAP_SUMMARY |

## Step 1 — 2026 guide (688213655830, `japanese-pokemon-one-piece-booster-boxes-australia-2026`)

Source: connector read of every `tag:jp-sealed` product (55). Rule: ACTIVE, and inventory > 0 or policy CONTINUE. That gives the 20 live products; the list takes the **18 booster boxes** (tag `booster-box`). Left off, because the paragraph above the list says "Everything below is a factory-sealed Japanese booster box": Mega Gengar starter deck (10734773862678) and Pokémon Center Fukuoka special box (15413357543702).

Order is newest set first (M6a → M6 → M5 → M3 → M1S/M1L → sv9a → sv8a → sv8 → sv7 → sv3a → s12a; OP-16 → OP-12 → OP-11 → OP-07). Markup copies the existing list exactly (`<li>\n<a …>Name (code)</a>: no outer shrink</li>` for no-shrink boxes, `<li><a …>Name (code)</a></li>` otherwise; One Piece by code only, as before).

Range sentence: min $115 (Nihil Zero M3 no-shrink), max $470 (OP-11) across the 18 listed boxes (read only). Including the deck and the Fukuoka box would have made it $70–$470.

| Links before (7) | Links after (21) |
|---|---|
| collection ×2, M6 no-shrink, sv8a, **collection as "M6a"**, **OP-17 (DRAFT)**, **OP-13 (DRAFT)** | collection ×2 (unchanged) + M6a, M6 no-shrink, M5, M5 no-shrink, M3, M3 no-shrink, M1S, M1L, sv9a, sv8a, sv8, sv7, sv3a, s12a, OP-16, OP-12, OP-11, OP-07 — **all ACTIVE** |

Everything else in the body is byte-identical: the script asserts that undoing the three replacements gives the backup back exactly, and the live read-back equals the built after-body (`check` → MATCH). The "(M6, sv8a, OP-17 and so on)" set-code example in the Release-timing paragraph is plain text, not a link, and was left alone.

## Step 2 — Japanese cards guide (683629674774, `japanese-pokemon-cards-australia`)

- Out: "Japanese booster boxes typically cost $60–120 AUD (vs $120–300 AUD for English boxes) and have better pull rates"
- In: "Japanese booster boxes hold fewer cards than English boxes, so compare them per box, not per pack"

Links before → after: 2 → 2 (collection, M1S — both unchanged). Read-back MATCH.

Finding, not actioned (outside "one bullet in, one out"): the same article still says "Pull rates in Japanese sets are often better than English equivalents (you pull chase cards more frequently)" under *Different set structure*. Same unbacked claim the brief removed from the price bullet. Say if you want it gone.

Files: `scripts/shopify/articles_organic2_2026_10_17.py` (build + check + banned-word assert), backups `reports/backups/2026-10-17-organic-2-articles-before.json` / `-after.json`.

## Step 3 — Dead-link sweep

Scope: all 130 articles paged; **40** published ones tagged `japanese`, `sealed`, `one-piece` or `pokemon` (exact tag). 7 of them hold product/collection links: **19 links, 11 targets** (9 products, 2 collections). Both collections (`japan-direct-sealed`, `pokemon`) resolve and are published. No MISSING or ARCHIVED targets.

| Article id | Article | href | Status | Product id | Action |
|---|---|---|---|---|---|
| 688213655830 | 2026 guide | /products/one-piece-tcg-op-17-sealed-japanese-booster-box | DRAFT | 10734775730454 | removed (step 1) |
| 688213655830 | 2026 guide | /products/one-piece-tcg-op-13-sealed-japanese-booster-box | DRAFT | 10734775566614 | removed (step 1) |
| 688481534230 | EB-05 guide | /products/pre-order-one-piece-heroines-edition-vol-2-eb-05-sealed-japanese-booster-box | DRAFT | 15431829848342 | **left** — no ACTIVE EB-05 product exists; the pre-order draft stays DRAFT (step 4) |

Plus the 2026 guide's M6a line pointed at the collection; now at the ACTIVE product. Table: `data/deadlinks-2026-10-17-organic-2.csv`.

The EB-05 guide's link goes live the moment the EB-05 pre-order is published (it is the right target, just not public yet). Until then the public gets a 404 on that one anchor.

Also checked: `/pages/black-friday` (linked from the EB-05 guide) exists and is published. `is-my-old-pokemon-binder-worth-anything-australia` (tag `Pokemon`, capital P) has no product/collection links.

## Step 4 — Channels

Publications: Online Store, Shop, Point of Sale, Google & YouTube, Facebook & Instagram, TikTok, Microsoft Channel, Pinterest, Inbox. Required 7 checked via `resourcePublicationsV2(onlyPublished:true)`:

| Product | Online Store | Google & YouTube | Pinterest | Shop | FB & IG | TikTok | Microsoft |
|---|---|---|---|---|---|---|---|
| all 20 ACTIVE jp-sealed (ids in `reports/channels-2026-10-17-organic-2.csv`) | 20 | 20 | 20 | 20 | 20 | 20 | 20 |

0 gaps → `publishablePublish` not called. OP-18, FB12, M7, EB-05 drafts: not touched.

## Step 5 — Social poster

- `python -m tools.social env`: every platform MISSING (no keys in this cloud environment).
- `python -m tools.social dry-run`: 0 invalid on all 7 platforms, `problems: []`. Valid future items: discord 15, facebook 29, instagram 29, pinterest 43, tiktok 42, tiktok_queue 14, youtube 29.
- `python -m tools.social cloud-run --dry-run`: every platform `NOT CONFIGURED`, `invalid.count 0`, `would_post 0`, queue 15 days on all 6 queued platforms. (It writes `data/social-runner.log`; reverted, not committed.)
- Discord-only: new test `NotConfigured.test_discord_only_posts_discord_and_nothing_else` sets only `DISCORD_WEBHOOK_PICKUPS` (fake URL), runs `cloud_run.run` with a fake HTTP client: Discord reports `configured`, every other platform `NOT CONFIGURED`, every HTTP call goes to the webhook, only Discord rows are logged OK, the webhook token never reaches the log. No network.
- Readiness by platform once keys land: **Discord and Pinterest post immediately** (no clips needed). **Instagram, Facebook, YouTube and the TikTok pack need the clips**: 49 queued mp4s are not in the repo (gitignored by design), and cloud-run renders them at run time. In this container `ffmpeg` is present but `piper-tts` is not installed, so a cloud render would fail. Add `pip install pillow numpy requests piper-tts` to the environment setup script, or render on the PC (`python -m tools.social render`).

## Step 6 — JAN retry

JAN_SECTION

## Step 7 — Gates

GATES_SECTION

## NOT CHECKED
- Storefront HTTP from the cloud (shell proxy blocks hokocollectables.com). Links were verified by Admin API handle → status, not by fetching pages.
- The 5 published articles whose tags are close to, but not exactly, the four in the brief ("pokemon cards australia", "pokemon cards", "one piece tcg", "pokemon tcg") and the untagged articles. Not swept. `Pokemon` (capital) was checked by hand: no links.
- Live posting on any platform (no keys).

## MANUAL

**Ethan only:**
- EB-05: publishing the pre-order (15431829848342) is your click. It fixes the last DRAFT link in the EB-05 guide. Price is still the $235 placeholder from the pre-orders run.
- Optional: drop the "Pull rates in Japanese sets are often better…" bullet from the Japanese cards guide (one line, say so).
- Social keys. One line per key. Put them in **claude.ai/code → this environment → Environment variables** for cloud-run, and/or Windows *User* environment variables for the PC runner. Never in the repo.
  - `DISCORD_WEBHOOK_PICKUPS`: Discord → HOKO server → #pickups-and-drops → Edit Channel → Integrations → Webhooks → New Webhook → Copy Webhook URL
  - `DISCORD_WEBHOOK_TIKTOK_QUEUE`: same steps on #tiktok-queue
  - `PINTEREST_TOKEN`: developers.pinterest.com → My apps → (create app) → Generate access token, scopes `pins:write`, `boards:read`
  - `PINTEREST_BOARD_ID`: with that token, `GET https://api.pinterest.com/v5/boards` → `id` of the board to pin to (or the number in the board's edit URL)
  - `META_PAGE_TOKEN`: developers.facebook.com → your app → Tools → Graph API Explorer → user token with `pages_show_list, pages_read_engagement, pages_manage_posts, instagram_basic, instagram_content_publish` → extend in Access Token Debugger → `GET /me/accounts` → the HOKO Page's `access_token` (or Meta Business Suite → Settings → Users → System users → Generate token, never expires)
  - `FB_PAGE_ID`: Facebook Page → About → Page transparency → Page ID (also the `id` in `/me/accounts`)
  - `IG_BUSINESS_ID`: Graph API Explorer → `GET /<FB_PAGE_ID>?fields=instagram_business_account` → its `id` (IG must be a professional account linked to the Page)
  - `YT_CLIENT_ID`: console.cloud.google.com → APIs & Services → Library → enable YouTube Data API v3 → Credentials → Create credentials → OAuth client ID (Desktop app) → Client ID
  - `YT_CLIENT_SECRET`: same Credentials page → that OAuth client → Client secret
  - `YT_REFRESH_TOKEN`: developers.google.com/oauthplayground → gear → "Use your own OAuth credentials" (the two above) → scope `https://www.googleapis.com/auth/youtube.upload` → Authorize as the HOKO channel → Exchange code → Refresh token
  - `SHOPIFY_STORE`: `dgcrmf-sh.myshopify.com` (Shopify admin → Settings → Domains shows it)
  - `SHOPIFY_ADMIN_TOKEN`: Shopify admin → Settings → Apps and sales channels → Develop apps → Create app → Admin API scopes `write_files` (+ `read_products`) → Install → Reveal token once
  - `TIKTOK_ENABLED`: leave unset / `false` (phone pack via Discord is the TikTok path)
  - `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN`: only if you turn the API on later. developers.tiktok.com → Manage apps → app → Content Posting API (`video.publish`)

**PC only (or environment setup script):** clips for IG/FB/YT/TikTok. Either `python -m tools.social render` on the PC, or add `pip install pillow numpy requests piper-tts` to the cloud environment's setup script so cloud-run can render them.

## COMPLETE
