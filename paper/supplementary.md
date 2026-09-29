# Supplementary Material

Supplementary material for *Evaluation area and the limits of cross-region transfer of pre-fire thermal wildfire models: five large Mediterranean fires*.

Section S1 gives the sensitivity analyses and the details behind the Results. Section S2 gives the
supporting tables, Section S3 the protocol details and limitations, Section S4 the target-label
recovery curve, Section S5 the code and Section S6 the data. Tables are numbered S1 to S35,
independently of the sections. Supplementary equations are numbered (S1), (S2) and so on. Every value
is read from a released output, named by its path in the repository
<https://github.com/dryuemco/thermal-twin>. Paths that begin with `paper/labelfix_rerun/` hold the
corrected-label outputs. Values computed under the original Manavgat label are marked "original
label".

## Contents

- S1 Sensitivity analyses and detail
  - S1.1 Evia AOI and prevalence
  - S1.2 CORAL regularisation
  - S1.3 Blocking scale
  - S1.4 Predictor-window closure
  - S1.5 Quality screening of the coarse thermal input
  - S1.6 Normalised against absolute dryness channels
  - S1.7 The coordinate-informed channels
  - S1.8 Model capacity
  - S1.9 The four evaluations of Section 4.3, in full
  - S1.10 The transfer-gap decomposition, in full
  - S1.11 The thermal sign, stratified
  - S1.12 The LST anomaly under the difference instrument
  - S1.13 The same-geography event pair
  - S1.14 The two interventions, in full
  - S1.15 Signed associations on both frames
  - S1.16 The contrast pair, in full
  - S1.17 The sensitivity arms, summarised
  - S1.18 Distance within a region
  - S1.19 The frame test, elaborated
  - S1.20 The transfer matrix and adaptation, elaborated
  - S1.21 The similarity diagnostics
  - S1.22 Additional robustness analyses
  - S1.23 Analyses added after the pre-submission review
- S2 Supporting tables
- S3 Protocol detail and limitations
- S4 Target-label recovery curve
- S5 Code
- S6 Data

# S1 Sensitivity analyses and detail

Each analysis below changes one design choice and keeps everything else fixed. None changes a
conclusion of the main text. Section S1.6 is different: it tests a claim of the introduction, and
the claim is not supported.

## S1.1 Evia AOI and prevalence

The raw transfer analyses between Evia and Bejís, Manavgat and Muğla were repeated with the
earlier, high-prevalence Evia rectangle. No qualitative conclusion changed. Thermal raw transfer AUCs
moved by up to 0.134. The largest change was Evia to Manavgat, at 0.543 with the earlier rectangle
against 0.677 with the extended one. No direction changed side of the chance line
(`paper/labelfix_rerun/round7/r7f_evia_legacy.csv`). On the earlier rectangle the natural-vegetation
population is smaller, and its burned prevalence is higher than on the extended rectangle (0.287;
Table S15).

## S1.2 CORAL regularisation

Nine λ values from 0 to 10⁻¹ were tested on four directions (Bejís and Muğla, and Manavgat and
Muğla, both ways). CORAL transfer AUC moved by at most 0.014 within any direction and model, and by at
most 0.009 for the thermal model
(`paper/labelfix_rerun/exports/coral_lambda_sensitivity_b74d643e/metrics.csv`). λ was not selected on
performance.

The Manavgat and Bejís pair is not in this sweep. Under the original label, the adapted result of
this pair depended on λ. It was therefore tested separately at λ = 10⁻⁵, 10⁻³ and 10⁻¹
(`paper/labelfix_rerun/step10/coral_lambda_sensitivity.csv`). Bejís to Manavgat gives 0.408 [0.389,
0.427], 0.410 and 0.367, which are below chance at every λ. Manavgat to Bejís gives 0.470 [0.444,
0.494], 0.474 and 0.466. No adapted direction of this pair has an interval above chance at any λ, so
no conclusion depends on the choice of λ in this range.

## S1.3 Blocking scale

The transfer intervals were recomputed at 10-cell (≈5 km) blocking from the re-frozen per-cell
predictions. The intervals became wider. The paired-delta verdicts changed from twelve positive,
seven negative and one uncertain at 1 km to six, five and nine at 5 km. Coarser blocking therefore
removed support from eight verdicts and added none. Across five bootstrap seeds, the 5 km counts were
5 to 6 positive, 4 to 5 negative and 9 to 11 uncertain, so they are not exact
(`paper/labelfix_rerun/round5/out_official/transfer_ci_blocksize.csv`,
`paper/labelfix_rerun/round6/seed_stability.json`).

The point estimates do not change, because the block size only sets the bootstrap resampling unit.
Each point estimate is computed once over all target cells. Every verdict that changed moved to "no
verdict", and no direction crossed the chance line. The counts of supported directions are therefore
the least stable numbers in this paper.

**Table 1 note (resampling units).** The bootstrap resamples spatial blocks, so the reliability of
an interval depends on the number of blocks with at least one burned cell. This number falls from
192 to 843 at 2 cells to **6 to 33** at 20 cells. An interval built on six such blocks has no useful
coverage, so **the 20-cell row should be read as indicative**. The 10-cell row is the coarsest
blocking that this design supports. There, every region has 16 to 70 blocks with burned cells, and
the gain holds in all five regions.

## S1.4 Predictor-window closure

The predictor window was closed 7 and 14 days earlier in all five regions. The thermal
contribution stayed positive, with bootstrap support, everywhere. The direction of the change
differed between regions. In Manavgat, on the corrected label, it was +0.065 [+0.059, +0.072] at the
standard window, +0.082 [+0.075, +0.090] at 7 days and +0.058 [+0.051, +0.065] at 14 days, all on the
common cohort of that analysis (`paper/labelfix_rerun/exports/window_closure_manavgat_2021/`). It
became stronger in Bejís, from 0.058 to 0.079 at 14 days, and in Muğla, from 0.115 to 0.128. It was
flat in Montiferru. It became weaker in Evia, from 0.156 to 0.149 to 0.135. The four regions other
than Manavgat are not affected by the label correction
(`paper/labelfix_rerun/exports/window_closure_<region>/tables/thermal_contributions.csv`). The gain
therefore survives in every region, but it does not always improve.

## S1.5 Quality screening of the coarse thermal input

The MODIS inputs were quality-screened in two regions and not in the other three. This split
follows the export date, not the design. It causes a change at the input that is correlated with
elevation (r = +0.615 in Manavgat). The Manavgat chain was therefore rebuilt from a quality-screened
input on the corrected label and compared with the unscreened version. The current pipeline step7
refuses the unscreened raster, because the raster has no nodata tag and 8.1 % exact zeros. The
unscreened version therefore uses the step7 of export time, and the screened version uses the current
one. The two versions differ in code as well as in screening. The result did not change. Elevation
stayed at 0.232, no other signed AUC moved by more than 0.005 (downscaled LST, −0.0044), and the
within-region gain moved from +0.067 to +0.068
(`paper/labelfix_rerun/round6/qc/qc_compare_manavgat_corrected.json`; Section S3.5(xii)). Elevation
comes from the DEM and is not affected by the screening. The MODIS-based surface is used for only
2.14 percentage points of coverage. The Muğla input was not re-examined.

## S1.6 Normalised against absolute dryness channels

Section 1.2 states that an internally normalised index should be less affected than raw land
surface temperature by temperature differences between regions. The thermal set contains both kinds
of channels, so this was tested directly by comparing feature sets.

In the two Muğla fires (Section S1.13), the normalised channels keep their direction and the absolute
channels do not. This holds for one region across two fires. It does not hold across regions:
`lst_anomaly_mean` is one of the predictors with a bootstrap-supported reversal on the original study
areas (Table S10). For this reason, Section S1.14 removes it together with elevation. On this
evidence, normalisation protects a channel against a difference between two seasons in one place,
but not against a change of place.

Three feature sets were run over all twenty directions and all five within-region folds. The
classifier, population, folds and bootstrap were kept fixed. The code stops unless its reference
configuration reproduces the re-frozen exports, and it does: the largest absolute difference from the
step9b transfer AUCs is 0.000000 across all twenty directions. Sources for this section and the next
two: `paper/labelfix_rerun/round3/no_coord_channels.json` and
`paper/labelfix_rerun/code/model_capacity.json`, summarised by
`paper/labelfix_rerun/round7/r7e_supplement_tables.py`.

**Table S23. Feature-set arms.** Mean over the twenty transfer directions and the five regions.

| Feature set | Mean transfer AUC | Directions > 0.5 | Mean within-region AUC |
|---|---:|---:|---:|
| Baseline only | 0.519 | 13 | 0.797 |
| Baseline + normalised anomalies | 0.524 | 14 | 0.862 |
| Baseline + absolute surface state | 0.531 | 13 | 0.864 |
| All ten features (reference) | 0.527 | 13 | 0.896 |

**The expected advantage was not found.** Per direction, the normalised set minus the absolute set
has a mean of −0.006. The difference is positive in 11 of 20 directions and ranges from −0.099 to
+0.087, so the spread is much larger than the mean difference. Within regions the two sets are almost
equal, at 0.862 and 0.864. Each recovers most of the gap between the baseline (0.797) and the full
model (0.896). The comparison uses two parts of one thermal set on one cohort. It does not test
normalised dryness indices in general.

## S1.7 The coordinate-informed channels

`downscaled_lst_mean` and `fused_lst_mean` come from a per-region downscaling model that uses
coordinates as inputs (Section S3.4). This is the only way in which coordinate information enters
the feature set. A surface smoothed by coordinates is informative locally and does not transfer. If
the within-region gain depended on it, the gain would be caused by the smoothing and not by the
thermal state. Both channels were therefore removed, and all models were refitted over all twenty
directions and all five within-region folds.

**Table S24. The within-region increment without the two coordinate-informed channels.**

| Region | Increment, full set | Without the two channels | Retained |
|---|---:|---:|---:|
| Manavgat 2021 | +0.067 | +0.064 | 95 % |
| Bejís 2022 | +0.056 | +0.046 | 82 % |
| Muğla 2021 | +0.116 | +0.097 | 84 % |
| North Evia 2021 | +0.153 | +0.145 | 94 % |
| Montiferru 2021 | +0.101 | +0.105 | 103 % |
| **Mean** | **+0.099** | **+0.091** | **92 %** |

**The gain does not depend on these channels.** It stays positive in every region and keeps 82 %
to 103 % of its size. Mean transfer also does not change: 0.528 without the two channels, 0.527 with
them, and 0.519 for the baseline alone.

## S1.8 Model capacity

All numbers in the paper come from one random forest with unlimited depth and
`min_samples_leaf = 3`. This configuration fits local structure well and extrapolates poorly. Three
other estimators were therefore run over the same twenty directions and five within-region folds.

**Table S25. Four estimators, within region and in transfer.**

| Estimator | Within-region AUC | Within increment | Transfer AUC | Transfer increment | Above chance |
|---|---:|---:|---:|---:|---:|
| Random forest, depth unlimited, leaf 3 | 0.896 | +0.099 | 0.527 | +0.007 | 13 of 20 |
| Random forest, depth 6, leaf 50 | 0.838 | +0.053 | 0.527 | −0.011 | 13 of 20 |
| Random forest, leaf 200 | 0.814 | +0.046 | 0.522 | −0.019 | 13 of 20 |
| Penalised logistic regression | 0.759 | +0.046 | 0.481 | −0.021 | 11 of 20 |

**Regularisation does not improve transfer.** The four estimators range from 0.481 to 0.527, with
eleven to thirteen of twenty directions above chance. The linear model, which is designed to
extrapolate, transfers worst. Within-region skill falls from 0.896 to 0.759 as capacity is reduced,
but transfer does not rise. The thermal contribution to transfer is +0.007 for the standard forest
and negative for all three alternatives. The estimators are not ranked, because only point estimates
are available.

## S1.9 The four evaluations of Section 4.3, in full

Section 4.3 reports four evaluations of the same models (main-text Table 2). The values per scar,
the controls and the thermal gain per scar are given here.

**Table S1. The four evaluations, per scar.** Natural-vegetation population, 5 km blocking,
2 km collar. Bejís and Manavgat have no row C, because each has only one burned area, and
withholding it leaves nothing to train on. Source `paper/labelfix_rerun/code/matched_holdout.json`.

| Region | Scar | Cells | Burned fraction | A whole region | B scar area | C scar withheld | D foreign |
|---|---:|---:|---:|---:|---:|---:|---:|
| Manavgat 2021 | 1 | 3,965 | 0.74 | 0.882 | 0.743 | n/a | 0.542 |
| Bejís 2022 | 1 | 1,657 | 0.66 | 0.824 | 0.575 | n/a | 0.589 |
| Muğla 2021 | 6 | 1,266 | 0.72 | 0.777 | 0.564 | 0.595 | 0.571 |
| Muğla 2021 | 1 | 1,244 | 0.59 | 0.777 | 0.654 | 0.561 | 0.514 |
| Muğla 2021 | 10 | 940 | 0.68 | 0.777 | 0.674 | 0.617 | 0.634 |
| Muğla 2021 | 8 | 954 | 0.57 | 0.777 | 0.761 | 0.542 | 0.623 |
| North Evia 2021 | 1 | 3,059 | 0.87 | 0.864 | 0.745 | 0.465 | 0.564 |
| Montiferru 2021 | 1 | 758 | 0.58 | 0.720 | 0.622 | 0.584 | 0.489 |
| Montiferru 2021 | 5 | 195 | 0.34 | 0.720 | 0.461 | 0.458 | 0.475 |

### S1.9.1 The pool controls

The same predictions were scored on a random sample of region cells with the burned fraction of
the scar area. Over nine scars this gives 0.793, against 0.791 for the whole region. Matching the
prevalence therefore changes nothing (−0.002 [−0.005, +0.001]). This is expected, because ROC-AUC
does not depend on class balance, so it is a check of the code. Scoring the predictions on the scar
area gives 0.644, a fall of **+0.149 [+0.087, +0.211]** from the prevalence-matched score. This
replaces both the burned and the unburned cells, so each group was also replaced alone. The cost is
always the prevalence-matched score minus the new score. Replacing only the unburned cells costs
**0.139 [0.098, 0.181]** (0.046 to 0.250 per scar). Replacing only the burned cells costs **−0.002
[−0.055, +0.051]** on average (−0.121 to +0.137 per scar). The cost therefore comes from the unburned
cells. All unburned cells in a scar collar are next to the fire and share its terrain, land cover and
weather. The unburned cells of a whole region also include easy distant cells
(`paper/labelfix_rerun/code/pool_decomposition.json`, `prevalence_control.json`).

### S1.9.2 The seven scars and the resampling unit

Rows A to D of Table 2 are means over the **same seven scars**: four in Muğla, two in Montiferru
and one in Evia. Under the corrected label, the 2,151 added Manavgat burned cells join its one
existing scar (2,934 of 2,935 cells). For this reason the controls above use nine scars and report
0.791 and 0.644, against 0.773 and 0.640 in Table 2. The intervals are Student *t* intervals over the
scars. **Row A is a region-level value that is repeated for each scar of a region, so its interval is
too narrow and should not be read as coverage.** The same applies to A − B and A − C. With the region
as the unit, A − B is **+0.137 [+0.048, +0.226]** over three regions and **+0.160 [+0.090, +0.230]**
over all nine scars in five regions (`paper/labelfix_rerun/round7/round7_summary.json`). A − C with
the region as the unit is +0.266 [−0.022, +0.553]. This interval is 3.6 times wider than the
scar-level interval and includes zero. **With the region as the unit, only the frame cost is
established.**

The scar definition does not drive the result. Over a range of minimum scar sizes and buffers, row C
ranges from 0.541 to 0.561 on nine to six scars. Its means at 2, 5 and 10 km buffers are 0.546 (seven
scars), 0.533 (seven) and 0.548 (six) (`paper/labelfix_rerun/code/scar_definition_sweep.csv`,
`scar_control.json`). For single scars, row D varies strongly between sources (Table S4), but little
after averaging. Row D uses 28 of the 36 source and scar combinations, and nine of them are below
chance.

### S1.9.3 Controls and the thermal-increment ladder, full specification

Three controls reuse the predictions of row A. Each is averaged over 20 draws without replacement.
The **prevalence-matched** control draws $`|H_K^{+}|`$ cells from $`P_R`$ and $`|H_K^{-}|`$ cells from
$`V_R \setminus P_R`$. The **negative-pool** control keeps the drawn burned cells but uses the
unburned cells of the scar, $`H_K^{-}`$. The positive-pool control does the opposite. A
**within-region half-split** completes the set: the modelled cells are cut at the median of a grid
axis, in both axes and both directions, and the transfer protocol of Section 3.8 is applied. A split
is dropped when one half has only one class. The numbers of burned cells in the two halves are
unequal (Table S2).

The **thermal gain** is evaluated with rows A to D on the seven scars of Table 2. Table S26 gives the
values per scar at both block sizes. Over the seven scars, the region-wide gain is +0.095 at 5 km
blocking and +0.117 at 1 km. On the scar area, the same predictions give +0.021 and +0.056.
Leave-one-scar-out gives +0.024, and a foreign-region model +0.008, at both block sizes. Blocked minus
leave-one-scar-out is −0.004 [−0.070, +0.063] at 5 km and +0.031 [−0.027, +0.090] at 1 km. Region-wide
minus scar area at 5 km is +0.074 [−0.009, +0.157] at scar level. With only three regions, no
reliable region-level interval can be given for this difference. The within-region half-split gives +0.028, positive in 13 of 18 splits
(`paper/labelfix_rerun/inference/ladder_summary.json`, `paper/labelfix_rerun/code/positive_control.json`).

**Table S26. The thermal gain by scar: region-wide, on the scar area, withheld and foreign.**
Thermal minus baseline ROC-AUC. Region-wide and scar-area values at 5 km blocking, with 1 km in
brackets. Leave-one-scar-out and foreign values do not depend on the blocking.

| Region | Scar | Region-wide | Scar frame, same blocked model | Scar withheld | Foreign |
|---|---:|---:|---:|---:|---:|
| Muğla 2021 | 6 | +0.079 (+0.116) | −0.016 (+0.018) | +0.025 | +0.033 |
| Muğla 2021 | 1 | +0.079 (+0.116) | +0.049 (+0.071) | −0.044 | +0.014 |
| Muğla 2021 | 10 | +0.079 (+0.116) | +0.063 (+0.107) | +0.045 | +0.042 |
| Muğla 2021 | 8 | +0.079 (+0.116) | +0.083 (+0.092) | +0.012 | +0.037 |
| North Evia 2021 | 1 | +0.148 (+0.153) | +0.060 (+0.065) | +0.143 | −0.038 |
| Montiferru 2021 | 1 | +0.100 (+0.101) | +0.066 (+0.086) | +0.060 | −0.008 |
| Montiferru 2021 | 5 | +0.100 (+0.101) | −0.160 (−0.049) | −0.070 | −0.023 |
| **Mean** | | **+0.095 (+0.117)** | **+0.021 (+0.056)** | **+0.024** | **+0.008** |

**Table S2. Within-region half-split, every split.** The numbers of burned cells in the source and
target halves are given because they are unequal. This is the main limit of this analysis, because a
straight cut does not give two comparable halves. Two splits cannot be used, because one half of
Manavgat has no burned cells. Source `paper/labelfix_rerun/code/positive_control.json`; checked row by
row by `paper/code/appendix_tables.py`.

| Region | Axis | Direction | Source positives | Target positives | Thermal AUC | Baseline AUC |
|---|---|---|---:|---:|---:|---:|
| manavgat 2021 | east-west | low to high | 1,795 | 1,140 | 0.761 | 0.793 |
| manavgat 2021 | east-west | high to low | 1,140 | 1,795 | 0.712 | 0.638 |
| manavgat 2021 | north-south | low to high | 0 | 2,935 | n/a | n/a |
| manavgat 2021 | north-south | high to low | 2,935 | 0 | n/a | n/a |
| bejis 2022 | east-west | low to high | 640 | 460 | 0.750 | 0.784 |
| bejis 2022 | east-west | high to low | 460 | 640 | 0.578 | 0.560 |
| bejis 2022 | north-south | low to high | 357 | 743 | 0.713 | 0.662 |
| bejis 2022 | north-south | high to low | 743 | 357 | 0.603 | 0.613 |
| mugla 2021 | east-west | low to high | 1,449 | 1,462 | 0.448 | 0.378 |
| mugla 2021 | east-west | high to low | 1,462 | 1,449 | 0.636 | 0.628 |
| mugla 2021 | north-south | low to high | 774 | 2,137 | 0.533 | 0.503 |
| mugla 2021 | north-south | high to low | 2,137 | 774 | 0.294 | 0.549 |
| evia 2021 extended | east-west | low to high | 2,052 | 612 | 0.589 | 0.506 |
| evia 2021 extended | east-west | high to low | 612 | 2,052 | 0.645 | 0.482 |
| evia 2021 extended | north-south | low to high | 2,564 | 100 | 0.649 | 0.513 |
| evia 2021 extended | north-south | high to low | 100 | 2,564 | 0.533 | 0.495 |
| montiferru 2021 | east-west | low to high | 410 | 129 | 0.475 | 0.461 |
| montiferru 2021 | east-west | high to low | 129 | 410 | 0.507 | 0.513 |
| montiferru 2021 | north-south | low to high | 438 | 101 | 0.583 | 0.511 |
| montiferru 2021 | north-south | high to low | 101 | 438 | 0.536 | 0.447 |

**Table S3. Leave-one-scar-out at a 2 km buffer, every scar.** Only Muğla and Montiferru contain
more than one burned area of at least 50 cells. Only in Muğla does every held-out case still leave a
well-trained source model. The two Montiferru areas are very unequal, so one case keeps 472 burned
source cells and the other 97. The mean is 0.579 for the four Muğla cases and 0.502 for the three
others. The pooled mean, 0.546, is row C of Table 2. Source
`paper/labelfix_rerun/code/scar_control.json`; checked row by row by `paper/code/appendix_tables.py`.

| Region | Component | Source positives left | Target positives | Target cells | AUC |
|---|---:|---:|---:|---:|---:|
| evia 2021 extended | 1 | 11 | 2,653 | 3,059 | 0.465 |
| montiferru 2021 | 1 | 97 | 442 | 758 | 0.584 |
| montiferru 2021 | 5 | 472 | 67 | 195 | 0.458 |
| mugla 2021 | 6 | 1,997 | 914 | 1,266 | 0.595 |
| mugla 2021 | 1 | 2,173 | 738 | 1,244 | 0.561 |
| mugla 2021 | 10 | 2,272 | 639 | 940 | 0.617 |
| mugla 2021 | 8 | 2,363 | 548 | 954 | 0.542 |

The evaluation populations of these analyses cannot be compared with each other or with the
transfer targets. A held-out scar with its 2 km collar contains only unburned cells next to the fire,
while a whole target region also contains easy distant cells. The burned fractions (34 to 87 %,
against 7.0 to 28.7 %) are a result of this difference, not its cause.

**Table S4. The foreign-region evaluation, by source.** Each held-out scar area is scored with a
model fitted on each of the other four regions. Row D of Table 2 is the mean over the seven scars
that have a row C (28 of the 36 combinations below). Over all nine scars the mean is 0.556. Source
`paper/labelfix_rerun/code/d_per_source.json`; checked row by row by `paper/code/appendix_tables.py`.

| Target region | Scar | Mean over sources | Min | Max | Spread |
|---|---:|---:|---:|---:|---:|
| Bejís 2022 | 1 | 0.589 | 0.519 | 0.631 | 0.112 |
| North Evia 2021 | 1 | 0.564 | 0.374 | 0.704 | 0.329 |
| Manavgat 2021 | 1 | 0.542 | 0.438 | 0.665 | 0.227 |
| Montiferru 2021 | 1 | 0.489 | 0.457 | 0.513 | 0.056 |
| Montiferru 2021 | 5 | 0.475 | 0.399 | 0.597 | 0.197 |
| Muğla 2021 | 1 | 0.514 | 0.410 | 0.608 | 0.198 |
| Muğla 2021 | 6 | 0.571 | 0.545 | 0.597 | 0.052 |
| Muğla 2021 | 8 | 0.623 | 0.533 | 0.724 | 0.192 |
| Muğla 2021 | 10 | 0.634 | 0.433 | 0.716 | 0.283 |

Over all 36 combinations the mean is 0.556, the range is 0.374 to 0.724, and ten combinations are
below chance. The mean spread across the four sources for one scar is 0.183 over nine scars and 0.187
over seven. Row D is averaged over sources so that it can be compared with row C, which is fitted on
one region. This does not mean that the choice of foreign source is unimportant.

**Table S5. Prevalence is not the cause of the evaluation-area effect.** The same fitted model and
the same out-of-fold predictions are scored in three ways: on the whole region, on a random sample of
region cells with the burned fraction of the scar area, and on the scar area. Twenty draws per scar,
seed 42. Nine scars are used, because this control needs no leave-one-scar-out model. Values at 4 dp,
as stored in the source `paper/labelfix_rerun/code/prevalence_control.json`; checked row by row by
`paper/code/appendix_tables.py`.

| Target region | Scar | Burned fraction | A whole region | A′ prevalence-matched | B scar area |
|---|---:|---:|---:|---:|---:|
| Manavgat 2021 | 1 | 0.74 | 0.8822 | 0.8837 | 0.7434 |
| Bejís 2022 | 1 | 0.66 | 0.8245 | 0.8251 | 0.5748 |
| Muğla 2021 | 6 | 0.72 | 0.7773 | 0.7782 | 0.5640 |
| Muğla 2021 | 1 | 0.59 | 0.7773 | 0.7787 | 0.6540 |
| Muğla 2021 | 10 | 0.68 | 0.7773 | 0.7835 | 0.6735 |
| Muğla 2021 | 8 | 0.57 | 0.7773 | 0.7796 | 0.7609 |
| North Evia 2021 | 1 | 0.87 | 0.8642 | 0.8632 | 0.7451 |
| Montiferru 2021 | 1 | 0.58 | 0.7199 | 0.7179 | 0.6215 |
| Montiferru 2021 | 5 | 0.34 | 0.7199 | 0.7285 | 0.4611 |
| **Mean** | | | **0.7911** | **0.7932** | **0.6443** |

A minus A′, the effect of prevalence alone, is −0.002 [−0.005, +0.001]. A′ minus B, which replaces
both groups of cells, is +0.149 [+0.087, +0.211]. Section S1.9.1 shows that it comes from the unburned
cells.

## S1.10 The transfer-gap decomposition, in full

Among the directions that started below chance, the recovered fraction of Section 3.10 is at most
+0.28 (Bejís to Evia). Seven directions have negative recovery, five of them with intervals fully
below zero. Manavgat to Muğla (−0.03 [−0.06, +0.01]) and Muğla to Bejís (−0.07 [−0.16, +0.01]) are
negative at the point estimate only. Values are from `four_aoi_decomposition.csv` of the re-frozen
outputs (`paper/labelfix_rerun/round5/tables/corrected/`). The within-region reference in the
denominator is not matched to a transfer evaluation (Section 4.3), and the raw column depends on the
study area (Section 4.4). The fractions are therefore only valid within this protocol.

**Table S6. Transfer-gap decomposition (four-AOI set, 12 directions).** Within = within-region thermal
AUC of the target. Best adapted = the better of z-score and CORAL; this choice uses target labels.
Recovered fraction = (adapted − raw)/(within − raw), signed and not clipped, with a paired bootstrap
CI (1000 replicates, 2-cell blocks). Montiferru directions are not part of this decomposition. The
status column shows whether the *adapted* value is above chance, using the 2-cell adapted intervals of
Table S16.

| Direction | Within | Raw | Best adapted (method) | Recovered fraction [CI] | Status |
|---|---|---|---|---|---|
| Bejís→Evia | 0.912 | 0.383 | 0.532 (z-score) | +0.28 [+0.23, +0.32] | adapted above chance |
| Muğla→Manavgat | 0.908 | 0.345 | 0.485 (z-score) | +0.25 [+0.22, +0.28] | adapted, chance not excluded |
| Evia→Bejís | 0.918 | 0.448 | 0.549 (z-score) | +0.22 [+0.16, +0.27] | adapted above chance |
| Bejís→Manavgat | 0.908 | 0.314 | 0.406 (CORAL) | +0.15 [+0.13, +0.18] | adapted still below chance |
| Manavgat→Bejís | 0.918 | 0.396 | 0.467 (CORAL) | +0.14 [+0.09, +0.17] | adapted still below chance |
| Manavgat→Muğla | 0.859 | 0.438 | 0.427 (z-score) | −0.03 [−0.06, +0.01] | **negative recovery** |
| Muğla→Bejís | 0.918 | 0.583 | 0.560 (CORAL) | −0.07 [−0.16, +0.01] | **negative recovery** |
| Evia→Muğla | 0.859 | 0.577 | 0.530 (CORAL) | −0.17 [−0.22, −0.11] | **negative recovery** |
| Muğla→Evia | 0.912 | 0.653 | 0.563 (CORAL) | −0.35 [−0.43, −0.27] | **negative recovery** |
| Bejís→Muğla | 0.859 | 0.618 | 0.518 (z-score) | −0.42 [−0.51, −0.34] | **negative recovery** |
| Manavgat→Evia | 0.912 | 0.654 | 0.529 (z-score) | −0.48 [−0.56, −0.42] | **negative recovery** |
| Evia→Manavgat | 0.908 | 0.677 | 0.417 (CORAL) | −1.13 [−1.27, −1.00] | **negative recovery** |

## S1.11 The thermal sign, stratified

Section 4.4 reports that four of five regions show a negative association between pre-fire surface
temperature and burning, and that Manavgat shows the same once elevation is held. The values per
region are given here. Signed AUC against `burned` within the 10 km collar. The stratified columns
pool the concordance within deciles of the named variable, and each decile is weighted by its number
of burned and unburned cell pairs. Sources: `paper/labelfix_rerun/code/matched_frame_gap.csv` (LST
raw, within NDVI, within distance; NDVI columns), which can be recomputed by
`paper/code/verify_matched_gap.py`, and `paper/labelfix_rerun/round7/r7b_lst_given_terrain.csv` (LST
within elevation, and LST detrended on elevation).

**Table S27. The LST association, stratified, 10 km collar.** Point estimates; 10-cell block-bootstrap intervals for every cell
are in `paper/labelfix_rerun/round8/r8e_stratified_intervals.csv`, and the Manavgat values are
summarised in Table S35.

| Region | LST raw | LST within elevation | LST detrended on elevation | LST within NDVI | LST within distance | NDVI raw | NDVI within LST |
|---|---:|---:|---:|---:|---:|---:|---:|
| Manavgat | 0.522 | **0.403** | **0.409** | 0.556 | 0.454 | 0.551 | 0.550 |
| Bejís | 0.405 | 0.509 | 0.411 | 0.486 | 0.350 | 0.618 | 0.574 |
| Muğla | 0.332 | 0.363 | 0.365 | 0.404 | 0.367 | 0.652 | 0.547 |
| Evia | 0.286 | 0.327 | 0.312 | 0.279 | 0.319 | 0.663 | **0.380** |
| Montiferru | 0.376 | 0.392 | 0.416 | 0.368 | 0.485 | 0.582 | **0.405** |

Three results follow. First, the raw LST association of Manavgat is above 0.5, and it falls well
below 0.5 once elevation is held. This holds both for deciles and for removing the linear dependence
of LST on elevation in the region (−5.6 K per km). On the full study area the same holds: 0.665 raw,
against 0.455 and 0.446. The positive signal in Manavgat therefore comes from terrain, and with
terrain held, Manavgat has the same sign as the other four regions. Second, in the other four regions
the sign stays below 0.5 within elevation deciles in three regions and within NDVI deciles in all
four. In Bejís it moves to 0.509 within elevation deciles and stays below 0.5 after detrending. Third,
NDVI reverses in two regions once LST is held, but LST reverses in none of the four once NDVI is
held. Aspect and illumination are not used, so terrain is held only through elevation.

## S1.12 The LST anomaly under the difference instrument

Section 4.4 reports two elevation reversals on the collar, both involving Manavgat, that meet the
per-comparison criterion. The LST anomaly differs between regions under a weaker test: the two regions
are bootstrapped separately and their difference is taken. The three pairs below have point estimates
on opposite sides of 0.5 and a difference interval that excludes zero, all for `lst_anomaly_mean`.
Signed AUC within the 10 km collar; the two regions are bootstrapped separately with 10-cell spatial
blocks, 1000 replicates, seed 42.

**Table S7. Between-region differences in the signed LST-anomaly association, 10 km collar.** Pairs
with point estimates on opposite sides of 0.5 and a difference interval that excludes zero. Source
`paper/labelfix_rerun/inference/reversal_family_holm.csv` (collar frame); checked row by row by
`paper/code/appendix_tables.py`.

| Pair | AUC A | AUC B | Difference | 95 % CI |
|---|---:|---:|---:|---|
| Bejís vs Evia | 0.392 | 0.584 | −0.191 | [−0.295, −0.083] |
| Evia vs Montiferru | 0.584 | 0.400 | +0.184 | [+0.012, +0.321] |
| Bejís vs Muğla | 0.392 | 0.507 | −0.115 | [−0.219, −0.002] |

On the collar, 27 of the 90 feature-by-pair differences have intervals that exclude zero, against
about 4.5 expected by chance at 5 %. Four of the 27 are for this feature. Three of these four have
point estimates on opposite sides of 0.5, and two of the three involve Evia. With a Holm correction
on normal-approximation p-values, 12 of the 90 remain. With the stricter intersection-union form, which
also requires the association in each region to be significant, none remains (Section S1.19). The
nine features carry about two independent thermal signals (Section 3.4), so the 90 comparisons are
not independent. This result is weaker than a reversal.

## S1.13 The same-geography event pair

Section 4.4 gives the result and shows why it does not survive the frame test. The design and two
differences from the twenty-direction matrix are given here. The protocol is in Section S3.3.

This comparison was designed to keep the place fixed and change only the fire. Muğla burned in 2021
and again eleven months later, on the same grid and with the same processing. The 2022 population is
the 2021 population without the 2021 scar: 41,730 rows with 2,911 burned for 2021, against 38,790
rows with 331 burned for 2022. **The 2021 population has 70 blocks of 5 km with burned cells, and the
2022 population has 11.** Eleven is below the minimum of sixteen used in this design, so the 2022
intervals are indicative, like the 20-cell row of Table 1. Values for all features are in Table S12.

**On the original study area, elevation reverses with bootstrap support.** In 2021, higher ground
burned more, at 0.611 [0.532, 0.690]. In 2022, lower ground burned more, at 0.296 [0.230, 0.355]. The
intervals do not overlap, and the difference is −0.317 [−0.414, −0.220].

**The collar removes this reversal.** The 2022 fire is one compact scar inside the whole Muğla
rectangle, so 93.2 % of its cells lie more than 10 km from any burned cell (median 43.6 km), against
55.3 % in 2021. This is the largest share of distant cells in the cohort. On the 10 km collar, the
2021 value hardly changes (0.611 to 0.606, still supported). The 2022 value moves from 0.297 to
0.565, to the same side of 0.5 as in 2021, with an interval that includes chance. Slope does not
reverse on either frame.

**Only elevation and slope can be evaluated.** The modelling export of the 2022 fire is not in this
repository. The released script (`paper/code/verify_mugla_collar.py`) rebuilds the 2022 population
from the 2021 predictor file with the 2022 burned mask. This is valid for elevation, slope and land
cover, which are the same in both years, but not for the seasonal channels. Compared with the
pipeline's own 2022 export, the rebuilt data agree on elevation (0.297 against 0.296) and slope
(0.559 against 0.558). They differ on every seasonal channel: by +0.136 on `lst_anomaly_mean`, +0.092
on `tvdi_difference_mean`, −0.078 on `ndvi_mean` and −0.025 on `current_tvdi_mean`. **Only elevation
and slope are therefore given a collar result here.**

| Feature | 2021, full | 2022, full | full verdict | 2021, collar | 2022, collar | collar verdict |
|---|---|---|---|---|---|---|
| **elevation_mean** | 0.611 [0.529, 0.692] | 0.297 [0.229, 0.363] | **supported reversal** | 0.606 [0.525, 0.685] | 0.565 [0.450, 0.677] | none |
| slope_mean | 0.637 [0.584, 0.689] | 0.559 [0.463, 0.643] | none | 0.635 [0.578, 0.692] | 0.457 [0.356, 0.548] | none |
| the state-dependent channels | n/a | n/a | n/a | n/a | n/a | **not evaluable here** |

Source `paper/labelfix_rerun/code/mugla_two_event_collar.csv`. The two populations are not separate
samples. They share 38,789 of the 38,790 cells of the 2022 population. Elevation, slope and land
cover are identical in all 73,098 grid cells, so only NDVI and the six thermal channels differ between
them. The 2021 burned cells were also removed from the 2022 population. In the 2022-to-2021 direction,
therefore, no burned target cell is in the source training data, while 38,789 of the 38,819 unburned
target cells are. Membership of the training data alone separates the two classes of the 2021 target
at ROC-AUC 0.9996. **The effect of this on a transfer estimate between the two years cannot be
bounded.** The known part of the bias makes the reversal smaller, not larger: the removed cells are
high (median 563 m), so removing them takes high unburned cells out of the 2022 population.

## S1.14 The two interventions, in full

**(a) Pooled multi-region training** (Fig. 6). A model trained on the pooled populations of the
other four regions is better than the mean of the four single-source models for one target of five,
Evia, at 0.715 [0.668, 0.757] against a mean of 0.569. For the other four targets it is worse than
this mean, by 0.009 to 0.057. It is better than the best single source only for Evia (0.654). The
best source can only be chosen with target labels, so it is a reference, not an option. For every
target the pooled model stays 0.20 to 0.48 AUC below the within-region ceiling. For Manavgat and
Bejís it is below chance, and only for Manavgat with interval support, at 0.426 [0.369, 0.486].
Outside Evia, pooling does not recover what single-source transfer loses
(`paper/labelfix_rerun/code/loro_all.json`, `paper/labelfix_rerun/round7/r7d_pooled_vs_single.csv`).

**(b) Removing the direction-reversing features.** Under the original label, two predictors
reversed between regions with bootstrap support on the original study areas:
**`elevation_mean` and `lst_anomaly_mean`**. This analysis keeps these two and does not re-select
under the corrected label (Table S10). Section 4.4 shows that the study area decides much of the
support, so this analysis measures the cost of removal under the original protocol. Without the two
predictors, mean within-region AUC falls by **−0.076**, with support in every region (−0.035, −0.130,
−0.073, −0.063 and −0.079 for Manavgat, Bejís, Muğla, Evia and Montiferru; every interval fully below
zero). Mean transfer changes by **+0.014 [−0.028, +0.056]**, which includes zero (source
`paper/labelfix_rerun/round3/feature_drop_transfer.json`, summarised by
`paper/labelfix_rerun/round7/r7e_supplement_tables.py`).

Two points should be noted. First, most of the cost does not come from the thermal set. Removing
elevation alone costs −0.056 (0.896 to 0.840). Removing the LST anomaly alone costs −0.013 (0.896 to
0.883). About three quarters of the cost therefore comes from removing a baseline terrain variable.
Second, both predictors were chosen because they reverse, on the same data on which the costs are
estimated, and no correction is applied.

**Table S28. Feature-removal configurations.**

| Configuration | Mean within-region AUC | Mean transfer AUC |
|---|---:|---:|
| full | 0.896 | 0.527 |
| drop `elevation_mean` | 0.840 | 0.533 |
| drop `lst_anomaly_mean` | 0.883 | 0.529 |
| drop both | 0.820 | 0.541 |

Fig. 7 shows the four configurations together. A local cost is measured, but no transfer gain. This
is not an exchange, because neither transfer effect is established: the thermal contribution to
transfer is +0.007 and removing the reversing predictors gives +0.014, and both intervals include
zero.

## S1.15 Signed associations on both frames

Section 4.4 gives the collar results. The values per region are given here. Values per feature on
both frames are in Table S14.

**Reversals that meet the per-comparison criterion.** On the original study areas, Table S10 counts
fourteen supported reversals between pairs, across seven features. All but the anomaly pair involve
Manavgat. On the collar, elevation is below 0.5 in Manavgat, at 0.376 [0.300, 0.465], and above 0.5
in the other four regions. It is supported in two of them: Muğla at 0.606 [0.525, 0.685] and Evia at
0.648 [0.550, 0.740] (`paper/labelfix_rerun/code/collar_frame_bootstrap.csv`). These two pairs are
the only supported reversals left on the collar, and neither survives the Holm intersection-union
correction (Section S1.19). The LST anomaly differs between regions only under the weaker difference
test (Section S1.12).

**The common sign.** On the collar, LST is below 0.5 in four of five regions: 0.405, 0.332, 0.286 and
0.376 in Bejís, Muğla, Evia and Montiferru. A hotter pre-fire surface is therefore associated with
less burning there, and the same holds for TVDI. Manavgat is the exception in the raw association
(0.522 for LST, 0.527 for TVDI), but it shows the same sign once elevation is held (Section S1.11).
Interval support differs: LST is supported in three of the four regions and TVDI in two, so "four of
five agree" refers to point estimates. The absolute thermal channels therefore behave here as
land-surface descriptors and not as a dryness index. The two differenced channels have no consistent
direction across regions.

**The number of independent reversals.** The channels whose reversals disappear on the collar partly
measure terrain. Across the regions, current LST is correlated with elevation at −0.695 to −0.125, and
TVDI at −0.722 to −0.298. Within the collar, `fused_lst_mean` is correlated with `current_lst_mean`
at 0.99 to 1.00, `downscaled_lst_mean` at 0.97 to 0.99 and `current_tvdi_mean` at 0.87 to 0.98. The
two differenced channels are correlated at 0.64 to 0.94. Counts over the nine features therefore
count features, not independent quantities. The thermal set carries about two independent signals.

**The paired thermal contribution to transfer.** The thermal and baseline matrices were
differenced direction by direction. The mean is **+0.007**. The single contributions range from
**−0.148 to +0.132**, with **twelve positive and eight negative**. A mean near zero therefore comes
from positive and negative values that cancel, not from a consistent absence of effect. The
directions are not independent, because each region appears in eight of the twenty. The interval
therefore depends on the resampling unit. All four units that the design allows give intervals that
include zero (1000 replicates where resampled; source
`paper/labelfix_rerun/code/transfer_delta_ci.json`):

**Table S29. The mean paired thermal contribution to transfer, by resampling unit.**

| Resampling unit | n | 95 % interval on the mean paired contribution |
|---|---:|---|
| Directions, naive bootstrap | 20 | [−0.023, +0.037] |
| Unordered pairs, cluster bootstrap (primary) | 10 | [−0.020, +0.038] |
| Unordered pairs, Student *t* on pair means | 10 | [−0.028, +0.043] |
| Regions, leave-one-out jackknife | 5 | [−0.018, +0.033] |

Leaving out Manavgat, Bejís, Muğla, Evia and Montiferru in turn gives +0.0148, +0.0050, +0.0072,
+0.0010 and +0.0087. No single region therefore carries the mean or changes its sign. These units
resample only between directions. They do not include the sampling variability within a direction.

**Precision.** Across the twenty directions, the mean PR-AUC of the thermal model is **0.181, against
a no-skill baseline of 0.157**. The mean of the twenty lifts over the baseline is 1.13. Seven of the
twenty directions are below their own no-skill baseline at the point estimate. At 1 km blocking all
seven have intervals fully below it. At 5 km blocking two do: Bejís to Manavgat and Muğla to Manavgat
(`paper/labelfix_rerun/round7/r7a_pr_auc_10cell.csv`). Only one direction, Evia to Manavgat, is above
twice its baseline, at 0.321 against 0.143 (Table S11).

**The within-region gain on the collar.** The baseline model was also run on the collar
(`paper/labelfix_rerun/round6/cosine/official_collar_increment_and_cosine.csv`). The thermal gain at
5 km blocking is +0.073, +0.030, +0.088, +0.134 and +0.090 in the five regions. It is positive in all
five, with a mean of +0.083, against +0.087 on the original study areas. On a 5 km collar the mean
falls to +0.042, but it is still positive in all five regions. These are point estimates. The
intervals of Table 1 refer to the original study areas.

**The five study areas are not comparable.** The share of modelled cells more than 10 km from any
burned cell is 58.5 % in Manavgat, 63.1 % in Bejís, 55.3 % in Muğla, 43.7 % in Evia and **2.1 %** in
Montiferru. The median distances are 13.1, 13.5, 11.3, 8.0 and 2.7 km (Table S13). In Manavgat, the
median elevation of modelled cells rises from 330 m within 5 km of the fire to 995 m at 10 to 20 km
and 1,273 m at 20 to 50 km. The median elevation of the burned cells is 287 m.

## S1.16 The contrast pair, in full

Manavgat and Muğla are in the same country, burned in the same year, and are 306 km apart. Their
burned cells have the most similar environmental range of any pair in the matrix. Bejís and
Montiferru have the least similar range (Fig. 8). Values for both pairs, on both frames, are in Table
S18.

For Manavgat and Muğla on the original study areas, seven of nine feature-response directions point
opposite ways, and all six features supported in both regions have opposite signs, including
elevation. On the collar the elevation reversal remains, at 0.376 [0.300, 0.465] in Manavgat against
0.606 [0.525, 0.685] in Muğla. Transfer is below chance in both directions on both frames: 0.438 and
0.345 as drawn, 0.493 and 0.433 under the collar. On the collar, the interval of Muğla to Manavgat,
[0.381, 0.491], excludes chance. The most similar pair is among the weakest in the matrix, but it is
not the weakest. On the collar, the weakest direction is Manavgat to Bejís at 0.407 and the strongest
is Muğla to Evia at 0.728. The niche-overlap and applicability measures of Table S18 are computed on
the original study areas.

Bejís and Montiferru are at the other extreme. Their burned ranges hardly overlap, and they have the
most different values on every overlap measure. They transfer above chance in both directions, but
only at the point estimate: neither direction has interval support at 5 km blocking. The
applicability measure was not produced for Montiferru. **At the point estimates, high niche overlap
did not ensure transfer, and low overlap did not prevent it.** This rests on two pairs. It is not a
correlation across pairs; that is tested in Section S1.21.

## S1.17 The sensitivity arms, summarised

Eight design choices were changed, one at a time, with everything else kept fixed: the Evia study
area and its prevalence, the CORAL regularisation, the block size, the closing date of the predictor
window, the quality screening of the coarse thermal input, normalised against absolute dryness
channels, the removal of the coordinate-informed channels, and the capacity of the classifier
(Sections S1.1 to S1.8). None changes a conclusion of the main text. Two of them affect how the
results should be read.

**The secondary population.** Section 3.5 defines a secondary population of all valid cells,
including cropland. It exists only for the within-region models in Manavgat and Bejís, so it is a
two-region sensitivity analysis, and no transfer quantity is defined on it. Across the two regions
and three block sizes, the thermal gain is +0.048 to +0.061, with every bootstrap interval above zero,
against +0.045 to +0.067 in the primary population. The paired difference between the populations is
−0.011 to +0.011, with no consistent sign
(`paper/labelfix_rerun/pipeline/robustness/step8_large_block_primary_all_valid/`; Table 1). The gain
is therefore not caused by excluding cropland. This analysis says nothing about transfer.

**The block size.** Larger blocks (5 km instead of 1 km) change the paired thermal-minus-baseline
verdicts from twelve positive, seven negative and one uncertain to six, five and nine. The verdicts
for the thermal model itself change from eleven above, seven below and two uncertain to nine, six and
five (Section S1.3). Support is removed, never added. The point estimates do not change.

## S1.18 Distance within a region

This analysis measures how skill falls with distance inside one region. A model is fitted on one
half of a region and applied to the other half. Target cells are grouped by their distance from the
training cells (`paper/code/distance_curve.py`; corrected output
`paper/labelfix_rerun/round3/distance_curve.json`, summarised in
`paper/labelfix_rerun/round7/r7h_distance_curve.csv`). Means are unweighted over bins. The bins
contain 1 to 1,067 burned cells and have no intervals.

**Table S32. Within-region skill by separation from the training cells.**

| Separation from training cells | Bins | Mean target AUC |
|---|---:|---:|
| 0 to 5 km | 18 | 0.709 |
| 5 to 10 km | 16 | 0.570 |
| 10 to 20 km | 11 | 0.519 |
| 20 to 40 km | 6 | 0.499 |
| 40 to 80 km | 3 | 0.541 |
| 80 to 160 km | 1 | 0.421 |
| cross-region, 306 to 2,802 km | 20 | 0.527 |

**At 10 to 20 km inside one region, the model is close to chance.** This limits how far such a
model can be used from its training cells. It agrees with Section 4.3, where withholding a scar or
using a foreign model had no measurable cost.

This does not show that the cross-region failure is only an effect of distance. Once the curve
reaches chance, any cross-region mean near 0.5 must lie on its continuation, so this comparison
cannot test it. Also, a model that carries no information does not give a reliably reversed ranking,
but Manavgat to Bejís is below chance with interval support both on the original study area and on
the 10 km collar.

Four limits apply. First, the two distance ranges do not overlap: within-region distances are 2 to
86 km, and cross-region distances start at 306 km. Second, the far bins contain few cells, so their
means should not be read closely; the rise at 40 to 80 km is not evidence of an effect. Third, the
near bins include the spatial autocorrelation that blocked validation is designed to remove, so
**0.709 is an upper bound on near-field skill, not an estimate of it**. Fourth, the design separates
distance from crossing a study-area boundary, but not from the land cover, terrain and fire history
that change with distance. The analysis gives a length scale for the fall of skill within a region,
not a cause.

## S1.19 The frame test, elaborated

Section 4.4 gives these results. Sources: `paper/labelfix_rerun/code/aoi_frame_auc.csv` (signed
associations by frame), `paper/labelfix_rerun/code/collar_frame_bootstrap.csv` (their 10-cell
intervals), `paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv` (the transfer matrix by
frame) and `paper/labelfix_rerun/code/matched_frame_gap.csv` (the matched reference); code in
`paper/code/`.

**Construction.** Every region is restricted to cells within 10 km of any burned cell. This removes
only distant unburned cells. Every burned cell is at distance zero and is kept at any radius, so
radii were compared to guard against a favourable choice. The interval criterion was evaluated at
the 10 km collar; the 5 and 10 km radii agree at the point estimate. The collar strongly reduces the
number of cells in two regions, so part of any loss of support is a loss of power. On average, 2.3
features per direction are supported in both regions on the original study areas, and 2.2 on the
collar.

**Multiplicity.** Each frame has a family of ninety feature-by-pair comparisons (nine features, ten
region pairs). Table S30 gives how many pass each criterion. The per-comparison criterion of Section
3.10 leaves two supported reversals on the collar, both on elevation and both involving Manavgat.
Neither survives the Holm intersection-union correction, which adjusts the tests of both regions
together (adjusted *p* = 0.33 for Manavgat against Evia and 0.79 for Manavgat against Muğla, normal
approximation).

**Table S30. Reversal family, ninety feature-by-pair comparisons per frame.** Source
`paper/labelfix_rerun/inference/reversal_family_holm.csv`, `reversal_per_region.csv`.

| Criterion | Full frame | 10 km collar |
|---|---:|---:|
| Difference interval excludes zero | 39 | 27 |
| … with opposite-sided point estimates | 31 | 21 |
| Per-comparison criterion (each region's own interval excludes 0.5, opposite sides) | 14 | 2 |
| Holm, normal approximation, difference test | 27 | 12 |
| Holm intersection-union (both regions' tests) | 5 | 0 |

**Similarity measures on the collar.** Two of the twenty similarity measures are built from the
signed associations, and they were recomputed on the collar. The sign-agreement fraction over
supported features is ρ = +0.52 [−0.27, +0.87] on the original study areas. On the collar it takes
only the values 0 and 1 across sixteen defined directions, and it correlates with collar transfer at
ρ = +0.38 [−0.17, +0.85]. The all-feature cosine is +0.44 [−0.29, +0.80] on the original study areas
and correlates with collar transfer at **+0.57 [+0.05, +0.88]**. This is the only interval of a
similarity measure in the study that excludes zero
(`paper/labelfix_rerun/round6/diag_collar/`; intervals from
`paper/labelfix_rerun/round7/r7g_collar_diagnostics.json`, which reproduces the original intervals
exactly). It is not treated as a result for three reasons. It is one of about forty uncorrected
tests. It rests on twenty directions that share regions. The collar is defined from the burned
cells, so the measure needs target labels twice. The other eighteen measures were not recomputed on
the collar.

**Data provenance.** A quality-screening rebuild overwrote the 500 m modelling datasets of Manavgat
and Muğla at the standard pipeline path after the frozen tables were computed. Each new file differs
in `downscaled_lst_mean` and `fused_lst_mean`. The pipeline records a SHA-256 for the modelling
dataset of each region, and this hash identifies the frozen copy. Every analysis of Section 4.4 reads
each region through `paper/code/_canonical.py`, which checks the hash on load, and reads Manavgat
from the corrected re-freeze (SHA-256 `5a5e876c…`). The provenance of the collar transfer matrix is
in `paper/labelfix_rerun/round5/collar/PROVENANCE.md`.

**Table S8. Cross-region transfer on comparable study areas.** Natural-vegetation population,
thermal model, twenty ordered directions per row. Above and below chance are point counts. The
supported counts use a 10-cell (≈5 km) spatial-block bootstrap on the target, 1000 replicates, seed
42. Table S16 gives the original matrix under 2-cell (≈1 km) blocking. Bounds per direction are in
`paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv`.

| Source frame | Target frame | Mean target AUC | Above chance | Below chance | Supported above / below | Paired thermal delta |
|---|---|---:|---:|---:|---:|---:|
| full | full | 0.527 | 13 of 20 | **7** | 9 / **6** | +0.007 |
| full | 10 km | 0.559 | 14 of 20 | 6 | 10 / 2 | +0.008 |
| 10 km | full | 0.546 | 14 of 20 | 6 | 10 / 5 | +0.014 |
| **10 km** | **10 km** | **0.589** | **15 of 20** | **5** | **13 / 2** | **+0.024** |
| 5 km | 5 km | 0.591 | 16 of 20 | 4 | 11 / 0 | +0.017 |

The baseline changes with the frame. On the 10 km collar, the static baseline transfers at 0.565
and the thermal model at 0.589, a paired difference of +0.024 instead of +0.007. The static baseline
still does not transfer well. The number of directions below chance falls from seven to five at the
point estimate, and from six to two with interval support. The largest rises are Bejís to Evia (0.383
to 0.602) and Bejís to Manavgat (0.314 to 0.452). The only large fall is Evia to Manavgat (0.677 to
0.594).

**The matched reference.** The within-region reference was recomputed on the same frame at 5 km
blocking (`paper/code/verify_matched_gap.py`):

**Table S33. Within-region reference and transfer on matched frames.**

| Frame | Within-region (5 km blocking) | Mean transfer | Gap |
|---|---:|---:|---:|
| full rectangle | 0.814 | 0.527 | 0.287 |
| 10 km collar | **0.786** | **0.589** | **0.197** |
| 5 km collar | 0.759 | 0.591 | 0.169 |

Paired by target region, the shortfall on the collar is **+0.197 [+0.091, +0.303]** (Student *t*
over the five target regions; +0.081 Montiferru, +0.319 Manavgat, +0.172 Muğla, +0.202 Bejís, +0.211
Evia). The shortfall remains on every matched row. It is 0.197 on the collar, not the 0.29 of the
unmatched comparison, and it becomes smaller as the frame moves closer to the fire. On the 5 km
collar, the within-region gain falls by half but stays positive in all five regions, with a mean of
+0.042 (Manavgat +0.035).

## S1.20 The transfer matrix and adaptation, elaborated

Section 4.5 gives these results.

**Raw transfer.** Raw target AUC ranges from 0.314 to 0.677 (Fig. 4). At 2-cell blocking, eleven of
20 directions are above chance with interval support and seven are below: both directions between
Manavgat and Bejís, both between Manavgat and Muğla, both between Bejís and Evia, and Montiferru to
Manavgat. At 10-cell blocking the same point estimates give 9 above, 6 below and 5 uncertain.
Manavgat to Muğla loses its support, and no direction changes side of the chance line. Of the
directions below chance, Manavgat to Bejís (0.407 [0.323, 0.493]) and Muğla to Manavgat (0.433
[0.381, 0.491]) keep interval support on the 10 km collar, but both intervals include chance on the
5 km collar. The lowest direction on the original study areas is Bejís to Manavgat, at 0.314 [0.296,
0.332].

**Label-free adaptation.** Under region-wise z-scoring the twenty directions range from 0.302 to
0.630, and under CORAL from 0.406 to 0.624. The change is not uniform: under z-scoring, Bejís to
Manavgat falls further below chance, from 0.314 to 0.302. With the better of the two methods in each
direction, 15 of the 20 directions end closer to chance and 5 end further from it. Four of these five
involve Montiferru and move up. The fifth, Manavgat to Muğla, moves down from 0.438 to 0.427. Under
CORAL alone, sixteen of twenty end closer to chance
(`paper/labelfix_rerun/round5/matrix20_official.csv`). In the six directions where raw transfer was
below chance, the best label-free method recovers at most 28 % of the gap to the within-region
reference (Bejís to Evia). On the twelve directions of the decomposition, seven show negative
recovery (Section S1.10).

**Seed stability.** Across five bootstrap seeds, every 2-cell verdict is stable. At 10 cells, one
level verdict and two paired-delta verdicts change: the level verdict of Evia to Bejís, and the
paired-delta verdicts of Manavgat to Muğla and Evia to Montiferru
(`paper/labelfix_rerun/round6/seed_stability.json`). The random-forest seed is fixed, so all
intervals per direction are conditional on one fitted source model.

**Jackknife.** Leaving out one region at a time moves the mean paired contribution between +0.001
(without Evia) and +0.015 (without Manavgat). Its sign never changes.

## S1.21 The similarity diagnostics

Twenty similarity measures from five families were each rank-correlated with raw thermal transfer
AUC over the directions on which they are defined. One pair-based bootstrap is used for all of them
(unordered pairs resampled with replacement, both directions kept, 2000 replicates, seed 42). The
measures were defined on 8 August 2026, together with their results under the original label, and
were not re-selected after the label correction. Table S17 lists all twenty. The source is
`paper/labelfix_rerun/round5/out_official/all_diagnostics_vs_transfer.csv`, and the original-label
values are in `paper/labelfix_rerun/round5/s6_diagnostics_20.md`.

**On the original study areas, no interpretable measure has an interval that excludes zero.** The
largest correlations are for the conditional family: the sign-agreement fraction over supported
features, at ρ = +0.52 [−0.27, +0.87], and its cosine, at +0.49 [−0.24, +0.87]. Under the original
label these two were the only rows with intervals that excluded zero (+0.84 and +0.81). This did not
hold after the label correction. The marginal family (applicability, dissimilarity, climatic
distance, domain classification), the niche-overlap family and the regime family all include zero.
Geographic distance does not order the matrix (ρ = −0.17 [−0.87, +0.84] on the twelve directions
where it is defined). The domain classifier separates source from target at AUC ≥ 0.96 for every
pair. Because it always succeeds, it gives no ordering. The twentieth measure, the vector Spearman of
signed AUCs over supported features, is defined on only six directions. Its interval is degenerate
(the upper bound equals the point estimate), so it is listed but not interpreted.

**Equal samples.** The families use different samples: twelve directions for the marginal,
applicability, climatic and geographic rows, eighteen for the supported conditional rows, and twenty
for the others. Every row was therefore recomputed on the common subsets of twelve and sixteen
directions. On both, every interpretable row includes zero
(`paper/labelfix_rerun/round5/out_official/diagnostics_common_subset.json`).

**The collar.** Section S1.19 gives the two measures recomputed on the collar. One of them, the
all-feature cosine, orders collar transfer with an interval that excludes zero. It is reported with
its limits and is not used.

**Limits.** Signed associations need burned labels in both regions, so the conditional family cannot
be used before a fire. The marginal family can be used, but it fails. Ten independent region pairs
give little power, and a moderate ordering would usually be missed. These results therefore show a
failure to find an ordering, not proof that none exists (Section S3.5(xiii)). Measures based on
interval support are unstable when bounds lie near 0.5 (Section S3.5(viii)).

## S1.22 Additional robustness analyses

The analyses in Table S21 were run after the main results. They test whether the main quantities
depend on analysis choices. None of them was used to select a reported configuration.

**Table S21. Additional robustness analyses (post hoc).** Sources under `paper/labelfix_rerun/`:
`geometry/` (a1 to a5), `inference/` (units, equivalence, ladder) and `round7/`.

| Analysis | Question | Result |
|---|---|---|
| Edge-excluded frame cost (a1) | Is the frame cost carried by the scar's edge cells? | Over nine scars, excluding 0, 1 or 2 cells of the scar edge gives A − B = 0.147 [0.086, 0.208], 0.137 [0.069, 0.205] and 0.129 [0.055, 0.204]; with the region as unit 0.160, 0.150 and 0.145, every interval above zero |
| Placebo collars (a2) | Is the cost a property of any fire-shaped frame? | The scar's real positives scored against the negatives of a same-shaped collar placed away from any burned cell reproduce A (A − placebo −0.002 [−0.056, +0.052], eight scars with placements); the real collar costs +0.155 [+0.108, +0.202] more, so the cost is the fire-adjacent negatives |
| Frame cost against the share of distant cells (a3) | Is the cost larger where the study area has more distant cells? | No. Region-level slope 0.005 [−0.41, +0.42], r = 0.02 (n = 5); scar-level slope −0.049 [−0.34, +0.24] (n = 9, scars not independent). The test has little power |
| Label-free target frames (a4) | Does a frame drawn without target labels change transfer? | Trimming the target to the source's per-feature range, or to the source's area of applicability [@Meyer2021], gives means of 0.520 to 0.574, and a 20 km window 0.482; every paired thermal Δ interval spans zero |
| Metric dependence (a5) | Is the frame cost specific to ROC-AUC? | Region-wide minus scar-frame over nine scars: partial AUC (FPR ≤ 0.1) 0.088 [0.048, 0.128]; average precision −0.342 [−0.477, −0.206], higher on the scar frame because its prevalence is higher |
| Collar within-region increment | Does the within-region increment survive the collar? | +0.083 [+0.037, +0.129] over five regions (Student *t*), against +0.087 [+0.037, +0.136] as drawn |
| Equalised Δ by resampling unit | Does the collar Δ exclude zero? | Table S31: two of six computable units exclude zero; the two-way estimators are undefined |
| Equivalence of the equalised Δ | How large a gain is excluded? | Within ±0.05 under four of five units; no gain above 0.047 at 90 % (pair cluster); not within ±0.02 under any unit |
| Within minus transfer increment | Is the local-versus-portable contrast itself supported? | Full frame +0.079 [+0.014, +0.145]; 10 km collar +0.059 [+0.007, +0.110]; 5 km collar +0.026 [−0.012, +0.063] |
| Reversal multiplicity | Do the collar reversals survive correction? | Table S30: two per-comparison reversals, none after Holm intersection-union |
| scikit-learn version | Do point estimates depend on the library version? | Under 1.5.2 against 1.9.0, single directions move by up to 0.047 and means by at most 0.003; one support count changes (`round7/sklearn152/compare_vs_1_9_0.json`) |

**Table S31. The equalised (10 km collar) paired contribution by resampling unit.** 20,000
replicates where resampled; 95 % intervals. Source `paper/labelfix_rerun/inference/units.json`.

| Unit | 95 % interval | Excludes zero |
|---|---|---|
| Directions, naive | [−0.001, +0.049] | no |
| Unordered pairs, cluster bootstrap (primary) | [−0.003, +0.051] | no |
| Target region, cluster bootstrap | [+0.010, +0.040] | yes |
| Source region, cluster bootstrap | [+0.010, +0.042] | yes |
| Pigeonhole (source and target) | [−0.005, +0.060] | no |
| Two-way cluster (CGM) | undefined (negative variance) | n/a |
| Dyadic-robust | undefined (negative variance) | n/a |
| Leave-one-region-out jackknife, *t* | [−0.017, +0.065] | no |

The primary unit is the pair cluster (Section 3.7), and on it the paired contribution on the collar
includes zero. With five regions, a percentile bootstrap over regions has at most 126 distinct
resamples, so the two region-clustered intervals are coarse.

## S1.23 Analyses added after the pre-submission review

The analyses in Table S35 were run after an internal review of the manuscript. They test the
dependence of the main results on the fitted forest, the adaptation method, the inference for the
similarity measures, and two data choices. Sources are in `paper/labelfix_rerun/round8/`, which also
describes each script.

**Table S35. Analyses added after the pre-submission review (post hoc).**

| Analysis | Question | Result |
|---|---|---|
| Random-forest seed (R8a) | Do the transfer results depend on the fitted forest? | With ten seeds, mean transfer on the original study areas ranged from 0.525 to 0.530 and the mean thermal gain from +0.005 to +0.008. The seed-to-seed standard deviation of a direction had a median of 0.005 (maximum 0.015), and no direction changed side of chance. On the 10 km collar, mean transfer ranged from 0.588 to 0.592, and one direction (Montiferru to Manavgat) changed side. Averaging the predictions of the ten forests gave 0.527 (gain +0.006) and 0.590 (gain +0.025). Seed 42 reproduces the published matrix exactly |
| CORAL variants and placebo (R8c) | Is the movement toward chance specific to aligning with the target? | CORAL with λ = 1 gave a mean of 0.512 and CORAL on two thermal principal components 0.523, against 0.527 without adaptation. A placebo that aligns the source with the covariance of a third region instead of the target gave 0.507 and moved 15 of 20 directions closer to chance, against 16 of 20 for CORAL. The movement is therefore not specific to the target. The published CORAL values were reproduced to within 0.009 |
| Permutation test of the similarity measures (R8d) | Does any measure predict transfer under a permutation test? | No. With all 120 permutations of the five regions, the smallest two-sided p-value was 0.10 (vector Spearman, six directions only); the two supported-feature conditional measures gave 0.125 and 0.15, and all other measures 0.15 or more. The smallest attainable p-value is 1/120 |
| Without Manavgat (R8d) | Does one region drive the transfer results? | Without the eight directions that involve Manavgat, mean transfer was 0.566 on the original study areas (two of twelve directions below chance) and 0.631 on the 10 km collar (none below chance). The thermal gain was +0.015 and +0.032. Transfer is better without Manavgat, but it stays far below within-region skill |
| Equivalence on the original study areas (R8d) | Is the as-drawn thermal gain within ±0.05? | Yes, under all six resampling units that can be computed; the 90 % upper bounds range from 0.021 to 0.037. It is not within ±0.02 under any unit |
| Intervals for Table S27 (R8e) | Are the stratified LST associations supported? | On the 10 km collar, the Manavgat LST association within elevation deciles is 0.403 [0.343, 0.464], and after removing the linear effect of elevation 0.409 [0.350, 0.475]; both intervals exclude 0.5. On the original study area the values are 0.455 [0.396, 0.509] and 0.446 [0.387, 0.502], which include 0.5 |
| Capture of burned cells (R8b, R8g) | How many burned cells fall in the highest-scored cells? | In transfer, the 10 % of target cells with the highest thermal scores contained on average 10.3 % of the burned cells (range 0.7 % to 27.1 %), which is what a random ranking gives; eight of twenty directions were below it. The top 20 % contained 19.9 %. Within regions (5 km blocking) the top 10 % contained 35.5 % of the burned cells on average (18.9 % to 44.5 %), and the top 20 % contained 55.7 % |
| Pre-fire land cover (R8i, R8j) | Does the post-fire WorldCover v200 map (2021 images) affect the population or the results? | The 2020 map (v100) was fetched on each region's 30 m grid and aggregated to the same cells; the same procedure applied to v200 reproduces the pipeline's raster and every cell value of the modelling datasets exactly. With the 2020 map, at most 43 burned cells left or entered the natural-vegetation population in Manavgat, Bejís, Muğla and Evia. In Montiferru, 142 burned cells entered it, and the gate fraction rose from 0.773 to 0.977, so the 2021 map left out about a fifth of the burned natural vegetation there. The within-region thermal gain (5 km blocking) changed from +0.062, +0.045, +0.079, +0.148 and +0.099 to +0.060, +0.071, +0.083, +0.155 and +0.095 (Manavgat, Bejís, Muğla, Evia, Montiferru). Mean transfer changed from 0.527 to 0.513, and the mean thermal gain in transfer from +0.007 to +0.013; seven directions were below chance with both maps, and no direction changed side. Part of the class changes reflects the different algorithms of v100 and v200, not the fires |
| Bejís pre-label cells (R8b) | Do the 48 cells that burned in the predictor window affect the results? | Ten of them are labelled burned. Without them, the within-region thermal gain was +0.050 at 1 km blocking (+0.056 with them) and +0.061 at 5 km (+0.045). Transfer in the eight directions that involve Bejís changed by at most 0.015, and their mean thermal gain from +0.011 to +0.007 |

A leave-one-block-out reference with a 10 km buffer was also tried. Its pooled AUC combines the
predictions of different models, and because the burned cells lie in one or two blocks, the pooled
value was dominated by calibration differences between the models. It is therefore not reported; the
distance curve of Section S1.18, which scores a single model, answers the same question.

# S2 Supporting tables

These tables give the values per region and per direction that the Results quote, so that every
statement can be checked against the values behind it.

**Table S9. Signed univariate AUC of each predictor against `burned`, by region.** Natural-vegetation
population; 10-cell (~5 km) spatial-block bootstrap, 1000 replicates, seed 42. The AUC is not folded
to max(AUC, 1 − AUC). A value below 0.5 means that lower values rank burned cells higher; it shows a
direction, not weakness. **Bold** marks a region whose own interval excludes 0.5. Source
`paper/labelfix_rerun/round5/tables/step9g_multi_aoi_feature_stability.csv` (the pipeline's Step9G
five-region synthesis, sha256 c864cd7d…); checked row by row by `paper/code/appendix_tables.py`.

| Feature | Manavgat | Bejís | Muğla | Evia | Montiferru |
|---|---|---|---|---|---|
| `elevation_mean` | **0.232** [0.179, 0.288] | **0.643** [0.558, 0.729] | **0.611** [0.532, 0.690] | 0.541 [0.448, 0.626] | 0.584 [0.395, 0.762] |
| `slope_mean` | **0.400** [0.340, 0.459] | 0.521 [0.439, 0.605] | **0.637** [0.582, 0.686] | 0.487 [0.418, 0.554] | **0.652** [0.506, 0.771] |
| `ndvi_mean` | 0.564 [0.499, 0.628] | 0.559 [0.497, 0.619] | **0.662** [0.616, 0.704] | **0.639** [0.575, 0.701] | 0.586 [0.450, 0.704] |
| `lst_anomaly_mean` | 0.509 [0.460, 0.560] | **0.418** [0.364, 0.480] | 0.485 [0.395, 0.566] | **0.640** [0.567, 0.710] | 0.395 [0.285, 0.535] |
| `current_lst_mean` | **0.665** [0.608, 0.719] | 0.477 [0.401, 0.547] | **0.325** [0.271, 0.382] | **0.377** [0.301, 0.456] | 0.370 [0.248, 0.513] |
| `current_tvdi_mean` | **0.677** [0.622, 0.733] | 0.517 [0.429, 0.595] | **0.336** [0.275, 0.398] | **0.362** [0.285, 0.442] | **0.356** [0.233, 0.499] |
| `tvdi_difference_mean` | 0.460 [0.409, 0.510] | 0.512 [0.443, 0.583] | 0.490 [0.396, 0.575] | 0.519 [0.444, 0.589] | **0.378** [0.282, 0.497] |
| `downscaled_lst_mean` | **0.683** [0.626, 0.739] | 0.484 [0.400, 0.560] | **0.307** [0.253, 0.366] | **0.377** [0.297, 0.459] | 0.365 [0.240, 0.511] |
| `fused_lst_mean` | **0.666** [0.610, 0.721] | 0.481 [0.404, 0.551] | **0.325** [0.272, 0.383] | **0.376** [0.300, 0.456] | 0.370 [0.248, 0.513] |

**Definition of a reversal.** A pair of regions is called a reversal only when their signed
associations lie on opposite sides of 0.5 **and the interval of each region excludes 0.5**. This is
stricter than requiring disjoint intervals. For example, for `current_lst_mean` in Manavgat and Bejís
the two intervals are disjoint ([0.608, 0.719] against [0.401, 0.547]), but the Bejís interval
includes 0.5. Bejís therefore has no established direction, and this pair is a point reversal only.

**Table S10. Cross-region reversals that meet the strict criterion.** The criterion is applied to
the intervals of Table S9. Difference intervals are from the paired 10-cell block bootstrap of
`paper/code/ems_inference_multiplicity.py` (`paper/labelfix_rerun/inference/reversal_family_holm.csv`,
1000 replicates), which flags the same fourteen pairs. Checked row by row by
`paper/code/appendix_tables.py`.

| Feature | Region A | AUC | Region B | AUC | Difference [95 % CI] |
|---|---|---:|---|---:|---|
| `elevation_mean` | Manavgat | 0.232 | Bejís | 0.643 | +0.411 [+0.312, +0.509] |
| `elevation_mean` | Manavgat | 0.232 | Muğla | 0.611 | +0.379 [+0.274, +0.476] |
| `slope_mean` | Manavgat | 0.400 | Muğla | 0.637 | +0.237 [+0.158, +0.313] |
| `slope_mean` | Manavgat | 0.400 | Montiferru | 0.652 | +0.252 [+0.100, +0.389] |
| `lst_anomaly_mean` | Bejís | 0.418 | Evia | 0.640 | +0.222 [+0.129, +0.316] |
| `current_lst_mean` | Muğla | 0.325 | Manavgat | 0.665 | +0.340 [+0.260, +0.413] |
| `current_lst_mean` | Evia | 0.377 | Manavgat | 0.665 | +0.288 [+0.195, +0.384] |
| `current_tvdi_mean` | Muğla | 0.336 | Manavgat | 0.677 | +0.341 [+0.253, +0.422] |
| `current_tvdi_mean` | Evia | 0.362 | Manavgat | 0.677 | +0.315 [+0.221, +0.413] |
| `current_tvdi_mean` | Montiferru | 0.356 | Manavgat | 0.677 | +0.322 [+0.161, +0.453] |
| `downscaled_lst_mean` | Muğla | 0.307 | Manavgat | 0.683 | +0.376 [+0.295, +0.451] |
| `downscaled_lst_mean` | Evia | 0.377 | Manavgat | 0.683 | +0.307 [+0.209, +0.405] |
| `fused_lst_mean` | Muğla | 0.325 | Manavgat | 0.666 | +0.341 [+0.261, +0.413] |
| `fused_lst_mean` | Evia | 0.376 | Manavgat | 0.666 | +0.291 [+0.198, +0.386] |

There are fourteen reversals between pairs, across **seven** features, and thirteen of them involve
Manavgat. Under the original label there were three, across two features: elevation and the LST
anomaly. The feature-removal analysis of Section 3.11 keeps these two and does not re-select.
Twenty-six further pairs reverse at the point estimate only, and they are not counted. The strict
criterion reduces the number of findings: a difference interval on the pair (the test of Section
S1.12) would support seventeen further reversals. None of the fourteen is corrected for
multiplicity; Table S30 gives the corrected counts.

## S2.1 The transfer matrix in precision-recall terms

ROC-AUC is used in the main text so that the results can be compared with the susceptibility
literature. A susceptibility map is used to rank areas, so precision-recall measures its practical
value. At target prevalences of 7.0 to 28.7 %, the two measures can differ strongly. Values are read
from the step9b exports of the re-frozen outputs
(`paper/labelfix_rerun/round5/tables/corrected/*/step9b_metrics.json`).

**Table S11. Thermal transfer, PR-AUC against the no-skill baseline.** The baseline is the burned
prevalence of the target. Lift is PR-AUC divided by this baseline; a lift of 1 is no better than a
random ranking. Ordered by lift. Checked row by row by `paper/code/appendix_tables.py`. PR-AUC
intervals at 2-cell and 10-cell blocking for every direction are in
`paper/labelfix_rerun/round7/r7a_pr_auc_10cell.csv`.

| Direction | ROC-AUC | PR-AUC | No-skill | Lift |
|---|---:|---:|---:|---:|
| Evia → Manavgat | 0.677 | 0.321 | 0.143 | **2.24** |
| Manavgat → Evia | 0.654 | 0.407 | 0.287 | 1.42 |
| Bejís → Montiferru | 0.594 | 0.289 | 0.212 | 1.36 |
| Evia → Montiferru | 0.647 | 0.283 | 0.212 | 1.34 |
| Bejís → Muğla | 0.618 | 0.093 | 0.070 | 1.33 |
| Muğla → Evia | 0.653 | 0.379 | 0.287 | 1.32 |
| Montiferru → Bejís | 0.548 | 0.093 | 0.072 | 1.28 |
| Montiferru → Muğla | 0.619 | 0.089 | 0.070 | 1.27 |
| Evia → Muğla | 0.577 | 0.086 | 0.070 | 1.23 |
| Muğla → Bejís | 0.583 | 0.088 | 0.072 | 1.22 |
| Manavgat → Montiferru | 0.518 | 0.243 | 0.212 | 1.15 |
| Montiferru → Evia | 0.586 | 0.317 | 0.287 | 1.11 |
| Muğla → Montiferru | 0.531 | 0.214 | 0.212 | 1.01 |
| Manavgat → Muğla | 0.438 | 0.060 | 0.070 | **0.85** |
| Evia → Bejís | 0.448 | 0.059 | 0.072 | **0.82** |
| Montiferru → Manavgat | 0.404 | 0.113 | 0.143 | **0.79** |
| Bejís → Evia | 0.383 | 0.226 | 0.287 | **0.79** |
| Manavgat → Bejís | 0.396 | 0.054 | 0.072 | **0.75** |
| Muğla → Manavgat | 0.345 | 0.101 | 0.143 | **0.70** |
| Bejís → Manavgat | 0.314 | 0.098 | 0.143 | **0.68** |
| **Mean** | **0.527** | **0.181** | **0.157** | **1.13** |

Seven directions are below their own no-skill baseline, and only one is above twice its baseline.
The seven are the same seven that are below chance on ROC-AUC, as expected for a reversed ranking. At
1 km blocking, all seven have PR-AUC intervals fully below the baseline. At 5 km blocking two do:
Bejís to Manavgat [0.067, 0.132] and Muğla to Manavgat [0.071, 0.135], against 0.143. Section 4.4
shows that the number of directions below chance depends largely on the study areas.

## S2.2 The same-geography event pair, in full

Section S1.13 reports this comparison. Section 4.4 shows that its elevation reversal is caused by
the study area, and Section S1.13 explains why its thermal channels are not evaluated. The values per
feature are kept here because this comparison led to the frame test.

**Table S12. Signed univariate feature-burned AUC, Muğla 2021 versus 2022.** Raw AUC against
`burned`, not folded to max(AUC, 1 − AUC); 10-cell (≈ 5 km) spatial-block bootstrap, 1,000
replicates, seed 42 (Section 3.14). Analysis population 41,730 rows / 2,911 burned (2021) and 38,790
rows / 331 burned (2022). **Blocks of 5 km with burned cells: 70 in 2021 and 11 in 2022.** The note
to Table 1 sets sixteen as the minimum for this blocking, so the 2022 intervals are indicative, like
the 20-cell row of Table 1. The 2022 fire is also one compact scar, so its eleven blocks are next to
each other. Read from
`paper/step9g_raw/.../mugla_2021__mugla_2022_event_relative/step9g_direction_reversal_table.csv`.

| Feature | 2021 AUC [95 % CI] | 2022 AUC [95 % CI] | Reversal |
|---|---|---|---|
| **elevation_mean** | **0.611 [0.532, 0.690]** | **0.296 [0.230, 0.355]** | **bootstrap-supported** |
| current_lst_mean | 0.325 [0.271, 0.382] | 0.515 [0.434, 0.580] | point only |
| current_tvdi_mean | 0.336 [0.275, 0.398] | 0.594 [0.475, 0.674] | point only |
| downscaled_lst_mean | 0.307 [0.253, 0.366] | 0.508 [0.435, 0.571] | point only |
| fused_lst_mean | 0.325 [0.272, 0.383] | 0.519 [0.436, 0.583] | point only |
| ndvi_mean | 0.662 [0.616, 0.704] | 0.707 [0.624, 0.777] | none |
| slope_mean | 0.637 [0.582, 0.686] | 0.558 [0.468, 0.634] | none |
| lst_anomaly_mean | 0.485 [0.395, 0.566] | 0.380 [0.249, 0.502] | none |
| tvdi_difference_mean | 0.490 [0.396, 0.575] | 0.397 [0.265, 0.514] | none |

## S2.3 The evaluation frames, and the signed associations they produce

Section 4.4 gives these results. The values per region are given here.

**Table S13. Geometry of the five study areas.** Natural-vegetation population. Distance is the
Euclidean distance to the nearest burned cell on the 500 m grid, at 0.45 km per cell. Corrected
Manavgat label. Computed by `paper/code/appendix_tables.py` from the step8a tables (read through
`paper/code/_canonical.py`, which checks the sha256 of each file), as in
`paper/code/verify_aoi_frame.py`.

| Region | cells | burned | median distance to burned | share beyond 10 km |
|---|---:|---:|---:|---:|
| Manavgat | 20,511 | 2,935 | 13.1 km | **58.5 %** |
| Bejís | 15,190 | 1,100 | 13.5 km | **63.1 %** |
| Muğla | 41,730 | 2,911 | 11.3 km | 55.3 % |
| Evia | 9,298 | 2,664 | 8.0 km | 43.7 % |
| Montiferru | 2,544 | 539 | 2.7 km | **2.1 %** |

**Table S14. Signed univariate AUC, original study area against a 10 km collar.** Point estimates.
The intervals used for the reversal test are given in the text and in `collar_frame_bootstrap.csv`
(10-cell blocks, 1000 replicates, seed 42). Signed and not folded to max(AUC, 1 − AUC), so a value
below 0.5 shows a direction, not weakness. The collar removes no burned cells in any region. Full
frame from the source of Table S9; collar from
`paper/labelfix_rerun/code/aoi_frame_auc_frozen_mugla.csv` (the collar analysis with Muğla read from
its canonical file). Checked row by row by `paper/code/appendix_tables.py`. On every row, Manavgat is
on the other side of 0.5 from the other regions, also on the collar.

| Signed univariate AUC | Manavgat | Bejís | Muğla | Evia | Montiferru | straddles 0.5 |
|---|---:|---:|---:|---:|---:|---|
| elevation, full frame (Table S9) | **0.232** | 0.643 | 0.611 | 0.541 | 0.584 | **yes** |
| elevation, 10 km collar | **0.376** | 0.614 | 0.606 | 0.648 | 0.581 | **yes** |
| current LST, full frame | **0.665** | 0.477 | 0.325 | 0.377 | 0.370 | **yes** |
| current LST, 10 km collar | **0.522** | 0.405 | 0.332 | 0.286 | 0.376 | **yes** |
| current TVDI, full frame | **0.677** | 0.517 | 0.336 | 0.362 | 0.356 | **yes** |
| current TVDI, 10 km collar | **0.527** | 0.454 | 0.342 | 0.250 | 0.361 | **yes** |

**Table S15. Region summary: populations and gate results.** Counts from the Step 8A dataset
statistics of each region; gate fractions from the burned-landcover gate output of each region. TSG =
the natural-vegetation population (tree, shrub and grass). The TSG columns use the modelled
population, `burnable_tree_shrub_grass` **and** `valid_for_modeling == True`, on which every model in
this paper was fitted and scored. Counts are computed from the step8a tables, and gate fractions are
read from the gate output of each region (`paper/labelfix_rerun/round5/tables/corrected/gates/`).
Checked row by row by `paper/code/appendix_tables.py`.

| Region | Total cells | Valid cells | Burned | Prevalence (all valid) | TSG cells | Burned in TSG | TSG prevalence | Burned natural-veg fraction | Gate verdict |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat 2021 | 24,150 | 24,087 | 3,046 | 0.126 | 20,511 | 2,935 | 0.143 | 0.955 | pass |
| Bejís 2022 | 15,759 | 15,759 | 1,103 | 0.070 | 15,190 | 1,100 | 0.072 | 0.991 | pass |
| Muğla 2021 | 73,098 | 73,045 | 3,026 | 0.041 | 41,730 | 2,911 | 0.070 | 0.958 | pass |
| North Evia 2021 (extended) | 22,925 | 22,906 | 2,788 | 0.122 | 9,298 | 2,664 | 0.287 | 0.945 | pass |
| Montiferru 2021 | 3,234 | 3,173 | 697 | 0.220 | 2,544 | 539 | 0.212 | 0.723 | pass |

**Table S16. Cross-region transfer matrix, thermal model, TSG population.** Target ROC-AUC with
2-cell spatial-block bootstrap 95% CIs (1000 replicates). CORAL is applied after region-wise
z-scoring (λ = 10⁻⁵). Generated by `paper/code/table_b9.py` from the re-frozen outputs
(`paper/labelfix_rerun/round5/matrix20_official.csv`).

| Direction | Raw | Region-wise z-score | CORAL |
|---|---|---|---|
| Manavgat→Bejís | 0.396 [0.373, 0.422] | 0.450 [0.423, 0.477] | 0.467 [0.441, 0.491] |
| Bejís→Manavgat | 0.314 [0.296, 0.332] | 0.302 [0.282, 0.323] | 0.406 [0.388, 0.423] |
| Manavgat→Muğla | 0.438 [0.418, 0.456] | 0.427 [0.408, 0.444] | 0.417 [0.398, 0.436] |
| Muğla→Manavgat | 0.345 [0.331, 0.359] | 0.485 [0.468, 0.502] | 0.476 [0.460, 0.493] |
| Manavgat→Evia | 0.654 [0.633, 0.676] | 0.529 [0.504, 0.553] | 0.504 [0.481, 0.528] |
| Evia→Manavgat | 0.677 [0.658, 0.697] | 0.404 [0.386, 0.421] | 0.417 [0.399, 0.435] |
| Bejís→Muğla | 0.618 [0.601, 0.635] | 0.518 [0.501, 0.535] | 0.507 [0.489, 0.524] |
| Muğla→Bejís | 0.583 [0.561, 0.607] | 0.535 [0.512, 0.557] | 0.560 [0.538, 0.581] |
| Bejís→Evia | 0.383 [0.363, 0.402] | 0.532 [0.509, 0.551] | 0.499 [0.479, 0.518] |
| Evia→Bejís | 0.448 [0.426, 0.470] | 0.549 [0.524, 0.575] | 0.549 [0.525, 0.573] |
| Muğla→Evia | 0.653 [0.636, 0.671] | 0.561 [0.543, 0.580] | 0.563 [0.545, 0.582] |
| Evia→Muğla | 0.577 [0.560, 0.593] | 0.501 [0.485, 0.518] | 0.530 [0.515, 0.546] |
| Montiferru→Manavgat | 0.404 [0.385, 0.422] | 0.388 [0.367, 0.408] | 0.436 [0.416, 0.456] |
| Manavgat→Montiferru | 0.518 [0.474, 0.563] | 0.527 [0.484, 0.568] | 0.505 [0.461, 0.547] |
| Montiferru→Bejís | 0.548 [0.521, 0.578] | 0.574 [0.552, 0.596] | 0.569 [0.548, 0.591] |
| Bejís→Montiferru | 0.594 [0.560, 0.631] | 0.550 [0.500, 0.601] | 0.574 [0.530, 0.621] |
| Montiferru→Muğla | 0.619 [0.604, 0.634] | 0.576 [0.562, 0.589] | 0.565 [0.550, 0.579] |
| Muğla→Montiferru | 0.531 [0.495, 0.568] | 0.587 [0.549, 0.624] | 0.584 [0.547, 0.623] |
| Montiferru→Evia | 0.586 [0.565, 0.606] | 0.630 [0.611, 0.649] | 0.624 [0.605, 0.641] |
| Evia→Montiferru | 0.647 [0.608, 0.682] | 0.568 [0.528, 0.609] | 0.581 [0.539, 0.623] |

## S2.4 The transferability-diagnostics tables

**Table S17. All similarity measures against raw thermal transfer (20 ordered directions).**
Spearman ρ with pair-based bootstrap 95 % CIs. Exp. = expected sign. Rows with n = 12 exist only for
the four-region subset, because these measures were not produced for Montiferru. The supported
conditional rows use the 18 directions with at least one supported feature. Every row is from
`paper/labelfix_rerun/round5/s6_diagnostics_20.csv`, checked by `paper/code/appendix_tables.py`. The
twenty measures were defined on 8 August 2026 and were not re-selected after the label correction.

| Diagnostic | Family | Exp. | n dir | Spearman ρ [95% CI] | CI excludes 0 |
|---|---|---|---|---|---|
| Agreement fraction, supported features | P(y\|x) conditional | + | 18 | +0.52 [−0.27, +0.87] | no |
| Cosine, supported features | P(y\|x) conditional | + | 18 | +0.49 [−0.24, +0.87] | no |
| Cosine, all 9 features | P(y\|x) conditional | + | 20 | +0.44 [−0.29, +0.80] | no |
| Vector Spearman, all 9 | P(y\|x) conditional | + | 20 | +0.43 [−0.21, +0.80] | no |
| Agreement count, all 9 | P(y\|x) conditional | + | 20 | +0.47 [−0.29, +0.80] | no |
| Schoener's D, 1-D mean | P(x\|y=1) niche | + | 20 | +0.10 [−0.53, +0.63] | no |
| Warren's I, 1-D mean | P(x\|y=1) niche | + | 20 | +0.19 [−0.43, +0.77] | no |
| Schoener's D, PCA-2D | P(x\|y=1) niche | + | 20 | +0.03 [−0.59, +0.63] | no |
| Warren's I, PCA-2D | P(x\|y=1) niche | + | 20 | −0.03 [−0.66, +0.56] | no |
| Mahalanobis, burned centroids | P(x\|y=1) niche | − | 20 | −0.22 [−0.82, +0.42] | no |
| Domain-classifier AUC | P(ix) marginal | − | 20 | −0.33 [−0.81, +0.36] | no |
| Predictor-space mean dissimilarity | P(ix) marginal | − | 12 | −0.13 [−0.67, +0.37] | no |
| Predictor-space p95 dissimilarity | P(ix) marginal | − | 12 | −0.15 [−0.68, +0.24] | no |
| Fraction inside weighted AoA | P(ix) marginal | + | 12 | +0.21 [−0.48, +0.62] | no |
| Fraction inside unweighted support | P(ix) marginal | + | 12 | +0.08 [−0.92, +0.76] | no |
| Climatic distance | P(ix) marginal | − | 12 | +0.03 [−0.84, +0.84] | no |
| Geographic distance | geographic | − | 12 | −0.17 [−0.87, +0.84] | no |
| Regime distance, log effective-N | P(y) structure | − | 20 | +0.11 [−0.67, +0.80] | no |
| Regime distance, largest share | P(y) structure | − | 20 | +0.11 [−0.66, +0.77] | no |
| Vector Spearman, supported (≥3 feats) ‡ | P(y\|x) conditional | + | 6 | +0.96 [+0.85, +0.96] | degenerate interval; not interpreted |

*Table note.* A null row means that the measure was **not shown to order transfer** in this design.
It does not mean that the measure cannot order transfer. With ten independent region pairs the power
is low, and the intervals are wide enough to include moderate true correlations in either direction.
‡ The last row belongs to the set of measures fixed in advance, so it stays in the table. It is
defined on six directions only, and its interval is degenerate (the upper bound equals the point
estimate), so it is not interpreted and cannot be compared with the other nineteen.

**Under the original label**, the two supported-feature variants excluded zero (+0.84 and +0.81 over
sixteen directions). Both choose their predictors by whether the bootstrap intervals of two regions
exclude 0.5, a choice made on the same data. Under the corrected label neither excludes zero (+0.52
and +0.49 over eighteen directions), and no interpretable row does (see Section S3.5(viii) on why
measures based on interval support are unstable).

**Equal-sample check.** The families use different samples: twelve directions for the marginal,
applicability, climatic and geographic rows, eighteen for the supported conditional rows, and twenty
for the others. Every row was recomputed on the common subset of twelve directions, and again on the
sixteen directions where the supported conditional rows are defined. Every interpretable row still
includes zero. On the common twelve, the supported conditional rows give +0.41 [−0.42, +0.88] and
+0.46 [−0.56, +0.84]. The published values are reproduced to 4.4 × 10⁻⁵. Source:
`paper/labelfix_rerun/round5/out_official/diagnostics_common_subset.json`.

**Table S18. The most and least environmentally similar pairs, on both frames.** Schoener's *D* is
computed over burned cells only, so it does not change with the collar. Transfer values are the two
ordered directions of each pair. Ranks are out of the twenty directions on the collar. Corrected
Manavgat label. Schoener's *D*, per-feature *D* and transfer on the original study areas are read from
the source of Fig. 8, `paper/labelfix_rerun/round5/out_official/figure_contrast_pairs.json`. Collar
transfer and ranks are from the source of Table S8, `paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv`,
and the AoA shares from `paper/labelfix_rerun/round5/collar/aoa_directed_pair_summary.csv`. Every
cell is checked against these files at build time (`paper/figures/fig8_contrast_pairs.py`).

| | Manavgat and Muğla | Bejís and Montiferru |
|---|---|---|
| Schoener's *D*, mean 1-D | **0.799** (highest) | **0.479** (lowest) |
| per-feature *D* | 0.74 to 0.87 | 0.23 to 0.77 |
| transfer, frames as drawn | 0.438, 0.345 | 0.594, 0.548 |
| transfer, 10 km collar | 0.493, 0.433 | 0.669, 0.624 |
| rank of 20 on the collar, from the bottom | 4th, 2nd | 16th, 12th |
| target cells inside the AoA | 0.876, 0.531 | n/a |

# S3 Protocol detail and limitations

These protocols are given here in full. They are needed only to check the related results, not to
follow the main argument. Sections 3.2 to 3.4, 3.7, 3.9, 3.10, 3.13 and 3.14 summarise them.

## S3.1 Burned-area label, the reconstructed analysis grid, and the admissibility gate

Labels come from MODIS MCD64A1 Collection 6.1 (`MODIS/061/MCD64A1`), retrieved through Google Earth
Engine [@Gorelick2017]. Its omission and commission errors [@Boschetti2019] limit every model here.
The product is exported onto the 30 m EPSG:4326 reference grid used by the rest of the pipeline. Each
native ~500 m observation is therefore copied to the 30 m pixels below it.

The analysis grid is therefore **reconstructed, not native**. The 30 m grid is divided into
non-overlapping blocks of `round(500 / 30) = 17 × 17` pixels, which gives a nominal cell edge of
510 m. Each cell is identified by its block indices `row_500m` and `col_500m`. This approximates the
MODIS sinusoidal cell but does not reproduce it, because it is anchored to the Landsat/EPSG:4326
reference grid. Blocks at the edges are cut. The cell is square in degrees but not on the ground:
about 510 m from north to south and 390 to 407 m from east to west. Its area is therefore 0.199 to
0.208 km², against 0.215 km² for the native MODIS cell (463 m edge). Every block size in this paper
refers to the north-south dimension. The collar step of 0.45 km per cell (Section 3.12) lies between
the two cell dimensions, so collar radii are nominal to within about 15 %.

The burn date of a cell is the **mode** of the burned sub-pixel day-of-year values in the block, and
it is tested against the label window of the region. The exported raster has no burned pixels outside
the window, so in this dataset one burned sub-pixel inside the window makes the cell burned. This can
extend each scar by up to one cell at its edge, and it can mark a water cell as burned where the
product does. The primary population keeps only cells dominated by natural vegetation, so water is
excluded. The fraction of burned sub-pixels that agree with the modal date is recorded as
`burn_date_pixel_agreement_fraction`, but no threshold is applied. The label never affects whether a
cell is modelled: unburned, all-no-data and out-of-window cells all stay in the negative class.

Earlier burning is handled differently in each region; this is given in Section S3.1.1. The only
historical exclusion applied by design removes the 2021 Muğla scar from the 2022 experiment of
Section 3.14.

Before any modelling, each region passes a gate that asks one question: what fraction of the burned
cells is dominated by natural vegetation? A region is admitted as a wildfire case when this fraction
is at least 0.50 and at least 30 burned cells are present. It is rejected as a cropland control when
the cropland fraction is at least 0.50. The gate uses ESA WorldCover classes aggregated to the same
cells. It separates burning of natural fuel from stubble burning after harvest, which MCD64A1 does
not distinguish. The results are given in Section 4.1.

### S3.1.1 Pre-label and historical burning, by region

Two kinds of earlier burning can affect a label. **Pre-label burning** is burning inside the
predictor window of the region, which the pipeline can remove. **Historical burning** is burning in
the five previous years, which no region screens for. Table S34 gives both, recomputed from the
MCD64A1 export of each region (`paper/code/ems_labels_1_prelabel.py`, `ems_labels_2_history.py`;
outputs `paper/labelfix_rerun/labels/r1_prelabel.json`, `r2_history.json`).

**Table S34. Earlier burning by region, natural-vegetation population.**

| Region | Pre-label cells removed | Pre-label burned cells retained | Historical-burn cells (five years) | … of which burned again in the event |
|---|---:|---:|---:|---:|
| Manavgat 2021 | none needed (no pre-label burning) | 0 | 0 | 0 |
| Bejís 2022 | exclusion not applied | 48 (49 in all valid cells; 10 burned again) | 163 | 0 |
| Muğla 2021 | 49 | 0 | 194 | 25 |
| North Evia 2021 | 16 | 0 | 366 | 88 |
| Montiferru 2021 | 61 | 0 | 58 | 32 |

Excluding the historically burned cells lowers the mean paired transfer contribution from +0.007 to
+0.003 (at 10-cell blocking: 5 positive, 4 negative and 11 uncertain verdicts, against 6, 5 and 9).
The within-region gain stays positive with interval support in every region: +0.062 (no change),
+0.055, +0.088, +0.162 and +0.111 for Manavgat, Bejís, Muğla, Evia and Montiferru.

### S3.1.2 The Manavgat label correction

**The Manavgat 2021 label is corrected.** The label first used for Manavgat was exported on 8 July
2026. This was before the month-alignment fix of the MCD64A1 query in the pipeline (commit 183be42,
11 July), and the export was not renewed. It therefore missed the first four days of the fire, 28 to
31 July. The error was an old export, not a code error. The corrected label only adds burned cells.
No cell that burned under the original label becomes unburned, and no predictor or validity flag
changes. In the primary population, the number of burned cells rises from 784 to 2,935. The Manavgat
outputs were re-frozen with the pipeline at commit 6381f4c. Two small changes were made: a one-line
patch to the window-closure diagnostic, and a runtime setting of the Earth Engine project
(`thermaltwin`). Python 3.12.10 and scikit-learn 1.9.0 were used (versions in `ENVIRONMENT.md`). The
correction, the re-freeze and the control run were carried out by the corresponding author with
AI-assisted code (Section 3.13). They were not repeated by the author of the pipeline. This pipeline
version writes one extra column, a flag for burning in earlier years, and it excludes no Manavgat
cell. In a control run, the original label was re-frozen with the same code and environment. It
reproduced the published outputs to within 10⁻⁵. The exceptions are listed in the manifest: file
paths, the column list, and one older pair that differs at the level of random-forest thread
nondeterminism. Differences between the two runs are therefore caused by the label alone. The
reproduction check of Section 3.13 covers the re-frozen outputs. The manifest, hashes and scripts
are released in `paper/data/manavgat_2021/refreeze/`.

### S3.1.3 Effect on Table 1

The Manavgat rows use the corrected label. It adds burned cells (784 to 2,935 in the primary
population) and changes no predictor (Section 3.2). The rows become stronger, not weaker. Absolute
AUCs rise by 0.04 to 0.11 across the three block sizes, and the gain holds at every scale. The 1 km
interval becomes narrower, from [+0.055, +0.079] to [+0.060, +0.073], because the region now has 814
blocks of 2 cells with burned cells instead of 235.

## S3.2 Transferability diagnostics versus transfer

Twenty similarity measures from five families are each rank-correlated with the same quantity, the
raw thermal transfer AUC over the twenty ordered directions, with one common pair-based bootstrap.
The families are marginal predictor-distribution measures P(x), burned-niche overlap P(x|y=1),
burned-pattern structure P(y), and conditional feature-response direction P(y|x).

The **marginal** family includes area-of-applicability dissimilarity in scaled, importance-weighted
predictor space [@Meyer2021; @Meyer2022; @Ludwig2023], climatic and geographic distance, and a domain
classifier trained to separate source cells from target cells. The **niche-overlap** family includes
Schoener's D [@Schoener1968] and Warren's I [@Warren2008] over the burned cells of each region. The
**regime** family includes counts of burned patches and effective patch counts. The **conditional**
family is the sign-agreement index: the fraction of predictors whose signed association points the
same way in both regions, computed over all predictors and over the predictors with interval support.

Two properties of this design limit what it can show. First, the set of measures was recorded on
8 August 2026, together with its results under the original label (commit abd6a4b on the `history-archive` branch of the public repository,
which keeps the development history without internal notes). It was not re-selected after the label correction. This is a
record, not a pre-registration. Second, with five regions the effective sample is ten unordered
pairs, and nineteen measures are evaluated at this power without family-wise error control. Where a
measure passes an interval test but not a Bonferroni threshold, both results are reported.

## S3.3 Same-geography event-to-event comparison (Muğla 2021 versus 2022)

Muğla is the only region in which a second fire is analysed on the same study area and grid. This
allows the direction of feature-label associations to be compared with the place held fixed. The
2022 windows are set relative to the 2022 fire: a 58-day predictor window that closes the day before
ignition, and a 49-day label window that opens on that day. These lengths are the same as in 2021.

**This is not a clean design for transfer over time, and it is not presented as one.** The 2022 fire
started about six weeks earlier in the season than the 2021 fire, so year and seasonal phase are
confounded, and no difference can be attributed to the year alone. The comparison is between two
fires in one place. The pair is kept out of the twenty-direction matrix, and this is enforced in the
released code.

Two further properties limit the comparison. A historical-burn exclusion applies only to the 2022
population: every cell that burned in 2021 is masked, so the scar of the previous year does not enter
the analysis. This removes 3,073 cells, 2,941 of them in the primary population, and reduces the
population from 41,730 to 38,790 rows (7.0 %). The two populations therefore share 38,789 of 38,790
cells and three identical static predictors. In the 2022-to-2021 direction, no burned target cell is
in the source training data. Section S1.13 describes the consequences.

**Table S19. Study regions, study areas and time windows.** Bounding boxes are in EPSG:4326, as
recorded. Window lengths in brackets are day counts, both ends included. The baseline years are the
four years before each predictor window, with the same calendar dates.

| Region | Bounding box (lon min, lat min, lon max, lat max) | Predictor window | Label window | Baseline years |
|---|---|---|---|---|
| Manavgat 2021 (Türkiye) | 31.05, 36.72, 31.85, 37.35 | 2021-06-01 to 2021-07-27 (57 d) | 2021-07-28 to 2021-08-31 (35 d) | 2017, 2018, 2019, 2020 |
| Bejís 2022 (Spain) | -1.05, 39.68, -0.35, 40.15 | 2022-06-15 to 2022-08-14 (61 d) | 2022-08-15 to 2022-09-30 (47 d) | 2018, 2019, 2020, 2021 |
| Muğla 2021 (Türkiye) | 27.1, 36.6, 28.9, 37.45 | 2021-06-01 to 2021-07-28 (58 d) | 2021-07-29 to 2021-09-15 (49 d) | 2017, 2018, 2019, 2020 |
| North Evia 2021 (Greece) | 23.05, 38.55, 23.85, 39.15 | 2021-06-05 to 2021-08-02 (59 d) | 2021-08-03 to 2021-09-30 (59 d) | 2017, 2018, 2019, 2020 |
| Montiferru 2021 (Italy) | 8.45, 40.05, 8.75, 40.27 | 2021-05-25 to 2021-07-23 (60 d) | 2021-07-24 to 2021-08-31 (39 d) | 2017, 2018, 2019, 2020 |

## S3.4 Predictor provenance, compositing and the downscaler

Ten predictors are used, four baseline and six thermal. All are summarised per cell over the
predictor window, through the chain shown in Fig. 2. All optical and thermal predictors come from
Landsat 8 Collection 2 Level-2 (`LANDSAT/LC08/C02/T1_L2`). They are quality-screened per pixel with
the `QA_PIXEL` band; the water bit is kept on purpose. The coarse thermal input is `MODIS/061/MOD11A1`.

- **NDVI** is the median of Landsat surface reflectance over the predictor window. It is the only
  baseline predictor that changes over time.
- **Elevation** and **slope** come from the Copernicus DEM GLO-30. Its heights are referenced to the
  EGM2008 geoid (EPSG:3855) in metres, according to the product handbook. The pipeline applies no
  datum conversion.
- **Land cover** is ESA WorldCover v200 [@Zanaga2022], used as the dominant class code.
- **Current LST** is the median of Landsat surface temperature over the predictor window, in °C.
- **LST anomaly** is a z-score of the current LST median against the four baseline years. It is set
  to no-data where the baseline standard deviation is below 1.0 °C or there are too few observations.
- **TVDI** and **TVDI difference**. The Temperature-Vegetation Dryness Index [@Sandholt2002] is
  computed in the LST-NDVI space. The wet and dry edges are the 2nd and 98th LST percentiles within
  each of twenty NDVI bins, and the index is limited to [0, 1]. The edges are percentiles of the LST
  values in a given scene, so they are fitted for each study area and window. A TVDI of 0.5 therefore
  means a different moisture state in each region. **TVDI difference** is the raw anomaly of this
  index against the same four baseline years: `tvdi_difference = current_tvdi − mean(baseline_tvdi)`.
  It is in index units, not standard deviations, so it is reported together with the z-scored channel.
- **Downscaled LST** and **fused LST**. A MODIS-to-Landsat downscaling model is trained on the
  predictor window and applied to the full 30 m grid. The fused product equals the observed Landsat
  LST where that is valid, and the downscaled surface only where it is not. Gap-filling therefore
  never replaces or blends a valid observation. The gap-filled share is 0.11 % to 9.70 % by region.
  The downscaler uses coordinates as inputs. This is the only way in which coordinate information
  enters a feature set from which Section 3.13 excludes coordinates. Section S1.7 gives the gain
  without these two channels.

**The six thermal channels carry about two signals.** In the primary population, current, fused and
downscaled LST are correlated at 0.97 to 1.00 in every region. Current LST and TVDI are correlated at
0.88 to 0.98, and the two anomaly channels at 0.71 to 0.94. Two principal components of the six
channels explain 92 % to 98 % of their variance, and their participation ratio is 1.6 to 1.8
(`paper/labelfix_rerun/labels/r4_dimensionality.json`).

**Table S20. Input data.** All retrieved through Google Earth Engine.

| Input | Product and version | Native resolution | Use | Reference |
|---|---|---|---|---|
| Burned area | MODIS MCD64A1 Collection 6.1 (`MODIS/061/MCD64A1`) | 500 m, monthly | label | [@Giglio2018; @MCD64A1] |
| Surface reflectance and temperature | Landsat 8 Collection 2 Level-2 (`LANDSAT/LC08/C02/T1_L2`), `QA_PIXEL` screening, water bit preserved | 30 m | NDVI, current LST, anomaly, TVDI | [@LandsatC2L2] |
| Coarse LST | MODIS MOD11A1 v061 (`MODIS/061/MOD11A1`) | 1 km, daily | downscaled and fused LST (gap-fill 0.11 % to 9.70 %) | [@MOD11A1] |
| Terrain | Copernicus DEM GLO-30 (EGM2008 heights) | 30 m | elevation, slope | [@CopernicusDEM] |
| Land cover | ESA WorldCover v200 (2021) | 10 m | dominant class, gate, population | [@Zanaga2022] |

Compositing uses the median over the predictor window. The anomaly channels refer to four baseline
years (Table S19). WorldCover 2021 is later than four of the five fires (Section 3.4).

## S3.5 Limitations, in full

Section 5.6 lists the limitations that affect the conclusions. All fourteen are given here.

(i) **No weather predictors** are used, so the behaviour of a combined thermal and weather
predictor set is not known.

(ii) **The same-place comparison covers one region only**, and there, year and seasonal phase are
confounded. This cannot be resolved in this study area. The two fires are 42 days apart in median
burn day-of-year, neither year has a second fire at the phase of the other, and a calendar-matched
comparison would have nine burned cells, against a gate minimum of thirty. The 2022 population also
has only eleven blocks with burned cells, against the minimum of sixteen (Section S1.13). Its 331
burned cells do not resolve the thermal reversals at interval level, and the pair keeps the place
fixed but not the population. The two Muğla populations were computed with the unmodified pipeline
code and the same fixed environment, not read from a frozen export.

(iii) **All labels come from one burned-area product**, MCD64A1 [@Giglio2018]. Its omission and
commission errors [@Boschetti2019] limit every model here. Its accuracy in the Mediterranean was
assessed against reference perimeters [@Katagis2022]. A second 500 m product, VIIRS VNP64A1
[@VNP64A1], covers both years but was not used as a label sensitivity.

(iv) **Evia has the most unusual class balance**, even on the extended study area. Its TSG prevalence
is 0.287, the highest in the cohort, against 0.070 to 0.212 in the other four regions.

(v) **Each region contributes one fire season**, so regional concept shift is confounded with the
weather of each fire. Labels from several years are needed to separate them.

(vi) **Point estimates depend on the software version.** Under scikit-learn 1.5.2 instead of 1.9.0,
single-direction AUCs of the frame-transfer matrix move by up to 0.023 for the thermal model and 0.047
for the baseline, and paired differences by up to 0.045. The means move by at most 0.003. One
direction changes interval support on each of the original and 10 km frames
(`paper/labelfix_rerun/round7/sklearn152/compare_vs_1_9_0.json`). All reported numbers come from one
verified version, and exact reproduction needs the archived environment.

(vii) **The low transfer into Manavgat is located but not explained.** Manavgat is the weakest target
(0.435), has the largest matched shortfall (+0.319) and has the most unusual univariate profile in
the cohort. Two processing causes were tested, and neither explains it. The quality screening of its
coarse thermal input moves no signed association by more than 0.005 (Section S1.5), and its elevation
reversal remains on the collar (Section 4.4). Holding elevation reverses its raw LST association
(Section S1.11). This rests on one region and one fire.

(viii) **Measures based on interval support are less stable than the point estimates.** Five to six
of the pipeline's interval bounds lie within 0.01 of 0.5, under both labels. One such flag, the NDVI
of Manavgat, moved the supported-feature cosine on the original study areas from ρ = 0.49 to 0.70,
when two equally valid bootstrap streams disagreed on it. The transfer verdicts are more stable.
Across five bootstrap seeds, every verdict at 1 km blocking is stable, and the paired split of twelve
positive, seven negative and one uncertain holds on every seed. At 5 km blocking, one level verdict
and two paired-delta verdicts change with the seed. Exact counts of supported directions should be
read at this precision.

(ix) **The five study areas are not comparable, and this cohort cannot fully correct this** (Section
4.4). The collar results are reported together with the original results, not instead of them,
because the collar radius is also a choice, and 5 km and 10 km do not agree exactly (0.591 against
0.589). The study areas were fixed earlier in the pipeline, in `repo/`, so they can be restricted but
not extended. Montiferru, whose rectangle is already close to the fire, cannot be given distant cells.
Their independence from the outcomes can also not be fully documented. Only the Montiferru rectangle
follows a rule, and the Manavgat rectangle is dated before its first gate result. For Bejís and Muğla,
the version history cannot show that the rectangle was fixed before the first gate result (Section
3.1). Future studies should fix the study area by a stated accessible-area rule [@Barve2011] before
any predictor is computed.

(x) **Other classifiers are compared by point estimate only.** The main results use a random forest
with unlimited depth, which fits local structure well and extrapolates poorly. Section S1.8 shows that
the transfer result does not depend on this choice. Three other estimators, including a penalised
linear model, range from 0.481 to 0.527 and have eleven to thirteen of twenty directions above chance.
These are point estimates without intervals, so the estimators are not ranked. Other estimator
classes were not tried.

(xi) **Burn timing and elevation are confounded in Manavgat.** The cells that burned in the first four
days lie at a median of 219 m, against 512 m for the later burns and 1,004 m for unburned cells. The
effects of timing and elevation cannot be separated in these data.

(xii) **The quality-screening comparison differs in code version as well as in screening.** The
current pipeline step7 refuses the unscreened MODIS input, because the raster has no nodata tag and
8.1 % exact zeros. The unscreened version therefore uses the step7 of export time, and the screened
version the current one. The two agree on elevation to four decimals and on every other signed AUC to
within 0.005; the largest change is −0.0044 for downscaled LST. The within-region gain moves from
+0.067 to +0.068. The confound could hide an effect only if two effects cancelled (Section S1.5).

(xiii) **The similarity tests rest on ten independent region pairs.** Five regions give twenty
ordered directions, but the two directions of a pair share both regions and are not independent. All
results of Section S1.21, positive and negative, have this low power. With ten pairs, a moderate true
ordering would usually be missed.

(xiv) **The frame cost rests on few scars.** The full comparison of Section 4.3 is defined on seven
scars in three regions. Its scar-level intervals are too narrow, because row A is repeated for each
scar of a region. The region-level estimates (+0.137 over three regions, +0.160 over five) should be
quoted.

## S3.6 Leakage control and reproducibility, in full

A fixed set of forbidden columns is checked at every model fit. Coordinates (`lon`, `lat`, `row`,
`col` and their normalised forms), every burn-date and label-provenance column, and the agreement
fraction are excluded from all feature sets. The check is an assertion in the code. The
natural-vegetation mask is used only to define the population, never as a predictor. Spatial blocking
keeps neighbouring cells in the same fold.

**Reproducibility.** All random processes use seed 42, and every bootstrap uses 1000 replicates. The
transfer and adaptation analysis runs in an environment separate from the pipeline. Every
within-region model was therefore refitted there and compared with the frozen pipeline output, and
the independent adaptation code was compared with the pipeline's own. The within-region results agree
exactly. The twenty CORAL transfers agree to within 1.3×10⁻⁸ with the re-frozen outputs (1.6×10⁻⁷
with the frozen ones), below the tolerance of 10⁻⁶ set in the repository (Section 3.13). All numbers
were produced under scikit-learn 1.9.0 or checked against it. The version sensitivity is given in
Section S3.5(vi).

**Sensitivity analyses.** The within-region results are repeated for three block sizes, four
classifier capacities and, in two regions, a second population. The transfer results are repeated for
both feature sets, the CORAL sweep, the Evia study-area variant and three evaluation frames. Where a
conclusion depends on one of these choices, the dependence is reported (Section S1).

### S3.6.1 Resampling units

Uncertainty is estimated with a spatial-block bootstrap. Let $`\beta_1, \dots, \beta_M`$ be the
blocks of [#eq:block] that contain cells of $`F`$. Replicate $`b`$ draws $`M`$ indices $`u_{bm}`$
uniformly with replacement:

```math {#eq:boot}
F^{*b} = \biguplus_{m=1}^{M} \beta_{u_{bm}}, \qquad \mathrm{CI}_{95} = \left[ Q_{0.025}\{\theta(F^{*b})\}_{b},\; Q_{0.975}\{\theta(F^{*b})\}_{b} \right].
```

Here $`\theta`$ is the statistic and $`Q`$ gives the 2.5 and 97.5 percentiles over 1000
replicates, seed 42. A replicate with only one class is dropped. Differences are formed within each
replicate, so they are paired. The block size of each interval is given with the result. Because
blocks are resampled, the reliability of an interval depends on the number of blocks with at least
one burned cell. These counts are reported with the intervals. Where a verdict rests on too few such
blocks, it is reported as indicative.

The twenty transfer directions are not independent, because each region appears in eight of them.
The **pair-cluster bootstrap** therefore resamples the ten unordered region pairs. Each pair carries
its set $`\pi_p`$ of ordered directions, and the carried values $`\delta_{st}`$ are averaged:

```math {#eq:pair}
\bar{\delta}^{*b} = \frac{\sum_{m=1}^{10} \sum_{(s,t) \in \pi_{u_{bm}}} \delta_{st}}{\sum_{m=1}^{10} |\pi_{u_{bm}}|}.
```

The interval has the same percentile form, with 1000 replicates for the direction-level intervals
of Sections 4.4 and 4.5, and 20,000 for the unit comparison of Table S31. Clustering by target region
replaces $`\pi_p`$ by the four directions that share a target. A quantity with one value per held-out
scar or target region gets a Student t interval over these $`n`$ units:

```math {#eq:tint}
\bar{x} \pm t_{0.975,\,n-1}\, s_x / \sqrt{n}.
```

**The effective sample is therefore ten pairs or five regions for direction-level intervals, and at
most seven scars from three regions for scar-level intervals.**

### S3.6.2 Reproduction of the re-frozen outputs

The transfer analysis runs in an environment separate from the pipeline. The reproduction check of
the repository therefore refitted every within-region model and all twenty CORAL transfers and
compared them with the frozen pipeline output. For Manavgat this output is the one re-frozen on the
corrected label (Section 3.2), produced with the pipeline at commit 6381f4c. Only two changes were
made. A one-line patch lets the window-closure module accept a population column that the corrected
label adds; its diff is released with the re-freeze. A runtime setting points the Earth Engine calls
at the project `thermaltwin`, which changes only the infrastructure. The within-region results agree
exactly, and the transfer directions to within 1.3×10⁻⁸, below the repository tolerance of 10⁻⁶. This
tolerance applies to the CORAL and within-region check. The frame-transfer script of Section 4.4 fits
its forests in parallel, so its values vary between runs by up to 2×10⁻⁶ (1.4×10⁻⁶ in a rerun on
29 September 2026, `paper/labelfix_rerun/round7/`). This is within the tolerance of 10⁻⁵ applied to
it, and the values are stable at the printed precision. The effect of an unpinned library version is
given in Section S3.5(vi).

## S3.7 Transfer-gap decomposition and the concept-shift diagnostic, in full

For each direction, the gap between the within-region skill of the target and the raw transfer
result is split in two parts. One part is what the best label-free adaptation recovers, and the other
is what it does not recover. The recovered fraction is (adapted − raw) / (within − raw), signed and not
clipped, with its interval from the same paired bootstrap. It describes what the two methods tested achieved, with the better one chosen using target labels;
other correction methods were not tested. Section 4.3 shows that the remainder should not be read
as a concept-shift residual, because much of it already appears inside a single region (Section
S1.10).

Concept shift is examined with the **signed univariate association**. For each numeric predictor, the
raw ROC-AUC of the predictor against `burned` is computed in each region and is not folded to
max(AUC, 1 − AUC), so a value below 0.5 shows a direction, not weakness. A reversal is called
bootstrap-supported only when the point estimates of the two regions lie on opposite sides of 0.5
**and the interval of each region excludes 0.5**, under the same 10-cell spatial-block bootstrap. This
is stricter than requiring disjoint intervals. A feature with disjoint intervals, one of which
includes 0.5, has not been shown to point in any direction in that region, so it is recorded as a
point reversal only. Section S2 repeats the rule next to the counts, and
`conditional_similarity_transfer.json` stores it as metadata.

---

### S3.7.1 Degenerate replicates

Replicates with $`|G| < 10^{-6}`$ are dropped.

## S3.8 Label-free adaptation, full specification

**Region-wise z-score.** The numeric features of each region are standardised with the statistics
of that region: source statistics from source data and target statistics from target data, never
pooled. For feature $`j`$ in region $`R`$,

```math {#eq:zscore}
z_{ij} = \frac{x_{ij} - \mu_j^{R}}{\sigma_j^{R}}, \qquad \mu_j^{R} = \frac{1}{n_j^{R}} \sum_{i \in O_j^{R}} x_{ij}, \qquad \sigma_j^{R} = \Big( \frac{1}{n_j^{R}} \sum_{i \in O_j^{R}} (x_{ij} - \mu_j^{R})^2 \Big)^{1/2},
```

where $`O_j^{R}`$ contains the $`n_j^{R}`$ cells with an observed value (ddof 0). A missing value is
first set to $`\mu_j^{R}`$, so it becomes zero, and $`\sigma_j^{R} < 10^{-12}`$ is replaced by 1.
Land cover is not transformed. Target feature statistics, but never target labels, are therefore used
in the adapted models. The classifier is refitted on the z-scored source and applied to the z-scored
target. This removes differences in the mean and variance of each feature.

**CORAL after region-wise z-score.** The source covariance is aligned to the target covariance with
the standard whitening and recolouring map [@Sun2016]. With $`Z_R`$ the $`n_R \times d`$ matrix of
z-scored numeric features, one row per cell,

```math {#eq:coral}
Z_s^{\mathrm{al}} = Z_s\,(C_s + \lambda I)^{-1/2}\,(C_t + \lambda I)^{1/2}, \qquad C_R = \frac{1}{n_R} \sum_{i=1}^{n_R} (z_i - \bar{z}_R)(z_i - \bar{z}_R)^{\top},
```

with $`\lambda = 10^{-5}`$ (ddof 0). Both means are zero after [#eq:zscore], so the mean terms of the
general map are zero. Matrix powers use a symmetric eigendecomposition, with eigenvalues set to at
least $`10^{-12}`$. **The transform is applied to the source only.** The target stays at $`Z_t`$, and
the classifier is refitted on $`Z_s^{\mathrm{al}}`$. Neither method uses a target label, and this is
checked at run time. The sensitivity to λ was tested over nine values on four of the twenty
directions; transfer AUC moved by at most 0.014, and λ was not selected on performance. The λ = 1 of
the original CORAL formulation lies outside this range. The value used throughout is λ = 10⁻⁵
(Section S1.2).

# S4 Target-label recovery curve

## S4.1 Purpose

The main text shows that label-free alignment does not close the transfer gap. This section asks
how much of the gap a small number of target labels can close. It is not a proposed method or an
operational claim, because the labels come from the fire that is predicted. It covers three of the
five regions (Manavgat, Bejís and Muğla) and all six directions among them. Source: the pipeline's
few-shot recovery diagnostic on the corrected label, analysis `7348dfe7…`, released in
`paper/labelfix_rerun/exports/few_shot_recovery_7348dfe7/` (`recovery_curve.csv`,
`repeat_metrics.csv`, `report.md`); every value below is read from it.

## S4.2 Design

The unit of labelling effort is one 10-cell (≈5 km) spatial block of the target. For a budget of k
blocks, k target blocks are drawn from the training folds of a 5-fold spatially blocked split of the
target. Their labels are added to the source training set, and the refitted model is scored on the
held-out target folds. The budgets are 0, 1, 2, 4, 8, 16 and 32 blocks, with ten repeated draws for
every k > 0. Budget 0 is raw transfer. The **ceiling** is a target-only model at the same 10-cell
blocking (0.777 for Muğla, 0.824 for Bejís and 0.882 for Manavgat). It reproduces the pipeline's own
large-block values exactly. The **recovered fraction** is (few-shot − raw) / (ceiling − raw), the
share of the gap between raw transfer and the ceiling that the labels close; it is signed and not
clipped. The intervals are **selection intervals**: the 2.5th and 97.5th percentiles over the ten
block draws. They describe only which blocks were drawn, and no hypothesis test is made.

## S4.3 Result

**Table S22. Few-shot recovery of target ROC-AUC, thermal model, natural-vegetation population.** Raw
= source-only transfer (budget 0); ceiling = target-only model at the same 10-cell blocking. Values
are means over ten repeated block draws.

| Direction | Raw | 1 blk | 2 blk | 4 blk | 8 blk | 16 blk | 32 blk | Ceiling | Gap closed at 32 |
|---|---|---|---|---|---|---|---|---|---|
| Bejís → Manavgat | 0.314 | 0.518 | 0.565 | 0.659 | 0.698 | 0.750 | 0.820 | 0.882 | 89 % |
| Muğla → Bejís | 0.583 | 0.578 | 0.603 | 0.625 | 0.666 | 0.743 | 0.789 | 0.824 | 85 % |
| Manavgat → Bejís | 0.396 | 0.447 | 0.456 | 0.541 | 0.598 | 0.690 | 0.752 | 0.824 | 83 % |
| Muğla → Manavgat | 0.345 | 0.358 | 0.380 | 0.407 | 0.437 | 0.505 | 0.624 | 0.882 | 52 % |
| Manavgat → Muğla | 0.438 | 0.447 | 0.453 | 0.468 | 0.490 | 0.532 | 0.571 | 0.777 | 39 % |
| Bejís → Muğla | 0.618 | 0.576 | 0.577 | 0.578 | 0.598 | 0.637 | 0.666 | 0.777 | 30 % |

**At 32 blocks, three of six directions close 83 to 89 % of the gap to the ceiling.** Two of these
three started below chance. The other three close 30 to 52 %. Thirty-two blocks contain 2,740 to
2,970 labelled cells, 7 to 20 % of the natural-vegetation population of the target. This is not a
small budget. For Bejís, the 32 labelled blocks contain on average 880 of its 1,100 burned cells, and
for Manavgat about 1,800 of 2,935.

**Recovery is slow where transfer is worst.** Muğla → Manavgat has the largest gap between raw
transfer and the ceiling. It is still below 0.5 after 8 labelled blocks and closes 52 % at 32.

**Small budgets harm the direction that already transfers.** Bejís → Muğla is above chance without
labels (0.618), and target labels help it least. The curve is below the raw value at 1, 2, 4 and 8
blocks (0.576 to 0.598), rises above it only at 16 blocks, and closes 30 % at 32.

## S4.4 Limits

1. **Three regions, six directions.** Evia and Montiferru are not included, so this covers six of
   the twenty directions and cannot cover all five regions. Six directions cannot support a general
   label budget, so none is given.
2. **It needs labelled target cells** from the fire that is predicted. Nothing here is a label-free
   method, and nothing here changes the negative result for label-free alignment. Labels from earlier
   fires in the same region were not tested.
3. **The interval is a selection interval. At the largest budgets it becomes narrow because the pool
   of blocks is used up, not because the value is well estimated.** Per outer fold, the target has on
   average about 12 blocks with both classes in Bejís, 29 in Manavgat and 48 in Muğla. At 16 and 32
   blocks, the draws therefore use almost all of these blocks and select almost the same set
   (`direction_budget_feasibility.csv`).
4. **The ceiling is the 10-cell target-only value**, not the ≈1 km within-region value of Table 1,
   so it is lower. The recovered fractions can only be read against this matched ceiling, and on the
   original study areas, which are not comparable across regions (Section 4.4).

# S5 Code

The analysis code is public at <https://github.com/dryuemco/thermal-twin> under the MIT licence,
and the version used for this paper is archived at Zenodo (https://doi.org/10.5281/zenodo.23035271).
This section is a guide to it; the README of the repository gives the same information. The satellite
processing pipeline is a separate public repository,
<https://github.com/emrehann17/satellite-thermal-digital-twin> (MIT licence). The re-frozen Manavgat
outputs were produced at its commit `6381f4c`. The outputs of the other regions were produced at
earlier commits and are reproduced by it (Section S3.6.2).

| Path | Role |
|---|---|
| `paper/code/` | Analysis and verification scripts. `_canonical.py` loads every modelling dataset, verifies its SHA-256 and asserts the leakage exclusions of Section 3.13 at every fit. |
| `paper/code/appendix_tables.py` | Rebuilds Tables S2 to S7 and S9 to S18 row by row from source files whose SHA-256 values are pinned in `paper/labelfix_rerun/round5/tables/SOURCES.sha256`, and compares them with this document. |
| `paper/figures/` | One script per figure. Each asserts every plotted value against the frozen outputs and the manuscript text, and checks its layout. |
| `paper/figures/check_all.py` | Runs all figure scripts and `appendix_tables.py`, restores the committed outputs byte for byte, and exits 0 when everything passes. |
| `paper/tex/` | Builds the manuscript and this document from their Markdown sources and checks the port: every number survives, and every cross-reference, citation and supplementary reference resolves. |
| `paper/labelfix_rerun/` | The corrected-label outputs from which every corrected number is read: `code/`, `geometry/`, `inference/`, `labels/` and `round3/` to `round7/` hold the analysis outputs, `pipeline/` the re-frozen pipeline outputs for Manavgat, and `exports/` the released pipeline diagnostics (few-shot recovery, CORAL λ sweep, window closure), each with its SHA-256 in `exports/SHA256SUMS.txt`. |

All commands are run from the repository root. The environment is Python 3.12.10 with NumPy 2.4.4,
pandas 3.0.2 and scikit-learn 1.9.0, fixed in `ENVIRONMENT.md`. Point estimates depend on the
scikit-learn version (Section S3.5(vi)). Fig. 1 also needs cartopy; without it, `check_all.py`
reports this figure as skipped. Tables S1 and S20 to S34 and the values in the text are not checked by
`appendix_tables.py`; they name their source files in their captions or text.

# S6 Data

All satellite inputs are public and were retrieved through Google Earth Engine (Table S20). No
proprietary or restricted data were used.

The five modelling datasets are in the analysis repository, one per region, as
`paper/data/<region>/step8a_500m_modeling_dataset.parquet`. Each is checked on load against the
SHA-256 recorded in `paper/code/_canonical.py`. For Bejís, Muğla, North Evia and Montiferru this hash
equals the pipeline's own record. For Manavgat the file is the corrected-label re-freeze (SHA-256
`5a5e876c…`; Section S3.1.2). The pipeline's record still names the original-label table (SHA-256
`054a1961…`), which is not in the repository and can be regenerated by the pipeline. The frozen
numeric outputs behind every table and figure are in the same repository, identified by the paths
and hashes given in the table captions and in `SOURCES.sha256`. The data derived from Landsat, MODIS,
the Copernicus DEM and ESA WorldCover remain subject to the terms of these products, which are given
in the Declarations.
