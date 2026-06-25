#!/usr/bin/env bash
# Download fonts and KaTeX into poster/assets, copy the IE logo.
# Safe to re-run. On any download failure the build falls back to system
# fonts (see poster.css), so a missing network does not block the poster.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
mkdir -p assets/fonts assets/katex/fonts assets/cache

# IE logo (always available locally).
cp -f ../docs/Report/IELogo.jpeg assets/ielogo.jpeg

# Node packages (puppeteer-core uses the already-installed Google Chrome, no
# Chromium download).
npm install --no-audit --no-fund || echo "WARN: npm install failed, render task will report this"

# Vendor KaTeX css and fonts from the installed package.
if [ -d node_modules/katex/dist ]; then
  cp -f node_modules/katex/dist/katex.min.css assets/katex/katex.min.css
  cp -f node_modules/katex/dist/fonts/* assets/katex/fonts/ 2>/dev/null || true
fi

# Fonts via google-webfonts-helper (packaged static woff2 + ttf). Each family
# is independent; a failure leaves the system-font fallback in poster.css.
fetch_font () {
  local id="$1" variants="$2"
  for fmt in woff2 ttf; do
    curl -sL --max-time 30 \
      "https://gwfh.mranftl.com/api/fonts/${id}?download=zip&subsets=latin&variants=${variants}&formats=${fmt}" \
      -o "assets/fonts/${id}-${fmt}.zip" \
      && unzip -o -q "assets/fonts/${id}-${fmt}.zip" -d assets/fonts \
      && rm -f "assets/fonts/${id}-${fmt}.zip" \
      || echo "WARN: could not fetch ${id} ${fmt}; system fallback will be used"
  done
}
fetch_font inter "regular,600,700"
fetch_font fraunces "regular,600,700"
fetch_font ibm-plex-mono "regular,500,700"

echo "Fonts present:"; ls assets/fonts 2>/dev/null | grep -iE 'inter|fraunces|plex' || echo "  none (using system fallback)"
echo "KaTeX present:"; ls assets/katex/katex.min.css 2>/dev/null || echo "  MISSING (math will not be styled)"
