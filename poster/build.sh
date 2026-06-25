#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
python3 figures.py "$@"
node build.mjs
# Preview image for a quick visual check (poppler).
pdftoppm -png -r 50 ../results/poster/poster.pdf ../results/poster/poster_preview >/dev/null 2>&1 \
  && mv -f ../results/poster/poster_preview-1.png ../results/poster/poster_preview.png 2>/dev/null || true
echo "done"
