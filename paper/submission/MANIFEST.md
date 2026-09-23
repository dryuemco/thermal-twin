# Submission package

Ecological Informatics. Every file below was built from, and is committed in, `5be3690`
(verify: `git show 5be3690:paper/submission/<file> | sha256sum`), with two later changes.
`highlights.txt` was added afterwards: the plain-text form of `paper/highlights.tex` (unchanged since
`99ee346`), one highlight per line with the LaTeX markup removed, written by `paper/tex/build_docx.py`.
On 2026-09-24 `fig5.pdf`, `fig6.pdf` and `fig7.pdf` were re-rendered without their in-figure titles
(Elsevier takes captions from the manuscript, and the captions carry the same statement), and
`manuscript.docx` was rebuilt after Section 4.2 gained its citation of Table 1, which the running
text previously never cited. The hashes below are for those files; `git log -- paper/submission/<file>`
gives the commit. Main text: 9,968 words, excluding references, tables, figure captions and
declarations.

| File | Format | Size (bytes) | SHA-256 | Source |
|---|---|---:|---|---|
| `manuscript.docx` | Word (.docx) | 58016 | `1e6b01516687303a…` | paper/0*.md, 07_declarations.md via paper/tex/build_docx.py |
| `supplement.pdf` | PDF | 643696 | `b2b1336f928bc936…` | paper/supplementary.md via build_tex.mjs + pdflatex |
| `fig1.pdf` | PDF (vector) | 180317 | `1362466cad2ea8de…` | paper/figures/fig1_study_map.py |
| `fig2.pdf` | PDF (vector) | 96427 | `0c573ea08629f973…` | paper/figures/fig2_schematic.py |
| `fig3.pdf` | PDF (vector) | 63431 | `354ad0d824d36351…` | paper/figures/fig3_within_robustness.py |
| `fig4.pdf` | PDF (vector) | 64362 | `972f30d801482073…` | paper/figures/fig4_transfer_matrix.py |
| `fig5.pdf` | PDF (vector) | 63246 | `86de93b84241f6e5…` | paper/figures/fig5_adaptation.py |
| `fig6.pdf` | PDF (vector) | 44900 | `668d7445bdd3528e…` | paper/figures/fig6_loro.py |
| `fig7.pdf` | PDF (vector) | 65723 | `581690af4a435c94…` | paper/figures/fig7_feature_drop.py |
| `fig8.pdf` | PDF (vector) | 119341 | `4cbc6639fbccac5c…` | paper/figures/fig8_contrast_pairs.py |
| `graphical_abstract.pdf` | PDF (vector) | 132047 | `823e8a031f61e654…` | paper/figures/graphical_abstract.py |
| `highlights.txt` | plain text, UTF-8, 5 lines of 68, 69, 71, 73 and 83 characters | 369 | `11854d0e60914b02…` | paper/highlights.tex |

## When the figures were rendered

The figure PDFs are the figures of record committed when each was last rendered. Figs. 3 to 8 and
the graphical abstract were rendered under the corrected Manavgat label. Figs. 1 and 2, the study map
and the processing schematic, plot no label-dependent value. Figs. 1 to 4, 8 and the graphical
abstract were rendered in ancestors of `dc9b307`, and later commits touched only text, tooling and
data placement, not any plotted value. Figs. 5 to 7 were re-rendered on 2026-09-24 only to remove
their in-figure titles: no plotted value, axis, legend or annotation changed, and the axes grew into
the band the title had occupied. `paper/figures/check_all.py` asserts every plotted value against
the frozen outputs and the manuscript text. It passed 10/10 at `dc9b307`, in a clean clone, and at
`5be3690`, where this package was built, and again after the 2026-09-24 re-render, in the working
tree and in a clean clone.

| File | Rendered in | Date |
|---|---|---|
| `fig1.pdf` | `7327c45` | 2026-09-23 |
| `fig2.pdf` | `7d543f6` | 2026-09-19 |
| `fig3.pdf` | `b0fdc1c` | 2026-09-23 |
| `fig4.pdf` | `a277d0c` | 2026-09-23 |
| `fig5.pdf` | commit "Figs. 5-7 without in-figure titles" (`git log -1 -- paper/submission/fig5.pdf`) | 2026-09-24 |
| `fig6.pdf` | same commit | 2026-09-24 |
| `fig7.pdf` | same commit | 2026-09-24 |
| `fig8.pdf` | `7bcda99` | 2026-09-23 |
| `graphical_abstract.pdf` | `7b99fac` | 2026-09-23 |

Fig. 4's three heatmap panels are embedded as 185 x 185 px raster blocks (no interpolation); every
other figure element is vector. The cover letter is prepared by the corresponding author.
