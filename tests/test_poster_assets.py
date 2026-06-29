# tests/test_poster_assets.py
import os

import pytest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HERE, "poster", "assets")


def test_ie_logo_copied():
    logo = os.path.join(ASSETS, "ielogo.jpeg")
    if not os.path.exists(logo):
        pytest.skip("logo not vendored; run poster/fetch_assets.sh (absent in CI)")
    assert os.path.getsize(logo) > 1000


def test_katex_css_vendored():
    css = os.path.join(ASSETS, "katex", "katex.min.css")
    if not os.path.exists(css):
        pytest.skip("katex not vendored; run poster/fetch_assets.sh (absent in CI)")
    assert os.path.getsize(css) > 1000
