import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = os.path.join(HERE, "poster", "assets", "schematic.svg")


def test_schematic_valid_and_labelled():
    import xml.dom.minidom as md
    txt = open(SVG, encoding="utf-8").read()
    md.parseString(txt)  # raises if not well-formed XML
    for token in ["forecast", "realised", "mu D", "1B6FC4", "C62828"]:
        assert token in txt, token
    assert "—" not in txt  # no em dash
