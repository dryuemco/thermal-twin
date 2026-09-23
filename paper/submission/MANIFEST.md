# Submission package

Ecological Informatics. Every file below was built from, and is committed in, `5be3690`
(verify: `git show 5be3690:paper/submission/<file> | sha256sum`). Main text: 9,966 words, excluding
references, tables, figure captions and declarations.

| File | Format | Size (bytes) | SHA-256 | Source |
|---|---|---:|---|---|
| `manuscript.docx` | Word (.docx) | 58013 | `28cb35c21ef178bf…` | paper/0*.md, 07_declarations.md via paper/tex/build_docx.py |
| `supplement.pdf` | PDF | 643696 | `b2b1336f928bc936…` | paper/supplementary.md via build_tex.mjs + pdflatex |
| `fig1.pdf` | PDF (vector) | 180317 | `1362466cad2ea8de…` | paper/figures/fig1_study_map.py |
| `fig2.pdf` | PDF (vector) | 96427 | `0c573ea08629f973…` | paper/figures/fig2_schematic.py |
| `fig3.pdf` | PDF (vector) | 63431 | `354ad0d824d36351…` | paper/figures/fig3_within_robustness.py |
| `fig4.pdf` | PDF (vector) | 64362 | `972f30d801482073…` | paper/figures/fig4_transfer_matrix.py |
| `fig5.pdf` | PDF (vector) | 64085 | `af5132b4332f66c4…` | paper/figures/fig5_adaptation.py |
| `fig6.pdf` | PDF (vector) | 45718 | `126d9c6591211d99…` | paper/figures/fig6_loro.py |
| `fig7.pdf` | PDF (vector) | 66068 | `f5ac3c87b6d6463b…` | paper/figures/fig7_feature_drop.py |
| `fig8.pdf` | PDF (vector) | 119341 | `4cbc6639fbccac5c…` | paper/figures/fig8_contrast_pairs.py |
| `graphical_abstract.pdf` | PDF (vector) | 132047 | `823e8a031f61e654…` | paper/figures/graphical_abstract.py |
| `highlights.tex` | LaTeX text | 706 | `50b26075ea28c968…` | paper/highlights.tex |

## When the figures were rendered

The figure PDFs are the figures of record committed when each was last rendered; no figure PDF has
changed since. Figs. 3 to 8 and the graphical abstract were rendered under the corrected Manavgat
label. Figs. 1 and 2, the study map and the processing schematic, plot no label-dependent value.
Every render commit is an ancestor of `dc9b307`, and later commits touched only text, tooling and
data placement, not any plotted value. `paper/figures/check_all.py` asserts every plotted value
against the frozen outputs and the manuscript text, and passed 10/10 at `dc9b307`, in a clean
clone, and at `5be3690`, where this package was built.

| File | Rendered in | Date |
|---|---|---|
| `fig1.pdf` | `7327c45` | 2026-09-23 |
| `fig2.pdf` | `7d543f6` | 2026-09-19 |
| `fig3.pdf` | `b0fdc1c` | 2026-09-23 |
| `fig4.pdf` | `a277d0c` | 2026-09-23 |
| `fig5.pdf` | `221f4ef` | 2026-09-23 |
| `fig6.pdf` | `25df566` | 2026-09-23 |
| `fig7.pdf` | `2cb6535` | 2026-09-23 |
| `fig8.pdf` | `7bcda99` | 2026-09-23 |
| `graphical_abstract.pdf` | `7b99fac` | 2026-09-23 |

Fig. 4's three heatmap panels are embedded as 185 x 185 px raster blocks (no interpolation); every
other figure element is vector. The cover letter is prepared by the corresponding author.
