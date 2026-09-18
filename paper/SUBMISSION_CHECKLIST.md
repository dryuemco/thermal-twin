# Environmental Modelling & Software — submission checklist (2026-09-19)

Retargeted from *Ecological Informatics* on 2026-09-19, because the authors will not pay an APC and
Ecological Informatics is Full Open Access (APC USD 3,190). Journal comparison: `JOURNAL_OPTIONS.md`.

## No APC: the evidence

| Check | Result | Source |
|---|---|---|
| Business model | **Hybrid Open Access**: subscription publication, OA optional at USD 3,570 | Elsevier `article-publishing-charge.xlsx`, prices as of 27-Aug-2026 |
| Indexed as OA journal? | No (`Open Access = No`) | SCImago 2025 ranking file |
| Announced move to full OA? | None found; Ecological Informatics' own announcement is findable, so the absence is informative | web search 2026-09-19 |
| Colour figures | "we will ensure that they appear in color online" — no charge stated | EMS guide for authors (Wayback 2026-03-25) |
| Page charges | none mentioned in the guide | same |

**At submission and again at acceptance, choose the subscription option, not open access.** Choosing
OA in the publishing agreement triggers the USD 3,570 APC. The subscription route still allows the
accepted manuscript to be shared under Elsevier's sharing policy.

## EMS requirements, and where the manuscript stands

Source: EMS guide for authors, Wayback copy of 2026-03-25 (ScienceDirect returns 403 to automated fetching).

| Requirement | Rule | Manuscript | Status |
|---|---|---|---|
| Article type | Research article | yes | OK |
| Abstract | ≤ 150 words | 146 | OK (cut from 238 on 2026-09-19) |
| Keywords | 1 to 7 | 6 | OK |
| Highlights | 3–5 bullets, ≤ 85 characters, separate file named "highlights" | 5 bullets, 68–75 chars | OK; #5 replaced 2026-09-19 |
| **Graphical abstract** | **required**, separate file, TIFF/EPS/PDF/Office | `figures/graphical_abstract.pdf` (+ .png, 1535×708 px) | **drafted; authors to approve** |
| Software and/or data availability section | name, developer, contact, year, hardware, software, language, size, availability, cost; "contact the author" not acceptable | added 2026-09-19 | OK, but see blocker 1 |
| Software available to reviewers | public, or password-protected download with the password given to the editors | analysis repo is private | **blocker 1** |
| Generative-AI declaration | before references | present | authors to confirm scope |
| Competing interests | Elsevier declaration tool, uploaded as .docx | statement in manuscript | **generate the .docx at submission** |
| References | Harvard (name, year) | `elsarticle-harv` | OK |
| Review model | single anonymised | author names on the PDF | OK |
| Source files | .tex accepted; PDF alone is not a source file | `manuscript.tex` | upload .tex + figures + .bib |

## Blockers before upload

1. **Analysis repository is private** (`dryuemco/thermal-twin`, no licence). Make a cleaned copy public
   with a licence, or give the editors a password-protected download. Authors' decision.
2. **Co-author approval** of the final text, including the new abstract, highlight #5 and the
   graphical abstract.
3. **Generative-AI declaration wording**, confirmed by both authors.
4. **Paper 2 also lists EMS as a target.** Decide before submitting either: ISPRS Journal of
   Photogrammetry and Remote Sensing (hybrid, Q1, no APC) is Paper 2's stated alternative.

## Resolved on 2026-09-19

- Funding sentence claiming EKUAL APC cover: removed (no APC is payable on the subscription route).
- Cover letter rewritten for EMS; the superseded one is in git history.
