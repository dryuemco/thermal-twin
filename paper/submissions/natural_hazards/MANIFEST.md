# Submission package: Natural Hazards (Springer)

Original research article. Built from commit `c6d5b6d9f90b983c44236fdcced6c0138d24a5cf (with uncommitted source changes)` by `python paper/tex/build_docx.py --journal nh`;
the profile is `paper/tex/journal_natural_hazards.py`. The earlier, never submitted Natural Hazards
package of 2026-09-29 is kept in `unsent_2026-09-29/`.

Build-time checks: abstract 247 words (150 to 250), abbreviations defined; 6
keywords (4 to 6); sections Introduction, Methods, Results, Discussion, Conclusions; the statement on generative AI at the end of Section 2.13;
8 figures and 4 tables cited in body prose, in order, placed after their
first citation; Online Resource 1 cited; every citation resolved; 533 decimals identical between the
assembled Markdown and the .docx. Main text 8716 words. Run separately: `paper/figures/check_all.py`,
`paper/code/check_stale_values.py`, `paper/code/verify_references.py`.

Open items for the corresponding author are Emrehan Metin's approval of this version, the date and
signature of the cover letter (`cover_letter.docx`, local) and the suggested reviewers
(`suggested_reviewers.md`, local).

| File | Size (bytes) | SHA-256 | Source |
|---|---:|---|---|
| `manuscript.docx` | 878599 | `980ccd94c7a762297b354f236be52bca78a1e649c8655fd87355d1693be62c6d` | paper/00_abstract.md, 01, 03-07 *.md, figure_captions.tex, frontmatter.json, REFERENCES.bib |
| `ESM_1.pdf` | 1473550 | `bdbfe5a9dd04644442b1e89e9fcc18e8cef0a9e1f87dc2662613548d7299b010` | paper/supplementary.md, Word PDF export |
| `Fig1.pdf` | 210603 | `7a0304766ad54715e3bd32dfd203463123efef7fc0f14dacf78faf08d3c2ab74` | paper/figures/fig1_study_map.pdf (vector, unchanged) |
| `Fig2.pdf` | 19768 | `7ef3e5fe3d1769b99b9fa129ece51c740c902fe25531c23361c9a031f12bdb0a` | paper/figures/fig2_schematic.pdf (vector, unchanged) |
| `Fig3.pdf` | 21335 | `0009b6c39aeb51bc5dee8f49a83f431de88fcfb0bf7d7adaf1601c2f2f66b3da` | paper/figures/fig3_within_robustness.pdf (vector, unchanged) |
| `Fig4.pdf` | 24594 | `47492f0bc53b5b589e693af75f8add8501c0b6a9398b55c7ab3af5a23105b4c3` | paper/figures/fig4_transfer_matrix.pdf (vector, unchanged) |
| `Fig5.pdf` | 32277 | `2190d7aed8dd39e9cf967cb216f97e2e4b4b37aae77cf2db64515c3cc8b8a4c5` | paper/figures/fig5_adaptation.pdf (vector, unchanged) |
| `Fig6.pdf` | 19118 | `0770d95605747766cfcba5a6d07a08cb7a124b296063ceecace915db900afff4` | paper/figures/fig6_loro.pdf (vector, unchanged) |
| `Fig7.pdf` | 15719 | `c042aa0e28c6f458ecf08d281f882f060e7ae4283dd1eabf539fd66b0b65a29f` | paper/figures/fig7_feature_drop.pdf (vector, unchanged) |
| `Fig8.pdf` | 28444 | `6ae6c444b5d7a58346be28e7c85d55dc37245cabc63ffb87848e743e3e08c6a7` | paper/figures/fig8_contrast_pairs.pdf (vector, unchanged) |
| `cover_letter_draft.docx` | 12595 | `17aa62e38f0dbfd9ccf4d51e12078a6c73f7b0ce3c725cde914e672eb8e8a301` | paper/tex/natural_hazards_cover_letter.md (unsigned, without the reviewers) |
