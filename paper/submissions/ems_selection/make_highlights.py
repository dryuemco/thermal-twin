"""make_highlights.py: writes highlights.docx (the separate highlights file Elsevier asks for) from the highlights
environment of manuscript.tex, with the value macros expanded, and checks the 85-character limit.

Run:  python make_highlights.py   (needs python-docx)
"""
import re
from pathlib import Path

import docx

HERE = Path(__file__).resolve().parent
macros = {}
for f in ("values_frozen.tex", "values.tex"):
    macros.update(re.findall(r"\\newcommand\{\\(\w+)\}\{(.*?)\}\s*$", (HERE / f).read_text(encoding="utf-8"), re.M))


def expand(s):
    s = re.sub(r"\\(\w+)\{\}", lambda m: macros[m.group(1)], s)
    s = re.sub(r"\\(\w+)", lambda m: macros[m.group(1)], s)
    return s


t = (HERE / "manuscript.tex").read_text(encoding="utf-8")
block = re.search(r"\\begin\{highlights\}(.*?)\\end\{highlights\}", t, re.S).group(1)
items = [expand(s.strip()) for s in re.findall(r"\\item (.+)", block)]
assert 3 <= len(items) <= 5
d = docx.Document()
d.add_paragraph("Highlights")
for i in items:
    assert len(i) <= 85, (len(i), i)
    d.add_paragraph(i, style="List Bullet")
d.save(HERE / "highlights.docx")
for i in items:
    print(len(i), i)
