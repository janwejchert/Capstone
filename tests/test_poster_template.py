import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(HERE, "poster")


def test_template_has_required_content():
    html = open(os.path.join(P, "poster.template.html"), encoding="utf-8").read()
    for s in ["Nacho Molina Clemente", "IE School of Science and Technology",
              "MSc in Business Analytics and Data Science", "July 2026",
              "jan.wejchert@student.ie.edu"]:
        assert s in html, s
    for tok in ["{{fig:dual_channel}}", "{{fig:schematic}}", "{{eq:return_law}}",
                "{{eq:decomposition}}", "{{val:r2_real_high}}", "{{logo}}"]:
        assert tok in html, tok
    assert "—" not in html  # no em dash


def test_css_is_a0_portrait():
    css = open(os.path.join(P, "poster.css"), encoding="utf-8").read()
    assert "841mm 1189mm" in css
    assert "print-color-adjust" in css
    assert "—" not in css
