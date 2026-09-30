"""build_docx.py: the manuscript and the Supplementary Material as .docx, from the same Markdown the
LaTeX build uses, formatted for Natural Hazards (Springer).

Springer's submission guidelines for Natural Hazards (read 2026-09-29) ask for: a title page with
authors, affiliations (institution, department, city, country) and the corresponding author's e-mail;
an abstract of 150 to 250 words; 4 to 6 keywords; name-year citations; a reference list in Springer's
basic style with DOIs as full links; and, before the reference list, Acknowledgements and a section
headed "Statements and Declarations" (funding, competing interests, author contributions, data and
code availability, ethics). The document is A4, 2.5 cm margins, Times New Roman
12 pt, double spaced, with continuous line numbers and page numbers.

Order: title page, abstract, keywords, sections 1-6, Acknowledgements, Statements and Declarations
(07_declarations.md), references, figure captions. Figures are separate files.

Drafting notes (Markdown blockquotes) are not allowed in the sources any more: the build fails on
one, and on any "NEEDS AUTHOR INPUT" marker. Display equations are numbered in order of appearance,
(1), (2), ... in the manuscript and (S1), (S2), ... in the supplement; "[#eq:x]" becomes "Eq. (n)",
and a supplement reference to a manuscript equation reads "Eq. (n) of the main text".

The same sources also build the Fire (MDPI) package: `--journal fire` runs journal_fire.py, which
reuses the helpers here and writes to paper/submission_fire/. Journal differences live only in the
build profiles; the Markdown, figures, supplement source and REFERENCES.bib are shared.

Usage (needs pandoc; pypandoc_binary and python-docx supply it):
    python paper/tex/build_docx.py                   # Natural Hazards (default)
        -> paper/submission/manuscript.docx; paper/tex/supplementary_material.docx
    python paper/tex/build_docx.py --journal fire --template <fire-template.dot>
        -> paper/submission_fire/ (see journal_fire.py)
"""
import argparse, io, json, re, subprocess, sys, zipfile
from pathlib import Path

import pypandoc
from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm

HERE = Path(__file__).resolve().parent
P = HERE.parent
OUT = P / "submission"
FM = json.loads((P / "frontmatter.json").read_text(encoding="utf-8"))
BODY = ["01_introduction", "02_related_work", "03_methods", "04_results", "05_discussion",
        "06_conclusions"]
DECL = "07_declarations"
CSL = HERE / "springer-basic-author-date.csl"
A4_W, A4_H, MARGIN = 11906, 16838, 1418            # twips; 1418 twips = 2.5 cm
TEXT_WIDTH = A4_W - 2 * MARGIN


def clean(md, name):
    md = re.sub(r"<!--[\s\S]*?-->", "", md)
    assert "NEEDS AUTHOR INPUT" not in md, f"{name}: unresolved NEEDS AUTHOR INPUT marker"
    bq = [l for l in md.splitlines() if re.match(r"^\s*>", l)]
    assert not bq, f"{name}: blockquote in a manuscript source (drafting notes belong in paper/archive/): {bq[0][:80]}"
    lines = [l for l in md.splitlines() if not re.fullmatch(r"\s*(-{3,}|\*{3,}|_{3,})\s*", l)]
    return "\n".join(lines)


# "Chuvieco et al. [@Chuvieco2004]" would render as "Chuvieco et al. (Chuvieco et al. 2004)"; a narrative
# citation "@Chuvieco2004" renders as "Chuvieco et al. (2004)" (internal review F66)
NARRATIVE = re.compile(r"\b([A-Z][A-Za-z\-]+(?: and [A-Z][A-Za-z\-]+| et al\.)) \[@([A-Za-z0-9]+)\]")


def narrative(md):
    def fix(m):
        surname = m.group(1).split()[0].lower()
        assert m.group(2).lower().startswith(surname[:4]), (m.group(0), "name and key disagree")
        return f"@{m.group(2)}"
    return NARRATIVE.sub(fix, md)


def equations(md, eq, prefix="", external=None):
    """Number labelled display equations into `eq`; resolve [#eq:x] against `eq`, then `external`."""
    def block(m):
        eq[m.group(1)] = f"{prefix}{len(eq) + 1}"
        return f"$$\n{m.group(2).strip()} \\qquad ({eq[m.group(1)]})\n$$"
    md = re.sub(r"```math\s*\{#(eq:[\w-]+)\}\s*\n([\s\S]*?)\n```", block, md)
    md = re.sub(r"```math\s*\n([\s\S]*?)\n```", lambda m: f"$$\n{m.group(1).strip()}\n$$", md)

    def ref(m):
        l = m.group(1)
        if l in eq:
            return f"Eq. ({eq[l]})"
        assert external and l in external, f"equation reference without an equation: {l}"
        return f"Eq. ({external[l]}) of the main text"
    md = re.sub(r"\[#(eq:[\w-]+)\]", ref, md)
    return re.sub(r"\$`([^`]+)`\$", r"$\1$", md)                   # GitLab inline math


# Acknowledgements text, shared by both journal profiles
ACK = ("# Acknowledgements\n\nThe authors thank the Department of Computer Engineering at Çukurova "
       "University for the laboratory environment in which this work was carried out.")


def captions():
    tex = "\n".join(l for l in (P / "figure_captions.tex").read_text(encoding="utf-8").splitlines()
                    if not l.lstrip().startswith("%"))
    out, i = [], 0
    while (i := tex.find("\\caption{", i)) >= 0:
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
    return [pypandoc.convert_text(refs(c), "markdown", format="latex", extra_args=["--wrap=none"]).strip()
            for c in out]


# ---------------------------------------------------------------- Word
def _fonts(rpr, name):
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts"); rpr.append(fonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(a), name)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):   # theme fonts override
        if fonts.get(qn(a)) is not None:
            del fonts.attrib[qn(a)]


def reference_doc(path):
    path.write_bytes(subprocess.run([pypandoc.get_pandoc_path(), "--print-default-data-file", "reference.docx"],
                                    capture_output=True, check=True).stdout)
    d = Document(path)
    for s in d.styles:
        try:
            f = s.font
        except AttributeError:
            continue
        if f is None:
            continue
        f.name = "Times New Roman"
        _fonts(s.element.get_or_add_rPr(), "Times New Roman")
    names = [s.name for s in d.styles]
    for name in ("Normal", "Body Text", "First Paragraph", "Compact", "Bibliography", "Abstract"):
        if name in names:
            d.styles[name].font.size = Pt(12)
            d.styles[name].paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    for name, size in (("Title", 16), ("Subtitle", 13), ("Heading 1", 14), ("Heading 2", 12), ("Heading 3", 12)):
        if name in names:
            d.styles[name].font.size = Pt(size)
            d.styles[name].font.bold = True
            d.styles[name].font.color.rgb = None
    if "Verbatim Char" in names:                                    # code spans read as code, not as a glitch
        d.styles["Verbatim Char"].font.size = Pt(10.5)
        _fonts(d.styles["Verbatim Char"].element.get_or_add_rPr(), "Consolas")
    # the theme's major/minor fonts (Aptos) must not reach headings through theme references
    for el in d.styles.element.iter(qn("w:rFonts")):
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            if el.get(qn(a)) is not None:
                del el.attrib[qn(a)]
    sect = d.sections[0]
    sect.page_width, sect.page_height = Cm(21.0), Cm(29.7)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sect, side, Cm(2.5))
    ln = OxmlElement("w:lnNumType")
    ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous")
    sect._sectPr.append(ln)
    fp = sect.footer.paragraphs[0] if sect.footer.paragraphs else sect.footer.add_paragraph()
    fp.alignment = 1
    r = fp.add_run()
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), kind); r._r.append(e)
        else:
            e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = text; r._r.append(e)
    d.save(path)


def strip_custom_props(path):
    """pandoc records the local bibliography and CSL paths in docProps/custom.xml; drop the part
    (added 2026-09-30: the paths named the build machine's user directory). Zip entries get a fixed
    timestamp, so that a rebuild from the same sources reproduces the file byte for byte."""
    buf = io.BytesIO()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/custom.xml":
                continue
            if item.filename == "_rels/.rels":
                data = re.sub(rb'<Relationship [^>]*Target="docProps/custom.xml"[^>]*/>', b"", data)
            if item.filename == "[Content_Types].xml":
                data = re.sub(rb'<Override [^>]*PartName="/docProps/custom.xml"[^>]*/>', b"", data)
            fixed = zipfile.ZipInfo(item.filename, date_time=(1980, 1, 1, 0, 0, 0))
            fixed.compress_type, fixed.external_attr = zipfile.ZIP_DEFLATED, item.external_attr
            zout.writestr(fixed, data)
    path.write_bytes(buf.getvalue())


def to_docx(md, out, title):
    ref = OUT / "_reference.docx"
    reference_doc(ref)
    pypandoc.convert_text(
        md, "docx", format="markdown+tex_math_dollars+pipe_tables+footnotes+superscript",
        outputfile=str(out),
        extra_args=["--citeproc", f"--bibliography={P / 'REFERENCES.bib'}", f"--csl={CSL}",
                    f"--reference-doc={ref}", "--resource-path=" + str(P), "--columns=1000"])
    ref.unlink()
    d = Document(out)
    # pandoc writes an equal-width grid; size each column by its longest cell, so no renderer wraps a
    # short interval such as [+0.060, +0.073] across two lines
    for t in d.tables:
        need = [max(max(len(c.text.strip()) for c in col.cells), 4) for col in t.columns]
        widths = [round(TEXT_WIDTH * n / sum(need)) for n in need]
        for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
            gc.set(qn("w:w"), str(w))
        for row in t.rows:
            for c, w in zip(row.cells, widths):
                tcpr = c._tc.get_or_add_tcPr()
                tcw = tcpr.find(qn("w:tcW"))
                if tcw is None:
                    tcw = OxmlElement("w:tcW"); tcpr.append(tcw)
                tcw.set(qn("w:type"), "dxa"); tcw.set(qn("w:w"), str(w))
        # tables single-spaced at 10 pt, rows kept whole, so they do not sprawl over pages
        for row in t.rows:
            trpr = row._tr.get_or_add_trPr()
            if trpr.find(qn("w:cantSplit")) is None:
                trpr.append(OxmlElement("w:cantSplit"))
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                    p.paragraph_format.space_after = Pt(1)
                    for run in p.runs:
                        run.font.size = Pt(10)
        # keep a table's caption on the same page as the table (internal review, render check)
        prev = t._tbl.getprevious()
        while prev is not None and prev.tag == qn("w:p") and not "".join(prev.itertext()).strip():
            prev = prev.getprevious()
        if prev is not None and prev.tag == qn("w:p"):
            ppr = prev.find(qn("w:pPr"))
            if ppr is None:
                ppr = OxmlElement("w:pPr"); prev.insert(0, ppr)
            if ppr.find(qn("w:keepNext")) is None:
                ppr.append(OxmlElement("w:keepNext"))
    # document properties: no local paths, no template statistics (internal review F103)
    cp = d.core_properties
    cp.title, cp.author, cp.last_modified_by = title, "Emrehan Metin; Yunus Emre Cogurcu", ""
    cp.comments = cp.keywords = cp.subject = cp.category = cp.identifier = ""
    cp.revision = 1
    d.save(out)
    strip_custom_props(out)
    return Document(out)


def main_text_words(doc):
    """Words of Sections 1-6 as Word holds them: from the '1 Introduction' heading to the References
    heading, table cells excluded (tables are not paragraphs); figure captions, references and
    declarations lie outside the range. Table captions and table notes, which are paragraphs, count."""
    n, on = 0, False
    for p in doc.paragraphs:
        if p.style.name.startswith("Heading 1"):
            if p.text.startswith("1 "):
                on = True
            elif p.text in ("Acknowledgements", "Statements and Declarations", "References"):
                break
        if on:
            n += len(p.text.split())
    return n


def build_nh():
    # ---------------------------------------------------------------- manuscript
    OUT.mkdir(exist_ok=True)
    EQ = {}
    body = equations(narrative("\n\n".join(clean((P / f"{f}.md").read_text(encoding="utf-8"), f) for f in BODY)), EQ)
    body = re.sub(r"(?m)^# (\d+)\. ", r"# \1 ", body)                # keep the section numbers as text
    decl = narrative(clean((P / f"{DECL}.md").read_text(encoding="utf-8"), DECL))
    abstract = re.sub(r"(?m)^# Abstract\s*$", "", clean((P / "00_abstract.md").read_text(encoding="utf-8"), "abstract")).strip()
    n_abs = len(abstract.split())
    assert 150 <= n_abs <= 250, f"abstract has {n_abs} words; Natural Hazards asks for 150 to 250"
    assert 4 <= len(FM["keywords"]) <= 6, "Natural Hazards asks for 4 to 6 keywords"
    title_page = f"""---
title: "{FM['title']}"
lang: en-GB
---

Emrehan Metin^1^, Yunus Emre Cogurcu^1,\\*^

^1^ Department of Computer Engineering, Faculty of Engineering, Çukurova University, 01330 Sarıçam,
Adana, Türkiye

^\\*^ Corresponding author: Yunus Emre Cogurcu, ycogurcu@cu.edu.tr

ORCID: Yunus Emre Cogurcu, 0000-0002-9229-9657

@@WORDCOUNT@@

# Abstract

{abstract}

**Keywords:** {'; '.join(FM['keywords'])}
"""


    caps = captions()
    # figures must be cited in numerical order (Springer; internal review F21)
    _first = [re.search(rf"Fig\. {n}\b", body) for n in range(1, len(caps) + 1)]
    assert all(_first), [n + 1 for n, m in enumerate(_first) if not m]
    _pos = [m.start() for m in _first]
    assert _pos == sorted(_pos), f"figures first cited out of order: {_pos}"
    fig_md = "# Figure captions\n\n" + "\n\n".join(f"**Fig. {n}** {c}" for n, c in enumerate(caps, 1))
    ms_md = (title_page + "\n\n" + body + "\n\n" + ACK + "\n\n" + decl
             + "\n\n# References\n\n::: {#refs}\n:::\n\n" + fig_md + "\n")

    # ---------------------------------------------------------------- supplement
    SEQ = {}
    sup = clean((P / "supplementary.md").read_text(encoding="utf-8"), "supplementary")
    sup = equations(narrative(sup), SEQ, prefix="S", external=EQ)
    sup = re.sub(r"\A# Supplementary Material\s*\n", "", sup)
    sup_md = (f'---\ntitle: "Supplementary Material"\nsubtitle: "{FM["title"]}"\nlang: en-GB\n---\n\n' + sup
              + "\n\n# References\n\n::: {#refs}\n:::\n")


    TITLE = FM["title"]
    ms_doc = to_docx(ms_md.replace("@@WORDCOUNT@@\n", ""), OUT / "manuscript.docx", TITLE)
    WORDS = main_text_words(ms_doc)
    WORDLINE = (f"**Word count:** {WORDS:,} words in the main text (Sections 1 to 6, table captions and notes "
                "included; tables, references, declarations and figure captions excluded). Abstract "
                f"{n_abs} words.")
    ms_md = ms_md.replace("@@WORDCOUNT@@", WORDLINE)
    (HERE / "manuscript_assembled.md").write_text(ms_md, encoding="utf-8")   # build record, not submitted
    ms_doc = to_docx(ms_md, OUT / "manuscript.docx", TITLE)
    assert main_text_words(ms_doc) == WORDS
    sup_doc = to_docx(sup_md, OUT / "supplementary_material.docx", "Supplementary Material: " + TITLE)

    for name, doc, eqs in (("manuscript.docx", ms_doc, EQ), ("supplementary_material.docx", sup_doc, SEQ)):
        print(f"{name}: {len(doc.paragraphs)} paragraphs, {len(doc.tables)} tables, {len(eqs)} numbered equations")
    print(WORDLINE.replace("**", ""))
    print(f"{len(caps)} figure captions")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the submission .docx files for one journal.")
    ap.add_argument("--journal", choices=["nh", "fire"], default="nh",
                    help="nh: Natural Hazards -> paper/submission/; fire: Fire (MDPI) -> paper/submission_fire/")
    ap.add_argument("--template", type=Path, help="fire only: the MDPI Fire Word template (.dot, .dotx or .docx)")
    ap.add_argument("--no-pdf", action="store_true", help="fire only: skip the Word PDF export of the supplement")
    args = ap.parse_args()
    if args.journal == "nh":
        build_nh()
    else:
        import journal_fire
        journal_fire.build(args.template, pdf=not args.no_pdf)
