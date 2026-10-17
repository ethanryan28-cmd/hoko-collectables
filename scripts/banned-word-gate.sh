#!/bin/sh
# Repo banned-word gate: every term on the CLAUDE.md list, via tools/banned_words.py (allowlist of real card/set names,
# matched case-sensitively as whole phrases). git grep picks candidate lines; the module re-checks each after the allowlist.
# Excluded: run history (reports/, REPORT-*.md, QUEUE.md, data/*.md and data/*.csv run logs and store exports), docs/archive/,
# *.json, calendar.md, mp4, the gate implementers (this script, dated run scripts scripts/shopify/*_2026_*.py, tools/banned_words.py, CLAUDE.md + template banned line,
# captions.py / relist-reconcile.py regexes, tests), the tz id Australia/Melbourne and Shopify CDN filenames.
cd "${1:-.}"
git grep -I -n -i -E 'whatnot|top[- ]rated|myst|chaos|re-?pack|\bofficial\b|same[- ]day dispatch|melbourne|\b1\.4k\b|HOKO10|\b2024\b' -- . \
  ':!reports/' ':!REPORT-*.md' ':!QUEUE.md' ':!docs/archive/' ':!*.json' ':!content/youtube/calendar.md' ':!*.mp4' ':!data/*.md' ':!data/*.csv' \
  ':!scripts/banned-word-gate.sh' ':!scripts/shopify/*_2026_*.py' ':!tools/banned_words.py' ':!tools/social/captions.py' ':!tools/relist-reconcile.py' \
  ':!tools/tests/' ':!tools/social/tests/' ':!content/youtube/hoko/tests/' \
  | grep -v -E 'Australia/Melbourne|cdn\.shopify\.com|^(CLAUDE\.md|local-setup/CLAUDE\.md\.template):25:' \
  | python3 -m tools.banned_words --grep
