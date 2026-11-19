# Submission package: International Journal of Wildland Fire (CSIRO Publishing)

Status on 2026-11-12. Text revised for this journal, reviewer simulation run and its points worked in
(second round of edits on 2026-11-11), all eight figures redrawn for the publisher's sizes, manuscript and
supplement built for the authors to read. Not submitted. The shared sources in `paper/` and the earlier
packages were not changed. Every file under `text/` is a copy that was edited here.

The journal's requirements were read on 2026-11-11 from connectsci.au (the author instructions of the
journal and of CSIRO Publishing, and the four guides kept in `template/`). A Research Article has at
most 6000 words from Introduction to Conclusions, without title, abstract, references, figure captions
and tables. The abstract has at most 200 words under the headings Background, Aims, Methods, Key
results, Conclusions and Implications. The template also asks for at least eight keywords, an online
summary of 50 to 80 words in three sentences, unnumbered headings, Harvard references, continuous line
numbers and at least three suggested reviewers. Submission is through ScholarOne.

Build with `python paper/submissions/ijwf/build_ijwf.py` (needs pypandoc, python-docx and MS Word for
the PDF). The last build (2026-11-12) reported an abstract of 199 words, an online summary of 79 words,
10 keywords, a main text of 5914 words as Word counts it, 8 figures, 4 tables and 55 references, and a
supplement with 5 figures, 17 tables and 10 numbered equations. Run
`python paper/submissions/ijwf/check_text.py` after any edit of the text.

| File | Size (bytes) | SHA-256 | Source |
|---|---:|---|---|
| `manuscript.docx` | 942507 | `eb07e5c0fd42d5d4…` | text/ (abstract, 01, 03 to 07, captions, frontmatter, REFERENCES.bib), CSIRO template, csiro-harvard.csl |
| `manuscript.pdf` | 1055295 | `3275def04dcb348d…` | Word export of manuscript.docx, for reading |
| `supplementary_material.docx` | 799135 | `0487c957391d963d…` | text/supplementary.md, own reference list, no line numbers |
| `supplementary_material.pdf` | 1326200 | `6aa68bbd8f13daf7…` | Word export of supplementary_material.docx |
| `figures/Fig1.pdf` | 211429 | `1511bfd08ef74196…` | figures/fig1_study_map.py (IJWF redraw, 8 and 7 pt) |
| `figures/Fig2.pdf` | 15895 | `5ee5a7fa1a29e415…` | figures/fig2_schematic.py (IJWF redraw, 8 and 7 pt) |
| `figures/Fig3.pdf` | 21527 | `d734b7d475e04910…` | figures/fig3_within_robustness.py (IJWF redraw, 8 and 7 pt) |
| `figures/Fig4.pdf` | 24982 | `9b91cb4b3ed6b572…` | figures/fig4_transfer_matrix.py (IJWF redraw, 8 and 7 pt) |
| `figures/Fig5.pdf` | 32390 | `f88697723cd01bcc…` | figures/fig5_adaptation.py (IJWF redraw, 8 and 7 pt) |
| `figures/Fig6.pdf` | 19160 | `9177b5a52f82547c…` | figures/fig6_loro.py (IJWF redraw, 8 and 7 pt) |
| `figures/Fig7.pdf` | 15575 | `6351989fc64f1168…` | figures/fig7_feature_drop.py (IJWF redraw, 8 and 7 pt) |
| `figures/Fig8.pdf` | 28678 | `2b0a7f87d58ca25d…` | figures/fig8_contrast_pairs.py (IJWF redraw, 8 and 7 pt) |

Other files

| Path | Content |
|---|---|
| `text/` | the edited sources (structured abstract and online summary, main text, statements, captions, supplement, frontmatter with the `ijwf` block, bibliography) |
| `template/` | the publisher's Word template and four guides (checklist, Harvard references, figures and tables, supplementary material), downloaded 2026-11-11, local only |
| `figures/fig1_study_map.py` … `fig8_contrast_pairs.py`, `_style_ijwf.py` | IJWF copies of the eight figure scripts with 8 pt and 7 pt text, sentence-case labels, part labels in Fig. 3, repositioned labels in Fig. 1a and Fig. 2 without section numbers, each with its PDF, SVG, preview and provenance file. The shared figures in `paper/figures/` are unchanged |
| `analyses/local_check_history.py` | exploratory check of borrowed models against the burns of the five earlier years (Supplementary Section S4.6, Table S17), with a reproduction gate against Table S8 |
| `analyses/make_supplement_sections.py` | writes Sections S2.3 (distance bands, Table S16) and S4.6 into `text/supplementary.md` between markers |
| `zotero_references.py`, `reference_check.json` | the cited works as a Zotero collection ("IJWF wildfire transfer manuscript references (2026-11)", 61 items) and the comparison of their metadata with Crossref and DataCite |
| `csiro-harvard.csl` | citation style written by hand after the publisher's Harvard examples |
| `build_ijwf.py`, `check_text.py` | the build and the comparison with the shared sources |

Title. The reviewer simulation of 2026-11-11 objected to "wildfire susceptibility models" for models
trained on one fire season, so the title now reads "single-season wildfire models". The earlier title is
kept in `text/frontmatter.json` under `title_before_reviewer_simulation`.

Open items

- A decision between submitting this version and a larger rewrite. A scale-up pilot (26 further fires chosen
  by rule, scratch copy of the pipeline, 2026-11-12) and a literature check of novelty are being run for that
  decision. Their files are outside this package and nothing from them is in the text.
- Twenty-seven references are no longer cited (the list is printed by the check).
- The earlier-burn check of Section S4.6 is a negative result. The authors decide whether it stays.
- The statement that label errors concentrate at scar edges has no test behind it.
- Cover letter, at least three suggested reviewers, the co-author's approval, a new Zenodo release that
  contains the scripts added here, and a link to the preprint if one was posted.
