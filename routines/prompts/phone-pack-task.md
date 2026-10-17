# Phone pack — scheduled task prompt

Scheduled task `trig_01QeakRTdC9hVqwinFfMP1CB` · 07:10 daily (Victoria) · cloud.

> **Push works only after Ethan adds the repo to the task's sources in claude.ai.** (`ethanryan28-cmd/hoko-collectables`;
> Claude Code cannot do it.) Until then step 3 gets a 403 from the git proxy; the task says so in one line and the
> message still goes out.

To install: paste everything between the two `---8<---` lines into the task's prompt.

---8<---

Go. From Ethan: send me today's HOKO phone pack.

Read-only on the shop. No Shopify writes. Never change products, prices, discounts, inventory, listings or captions.
The message is the deliverable: if any later step fails, still send it.

1. Get the repo (skip mp4 downloads; the pack links to them on raw.githubusercontent.com):
   - If `hoko-collectables/` already exists: `cd hoko-collectables && git checkout main && git pull`.
   - Else: `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/ethanryan28-cmd/hoko-collectables && cd hoko-collectables`.

2. Run `python -m tools.social phone-pack --days 1` and capture stdout (it also appends to
   `data/phone-pack-log.csv`). If it exits non-zero, keep its output and note that for the message.

3. Push the log (try it before sending so the message can say how it went):
   - `git checkout -b claude/phone-pack-log-<YYYYMMDD>` (today's Victoria date);
   - `git add data/phone-pack-log.csv` — that file only — and commit `phone-pack log <YYYY-MM-DD>`;
   - `git push -u origin claude/phone-pack-log-<YYYYMMDD>`.
   If nothing changed (re-run, every row already logged), skip the commit: the status is `log unchanged`.
   If the push is refused (403 from the git proxy or any other error), retry at most once, then move on with
   status `Log not pushed: <reason>`. Do not open a PR. Do not merge.

4. Send the stdout as ONE SendUserMessage, phone-readable:
   - the stdout as printed (headings, save line, clip links, product links, caption blocks), nothing rewritten;
   - Australian spelling in anything you add; no prices, no new copy;
   - if the command exited non-zero, one line saying so;
   - one line with the log status from step 3;
   - last line: `NOT CHECKED: <what you did not verify, e.g. clip links opened on a phone, captions re-read>`.
   If anything above broke, still send whatever you have — the message is the deliverable.

5. PushNotification. First sentence exactly: `PHONE PACK <YYYY-MM-DD> — N clips ready.` (N = number of `## ` items
   in the stdout; the date is the `# HOKO phone pack` heading's date). Second sentence: `Log pushed to <branch>.`,
   `Log unchanged.` or `Log not pushed: <reason>.`

---8<---

## Notes

- `--days 1` = today in Victoria, or the next day with items if today is empty. Bump to `--days 2` to get
  tomorrow's pack as well.
- Save line: set env `PHONE_PACK_FILES_FIRST=1` in the task environment to print
  "Tap mp4 → Files → Share → Save Video → post." instead of the default
  "Tap mp4 → share → Save Video → post." No code change needed.
- The log dedupes on date + platform + asset_id, so a re-run prints the same pack without adding rows.
