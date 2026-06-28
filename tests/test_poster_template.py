import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(HERE, "poster")


def test_template_has_required_content():
    html = open(os.path.join(P, "poster.template.html"), encoding="utf-8").read()
    for s in ["Nacho Molina Clemente", "IE School of Science and Technology",
              "MSc in Business Analytics and Data Science", "July 2026",
              "jan.wejchert@student.ie.edu",
              "One forecast, two channels", "Self-fulfilment",
              "Independent signal", "one simulated market",
              "As adoption rises"]:
        assert s in html, s
    for tok in ["{{eq:decomposition}}", "{{eq:return_law}}",
                "{{val:r2_real_high}}", "{{val:price_path_d}}",
                "{{val:result_real_d}}", "{{val:result_da_d}}",
                "{{val:plateau_real}}", "{{logo}}"]:
        assert tok in html, tok
    assert "—" not in html  # no em dash


def test_css_is_a0_portrait():
    css = open(os.path.join(P, "poster.css"), encoding="utf-8").read()
    assert "841mm 1189mm" in css
    assert "print-color-adjust" in css
    assert "—" not in css
