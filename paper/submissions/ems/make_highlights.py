"""make_highlights.py: writes highlights.docx (the separate highlights file Elsevier asks for) from the
highlights environment of manuscript.tex, and checks the 85-character limit.

Run:  python make_highlights.py   (needs python-docx)
"""
import re
from pathlib import Path

import docx

HERE = Path(__file__).resolve().parent
t = (HERE / "manuscript.tex").read_text(encoding="utf-8")
block = re.search(r"\\begin\{highlights\}(.*?)\\end\{highlights\}", t, re.S).group(1)
items = [s.strip() for s in re.findall(r"\\item (.+)", block)]
d = docx.Document()
d.add_paragraph("Highlights")
for i in items:
    assert len(i) <= 85, (len(i), i)
    d.add_paragraph(i, style="List Bullet")
d.save(HERE / "highlights.docx")
print([len(i) for i in items])
