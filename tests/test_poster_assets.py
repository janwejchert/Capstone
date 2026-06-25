# tests/test_poster_assets.py
import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HERE, "poster", "assets")

def test_ie_logo_copied():
    assert os.path.getsize(os.path.join(ASSETS, "ielogo.jpeg")) > 1000

def test_katex_css_vendored():
    css = os.path.join(ASSETS, "katex", "katex.min.css")
    assert os.path.exists(css), "run poster/fetch_assets.sh"
    assert os.path.getsize(css) > 1000
