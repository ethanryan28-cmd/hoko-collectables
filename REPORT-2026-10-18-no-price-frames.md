# REPORT 2026-10-18 · No price frames (`claude/no-price-frames`)

From Ethan's rulings of 17 Oct 2026:
1. No price in the video frame or the voiceover.
2. Rebuild `captions/` without rendering.
3. Retire the PC "HOKO publish" job.
4. The BF "$5 off boxes" calendar line stays.

There were 0 Shopify reads or writes and 0 price, discount or listing changes. Product images came from the public Shopify CDN through the existing render image cache.

## Steps

| Step | Result |
|---|---|
| 0 Network + state | **PASS.** PyPI `200`. `speech.platform.bing.com` `400` (not a 403 policy denial). Proxy status enabled, no relay failures. Branch cut from origin/main `395bb11` |
| 1 Strip prices (code) | **PASS.** Details below. 56 tests OK (54 + 2 new) |
| 2 Re-render all reels | **PASS.** 75/75 clips, 0 fallback voice, 93.8 MB, 0 missing media |
| 3 Rebuild captions/ | **PASS.** The no-render rebuild has 0 diff against the render build. Only `$5 off boxes` is left (15 files) |
| 4 Retire PC publisher | **PASS.** Both READMEs updated. `publish.run()` prints one line first and nothing else changes |
| 5 Gates + wrap | **PASS.** Results under Gates |

## Step 1 — code

**`content/youtube/hoko/reel.py`**
- `hook_text`:
  - Slab k≥1 is now `One in stock — {g} {name}`.
  - Sealed k==2 without packs: on-screen `{s} — sealed Japanese {kd}`, voiceover `{s}. Sealed Japanese {kd}, free Australian postage on sealed boxes. Link in bio.`
  - Docstring: neither the hook nor the voiceover says a price.
- `caption_text`: the de-pricing added in bf-media-tidy is removed. Regenerating all 57 `reels/**/*.caption.txt` that have a source row gives **57/57 byte-identical** output. The 4 others are the two drafted products; see Step 2.
- `preorder_body` line 4 is now `Free AU post on sealed`.
- `render()`:
  - The gold `L_price` layer is now `L_badge` in the same slot (y=1500). Sealed shows `SEALED · JAPANESE` at 80 px; 110 px wrapped onto the sub line. Slab shows `{grader} {grade}` at 110 px.
  - Roundup item labels show the set code instead of the price (y=1590).
  - The `price_str` import was dropped.
- **Beyond the brief (ruling 1):** the second-half postage strip `L_post` read `Tracked post · free $150+` / `Free AU post on sealed $250+`. It now reads `Tracked post from Victoria` / `Free AU post on sealed`.

**`content/youtube/hoko/calendar_gen.py`** (needed for the sidecar and caption gates)
- Roundup `under-200` title: `Japanese sealed under $200` → `Cheapest Japanese sealed in stock`. The key and file `roundups/under-200.mp4` are unchanged, and it still selects boxes under 200.
- `roundup_caption`: the per-item price is dropped. The postage line is now `Free AU post on sealed boxes.`
- `beat_caption`: `Featured: {s} — {p}` becomes `Featured: {s}`, in all 4 variants.
- Buyback tip: on-screen `Sealed + verified slabs $100+` → `Sealed + graded slabs`. The voiceover drops "over a hundred dollars". The threshold stays on `/pages/sell-your-cards`.

**`price_str` callers left:** none in `reel.py`. Three remain in `calendar_gen.py`, at lines 243, 267 and 268, and all three build the `calendar.md` **item column**. That column is an internal planning table and is not posted. The brief said to leave it, and 53 rows still show a price. Nothing reachable from `render()`, `hook_text`, `preorder_body` or `caption_text` calls it. Other matches are the `common.py` definition and an unrelated local variable in `scripts/shopify/update_prices.py`.

**Grep `\$[0-9]|two fifty|\$250` on reel.py:** one non-comment hit remains, line 141 `Join the BF box drop list — $5 off boxes`. That is the caption-only BF line kept by ruling 4. It is not in the frame or the voiceover. The regex at line 307 (`[^a-z0-9$]`) does not match the pattern.

**New tests:** `tools/social/tests/test_reel_prices.py`.
- `hook_text`: no `$` and no "two fifty" across every hook the function implements, on all 24 sealed and 6 slab rows. That covers slab h0/h1 and sealed h1/h2 (both with and without packs), plus h3/h4 where `release_date`/`chase` is set.
- `preorder_body`: no `$` on any row that has a release date.

## Step 2 — re-render

- Installed `edge-tts` 7.3.1, `piper-tts` 1.8.0 and `faster-whisper` 1.2.1. The 5-s gate returned `edge-tts:en-AU-WilliamMultilingualNeural`.
- Order of the renders:
  1. `reel sealed all --force` and `reel slab all --force`.
  2. Any sidecar left over.
  3. The calendar with every beat, tip and roundup forced.
  4. A second sealed pass (45 clips, h1/h2/h4) after the badge was shrunk to fit one line.
  5. The buyback tip, twice, for its copy.
- **4 extra clips:** `sealed/10734771896598/h1,h2` (Ruler of the Black Flame) and `sealed/10734773666070/h1,h2` (Inferno X). Their products are drafts and no longer in `source.csv`. Only their sidecars were ever committed; those recorded `piper:en_GB-alan-medium` and a priced h2 hook. I re-rendered them from the rows in `f155f4b:content/youtube/sealed/source.csv`, so the sidecars now match real William clips with no price. The queue does not reference them. That is why the count is 75, not 71.
- **Per-clip gate (all 75):** 1080×1920 · audio · 8–20 s · sidecar `tts` = William · no `$` and no "two fifty" in the sidecar hook or voiceover. **75/75 PASS.**
- **Frames checked visually:** I took frames at 50% and 90% of the clip plus 80% of the content segment, for 36 clips: 22 sealed h2, 4 pre-order h3, 6 slab h1 and 4 roundups. The 90% frame is the end card on every clip; one is checked and it has no price. I looked at 4 contact sheets and found 0 prices. They cover:
  - sealed h2: Abyss Eye M5 (10734771765526), Ruler of the Black Flame sv3, Heat Wave Arena sv9a, Inferno X M2, Mega Brave M1L, 30th Celebration M6a, Nihil Zero M3, Mega Symphonia M1S, Pokémon Center Fukuoka, VSTAR Universe s12a (after the badge fix)
  - pre-order h3: OP-18, FB12, M7, EB-05
  - slab h1: Bellsprout PSA 9, Magikarp PSA 9, Detective Pikachu BGS 9, Nico Robin BGS 9.5, Nami BGS 10, Pikachu PSA 10
  - roundups: mega-era, one-piece, preorders, under-200
  - tip: buyback, after the copy change
- **Size:** 75 mp4s committed, **93.8 MB** (limit 150).
- **Queue:** dry-run shows 0 invalid and missing media 0 on every platform.

## Step 3 — captions/

- Backup of `captions/` (72 files), `calendar.md` and `CUTOFF.md` is in `reports/backups/2026-10-18-no-price-frames-calendar/`. It was taken before the render touched them and compared byte-for-byte.
- `calendar_gen.build(render_beats=False)` gives **0 diff** against the Step 2 build.
- **`\$[0-9]` in captions/:** 15 files, and in every one the only match is `$5 off boxes`. The files are 2026-11-01, 11-02, 11-05, 11-06, 11-09, 11-11, 11-13, 11-15, 11-18, 11-19, 11-20, 11-23, 11-24, 11-25 and 11-26.
- `calendar.md` has 72 rows, the same as the backup. The item column still shows prices (53 rows); it is internal and was not changed. `CUTOFF.md` is identical to the backup.
- **Read-back against the backup:**
  - 65 files changed, with 117 lines removed and 70 added.
  - **All 117 removed lines are price or postage lines or priced hooks.** That includes the `under $200` roundup title and the `$100+` buyback bullet.
  - The added lines are the de-priced replacements: the item line without a price, `Free AU post on sealed boxes.`, the de-priced hooks, `Featured: {s}.`, `Cheapest Japanese sealed in stock` and `• Sealed + graded slabs`.

## Step 4 — PC publisher retired

- `content/youtube/README.md`: there is a RETIRED 17 Oct 2026 banner, and the `publish` and `schedule` rows are struck through. Both carry `schtasks /Delete /TN "HOKO publish" /F`. I also fixed the stale "mp4 is gitignored" note and added a no-price note.
- `tools/social/README.md`: there is a RETIRED banner with the same command. It notes that `install-tasks.ps1` only *disables* the job.
- `hoko/publish.py`: the first line of `run()` is a pure `print('RETIRED 17 Oct 2026 …')`. Nothing else changed. `publish.py` and `hoko-publish.cmd` are not deleted.

## Gates

| Gate | Result |
|---|---|
| `python -m unittest discover -s tools/social/tests -t .` | **56 OK** (54 + 2) |
| `python -m tools.social check` | **PASS**: 15 days on all 6, 60% hot on every platform (117/195) |
| `python -m tools.social dry-run` | **0 invalid**, missing 0 on every platform |
| Banned words on changed text files (179, excluding mp4) | **0** (CDN filenames and the IANA tz are excluded) |
| `$` in any sidecar hook or voiceover | **0** |
| `reels/**/*.caption.txt` with `$N` | **0** |

## Findings (not actioned)
1. The BF beat clips (6) still show `$5 off boxes` / `List: $5 off` on screen. It is a discount amount, not a product price, and it matches the line kept by ruling 4. It is not in any sidecar hook or voiceover. Say if you want it out of the frame too; that is a 6-clip re-render.
2. `calendar.md` item column prices (53 rows) are internal and unchanged, as briefed.
3. CLAUDE.md postage canon still reads `sealed boxes: $15.25 tracked, free on sealed orders of $250+`. The clips now say "free AU post on sealed" because of your ruling of free postage on all sealed. The BF automatic is still unchanged (see MANUAL).

## NOT CHECKED
- Live posting (no platform keys).
- Shopify (not read, per brief).
- Whether the PC "HOKO publish" task still exists.
- An OCR pass on every frame. The visual check covered 36 clips via contact sheets, not all 75.

## MANUAL

**PC only**
- `schtasks /Delete /TN "HOKO publish" /F`

**Ethan only**
- BF free-shipping automatic: still "all orders $100+, AU". Your ruling is free postage on every Japanese sealed box with no minimum.
- Platform keys (list in `REPORT-2026-10-17-bf-lockin.md` MANUAL).
- Environment setup line `pip install edge-tts piper-tts faster-whisper pillow numpy requests` + `ffmpeg`. Network allowlist: `pypi.org`, `files.pythonhosted.org`, `speech.platform.bing.com`, `huggingface.co`.
- Optional: the BF beat on-screen `$5 off` (Findings 1).

## Wrap
- Commits on `claude/no-price-frames`: code + docs + tests + backup, then the badge/buyback code, then 75 clips + sidecars + captions + calendar, then this report + QUEUE. Merged `--no-ff` into `main`, pushed, and `git ls-remote` was checked against local main.

## COMPLETE
