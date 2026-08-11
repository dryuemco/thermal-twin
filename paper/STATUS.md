# Manuscript status — one-page overview

**Snapshot 2026-08-08** (after the figure/typography round, the figure renumbering, the caption
round and the literature sweep). Word counts are whole-file (incl. tables/notes). Marker counts
distinguish the document **body** from housekeeping mentions inside DRAFT-NOTES comment blocks
and file headers.

**Updated 2026-08-11** — ERA5-Land block (§3.17, §4.9, §5.7) and the Muğla two-event block
(§3.16.4, §4.8, §5.2 addition) added from hash-verified raw files; ERA5 validator executed
(27/27 PASS); §3.1 and §3.16.3 TO VERIFY markers closed from source; discussion renumbered
(§5.7 inserted, former §5.7–§5.10 → §5.8–§5.11); results gained §4.8 and §4.9 with
Tables R7–R10.
The Muğla 2021↔2022 transfer arms, which had never been run, were computed here with the pipeline
author's unmodified step9b/step9c — the only transfer directions in the paper not from his export.

**One-line state:** all eight figures, all captions and every citation decision are closed; the
manuscript is complete in draft and waits on four external inputs and one assembly pass.

## 1. Manuscript sections

| File | Status | Words | Open markers (body) |
|---|---|---|---|
| `00_abstract.md` | **draft complete** (trim to journal limit at submission) | 331 | none |
| `01_introduction.md` | **draft complete**; contributions filled with final numbers | 2 511 | none (1 UNVERIFIED mention is the header convention note) |
| `02_related_work.md` | **draft complete**; Dimarco §2.5 passage now confirmed against the full text (read by YEC 2026-08-08; 80/20 hold-out and NTL-log1p details added) | 5 267 | none — the Huang §2.4 marker was **closed 2026-08-08 by decision** (no coefficient quoted; §2.4 now says so explicitly, abstract suffices). *Correction: an earlier STATUS mislabelled this marker as Dimarco.* |
| `03_methods.md` | **draft complete** incl. §3.14–3.16; awaiting independent-description comparison | 9 388 | **1 TO VERIFY** (was 3): reproduction-check quote for the five-region set. **Closed 2026-08-11:** regions.py registry lines (repo pulled to 48b56e7; core.regions imported and queried, all Table 1 values match, caption line numbers corrected) and window-closure block edge length (2 cells ~1 km, read from source). Gained §3.16.4 (Muğla two-event design) and §3.17 (ERA5-Land diagnostic, validator 27/27 PASS). **Closed 2026-08-08:** Kozan inclusion (now in — §3.1 pointer, §3.3 negative-control paragraph, §4.1 result); §3.3 gate-verdict marker (§3.3 now points to §4.1, where Table R1 carries the numbers); repository URL/DOI (data-and-code availability statement written, GitHub URL, no DOI) |
| `04_results.md` | **draft complete, audited**; Tables 3–6 + R1–R10 | 6 697 | none. §4.8 (two Muğla events, Tables R7–R9) and §4.9 (ERA5, Table R10) added 2026-08-11; the §4.8 [PENDING] was closed by running the transfer arms. |
| `05_discussion.md` | **draft complete, audited**; renumbered 2026-08-11 (§5.7 inserted; former §5.7–§5.10 → §5.8–§5.11) | 6 383 | 1 TO VERIFY in body (§5.5 few-shot supplementary inclusion). §5.11(ii) now states the Muğla-2022 position from data rather than as a placeholder; an AoA per-pair number is conditional on a reviewer request (notes only) |
| `06_conclusions.md` | **draft complete** | 334 | none |
| `highlights.md` | **complete** (5 bullets, all ≤85 chars, verified) | 90 | none |
| `figure_captions.tex` | **complete** — Elsevier format, 8 captions in figure order, each self-contained (what is plotted, population, interval, meaning; panel letters explained inline). Every numeric value verified against the frozen outputs | 1 786 | none |
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

**Figure standard (applies to all eight).** Double column 190 mm, body 9 pt, minimum 8 pt,
vector PDF + SVG, Okabe-Ito, no red–green pair. Numbering is consecutive integers; lettered
sub-numbers are reserved for panels of one figure and are not used.

*Build-time verification.* `figures/_layout_check.py` runs inside every figure script and fails
the build on: text–text overlap or sub-threshold gap, text over a data artist, text leaving its
axes or the canvas, a legend leaving its own axes, a label overflowing its container box, or any
text below the minimum point size. All eight currently report **no problems**, minimum text gap
3.02–9.78 pt. Each script additionally asserts its own numbers against the frozen outputs; Fig. 2
asserts its 14 section references against the live `03_methods.md` heading list, and Fig. 7
asserts the monotone trade-off it depicts.

*Print safety.* Greyscale is measured, not assumed. Fig. 4 picks each cell label's colour by WCAG
contrast against that cell's rendered colour (worst case 4.7:1) and hatches below-chance cells,
because a diverging palette is symmetric in luminance and would otherwise lose the sign in
greyscale. Okabe-Ito blue vs orange measures only 2.30:1, so Figs 5 and 8 carry their two-class
distinction on line style as well as hue. Rendered greyscale proofs sit beside Figs 4, 5, 6, 7
and 8 (`*_greyscale.png`).

## 4. Process / historical documents

| File | Role |
|---|---|
| `POSITIONING.md` | authoritative direction document (thesis, C1–C5) — stable |
| `OUTLINE.md` | **stale in parts**: written pre-Evia/pre-Montiferru; §5 "missing before Results" is fully discharged; use only for figure/table budget and honesty constraints |
| `RESULTS_INVENTORY.md` | historical catalogue of the July partial export — superseded by drive_new numbers |
| `LITERATURE.md` | working literature notes; **swept twice on 2026-08-08**. First sweep closed A4/D2/Deep-CORAL/arXiv-2103.05898/Manavgat/Evia/Dimarco. Second sweep closed four of the five consolidated items by decision — GLO-30, Bejís event, Muğla candidate, Huang full text — each with its reasoning recorded. **One item remains open: WildfireGenome (arXiv preprint only; re-check for a peer-reviewed version before submission).** |
| `emrehan_mail.md`, `INTERN_REQUESTS.md` | historical correspondence — delivered |
| `STATUS.md` | this file |

## 5. Waiting on external input (coordinated by YEC)

1. **Emrehan's independent Methods narrative** — to be compared against §3.1–3.16; the ten
   candidate discrepancy points are pre-listed in 03_methods' METHODS ROUND NOTES.
2. **Few-shot × conditional-index joint analysis** — planned as supplementary; until decided,
   the §5.5 pointer stays [TO VERIFY]. Emrehan's existing curve: 3 regions, 6 directions.
3. ~~**Muğla 2022**~~ — **closed 2026-08-11.** Both frozen diagnostics arrived
   (`paper/mugla_temporal_raw/`, `paper/step9g_raw/`) and the transfer arms, which had never
   been run, were computed here with the pipeline author's unmodified step9b/step9c at 48b56e7
   in a shadow project root (`paper/mugla_transfer_raw/`). §3.16.4, §4.8 (Tables R7–R9) and the
   §5.2 addition are written from them; §5.11(ii) rewritten. **Note the provenance:** these are
   the only two transfer directions in the paper not produced by the pipeline author. The design
   is same-geography event-to-event, not clean temporal transfer (year × seasonal phase
   confounded; see §3.16.4).
4. ~~**Updated `repo/core/regions.py`**~~ — **closed 2026-08-11.** `repo/` is at `48b56e7`, which
   contains all five regions plus `mugla_2022_event_relative`; `core.regions` was imported and
   queried with `get_experiment()` and every Table 1 value matches. `repo/` is now wired into this
   repository as a git submodule pinned at that commit.
5. **Two ERA5-Land follow-ups for the pipeline author** (new 2026-08-11):
   (a) *Reproduction tolerances for the five-region set.* No `reproduction_check.json` exists
   anywhere in `drive_new`; §3.13 still quotes the historical two-region figures. This is the last
   TO VERIFY in `03_methods.md`.
   (b) *Manifest commit discrepancy.* `manifest.git_commit` is `a07ea33`, but the diagnostic
   source does not exist at that commit (first committed in `48b56e7`), so the production run used
   an uncommitted working tree. Every contract semantics string matches `48b56e7` verbatim and the
   validator passes, so the output is consistent with the described code, but bit-identity is not
   established. Recorded in §3.17 and `paper/era5_raw/SHA256SUMS.txt`; one question would close it.

   *Repository URL / DOI is no longer waiting:* **closed 2026-08-08** — the data-and-code
   availability statement now names Emrehan's public repository
   `https://github.com/emrehann17/satellite-thermal-digital-twin` (verified reachable
   unauthenticated, MIT licence) and states that **no DOI is minted**. No Zenodo deposit.

## 6. Remaining internal work (no external dependency)

Mechanical only — no analysis, no new numbers, no open judgement calls.

1. **Assembly round.** Merge the section files into one document; renumber the lettered
   R-tables (R1–R10) into the final sequence alongside Tables 3–6; drop the DRAFT-NOTES comment
   blocks; apply the journal template. Figure numbering is already final and consistent across
   `figure_captions.tex`, §4 and §5 — no figure work is left.
2. **Abstract trim** to the journal's word limit (currently 331 words).
3. **WildfireGenome re-check** — the single remaining literature item; confirm whether a
   peer-reviewed version has replaced the arXiv preprint, then cite whichever is current.
4. **Optional: graphical abstract** (Elsevier), from a Fig. 8 + Fig. 4 composite.

### Closed this round (kept for the audit trail)

- ~~Kozan inclusion decision~~ — **in**: §3.3 negative-control paragraph, §4.1 result, and shown
  on Fig. 1 in a deliberately distinct style.
- ~~Repository URL / archival DOI~~ — data-and-code availability statement written; public GitHub
  repository named, **no DOI, no Zenodo deposit**, stated explicitly.
- ~~GLO-30 DEM citation route~~ — verified rather than assumed (frozen `used_fallback: false`);
  cited by ESA product-page URL + access date; SRTM deliberately not cited.
- ~~Bejís / Muğla event sources~~ — left uncited after no citable event-specific source was
  found; extents and dates come from MCD64A1. `Cosandal2022` removed from the bibliography.
- ~~Huang et al. full text~~ — closed by decision; no coefficient of theirs is quoted and §2.4
  now says so. ~~Dimarco full text~~ — read by YEC, §2.5 confirmed.
- ~~§3.3 gate-verdict marker~~ — resolved by pointing §3.3 at §4.1, where Table R1 carries the
  per-region verdicts and fractions.
- ~~Figure typography, greyscale safety, captions, numbering~~ — all eight figures rebuilt to the
  standard in §3; `figure_captions.tex` written and number-checked against the frozen outputs.
