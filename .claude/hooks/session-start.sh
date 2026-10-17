#!/bin/bash
# Cloud sessions only: install what `python -m tools.social cloud-run` needs to render clips
# (ffmpeg ships with the image; Piper is the cloud voice, see tools/social/README.md "Rendering in the cloud").
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

pip install -q --disable-pip-version-check --root-user-action=ignore pillow numpy requests piper-tts
