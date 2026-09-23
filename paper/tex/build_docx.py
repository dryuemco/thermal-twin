"""build_docx.py: the manuscript as .docx, from the same Markdown the LaTeX build uses.

Ecological Informatics has no Word template of its own (Elsevier's "Your Paper Your Way"), so the
document follows Elsevier's general manuscript conventions: Times New Roman 12 pt, double spacing,
continuous line numbers, page numbers, title page, abstract, keywords, body, declarations, references
(Elsevier Harvard, via pandoc citeproc) and figure captions. Figures, the graphical abstract, the
highlights and the Supplementary Material are submitted as separate files and are not embedded.

Drafting notes (Markdown blockquotes) and HTML comments are dropped, as in build_tex.mjs. Display
equations are numbered in order of appearance and "[#eq:x]" becomes "Eq. (n)".

Usage (needs pandoc; pypandoc_binary and python-docx supply it):
    python paper/tex/build_docx.py            -> paper/submission/manuscript.docx
"""
import json, re, subprocess, sys
from pathlib import Path

import pypandoc
from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

HERE = Path(__file__).resolve().parent
P = HERE.parent
OUT = P / "submission"
OUT.mkdir(exist_ok=True)
FM = json.loads((P / "frontmatter.json").read_text(encoding="utf-8"))
BODY = ["01_introduction", "02_related_work", "03_methods", "04_results", "05_discussion",
        "06_conclusions", "07_declarations"]


def clean(md):
    md = re.sub(r"<!--[\s\S]*?-->", "", md)
    lines = [l for l in md.splitlines() if not re.match(r"^\s*>", l)]
    lines = [l for l in lines if not re.fullmatch(r"\s*(-{3,}|\*{3,}|_{3,})\s*", l)]
    return "\n".join(lines)


# ---- body, with numbered equations
body = "\n\n".join(clean((P / f"{f}.md").read_text(encoding="utf-8")) for f in BODY)
EQ = {}


def eq_block(m):
    label, tex = m.group(1), m.group(2).strip()
    EQ[label] = len(EQ) + 1
    return f"$$\n{tex} \\qquad ({EQ[label]})\n$$"


body = re.sub(r"```math\s*\{#(eq:[\w-]+)\}\s*\n([\s\S]*?)\n```", eq_block, body)
body = re.sub(r"```math\s*\n([\s\S]*?)\n```", lambda m: f"$$\n{m.group(1).strip()}\n$$", body)
missing = [l for l in re.findall(r"\[#(eq:[\w-]+)\]", body) if l not in EQ]
assert not missing, f"equation references without an equation: {missing}"
body = re.sub(r"\[#(eq:[\w-]+)\]", lambda m: f"Eq. ({EQ[m.group(1)]})", body)
body = re.sub(r"\$`([^`]+)`\$", r"$\1$", body)                      # GitLab inline math
# the "# 1. Introduction" style headings: keep the author's numbers as text
body = re.sub(r"(?m)^# (\d+)\. ", r"# \1 ", body)

# ---- title page, abstract, keywords
abstract = clean((P / "00_abstract.md").read_text(encoding="utf-8"))
abstract = re.sub(r"(?m)^# Abstract\s*$", "", abstract).strip()
title_page = f"""---
title: "{FM['title']}"
lang: en-GB
---

Emrehan Metin^a^, Yunus Emre Cogurcu^a,\\*^

^a^ Çukurova University, Adana, Türkiye

^\\*^ Corresponding author. E-mail: ycogurcu@cu.edu.tr

# Abstract

{abstract}

**Keywords:** {'; '.join(FM['keywords'])}
"""


# ---- figure captions, from figure_captions.tex (LaTeX -> Markdown through pandoc)
def captions():
    tex = "\n".join(l for l in (P / "figure_captions.tex").read_text(encoding="utf-8").splitlines()
                    if not l.lstrip().startswith("%"))
    out, i = [], 0
    while True:
        i = tex.find("\\caption{", i)
        if i < 0:
            break
        j, depth = i + len("\\caption{"), 1
        while depth:
            depth += {"{": 1, "}": -1}.get(tex[j], 0)
            j += 1
        out.append(tex[i + len("\\caption{"):j - 1])
        i = j
    labels = re.findall(r"\\label\{(fig:[^}]+)\}", tex)
    def refs(c):
        c = re.sub(r"\\ref\{fig:([^}]+)\}", lambda m: str(labels.index("fig:" + m.group(1)) + 1), c)
        return re.sub(r"\\ref\{(?:sec|tab):([^}]+)\}", r"\1", c)
    out = [refs(c) for c in out]
    return [pypandoc.convert_text(c, "markdown", format="latex", extra_args=["--wrap=none"]).strip() for c in out]


caps = captions()
fig_md = "# Figure captions\n\n" + "\n\n".join(f"**Fig. {n}.** {c}" for n, c in enumerate(caps, 1))

doc_md = title_page + "\n\n" + body + "\n\n# References\n\n::: {#refs}\n:::\n\n" + fig_md + "\n"
(OUT / "manuscript_assembled.md").write_text(doc_md, encoding="utf-8")

# ---- reference document: Elsevier's general conventions
ref = OUT / "_reference.docx"
ref.write_bytes(subprocess.run([pypandoc.get_pandoc_path(), "--print-default-data-file", "reference.docx"],
                               capture_output=True, check=True).stdout)
d = Document(ref)
for s in d.styles:
    try:
        f = s.font
    except AttributeError:
        continue
    if f is not None:
        f.name = "Times New Roman"
        rpr = s.element.get_or_add_rPr()
        fonts = rpr.find(qn("w:rFonts"))
        fonts = fonts if fonts is not None else OxmlElement("w:rFonts")
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            fonts.set(qn(a), "Times New Roman")
        if fonts.getparent() is None:
            rpr.append(fonts)
for name in ("Normal", "Body Text", "First Paragraph", "Compact", "Bibliography", "Abstract"):
    if name in [s.name for s in d.styles]:
        st = d.styles[name]
        st.font.size = Pt(12)
        st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
for name, size in (("Title", 16), ("Heading 1", 14), ("Heading 2", 12), ("Heading 3", 12)):
    if name in [s.name for s in d.styles]:
        d.styles[name].font.size = Pt(size)
        d.styles[name].font.bold = True
        d.styles[name].font.color.rgb = None
sect = d.sections[0]
ln = OxmlElement("w:lnNumType")
ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous")
sect._sectPr.append(ln)
# page number, centred in the footer
fp = sect.footer.paragraphs[0] if sect.footer.paragraphs else sect.footer.add_paragraph()
fp.alignment = 1
r = fp.add_run()
for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
    if kind:
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), kind); r._r.append(e)
    else:
        e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = text; r._r.append(e)
d.save(ref)

pypandoc.convert_text(
    doc_md, "docx", format="markdown+tex_math_dollars+pipe_tables+footnotes+superscript",
    outputfile=str(OUT / "manuscript.docx"),
    extra_args=["--citeproc", f"--bibliography={P / 'REFERENCES.bib'}", f"--csl={HERE / 'elsevier-harvard.csl'}",
                f"--reference-doc={ref}", "--resource-path=" + str(P),
                # no relative column widths: a pipe table narrower than this is autofitted by Word,
                # instead of taking equal widths from its dash separators (which wrapped Table 1's CIs)
                "--columns=1000"])
ref.unlink()

# ---- column widths from content. pandoc writes an equal-width grid as a hint; set each column in
# proportion to its longest cell so no renderer wraps a short interval such as [+0.060, +0.073].
TEXT_WIDTH = 9360                                     # twips: Letter, 1 inch margins (pandoc's default page)
d = Document(OUT / "manuscript.docx")
for t in d.tables:
    ncol = len(t.columns)
    need = [max(max(len(c.text.strip()) for c in col.cells), 4) for col in t.columns]
    widths = [round(TEXT_WIDTH * n / sum(need)) for n in need]
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(w))
    for row in t.rows:
        for c, w in zip(row.cells, widths):
            tcpr = c._tc.get_or_add_tcPr()
            tcw = tcpr.find(qn("w:tcW"))
            if tcw is None:
                tcw = OxmlElement("w:tcW"); tcpr.append(tcw)
            tcw.set(qn("w:type"), "dxa"); tcw.set(qn("w:w"), str(w))
d.save(OUT / "manuscript.docx")

# ---- report: tables as Word will hold them
d = Document(OUT / "manuscript.docx")
print(f"manuscript.docx: {len(d.paragraphs)} paragraphs, {len(d.tables)} tables, {len(EQ)} numbered equations, "
      f"{len(caps)} figure captions")
for k, t in enumerate(d.tables, 1):
    print(f"  table {k}: {len(t.rows)} rows x {len(t.columns)} columns")
