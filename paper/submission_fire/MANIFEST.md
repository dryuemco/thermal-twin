# Submission package: Fire (MDPI)

Second target; the Natural Hazards package in `paper/submission/` is unchanged. Built from commit
`f2926df30a742b7ee150cf1a0cc5de44624727fc` by `python paper/tex/build_docx.py --journal fire --template <fire-template.dot>` (the MDPI
template is not in the repository). `manuscript.docx` is built in the MDPI template, which MDPI
licenses for submission only and not for posting online, so it is not committed to this public
repository; rebuild it and compare its SHA-256 below. The text, figures, supplement source and references are the ones
the Natural Hazards build uses; the differences are in `paper/tex/journal_fire.py`.

Build-time checks: abstract 200 words (Fire: about 200 at most); every citation resolves to one of
72 references, every reference is cited, numbered in order of first citation (101 citation
numbers); every figure and table cited in body prose, in order, and placed after its first citation;
570 decimals identical between the assembled Markdown and the .docx. Run separately:
`paper/figures/check_all.py`, `paper/code/check_stale_values.py`, `paper/code/verify_references.py`.

Authors: Emrehan Metin (first) and Yunus Emre Cogurcu (second, corresponding), both Department of
Computer Engineering, Çukurova University, with their e-mail addresses on the title page. Funding names
the BAP project FKB-2025-17608, "Early detection and prevention of forest fires with a thermal digital twin-based UAV swarm system" (checked in the .docx at build time).

Open items: the cover letter's date, signature and the check that the manuscript is not under
consideration elsewhere when it is sent; three suggested reviewers in the submission system.

| File | Size (bytes) | SHA-256 | Source |
|---|---:|---|---|
| `manuscript.docx` | 1312397 | `0022680a107db5c984bbb7688858ed823b9befaf89c0482947f973745f1a5557` | paper/0*.md, figure_captions.tex, frontmatter.json, REFERENCES.bib via build_docx.py --journal fire |
| `supplement.pdf` | 1244140 | `98a69c259c6149fe5cfc9185e429a2b1d437d1963802a5f92b741a54ca981899` | paper/supplementary.md via build_docx.py --journal fire and Word PDF export |
| `Figure1.png` | 428923 | `53445edaf8368757120984692a0ebb6841765b7c9ebc1c2439da22a7d2f893f4` | paper/figures/fig1_study_map.pdf, rasterised at 600 dpi |
| `Figure2.png` | 533452 | `f5b69c9dce8eff0f05e33df08f5e81dd872b47425362c23ed6e5e0694515b7af` | paper/figures/fig2_schematic.pdf, rasterised at 600 dpi |
| `Figure3.png` | 376264 | `db5ae57a56ca391272815c3282a5b528fe398e855359d667bb33f4b9404ce5a2` | paper/figures/fig3_within_robustness.pdf, rasterised at 600 dpi |
| `Figure4.png` | 449336 | `e230a6848f1f50b5ce384e931f927e4e637eaf4069e774d85808273b43190c0e` | paper/figures/fig4_transfer_matrix.pdf, rasterised at 600 dpi |
| `Figure5.png` | 241961 | `f925d09961ef0f5b2fef7905298f557f884f47ebe0ee39efcadc1c799a40e17a` | paper/figures/fig5_adaptation.pdf, rasterised at 600 dpi |
| `Figure6.png` | 135360 | `bb92e72ae05ee4ab490e399f8983f4ddfdf197afcd76903a2e443e07a0dfc5f8` | paper/figures/fig6_loro.pdf, rasterised at 600 dpi |
| `Figure7.png` | 229159 | `b0f78484dd497222830d481940253d6bfc5832e6098eefb1f5a4e378f78d8fb8` | paper/figures/fig7_feature_drop.pdf, rasterised at 600 dpi |
| `Figure8.png` | 354176 | `3017f53389394dc31df9005fed45450044ab272ebd47d3549eea93d44939efaf` | paper/figures/fig8_contrast_pairs.pdf, rasterised at 600 dpi |
| `graphical_abstract.png` | 129019 | `c07d9b3435372eca1f4f5f165678cdfdcee3a7bfcda8e3a1b42d855be69d25e7` | paper/figures/graphical_abstract.py, flattened to RGB |
| `cover_letter_draft.docx` | 12261 | `8a16896c21b01110cffcbf4bc29b7ea4a534c5a51758948e28456a229dc398c4` | paper/tex/fire_cover_letter.md (unsigned draft; the signed cover_letter.docx is kept locally, not committed) |
