"""Smoke test that the package imports cleanly.

Phase-specific tests are added alongside each phase. This file just keeps the
test runner happy until phase 1 lands.
"""

import reflexive_market


def test_version_string():
    assert isinstance(reflexive_market.__version__, str)
