#!/bin/sh
# Repo banned-word gate: every term on the CLAUDE.md list.
# Excluded: run history (reports/, REPORT-*.md, data/*.md run logs), docs/archive/, *.json, calendar.md, mp4,
# the gate implementers (CLAUDE.md + template banned line, captions.py / relist-reconcile.py regexes, tests),
# the tz id Australia/Melbourne and Shopify CDN filenames.
cd "${1:-.}"
git grep -I -n -i -E 'whatnot|top rated|myster(y|ies) pack|repack|\bofficial\b|same[- ]day dispatch|melbourne|\b1\.4k\b|HOKO10|\b2024\b' -- . \
  ':!reports/' ':!REPORT-*.md' ':!docs/archive/' ':!*.json' ':!content/youtube/calendar.md' ':!*.mp4' ':!data/*.md' \
  ':!tools/social/captions.py' ':!tools/relist-reconcile.py' ':!tools/social/tests/' ':!content/youtube/hoko/tests/' \
  | grep -v -E 'Australia/Melbourne|cdn\.shopify\.com|^(CLAUDE\.md|local-setup/CLAUDE\.md\.template):25:'
