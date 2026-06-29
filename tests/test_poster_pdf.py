import os
import re
import shutil
import subprocess

import pytest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(HERE, "results", "poster", "poster.pdf")
HTML = os.path.join(HERE, "poster", "poster.html")


def test_pdf_is_single_a0_page():
    if shutil.which("pdfinfo") is None:
        pytest.skip("pdfinfo (poppler) not installed (absent in CI)")
    if not os.path.exists(PDF):
        pytest.skip("poster.pdf not built; run the poster build (absent in CI)")
    assert os.path.getsize(PDF) > 20000
    info = subprocess.check_output(["pdfinfo", PDF], text=True)
    assert re.search(r"Pages:\s*1", info)
    m = re.search(r"Page size:\s*([\d.]+) x ([\d.]+) pts", info)
    w, h = float(m.group(1)), float(m.group(2))
    assert abs(w - 2383.94) < 3 and abs(h - 3370.39) < 3, (w, h)


def test_no_unfilled_tokens():
    if not os.path.exists(HTML):
        pytest.skip("poster.html not built; run the poster build (absent in CI)")
    html = open(HTML, encoding="utf-8").read()
    assert "{{" not in html and "?eq:" not in html and "?fig:" not in html
