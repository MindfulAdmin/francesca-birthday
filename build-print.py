#!/usr/bin/env python3
"""Build print/index.html from the card panels in index.html, then render print/*.pdf.

Usage: python3 build-print.py
"""
import base64
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).parent
# any local playwright-core install works; override with the PLAYWRIGHT_CORE env var
PLAYWRIGHT_CORE = "/Users/matt/Local Sites/loungemesh/node_modules/playwright-core"
PDF_NAME = "Francesca-19th-birthday-card.pdf"

src = (ROOT / "index.html").read_text()


def panel(open_tag, end_marker):
    """Inner HTML of the panel that starts with open_tag and ends just before end_marker."""
    start = src.index(open_tag) + len(open_tag)
    end = src.index(end_marker, start)
    inner = src[start:end].rstrip()
    assert inner.endswith("</div>"), open_tag
    return inner[: -len("</div>")]


inside_right = panel('<div class="page paper inside-right" aria-hidden="true" id="insideRight">', "<!-- cover -->")
front = panel('<div class="face front paper" id="front">', "<!-- back of cover")
inside_left = panel('<div class="face back paper" id="insideLeft">', "</div>\n\n  <button")

out = ROOT / "print"
out.mkdir(exist_ok=True)
html = (ROOT / "print-template.html").read_text()
html = html.replace("{{FRONT}}", front).replace("{{INSIDE_LEFT}}", inside_left).replace("{{INSIDE_RIGHT}}", inside_right)
html = html.replace("{{PDF_NAME}}", PDF_NAME)
mark = base64.b64encode((ROOT / "mindful-mark.png").read_bytes()).decode()
html = html.replace("{{MARK}}", "data:image/png;base64," + mark)
(out / "index.html").write_text(html)

# Chrome's own --print-to-pdf shrinks this layout, so render through Playwright instead
subprocess.run(
    ["node", str(ROOT / "render-pdf.js"), str(out / "index.html"), str(out / PDF_NAME)],
    check=True,
    env={**os.environ, "PLAYWRIGHT_CORE": os.environ.get("PLAYWRIGHT_CORE", PLAYWRIGHT_CORE)},
)
print("built", out / "index.html", "and", out / PDF_NAME)
