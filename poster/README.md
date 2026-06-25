# Capstone poster

A0 portrait scientific poster, built from HTML and CSS rendered by headless
Google Chrome, with vector figures regenerated from results/data.

## Rebuild

    cd poster
    ./fetch_assets.sh     # once, downloads fonts and KaTeX
    ./build.sh            # regenerate figures and the PDF

Output: results/poster/poster.pdf (A0, 841 x 1189 mm) and poster_preview.png.

The first figures.py run executes the Monte Carlo simulations and caches the
arrays under assets/cache, so later runs are fast. Pass --recompute to
figures.py to force a fresh simulation.

## Prerequisites

- Python with numpy and matplotlib, plus the local reflexive_market package.
- Node, and Google Chrome installed at the standard macOS path.
- poppler (pdfinfo, pdftoppm) for verification and the preview image.
