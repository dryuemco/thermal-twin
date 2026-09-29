# Submission package: Natural Hazards (Springer)

Built 2026-09-29. Rebuild: `python paper/tex/build_docx.py` (manuscript.docx,
supplementary_material.docx), Word export for supplementary_material.pdf, and
`paper/figures/fig*.py` for the figures. Checks at build time: `paper/figures/check_all.py` 9/9 PASS
(176 supplementary table rows), `paper/code/check_stale_values.py` clean,
`paper/code/verify_references.py` 54/54.

| File | Size (bytes) | SHA-256 | Source |
|---|---:|---|---|
| `manuscript.docx` | 49534 | `83b3669d6c146bd6…` | paper/0*.md, frontmatter.json, REFERENCES.bib via build_docx.py |
| `supplementary_material.pdf` | 973294 | `b2f1fc51393106ab…` | paper/supplementary.md via build_docx.py and Word PDF export |
| `supplementary_material.docx` | 83466 | `2974c883efd7535c…` | paper/supplementary.md via build_docx.py |
| `cover_letter.md` | 2811 | `5a7e0a322f195b28…` | written for Natural Hazards (kept locally, not in the public repository) |
| `fig1.pdf` | 180317 | `1362466cad2ea8de…` | paper/figures/fig1_study_map.py |
| `fig2.pdf` | 96257 | `b4925e0014b81a99…` | paper/figures/fig2_schematic.py |
| `fig3.pdf` | 63431 | `354ad0d824d36351…` | paper/figures/fig3_within_robustness.py |
| `fig4.pdf` | 51236 | `07db1ebfdc6ec7be…` | paper/figures/fig4_transfer_matrix.py |
| `fig5.pdf` | 63246 | `86de93b84241f6e5…` | paper/figures/fig5_adaptation.py |
| `fig6.pdf` | 45110 | `513638fb195b1ace…` | paper/figures/fig6_loro.py |
| `fig7.pdf` | 65723 | `581690af4a435c94…` | paper/figures/fig7_feature_drop.py |
| `fig8.pdf` | 109308 | `f8882b3bb6cbea04…` | paper/figures/fig8_contrast_pairs.py |

Main text: 7,092 words (Sections 1 to 6, table captions and notes included; tables, references,
declarations and figure captions excluded).
