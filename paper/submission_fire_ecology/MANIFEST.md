# Submission package: Fire Ecology (SpringerOpen)

Research article. Built from commit `9bae6c75b9d6c462fde1bea0b57a6f1f2563ccfc` by `python paper/tex/build_docx.py --journal fire-ecology`;
the profile is `paper/tex/journal_fire_ecology.py`. The shared sources were restructured for this journal
on 2026-10-12 (Background merged from the former Introduction and Related work, Methods in the active
voice, about 900 words shorter); the earlier Fire (MDPI) package was built from commit `ab058c2`.

Build-time checks: title 9 words, no numbers or acronyms; structured abstract
342 words (limit 500); 10 keywords, alphabetical, none in the title; main text
7862 words (about 8000 asked, 8800 at most without the Editor-in-Chief); figure and
table titles at most 15 words and legends at most 300 (Table 1: title 8 words, legend 93 words; Table 2: title 7 words, legend 75 words; Table 3: title 12 words, legend 86 words); 8 figures and
3 tables cited in body prose, in order, placed after their first citation; every
citation resolved; abbreviations listed; 558 decimals identical between the assembled Markdown and the
.docx. Run separately: `paper/figures/check_all.py`, `paper/code/check_stale_values.py`,
`paper/code/verify_references.py`.

Open items for the corresponding author: Emrehan Metin's approval of this version (title and text
changed); the cover letter's date and signature (`cover_letter.docx`, local); at least five suggested
reviewers (`suggested_reviewers.md`, local); the article processing charge is paid from the BAP project
after acceptance.

| File | Size (bytes) | SHA-256 | Source |
|---|---:|---|---|
| `manuscript.docx` | 1259793 | `015f0433e6e43d29e1a842c154b3bd5e9d6eed7fd8c8f53db8cd9c87e0fdc9e4` | paper/01, 03-07 *.md, 00_abstract_fire_ecology.md, figure_captions.tex, frontmatter.json, REFERENCES.bib |
| `Additional_file_1.pdf` | 1254593 | `10cf66397299539b2ecd34a7e1b21eb1f1474fdc494a3c1d555d9d71b46112d2` | paper/supplementary.md, Word PDF export |
| `Fig1.pdf` | 184479 | `8a4c3d70ccb26bc456151c1bf171c497b402025fdc3a59f9a764d77b99535ce3` | paper/figures/fig1_study_map.pdf (vector, unchanged) |
| `Fig2.pdf` | 100302 | `6efeecda7fc133e01bd867f3e747747f295168bcc2eeb9ba4d12049a7d7e5a63` | paper/figures/fig2_schematic.pdf (vector, unchanged) |
| `Fig3.pdf` | 62922 | `7f6ae47fd2c1cbbefe64befe52764043523c417435e141a186474986c58bfb45` | paper/figures/fig3_within_robustness.pdf (vector, unchanged) |
| `Fig4.pdf` | 53299 | `203f0064163f460b29b8e2b8ed185baad2ed3e41361db8f83ee0f20a4c603906` | paper/figures/fig4_transfer_matrix.pdf (vector, unchanged) |
| `Fig5.pdf` | 64148 | `0eea6783f90170fbe69270a5a3e88b97eaa2e09e6d054ef2cfe2e3121d0fae0a` | paper/figures/fig5_adaptation.pdf (vector, unchanged) |
| `Fig6.pdf` | 45110 | `065faaf3a398d2b5d2305a75e6bfb6d0717387e93541176c3cbddfbd4afad9bc` | paper/figures/fig6_loro.pdf (vector, unchanged) |
| `Fig7.pdf` | 65723 | `f794794dcf4a493967479f213e1a1c47d4d06d0c8b9f256d7bc2064c5909b90e` | paper/figures/fig7_feature_drop.pdf (vector, unchanged) |
| `Fig8.pdf` | 109340 | `63687ef11a5654a25a12c3a24a570d6a6723fe5bd0d09eeed1ec361184a5540c` | paper/figures/fig8_contrast_pairs.pdf (vector, unchanged) |
| `cover_letter_draft.docx` | 12557 | `adc32aac0a463e5e5d5f35c89a46d51c2a25327b7184785cd0f58c885df9e53b` | paper/tex/fire_ecology_cover_letter.md (unsigned, without the reviewers) |
