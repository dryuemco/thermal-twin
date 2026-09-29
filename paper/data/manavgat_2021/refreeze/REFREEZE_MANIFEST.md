# Manavgat re-freeze manifest

The re-freeze tree was built from the pipeline repository at commit 6381f4c (6381f4cd752d77a3069fcaa2364d10109b5adaf7), run unchanged. Manavgat's original label raster was exported on 2026-07-08; the month-boundary alignment fix of the MCD64A1 query is commit 183be42 of 2026-07-11. The label defect was therefore not a code defect at the time of this re-freeze: it was an export made before the fix and never renewed. The re-freeze chain (label, gate, step8a-8e, robustness, step9/step10 and the diagnostics) ran unchanged. Only the window-closure diagnostic carries a one-line patch (see code_patches), because its Step8A column contract predates the historical_burn_excluded column.

- Repo commit: `6381f4cd752d77a3069fcaa2364d10109b5adaf7`; label fix `183be42` (2026-07-11); original export 2026-07-08.
- GEE project: `thermaltwin` (runner override; infrastructure only).
- Environment: Python 3.12.10, scikit-learn 1.9.0, numpy 2.4.4, pandas 3.0.2 (Windows).
- Label: 803,797 positive pixels (624,130 added, all DOY 209–212); identical to the 2026-09-19 rebuild.
- Burned cells, TSG 784 → 2,935; all valid 796 → 3,046; none removed. Gate: wildfire_candidate_pass (burned_count 3046).
- step8a: 80 columns; extra `historical_burn_excluded` (all False). SHA-256 official `5a5e876cebc8c708c5650cd69095ddff2e160c4d7f410e777ffad616460541eb`, control `607a6359af6c6ba0378bfb11665f21c22c279ef71af7de4fb85c7515d4cda2e4`, frozen canonical `054a1961…`. The control hash differs from frozen only by that column; the official hash also differs by the label.
- Gate JSON: HEAD adds 48 QA fields; all 87 frozen fields reproduced by the control arm.
- Files hashed: 823 (`SHA256SUMS.txt`).
- Raw label raster SHA-256 `32d1d0d3fd9db568800f6447354269a8e299e6bd7a1e2c31678df0edc723dc25`: pixel- and profile-identical to the 2026-09-19 rebuild (`8940e706…`), different bytes.
- G1, control arm (frozen label) vs drive_new, tolerance 1e-5: step8b/8c/8d, robustness (big_blocks_v2, large_block, all_valid) and the five modern pair folders PASS (max 6.2e-6). Not PASS: step8e (9 text diffs, all `results_ran` file paths; numbers max 2.2e-16); large_block `input_audit` (72 diffs, all the column list shifted by the 80th column); legacy `manavgat_2021__evia_2021` (metrics 1.3e-5, bootstrap samples 1.2e-4, calibration bin counts ±1; same magnitude as the 2026-09-19 control, RF thread nondeterminism). Full record: `REFREEZE_MANIFEST.json` → `control_arm.g1`.
- G1 exceptions ACCEPTED by the user on 2026-09-23 (legacy pair: RF nondeterminism, same magnitude on 2026-09-19, outside the eight modern directions); tolerance not changed.
