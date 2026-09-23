# Declarations

<!-- Moved here from the template in paper/tex/build_tex.mjs on 2026-09-23, so that the declarations are
authored in Markdown like the rest of the manuscript and reach the .docx through pandoc. Funding,
acknowledgements, competing interests, ethics, author contributions and the generative-AI declaration are
carried over verbatim; the data and code availability statement is new. Declarations do not count
towards the article's word limit. -->

## Data and code availability

All satellite inputs are public and were retrieved through Google Earth Engine: burned-area labels
from MODIS MCD64A1 Collection 6.1, land cover from ESA WorldCover, and the thermal, optical and
terrain inputs described in Section 3.4. No proprietary or restricted data were used.

The upstream processing pipeline, `satellite-thermal-digital-twin` (E. Metin), is public at
<https://github.com/emrehann17/satellite-thermal-digital-twin> under the MIT licence. The commit of
record for every number reported here is `6381f4c`. The modelling dataset behind each number is
identified by SHA-256 in the pipeline's canonical-input record, and every analysis script verifies
that hash on load.

The analysis code, the five modelling datasets, the frozen numeric outputs and the Supplementary
Material are at
<https://github.com/dryuemco/thermal-twin>. Figs. 1–8 and the graphical abstract are drawn by the scripts in `paper/figures/`,
which also assert Table 1 and every plotted value against the frozen outputs. Sixteen of the
twenty-two supplementary tables (S2–S7, S9–S18) are rebuilt row by row by
`paper/code/appendix_tables.py` from source files whose SHA-256 values are pinned in
`paper/labelfix_rerun/round5/tables/SOURCES.sha256`; the others name their source files in their
captions. `paper/figures/check_all.py` runs all of these checks. Software: Python 3.12.10 with NumPy
2.4.4, pandas 3.0.2 and scikit-learn 1.9.0; the cross-region tolerance between scikit-learn versions
is about ±0.02 to 0.03 (Section S3.5(vi)).

## Funding

This work was supported by the Çukurova University Scientific Research Projects Coordination Unit
(Bilimsel Araştırma Projeleri Koordinasyon Birimi) under the Career Starter Project (Kariyer
Başlangıç Projesi) scheme, project code `FKB-2025-17608` ("Termal Dijital İkiz Tabanlı Sürü İHA
Sistemi ile Orman Yangınlarının Erken Tespiti ve Önlenmesi").

## Acknowledgments

The authors gratefully acknowledge the Çukurova University Scientific Research Projects Coordination
Unit for financial support of this research, and the Department of Computer Engineering at Çukurova
University for providing the laboratory environment and institutional support that made this work
possible.

## Competing interests

The authors declare no competing interests.

## Ethics approval

Not applicable. This study involved no human participants, animal subjects, or personally
identifiable data.

## Author contributions

Stated in CRediT terms. **Emrehan Metin:** Software, Data curation, Investigation, Validation,
Writing – review and editing. **Yunus Emre Cogurcu:** Conceptualization, Methodology, Formal
analysis, Investigation, Writing – original draft, Writing – review and editing, Supervision.

<!-- NEEDS AUTHOR INPUT: confirm the contribution split with the co-author before the manuscript is
uploaded. -->

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used Claude (Anthropic) in order to write and run
analysis and verification code against the frozen pipeline outputs, cross-check reported numbers
against those outputs, and draft and edit manuscript text. After using this tool, the authors
reviewed and edited the content as needed and take full responsibility for the content of the
publication.

<!-- NEEDS AUTHOR INPUT: Elsevier's policy (updated June 2026) places this section immediately before
the references and asks that AI use in the research process also be described in Methods. Confirm
the scope stated above with both authors. -->
