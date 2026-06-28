import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "poster"))
import figures  # noqa: E402


def test_make_polyline_maps_and_flips_y():
    d = figures.make_polyline([0, 1, 2], [0, 1, 0], 0, 2, 0, 1, 100, 50)
    assert d == "M0.0,50.0 L50.0,0.0 L100.0,50.0"
