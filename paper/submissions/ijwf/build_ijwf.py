#!/usr/bin/env python3
"""build_ijwf.py: the IJWF manuscript and its supplement, built from submissions/ijwf/text/.

Run with an interpreter that has pypandoc and python-docx (the project's scratch/venv_docx has both):
    python paper/submissions/ijwf/build_ijwf.py            # .docx and .pdf (the PDF needs MS Word)
    python paper/submissions/ijwf/build_ijwf.py --no-pdf

Output, in submissions/ijwf/:
    manuscript.docx                 in the CSIRO Publishing Word template (its styles, page setup, line
                                    numbers and footer), figures and tables placed after their first citation
    manuscript.pdf                  Word export, for reading
    supplementary_material.docx     separate file, no line numbers, its own reference list
    supplementary_material.pdf
    figures/Fig1.pdf ... Fig8.pdf   the vector figures for upload (the IJWF redraws in figures/)

Nothing outside submissions/ijwf/ is written. The figures are the IJWF copies in figures/.
The build stops on an unresolved citation, a missing figure or table, an abstract over 200 words or a
main text over 6000 words as Word holds it.
"""
import io
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pypandoc
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
TEXT = HERE / "text"
TEMPLATE = HERE / "template" / "CSIROP_generic_template.docx"
PAPER = HERE.parents[1]
SHARED_FIGS = PAPER / "figures"
OWN_FIGS = HERE / "figures"
CSL = HERE / "csiro-harvard.csl"
BIB = TEXT / "REFERENCES.bib"
BODY = ["01_introduction", "03_methods", "04_results", "05_discussion", "06_conclusions"]
LIMIT, ABSTRACT_LIMIT = 6000, 200
FM = json.loads((TEXT / "frontmatter.json").read_text(encoding="utf-8"))["ijwf"]
TITLE = FM["title"]
AUTHORS = ["Emrehan Metin", "Yunus Emre Cogurcu"]
CORRESPONDING = ("Yunus Emre Cogurcu", "ycogurcu@cu.edu.tr")
AFFILIATION = ("Department of Computer Engineering, Faculty of Engineering, Çukurova University, "
               "01330 Sarıçam, Adana, Türkiye")
FOOTER_NAME = "Metin and Cogurcu"
FIG_STEMS = {1: OWN_FIGS / "fig1_study_map", 2: OWN_FIGS / "fig2_schematic",
             3: OWN_FIGS / "fig3_within_robustness", 4: OWN_FIGS / "fig4_transfer_matrix",
             5: OWN_FIGS / "fig5_adaptation", 6: OWN_FIGS / "fig6_loro",
             7: OWN_FIGS / "fig7_feature_drop", 8: OWN_FIGS / "fig8_contrast_pairs"}   # the IJWF redraws (8 and 7 pt)
FIG_WIDTH_CM = 16.5
# heading in 07_declarations.md -> paragraph style of the template, in the template's order
STATEMENTS = [("Data availability", "Data statement"), ("Conflicts of interest", "Conflicts statement"),
              ("Declaration of funding", "Funding statement"), ("Author contributions", "Other statements"),
              ("Declaration of use of AI", "Other statements"), ("Ethics statement", "Other statements"),
              ("Acknowledgements", "Other statements")]
NARRATIVE = re.compile(r"\b([A-Z][A-Za-z\-]+(?: and [A-Z][A-Za-z\-]+| et al\.)) \[@([A-Za-z0-9]+)\]")
MD_FORMAT = "markdown+tex_math_dollars+pipe_tables+superscript+fenced_divs-subscript"


# ---------------------------------------------------------------- sources
def read(name, ext=".md"):
    return re.sub(r"<!--[\s\S]*?-->", "", (TEXT / f"{name}{ext}").read_text(encoding="utf-8"))


def words(s):
    return len(re.sub(r"[*_`#|]", " ", s).split())


def narrative(md):
    """'Lobo et al. [@Lobo2008]' -> '@Lobo2008', which pandoc prints as 'Lobo et al. (2008)'."""
    def fix(m):
        assert m.group(2).lower().startswith(m.group(1).split()[0].lower()[:4]), m.group(0)
        return f"@{m.group(2)}"
    return NARRATIVE.sub(fix, md)


def styled(style, text):
    return f'::: {{custom-style="{style}"}}\n{text.strip()}\n:::\n'


def headings(md):
    md = re.sub(r"(?m)^# (.+)$", lambda m: styled("Heading1", m.group(1)), md)
    return re.sub(r"(?m)^## (.+)$", lambda m: styled("Heading2", m.group(1)), md)


TABLE = re.compile(r"\*\*Table (\d+)\. (.+?)\.\*\*[ \n]*(.*?)\n\n((?:\|[^\n]*\n?)+)"
                   r"(?:\n\*Table note\.\* (.*?)(?=\n\n|\Z))?", re.S)


def tables(body):
    """The title goes above the table in the template's TableHead style, the legend and the note below it."""
    seen = []

    def fix(m):
        num, title, legend, table, note = m.groups()
        seen.append(int(num))
        below = " ".join(legend.split()) + (" " + " ".join(note.split()) if note else "")
        out = styled("TableHead", f"Table {num}. {title}.") + "\n" + table.rstrip() + "\n\n"
        return out + (styled("TableFootnote", below) if below.strip() else "")
    body = TABLE.sub(fix, body)
    assert seen == list(range(1, len(seen) + 1)) and len(seen) == 4, f"tables found: {seen}"
    return body, len(seen)


def captions():
    tex = "\n".join(l for l in (TEXT / "figure_captions.tex").read_text(encoding="utf-8").splitlines()
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
    caps = [pypandoc.convert_text(refs(c), "markdown", format="latex", extra_args=["--wrap=none"]).strip()
            for c in out]
    assert len(caps) == len(FIG_STEMS), f"{len(caps)} captions for {len(FIG_STEMS)} figures"
    return caps


def first_cite_end(body, n):
    """End offset of the prose paragraph that first cites Fig. n (headings, tables and styled blocks skipped)."""
    for m in re.finditer(rf"(?<!Supplementary )\bFigs?\. (?:\d+[a-z]?(?:, | and | to ))*{n}(?!\d)", body):
        start = body.rfind("\n\n", 0, m.start()) + 2
        if body[start:m.start()].lstrip().startswith(("|", "#", "![", ":::")):
            continue
        end = body.find("\n\n", m.end())
        return len(body) if end < 0 else end
    raise AssertionError(f"Fig. {n} is not cited in the body prose")


def insert_figures(body, caps):
    ends = sorted((first_cite_end(body, n), n) for n in FIG_STEMS)
    assert [n for _, n in ends] == sorted(FIG_STEMS), f"figures first cited out of order: {[n for _, n in ends]}"
    out, last = [], 0
    for end, n in ends:
        png = FIG_STEMS[n].with_name(FIG_STEMS[n].name + "_preview.png")
        pdf = FIG_STEMS[n].with_suffix(".pdf")
        assert png.exists() and pdf.exists(), f"figure {n}: {png.name} or {pdf.name} is missing"
        shutil.copyfile(pdf, OWN_FIGS / f"Fig{n}.pdf")
        out += [body[last:end], f"\n\n![]({png.as_posix()}){{width={FIG_WIDTH_CM}cm}}\n\n",
                styled("FigCap", f"**Fig. {n}.** {caps[n - 1]}")]
        last = end
    return "".join(out) + body[last:]


def statements():
    src = read("07_declarations")
    parts = dict(re.findall(r"(?ms)^## (.+?)\n(.*?)(?=^## |\Z)", src))
    assert set(parts) == {h for h, _ in STATEMENTS}, sorted(parts)
    return "\n".join(styled(style, head) + "\n" + narrative(parts[head]).strip() + "\n" for head, style in STATEMENTS)


def front():
    src = read("00_abstract_ijwf")
    abstract, summary = src.split("# Online summary")
    abstract = abstract.replace("# Abstract", "").strip()
    summary = " ".join(summary.split())
    n_abs, n_sum = words(abstract), words(summary)
    assert n_abs <= ABSTRACT_LIMIT, f"abstract has {n_abs} words with its headings; the limit is {ABSTRACT_LIMIT}"
    assert 50 <= n_sum <= 80, f"online summary has {n_sum} words; the template asks for 50 to 80"
    assert "@" not in abstract, "citation in the abstract"
    kw = FM["keywords"]
    assert len(kw) >= 8, f"{len(kw)} keywords; the template asks for at least eight"
    names = " and ".join(f"{a}^A{',\\*' if a == CORRESPONDING[0] else ''}^" for a in AUTHORS)
    md = [styled("Arttitle", TITLE), styled("Author", names), styled("Address", f"^A^{AFFILIATION}"),
          styled("Corresponding author", f"^\\*^Corresponding author. Email: {CORRESPONDING[1]}"),
          styled("AbsHeading", "Abstract")]
    md += [styled("Abspara", p) for p in re.split(r"\n\s*\n", abstract)]
    md += [styled("Keywords", "**Keywords:** " + ", ".join(kw)),
           styled("TOCAbstract", "**Online summary text.** " + summary)]
    return "\n".join(md), n_abs, n_sum


# ---------------------------------------------------------------- Word
def strip_custom_props(path):
    """pandoc records the local bibliography and CSL paths in docProps/custom.xml; drop that part."""
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
            zout.writestr(item, data)
    path.write_bytes(buf.getvalue())


def _set_style(p, sid):
    ppr = p.find(qn("w:pPr"))
    if ppr is None:
        ppr = OxmlElement("w:pPr")
        p.insert(0, ppr)
    ps = ppr.find(qn("w:pStyle"))
    if ps is None:
        ps = OxmlElement("w:pStyle")
        ppr.insert(0, ps)
    ps.set(qn("w:val"), sid)
    return ppr


def _style_id(p):
    ps = p.find(f"{qn('w:pPr')}/{qn('w:pStyle')}")
    return ps.get(qn("w:val")) if ps is not None else None


def fit_tables(d, text_width, size_pt=None):
    """Column widths by the longest cell, rows kept whole, the title kept with its table."""
    for t in d.tables:
        need = [max(max(len(c.text.strip()) for c in col.cells), 4) for col in t.columns]
        widths = [round(text_width * n / sum(need)) for n in need]
        for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
            gc.set(qn("w:w"), str(w))
        for row in t.rows:
            trpr = row._tr.get_or_add_trPr()
            if trpr.find(qn("w:cantSplit")) is None:
                trpr.append(OxmlElement("w:cantSplit"))
            for c, w in zip(row.cells, widths):
                tcpr = c._tc.get_or_add_tcPr()
                tcw = tcpr.find(qn("w:tcW"))
                if tcw is None:
                    tcw = OxmlElement("w:tcW")
                    tcpr.append(tcw)
                tcw.set(qn("w:type"), "dxa")
                tcw.set(qn("w:w"), str(w))
                if size_pt:
                    for p in c.paragraphs:
                        p.paragraph_format.space_after = Pt(1)
                        for run in p.runs:
                            run.font.size = Pt(size_pt)
        prev = t._tbl.getprevious()
        if prev is not None and prev.tag == qn("w:p"):
            ppr = prev.find(qn("w:pPr"))
            if ppr is None:
                ppr = OxmlElement("w:pPr")
                prev.insert(0, ppr)
            if ppr.find(qn("w:keepNext")) is None:
                ppr.append(OxmlElement("w:keepNext"))


def template_styles(path):
    """Put every paragraph into a style of the CSIRO template and fill in the footer."""
    d = Document(path)
    have = {s.style_id for s in d.styles}
    generic = {None, "Normal", "BodyText", "FirstParagraph", "Compact"}
    for p in d.element.body.iter(qn("w:p")):
        sid = _style_id(p)
        cell = next((a for a in p.iterancestors() if a.tag == qn("w:tc")), None)
        if cell is not None:
            row = cell.getparent()
            first = row.getprevious() is None or row.getprevious().tag != qn("w:tr")
            _set_style(p, "TableColumnHead" if first else "TableText")
        elif sid == "Bibliography":
            _set_style(p, "Reference")
        elif sid in generic:
            ppr = _set_style(p, "Para")
            if p.find(f".//{qn('w:drawing')}") is not None:            # a figure: centred, kept with its caption
                for tag, val in (("w:keepNext", None), ("w:jc", "center")):
                    el = OxmlElement(tag)
                    if val:
                        el.set(qn("w:val"), val)
                    ppr.append(el)
        else:
            assert sid in have, f"paragraph style {sid} is not in the template"
    for t in d.tables:
        t.style = d.styles["Table Grid"]
    for s in d.sections:
        for foot in (s.footer, s.first_page_footer, s.even_page_footer):
            for t in foot._element.iter(qn("w:t")):
                if t.text:
                    t.text = t.text.replace("Lead author name", FOOTER_NAME).replace("Manuscript ID", "")
        if s._sectPr.find(qn("w:lnNumType")) is None:
            ln = OxmlElement("w:lnNumType")
            ln.set(qn("w:countBy"), "1")
            ln.set(qn("w:restart"), "continuous")
            s._sectPr.append(ln)
    sect = d.sections[0]
    fit_tables(d, sect.page_width - sect.left_margin - sect.right_margin and
               int((sect.page_width - sect.left_margin - sect.right_margin) / 635))
    cp = d.core_properties
    cp.title, cp.author, cp.last_modified_by = TITLE, "; ".join(AUTHORS), ""
    cp.comments = cp.keywords = cp.subject = cp.category = ""
    d.save(path)
    strip_custom_props(path)
    return Document(path)


def main_text_words(d):
    """Words from the Introduction heading to the first author statement as Word holds them: table cells,
    table titles and notes, figure captions and the figures themselves are not counted."""
    n, on = 0, False
    for p in d.paragraphs:
        sid, t = p.style.style_id, p.text.strip()
        if sid == "Heading10" and t == "Introduction":
            on = True
        elif sid == "Datastatement":
            break
        if on and sid not in ("TableHead", "TableFootnote", "FigCap"):
            n += len(t.split())
    assert on, "the Introduction heading was not found in the template's Heading1 style"
    return n


def word_pdf(docx, pdf):
    pdf.unlink(missing_ok=True)
    ps = (f"$ErrorActionPreference = 'Stop'; $w = New-Object -ComObject Word.Application; $w.Visible = $false; "
          f"try {{ $d = $w.Documents.Open('{docx}', $false, $true); $d.ExportAsFixedFormat('{pdf}', 17); "
          f"$d.Close($false) }} finally {{ $w.Quit() }}")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    assert pdf.exists() and pdf.stat().st_size > 0, pdf


def pandoc(md, out, reference):
    pypandoc.convert_text(md, "docx", format=MD_FORMAT, outputfile=str(out),
                          extra_args=["--citeproc", f"--bibliography={BIB}", f"--csl={CSL}",
                                      f"--reference-doc={reference}", f"--resource-path={PAPER}",
                                      "--columns=1000", "-M", "lang=en-AU"])


def check_text(d, what):
    text = "\n".join(p.text for p in d.element.body.iter(qn("w:p")) for p in [type("P", (), {"text": "".join(p.itertext())})])
    assert "???" not in text and not re.search(r"(?<![\w.])@[A-Za-z]", text), f"unresolved citation in {what}"
    return text


# ---------------------------------------------------------------- manuscript
def build_manuscript(pdf):
    front_md, n_abs, n_sum = front()
    body = narrative("\n\n".join(read(f) for f in BODY))
    assert "$" not in body and "```" not in body, "the main text is expected to hold no mathematics"
    body, n_tab = tables(body)
    body = headings(body)
    body = insert_figures(body, captions())
    back = (statements()
            + styled("Supplementary heading", "Supplementary material") + "\nSupplementary material is available online.\n\n"
            + styled("Reference head", "References") + "\n::: {#refs}\n:::\n")
    md = front_md + "\n\n" + body + "\n\n" + back
    for item in re.findall(r"Supplementary (?:Sections?|Tables?|Figs?\.?) S\d[\d.]*", md):
        pass                                                         # (the cross-reference targets are checked by check_text.py)
    out = HERE / "manuscript.docx"
    pandoc(md, out, TEMPLATE)
    d = template_styles(out)
    check_text(d, "the manuscript")
    n_fig = len(d.element.body.findall(f".//{qn('w:drawing')}"))
    assert n_fig == len(FIG_STEMS) and len(d.tables) == n_tab, f"{n_fig} figures and {len(d.tables)} tables in the .docx"
    n_words = main_text_words(d)
    n_ref = sum(p.style.style_id == "Reference" for p in d.paragraphs)
    assert n_words <= LIMIT, f"the main text has {n_words} words in Word; the limit is {LIMIT}"
    if pdf:
        word_pdf(out, HERE / "manuscript.pdf")
    print(f"manuscript.docx: abstract {n_abs} words, online summary {n_sum} words, {len(FM['keywords'])} keywords, "
          f"main text {n_words} words in Word (limit {LIMIT}), {n_fig} figures, {n_tab} tables, {n_ref} references")
    return n_words, n_ref


# ---------------------------------------------------------------- supplement
def equations(md, prefix="S"):
    eq = {}

    def block(m):
        eq[m.group(1)] = f"{prefix}{len(eq) + 1}"
        return f"$$\n{m.group(2).strip()} \\qquad ({eq[m.group(1)]})\n$$"
    md = re.sub(r"```math\s*\{#(eq:[\w-]+)\}\s*\n([\s\S]*?)\n```", block, md)
    md = re.sub(r"```math\s*\n([\s\S]*?)\n```", lambda m: f"$$\n{m.group(1).strip()}\n$$", md)
    md = re.sub(r"\[#(eq:[\w-]+)\]", lambda m: f"Eqn {eq[m.group(1)]}", md)
    return re.sub(r"\$`([^`]+)`\$", r"$\1$", md), len(eq)


def plain_reference(path):
    """pandoc's own reference document in Times New Roman 11 pt, A4, without line numbers."""
    path.write_bytes(subprocess.run([pypandoc.get_pandoc_path(), "--print-default-data-file", "reference.docx"],
                                    capture_output=True, check=True).stdout)
    d = Document(path)
    for s in d.styles:
        font = getattr(s, "font", None)
        if font is None:
            continue
        font.name = "Times New Roman"
        rpr = s.element.get_or_add_rPr()
        fonts = rpr.find(qn("w:rFonts"))
        if fonts is None:
            fonts = OxmlElement("w:rFonts")
            rpr.append(fonts)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            fonts.set(qn(a), "Times New Roman")
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            if fonts.get(qn(a)) is not None:
                del fonts.attrib[qn(a)]
        if s.name in ("Title", "Subtitle", "Heading 1", "Heading 2", "Heading 3"):
            font.color.rgb = None
    for name in ("Normal", "Body Text", "First Paragraph", "Compact", "Bibliography"):
        if name in [s.name for s in d.styles]:
            d.styles[name].font.size = Pt(11)
    sect = d.sections[0]
    sect.page_width, sect.page_height = Cm(21.0), Cm(29.7)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sect, side, Cm(2.2))
    d.save(path)


def build_supplement(pdf):
    src = read("supplementary")
    assert src.count(f"Supplementary material for *{TITLE}*.") == 1, "the supplement does not name the IJWF title"
    src = re.sub(r"\A\s*# Supplementary Material\s*\n", "", src)
    src, n_eq = equations(narrative(src))
    meta = (f'---\ntitle: "Supplementary material"\nsubtitle: "{TITLE}"\nauthor: "{" and ".join(AUTHORS)}"\n'
            f"lang: en-AU\n---\n\n")
    md = meta + src.strip() + "\n\n# References\n\n::: {#refs}\n:::\n"
    out = HERE / "supplementary_material.docx"
    ref = HERE / "_reference.docx"
    plain_reference(ref)
    pandoc(md, out, ref)
    ref.unlink()
    d = Document(out)
    sect = d.sections[0]
    fit_tables(d, int((sect.page_width - sect.left_margin - sect.right_margin) / 635), size_pt=8.5)
    cp = d.core_properties
    cp.title, cp.author, cp.last_modified_by = "Supplementary material: " + TITLE, "; ".join(AUTHORS), ""
    d.save(out)
    strip_custom_props(out)
    d = Document(out)
    check_text(d, "the supplement")
    n_fig = len(d.element.body.findall(f".//{qn('w:drawing')}"))
    assert n_fig == 5 and len(d.tables) == 17, f"{n_fig} figures and {len(d.tables)} tables in the supplement"
    if pdf:
        word_pdf(out, HERE / "supplementary_material.pdf")
    print(f"supplementary_material.docx: {n_fig} figures, {len(d.tables)} tables, {n_eq} numbered equations")


if __name__ == "__main__":
    make_pdf = "--no-pdf" not in sys.argv
    OWN_FIGS.mkdir(exist_ok=True)
    build_manuscript(make_pdf)
    build_supplement(make_pdf)
