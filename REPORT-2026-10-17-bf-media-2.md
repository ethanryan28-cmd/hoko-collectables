# REPORT — 2026-10-17 BF media 2 (`claude/bf-media-1017`)

Unattended **cloud** run, brief pasted by Ethan as the session's opening message. Authorised: clip renders, committing rendered mp4s, merging `claude/bf-media-1017`, README/QUEUE edits. **0 Shopify writes, 0 Shopify reads.** No price, discount, inventory, order, product or theme change. No code edited: the `tts.py` fix, 7 tests, `.gitignore` un-ignore and README line from `REPORT-2026-10-17-bf-media.md` were already on the branch and were not redone.

**Outcome: all gates PASS.** The `tts.py` proxy-CA fix rendered for real against Bing (William en-AU, verification on, no sitecustomize). 71/71 clips rendered and passed ffprobe, **86.5 MB (83 MiB) committed**, queue missing media went from 30 to **0**, branch merged into `main`.

## Summary

| Step | Result |
|---|---|
| 0 Network + state | **PASS.** Read CLAUDE.md, QUEUE.md, `REPORT-2026-10-17-bf-media.md`, git log (main `307d1a1`, branch `6749b75` = main + 1 commit). Probes below |
| 1 TTS live gate | **PASS.** pip install edge-tts piper-tts faster-whisper OK · 54 tests OK · live synth → `edge-tts:en-AU-WilliamMultilingualNeural`, `/tmp/hoko-gate.wav` pcm_s16le audio, 2.30 s |
| 2 Render + keep | **PASS.** 71 mp4s, 71 ffprobe PASS, 0 fallback voice, 0 ignored by git, 86.5 MB ≤ 150 → all 71 added |
| 3 Queue | **PASS.** check PASS (15 days, 60% hot on every platform, 0 violations) · dry-run 0 invalid, missing 0 on every platform · cloud-run dry: all 8 NOT CONFIGURED, missing_media 0, cannot_render [] · `data/social-runner.log` reverted |
| 4 Gates + wrap | **PASS.** See Gates. Committed, pushed, QUEUE entry, merged `--no-ff` into main, pushed |

## Step 0 — probe output

```
curl https://pypi.org/simple/edge-tts/            → 200
curl https://speech.platform.bing.com/            → 400   (reached Bing; not a 403 policy denial)
$HTTPS_PROXY/__agentproxy/status recentRelayFailures → []
```
Gate: PyPI reachable AND Bing not policy-denied → PASS. Env had `SSL_CERT_FILE` / `REQUESTS_CA_BUNDLE` = `/root/.ccr/ca-bundle.crt` (the container default, not set by this run); no PYTHONPATH, no sitecustomize.

## Step 1 — live gate

```
$ cd content/youtube && python -c "from hoko import tts; print(tts.synth('G day, HOKO test render.', '/tmp/hoko-gate'))"
edge-tts:en-AU-WilliamMultilingualNeural
$ ffprobe /tmp/hoko-gate.wav → stream codec_name=pcm_s16le codec_type=audio · duration=2.304000
```
`python -m unittest discover -s tools/social/tests -t .` → **Ran 54 tests … OK**. This is the first real-endpoint check of the branch's `tts.py` change. Until now it had only been tested against stand-ins.

## Step 2 — render

Commands: `run.py reel sealed <id> --hook 3 --force` for EB-05 `15431829848342`, M7 `15417947455766`, FB12 `15417947291926`, then `python -m tools.social render` → `reel sealed all`, `reel slab all`, `calendar` (tips, roundups incl. `one-piece` + `under-200`, 6 BF beats). `calendar.md: 72 rows, 0 missing reels`. 0 tracebacks, 0 "fallback voice" (every clip William).

| Type | Clips | MiB |
|---|---|---|
| sealed | 45 | 47 |
| slab | 12 | 19 |
| tips | 4 | 5 |
| roundups | 4 | 7 |
| beats | 6 | 8 |
| **total** | **71** | **86.5 MB (`du -ch`: 83M)** |

Gate per clip: 1080×1920 video, audio stream present, 8–20 s, sidecar exists, no "$" in the sidecar `voiceover`. `git check-ignore` on all 71 → 0 ignored; `git status` showed all 71 as added.

Sidecars: 30 existing `.json` updated by the render, `tts` `piper:en_GB-alan-medium` → `edge-tts:en-AU-WilliamMultilingualNeural` plus `duration`, voiceover text unchanged. 3 new hook sidecars rendered (`sealed/10734771765526/h2`, `10734775664918/h2`, `15398993723670/h2`, + `.caption.txt`), none referenced by the queue.

Not rendered (no mp4, sidecar only): `sealed/10734771896598/h1,h2`, `sealed/10734773666070/h1,h2`. Neither ID is in `sealed/source.csv` or `content/social-queue.json` any more (dropped products), so `reel sealed all` skips them. NOT KEPT: none.

### Clip table

| Clip | Voice | Duration | Size | Gate |
|---|---|---|---|---|
| beats/2026-11-01 | en-AU-WilliamMultilingualNeural | 10.74 s | 1.18 MB | PASS |
| beats/2026-11-20 | en-AU-WilliamMultilingualNeural | 10.78 s | 1.20 MB | PASS |
| beats/2026-11-24 | en-AU-WilliamMultilingualNeural | 10.74 s | 1.58 MB | PASS |
| beats/2026-11-26 | en-AU-WilliamMultilingualNeural | 10.63 s | 1.05 MB | PASS |
| beats/2026-11-27 | en-AU-WilliamMultilingualNeural | 11.80 s | 1.00 MB | PASS |
| beats/2026-11-30 | en-AU-WilliamMultilingualNeural | 11.74 s | 1.34 MB | PASS |
| roundups/mega-era | en-AU-WilliamMultilingualNeural | 11.80 s | 1.90 MB | PASS |
| roundups/one-piece | en-AU-WilliamMultilingualNeural | 11.80 s | 1.88 MB | PASS |
| roundups/preorders | en-AU-WilliamMultilingualNeural | 11.80 s | 1.54 MB | PASS |
| roundups/under-200 | en-AU-WilliamMultilingualNeural | 11.80 s | 1.93 MB | PASS |
| sealed/10734771765526/h1 | en-AU-WilliamMultilingualNeural | 8.27 s | 0.84 MB | PASS |
| sealed/10734771765526/h2 | en-AU-WilliamMultilingualNeural | 8.63 s | 0.92 MB | PASS |
| sealed/10734771798294/h1 | en-AU-WilliamMultilingualNeural | 8.98 s | 0.96 MB | PASS |
| sealed/10734771798294/h2 | en-AU-WilliamMultilingualNeural | 9.40 s | 1.00 MB | PASS |
| sealed/10734773633302/h1 | en-AU-WilliamMultilingualNeural | 8.58 s | 1.26 MB | PASS |
| sealed/10734773633302/h2 | en-AU-WilliamMultilingualNeural | 8.98 s | 1.36 MB | PASS |
| sealed/10734773731606/h1 | en-AU-WilliamMultilingualNeural | 8.38 s | 1.04 MB | PASS |
| sealed/10734773731606/h2 | en-AU-WilliamMultilingualNeural | 8.80 s | 1.08 MB | PASS |
| sealed/10734773862678/h1 | en-AU-WilliamMultilingualNeural | 9.07 s | 1.31 MB | PASS |
| sealed/10734773862678/h2 | en-AU-WilliamMultilingualNeural | 9.51 s | 1.37 MB | PASS |
| sealed/10734773895446/h1 | en-AU-WilliamMultilingualNeural | 8.87 s | 0.94 MB | PASS |
| sealed/10734773895446/h2 | en-AU-WilliamMultilingualNeural | 9.27 s | 1.03 MB | PASS |
| sealed/10734775370006/h1 | en-AU-WilliamMultilingualNeural | 9.18 s | 0.97 MB | PASS |
| sealed/10734775370006/h2 | en-AU-WilliamMultilingualNeural | 9.58 s | 1.02 MB | PASS |
| sealed/10734775435542/h1 | en-AU-WilliamMultilingualNeural | 8.91 s | 1.15 MB | PASS |
| sealed/10734775435542/h2 | en-AU-WilliamMultilingualNeural | 9.33 s | 1.20 MB | PASS |
| sealed/10734775501078/h1 | en-AU-WilliamMultilingualNeural | 8.77 s | 1.10 MB | PASS |
| sealed/10734775501078/h2 | en-AU-WilliamMultilingualNeural | 9.18 s | 1.16 MB | PASS |
| sealed/10734775664918/h1 | en-AU-WilliamMultilingualNeural | 8.47 s | 1.06 MB | PASS |
| sealed/10734775664918/h2 | en-AU-WilliamMultilingualNeural | 8.80 s | 1.09 MB | PASS |
| sealed/10734778482966/h1 | en-AU-WilliamMultilingualNeural | 8.47 s | 0.99 MB | PASS |
| sealed/10734778482966/h2 | en-AU-WilliamMultilingualNeural | 8.84 s | 1.08 MB | PASS |
| sealed/10734779072790/h1 | en-AU-WilliamMultilingualNeural | 8.53 s | 0.74 MB | PASS |
| sealed/10734779072790/h2 | en-AU-WilliamMultilingualNeural | 8.94 s | 0.78 MB | PASS |
| sealed/10734779138326/h1 | en-AU-WilliamMultilingualNeural | 8.67 s | 1.00 MB | PASS |
| sealed/10734779138326/h2 | en-AU-WilliamMultilingualNeural | 8.97 s | 1.01 MB | PASS |
| sealed/10734779171094/h1 | en-AU-WilliamMultilingualNeural | 8.91 s | 0.83 MB | PASS |
| sealed/10734779171094/h2 | en-AU-WilliamMultilingualNeural | 9.33 s | 0.92 MB | PASS |
| sealed/10734779433238/h1 | en-AU-WilliamMultilingualNeural | 8.17 s | 0.89 MB | PASS |
| sealed/10734779433238/h2 | en-AU-WilliamMultilingualNeural | 8.31 s | 0.93 MB | PASS |
| sealed/10734779433238/h4 | en-AU-WilliamMultilingualNeural | 11.80 s | 1.44 MB | PASS |
| sealed/10734779564310/h1 | en-AU-WilliamMultilingualNeural | 8.87 s | 1.28 MB | PASS |
| sealed/10734779564310/h2 | en-AU-WilliamMultilingualNeural | 9.27 s | 1.37 MB | PASS |
| sealed/15398993723670/h1 | en-AU-WilliamMultilingualNeural | 9.70 s | 1.10 MB | PASS |
| sealed/15398993723670/h2 | en-AU-WilliamMultilingualNeural | 10.07 s | 1.12 MB | PASS |
| sealed/15413124170006/h1 | en-AU-WilliamMultilingualNeural | 8.41 s | 0.93 MB | PASS |
| sealed/15413124170006/h2 | en-AU-WilliamMultilingualNeural | 8.80 s | 0.97 MB | PASS |
| sealed/15413124268310/h1 | en-AU-WilliamMultilingualNeural | 8.60 s | 0.98 MB | PASS |
| sealed/15413124268310/h2 | en-AU-WilliamMultilingualNeural | 9.01 s | 1.06 MB | PASS |
| sealed/15413357543702/h1 | en-AU-WilliamMultilingualNeural | 9.13 s | 1.37 MB | PASS |
| sealed/15413357543702/h2 | en-AU-WilliamMultilingualNeural | 9.50 s | 1.45 MB | PASS |
| sealed/15417946865942/h3 | en-AU-WilliamMultilingualNeural | 11.80 s | 1.39 MB | PASS |
| sealed/15417947291926/h3 | en-AU-WilliamMultilingualNeural | 11.80 s | 1.05 MB | PASS |
| sealed/15417947455766/h3 | en-AU-WilliamMultilingualNeural | 11.80 s | 0.69 MB | PASS |
| sealed/15431829848342/h3 | en-AU-WilliamMultilingualNeural | 11.80 s | 1.00 MB | PASS |
| slab/10655248122134/h0 | en-AU-WilliamMultilingualNeural | 9.87 s | 1.34 MB | PASS |
| slab/10655248122134/h1 | en-AU-WilliamMultilingualNeural | 8.00 s | 1.04 MB | PASS |
| slab/10655248220438/h0 | en-AU-WilliamMultilingualNeural | 11.30 s | 3.14 MB | PASS |
| slab/10655248220438/h1 | en-AU-WilliamMultilingualNeural | 8.00 s | 2.22 MB | PASS |
| slab/10655248613654/h0 | en-AU-WilliamMultilingualNeural | 10.57 s | 1.96 MB | PASS |
| slab/10655248613654/h1 | en-AU-WilliamMultilingualNeural | 8.00 s | 1.32 MB | PASS |
| slab/10655248711958/h0 | en-AU-WilliamMultilingualNeural | 10.70 s | 1.82 MB | PASS |
| slab/10655248711958/h1 | en-AU-WilliamMultilingualNeural | 8.00 s | 1.26 MB | PASS |
| slab/10655248777494/h0 | en-AU-WilliamMultilingualNeural | 9.87 s | 1.50 MB | PASS |
| slab/10655248777494/h1 | en-AU-WilliamMultilingualNeural | 8.00 s | 1.14 MB | PASS |
| slab/10655248810262/h0 | en-AU-WilliamMultilingualNeural | 8.84 s | 1.42 MB | PASS |
| slab/10655248810262/h1 | en-AU-WilliamMultilingualNeural | 8.00 s | 1.22 MB | PASS |
| tips/buyback | en-AU-WilliamMultilingualNeural | 11.80 s | 1.14 MB | PASS |
| tips/no-outer-shrink | en-AU-WilliamMultilingualNeural | 10.77 s | 1.09 MB | PASS |
| tips/spot-a-fake | en-AU-WilliamMultilingualNeural | 11.80 s | 1.06 MB | PASS |
| tips/verified-graders | en-AU-WilliamMultilingualNeural | 11.67 s | 1.02 MB | PASS |

## Step 3 — queue

```
days per platform {'tiktok_queue': 15, 'pinterest': 15, 'youtube': 15, 'instagram': 15, 'facebook': 15, 'discord': 15}
hot sets ['M6a', 'EB-05', 'OP-18', 'M7', 'FB12'] share target 60% · tiktok_queue 27/45 (60%) · pinterest 27/45 (60%) · youtube 18/30 (60%) · instagram 18/30 (60%) · facebook 18/30 (60%) · discord 9/15 (60%) · all 117/195 (60%)
PASS
```
```
discord       valid  14  invalid  0  past  1  media present   0 / missing   0
facebook      valid  28  invalid  0  past  2  media present  28 / missing   0
instagram     valid  28  invalid  0  past  2  media present  28 / missing   0
pinterest     valid  43  invalid  0  past  2  media present   0 / missing   0
tiktok        valid  42  invalid  0  past  3  media present  42 / missing   0
tiktok_queue  valid  14  invalid  0  past  1  media present  42 / missing   0
youtube       valid  28  invalid  0  past  2  media present  28 / missing   0
```
cloud-run `--dry-run --no-render`: instagram, facebook, youtube, pinterest, discord, tiktok_queue, tiktok, shopify_files → all NOT CONFIGURED · invalid 0 · `missing_media` 0 · `cannot_render` [] · would_post 0. `git checkout -- data/social-runner.log` done; `data/social-dryrun.json` is gitignored.

## Gates

| Gate | Result |
|---|---|
| 54 tests OK | PASS |
| live William render | PASS (2.30 s, `edge-tts:en-AU-WilliamMultilingualNeural`) |
| every mp4 passes ffprobe | PASS (71/71) |
| total mp4 ≤ 150 MB | PASS (86.5 MB) |
| dry-run missing media 0 | PASS (0 on every platform; cloud-run 0 / []) |
| 0 banned words on changed text files | PASS (see Wrap) |

## Findings (not actioned)
- `h*.caption.txt` files still carry price lines (all 61 committed ones, plus the 3 new h2). The queue builds its captions in `tools/social/captions.py` and doesn't read these, so posted captions are price-free; the files are only used for manual posting on the phone. Still open from bf-render.
- The h2 sealed hooks put a price on screen (`hook` text, e.g. "Abyss Eye for $190 …"). None of the h2 clips is in the 14-day queue. Pre-order on-screen price card from bf-render Findings also still open.
- `tools/social/cloud_run.py` docstring (lines 10–11) still says edge-tts can't connect from the cloud. That's stale now that the live gate passed. Not edited (outside this brief).
- The render reached Bing and HuggingFace (faster-whisper model download) without changes. Egress still varies between sessions (the last run had all four hosts denied), so the allowlist line in MANUAL still applies.

## NOT CHECKED
- Each clip by eye or ear (gates are ffprobe + sidecar only). Whisper word-timing alignment not reviewed.
- Live posting (no platform keys). Shopify not read at all this run.
- `source.csv` freshness (no Shopify token): rendered from the committed rows.

## MANUAL

**Ethan only**
- BF free-shipping automatic still to be edited (all orders $100+ → Japanese Sealed collection, no minimum, 27–30 Nov). Unchanged.
- Platform keys (list in `REPORT-2026-10-17-bf-lockin.md` MANUAL). Every platform is NOT CONFIGURED.
- Environment setup script line: `pip install edge-tts piper-tts faster-whisper pillow numpy requests` + `ffmpeg` on PATH.
- Network allowlist: `pypi.org`, `files.pythonhosted.org`, `speech.platform.bing.com`, `huggingface.co`.

**PC only**
- `git pull` on main brings the 71 mp4s down (86.5 MB). No PC render needed now.

## Wrap
- Commit on `claude/bf-media-1017`: 71 mp4s, 30 updated + 3 new sidecars (+3 caption.txt), this report, QUEUE.md entry.
- Banned-word grep over every changed text file (sidecar .json, .caption.txt, this report, QUEUE.md; CDN filenames, IANA tz and the gate's own regex excluded): 0 hits.
- `git push origin claude/bf-media-1017`, then `git merge --no-ff claude/bf-media-1017` into `main`, `git push origin main`. Confirmed with `git ls-remote --heads origin`.

## COMPLETE
