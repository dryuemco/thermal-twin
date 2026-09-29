# Submission package: Natural Hazards (Springer)

Built 2026-09-29. Rebuild: `python paper/tex/build_docx.py` (manuscript.docx,
supplementary_material.docx), Word export for supplementary_material.pdf, and
`paper/figures/fig*.py` for the figures. Checks at build time: `paper/figures/check_all.py` 9/9 PASS
(176 supplementary table rows), `paper/code/check_stale_values.py` clean,
`paper/code/verify_references.py` 61/62 (the Zenodo DOI was not yet registered at DataCite).

| File | Size (bytes) | SHA-256 | Source |
|---|---:|---|---|
| `manuscript.docx` | 54558 | `c4db3f58ff29b762…` | paper/0*.md, frontmatter.json, REFERENCES.bib via build_docx.py |
| `supplementary_material.pdf` | 1159504 | `6365a27150f51fd2…` | paper/supplementary.md via build_docx.py and Word PDF export |
| `supplementary_material.docx` | 496702 | `814639ed336e26e2…` | paper/supplementary.md via build_docx.py |
| `fig1.pdf` | 180363 | `2190ca969dbba1fe…` | paper/figures/fig1_study_map.py |
| `fig2.pdf` | 96257 | `c9a983272fb2c066…` | paper/figures/fig2_schematic.py |
| `fig3.pdf` | 62922 | `7f6ae47fd2c1cbbe…` | paper/figures/fig3_within_robustness.py |
| `fig4.pdf` | 53299 | `203f0064163f460b…` | paper/figures/fig4_transfer_matrix.py |
| `fig5.pdf` | 64148 | `0eea6783f90170fb…` | paper/figures/fig5_adaptation.py |
| `fig6.pdf` | 45110 | `065faaf3a398d2b5…` | paper/figures/fig6_loro.py |
| `fig7.pdf` | 65723 | `f794794dcf4a4939…` | paper/figures/fig7_feature_drop.py |
| `fig8.pdf` | 109340 | `63687ef11a5654a2…` | paper/figures/fig8_contrast_pairs.py |

Main text: 8,793 words (Sections 1 to 6, table captions and notes included; tables, references,
declarations and figure captions excluded).
