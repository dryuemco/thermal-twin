# Referee round 2 — computed numbers

Frozen extraction, 2026-08-14, produced by `paper/referee2_numbers.mjs`. Every input is a
frozen artefact under `drive_new/` or `paper/`. No model was fitted. Nothing under `repo/`,
`drive_new/` or any existing `step8*`/`step9*` output was modified. Seed 42.

---

## A. Interval on the mean paired thermal contribution

Input: `point_delta` for all 20 ordered directions in `paper/transfer_ci_blocksize.json`,
which is the paired thermal-minus-baseline raw transfer delta recomputed from the frozen
per-cell predictions.

Mean **0.00733**, SD 0.0682, range -0.1476 to 0.1325,
12 positive and 8 negative.

| Resampling unit | n | 95% interval |
|---|---|---|
| Directions (naive, ignores pairing) | 20 | [-0.0222, 0.0357] |
| Unordered pairs, cluster bootstrap | 10 | [-0.0225, 0.0371] |
| Unordered pairs, t on pair means | 10 | [-0.0285, 0.0431] |
| Regions, leave-one-out jackknife | 5 | [-0.0179, 0.0326] |

20000 replicates for the two bootstrap rows. Every interval spans zero, and the
point estimate is a small fraction of the width of each of them. The pair-cluster row is the
right primary quantity: the two directions of a pair share geography, data and, for the
paired delta, the same target prediction table.

Leave-one-region-out means:

| Region held out | directions remaining | mean delta |
|---|---|---|
| manavgat_2021 | 12 | 0.01480 |
| bejis_2022 | 12 | 0.00496 |
| mugla_2021 | 12 | 0.00719 |
| evia_2021_extended | 12 | 0.00100 |
| montiferru_2021 | 12 | 0.00869 |

---

## B. The conditional index at the design's own sample size

Input: `paper/conditional_similarity_transfer.json`, the 16 directions on which the
supported-feature agreement fraction is defined, and the published values in
`paper/diagnostics_common_subset.json`.

Recomputed 16-direction Spearman **0.5172** against the published
0.8404 (agreement to 3.2e-1).
The tie structure of the index caps the attainable value at **0.8620**, so the
observed statistic sits essentially on its own ceiling.

Pair level, which is the unit the published bootstrap resamples: 9 pairs,
Spearman **0.5196**, exact one-sided permutation
p = **0.0952** over 362,880 permutations.
A Bonferroni threshold over the 19 computed diagnostic variants is 2.63e-3,
so the result **does not clear** it.

| Interval construction | n | 95% interval |
|---|---|---|
| Published percentile bootstrap (8 pairs) | 8 | [0.5765, 0.8764] |
| Fisher z on the pair-level rho | 8 | [-0.2920, 0.8962] |
| Bonett-Wright on the pair-level rho | 8 | [-0.3435, 0.9069] |
| Fisher z treating 16 directions as independent | 16 | [0.0289, 0.8062] |

The published lower bound sits close to the bound obtained by treating all 16 directions as
independent, and the published upper bound sits below every analytic upper bound. Both are
symptoms of a statistic pinned near a combinatorial ceiling under heavy ties, not of
precision.

Index values across the 8 pairs:

| Pair | index | mean raw thermal AUC |
|---|---|---|
| bejis_2022 ~ manavgat_2021 | 0.000 | 0.3553 |
| manavgat_2021 ~ mugla_2021 | 0.000 | 0.3913 |
| evia_2021_extended ~ manavgat_2021 | 0.000 | 0.6654 |
| manavgat_2021 ~ montiferru_2021 | 0.000 | 0.4610 |
| bejis_2022 ~ mugla_2021 | 1.000 | 0.6008 |
| bejis_2022 ~ evia_2021_extended | 0.000 | 0.4154 |
| evia_2021_extended ~ mugla_2021 | 1.000 | 0.6151 |
| montiferru_2021 ~ mugla_2021 | 1.000 | 0.5753 |
| evia_2021_extended ~ montiferru_2021 | 1.000 | 0.6164 |

Distinct index values: 0.000, 1.000. Tie counts: 0.000 occurs 5 times; 1.000 occurs 4 times.

---

## C. Spatial-block counts per region

Input: the frozen per-cell transfer prediction tables, primary population, one file per
target region. Blocks are `row_500m // B` by `col_500m // B`, the manuscript's own
construction, with `row`/`col` read from `target_cell_id`.

| Region | cells | burned | B=2 total / positive | B=10 total / positive | B=20 total / positive |
|---|---|---|---|---|---|
| Manavgat | 20,511 | 2,935 | 5439 / 814 | 237 / 47 | 60 / 17 |
| Bejis | 15,190 | 1,100 | 3967 / 302 | 176 / 19 | 48 / 6 |
| Mugla | 41,730 | 2,911 | 11316 / 843 | 576 / 70 | 167 / 33 |
| Evia | 9,298 | 2,664 | 2566 / 716 | 155 / 41 | 50 / 15 |
| Montiferru | 2,544 | 539 | 743 / 192 | 35 / 16 | 12 / 6 |

The variance of an AUC is dominated by the minority class, so the positive-carrying count is
the number that matters for interval coverage.

---

## D. Step 8D thermal ablation, primary population

Input: `drive_new/experiments/<region>/step8d/step8d_ablation_delta_auc_by_population.csv`,
population `burnable_tree_shrub_grass`. This artefact is frozen, was produced by the pipeline
author, and is not currently cited anywhere in the manuscript.

| Region | full thermal block | best subset | its delta | share of the full block |
|---|---|---|---|---|
| Manavgat | missing step8d | | | |
| Bejis | 0.0561 | `fused_downscaled_group` | 0.0401 | 71% |
| Mugla | 0.1157 | `tvdi_group` | 0.0893 | 77% |
| Evia | 0.1533 | `lst_anomaly_group` | 0.1245 | 81% |
| Montiferru | 0.1014 | `tvdi_group` | 0.1004 | 99% |

---

## E. Step 7C downscaling validation and coordinate content

| Region | test RMSE (C) | test R2 | top input | coordinate importance sum |
|---|---|---|---|---|
| Manavgat | n/a | n/a | n/a | n/a |
| Bejis | 1.75 | 0.795 | `ndvi` 0.482 | 0.122 |
| Mugla | 1.65 | 0.956 | `slope` 0.777 | 0.035 |
| Evia | 1.80 | 0.866 | `modis_lst_mean_celsius` 0.593 | 0.097 |
| Montiferru | 1.83 | 0.909 | `ndvi` 0.666 | 0.066 |

Per-region MODIS input semantics, from `downscaling_model_metadata.json`:

- **Manavgat:** no note recorded
- **Bejis:** modis_lst_mean_celsius and modis_lst_std_celsius are single-season MODIS predictor-window summary layers for 2022-06-15 -> 2022-08-14; they are not multi-year baselines and not daily MODIS products.
- **Mugla:** modis_lst_mean_celsius and modis_lst_std_celsius are single-season MODIS predictor-window summary layers for 2021-06-01 -> 2021-07-28; they are not multi-year baselines and not daily MODIS products.
- **Evia:** modis_lst_mean_celsius and modis_lst_std_celsius are single-season MODIS predictor-window summary layers for 2021-06-05 -> 2021-08-02; they are not multi-year baselines and not daily MODIS products.
- **Montiferru:** modis_lst_mean_celsius and modis_lst_std_celsius are single-season MODIS predictor-window summary layers for 2021-05-25 -> 2021-07-23; they are not multi-year baselines and not daily MODIS products.

---

## F. Fused-LST gap fill, per region

Input: `drive_new/experiments/<region>/step7e/fused_lst_stats.json`. `fused_lst` equals the
observed Landsat LST wherever that is valid, so the gap-filled share is the only part of the
channel that is not `current_lst`.

| Region | observed coverage % | fused coverage % | gap-filled % of fused |
|---|---|---|---|
| Manavgat | 97.24 | 99.37 | 2.15 |
| Bejis | 90.30 | 100.00 | 9.70 |
| Mugla | 99.39 | 99.97 | 0.59 |
| Evia | 98.93 | 99.83 | 0.90 |
| Montiferru | 99.84 | 99.95 | 0.11 |

---

## G. Pre-label burn exclusion, per region

| Region | field present | exclusion ran | cells excluded |
|---|---|---|---|
| Manavgat | yes | **no** | 0 |
| Bejis | **no** | **not recorded** | n/a |
| Mugla | yes | yes | 49 |
| Evia | yes | yes | 16 |
| Montiferru | yes | yes | 61 |

