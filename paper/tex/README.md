# LaTeX build — Ecological Informatics (Elsevier, `elsarticle`)

## What this is

`manuscript.tex` and `supplementary.tex` are **generated**. They are produced from the Markdown
sources in `paper/` by `build_tex.mjs`. Do not edit them by hand — edit the Markdown and re-run
the script, or the next build silently discards your changes.

```
node paper/tex/build_tex.mjs     # writes manuscript.tex, supplementary.tex, build_report.md
node paper/tex/verify_tex.mjs    # checks the port did not corrupt anything
```

## The one thing to know before trusting this

**Nothing here has ever been compiled.** This machine has no TeX installation and no pandoc, so
the files have never been run through LaTeX. `verify_tex.mjs` checks the *source*: that no number
changed, that no cross-reference dangles, that environments balance. A clean run means the port
did not corrupt the content. It does **not** mean the document typesets. Treat the first compile
as a debugging pass and expect to fix things.

Build it on Overleaf (which ships `elsarticle`) or with a local TeX Live / MiKTeX:

```
pdflatex manuscript && bibtex manuscript && pdflatex manuscript && pdflatex manuscript
```

`\bibliography{../REFERENCES}` and the figure paths point up one level, so compile from inside
`paper/tex/` with the repository intact. If your build tool dislikes `..` paths, copy
`REFERENCES.bib` and `figures/` next to the `.tex` instead.

## Why a converter and not hand conversion

Every number in this manuscript traces to a frozen pipeline output, and the project's whole
discipline is that numbers are never retyped. Hand-converting ~29,000 words and 157 table rows
would have introduced exactly the transcription risk the rest of the work exists to avoid. The
script copies text; it never re-derives it, and `verify_tex.mjs` proves the copy is faithful by
comparing every numeric token on both sides.

That check earned its keep. It caught three real defects during the port:

- Every superscript was being corrupted. `10⁻⁸` came out as `10\$\textasciicircum{}{-8}\$`
  because the math produced by the exponent folder was not protected from the escaping pass.
  In a paper whose headline reproduction result *is* `1.6×10⁻⁷`, that was not cosmetic.
- A whole sentence was deleted. The paragraph opening `**Table 2** (feature dictionary ...)` was
  mistaken for a table caption, and because no table followed, it was dropped. The converter now
  only treats such a paragraph as a caption when a table actually follows it.
- A table lost a column. Cells containing the escaped pipe in `P(y\|x)` were split on it, shearing
  a column off two rows of the diagnostics table.

## Decisions the converter makes

`build_report.md` lists every one of them, so each can be reviewed rather than trusted.

| Markdown | LaTeX | Note |
|---|---|---|
| `## 3.1 Title` | `\subsection{Title}\label{sec:3.1}` | numbering handed to LaTeX; labels keep the manuscript's own numbers |
| `Section 3.16.4` | `Section~\ref{sec:3.16.4}` | 119 cross-references |
| `Author et al. [@Key]` | `\citet{Key}` | the literal name is dropped, because `\citet` prints it — 42 of these, all listed in the report |
| `[@Key]` / `[@A; @B]` | `\citep{Key}` / `\citep{A,B}` | |
| `Fig. 3` | `\ref{fig:within-robustness}` | figure labels are read from `figure_captions.tex` in order, so the two files cannot drift |
| `**Table R7.** …` + table | `table` environment with `\caption` and `\label{tab:R7}` | the literal "Table R7." prefix is stripped, since `\caption` emits it |
| `[^id]` … `[^id]: text` | `\footnote{text}` | |
| ``` fences | `verbatim` | |
| `<!-- … -->`, `> Drafting note…` | dropped | 10 blocks; each removal is logged |

## What still needs a human

1. **Affiliation** — `[AFFILIATION]` placeholder in the author block. I cannot invent it.
2. **Keywords** — a plausible set is in place but marked; confirm against the journal's count.
3. **Abstract length** — currently 331 words. The journal's limit is not recorded anywhere in the
   project and ScienceDirect blocks automated fetching of the guide-for-authors, so it was not
   verified. Check it and trim (`STATUS.md`, remaining work item 2).
4. **Table 2** does not exist yet. The feature dictionary is described in Methods §3.4 but was
   never built as a table, so references to it are left as literal text rather than as a `\ref`
   that would compile to `??`. Build it at assembly, or reword the sentence.
5. **Title** is set from `POSITIONING.md`'s Branch A decision, not invented — but it is a
   decision, so confirm it.
6. **Supplementary figure S1** is still unbuilt (`STATUS.md` item 6).

## Class options

`\documentclass[preprint,review,12pt]{elsarticle}` — single column, double spaced, line numbers on,
which is what Elsevier asks for at submission. Switch to `[final,5p,times,twocolumn]` only to
preview the typeset look. Bibliography style is `elsarticle-harv` (author–year), matching the
author–year citations the manuscript is written in.
