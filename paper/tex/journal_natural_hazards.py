"""journal_natural_hazards.py: the Natural Hazards (Springer) build profile, `build_docx.py --journal nh`.

It replaces the September profile (build_nh in build_docx.py), which built the package now kept in
paper/submissions/natural_hazards/unsent_2026-09-29/ from the sources as they were before the Fire Ecology
restructuring. That package was never submitted. Natural Hazards became the target again on 2026-10-25,
after the Fire Ecology desk rejection.

One source, several profiles: the section Markdown (01, 03-07), figure_captions.tex, supplementary.md, the
figures and REFERENCES.bib are the ones the other builds read. Natural Hazards' own items are
00_abstract.md, the keywords at the top of frontmatter.json and the title under "natural_hazards";
everything else that differs lives here, as a transformation of the shared sources.

Natural Hazards' requirements, read 2026-10-25 from link.springer.com/journal/11069/submission-guidelines:
- a Word file with line numbers; a title page with the title, the authors, their affiliations, the
  corresponding author's e-mail and ORCID iDs; Acknowledgements in a separate section on the title page;
- an abstract of 150 to 250 words without undefined abbreviations or references; 4 to 6 keywords;
- decimal headings of at most three levels; name-year citations and the basic Springer reference style
  with DOIs as links;
- the use of a large language model beyond copy editing stated in the Methods section;
- "Statements and Declarations" after the References: funding, competing interests, author
  contributions and data availability (code availability and ethics added here);
- figures within the body of the text; captions start with "Fig." and the number in bold, with no
  punctuation after the number and none at the end of the caption; figure files named Fig1, Fig2, ...;
- supplementary material cited in the text as "Online Resource 1", the file named ESM_1, and the file
  giving the article title, the journal, the authors, and the corresponding author's affiliation and
  e-mail.

Output, paper/submissions/natural_hazards/:
    manuscript.docx          figures and tables embedded, references in the basic Springer style
    ESM_1.pdf                Online Resource 1: the Supplementary Material with its own reference list
    Fig1.pdf ... Fig8.pdf    the eight vector figures, as drawn and checked by paper/figures/
    cover_letter_draft.docx  unsigned draft, reviewers left out (they are not public)
    MANIFEST.md              file, size, SHA-256, source commit
  local only (gitignored): suggested_reviewers.md, and cover_letter.docx built from the draft with the
  reviewers from that file, for signing.

Checks run at build time (any failure stops the build): the abstract length, its abbreviations and the
keyword count; the five section headings; the statement on generative AI moved into Section 2.13; every
figure and table cited in body prose, first cited in numerical order and placed after its first
citation; Online Resource 1 cited; every citation resolved; every internal link has a target; every
decimal of the sources reaches the assembled Markdown, and the Markdown and the .docx hold the same
decimals.
"""
import datetime
import hashlib
import re
import shutil
import subprocess
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

import build_docx as B
import journal_fire as F
import journal_fire_ecology as J

HERE = Path(__file__).resolve().parent
P = B.P
ROOT = P.parent
OUT = P / "submissions" / "natural_hazards"
FIGS = P / "figures"
NH = B.FM["natural_hazards"]
JOURNAL = "Natural Hazards"
ESM = "Online Resource 1"
POINTER = ("Sections, figures and tables numbered with S (for example Section S1.2, Fig. S1 and Table S1) "
           f"are in {ESM}.")
HEADS = ["Introduction", "Methods", "Results", "Discussion", "Conclusions"]
CORRESPONDING_NAME = "Yunus Emre Cogurcu"


# ---------------------------------------------------------------- sources
def abstract():
    src = B.clean((P / "00_abstract.md").read_text(encoding="utf-8"), "abstract")
    text = re.sub(r"(?m)^# Abstract\s*$", "", src).strip()
    assert "@" not in text, "citation in the abstract"
    n = J.words(text)
    assert 150 <= n <= 250, f"abstract has {n} words; Natural Hazards asks for 150 to 250"
    defined = {part for d in re.findall(r"\(([A-Z]{2,}(?:-[A-Z]{2,})*)\)", text) for part in d.split("-")}
    undefined = set(re.findall(r"\b[A-Z]{2,}\b", text)) - defined
    assert not undefined, f"abbreviations not defined in the abstract: {sorted(undefined)}"
    return text, n


def move_genai(body, statement):
    """Springer asks for the use of a large language model to be stated in the Methods. The statement of
    07_declarations.md (the Fire Ecology wording) moves, unchanged, to the end of Section 2.13."""
    i = body.index("\n# 3 Results")
    last = re.findall(r"(?m)^## (\d+\.\d+) ", body[:i])[-1]
    assert last == "2.13", f"the last Methods subsection is {last}, not 2.13"
    return body[:i].rstrip() + "\n\n" + statement + "\n" + body[i:]


def tables(body):
    """'**Table n. Title.** legend' + pipe table + optional table note -> 'Table n' in bold and the title
    above the table (Springer), the legend and the note below it."""
    pat = re.compile(r"\*\*Table (\d+)\. (.+?)\.\*\*\s*(.*?)\n\n((?:\|[^\n]*\n?)+)(?:\n\*Table note\.\* (.*?)(?=\n\n|\Z))?", re.S)
    n, items = 0, []

    def fix(m):
        nonlocal n
        n += 1
        num, title, legend, table, note = m.groups()
        assert int(num) == n, f"table {num} out of order"
        below = " ".join(legend.split()) + (" " + " ".join(note.split()) if note else "")
        items.append(int(num))
        return f"**Table {num}** {title}\n\n{table.rstrip()}\n\n{below}\n"
    body = pat.sub(fix, body)
    assert not re.search(r"\*\*Table \d+\. ", body), "a table caption was not converted"
    return body, items


def caption(n, title, legend):
    """'Fig. n' in bold, no punctuation after the number and none at the end (Springer)."""
    return re.sub(r"\.\s*$", "", f"**Fig. {n}** {title} {legend}".strip())


def insert_figures(body, caps, embed):
    ends = [(F.first_cite_paragraph_end(body, rf"\bFigs?\. (?:\d+(?:, | and | to ))*{n}\b(?!\.\d)"), n)
            for n in range(1, len(caps) + 1)]
    out, last = [], 0
    for end, n in sorted(ends):
        path, width = embed[n]
        out += [body[last:end], f"\n\n![{caption(n, *caps[n - 1])}]({path.as_posix()}){{width={width:.2f}cm}}\n"]
        last = end
    return "".join(out) + body[last:]


def check_display_items(md, n_fig, n_tab):
    """As journal_fire_ecology.check_display_items, for this layout: every figure and table cited in body
    prose, first cited in numerical order, and placed after that citation."""
    body = md[md.index("\n# 1 Introduction"):md.index("\n# References")]
    blocks = [(m.start(), m.group(0)) for m in re.finditer(r"[^\n]+(?:\n[^\n]+)*", body)]
    report = {}
    for label, cite, place, n_items in (("Fig", r"\bFigs?\. ((?:\d+(?:, | and | to ))*\d+)\b(?!\.\d)", r"!\[\*\*Fig\. (\d+)\*\* ", n_fig),
                                        ("Table", r"\bTables? ((?:\d+(?:, | and | to ))*\d+)\b", r"\*\*Table (\d+)\*\* ", n_tab)):
        placed = {int(m.group(1)): m.start() for m in re.finditer(place, body)}
        first = {}
        for pos, t in blocks:
            if t.startswith(("|", "#", "![", "$$")) or re.match(r"\*\*Table \d+\*\* ", t):
                continue
            for m in re.finditer(cite, t):
                for k in J._expand(m.group(1)):
                    first.setdefault(k, pos)
        want = set(range(1, n_items + 1))
        assert set(placed) == want, f"{label} placed {sorted(placed)} != 1..{n_items}"
        assert want <= set(first), f"{label}s not cited in body prose: {sorted(want - set(first))}"
        order = [first[k] for k in sorted(want)]
        assert order == sorted(order), f"{label}s first cited out of numerical order"
        late = [k for k in want if placed[k] < first[k]]
        assert not late, f"{label}s placed before their first citation: {late}"
        report[label] = len(want)
    return report


def anchor_figures(md):
    """Bookmarks for the figures; journal_fire_ecology.anchor_targets does headings, tables and equations
    (its figure pattern expects the Fire Ecology caption, so it leaves these alone)."""
    ids = set()

    def fig(m):
        ids.add(f"fig_{m.group(2)}")
        return f"::: {{#fig_{m.group(2)}}}\n{m.group(1)}\n:::"
    md = re.sub(r"(?ms)^(!\[\*\*Fig\. (\d+)\*\* .*?\)\{[^}]*\})", fig, md)
    return md, ids


# ---------------------------------------------------------------- build
def build(pdf=True):
    OUT.mkdir(parents=True, exist_ok=True)
    B.OUT = OUT
    title, kw = NH["title"], B.FM["keywords"]
    assert title != B.FM["title"], "Natural Hazards title not set"
    assert 4 <= len(kw) <= 6, f"{len(kw)} keywords; Natural Hazards asks for 4 to 6"
    abs_text, n_abs = abstract()

    raw = {f: B.clean((P / f"{f}.md").read_text(encoding="utf-8"), f) for f in B.BODY}
    EQ = {}
    body = B.equations(B.narrative("\n\n".join(raw[f] for f in B.BODY)), EQ)
    body = re.sub(r"(?m)^# (\d+)\. ", r"# \1 ", body)
    body, n = re.subn(r"(?m)^# 1 Background$", "# 1 Introduction", body)
    assert n == 1, "the heading '1 Background' was not found"
    heads = re.findall(r"(?m)^# \d+ (.+)$", body)
    assert heads == HEADS, heads
    assert body.count(J.ADDITIONAL_AFTER) == 1, "anchor for the Online Resource 1 pointer not found"
    body = body.replace(J.ADDITIONAL_AFTER, J.ADDITIONAL_AFTER + " " + POINTER)
    body, n = re.subn(r"\bthe\s+Supplementary Material\b", ESM, body)
    assert n == 1, f"{n} mentions of 'the Supplementary Material' in the main text; expected one"
    assert "Supplementary Material" not in body and "Additional file" not in body

    decl_src = B.clean((P / f"{B.DECL}.md").read_text(encoding="utf-8"), B.DECL)
    decl = F.sections(decl_src)
    assert set(decl) == {"Funding", "Competing interests", "Author contributions", "Data availability",
                         "Code availability", "Ethics approval", "Use of generative AI"}, sorted(decl)
    genai = F.flat(decl["Use of generative AI"])
    body = move_genai(body, B.narrative(genai))
    decl_md, n = re.subn(r"(?ms)^## Use of generative AI\n.*?(?=^## |\Z)", "", decl_src)
    assert n == 1 and "generative AI" not in decl_md, "the statement on generative AI is still in the declarations"
    decl_md = B.narrative(decl_md).rstrip()
    body, tab_items = tables(body)

    # figures: vector PDFs for upload, 300 dpi copies embedded after the first citing paragraph
    caps = J.figure_captions()
    tmp = OUT / "_embed"
    tmp.mkdir(exist_ok=True)
    embed, fig_src = {}, {}
    for n in range(1, len(caps) + 1):
        src = sorted(FIGS.glob(f"fig{n}_*.pdf"))
        assert len(src) == 1, src
        fig_src[n] = src[0]
        shutil.copyfile(src[0], OUT / f"Fig{n}.pdf")
        _, width = F.rasterise(n, 300, tmp / f"Fig{n}.png")
        embed[n] = (tmp / f"Fig{n}.png", min(width, 16.0))
    n_words = J.main_text_words(body)
    body = insert_figures(body, caps, embed)

    names = ", ".join(f"{name}^1{'\\*' if mail == J.CORRESPONDING else ''}^" for name, _, mail, _ in J.AUTHORS)
    orcid = ", ".join(f"{name} (ORCID {o})" for name, _, _, o in J.AUTHORS if o)
    ack = B.ACK.split("\n\n", 1)[1].strip()
    # the authors' rule: no colons or semicolons in the prose this profile writes
    front = f"""---
title: "{title}"
lang: en-GB
---

{names}

^1^ {J.AFFILIATION}

^\\*^ Corresponding author {CORRESPONDING_NAME} ({J.CORRESPONDING})

{orcid}

The main text (Sections 1 to 5, without tables, figure captions, equations, references and
declarations) has @@WORDS@@ words, and the abstract has {n_abs} words.

# Acknowledgements

{ack}

# Abstract

{abs_text}

**Keywords** {" · ".join(kw)}
"""
    back = "# References\n\n::: {#refs}\n:::\n\n" + decl_md + "\n"
    ms_md = front + "\n\n" + body + "\n\n" + back
    assert ESM in body, f"{ESM} not cited in the text"
    items = check_display_items(ms_md, len(caps), len(tab_items))
    ms_md = ms_md.replace("@@WORDS@@", f"{n_words:,}")
    ms_md, fig_ids = anchor_figures(ms_md)
    ms_md, ids = J.anchor_targets(ms_md)
    ms_md, _ = J.link_refs(ms_md, ids | fig_ids)
    assert "§" not in ms_md and "\\S" not in ms_md, "section sign in the manuscript (author's rule)"
    (HERE / "manuscript_natural_hazards_assembled.md").write_text(ms_md, encoding="utf-8")   # build record

    out = OUT / "manuscript.docx"
    B.to_docx(ms_md, out, title)
    n_ms_links = J.check_links(out)
    d = Document(out)
    allt = "\n".join(F._text(p) for p in d.element.body.iter(qn("w:p")))
    assert "???" not in allt and not re.search(r"(?<![\w.])@[A-Za-z]", allt), "unresolved citation in the .docx"
    cp = d.core_properties
    iso = subprocess.run(["git", "log", "-1", "--format=%cI"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    cp.created = cp.modified = datetime.datetime.fromisoformat(iso).astimezone(datetime.timezone.utc).replace(tzinfo=None)
    d.save(out)
    B.strip_custom_props(out)
    shutil.rmtree(tmp)
    sources = "\n".join([abs_text, "\n".join(raw.values()), "\n".join(B.captions()), decl_src])
    n_dec = J.check_numbers(sources, ms_md, out)

    # ---- Online Resource 1: the shared Supplementary Material, with its own reference list
    sup_src = B.clean((P / "supplementary.md").read_text(encoding="utf-8"), "supplementary")
    old = f"Supplementary material for *{B.FM['title']}*."
    assert sup_src.count(old) == 1, "the supplement's opening line no longer names the shared title"
    sup_src = sup_src.replace(old, f"Supplementary material for *{title}*.")
    assert B.FM["title"] not in sup_src, "the supplement still names the shared title"
    SEQ = {}
    sup = B.equations(B.narrative(sup_src), SEQ, prefix="S", external=EQ)
    sup = re.sub(r"\A# Supplementary Material\s*\n", "", sup)
    sup, sup_ids = J.anchor_targets(sup, "S")
    head, toc, rest = re.split(r"(?ms)(^## Contents\n.*?)(?=^# )", sup, maxsplit=1)
    toc = re.sub(r"(?m)^(\s*- )(S\d+(?:\.\d+)*) (.+)$",
                 lambda m: (f"{m.group(1)}[{m.group(2)} {m.group(3)}](#sec_{J._key(m.group(2))})"
                            if f"sec_{J._key(m.group(2))}" in sup_ids else m.group(0)), toc)
    sup, _ = J.link_refs(head + toc + rest, sup_ids, "S")
    assert "§" not in sup and "\\S" not in sup, "section sign in Online Resource 1 (author's rule)"
    authors = ", ".join(name for name, *_ in J.AUTHORS)
    ident = (f"*{JOURNAL}*. {authors}. {J.AFFILIATION}. Corresponding author {CORRESPONDING_NAME} "
             f"({J.CORRESPONDING}).")
    sup_md = (f'---\ntitle: "{ESM} (Supplementary Material)"\nsubtitle: "{title}"\nlang: en-GB\n---\n\n'
              + ident + "\n\n" + sup + "\n\n# References\n\n::: {#refs}\n:::\n")
    sup_docx = OUT / "_esm_1.docx"
    B.to_docx(sup_md, sup_docx, f"{ESM}: " + title)
    n_sup_links = J.check_links(sup_docx)
    F.balance_tables(sup_docx)
    J.supplement_layout(sup_docx)
    if pdf:
        F.word_pdf(sup_docx, OUT / "ESM_1.pdf")
    sup_docx.unlink()

    # ---- cover letter: the committed draft has no reviewers; the local copy gets them
    letter = (HERE / "natural_hazards_cover_letter.md").read_text(encoding="utf-8")
    # the letter's own prose, before the title and the reviewers go in (the title is the authors' choice)
    assert not re.search(r"[;§]|(?<!https):(?!//)", letter), \
        "colon, semicolon or section sign in the cover letter (authors' rule)"
    letter = letter.replace("{{TITLE}}", title).replace("{{WORDS}}", f"{n_words:,}")
    for s in ("has not been published, and it is not under consideration for publication elsewhere",
              "All authors have approved the manuscript for submission", "competing interests"):
        assert s in F.flat(letter), f"cover letter lacks: {s}"
    stray = set(F.DEC.findall(re.sub(r"https?://\S+", "", letter))) - set(F.DEC.findall(abs_text))   # DOIs are not results
    assert not stray, f"cover letter numbers not in the abstract: {stray}"
    draft = letter.replace("{{REVIEWERS}}", "\\[The suggested reviewers, with affiliation and institutional "
                                             "e-mail, are inserted from the local file suggested_reviewers.md, "
                                             "which is not public.\\]")
    B.to_docx(draft, OUT / "cover_letter_draft.docx", "Cover letter")
    F.letter_format(OUT / "cover_letter_draft.docx")
    rev = OUT / "suggested_reviewers.md"
    if (OUT / "cover_letter.docx").exists():
        # the authors date and sign this local copy by hand (2026-10-25), so a rebuild must not replace it
        print("cover_letter.docx exists and was left as it is (delete it to rebuild it from the template)")
    elif rev.exists():
        block = rev.read_text(encoding="utf-8").split("<!-- cover letter -->", 1)
        assert len(block) == 2, "suggested_reviewers.md lacks the '<!-- cover letter -->' marker"
        B.to_docx(letter.replace("{{REVIEWERS}}", block[1].strip()), OUT / "cover_letter.docx", "Cover letter")
        F.letter_format(OUT / "cover_letter.docx")

    manifest(fig_src, n_abs, n_words, n_dec, items)
    print(f"manuscript.docx: title {len(title.split())} words, abstract {n_abs} words, {len(kw)} keywords, "
          f"main text {n_words} words, {len(caps)} figures and {len(tab_items)} tables embedded, "
          f"{n_dec} decimals matched; internal links: {n_ms_links} in the manuscript, {n_sup_links} in {ESM}")


def manifest(fig_src, n_abs, n_words, n_dec, items):
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "paper", ":!paper/submissions/natural_hazards",
                            ":!paper/tex/manuscript_natural_hazards_assembled.md"],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    state = commit + (" (with uncommitted source changes)" if dirty else "")
    src = {"manuscript.docx": "paper/00_abstract.md, 01, 03-07 *.md, figure_captions.tex, frontmatter.json, REFERENCES.bib",
           "ESM_1.pdf": "paper/supplementary.md, Word PDF export",
           "cover_letter_draft.docx": "paper/tex/natural_hazards_cover_letter.md (unsigned, without the reviewers)"}
    for n, f in fig_src.items():
        src[f"Fig{n}.pdf"] = f"{f.relative_to(ROOT).as_posix()} (vector, unchanged)"
    rows = []
    for name in ["manuscript.docx", "ESM_1.pdf", *[f"Fig{n}.pdf" for n in fig_src], "cover_letter_draft.docx"]:
        f = OUT / name
        if f.exists():
            rows.append(f"| `{name}` | {f.stat().st_size} | `{hashlib.sha256(f.read_bytes()).hexdigest()}` | {src[name]} |")
    text = f"""# Submission package: Natural Hazards (Springer)

Original research article. Built from commit `{state}` by `python paper/tex/build_docx.py --journal nh`;
the profile is `paper/tex/journal_natural_hazards.py`. The earlier, never submitted Natural Hazards
package of 2026-09-29 is kept in `unsent_2026-09-29/`.

Build-time checks: abstract {n_abs} words (150 to 250), abbreviations defined; {len(B.FM['keywords'])}
keywords (4 to 6); sections {", ".join(HEADS)}; the statement on generative AI at the end of Section 2.13;
{items.get('Fig')} figures and {items.get('Table')} tables cited in body prose, in order, placed after their
first citation; Online Resource 1 cited; every citation resolved; {n_dec} decimals identical between the
assembled Markdown and the .docx. Main text {n_words} words. Run separately: `paper/figures/check_all.py`,
`paper/code/check_stale_values.py`, `paper/code/verify_references.py`.

Open items for the corresponding author are Emrehan Metin's approval of this version, the date and
signature of the cover letter (`cover_letter.docx`, local) and the suggested reviewers
(`suggested_reviewers.md`, local).

| File | Size (bytes) | SHA-256 | Source |
|---|---:|---|---|
""" + "\n".join(rows) + "\n"
    (OUT / "MANIFEST.md").write_text(text, encoding="utf-8")
