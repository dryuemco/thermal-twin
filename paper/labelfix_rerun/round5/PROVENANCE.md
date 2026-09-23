# Stage D (S4–S7) provenance, 2026-09-23

All inputs come from the Manavgat re-freeze.
- **Official tree:** `refreeze/manavgat_2021`, repo 6381f4c unchanged, corrected label.
- **Control tree:** `refreeze/_control_frozenlabel`, frozen label.
- Their manifests are on main in `paper/data/manavgat_2021/refreeze/`.
- The environment is `.venv-step10` (sklearn 1.9.0, numpy 2.4.4, pandas 3.0.2), seed 42.
- No model is refitted in S4b, S5, S6 or S7. The only model fits of stage D are the marginal AoA
  completion (both trees, round-3 driver).

| Analysis | Script / producer | Inputs | Outputs | Checks |
|---|---|---|---|---|
| S4a | `s4a.py` | Step9G `step9g_univariate_auc_by_region.csv` (10-cell bootstrap), both trees; `refreeze/_runners/matrix8_*.csv`; `matrix.py` (09-19) on both trees | `s4a_signed_auc_long.csv`, `s4a_outlier_by_feature.csv`, `s4a_source_target_means.csv`, `s4a_summary.json`, `matrix20_{official,frozen}.csv` | The other four regions are identical across arms (max 0). The official 20-direction matrix equals the 09-19 scratch run (max 0). |
| S4b | `s4b.py` (EXPLORATORY) | Official step8a + frozen drive_new step8a (phase split); official step9b predictions; `src.step9c_cross_region_block_bootstrap.bootstrap_one_group` (pipeline's own, 1000 reps, seed 42) | `s4b_phase_transfer_auc.csv`, `s4b_phase_univariate_auc.csv`, `s4b_meta.json` | "all" transfer AUCs equal official step9b to 6 dp; "all" univariate AUCs equal official Step9G. Subsets: 2,151 / 784 / 17,576 as expected. |
| S5 | round-3 `baseline_vs_thermal.mjs`, `transfer_ci_blocksize.mjs` (unchanged) on overlays `ov_official`, `ov_control`; then `s5.py` | step9b/9c/10 of both trees | `out_*/baseline_vs_thermal_transfer.*`, `out_*/transfer_ci_blocksize.*`, `s5_paired_delta_20.csv`, `s5_manavgat_8.md`, `s5_summary.json` | Official = round-3 corrected (exact); G2 12 non-Manavgat rows exact. Control = published R6 and frozen arm, except one 4-dp rounding flip (Bej→Man delta_ci_low −0.00045; unrounded diff ~1e-6, verdict equal). 10-cell unrounded max 1.4e-6, verdicts equal. |
| S6 | marginal AoA (`refreeze/_runners/aoa_driver.py`, strict_hashes False, see its header); round-3 chain `run_s6_chain.sh` (burned_components → conditional_similarity → build_comparison_inputs → regime_correlation → niche_corr → niche_vs_conditional → diagnostics_common_subset); `s6.py` | AoA ids: official `6d998eb5…`, control `715872ac…`. Copied label-free inputs: marginal_area_of_applicability, domain_classifier_audit. niche_measures: 09-19 corrected (from a parquet value-identical to the official 79 columns) and frozen | `out_*/all_diagnostics_vs_transfer.csv` etc., `s6_diagnostics_20.{csv,md}` | AoA: control = drive_new (G1), official = 09-19 corrected. All 7 aggregator tables: control = 09-19 frozen arm exact; official = round-3 corrected exact. The control arm uses `code_control/` = round-3 code with its three "ROUND3 ASSERT CHANGE" values restored to the frozen ones (4, 4; setB 16). |
| S7 | `s7.py` | `out_*/figure_contrast_pairs.json`, `transfer_ci_blocksize.json`, `niche_overlap_transfer.json` | `s7_contrast_pair.json` | Matches the S2 preliminary values. |

`vector_spearman_supported` is one of the 20 pre-fixed candidates, so it STAYS IN the S6 table, flagged ‡: 6 directions,
degenerate interval, not interpreted, not comparable with the other 19. This reverses the user's earlier instruction
to drop it: removing a fixed candidate after seeing its result would be a forking path in the other direction.
S4b is exploratory: one region, one event, not a registered diagnostic; it is a mechanism proposal, not
evidence.
