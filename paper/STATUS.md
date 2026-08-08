# Manuscript status — one-page overview

**Snapshot 2026-08-08** (after the figure round and the literature sweep). Word counts are
whole-file (incl. tables/notes). Marker counts distinguish the document **body** from
housekeeping mentions inside DRAFT-NOTES comment blocks and file headers.

## 1. Manuscript sections

| File | Status | Words | Open markers (body) |
|---|---|---|---|
| `00_abstract.md` | **draft complete** (trim to journal limit at submission) | 331 | none |
| `01_introduction.md` | **draft complete**; contributions filled with final numbers | 2 511 | none (1 UNVERIFIED mention is the header convention note) |
| `02_related_work.md` | **draft complete**; Dimarco §2.5 passage now confirmed against the full text (read by YEC 2026-08-08; 80/20 hold-out and NTL-log1p details added) | 5 260 | 1 TO VERIFY — **Huang et al. §2.4** (read full text before quoting any effect coefficient). *Correction: an earlier STATUS mislabelled this marker as Dimarco.* |
| `03_methods.md` | **draft complete** incl. §3.14–3.16; awaiting independent-description comparison | 7 192 | 6 TO VERIFY: regions.py registry lines; Kozan inclusion decision; §3.3 gate-verdict marker (numbers now in Table R1 — resolvable at assembly); reproduction-check quote; repository URL/DOI; window-closure block edge length |
| `04_results.md` | **draft complete, audited**; Tables 3–6 + R1–R6 | 5 179 | none (notes only) |
| `05_discussion.md` | **draft complete, audited** | 3 898 | 2 TO VERIFY: few-shot supplementary inclusion; §5.10 Muğla-2022 placeholder (a third, AoA per-pair number, is conditional on a reviewer request; notes only) |
| `06_conclusions.md` | **draft complete** | 334 | none |
| `highlights.md` | **complete** (5 bullets, all ≤85 chars, verified) | 90 | none |
| `REFERENCES.bib` | complete for all cited keys; 2026-08-08 sweep added Crossref-verified Sun2016 DOI, Soydan2022 (Manavgat event), Varela2022 (Evia event), Cosandal2022 (Muğla, weak-fit, flagged) | — | 2 UNVERIFIED remain: GLO-30 DEM (candidate DataCite DOI returned 404 — cite product page or SRTM fallback, decision open) and Bejís 2022 event description (no Crossref record exists — use EFFIS/regional report or omit) |

## 2. Analysis reports (frozen evidence base — all complete, no open markers)

| File | Words | Feeds |
|---|---|---|
| `regime_transfer_correlation.md` | 1 230 | §4.4, §5.6 |
| `conditional_similarity_transfer.md` (incl. 2026-08-08 scope correction) | 1 184 | §4.4–4.5, §5.4 |
| `loro_pooled_transfer.md` | 821 | §4.6a |
| `feature_drop_transfer.md` | 754 | §4.6b |
| `niche_overlap_transfer.md` | 843 | §4.4–4.5 |
| `niche_vs_conditional.md` | 790 | §4.4, §5.3 |
| `baseline_vs_thermal_transfer.md` | 672 | §4.3 Table R6, §5.1 |
| `all_diagnostics_vs_transfer.md` | 672 | Table 6 |
| `sklearn_version_sensitivity.md` | 364 | §4.7e, §3.13 |
| `signed_auc_bootstrap.md` | 1 135 | historical (3-region, partial export); superseded by the five-region feature-stability table but kept as independent validation |

## 3. Figures (`paper/figures/` — all built: vector PDF+SVG, provenance JSON, build-time asserts)

| Fig. | Content | Status |
|---|---|---|
| 1 | Study-region map (Natural Earth 1:50m, plain) | done |
| 2 | Methods schematic | done |
| 3+4 | Within-region increment + block robustness (combined, 3 panels) | done |
| 5 | Transfer matrices raw/z/CORAL (diverging, chance-centred) | done |
| 6 | Conservation: adaptation compression, LORO, feature drop | done |
| 7 | **Main figure** — contrast pairs with per-region CI-support arrowheads | done |

## 4. Process / historical documents

| File | Role |
|---|---|
| `POSITIONING.md` | authoritative direction document (thesis, C1–C5) — stable |
| `OUTLINE.md` | **stale in parts**: written pre-Evia/pre-Montiferru; §5 "missing before Results" is fully discharged; use only for figure/table budget and honesty constraints |
| `RESULTS_INVENTORY.md` | historical catalogue of the July partial export — superseded by drive_new numbers |
| `LITERATURE.md` | working literature notes; **swept 2026-08-08** — A4/D2/Deep-CORAL/arXiv-2103.05898/Manavgat/Evia/Dimarco closed; the 5 genuinely open items consolidated in one list ("Consolidated open verification items"): GLO-30, Bejís event, Muğla weak candidate, Huang full text, WildfireGenome preprint recheck |
| `emrehan_mail.md`, `INTERN_REQUESTS.md` | historical correspondence — delivered |
| `STATUS.md` | this file |

## 5. Waiting on external input (coordinated by YEC)

1. **Emrehan's independent Methods narrative** — to be compared against §3.1–3.16; the ten
   candidate discrepancy points are pre-listed in 03_methods' METHODS ROUND NOTES.
2. **Few-shot × conditional-index joint analysis** — planned as supplementary; until decided,
   the §5.5 pointer stays [TO VERIFY]. Emrehan's existing curve: 3 regions, 6 directions.
3. **Muğla 2022 temporal transfer** — in progress; on arrival a temporal-transfer subsection
   enters §4 and §5.10(ii) is rewritten.
4. **Repository URL / archival DOI + updated `repo/core/regions.py`** — resolves two §3 markers
   (data-and-code availability section also depends on this).

## 6. Remaining internal work (no external dependency)

- Assembly round: merge section files, final table/figure numbering (R-tables), resolve the
  §3.3 gate marker from Table R1, journal formatting.
- Read Huang et al. [@Huang2026] full text before quoting any effect coefficient (02 §2.4 /
  LITERATURE marker). ~~Dimarco full text~~ — done 2026-08-08 (read by YEC; §2.5 confirmed).
- Decide GLO-30 DEM citation route (product page vs SRTM fallback) and the Bejís event source
  (EFFIS/regional report vs omit); confirm Muğla weak candidate or replace.
- Optional: graphical abstract (Elsevier), from Fig. 7 + Fig. 5 composites.
