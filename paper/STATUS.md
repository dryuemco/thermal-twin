# Manuscript status — one-page overview

**Snapshot 2026-08-08** (after the figure round and the literature sweep). Word counts are
whole-file (incl. tables/notes). Marker counts distinguish the document **body** from
housekeeping mentions inside DRAFT-NOTES comment blocks and file headers.

## 1. Manuscript sections

| File | Status | Words | Open markers (body) |
|---|---|---|---|
| `00_abstract.md` | **draft complete** (trim to journal limit at submission) | 331 | none |
| `01_introduction.md` | **draft complete**; contributions filled with final numbers | 2 511 | none (1 UNVERIFIED mention is the header convention note) |
| `02_related_work.md` | **draft complete**; Dimarco §2.5 passage now confirmed against the full text (read by YEC 2026-08-08; 80/20 hold-out and NTL-log1p details added) | 5 262 | none — the Huang §2.4 marker was **closed 2026-08-08 by decision** (no coefficient quoted; §2.4 now says so explicitly, abstract suffices). *Correction: an earlier STATUS mislabelled this marker as Dimarco.* |
| `03_methods.md` | **draft complete** incl. §3.14–3.16; awaiting independent-description comparison | 7 460 | 3 TO VERIFY: regions.py registry lines; reproduction-check quote; window-closure block edge length. **Closed 2026-08-08:** Kozan inclusion (now in — §3.1 pointer, §3.3 negative-control paragraph, §4.1 result); §3.3 gate-verdict marker (§3.3 now points to §4.1, where Table R1 carries the numbers); repository URL/DOI (data-and-code availability statement written, GitHub URL, no DOI) |
| `04_results.md` | **draft complete, audited**; Tables 3–6 + R1–R6 | 5 179 | none (notes only) |
| `05_discussion.md` | **draft complete, audited** | 3 898 | 2 TO VERIFY: few-shot supplementary inclusion; §5.10 Muğla-2022 placeholder (a third, AoA per-pair number, is conditional on a reviewer request; notes only) |
| `06_conclusions.md` | **draft complete** | 334 | none |
| `highlights.md` | **complete** (5 bullets, all ≤85 chars, verified) | 90 | none |
| `REFERENCES.bib` | complete for all cited keys; 2026-08-08 sweep added Crossref-verified Sun2016 DOI, Soydan2022 (Manavgat event), Varela2022 (Evia event); **second round 2026-08-08 removed Cosandal2022** (Muğla weak-fit, never cited) | — | **none.** GLO-30 closed (cited inline by product-page URL + access date, no DOI, no bib entry; GLO-30 confirmed as the DEM that ran). Bejís and Muğla event descriptions closed as deliberately uncited — no citable event-specific source exists, numbers come from MCD64A1 |

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

| Fig. | Content | File | Status |
|---|---|---|---|
| 1 | Study-region map + Kozan gate control (Natural Earth 1:50m, plain) | `fig1_study_map` | done |
| 2 | Methods schematic (gate branch, §3.12 decomposition, footer) | `fig2_schematic` | done |
| 3 | Within-region increment + block robustness (3 panels) | `fig3_within_robustness` | done |
| 4 | Transfer matrices raw/z/CORAL (diverging, chance-centred, below-chance hatched) | `fig4_transfer_matrix` | done |
| 5 | Label-blind adaptation compresses toward chance (12 directions) | `fig5_adaptation` | done |
| 6 | LORO pooling never beats the best single source | `fig6_loro` | done |
| 7 | Feature removal is a zero-sum trade-off | `fig7_feature_drop` | done |
| 8 | **Main figure** — contrast pairs with per-region CI-support arrowheads | `fig8_contrast_pairs` | done |

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
4. **Updated `repo/core/regions.py`** — resolves the §3.1 registry-line marker (the working copy
   predates the `evia_2021_extended` and `montiferru_2021` entries).
   *Repository URL / DOI is no longer waiting:* **closed 2026-08-08** — the data-and-code
   availability statement now names Emrehan's public repository
   `https://github.com/emrehann17/satellite-thermal-digital-twin` (verified reachable
   unauthenticated, MIT licence) and states that **no DOI is minted**. No Zenodo deposit.

## 6. Remaining internal work (no external dependency)

- Assembly round: merge section files, final table/figure numbering (R-tables), resolve the
  §3.3 gate marker from Table R1, journal formatting.
- ~~Read Huang et al. [@Huang2026] full text~~ — **closed 2026-08-08 by decision**: no coefficient
  is quoted, §2.4 says so explicitly, abstract suffices. ~~Dimarco full text~~ — done 2026-08-08
  (read by YEC; §2.5 confirmed).
- ~~Decide GLO-30 DEM citation route, Bejís event source, Muğla candidate~~ — **all closed
  2026-08-08**: GLO-30 confirmed as the DEM that actually ran (`used_fallback: false` in frozen
  step2b metadata) and cited by product-page URL + access date, no DOI, no SRTM citation; Bejís
  and Muğla event descriptions left uncited, numbers from MCD64A1; `Cosandal2022` removed from the
  bib.
- Optional: graphical abstract (Elsevier), from Fig. 8 + Fig. 4 composites.
