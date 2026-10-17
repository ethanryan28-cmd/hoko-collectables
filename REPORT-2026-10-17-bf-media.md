# REPORT — 2026-10-17 BF media (`claude/bf-media-1017`)

Unattended **cloud** run (Linux container, no `.env`), brief pasted by Ethan as the session's opening message. Authorised: clip renders, committing rendered mp4s, `tts.py` proxy-CA change, `.gitignore` edit, README note, backup + read-back on every write. **0 Shopify writes, 0 Shopify reads.** No price, discount, inventory, order, product or theme change.

**Outcome: STOPPED at the Step 1 live-render gate — network policy, not code.** This session's egress proxy answers **403 (policy denial)** for every host the render pipeline needs: `pypi.org`, `files.pythonhosted.org` (no `edge-tts`, `piper-tts`, `faster-whisper`, `aiohttp` can be installed — none is present in the image), `speech.platform.bing.com` (edge-tts' endpoint) and `huggingface.co` (the Piper voice download). The last run (`bf-render`) had PyPI + Bing open; this one has neither. **0 clips rendered, 0 mp4s committed.** Everything that does not need the network was done, tested and pushed on the branch; **not merged** (failed gate = stop).

## Summary

| Step | Result |
|---|---|
| 0 State | PASS — read CLAUDE.md, QUEUE.md, `REPORT-2026-10-17-bf-render.md`, git log (HEAD `307d1a1`, the bf-render merge). 72 sidecar `.json` under `content/youtube/reels/`, **0 `.mp4`** on disk (lost with the bf-render container, as the brief said). Branch `claude/bf-media-1017` created from `main` |
| 1 TTS proxy fix | **PASS (code + 54 tests OK) / FAIL (live 5-second render — `speech.platform.bing.com` 403 at the proxy and `edge-tts` not installable, PyPI 403)** — details below |
| 2 Render + keep | **FAIL — nothing renderable.** `pip install edge-tts piper-tts faster-whisper` → `pypi.org` / `files.pythonhosted.org` 403 (policy). No TTS engine of any kind on the box (no edge-tts, piper, aiohttp, espeak). Piper fallback impossible too (package + `huggingface.co` voice download both denied). `.gitignore` un-ignore + README line **done** (verified with `git check-ignore`, table below) so the next run that can render will keep its mp4s. Total mp4 committed: **0 MB** |
| 3 Queue | PASS for check: 15 days every platform, 60% hot on all 6 (117/195 all), 0 violations. dry-run: **0 invalid**, **missing media 30 unique clips** (facebook/instagram/youtube 28 each, tiktok 42 slots, tiktok_queue 42, discord 0, pinterest 0) → **FAIL** on the "missing media 0" gate — the 30 clips are exactly the mp4s this run could not render. cloud-run `--dry-run --no-render`: all 8 platforms NOT CONFIGURED (expected), invalid 0, `missing_media` 30, `cannot_render` = the same 30 |
| 4 Gates + wrap | Tests OK · banned words 0 · ffprobe N/A (no mp4) · missing media 30 (FAIL) → **branch pushed, NOT merged**, QUEUE.md entry added on the branch |

## Step 1 — `content/youtube/hoko/tts.py` diff summary

Backup: `reports/backups/2026-10-17-bf-media-tts-before.py` (read back: differs from the new file only by the edit, +61 lines, 0 removed).

Read the real edge-tts source first (`rany2/edge-tts` at 7.3.1, anonymous git read): `communicate.py` builds a module-level `_SSL_CTX = ssl.create_default_context(cafile=certifi.where())` and passes it as `ssl=_SSL_CTX` on every `session.ws_connect(...)`. In aiohttp a per-request `ssl=` context **overrides the connector's**, so the brief's "pass the context to the aiohttp connector" alone would have had no effect on 7.x. The fix does both, verification ON throughout:

- `ca_bundle()` — first of `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE` that points at an existing file, else `/root/.ccr/ca-bundle.crt` when it exists, else `None`.
- `edge_ssl_context()` — `None` when `ca_bundle()` is `None` (the PC path: `ssl.create_default_context` is never called); otherwise `ssl.create_default_context(cafile=<bundle>)` — `CERT_REQUIRED` + `check_hostname` stay on, the bundle only adds the proxy CA to the roots. No `ssl=False`, no `verify=False` anywhere.
- `edge_kwargs(ctx)` — `{}` for `None`; otherwise `connector=aiohttp.TCPConnector(ssl=ctx)` plus `proxy=$HTTPS_PROXY` (aiohttp's `trust_env` does not apply env proxies to `wss://` URLs, so edge-tts needs it explicitly — this is what the bf-render sitecustomize did by hand).
- `_edge()` — unchanged call when `ctx is None` (`Communicate(text, voice, rate='+8%')`, byte-for-byte the old behaviour). With a context: sets `edge_tts.communicate._SSL_CTX = ctx` **only if that attribute exists** (version guard, no AttributeError on other releases), passes the kwargs, closes the connector in `finally` if edge-tts didn't.
- Module docstring explains the above.

**Unit tests** — `tools/social/tests/test_tts.py`, 7 tests (loads `tts.py` by path; edge_tts/aiohttp are stand-ins in `sys.modules`, nothing touches the network):
`SSL_CERT_FILE` → context created with `cafile=<temp PEM>` (asserted on a wrapped `ssl.create_default_context`), verify mode `CERT_REQUIRED`, hostname check on · same for `REQUESTS_CA_BUNDLE` · ccr bundle used when no env var · env var pointing at a missing file ignored · no env var → `None` and `create_default_context` never called, `edge_kwargs(None) == {}` · `_edge` with CA passes connector + proxy and pins `_SSL_CTX` to the same verifying context, connector closed · `_edge` with CA but no proxy env omits `proxy` and tolerates an edge-tts without `_SSL_CTX` · `_edge` without CA calls `Communicate` with exactly `text, voice, rate` and leaves `_SSL_CTX` alone.
`python -m unittest discover -s tools/social/tests -t .` → **Ran 54 tests … OK** (47 existing + 7 new).

**Live gate** — `edge_tts` cannot be imported (not installed, PyPI 403) and `speech.platform.bing.com:443` is a proxy policy denial (`recentRelayFailures`: "gateway answered 403 to CONNECT"). Not retried (README: do not retry policy denials). **FAIL — environment.** The fix is exercised against stand-ins only; it still needs one real en-AU render in a session where Bing is reachable before it is trusted.

## Step 2 — clip table

| Clip | Voice | Duration | Size | Gate |
|---|---|---|---|---|
| (none — 0 of the 30 queue-referenced clips + 6 beats rendered) | — | — | — | FAIL (no TTS engine: PyPI, Bing and HuggingFace all 403) |

Total MB committed: **0**. Would-be clips (queue-referenced, from cloud-run `cannot_render`): sealed `10734773862678/h2`, `10734773895446/h2`, `10734775501078/h1`+`h2`, `10734778482966/h2`, `10734779564310/h1`, `15398993723670/h1`, `15413124268310/h1`, `15413357543702/h1`, `15417946865942/h3`, `15417947291926/h3`, `15417947455766/h3`, `15431829848342/h3`; slab `10655248122134/h0`+`h1`, `10655248220438/h0`+`h1`, `10655248613654/h1`, `10655248711958/h0`+`h1`, `10655248777494/h0`+`h1`, `10655248810262/h0`+`h1`; tips `buyback`, `no-outer-shrink`, `spot-a-fake`, `verified-graders`; roundups `mega-era`, `preorders` — 30. Plus the 6 BF beats (20–30 Nov, outside the 14-day window, so not in `cannot_render`) and `roundups/one-piece`, `under-200` from the bf-render list.

**`.gitignore` (done)** — `content/youtube/.gitignore`: added `!reels/**/*.mp4` after `*.mp4` (+ a comment). Backup `reports/backups/2026-10-17-bf-media-youtube-gitignore-before`. Read-back with `git check-ignore`:

| Path | Now |
|---|---|
| `reels/sealed/<id>/h2.mp4`, `reels/beats/x.mp4` | **tracked-able** |
| `out/<video>/short_1.mp4` (Shorts source/cuts) | ignored |
| `reels/tips/x.wav` | ignored |
| `inbox/x.mp4` | ignored |
| `.cache/piper/x.onnx` | ignored |

**README (done)** — `tools/social/README.md` Cloud section: "Reels are committed; cloud-run only renders what's missing." added, and the now-false sentence "the en-AU edge-tts voice cannot connect from the cloud sandbox" replaced by two lines describing the CA-bundle behaviour; the pip line now reads `pip install edge-tts piper-tts faster-whisper pillow numpy requests`. Backup `reports/backups/2026-10-17-bf-media-social-README-before.md`.

## Step 3 — queue

check: days `{tiktok_queue 15, pinterest 15, youtube 15, instagram 15, facebook 15, discord 15}`; hot share tiktok_queue 27/45, pinterest 27/45, youtube 18/30, instagram 18/30, facebook 18/30, discord 9/15, all 117/195 = 60% → PASS. dry-run: discord 14 valid / 0 invalid / media missing 0; facebook 28/0/28; instagram 28/0/28; pinterest 43/0/0; tiktok 42/0/42; tiktok_queue 14/0/42; youtube 28/0/28. `data/social-runner.log` was touched by the dry-run and reverted (`git checkout`), `data/social-dryrun.json` is gitignored.

## Gates

| Gate | Result |
|---|---|
| 54 tests OK | PASS |
| real 5-s edge-tts en-AU render in this session | **FAIL** — edge-tts not installable (PyPI 403), Bing endpoint 403 at proxy |
| every mp4 ffprobe 1080×1920 / audio / 8–20 s / no "$" | NOT CHECKED — no mp4 produced |
| total added mp4 ≤ 150 MB | N/A — 0 MB |
| dry-run missing media 0 | **FAIL** — 30 |
| 0 banned words on changed text files | PASS — grep over `.gitignore`, `tts.py`, `README.md`, `test_tts.py`: 0 hits |
| push branch | see Wrap |

## Findings (not actioned)
- `tools/social/cloud_run.py` docstring (lines 10–11) and its `AU_VOICE_PREFIX` logic still describe edge-tts as unable to connect from the cloud; once the live gate passes, that docstring is stale (code behaviour is fine — it just logs `fallback voice` when piper is used). Not edited: cloud_run.py was outside this brief.
- Egress policy differs run to run: bf-render (this morning) had PyPI + Bing open; this session has PyPI, Bing and HuggingFace all denied. If the environment's allowlist can be pinned (environment settings → network policy), add `pypi.org`, `files.pythonhosted.org`, `speech.platform.bing.com`, `huggingface.co` — otherwise renders are a lottery per session.
- `h*.caption.txt` price lines and the pre-order on-screen price card from the bf-render Findings are still open.

## NOT CHECKED
- Any render, ffprobe, voice or duration — no clip exists.
- The tts.py fix against the real edge-tts/aiohttp — stand-ins only (see Step 1 live gate).
- Live posting (no platform keys); Shopify not read at all this run.

## MANUAL

**Ethan only**
- BF free-shipping automatic still to be edited (all orders $100+ → Japanese Sealed collection, no minimum, 27–30 Nov) — unchanged since bf-render.
- Platform keys (list in `REPORT-2026-10-17-bf-lockin.md` MANUAL).
- Environment setup script line: `pip install edge-tts piper-tts faster-whisper pillow numpy requests` + `ffmpeg` on PATH; and allow `pypi.org`, `files.pythonhosted.org`, `speech.platform.bing.com`, `huggingface.co` in the environment's network policy if that setting exists.
- Merge decision: `claude/bf-media-1017` holds the tts fix (unit-tested), the `.gitignore` un-ignore and the README note. Merge it, or let the next render-capable run re-run the Step 1 live gate and merge (one-line next prompt: "Go. Fetch `claude/bf-media-1017`, pip install edge-tts piper-tts faster-whisper, run the 5-s William gate, then Steps 2–4 of the bf-media brief").

**PC only**
- Until a cloud run can render: `python -m tools.social render` on the PC, then `git add content/youtube/reels/**/*.mp4` (now un-ignored on this branch) and push, so the committed reels exist. The PC still has the pre-bf-render mp4s if they weren't deleted; the three h3 clips (EB-05 `15431829848342`, M7 `15417947455766`, FB12 `15417947291926`) need `--force`.

## Wrap
- Commits on `claude/bf-media-1017`: tts fix + tests + gitignore + README + backups + this report + QUEUE.md entry.
- `git push -u origin claude/bf-media-1017` — see the line below this heading in the pushed version of this file.
- **Not merged** into `main` (two gates failed: live render, missing media 0).

## COMPLETE
