# Submission package: Fire Ecology (SpringerOpen)

Research article. Built from commit `5f97fec4ac898133f6ac5f32a81400a637a7c0bb` by `python paper/tex/build_docx.py --journal fire-ecology`;
the profile is `paper/tex/journal_fire_ecology.py`. The shared sources were restructured for this journal
on 2026-10-12 (Background merged from the former Introduction and Related work, Methods in the active
voice, about 900 words shorter); the earlier Fire (MDPI) package was built from commit `ab058c2`.

Build-time checks: title 9 words, no numbers or acronyms; structured abstract
332 words (limit 500); 10 keywords, alphabetical, none in the title; main text
8536 words (about 8000 asked, 8800 at most without the Editor-in-Chief); figure and
table titles at most 15 words and legends at most 300 (Table 1: title 7 words, legend 77 words; Table 2: title 8 words, legend 93 words; Table 3: title 7 words, legend 75 words; Table 4: title 12 words, legend 86 words); 8 figures and
4 tables cited in body prose, in order, placed after their first citation; every
citation resolved; abbreviations listed; 544 decimals identical between the assembled Markdown and the
.docx. Run separately: `paper/figures/check_all.py`, `paper/code/check_stale_values.py`,
`paper/code/verify_references.py`.

Open items for the corresponding author: Emrehan Metin's approval of this version (title and text
changed); the cover letter's date and signature (`cover_letter.docx`, local); at least five suggested
reviewers (`suggested_reviewers.md`, local); the article processing charge is paid from the BAP project
after acceptance.

| File | Size (bytes) | SHA-256 | Source |
|---|---:|---|---|
| `manuscript.docx` | 877475 | `59f00ad503134f631e6e7e185324224eb6fd3198ce190dcd4aca47a693fcb19a` | paper/01, 03-07 *.md, 00_abstract_fire_ecology.md, figure_captions.tex, frontmatter.json, REFERENCES.bib |
| `Additional_file_1.pdf` | 1458787 | `3e16b125bddf91d44ba9c9afeda22243611d3547616584215f0a189c8cc57b00` | paper/supplementary.md, Word PDF export |
| `Fig1.pdf` | 210524 | `9534c0e6407dd9ed48899690b25ee4a945176c330bab32f6abf4d6028f79bb38` | paper/figures/fig1_study_map.pdf (vector, unchanged) |
| `Fig2.pdf` | 19769 | `36321b10208588d83805fb6f4d07f4913ebdc04c3a24a0f96541dad246d70c0a` | paper/figures/fig2_schematic.pdf (vector, unchanged) |
| `Fig3.pdf` | 21335 | `0009b6c39aeb51bc5dee8f49a83f431de88fcfb0bf7d7adaf1601c2f2f66b3da` | paper/figures/fig3_within_robustness.pdf (vector, unchanged) |
| `Fig4.pdf` | 24594 | `47492f0bc53b5b589e693af75f8add8501c0b6a9398b55c7ab3af5a23105b4c3` | paper/figures/fig4_transfer_matrix.pdf (vector, unchanged) |
| `Fig5.pdf` | 32277 | `2190d7aed8dd39e9cf967cb216f97e2e4b4b37aae77cf2db64515c3cc8b8a4c5` | paper/figures/fig5_adaptation.pdf (vector, unchanged) |
| `Fig6.pdf` | 19118 | `0770d95605747766cfcba5a6d07a08cb7a124b296063ceecace915db900afff4` | paper/figures/fig6_loro.pdf (vector, unchanged) |
| `Fig7.pdf` | 15719 | `c042aa0e28c6f458ecf08d281f882f060e7ae4283dd1eabf539fd66b0b65a29f` | paper/figures/fig7_feature_drop.pdf (vector, unchanged) |
| `Fig8.pdf` | 28444 | `6ae6c444b5d7a58346be28e7c85d55dc37245cabc63ffb87848e743e3e08c6a7` | paper/figures/fig8_contrast_pairs.pdf (vector, unchanged) |
| `cover_letter_draft.docx` | 12518 | `a686c8a78bcd8ced2b1ebbc76c4f4dc16e28cb891250a3a8ffde9a7e495033a3` | paper/tex/fire_ecology_cover_letter.md (unsigned, without the reviewers) |
