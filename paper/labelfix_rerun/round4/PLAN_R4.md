# Label-fix re-run, round 4 — what is still to run, and the gates (2026-09-23)

Scope: everything whose output depends on the Manavgat label and was not re-run on 2026-09-19
(`paper/labelfix_rerun/CHANGES.md` §4 "Skipped", `pipeline/RUN_LOG.md` "Not run here").
Corrected parquet `e4ab8b85…` differs from frozen `054a1961…` only in `burned` and four `burn_*` columns;
predictors, populations and `valid_for_modeling` are identical (checked 2026-09-23).

## Gates (apply to every job; any failure = STOP and report, no workaround without the user's go)

- **G1 control reproduces.** The control arm (frozen label, tree `control/`, drive `Q:`) reproduces the frozen
  artefact (`drive_new/` or `paper/canonical_rerun/`) to ≤ 1e-5 in metrics (RF thread nondeterminism was
  ≤ 6.8e-6 on 09-19). Deterministic outputs: exact.
- **G2 only Manavgat moves.** In the corrected arm, every quantity that does not involve Manavgat equals the
  control arm (same tolerance).
- **G3 read-only trees untouched.** `repo/` and `drive_new/` path/size/mtime audit before and after: 0 diffs.
- **G4 no new code change.** Only the shims already documented (hash literals, ceiling reference, subst
  drives, lineage path rebase in `wc_driver.py`). Any new shim, schema workaround or design choice = STOP.
- **G5 sanity.** Corrected outputs are finite, AUCs in [0, 1], module validators PASS.
- **G6 registration inputs.** If any job changes a file that `thermal-twin-main/design/precision/` reads
  (`matrix_corrected.csv`, `transfer_ci_blocksize.csv`, large-block within-region), STOP: the
  pre-registration's precision analysis depends on it.

Scientific direction is **not** a gate: a corrected number that moves a verdict is recorded (as in
CHANGES.md §3), not treated as a failure. Gating on direction would be choosing results.

## Execution order: jobs needing no decision (run now, by hand, no delegation)

| # | Job | Check |
|---|---|---|
| N1 ✔ (G1 marginal, see REPORT) | Few-shot recovery, corrected then control (job 1) | G1 control vs drive_new; G2 Bej↔Muğ; validator PASS |
| N2 ✔ | Paper jobs 3–7 (round-3 slot-4 queue, unchanged wiring) | G2 per output vs `paper/canonical_rerun` (`_round4/g2_check.py`, negative-tested); run_d's own block-2 check |
| N3 ✔ | Marginal AoA (ran 09-19 in round 3, never compared) | G1 control vs drive_new; G2; explain the `aside/aoa_*_no_unweighted` set-asides |
| N4 ✔ | CORAL λ sweep (RUN_LOG: "bootstrap pending") | G1 control vs drive_new; G2 non-Manavgat directions |
| N5 ✔ | Round-3 loose ends: `aside/no_coord_channels_firstrun.json`; `referee2_numbers` prints "undefined" | explain; must match the frozen-control run's behaviour |
| N6 ✔ | G3 audit of `repo/` and `drive_new/` (snapshot taken 2026-09-23 in `_round4/`) | 0 diffs |
| N7 ✔ | Round-4 report `_round4/REPORT.md`: every job, gate result, frozen → corrected numbers | written; committing waits for the round3/ gitignore decision |

Added during the run and done: step8d ablation (Manavgat), feature_drop merge, transfer_delta_ci step9b check.
Results: `_round4/REPORT.md`.

Decision-bound (not started): 2 window closure, 8 Muğla subsampling, 9 Landsat A/B, 10 positive-matched,
12 commit of `round3/`.

## Jobs

| # | Job | Arm order | Status / blocker | Gate notes |
|---|---|---|---|---|
| 1 | Few-shot recovery (`fsr_driver.py`) | corrected, then control | done (N1) | G1 vs `drive_new/diagnostics/few_shot_recovery/7e4c…` (`recovery_curve.csv`, `repeat_metrics.csv`); validator PASS; G2 on Bej↔Muğ directions |
| 2 | Window closure, Manavgat (`wc_driver.py`) | — | **BLOCKED (G4).** repo HEAD step8a (48b56e7, 08-10) writes `historical_burn_excluded`; window_closure module (4eff201, 07-31) rejects the unknown column. Both arms fail identically → code-version mismatch, not the label. The frozen run's commit `734d621` is absent from the local repo history. | Needs a user decision (below) |
| 3 | `feature_drop` (paper) | control (froot, done), corrected | corrected output missing in `round3/` | G1 already met on froot? verify; then corrected |
| 4 | `distance_curve.py` | control, corrected | not run | G1 vs canonical_rerun |
| 5 | `verify_collar_increment.py`, `verify_diag_collar.py` | control, corrected | not run (inputs now exist in round3) | G1; collar increments must equal `ems_inference_ladder` §2.4 |
| 6 | `step10/run_d_within_robustness.py` | control, corrected | not run (needs corrected step8e) | its own block-2 hard check; G2 Bejís rows |
| 7 | `ems_inference_multiplicity` (diagnostic half), `ems_inference_units` / `_equivalence` (Q1), `transfer_delta_ci` step9b check | control, corrected | not run (B inputs now exist in round3) | G1 |
| 8 | Muğla subsampling (module) | control, corrected | **BLOCKED (G4)**: needs `cross_region/mugla_2021__manavgat_2021/step9b` which the module reads only under that pair name; corrected tree has the direction inside `manavgat_2021__mugla_2021/step9b` | Needs a staging decision (copy/link = new shim) |
| 9 | Landsat composite downstream A/B, then harmonization A/B (#3, #5 of the audit) | control, corrected | **BLOCKED (G4)**: MODIS attestation stores a Linux path and requires an exact string match; needs a merged tree (corrected labels + frozen step5–7d) | Then re-check #4/#6 gate status (`eligible_for_second_aoi_validation`) |
| 10 | Muğla positive-matched supplement (`paper/mugla_positive_matched`) | — | **DESIGN DECISION**: no producer script exists; `target_positives=784` hard-coded; 2,935 > Muğla's 2,911 → infeasible as specified | Re-specify or withdraw |
| 11 | Bookkeeping only (optional): domain_classifier_audit, residual seam, provenance hash audit | — | numbers unchanged by construction (features/populations identical); only stale n_burned/hashes | none needed |
| — | No re-run: landsat counterfactual, current-support harmonization numbers, window_closure_region, ERA5, Evia signed AUC | — | label-free or no Manavgat | — |
| 12 | Wrap-up | — | after 1–9 | update CHANGES.md / RUN_LOG.md; decide whether to commit `round3/` (gitignored in main at `.gitignore:85`) |

Order: 1 → 3–7 (no blocker, paper side) → 8/9 after decisions → 12.
