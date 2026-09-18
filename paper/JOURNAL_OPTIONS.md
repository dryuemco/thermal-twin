# Journal options: Q1, no APC paid by the authors (researched 2026-09-19)

Constraint from the authors: Q1, and no APC. Two routes satisfy it:
(a) a **hybrid** journal published on the subscription route (no APC), or
(b) a journal whose APC is paid by a TÜBİTAK EKUAL agreement that still has room.

## Sources and how each fact was checked

- Business model and APC of Elsevier titles: Elsevier `article-publishing-charge.xlsx`, prices as of 27-Aug-2026.
- Quartiles: SCImago full ranking download, 2025 edition (SJR). JCR quartiles are not freely
  downloadable; where they matter they are from secondary sources and marked as such.
- EKUAL: the IOP eligible-journal list and consortium page on publishingsupport.iopscience.iop.org (Çukurova
  listed; ERL in List D, unlimited); university library notices for Wiley and Springer Nature quotas.

## EKUAL state in September 2026

| Publisher | Covers | State |
|---|---|---|
| IOP | hybrid + gold, **unlimited**, 2026–2028 | open; Çukurova eligible; ERL covered (List D) |
| Wiley | hybrid + gold, WoS Q1/Q2, quota | **gold quota for 2026 exhausted (Aug 2026)**; hybrid free on the subscription route anyway |
| Springer Nature | quota, 2024–2026 | **2026 quota exhausted**; hybrid free on the subscription route anyway |
| Elsevier | — | **no agreement** |

## Shortlist

| # | Journal | Route | SJR 2025 | JCR (secondary) | Length | Fit |
|---|---|---|---|---|---|---|
| 1 | **Environmental Modelling & Software** | Elsevier hybrid, subscription | Q1 | Q1 | no limit for research papers found (4,000 is for invited opinion papers) | model evaluation and transferability is its core; same `elsarticle` template |
| 2 | **Remote Sensing of Environment** | Elsevier hybrid, subscription | Q1 | Q1 | no limit found | highest prestige; risk: the contribution is evaluation design, not a new RS method |
| 3 | **Agricultural and Forest Meteorology** | Elsevier hybrid, subscription | Q1 | Q1 | no body limit found; abstract ≤ 300 | fire and thermal dryness fit; transfer framing less central |
| 4 | **Environmental Research Letters** | IOP gold, APC paid by EKUAL | Q1 | Q1 | **Letters ≤ 4,000 words** (excl. abstract, figures, tables, refs) | broad, high visibility, free OA; needs a condensation from ~12.4k words |
| 5 | Global Ecology and Biogeography | Wiley hybrid, subscription | Q1 | Q1 | ~5,000 words, 6–8 display items | transferability yes, fire is peripheral |
| 6 | Landscape Ecology | Springer hybrid, subscription | Q1 | — | not checked | moderate |
| 7 | Forest Ecology and Management; Science of the Total Environment | Elsevier hybrid | Q1 | Q1 | not checked | moderate |

## Excluded, and why

- Ecological Informatics, Int. J. Applied Earth Obs. & Geoinf., Ecological Indicators, Science of Remote
  Sensing: Elsevier **Full Open Access**, APC compulsory, no Elsevier agreement.
- International Journal of Wildland Fire: **gold OA since 2024-01-01**, APC, no agreement with CSIRO.
- Fire Ecology (SpringerOpen): gold; Springer Nature 2026 quota exhausted.
- Ecography, Methods in Ecology and Evolution, Diversity and Distributions, Remote Sensing in Ecology and
  Conservation: gold; Wiley 2026 gold quota exhausted.
- Ecological Modelling: SJR Q1 but **JCR Q2** (IF 3.5, June 2026, secondary source).
- International Journal of Remote Sensing, Transactions in GIS: SJR Q2.

## If an Elsevier hybrid is chosen

The template, highlights rule (3–5 × ≤ 85 characters) and the generative-AI declaration carry over
unchanged. Remove the funding sentence claiming EKUAL APC cover. Check the abstract limit on the chosen
journal's guide (AFM: 300). The private-repository blocker in `SUBMISSION_CHECKLIST.md` still applies.

## EMS: ÜAK doçentlik value and review times (checked 2026-09-19)

**ÜAK, Tablo 9 Mühendislik Temel Alanı** (uak.gov.tr PDF, read in full):
- SCIE article, Q1 = 30 points; Q is the **Web of Science JIF quartile** (table footnote).
- Two-author article: *başlıca yazar* 0.8, second author 0.5. *Başlıca yazar* is defined as a sole author,
  or the candidate on an article written with **a graduate student the candidate supervises**. Where no
  başlıca yazar exists, the points are split equally. Author order does not decide this.
- So for Cogurcu on this two-author paper: 24 points if Metin is his supervised graduate student,
  otherwise 15. Only the first case counts towards the mandatory "başlıca yazar on at least one Q1–Q3
  article" condition (within the 40-point floor of item 1).
- The work must relate to the bilim alanı applied in; articles produced from the candidate's own
  graduate theses are scored under item 3 instead (20 points, capped at 20).
- Which JIF year counts (publication year vs latest) is stated only by secondary sources; check at application.

**EMS timing**, Elsevier's own Journal Insights (Wayback snapshot of 2024-04-16, medians):
review time 148 days; submission to acceptance 180 days; acceptance to online 5.5 days.
SciRev (author-reported, n = 9): first round 5.8 months, accepted total 7.0 months, desk rejection
34 days, 1.7 rounds. No current (2026) official figure was retrievable; ScienceDirect returns 403.
