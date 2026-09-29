# Supplementary Material

Supplementary material for *Evaluation geometry and the limits of cross-region transfer in pre-fire
thermal wildfire prediction*.

Section S1 reports the sensitivity analyses and the detail behind the Results; Section S2 the
supporting tables; Section S3 the protocol detail and the limitations; Section S5 the target-label
recovery curve; Section S6 the code and Section S7 the data. Tables are numbered S1 to S34, independently of the sections, and supplementary equations are
numbered (S1), (S2), and so on. Every value is read from a released output, named by its path in the repository
<https://github.com/dryuemco/thermal-twin>; paths beginning `paper/labelfix_rerun/` hold the
corrected-label outputs. Values computed under the original Manavgat label are marked "original
label" wherever they appear.

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
  - S1.20 The frame test, elaborated
  - S1.21 The transfer matrix and adaptation, elaborated
  - S1.22 The similarity diagnostics
  - S1.23 Additional robustness analyses
- S2 Supporting tables
- S3 Protocol detail and limitations
- S5 Target-label recovery curve
- S6 Code
- S7 Data

Section S1.19 of earlier versions is merged into Section S5, so the numbering skips it; the S4
record of earlier versions is replaced by Sections S1.22 and S2.4.

# S1 Sensitivity analyses and detail

Each arm below varies one design choice and leaves everything else fixed. None changes a conclusion
in the main text. Section S1.6 is the exception in one respect: it is not a robustness check but a
test of a claim the introduction makes, and the claim is not upheld.

## S1.1 Evia AOI and prevalence

The raw transfer arms that involve Evia with Bejís, Manavgat and Muğla were repeated with the
legacy, high-prevalence Evia box. Every qualitative conclusion is unchanged. Thermal raw transfer AUCs
move by up to 0.134, the largest being Evia to Manavgat at 0.543 with the legacy box against 0.677
with the extended one, and no direction changes side of the chance line
(`paper/labelfix_rerun/round7/r7f_evia_legacy.csv`). On the legacy box the natural-vegetation
population is smaller and its burned prevalence higher than the extended box's 0.287 (Table S15).

## S1.2 CORAL regularisation

Over nine λ values from 0 to 10⁻¹ on four directions (Bejís and Muğla, and Manavgat and Muğla, both ways),
CORAL transfer AUC moves by at most 0.014 within any direction and model, and by at most 0.009 for
the thermal model (`paper/labelfix_rerun/exports/coral_lambda_sensitivity_b74d643e/metrics.csv`). No
value of λ was selected on performance.

The Manavgat and Bejís pair is not in that sweep, and it is the pair whose adapted result depended on λ
under the original label. It was therefore swept separately at λ = 10⁻⁵, 10⁻³ and 10⁻¹
(`paper/labelfix_rerun/step10/coral_lambda_sensitivity.csv`). Bejís to Manavgat gives 0.408 [0.389,
0.427], 0.410 and 0.367, below chance at every λ; Manavgat to Bejís gives 0.470 [0.444, 0.494], 0.474
and 0.466. No adapted direction of this pair has an interval above chance at any λ, so no conclusion
of the paper depends on the choice of λ within this range.

## S1.3 Blocking scale

Recomputing the transfer quantities at 10-cell (≈5 km) blocking from the re-frozen per-cell
predictions widens the intervals and moves the paired-delta verdict counts, from twelve positive,
seven negative and one uncertain at 1 km to six, five and nine at 5 km. Coarser blocking therefore
removes support from eight verdicts and adds none. Across five bootstrap seeds the 5 km counts run 5
to 6 positive, 4 to 5 negative and 9 to 11 uncertain, so they are not exact
(`paper/labelfix_rerun/round5/out_official/transfer_ci_blocksize.csv`,
`paper/labelfix_rerun/round6/seed_stability.json`).

The point estimates are unchanged. That is an identity rather than a result: the blocking scale is
the bootstrap *resampling unit*, and each point estimate is computed once over all target cells. The
comparison does establish two things. Every verdict that changes, changes towards "no verdict", and
no direction crosses the chance line under the widened intervals. The counts are the fragile part of
this paper; the sign pattern is simply not tested by this variation.

**Table 1 note (resampling units).** The bootstrap resamples spatial blocks, so an interval's
reliability is bounded by the number of blocks carrying at least one burned cell. Those counts fall
from 192 to 843 at 2 cells to **6 to 33** at 20 cells. An interval built on six such blocks has no
meaningful coverage, so **the 20-cell row should be read as indicative rather than as an interval**.
The 10-cell row is the coarsest blocking this design supports properly: every region there has 16 to
70 positive-carrying blocks, and the increment holds at that scale in all five regions.

## S1.4 Predictor-window closure

The predictor window was closed 7 and 14 days earlier in all five regions. The thermal contribution
stays positive and bootstrap-supported everywhere, and the direction of the change is
region-specific. In Manavgat, on the corrected label, it is +0.065 [+0.059, +0.072] at the canonical
window, +0.082 [+0.075, +0.090] at 7 days and +0.058 [+0.051, +0.065] at 14 days, all on the common
cohort of that analysis (`paper/labelfix_rerun/exports/window_closure_manavgat_2021/`). It strengthens
in Bejís, from 0.058 to 0.079 at 14 days, and in Muğla, from 0.115 to 0.128. It is flat in
Montiferru. It weakens monotonically in Evia, from 0.156 to 0.149 to 0.135. The four regions other
than Manavgat are unaffected by the label correction
(`paper/labelfix_rerun/exports/window_closure_<region>/tables/thermal_contributions.csv`). What holds
in every region is survival, not improvement.

## S1.5 Quality screening of the coarse thermal input

Two of the five regions' MODIS inputs are quality-screened and three are not. The split follows
export date rather than design, and it induces an elevation-correlated change at the input, at
r = +0.615 in Manavgat. Manavgat's downstream chain was therefore rebuilt from a quality-screened
input on the corrected label and compared with the unscreened arm. The current pipeline's step7
refuses the unscreened raster, because it carries no nodata tag and 8.1 % exact zeros, so the
unscreened arm runs the step7 of export time and the screened arm the current one: the two differ in
code version as well as in screening. The result does not change. Elevation stays at 0.232, no other
signed AUC moves by more than 0.005 (downscaled LST, −0.0044), and the within-region increment moves
from +0.067 to +0.068 (`paper/labelfix_rerun/round6/qc/qc_compare_manavgat_corrected.json`; Section
S3.5(xii)). The reason is structural: elevation is a DEM variable the screening cannot touch, and
fusion falls back on the MODIS-derived surface across only 2.14 percentage points of coverage. The
Muğla arm was not re-examined.

## S1.6 Normalised against absolute dryness channels

Section 1.2 argues that an internally normalised index should be less exposed to
absolute-temperature offsets between regions than raw land surface temperature. The thermal block
contains both kinds, so the argument can be tested directly as a feature-set contrast.

The normalised channels are the two that hold their direction in the same-geography two-event
comparison of Section S1.13, where the absolute channels move. That is a statement about one region
across two fires. Across regions it does not hold: `lst_anomaly_mean` is itself one of the
predictors whose reversal is bootstrap-supported on the frames as drawn (Table S10), which is why
Section S1.14 drops it alongside elevation. Being internally normalised protects a channel against
the offset between two seasons in one place. It does not, on this evidence, protect it against a
change of place.

Three feature sets were run over all twenty directions and all five within-region folds, with the
classifier, population, folds and bootstrap held fixed. The harness aborts unless its reference
configuration lands on the re-frozen exports, and it does exactly: the maximum absolute difference
between the reference arm and the step9b transfer AUCs is 0.000000 across all twenty directions.
Source for this section and the next two: `paper/labelfix_rerun/round3/no_coord_channels.json` and
`paper/labelfix_rerun/code/model_capacity.json`, summarised by
`paper/labelfix_rerun/round7/r7e_supplement_tables.py`.

**Table S23. Feature-set arms.** Mean over the twenty transfer directions and the five regions.

| Feature set | Mean transfer AUC | Directions > 0.5 | Mean within-region AUC |
|---|---:|---:|---:|
| Baseline only | 0.519 | 13 | 0.797 |
| Baseline + normalised anomalies | 0.524 | 14 | 0.862 |
| Baseline + absolute surface state | 0.531 | 13 | 0.864 |
| All ten features (reference) | 0.527 | 13 | 0.896 |

**The advantage is not found.** Per direction, the normalised set minus the absolute set has a mean
of −0.006. It is positive in 11 of 20 directions and runs from −0.099 to +0.087, so the spread is an
order of magnitude larger than the difference. Within region the two sub-blocks are
indistinguishable, at 0.862 and 0.864, and each recovers most of the gap between the baseline's
0.797 and the full model's 0.896. The comparison is between two sub-blocks of one thermal set on one
cohort. It does not test normalised dryness indices in general, nor a normalisation fitted against a
pooled multi-region reference.

## S1.7 The coordinate-informed channels

`downscaled_lst_mean` and `fused_lst_mean` come from a per-region downscaling model whose own inputs
include coordinates, the one route by which a coordinate-derived surface re-enters a feature set that
excludes coordinates (Section S3.4). A coordinate-smoothed surface is by construction locally
informative and non-portable, so if the within-region increment depended on it, that increment
would be an artefact of the smoothing rather than a finding about thermal state. Both channels were
dropped and everything refitted, over all twenty directions and all five within-region folds.

**Table S24. The within-region increment without the two coordinate-informed channels.**

| Region | Increment, full set | Without the two channels | Retained |
|---|---:|---:|---:|
| Manavgat 2021 | +0.067 | +0.064 | 95 % |
| Bejís 2022 | +0.056 | +0.046 | 82 % |
| Muğla 2021 | +0.116 | +0.097 | 84 % |
| North Evia 2021 | +0.153 | +0.145 | 94 % |
| Montiferru 2021 | +0.101 | +0.105 | 103 % |
| **Mean** | **+0.099** | **+0.091** | **92 %** |

**The increment does not depend on them.** It stays positive in every region and retains 82 % to
103 % of its size. Mean transfer is likewise unchanged, at 0.528 without the two channels against
0.527 with them and 0.519 for the baseline alone.

## S1.8 Model capacity

Every number in the paper comes from one random forest with unlimited depth and
`min_samples_leaf = 3`, the configuration most able to encode local structure and least able to
extrapolate. Three further estimators were therefore run over the same twenty directions and the
same five within-region folds.

**Table S25. Four estimators, within region and in transfer.**

| Estimator | Within-region AUC | Within increment | Transfer AUC | Transfer increment | Above chance |
|---|---:|---:|---:|---:|---:|
| Random forest, depth unlimited, leaf 3 | 0.896 | +0.099 | 0.527 | +0.007 | 13 of 20 |
| Random forest, depth 6, leaf 50 | 0.838 | +0.053 | 0.527 | −0.011 | 13 of 20 |
| Random forest, leaf 200 | 0.814 | +0.046 | 0.522 | −0.019 | 13 of 20 |
| Penalised logistic regression | 0.759 | +0.046 | 0.481 | −0.021 | 11 of 20 |

**Regularisation does not rescue transfer.** The four estimators land between 0.481 and 0.527, with
eleven to thirteen of twenty directions above chance, and the linear model, the one built to
extrapolate, transfers worst. Within-region skill falls as capacity is reduced, from 0.896 to 0.759;
transfer does not rise to meet it. The thermal block's contribution to transfer is +0.007 under the
canonical forest and negative under all three alternatives. The ordering of the estimators is not
claimed, since it rests on point estimates only.

## S1.9 The four evaluations of Section 4.3, in full

Section 4.3 reports four evaluations of the same models (main-text Table 2). The per-scar values,
the controls and the per-scar ladder of the thermal increment are here.

**Table S1. The four evaluations, per scar.** Primary natural-vegetation population, 5 km blocking,
2 km collar. Bejís and Manavgat have no row C, because in each the burned area is a single component,
so withholding it leaves nothing to train on. Source `paper/labelfix_rerun/code/matched_holdout.json`.

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

The same predictions were scored on a random sample of region cells drawn at the scar area's own
burned fraction. Over the nine scars that gives 0.793 against the region-wide 0.791, so matching
prevalence changes nothing, at −0.002 [−0.005, +0.001]. ROC-AUC does not depend on class balance at
fixed class-conditional distributions, so this is an implementation check rather than a finding.
Scoring the predictions on the scar area gives 0.644, a fall of **+0.149 [+0.087, +0.211]** from the
prevalence-matched score. That swaps both pools at once, so each was swapped singly, with the cost
always defined as the prevalence-matched score minus the swapped score. Replacing only the
negatives costs **0.139 [0.098, 0.181]**, 0.046 to 0.250 per scar. Replacing only the positives costs
**−0.002 [−0.055, +0.051]** on average, −0.121 to +0.137 per scar. The cost is therefore carried by
the negative pool. Every negative in a scar collar is fire-adjacent and shares the terrain, land
cover and weather of the positives, whereas a region's negatives include its easy far field
(`paper/labelfix_rerun/code/pool_decomposition.json`, `prevalence_control.json`).

### S1.9.2 The seven scars and the resampling unit

Rows A to D of Table 2 are means over the **same seven scars**, four in Muğla, two in Montiferru and one
in Evia. Under the corrected label the 2,151 added Manavgat burns merge into its one existing scar
(2,934 of 2,935 cells), which is why the controls above use nine scars and report 0.791 and 0.644
against Table 2's 0.773 and 0.640. The intervals are Student *t* over the scars. **Row A is a
region-level quantity repeated identically across a region's scars, so its interval is
pseudo-replicated and should not be read as coverage.** That repetition propagates into A − B and
A − C. Clustering by region gives **+0.137 [+0.048, +0.226]** for A − B over the three regions, and
**+0.160 [+0.090, +0.230]** over all nine scars in five regions
(`paper/labelfix_rerun/round7/round7_summary.json`). A − C clustered by region is +0.266 [−0.022,
+0.553], 3.6 times wider than its scar-level interval and spanning zero. **On the region unit only
the frame cost is established.**

The patch definition does not drive the result. Row C over a sweep of minimum scar sizes and buffers
runs from 0.541 to 0.561 on nine to six scars, and its means at 2, 5 and 10 km buffers are 0.546
(seven scars), 0.533 (seven) and 0.548 (six) (`paper/labelfix_rerun/code/scar_definition_sweep.csv`,
`scar_control.json`). Row D's spread over sources is large for single scars (Table S4) and small
after averaging: 28 of the 36 source-scar combinations enter it, nine of them below chance.

### S1.9.3 Controls and the thermal-increment ladder, full specification

Three controls reuse A's predictions, each averaged over 20 draws without replacement. The
**prevalence-matched** control draws $`|H_K^{+}|`$ cells from $`P_R`$ and $`|H_K^{-}|`$ from
$`V_R \setminus P_R`$. The **negative-pool** control keeps the drawn burned cells but uses the scar's
own negatives $`H_K^{-}`$, and the positive-pool control does the converse. A **within-region
half-split** (modelled cells cut at the median of a grid axis, both axes and directions, a split
discarded when either half is single-class) completes the set, under the transfer protocol of
Section 3.8 unchanged. The per-split positive counts are unequal and bear on the interpretation
(Table S2).

The **thermal-increment ladder** of Section 4.3 applies rows A to D to the paired thermal-minus-
baseline difference, on the seven scars of Table 2. Table S26 gives it per scar at both blockings.
Averaged over the seven scars, the region-wide increment is +0.095 at 5 km blocking and +0.117 at
1 km; scored on the scar area the same blocked predictions give +0.021 and +0.056; leave-one-scar-out
gives +0.024 and a foreign-region model +0.008 at both. Blocked minus leave-one-scar-out is −0.004
[−0.070, +0.063] at 5 km and +0.031 [−0.027, +0.090] at 1 km. The region-wide minus scar-frame
difference at 5 km is +0.074 [−0.009, +0.157] scar-level and [+0.034, +0.146] under a
region-cluster bootstrap. The within-region half-split gives +0.028, positive in 13 of 18 splits
(`paper/labelfix_rerun/inference/ladder_summary.json`, `paper/labelfix_rerun/code/positive_control.json`).

**Table S26. The thermal increment by scar: region-wide, on the scar frame, withheld and foreign.**
Thermal minus baseline ROC-AUC. Region-wide and scar-frame values at 5 km blocking, with 1 km in
brackets; leave-one-scar-out and foreign values do not depend on the blocking.

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

**Table S2. Within-region half-split, every split.** Source and target positive counts are given
because they are unequal, which is the principal limit on this arm: a straight cut does not produce
two exchangeable halves. Two splits are unusable because one half of Manavgat contains no burned
cells. Source `paper/labelfix_rerun/code/positive_control.json`; checked row by row by
`paper/code/appendix_tables.py`.

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

**Table S3. Leave-one-scar-out at a 2 km buffer, every scar.** Muğla and Montiferru are the only
regions containing more than one burned component of at least 50 cells. Muğla is the only region
where holding one out still leaves the source model properly trained in every arm; Montiferru's two
components are very unequal, so one of its arms retains 472 source positives and the other 97.
Muğla's four arms mean 0.579 and the three arms in the other regions 0.502; the pooled 0.546 is row
C of Table 2. Source `paper/labelfix_rerun/code/scar_control.json`; checked row by row by
`paper/code/appendix_tables.py`.

| Region | Component | Source positives left | Target positives | Target cells | AUC |
|---|---:|---:|---:|---:|---:|
| evia 2021 extended | 1 | 11 | 2,653 | 3,059 | 0.465 |
| montiferru 2021 | 1 | 97 | 442 | 758 | 0.584 |
| montiferru 2021 | 5 | 472 | 67 | 195 | 0.458 |
| mugla 2021 | 6 | 1,997 | 914 | 1,266 | 0.595 |
| mugla 2021 | 1 | 2,173 | 738 | 1,244 | 0.561 |
| mugla 2021 | 10 | 2,272 | 639 | 940 | 0.617 |
| mugla 2021 | 8 | 2,363 | 548 | 954 | 0.542 |

The evaluation populations of the arms are not comparable with each other or with the transfer
targets. A held-out scar with its 2 km collar contains only fire-adjacent negatives, whereas a whole
target region includes its easy far field; the burned fractions, 34 to 87 % against 7.0 to 28.7 %,
are a symptom of that rather than the cause.

**Table S4. The foreign-region arm, decomposed by source.** Each held-out scar area is scored with a
model fitted on each of the other four regions. Row D of Table 2 is the mean over the seven scars
that carry a row C, 28 of the 36 combinations below; over all nine scars the mean is 0.556. Source
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

Over all 36 combinations the mean is 0.556, the range 0.374 to 0.724, and ten fall below chance. The
mean spread across the four sources for a single scar is 0.183 over the nine scars and 0.187 over the
seven. Averaging over sources is what makes row D comparable with row C, which is fitted on one
region; it is not a claim that the choice of foreign source is immaterial.

**Table S5. Prevalence is not the cause of the evaluation-area effect.** The same fitted model and
the same out-of-fold predictions are scored three ways: on the whole region, on a random sample of
region cells drawn at the scar area's own burned fraction, and on the scar area. Twenty draws per
scar, seed 42. Nine scars, since this control needs no leave-one-scar-out arm. Values at 4 dp, as
stored in the source `paper/labelfix_rerun/code/prevalence_control.json`; checked row by row by
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

A minus A′, the effect of prevalence alone, is −0.002 [−0.005, +0.001]. A′ minus B, which swaps both
pools, is +0.149 [+0.087, +0.211]; Section S1.9.1 attributes it to the negative pool.

## S1.10 The transfer-gap decomposition, in full

The recovered fraction of Section 3.10 is at most +0.28 among the directions that started below
chance (Bejís to Evia), and seven directions have negative recovery, five of them with intervals
entirely below zero; Manavgat to Muğla (−0.03 [−0.06, +0.01]) and Muğla to Bejís (−0.07 [−0.16,
+0.01]) are point-estimate cases. Values are from `four_aoi_decomposition.csv` of the re-frozen
outputs (`paper/labelfix_rerun/round5/tables/corrected/`). Section 4.3 shows that the within-region
reference in the denominator is not matched to a transfer evaluation, and Section 4.4 that the raw
column depends on the frame, so the fractions are within-protocol quantities.

**Table S6. Transfer-gap decomposition (four-AOI set, 12 directions).** Within = target's
within-region thermal AUC; best adapted = the better of z-score and CORAL, a choice that uses target
labels; recovered fraction = (adapted − raw)/(within − raw), signed and unclipped, with paired
bootstrap CI (1000 replicates, 2-cell blocks). Montiferru directions are not part of this
decomposition. The status column asks whether the *adapted* value clears chance, using the 2-cell
adapted intervals of Table S16.

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

Section 4.4 reports that four of five regions agree on a negative association between pre-fire
surface temperature and burning, and that Manavgat joins them once elevation is held. The per-region
values are here. Signed AUC against `burned` within the 10 km collar. The stratified columns pool
within-stratum concordance over deciles of the named variable, weighting each stratum by its
positive-negative pair count. Sources: `paper/labelfix_rerun/code/matched_frame_gap.csv` (LST raw,
within NDVI, within distance; NDVI columns), recomputable by `paper/code/verify_matched_gap.py`, and
`paper/labelfix_rerun/round7/r7b_lst_given_terrain.csv` (LST within elevation, and LST detrended on
elevation).

**Table S27. The LST association, stratified, 10 km collar.**

| Region | LST raw | LST within elevation | LST detrended on elevation | LST within NDVI | LST within distance | NDVI raw | NDVI within LST |
|---|---:|---:|---:|---:|---:|---:|---:|
| Manavgat | 0.522 | **0.403** | **0.409** | 0.556 | 0.454 | 0.551 | 0.550 |
| Bejís | 0.405 | 0.509 | 0.411 | 0.486 | 0.350 | 0.618 | 0.574 |
| Muğla | 0.332 | 0.363 | 0.365 | 0.404 | 0.367 | 0.652 | 0.547 |
| Evia | 0.286 | 0.327 | 0.312 | 0.279 | 0.319 | 0.663 | **0.380** |
| Montiferru | 0.376 | 0.392 | 0.416 | 0.368 | 0.485 | 0.582 | **0.405** |

Three readings follow. First, Manavgat's raw LST association is above 0.5 and falls well below it
once elevation is held, whether by deciles or by removing the region's own linear dependence of LST
on elevation (−5.6 K per km); on the full frame the same holds, 0.665 raw against 0.455 and 0.446.
Its hot-burn signal is therefore carried by terrain, and with terrain held it shares the sign of the
other four. Second, in the other four regions the sign survives stratification within elevation in
three and within greenness in all four, so there it is neither a lapse-rate proxy nor an
inverse-greenness proxy; in Bejís it moves to 0.509 within elevation deciles and stays below 0.5
after detrending. Third, the reciprocal adjustment runs one way: NDVI reverses in two regions once
temperature is held, while LST reverses in none of the four once greenness is held. Aspect and
illumination are not used, so terrain is held only through elevation.

## S1.12 The LST anomaly under the difference instrument

Section 4.4 reports two elevation reversals, both involving Manavgat, that meet this paper's
per-comparison criterion on the collar. The LST anomaly differs between regions on a weaker
instrument: bootstrapping the two regions independently and differencing. These are the three pairs
that have opposite-sided point estimates and a difference interval excluding zero, all on
`lst_anomaly_mean`. Signed AUC within the 10 km collar; the two regions are bootstrapped
independently under the 10-cell spatial-block scheme and differenced, 1000 replicates, seed 42.

**Table S7. Between-region differences in the signed LST-anomaly association, 10 km collar.** Pairs
with opposite-sided point estimates and a difference interval excluding zero. Source
`paper/labelfix_rerun/inference/reversal_family_holm.csv` (collar frame); checked row by row by
`paper/code/appendix_tables.py`.

| Pair | AUC A | AUC B | Difference | 95 % CI |
|---|---:|---:|---:|---|
| Bejís vs Evia | 0.392 | 0.584 | −0.191 | [−0.295, −0.083] |
| Evia vs Montiferru | 0.584 | 0.400 | +0.184 | [+0.012, +0.321] |
| Bejís vs Muğla | 0.392 | 0.507 | −0.115 | [−0.219, −0.002] |

Twenty-seven of the ninety feature-by-pair differences on the collar clear zero, against about 4.5
expected at nominal 5 % under the null. Four of the twenty-seven are this feature, three of those
have opposite-sided point estimates, and two of the three involve Evia. Under a Holm correction
applied with normal-approximation p-values, twelve of the ninety survive; under the stricter
intersection-union form, which requires both regions' own associations to be significant, none does
(Section S1.20). The nine features carry about two independent thermal signals (Section 3.4), so
the ninety comparisons are not independent either. This is a weaker result than a reversal.

## S1.13 The same-geography event pair

Section 4.4 states the result and why it does not survive the frame test. The design, the two
structural asymmetries that have no analogue in the twenty-direction matrix, and the direction of
the bias they impose are here; the protocol is in Section S3.3.

This arm was designed to hold place fixed and vary only the fire, which would have separated
regional concept shift from everything that differs between study areas. Muğla burned twice, in 2021
and again eleven months later, on the same grid and through the same processing chain, and the 2022
arm is the 2021 population with the 2021 scar removed: 41,730 rows and 2,911 burned for 2021
against 38,790 rows and 331 burned for 2022. **Positive-carrying 5 km blocks: 70 for the 2021 arm
and 11 for the 2022 arm**, and eleven is below the sixteen this design sets as its own floor, so the
2022 intervals are indicative, like the 20-cell row of Table 1. Full per-feature values are in
Table S12.

**On the frame as drawn, elevation reverses with bootstrap support.** In 2021 higher ground burned
preferentially, at 0.611 [0.532, 0.690]; in 2022 lower ground did, at 0.296 [0.230, 0.355]. The
intervals are disjoint and the difference is −0.317 [−0.414, −0.220].

**The collar removes it.** The 2022 arm is one compact scar inside the whole Muğla box, so 93.2 % of
its cells lie beyond 10 km of any burned cell (median 43.6 km), against 55.3 % for the 2021 arm, the
most extreme far field in the cohort. Under the same 10 km collar the 2021 figure barely moves, 0.611
to 0.606 and still supported, while the 2022 figure moves from 0.297 to 0.565, onto the same side of
0.5 as 2021 with an interval covering chance. Slope reverses on neither frame.

**What this arm can and cannot evaluate.** The 2022 event's own modelling export is not in this tree.
The released script (`paper/code/verify_mugla_collar.py`) reconstructs the arm from the 2021
predictor file with the 2022 burned mask, which is valid for elevation, slope and land cover (they are
identical between the arms) and not for the state-dependent channels. Against the pipeline's own
2022 export the reconstruction agrees on elevation (0.297 against 0.296) and slope (0.559 against
0.558) and diverges on every seasonal channel, by +0.136 on `lst_anomaly_mean`, +0.092 on
`tvdi_difference_mean`, −0.078 on `ndvi_mean` and −0.025 on `current_tvdi_mean`. **So only elevation
and slope can be given a collar verdict for this arm**, and on the thermal channels it is silent.

| Feature | 2021, full | 2022, full | full verdict | 2021, collar | 2022, collar | collar verdict |
|---|---|---|---|---|---|---|
| **elevation_mean** | 0.611 [0.529, 0.692] | 0.297 [0.229, 0.363] | **supported reversal** | 0.606 [0.525, 0.685] | 0.565 [0.450, 0.677] | none |
| slope_mean | 0.637 [0.584, 0.689] | 0.559 [0.463, 0.643] | none | 0.635 [0.578, 0.692] | 0.457 [0.356, 0.548] | none |
| the state-dependent channels | n/a | n/a | n/a | n/a | n/a | **not evaluable here** |

Source `paper/labelfix_rerun/code/mugla_two_event_collar.csv`. The two arms are not disjoint samples:
they share 38,789 of the 2022 arm's 38,790 cells, and elevation, slope and land cover are identical
across all 73,098 grid cells, so only NDVI and the six thermal channels carry new information
between them. And the removal is the target's own positive class, so in the 2022-to-2021 direction
not one target positive is in the source training population while 38,789 of 38,819 target
negatives are, and membership of the source training set alone separates the 2021 target's classes
at ROC-AUC 0.9996. **We therefore cannot bound what that asymmetry does to a transfer estimate
between the two arms.** The known part of the bias runs the safe way: the removed cells are high,
with a median of 563 m, so removing them strips high negatives from the 2022 arm and makes the
observed reversal smaller rather than larger.

## S1.14 The two interventions, in full

**(a) Pooled multi-region training** (Fig. 6). Training on the pooled primary populations of the
other four regions beats the mean of the four single-source models for one target of five, Evia, at
0.715 [0.668, 0.757] against a mean of 0.569, and falls below that mean for the other four, by 0.009
to 0.057. It also beats the best single source only for Evia (0.654); choosing that best source
would use target labels, so it is an oracle benchmark rather than an alternative. In every target
the pooled model stays 0.20 to 0.48 AUC below the within-region ceiling. For Manavgat and Bejís it
falls below chance, only Manavgat with interval support, at 0.426 [0.369, 0.486]. Outside Evia,
aggregation does not recover what single-source transfer loses (`paper/labelfix_rerun/code/loro_all.json`,
`paper/labelfix_rerun/round7/r7d_pooled_vs_single.csv`).

**(b) Removing the direction-reversing features.** The two predictors whose signed association
reversed between regions with bootstrap support on the frames as drawn under the original label are
**`elevation_mean` and `lst_anomaly_mean`**. The arm keeps them, rather than re-selecting under the
corrected label (Table S10), and Section 4.4 shows that the frame decides much of the support, so
this arm measures what the removal costs under the original protocol. Retraining without them costs
**−0.076** of mean within-region AUC, supported in every region (per-region deltas −0.035, −0.130,
−0.073, −0.063 and −0.079 for Manavgat, Bejís, Muğla, Evia and Montiferru, every interval entirely
below zero), and changes mean transfer by **+0.014 [−0.028, +0.056]**, which spans zero (source
`paper/labelfix_rerun/round3/feature_drop_transfer.json`, summarised by
`paper/labelfix_rerun/round7/r7e_supplement_tables.py`).

Two qualifications belong with those numbers. First, the debit is mostly not the thermal block's.
Dropping elevation alone accounts for −0.056 of it, from 0.896 to 0.840. Dropping the LST anomaly
alone accounts for −0.013, from 0.896 to 0.883. Roughly three quarters of the cost is therefore the
removal of a baseline terrain variable. Second, both figures are post-selection: the two predictors
were chosen because they reverse, using the same data on which the costs are then estimated, and no
correction is applied.

**Table S28. Feature-removal configurations.**

| Configuration | Mean within-region AUC | Mean transfer AUC |
|---|---:|---:|
| full | 0.896 | 0.527 |
| drop `elevation_mean` | 0.840 | 0.533 |
| drop `lst_anomaly_mean` | 0.883 | 0.529 |
| drop both | 0.820 | 0.541 |

Fig. 7 shows the four configurations together. What this measures is a local cost with no
compensating transfer gain. It does not measure an exchange, because the transfer side is a null on
both arms: the thermal block's own contribution to transfer is +0.007 and removing the reversing
predictors returns +0.014, both with intervals spanning zero.

## S1.15 Signed associations on both frames

Section 4.4 states the collar results; the per-region values and the difference-instrument argument
are here. Per-feature values on both frames are in Table S14.

**The reversals that meet the per-comparison criterion.** On the frames as drawn, Table S10 counts
fourteen supported pair-level reversals across seven features, every one but the anomaly pair
involving Manavgat. Under the collar, elevation is below 0.5 in Manavgat, at 0.376 [0.300, 0.465],
and above it in the other four, individually supported in two, Muğla at 0.606 [0.525, 0.685] and
Evia at 0.648 [0.550, 0.740] (`paper/labelfix_rerun/code/collar_frame_bootstrap.csv`). Those two
pairs are the only supported reversals left on the collar, and neither survives the Holm
intersection-union correction (Section S1.20). The LST anomaly differs between regions on the
weaker difference instrument (Section S1.12).

**The sign most regions share.** Under the collar, LST lies below 0.5 in four of five regions, at
0.405, 0.332, 0.286 and 0.376 in Bejís, Muğla, Evia and Montiferru: a hotter pre-fire surface is
associated with less burning there, and the same holds for TVDI. Manavgat is the exception on the raw
association, at 0.522 for LST and 0.527 for TVDI, and joins the other four once elevation is held
(Section S1.11). Interval support is not uniform: LST is supported in three of the four and TVDI in
two, so "four of five agree" is a statement about point estimates. The absolute thermal channels
therefore behave here as static land-surface descriptors rather than as a dryness index, and the two
internally differenced channels carry no consistent cross-region direction. Compositing depth was not
tested and remains an open alternative.

**How many independent reversals there could be.** The channels whose reversals vanish on the
collar are the ones partly measuring terrain: current LST correlates with elevation at −0.695 to
−0.125 across the regions and TVDI at −0.722 to −0.298. Within the collar `fused_lst_mean` correlates
with `current_lst_mean` at 0.99 to 1.00, `downscaled_lst_mean` at 0.97 to 0.99 and
`current_tvdi_mean` at 0.87 to 0.98, and the two differenced channels at 0.64 to 0.94. Counts over
the nine features therefore count features, not independent quantities; in effective dimensions the
thermal block is closer to two.

**The thermal block's paired contribution to transfer, with its interval.** The two matrices were
differenced direction by direction. The mean is **+0.007**; the individual paired contributions span
**−0.148 to +0.132**, with **twelve positive and eight negative**. A mean near zero here records
cancellation, not consistent absence of effect. The directions are not independent, because each
region appears in eight of the twenty, so the interval depends on the resampling unit. All four units
the design permits span zero (1000 replicates where resampled; source
`paper/labelfix_rerun/code/transfer_delta_ci.json`):

**Table S29. The mean paired thermal contribution to transfer, by resampling unit.**

| Resampling unit | n | 95 % interval on the mean paired contribution |
|---|---:|---|
| Directions, naive bootstrap | 20 | [−0.023, +0.037] |
| Unordered pairs, cluster bootstrap (primary) | 10 | [−0.020, +0.038] |
| Unordered pairs, Student *t* on pair means | 10 | [−0.028, +0.043] |
| Regions, leave-one-out jackknife | 5 | [−0.018, +0.033] |

Holding out Manavgat, Bejís, Muğla, Evia and Montiferru in turn gives +0.0148, +0.0050, +0.0072,
+0.0010 and +0.0087, so no single region carries the mean or reverses its sign. None of these units
propagates within-direction sampling variability; they resample between directions only.

**In precision terms.** Across the twenty directions the thermal model's PR-AUC averages **0.181
against a no-skill baseline of 0.157**; the mean of the twenty per-direction lifts is 1.13. Seven of
the twenty fall below their own no-skill baseline at the point estimate. At 1 km blocking all seven
have intervals entirely below it; at 5 km blocking two do, Bejís to Manavgat and Muğla to Manavgat
(`paper/labelfix_rerun/round7/r7a_pr_auc_10cell.csv`). Only one direction, Evia to Manavgat, exceeds
twice its baseline, at 0.321 against 0.143 (Table S11).

**The within-region increment on the collar.** Running the baseline arm on the collar as well
(`paper/labelfix_rerun/round6/cosine/official_collar_increment_and_cosine.csv`), the thermal
increment at 5 km blocking is +0.073, +0.030, +0.088, +0.134 and +0.090 across the five regions,
positive in all five, with a mean of +0.083 against +0.087 on the frame as drawn. It erodes as the
frame tightens further: at a 5 km collar the mean halves to +0.042, still positive in all five. These
are point estimates; the intervals of Table 1 are on the frame as drawn.

**The five areas of interest are not comparable frames.** The share of modelled cells lying beyond
10 km of any burned cell is 58.5 % in Manavgat, 63.1 % in Bejís, 55.3 % in Muğla, 43.7 % in Evia and
**2.1 %** in Montiferru, with median distances of 13.1, 13.5, 11.3, 8.0 and 2.7 km (Table S13). In
Manavgat the median elevation of modelled cells rises from 330 m within 5 km of the fire to 995 m at
10 to 20 km and 1,273 m at 20 to 50 km, against 287 m for the burned cells themselves.

## S1.16 The contrast pair, in full

Manavgat and Muğla lie in the same country and fire year, 306 km apart by centroid, and their burned
cells occupy the most similar environmental envelope of any pair in the matrix; Bejís and Montiferru
occupy the least similar (Fig. 8). Per-quantity values for both pairs, on both frames, are in Table
S18.

For Manavgat and Muğla, on the frames as drawn seven of nine feature-response directions point
opposite ways, and all six features supported in both regions have opposite signs, elevation among
them. Under the collar the elevation reversal remains, at 0.376 [0.300, 0.465] in Manavgat against
0.606 [0.525, 0.685] in Muğla. Transfer is below chance in both directions on both frames: 0.438 and
0.345 as drawn, 0.493 and 0.433 under the collar, where Muğla to Manavgat's interval, [0.381, 0.491],
excludes chance. The most similar pair is among the weakest in the matrix, but not the extreme: under
the collar the weakest direction is Manavgat to Bejís at 0.407 and the strongest Muğla to Evia at
0.728. The niche-overlap and applicability measures of Table S18 are full-frame quantities.

Bejís and Montiferru sit at the opposite extreme. Their burned envelopes barely overlap, and they
carry the most dissimilar values on every overlap measure. They transfer above chance in both
directions, at the point estimate only: neither direction carries a verdict at 5 km blocking, and the
marginal applicability audit was not produced for Montiferru. **At the point estimates, high niche
overlap did not guarantee transfer and low overlap did not preclude it.** That rests on two pairs; it
is not a correlation across pairs, which Section S1.22 treats.

## S1.17 The sensitivity arms, summarised

Eight design choices were varied with everything else held fixed: the Evia AOI and its prevalence,
the CORAL regularisation constant, the blocking scale, the closure date of the predictor window, the
quality screening of the coarse thermal input, the contrast between the normalised and the absolute
dryness channels, the removal of the coordinate-informed channels, and the capacity of the classifier
(Sections S1.1 to S1.8). None changes a conclusion of the main text. Two bound how the results should
be read.

**The secondary population.** Section 3.5 defines a secondary population of all valid cells,
including cropland. It exists for the within-region arm in Manavgat and Bejís only, so it is a
two-region sensitivity rather than a cohort-wide one, and no transfer quantity is defined on it.
Across the two regions and the three block sizes the thermal increment runs +0.048 to +0.061 with
every bootstrap interval above zero, against +0.045 to +0.067 on the primary population, and the
paired difference between populations runs −0.011 to +0.011 with no consistent sign
(`paper/labelfix_rerun/pipeline/robustness/step8_large_block_primary_all_valid/`; Table 1). The
increment is therefore not an artefact of excluding cropland, which is what this arm was run to
test; it says nothing about the transfer results.

**The blocking scale.** Coarsening the blocks from 1 km to 5 km moves the paired thermal-minus-
baseline delta verdicts from twelve positive, seven negative and one uncertain to six, five and nine,
and the verdicts on the thermal arm itself from eleven above, seven below and two uncertain to nine,
six and five (Section S1.3). Support is removed and never added. The point estimates are unchanged,
which is an identity rather than a result.

## S1.18 Distance within a region

One further arm measures how skill decays with distance inside a single region. A model is fitted on
one half of a region and applied to the other, and target cells are binned by their distance from the
training cells (`paper/code/distance_curve.py`; corrected output
`paper/labelfix_rerun/round3/distance_curve.json`, summarised in
`paper/labelfix_rerun/round7/r7h_distance_curve.csv`). Means are unweighted over bins, whose positive
counts range from 1 to 1,067, and the bins carry no intervals.

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

**By 10 to 20 km inside a single region the model is close to chance.** That bounds how far a
surface of this kind can be carried from the cells it was fitted on, and it is consistent with
Section 4.3, where withholding a scar and replacing the model with a foreign one cost nothing
distinguishable.

It does not follow that the cross-region failure needs no regional mechanism. Once the curve reaches
the chance floor, any cross-region mean near 0.5 lies on its continuation by construction, so that
comparison could not have come out otherwise. And extrapolating an uninformative model does not
produce a reliably reversed ranking: Manavgat to Bejís is below chance with interval support on the
frame as drawn and at the 10 km collar.

Four limits bound even the descriptive reading. The two distance ranges do not overlap: within-region
separations span 2 to 86 km and cross-region separations start at 306 km. The far bins are thin, so
their means should not be read closely and the rise at 40 to 80 km is not evidence of anything. The
near bins carry exactly the autocorrelation blocked validation exists to remove, so **0.709 is an
upper bound on near-field skill rather than an estimate of it**. And this design separates distance
from crossing a study-area boundary, but not from the land cover, terrain and fire history that
covary with it. The arm contributes a length scale for the within-region decay, not an attribution.

## S1.20 The frame test, elaborated

Section 4.4 states these results. Sources: `paper/labelfix_rerun/code/aoi_frame_auc.csv` (signed
associations by frame), `paper/labelfix_rerun/code/collar_frame_bootstrap.csv` (their 10-cell
intervals), `paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv` (the transfer matrix by
frame) and `paper/labelfix_rerun/code/matched_frame_gap.csv` (the matched reference); code under
`paper/code/`.

**Construction.** Restricting every region to cells within 10 km of any burned cell removes only
far-field negatives. Every burned cell is at distance zero and is retained at any radius, so the
protection against a flattering radius is the sweep over radii, not the retention of positives.
The interval criterion was evaluated at the 10 km collar; at the point estimate the 5 and 10 km radii
agree. The collar reduces two regions' cell counts substantially, so part of any loss of support is
a loss of power. Features supported in both regions of a direction average 2.3 per direction on the
full frame and 2.2 on the collar.

**Multiplicity.** Each frame carries a family of ninety feature-by-pair comparisons (nine features,
ten region pairs). Table S30 gives how many pass each criterion. The per-comparison criterion of
Section 3.10 leaves two supported reversals on the collar, both on elevation and both involving
Manavgat. Neither survives the Holm intersection-union correction, which adjusts both regions'
tests together (adjusted *p* = 0.33 for Manavgat against Evia and 0.79 for Manavgat against Muğla,
normal approximation).

**Table S30. Reversal family, ninety feature-by-pair comparisons per frame.** Source
`paper/labelfix_rerun/inference/reversal_family_holm.csv`, `reversal_per_region.csv`.

| Criterion | Full frame | 10 km collar |
|---|---:|---:|
| Difference interval excludes zero | 39 | 27 |
| … with opposite-sided point estimates | 31 | 21 |
| Per-comparison criterion (each region's own interval excludes 0.5, opposite sides) | 14 | 2 |
| Holm, normal approximation, difference test | 27 | 12 |
| Holm intersection-union (both regions' tests) | 5 | 0 |

**The diagnostics on the collar.** Two of the twenty similarity diagnostics are built from the signed
associations themselves and were recomputed on the collar. The sign-agreement fraction over
interval-supported features, ρ = +0.52 [−0.27, +0.87] on the frames as drawn, takes only the values
0 and 1 across sixteen defined directions on the collar and correlates with collar transfer at
ρ = +0.38 [−0.17, +0.85]. The all-feature cosine, +0.44 [−0.29, +0.80] as drawn, correlates with
collar transfer at **+0.57 [+0.05, +0.88]**, the only diagnostic interval in the study that excludes zero
(`paper/labelfix_rerun/round6/diag_collar/`, intervals from
`paper/labelfix_rerun/round7/r7g_collar_diagnostics.json`, which reproduces the as-drawn intervals
exactly). Three cautions keep it from being a result: it is one variant among about forty
uncorrected diagnostic tests, it rests on twenty directions that share regions, and the collar is
defined from the burned cells, so the diagnostic needs target labels twice over. The other eighteen
diagnostics were not recomputed on the collar, so their collar correlations are unknown.

**Data provenance.** A quality-screening rebuild had overwritten two regions' 500 m modelling
datasets at the pipeline's canonical path, Manavgat's and Muğla's, after the frozen tables were
computed; each replacement differs in `downscaled_lst_mean` and `fused_lst_mean`. The pipeline
records a SHA-256 for each region's modelling dataset, and that hash identifies the frozen copy.
Every arm of Section 4.4 reads each region through `paper/code/_canonical.py`, which verifies the
hash on load, and reads Manavgat from the corrected re-freeze (SHA-256 `5a5e876c…`). The provenance
of the collar transfer matrix is in `paper/labelfix_rerun/round5/collar/PROVENANCE.md`.

**Table S8. Cross-region transfer under equalised evaluation frames.** Primary natural-vegetation
population, thermal model, twenty ordered directions per row. Above/below chance are point counts.
The supported counts use a 10-cell (≈5 km) spatial-block bootstrap on the target, 1000 replicates,
seed 42; Table S16 reports the as-drawn matrix under 2-cell (≈1 km) blocking. Per-direction bounds
are in `paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv`.

| Source frame | Target frame | Mean target AUC | Above chance | Below chance | Supported above / below | Paired thermal delta |
|---|---|---:|---:|---:|---:|---:|
| full | full | 0.527 | 13 of 20 | **7** | 9 / **6** | +0.007 |
| full | 10 km | 0.559 | 14 of 20 | 6 | 10 / 2 | +0.008 |
| 10 km | full | 0.546 | 14 of 20 | 6 | 10 / 5 | +0.014 |
| **10 km** | **10 km** | **0.589** | **15 of 20** | **5** | **13 / 2** | **+0.024** |
| 5 km | 5 km | 0.591 | 16 of 20 | 4 | 11 / 0 | +0.017 |

The baseline control moves with the frame: the static baseline transfers at 0.565 against the thermal
model's 0.589 on the 10 km collar, a paired difference of +0.024 rather than +0.007. The control still
holds in kind: the static predictor class is not the portable one either. The below-chance count
moves from seven to five at the point estimate and from six to two with interval support. The
largest movers are Bejís to Evia, 0.383 to 0.602, and Bejís to Manavgat, 0.314 to 0.452; the one
large fall is Evia to Manavgat, 0.677 to 0.594.

**The matched reference.** Recomputing the within-region reference on the same frame and at 5 km
blocking (`paper/code/verify_matched_gap.py`):

**Table S33. Within-region reference and transfer on matched frames.**

| Frame | Within-region (5 km blocking) | Mean transfer | Gap |
|---|---:|---:|---:|
| full rectangle | 0.814 | 0.527 | 0.287 |
| 10 km collar | **0.786** | **0.589** | **0.197** |
| 5 km collar | 0.759 | 0.591 | 0.169 |

Paired by target region, the collar shortfall is **+0.197 [+0.091, +0.303]** (Student *t* over the
five target regions; per region +0.081 Montiferru, +0.319 Manavgat, +0.172 Muğla, +0.202 Bejís,
+0.211 Evia). The shortfall survives on every matched row, but it is 0.197 at the collar, not the
0.29 the unmatched comparison implies, and it shrinks as the frame approaches the fire. At the 5 km
collar the within-region increment itself halves but stays positive in all five regions, at a mean of
+0.042 (Manavgat +0.035).

## S1.21 The transfer matrix and adaptation, elaborated

Section 4.5 states these results.

**Raw transfer.** Raw target AUC spans 0.314 to 0.677 (Fig. 4). At 2-cell blocking eleven of 20
directions are above chance with interval support and seven below: both directions between Manavgat
and Bejís, both between Manavgat and Muğla, both between Bejís and Evia, and Montiferru to Manavgat.
At 10-cell blocking the same points give 9 above, 6 below and 5 uncertain; Manavgat to Muğla loses its
support and carries no verdict, and no direction changes side of the chance line. Of the below-chance
directions, Manavgat to Bejís (0.407 [0.323, 0.493]) and Muğla to Manavgat (0.433 [0.381, 0.491])
keep interval support on the 10 km collar, though both intervals cover chance at the 5 km collar.
The sharpest below-chance direction as drawn is Bejís to Manavgat at 0.314 [0.296, 0.332].

**Label-blind adaptation.** Under region-wise z-scoring the twenty directions span 0.302 to 0.630 and
under CORAL 0.406 to 0.624. The compression is not uniform: under z-scoring Bejís to Manavgat moves
further below chance, from 0.314 to 0.302. Taking the better of the two adaptations per direction,
15 of the 20 end closer to chance than they began and 5 end further from it; four of those five
involve Montiferru and move upward, while the fifth is Manavgat to Muğla moving downward from 0.438 to
0.427. Under CORAL alone sixteen of twenty end closer
(`paper/labelfix_rerun/round5/matrix20_official.csv`). In the six directions where raw transfer was
below chance, the best label-free method recovers at most 28 % of the gap to the within-region
reference (Bejís to Evia). On the twelve-direction subset for which the decomposition is defined,
seven directions show negative recovery (Section S1.10).

**Seed stability.** Across five bootstrap seeds every 2-cell verdict is stable. At 10 cells, one
level verdict and two paired-delta verdicts are not: the level verdict of Evia to Bejís and the
paired-delta verdicts of Manavgat to Muğla and Evia to Montiferru
(`paper/labelfix_rerun/round6/seed_stability.json`). The random-forest seed is fixed, so all
direction-level intervals are conditional on one fitted source model.

**Jackknife.** Dropping one region at a time moves the mean paired contribution between +0.001
(without Evia) and +0.015 (without Manavgat), and never reverses its sign.

## S1.22 The similarity diagnostics

Twenty candidate diagnostics from five families were each rank-correlated with the raw thermal
transfer AUC over the ordered directions on which they are defined, under one common pair-based
bootstrap (unordered pairs resampled with replacement, both directions carried, 2000 replicates,
seed 42). They were defined on 8 August 2026, with their results under the
original label, and were not re-selected after the label correction. Table S17 lists all twenty; the
source is `paper/labelfix_rerun/round5/out_official/all_diagnostics_vs_transfer.csv`, with the
original-label values alongside in `paper/labelfix_rerun/round5/s6_diagnostics_20.md`.

**On the frames as drawn, no interpretable diagnostic has an interval excluding zero.** The largest
correlations are conditional: the sign-agreement fraction over interval-supported features at
ρ = +0.52 [−0.27, +0.87] and its cosine at +0.49 [−0.24, +0.87]. Under the original label these two
were the only rows whose intervals excluded zero (+0.84 and +0.81); the label correction removed that.
The marginal family (applicability, dissimilarity, climatic distance, domain classification), the
niche-overlap family and the regime family all span zero, and geographic distance does not order the
matrix (ρ = −0.17 [−0.87, +0.84] on the twelve directions where it is defined). The learned domain
classifier separates source from target at AUC ≥ 0.96 for every pair; it always succeeds, which is
why it carries no ordering information. The twentieth measure, the signed-AUC vector Spearman over
supported features, is defined on only six directions and its interval is degenerate (upper bound
equal to the point estimate), so it is listed and not interpreted.

**Equal samples.** The families sit on unequal samples: twelve directions for the marginal,
applicability, climatic and geographic rows, eighteen for the supported-conditional rows, twenty for
the rest. Every row was therefore recomputed on the common twelve-direction and sixteen-direction
subsets. On both, every interpretable row spans zero
(`paper/labelfix_rerun/round5/out_official/diagnostics_common_subset.json`).

**The collar.** Section S1.20 reports the two diagnostics recomputed on the equalised frame, one of
which, the all-feature cosine, orders collar transfer with an interval excluding zero; it is reported,
with its cautions, and not relied on.

**Limits.** Signed associations need burned labels in both regions, so the conditional family is not
available before deployment, while the marginal family, which is, fails. Ten effective region pairs
give little power: a moderate ordering would usually be missed, so these results show a failure to
demonstrate ordering, not the absence of one (Section S3.5(xiii)). Measures built from interval
support are unstable where bounds sit near 0.5 (Section S3.5(viii)).

## S1.23 Additional robustness analyses

The analyses in Table S21 were run after the main results, to test whether the headline quantities
depend on choices a reader might question. None was used to select a reported configuration.

**Table S21. Additional robustness analyses (post hoc).** Sources under `paper/labelfix_rerun/`:
`geometry/` (a1 to a5), `inference/` (units, equivalence, ladder) and `round7/`.

| Analysis | Question | Result |
|---|---|---|
| Edge-excluded frame cost (a1) | Is the frame cost carried by the scar's edge cells? | Over nine scars, excluding 0, 1 or 2 cells of the scar edge gives A − B = 0.147 [0.086, 0.208], 0.137 [0.069, 0.205] and 0.129 [0.055, 0.204]; with the region as unit 0.160, 0.150 and 0.145, every interval above zero |
| Placebo collars (a2) | Is the cost a property of any fire-shaped frame? | The scar's real positives scored against the negatives of a same-shaped collar placed away from any burned cell reproduce A (A − placebo −0.002 [−0.056, +0.052], eight scars with placements); the real collar costs +0.155 [+0.108, +0.202] more, so the cost is the fire-adjacent negatives |
| Label-free target frames (a4) | Does a frame drawn without target labels change transfer? | Trimming the target to the source's per-feature range, or to the source's area of applicability [@Meyer2021], gives means of 0.520 to 0.574, and a 20 km window 0.482; every paired thermal Δ interval spans zero |
| Metric dependence (a5) | Is the frame cost specific to ROC-AUC? | Region-wide minus scar-frame over nine scars: partial AUC (FPR ≤ 0.1) 0.088 [0.048, 0.128]; average precision −0.342 [−0.477, −0.206], higher on the scar frame because its prevalence is higher |
| Collar within-region increment | Does the within-region increment survive the collar? | +0.083 [+0.037, +0.129] over five regions (Student *t*), against +0.087 [+0.037, +0.136] as drawn |
| Equalised Δ by resampling unit | Does the collar Δ exclude zero? | Table S31: two of five computable units exclude zero; the two-way estimators are undefined |
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

The primary unit is fixed in Section 3.7 as the pair cluster, and on it the equalised contribution
spans zero. With five regions a percentile bootstrap over regions has at most 126 distinct resamples,
so the two region-clustered intervals are coarse.

# S2 Supporting tables

These are the per-region and per-direction numbers the Results sections quote, given in full so that
every claim can be checked against the values it rests on rather than against a summary of them.

**Table S9. Signed univariate AUC of each predictor against `burned`, by region.** Primary
natural-vegetation population; 10-cell (~5 km) spatial-block bootstrap, 1000 replicates, seed 42.
The AUC is never folded to max(AUC, 1 − AUC), so a value below 0.5 means lower values rank burned
and is a direction rather than weakness. **Bold** marks a region whose own interval excludes 0.5.
Source `paper/labelfix_rerun/round5/tables/step9g_multi_aoi_feature_stability.csv` (the pipeline's
Step9G five-region synthesis, sha256 c864cd7d…), checked row by row by `paper/code/appendix_tables.py`.

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

**What counts as a reversal.** A pair of regions is called a reversal only when their signed
associations point to opposite sides of 0.5 **and each region's own interval excludes 0.5**. That is
stricter than requiring the two regions' intervals to be disjoint, and the difference matters: for
`current_lst_mean` between Manavgat and Bejís the two intervals are disjoint, [0.608, 0.719] against
[0.401, 0.547], but Bejís's own interval includes 0.5, so Bejís has no established direction to
reverse from. That pair is a point reversal, not a supported one.

**Table S10. The cross-region reversals that meet the stricter criterion.** The strict criterion is applied to Table S9's intervals. Difference intervals are the paired 10-cell
block bootstrap of `paper/code/ems_inference_multiplicity.py`
(`paper/labelfix_rerun/inference/reversal_family_holm.csv`, 1000 replicates), which flags the same
fourteen pairs. Checked row by row by `paper/code/appendix_tables.py`.

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

Fourteen pair-level reversals across **seven** features, thirteen of them involving Manavgat. Under
the original label there were three, across two features, elevation and the LST anomaly; the
feature-removal arm of Section 3.11 keeps exactly those two and does not re-select. Twenty-six further
pairs reverse at the point estimate only, and they are not counted. The conservative criterion costs
the paper findings rather than manufacturing them: a difference interval on the pair, the instrument
of Section S1.12, would support seventeen further reversals. None of the fourteen is corrected for
multiplicity; Table S30 gives the corrected counts.

## S2.1 The transfer matrix in precision-recall terms

ROC-AUC is reported throughout the main text for comparability with the susceptibility literature.
A susceptibility surface is used as a ranked area budget, so precision-recall is the operational
quantity, and at target prevalences of 7.0 to 28.7 % the two can differ sharply. Read from the step9b
exports of the re-frozen outputs (`paper/labelfix_rerun/round5/tables/corrected/*/step9b_metrics.json`).

**Table S11. Thermal transfer, PR-AUC against the no-skill baseline.** The baseline is the target's
burned prevalence. Lift is PR-AUC divided by that baseline; a lift of 1 is no better than random ranking. Ordered by lift.
Checked row by row by `paper/code/appendix_tables.py`. PR-AUC intervals at 2-cell and 10-cell
blocking for every direction are in `paper/labelfix_rerun/round7/r7a_pr_auc_10cell.csv`.

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

Seven directions fall below their own no-skill baseline, and only one exceeds twice it. The seven are
the same seven that are below chance on ROC-AUC, which is what a reversed ranking predicts in either
metric. At 1 km blocking all seven have PR-AUC intervals entirely below the baseline; at 5 km
blocking two do, Bejís to Manavgat [0.067, 0.132] and Muğla to Manavgat [0.071, 0.135] against 0.143.
Section 4.4 shows that the below-chance count is largely a property of the evaluation frames.

## S2.2 The same-geography event pair, in full

Section S1.13 reports this arm; Section 4.4 shows its elevation reversal to be a frame artefact, and
Section S1.13 explains why its thermal channels carry no verdict. The per-feature values are kept here
because the arm is what motivated the frame test.

**Table S12. Signed univariate feature-burned AUC, Muğla 2021 versus 2022.** Raw AUC against
`burned`, never folded to max(AUC, 1 − AUC); 10-cell (≈ 5 km) spatial-block bootstrap, 1,000
replicates, seed 42 (Section 3.14). Analysis population 41,730 rows / 2,911 burned (2021) and
38,790 rows / 331 burned (2022). **Positive-carrying 5 km blocks: 70 for the 2021 arm and 11 for the
2022 arm.** Table 1's note sets sixteen as the floor this design supports at that blocking, so the
2022 intervals here fall below the paper's own standard and are read as indicative, exactly as the
20-cell row of Table 1 is. The 2022 arm is additionally a single compact scar, so its eleven blocks
are contiguous. Read from
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

Section 4.4 states these results; the per-region values are here.

**Table S13. Evaluation-frame geometry of the five study regions.** Primary natural-vegetation
population. Distance is Euclidean to the nearest burned cell on the 500 m grid, at 0.45 km per cell.
Corrected Manavgat label. Computed by `paper/code/appendix_tables.py` from the step8a tables (read
through `paper/code/_canonical.py`, which verifies each file's sha256), as
`paper/code/verify_aoi_frame.py` does.

| Region | cells | burned | median distance to burned | share beyond 10 km |
|---|---:|---:|---:|---:|
| Manavgat | 20,511 | 2,935 | 13.1 km | **58.5 %** |
| Bejís | 15,190 | 1,100 | 13.5 km | **63.1 %** |
| Muğla | 41,730 | 2,911 | 11.3 km | 55.3 % |
| Evia | 9,298 | 2,664 | 8.0 km | 43.7 % |
| Montiferru | 2,544 | 539 | 2.7 km | **2.1 %** |

**Table S14. Signed univariate AUC, frame as drawn against a 10 km collar.** Point estimates; the
intervals that decide the reversal question are given in the text below and in
`collar_frame_bootstrap.csv` (10-cell blocks, 1000 replicates, seed 42). Signed and never folded to
max(AUC, 1 − AUC), so a value below 0.5 is a direction, not weakness. The collar drops no burned cells in any region. Full frame from Table S9's source, collar from
`paper/labelfix_rerun/code/aoi_frame_auc_frozen_mugla.csv` (the collar arm with Muğla read from its
canonical file). Checked row by row by `paper/code/appendix_tables.py`. Manavgat sits on the other
side of 0.5 from the other regions on every row, the collar rows included.

| Signed univariate AUC | Manavgat | Bejís | Muğla | Evia | Montiferru | straddles 0.5 |
|---|---:|---:|---:|---:|---:|---|
| elevation, full frame (Table S9) | **0.232** | 0.643 | 0.611 | 0.541 | 0.584 | **yes** |
| elevation, 10 km collar | **0.376** | 0.614 | 0.606 | 0.648 | 0.581 | **yes** |
| current LST, full frame | **0.665** | 0.477 | 0.325 | 0.377 | 0.370 | **yes** |
| current LST, 10 km collar | **0.522** | 0.405 | 0.332 | 0.286 | 0.376 | **yes** |
| current TVDI, full frame | **0.677** | 0.517 | 0.336 | 0.362 | 0.356 | **yes** |
| current TVDI, 10 km collar | **0.527** | 0.454 | 0.342 | 0.250 | 0.361 | **yes** |

**Table S15. Region summary: populations and gate outcomes.** Counts from each
region's Step 8A dataset statistics; gate fractions from each region's burned-landcover gate output.
TSG = the primary natural-vegetation population (tree, shrub and grass). The TSG columns use the canonical modelled
population, `burnable_tree_shrub_grass` **and** `valid_for_modeling == True`, which is the
population every model in this paper was fitted and scored on. Counts are
computed from the step8a tables and gate fractions read from each region's gate output
(`paper/labelfix_rerun/round5/tables/corrected/gates/`). Checked row by row by `paper/code/appendix_tables.py`.

| Region | Total cells | Valid cells | Burned | Prevalence (all valid) | TSG cells | Burned in TSG | TSG prevalence | Burned natural-veg fraction | Gate verdict |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat 2021 | 24,150 | 24,087 | 3,046 | 0.126 | 20,511 | 2,935 | 0.143 | 0.955 | pass |
| Bejís 2022 | 15,759 | 15,759 | 1,103 | 0.070 | 15,190 | 1,100 | 0.072 | 0.991 | pass |
| Muğla 2021 | 73,098 | 73,045 | 3,026 | 0.041 | 41,730 | 2,911 | 0.070 | 0.958 | pass |
| North Evia 2021 (extended) | 22,925 | 22,906 | 2,788 | 0.122 | 9,298 | 2,664 | 0.287 | 0.945 | pass |
| Montiferru 2021 | 3,234 | 3,173 | 697 | 0.220 | 2,544 | 539 | 0.212 | 0.723 | pass |

**Table S16. Cross-region transfer matrix, thermal model, TSG population.** Target ROC-AUC with 2-cell
spatial-block bootstrap 95% CIs (1000 replicates). CORAL is applied after region-wise z-scoring (λ =
10⁻⁵). Generated by `paper/code/table_b9.py` from the re-frozen outputs
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

**Table S17. All transferability diagnostics versus raw thermal transfer (20 ordered directions).**
Spearman ρ with pair-based bootstrap 95 % CIs. Exp. = expected sign. Rows with n = 12 exist only for
the four-AOI subset, because those diagnostics were never produced for Montiferru. The
supported-features conditional rows use the 18 directions with at least one CI-supported feature.
Every row from `paper/labelfix_rerun/round5/s6_diagnostics_20.csv`, checked by
`paper/code/appendix_tables.py`. The twenty diagnostics were defined on 8 August 2026 and not
re-selected after the label correction.

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

*Table note.* A null row means the diagnostic was **not shown to order transfer** on this design, not
that it was shown incapable of ordering it. With ten effective region pairs the power is low, and the
intervals are wide enough to admit moderate true correlations in either direction. ‡ The last row is a
member of the candidate set fixed in advance, so it stays in the table. It is defined on six
directions only, and its interval is degenerate (the upper bound equals the point estimate), so it is
not interpreted and is not comparable with the other nineteen.

**Under the original label** the two supported-feature variants cleared zero (+0.84 and +0.81 over
sixteen directions). Both select their predictor subset by whether two regions' bootstrap intervals
happen to exclude 0.5, a data-dependent selection made on the same data. Under the corrected label
neither clears zero (+0.52 and +0.49 over eighteen directions), and no interpretable row does
(Section S3.5(viii) on why measures built from interval support are unstable).

**Equal-sample check.** The families sit on unequal samples: marginal, applicability, climatic and
geographic rows on twelve directions, the supported-conditional rows on eighteen, the rest on twenty.
Recomputing every row on the common twelve-direction subset, and again on the sixteen directions
where the supported-conditional rows are defined, leaves every interpretable row spanning zero; the
supported-conditional rows give +0.41 [−0.42, +0.88] and +0.46 [−0.56, +0.84] on the common twelve.
The published values are reproduced to 4.4 × 10⁻⁵. Source:
`paper/labelfix_rerun/round5/out_official/diagnostics_common_subset.json`.

**Table S18. The most and least environmentally similar pairs, on both frames.** Schoener's *D* is
computed over burned cells only and is therefore collar-invariant. Transfer values are the two
ordered directions of each pair; ranks are out of the twenty directions on the equalised frame.
Corrected Manavgat label. Schoener's *D*, per-feature *D* and as-drawn transfer are read from Fig. 8's
source, `paper/labelfix_rerun/round5/out_official/figure_contrast_pairs.json`; collar transfer and
ranks from Table S8's source, `paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv`; the AoA
shares from `paper/labelfix_rerun/round5/collar/aoa_directed_pair_summary.csv`. Every cell is
asserted against those files at build time (`paper/figures/fig8_contrast_pairs.py`).

| | Manavgat and Muğla | Bejís and Montiferru |
|---|---|---|
| Schoener's *D*, mean 1-D | **0.799** (highest) | **0.479** (lowest) |
| per-feature *D* | 0.74 to 0.87 | 0.23 to 0.77 |
| transfer, frames as drawn | 0.438, 0.345 | 0.594, 0.548 |
| transfer, 10 km collar | 0.493, 0.433 | 0.669, 0.624 |
| rank of 20 on the collar, from the bottom | 4th, 2nd | 16th, 12th |
| target cells inside the AoA | 0.876, 0.531 | n/a |

# S3 Protocol detail and limitations

These protocols are given here in full rather than in Methods, because each is a specification a
reader needs only when checking the corresponding result, and none is needed to follow the
argument. Sections 3.2 to 3.4, 3.7, 3.9, 3.10, 3.13 and 3.14 state in summary what each does.

## S3.1 Burned-area label, the reconstructed analysis grid, and the admissibility gate

Labels come from MODIS MCD64A1 Collection 6.1 (`MODIS/061/MCD64A1`) retrieved through Google Earth
Engine [@Gorelick2017], whose omission and commission characteristics [@Boschetti2019] bound every
model here. The product is exported onto the 30 m EPSG:4326 reference grid used by the rest of the
pipeline, which duplicates each native ~500 m observation across the 30 m pixels beneath it.

The analysis grid is therefore **reconstructed rather than native**: the 30 m grid is partitioned
into non-overlapping blocks of `round(500 / 30) = 17 × 17` pixels, giving a nominal cell edge of
510 m, and each cell is identified by its integer block indices `row_500m` and `col_500m`. This
approximates the MODIS sinusoidal cell rather than reproducing it, being anchored to the
Landsat/EPSG:4326 reference grid, and marginal blocks are truncated. The cell is square in degrees
but not on the ground, about 510 m north to south and 390 to 407 m east to west, so its area is
0.199 to 0.208 km² against the native MODIS cell's 0.215 km² (463 m edge); every block-size label in
this paper is therefore the north-south dimension. The collar step of 0.45 km per cell (Section 3.12)
is a single value between the cell's two dimensions, so collar radii are nominal to within about 15 %.

A cell's representative burn date is the **mode** of the positive sub-pixel day-of-year values in
the block, tested against the region's label window. Because the exported raster carries no
out-of-window positives, in this dataset a single in-window positive sub-pixel makes the cell burned. That dilates each scar by
up to one cell at its edge, and it can mark a water cell burned where the product does; the primary
population keeps only cells dominated by natural vegetation, which excludes water.
The fraction of positive sub-pixels agreeing with the modal date is recorded as
`burn_date_pixel_agreement_fraction` but no agreement threshold is imposed. The label never affects a
cell's eligibility for modelling: unburned, all-no-data and out-of-window cells all remain as the
negative class.

Earlier burning is handled unevenly and is stated region by region in Section S3.1.1. The only
historical exclusion applied by design removes the 2021 Muğla scar from the 2022 event-relative
experiment of Section 3.14.

Before any modelling each region passes a gate that answers one question: of the cells labelled
burned, what fraction is dominated by natural vegetation? A region is admitted as a wildfire
candidate when that fraction reaches 0.50 and at least 30 burned cells are present, and is rejected
as a cropland-dominated control when the cropland fraction reaches 0.50 instead. The gate uses ESA
WorldCover classes aggregated to the same reconstructed cells. Its purpose is to separate burned area
produced by natural-fuel combustion from burned area produced by post-harvest stubble burning, which
MCD64A1 does not distinguish. Verdicts are reported in Section 4.1.

### S3.1.1 Pre-label and historical burning, by region

Two kinds of earlier burning can contaminate a label. **Pre-label burning** is burning inside the
region's own predictor window, which the pipeline can remove from the analysis universe. **Historical
burning** is burning in the five preceding years, which no region screens for. Table S34 gives both,
recomputed from the MCD64A1 export of each region (`paper/code/ems_labels_1_prelabel.py`,
`ems_labels_2_history.py`; outputs `paper/labelfix_rerun/labels/r1_prelabel.json`, `r2_history.json`).

**Table S34. Earlier burning by region, natural-vegetation population.**

| Region | Pre-label cells removed | Pre-label burned cells retained | Historical-burn cells (five years) | … of which burned again in the event |
|---|---:|---:|---:|---:|
| Manavgat 2021 | none needed (no pre-label burning) | 0 | 0 | 0 |
| Bejís 2022 | exclusion not applied | 48 (49 in all valid cells; 10 burned again) | 163 | 0 |
| Muğla 2021 | 49 | 0 | 194 | 25 |
| North Evia 2021 | 16 | 0 | 366 | 88 |
| Montiferru 2021 | 61 | 0 | 58 | 32 |

Excluding the historical-burn cells lowers the mean paired transfer contribution from +0.007 to
+0.003 (at 10-cell blocking, 5 positive, 4 negative and 11 uncertain verdicts against 6, 5 and 9), and
leaves the within-region increment positive with interval support in every region, at +0.062 (no
change), +0.055, +0.088, +0.162 and +0.111 for Manavgat, Bejís, Muğla, Evia and Montiferru.

### S3.1.2 The Manavgat label correction

**The Manavgat 2021 label is a corrected one.** The label first used for Manavgat was exported on
8 July 2026. That was before the month-alignment fix to the MCD64A1 query (commit 183be42, 11 July),
and the export was never renewed. It therefore missed the fire's first four days, 28 to 31 July.
The defect was a stale export, not a code error. The corrected label only adds burned cells. No
cell burned under the original label becomes unburned, and no predictor or validity flag changes.
In the primary population the burned count rises from 784 to 2,935. The Manavgat outputs were
re-frozen with the upstream pipeline at commit 6381f4c, run unchanged except for a one-line patch to
the window-closure diagnostic and a runtime override of the Earth Engine project (`thermaltwin`), in
Python 3.12.10 with scikit-learn 1.9.0 (pins in `ENVIRONMENT.md`). The correction, the re-freeze and
its control arm were carried out by the corresponding author with AI-assisted code (Section 3.13); they
were not independently repeated by the author of the pipeline. That pipeline version
writes one extra column, a flag for burning in earlier years, and it excludes no Manavgat cell. A
control arm re-froze the original label with the same code and environment and reproduced the
published outputs to within 10⁻⁵. The exceptions are listed in the manifest: file paths, the column
list, and one legacy pair that differs at the level of random-forest thread nondeterminism. Differences between the two arms are therefore attributable to the label alone.
The reproduction check of Section 3.13 covers the re-frozen outputs. The manifest, hashes and
runner scripts are released under `paper/data/manavgat_2021/refreeze/`.

### S3.1.3 Effect on Table 1

The Manavgat rows are computed on the corrected label. It adds burned cells, 784 to 2,935 in the
primary population, and changes no predictor (Section 3.2). The rows strengthen rather than weaken.
Absolute AUCs rise by 0.04 to 0.11 across the three block sizes, and the increment holds at every
scale. The 1 km interval narrows from [+0.055, +0.079] to [+0.060, +0.073], because the region now
carries 814 positive-carrying 2-cell blocks rather than 235.

## S3.2 Transferability diagnostics versus transfer

Twenty candidate diagnostics from five families are each rank-correlated against the same target
quantity, the raw thermal transfer AUC over the twenty ordered directions, under one common
pair-based bootstrap. The families are marginal predictor-distribution measures P(ix), burned-niche
overlap P(x|y=1), fire-regime label-pattern structure P(y), and conditional feature-response
direction P(y|x).

The **marginal** family includes area-of-applicability-style dissimilarity in scaled,
importance-weighted predictor space [@Meyer2021; @Meyer2022; @Ludwig2023], climatic and geographic
distance, and a learned domain classifier trained to separate source from target cells. The
**niche-overlap** family includes Schoener's D [@Schoener1968] and Warren's I [@Warren2008] over the burned cells of each region.
The **regime** family includes burned-patch component counts and effective component counts. The
**conditional** family is the sign-agreement index: the fraction of predictors whose signed
univariate association points the same way in both regions, computed over all predictors and over
the subset whose associations are individually interval-supported.

Two properties of this design are stated in advance because they bound what it can show. The candidate set was recorded on 8 August 2026, together with its results under the original label
(commit d0b20af in the authors' version history, available on request). It was not re-selected
after the label correction. This is a record, not a pre-registration. And with five
regions the effective sample is ten unordered pairs, so nineteen computed variants are evaluated at
that power with no family-wise error control claimed; where a diagnostic clears an interval test but
not a Bonferroni threshold, both are reported.

## S3.3 Same-geography event-to-event comparison (Muğla 2021 versus 2022)

Muğla is the one region for which a second fire event is analysed on the identical AOI and analysis
grid, which allows the direction of feature-label associations to be compared with geography held
fixed. The 2022 experiment is registered with windows anchored to its own event: a 58-day predictor
window closing the day before ignition and a 49-day label window opening on it, matching the 2021
durations exactly.

**This is not a clean temporal-transfer design and is not presented as one.** The 2022 event ignites
about six weeks earlier in the season than the 2021 event, so calendar year and seasonal phase are
confounded and no difference can be attributed to the year alone. The registered claim is
same-geography event-to-event. The pair is deliberately kept out of the twenty-direction matrix, and
that exclusion is enforced in released code rather than merely asserted here.

Two further properties bound the comparison. A historical-burn exclusion applies to the 2022 arm
alone, masking every cell that burned in 2021 so the previous year's scar does not enter the
following year's analysis: it removes 3,073 cells, of which 2,941 belong to the primary population,
taking it from 41,730 rows to 38,790, a drop of 7.0 %. The two arms therefore share 38,789 of 38,790
cells and three byte-identical static predictors, and in the 2022-to-2021 direction every target
positive lies outside the source training population. Section S1.13 states what follows for how these
two numbers may be read.

**Table S19. Study regions, areas of interest and temporal windows.** Bounding boxes are in EPSG:4326,
as registered. Window lengths in brackets are inclusive day counts. The baseline years are the four
window-symmetric years preceding each predictor window.

| Region | Bounding box (lon min, lat min, lon max, lat max) | Predictor window | Label window | Baseline years |
|---|---|---|---|---|
| Manavgat 2021 (Türkiye) | 31.05, 36.72, 31.85, 37.35 | 2021-06-01 to 2021-07-27 (57 d) | 2021-07-28 to 2021-08-31 (35 d) | 2017, 2018, 2019, 2020 |
| Bejís 2022 (Spain) | -1.05, 39.68, -0.35, 40.15 | 2022-06-15 to 2022-08-14 (61 d) | 2022-08-15 to 2022-09-30 (47 d) | 2018, 2019, 2020, 2021 |
| Muğla 2021 (Türkiye) | 27.1, 36.6, 28.9, 37.45 | 2021-06-01 to 2021-07-28 (58 d) | 2021-07-29 to 2021-09-15 (49 d) | 2017, 2018, 2019, 2020 |
| North Evia 2021 (Greece) | 23.05, 38.55, 23.85, 39.15 | 2021-06-05 to 2021-08-02 (59 d) | 2021-08-03 to 2021-09-30 (59 d) | 2017, 2018, 2019, 2020 |
| Montiferru 2021 (Italy) | 8.45, 40.05, 8.75, 40.27 | 2021-05-25 to 2021-07-23 (60 d) | 2021-07-24 to 2021-08-31 (39 d) | 2017, 2018, 2019, 2020 |

## S3.4 Predictor provenance, compositing and the downscaler

Ten predictors are used, four baseline and six thermal, all summarised per cell over the predictor
window, through the chain shown in Fig. 2. All optical and thermal predictors come from Landsat 8 Collection 2 Level-2
(`LANDSAT/LC08/C02/T1_L2`), quality-screened per pixel from the `QA_PIXEL` band with the water bit
deliberately preserved; the coarse-resolution thermal input is `MODIS/061/MOD11A1`.

- **NDVI**, the predictor-window median of Landsat surface reflectance, is the baseline's one
  time-varying member.
- **Elevation** and **slope** come from the Copernicus DEM GLO-30, whose heights are referenced to
  the EGM2008 geoid (EPSG:3855) in metres according to the product handbook; the pipeline applies no
  datum conversion.
- **Land cover** is ESA WorldCover v200 [@Zanaga2022], entering as the dominant class code.
- **Current LST**, the predictor-window median of Landsat surface temperature in °C.
- **LST anomaly**, a z-score of the current-window LST median against the four baseline years,
  set to no-data where the baseline standard deviation is below 1.0 °C or observations are too few.
- **TVDI** and **TVDI difference**. The Temperature-Vegetation Dryness Index [@Sandholt2002] is
  computed in the LST-NDVI feature space, with wet and dry edges taken as the 2nd and 98th LST
  percentiles within each of twenty NDVI bins and the index clamped to [0, 1]. The edges are
  percentiles of the LST values a given scene contains, so they are fitted per AOI and per window,
  and a TVDI of 0.5 denotes a different physical moisture state in each region. **TVDI difference** is the raw
  anomaly of that index against the same four window-symmetric baseline years used for the LST
  anomaly: `tvdi_difference = current_tvdi − mean(baseline_tvdi)`, in index units rather than
  standard deviations, which is why it is reported alongside the z-scored channel rather than in
  place of it.
- **Downscaled LST** and **fused LST**. A MODIS-to-Landsat downscaling model is trained on the
  predictor window and applied to the full 30 m grid. The fused product equals observed Landsat LST
  wherever that is valid, and the downscaled surface only where it is not. Gap-filling therefore
  never replaces or blends a valid observation. The gap-filled share is 0.11 % to 9.70 % by region. The
  downscaler's own inputs include coordinates, which is the one route by which a coordinate-derived
  surface re-enters a feature set from which Section 3.13 excludes coordinates. Section S1.7
  reports the increment without these two channels.

**The six thermal channels carry about two signals.** In the primary population current, fused and
downscaled LST correlate at 0.97 to 1.00 in every region, current LST and TVDI at 0.88 to 0.98, and the
two anomaly channels at 0.71 to 0.94. Two principal components of the six hold 92 % to 98 % of their
variance, and their participation ratio is 1.6 to 1.8 (`paper/labelfix_rerun/labels/r4_dimensionality.json`).

**Table S20. Input data.** All retrieved through Google Earth Engine.

| Input | Product and version | Native resolution | Use | Reference |
|---|---|---|---|---|
| Burned area | MODIS MCD64A1 Collection 6.1 (`MODIS/061/MCD64A1`) | 500 m, monthly | label | [@Giglio2018; @MCD64A1] |
| Surface reflectance and temperature | Landsat 8 Collection 2 Level-2 (`LANDSAT/LC08/C02/T1_L2`), `QA_PIXEL` screening, water bit preserved | 30 m | NDVI, current LST, anomaly, TVDI | [@LandsatC2L2] |
| Coarse LST | MODIS MOD11A1 v061 (`MODIS/061/MOD11A1`) | 1 km, daily | downscaled and fused LST (gap-fill 0.11 % to 9.70 %) | [@MOD11A1] |
| Terrain | Copernicus DEM GLO-30 (EGM2008 heights) | 30 m | elevation, slope | [@CopernicusDEM] |
| Land cover | ESA WorldCover v200 (2021) | 10 m | dominant class, gate, population | [@Zanaga2022] |

Compositing is the predictor-window median; the anomaly channels reference four window-symmetric
baseline years (Table S19). WorldCover 2021 post-dates four of the five fires (Section 3.4).

## S3.5 Limitations, in full

Section 5.6 lists the limitations that affect the conclusions. All fourteen are given here.

(i) **No meteorological covariates** enter the models, so we cannot say how local skill and
portability behave for a mixed thermal-plus-weather predictor set.

(ii) **The same-geography comparison covers one region only**, and even there year and seasonal phase
are confounded. That confound cannot be resolved in this study area, and the reason is specific: the
two events sit 42 days apart in median burn day-of-year, neither year contains a second event at the
other's phase, and a calendar-matched arm would carry nine burned cells against this design's gate
minimum of thirty. The positive-block count for the 2022 arm is separately below the floor this
design sets itself, at eleven against sixteen (Section S1.13). Its 331 burned cells also leave the thermal reversals unresolved at interval level, and
the pair holds place fixed but not population. Those two arms were computed with the pipeline's unmodified code and the same pinned environment
rather than read from its frozen export.

(iii) **All labels derive from a single burned-area product**, MCD64A1 [@Giglio2018], whose omission
and commission characteristics [@Boschetti2019] bound every model evaluated here. Its Mediterranean
accuracy has been assessed against reference perimeters [@Katagis2022]. A second 500 m product,
VIIRS VNP64A1 [@VNP64A1], covers both years and was not used as a label sensitivity here.

(iv) **Evia remains the most imbalance-atypical population** even after the AOI extension. Its TSG
prevalence is 0.287, the highest in the cohort, against 0.070 to 0.212 in the other four.

(v) **Each region contributes one fire season**, so regional concept shift is confounded with event
meteorology, and distinguishing them requires multi-year labels.

(vi) **Point estimates depend on the software version.** Rerunning the frame-transfer matrix under
scikit-learn 1.5.2 instead of 1.9.0 moves single-direction AUCs by up to 0.023 for the thermal model
and 0.047 for the baseline, and paired differences by up to 0.045; the means move by at most 0.003,
and one direction changes interval support on each of the as-drawn and 10 km frames
(`paper/labelfix_rerun/round7/sklearn152/compare_vs_1_9_0.json`). All reported numbers are fixed to
one verified version, and exact reproduction requires the archived environment.

(vii) **Manavgat's atypical transfer is localised, not explained, and the localisation rests on one
region and one event.** Manavgat is the weakest target (0.435), carries the largest matched shortfall
(+0.319) and has the most outlying univariate profile in the cohort. Two processing candidates have
been tested and neither accounts for it: the quality screening of its coarse thermal input moves no
signed association by more than 0.005 (Section S1.5), and the evaluation frame leaves its elevation
reversal supported (Section 4.4). Holding elevation reverses
its raw LST association (Section S1.11). The low-lying burned cells explain part of it, but this rests on one region and one event.

(viii) **The interval-support measures are less stable than the point estimates behind them.** Five
to six of the pipeline's interval bounds lie within 0.01 of 0.5, under both labels. A single such
flag, Manavgat's NDVI, moved the full-frame supported-feature cosine from ρ = 0.49 to 0.70 when two
equally valid bootstrap streams disagreed on it. The transfer verdicts are steadier.
Across five bootstrap seeds, every verdict at 1 km blocking is stable, and the paired split of twelve
positive, seven negative and one uncertain holds on every seed. At 5 km blocking, one level verdict
and two paired-delta verdicts change with the seed. Every sentence in this paper that leans on an
exact count of supported directions should be read at that precision.

(ix) **The five areas of interest are not comparable frames, and this cohort cannot fully repair it**
(Section 4.4). We report the equalised arm alongside the frame-as-drawn arm rather than replacing one
with the other, because the collar radius is itself a choice and 5 km and 10 km do not agree exactly
(0.591 against 0.589). The deeper limitation is that the frames were fixed upstream of this work, in
`repo/`, so we can restrict them but not extend them; a region whose rectangle is already fire-scale,
Montiferru, cannot be given a far field for symmetry. Nor can their independence from outcomes be
fully documented: only Montiferru's box is derived by a rule, Manavgat's is dated before its first gate result, and for Bejís and Muğla the
version history cannot show the box fixed before the first gate result (Section 3.1). Any future cohort should fix the frame by an
explicit accessible-area rule [@Barve2011] before any predictor is computed, and we treat that as the
main design lesson of this paper.

(x) **Other classifiers are compared by point estimate only.** The headline numbers use a random forest with unlimited depth, the
configuration most able to encode local structure and least able to extrapolate. Section S1.8 shows the transfer result is not an artefact of that
choice: three further estimators, including a penalised linear one, all land between 0.481 and 0.527
and place eleven to thirteen of twenty directions above chance. Those are point estimates without
intervals, so the ordering among them is not claimed as a result. Other estimator classes were not tried. Across the four that were tried, the negative result does
not depend on the estimator.

(xi) **Burn timing and elevation are confounded in Manavgat.** The cells that burned in the
first four days lie at a median of 219 m, against 512 m for the later burns and 1,004 m for
unburned cells. The effects of timing and elevation cannot be separated in this data.

(xii) **The quality-screening comparison differs in code version as well as in screening.** The
current pipeline's step7 refuses the unscreened MODIS input, because the raster carries no nodata tag
and 8.1 % exact zeros. The unscreened arm therefore uses the step7 of export time, and the screened
arm the current one. The two agree on elevation to four decimals and on every other signed AUC to
within 0.005, the largest move being downscaled LST at −0.0044. The within-region increment moves
from +0.067 to +0.068. The confound could therefore have hidden an effect only if two effects had
cancelled (Section S1.5).

(xiii) **The diagnostic correlations rest on an effective sample of ten region pairs.** Five regions
give twenty ordered directions, but the two directions of a pair share both regions and are not
independent. The diagnostic results of Section S1.22, successes and failures alike, read at that
power: with ten pairs a moderate true ordering would usually be missed.

(xiv) **The frame cost rests on few scars.** The full four-row comparison of Section 4.3 is defined on
seven scars in three regions, and its scar-level intervals are pseudo-replicated because row A
repeats across a region's scars. The region-level estimates (+0.137 over three regions, +0.160 over
five) are the ones to quote.

## S3.6 Leakage control and reproducibility, in full

An explicit forbidden-column set is enforced at every model fit. Coordinates (`lon`, `lat`, `row`,
`col` and their normalised forms), every burn-date and label-provenance column, and the agreement
fraction are excluded from all feature sets, and the enforcement runs as an assertion rather than a
convention. The natural-vegetation mask is used only to define the population, never as a predictor.
Spatial blocking prevents a cell from sharing a fold with its own neighbours.

**Reproducibility.** All randomness uses seed 42 and the bootstrap uses 1000 replicates throughout.
The transfer and adaptation analysis runs in an environment separate from the upstream pipeline's.
Every within-region model was therefore refitted there and compared against the frozen upstream
output, and the independently implemented adaptation was compared against the pipeline's own. The
within-region comparisons agree exactly and the twenty directed CORAL transfers to within 1.3×10⁻⁸
against the re-frozen outputs (1.6×10⁻⁷ against the frozen ones), under the repository's
pre-existing tolerance of 10⁻⁶ (Section 3.13). All numbers here were produced under scikit-learn 1.9.0 or verified against it; the
version sensitivity is stated in Section S3.5(vi).

**Sensitivity analyses.** The within-region results are repeated across three spatial-block sizes,
four classifier capacities and, in two regions, a second population; the transfer results across both
feature sets, the CORAL sweep, the Evia AOI variant and three evaluation frames; where a
conclusion depends on one of those choices the dependence is reported rather than resolved by
choosing the favourable setting (Section S1).

### S3.6.1 Resampling units

Uncertainty is a spatial-block bootstrap. Let $`\beta_1, \dots, \beta_M`$ be the blocks of
[#eq:block] holding cells of $`F`$. Replicate $`b`$ draws $`M`$ indices $`u_{bm}`$ uniformly with replacement:

```math {#eq:boot}
F^{*b} = \biguplus_{m=1}^{M} \beta_{u_{bm}}, \qquad \mathrm{CI}_{95} = \left[ Q_{0.025}\{\theta(F^{*b})\}_{b},\; Q_{0.975}\{\theta(F^{*b})\}_{b} \right].
```

Here $`\theta`$ is the statistic and $`Q`$ the 2.5 and 97.5 percentiles over 1000 replicates, seed 42. A
single-class replicate is discarded. Differences are formed within each replicate, so they are
paired. The block size of each interval is stated with the result. Because it is blocks that are resampled,
what bounds an interval's reliability is the number of blocks carrying at least one burned cell, and
those counts are reported alongside the intervals. Where a verdict rests on too few such blocks it
is stated as indicative rather than as an interval.

The twenty transfer directions are not independent, since each region appears in eight. The
**pair-cluster bootstrap** therefore resamples the ten unordered region pairs, each carrying its set
$`\pi_p`$ of ordered directions, and averages the carried values $`\delta_{st}`$:

```math {#eq:pair}
\bar{\delta}^{*b} = \frac{\sum_{m=1}^{10} \sum_{(s,t) \in \pi_{u_{bm}}} \delta_{st}}{\sum_{m=1}^{10} |\pi_{u_{bm}}|}.
```

The interval is the same percentile form, over 1000 replicates for the direction-level intervals of
Sections 4.4 and 4.5, and 20,000 for the unit comparison of Table S31. Clustering by
target region replaces $`\pi_p`$ by the four directions sharing a target. A quantity with one value
per held-out scar or target region gets a Student t interval over those $`n`$ units,

```math {#eq:tint}
\bar{x} \pm t_{0.975,\,n-1}\, s_x / \sqrt{n}.
```

**The effective sample is thus ten pairs or five regions for direction-level intervals, and at most
seven scars from three regions for scar-level ones.**

### S3.6.2 Reproduction of the re-frozen outputs

The transfer analysis runs in an environment separate from the upstream pipeline's. The
repository's own reproduction check therefore refitted every within-region model and all twenty
directed CORAL transfers against the frozen upstream output. For Manavgat that output is the one
re-frozen on the corrected label (Section 3.2), produced with the upstream pipeline at commit
6381f4c, run unchanged apart from a one-line patch and a runtime override. The patch lets the
window-closure module accept a population column the corrected label adds, and its diff is released
with the re-freeze; the override points the Earth Engine calls at the project `thermaltwin`, which
changes infrastructure only. The
within-region comparisons agree exactly, and the transfer directions to within 1.3×10⁻⁸, under the
repository's pre-existing tolerance of 10⁻⁶. That 10⁻⁶ tolerance belongs to the CORAL and within-region reproduction check. The frame-transfer
script of Section 4.4 fits its forests in parallel, so its values vary from run to run by up to
2×10⁻⁶ (1.4×10⁻⁶ in a rerun on 29 September 2026,
`paper/labelfix_rerun/round7/`), within the 10⁻⁵ tolerance applied to it, and are stable at the printed precision. The tolerance that applies if the library
version is not pinned is given in Section S3.5(vi).

## S3.7 Transfer-gap decomposition and the concept-shift diagnostic, in full

For each direction the gap between the target's own within-region skill and the raw transfer result
is split in two. One part is what the best label-free adaptation recovers, and the other is what it
does not. The recovered fraction is (adapted − raw) / (within − raw), signed and unclipped, with its interval
from the same paired bootstrap; it bounds what covariate-level correction can achieve. Section 4.3
shows the remainder should not be read as a conditional residual, because much of it is incurred
inside a single region (Section S1.10).

The mechanism is diagnosed by **signed univariate association**. For each numeric predictor the raw
ROC-AUC of that predictor against `burned` is computed in each region and never folded to
max(AUC, 1 − AUC), so a value below 0.5 is read as a direction rather than as weakness. A reversal is
called bootstrap-supported only when the two regions' point estimates fall on opposite sides of 0.5
**and each region's own interval excludes 0.5**, under the same 10-cell spatial-block bootstrap.
That is stricter than requiring the two regions' intervals to be disjoint: a feature whose intervals
are disjoint but one of which straddles 0.5 has not been shown to point anywhere in that region, so
it is recorded as a point reversal only. Section S2 states the rule again beside the counts, and
`conditional_similarity_transfer.json` carries it as machine-readable metadata.

---

### S3.7.1 Degenerate replicates

Replicates with $`|G| < 10^{-6}`$ are dropped.

## S3.8 Label-blind adaptation, full specification

**Region-wise z-score.** Each region's numeric features are standardised using its own statistics,
source statistics from source data and target statistics from target data, never pooled. For
feature $`j`$ in region $`R`$,

```math {#eq:zscore}
z_{ij} = \frac{x_{ij} - \mu_j^{R}}{\sigma_j^{R}}, \qquad \mu_j^{R} = \frac{1}{n_j^{R}} \sum_{i \in O_j^{R}} x_{ij}, \qquad \sigma_j^{R} = \Big( \frac{1}{n_j^{R}} \sum_{i \in O_j^{R}} (x_{ij} - \mu_j^{R})^2 \Big)^{1/2},
```

where $`O_j^{R}`$ holds the $`n_j^{R}`$ cells with an observed value (ddof 0). A missing value is
first set to $`\mu_j^{R}`$, so it becomes zero, and $`\sigma_j^{R} < 10^{-12}`$ is replaced by 1.
Land cover is not transformed. Target feature statistics, never target labels, thus enter the
adapted arms by design. The
classifier is refitted on the z-scored source and applied to the z-scored target. This removes
first- and second-order marginal offsets.

**CORAL after region-wise z-score.** The source covariance is aligned to the target's by the standard
whitening-recolouring map [@Sun2016]. With $`Z_R`$ the $`n_R \times d`$ matrix of z-scored numeric
features, one row per cell,

```math {#eq:coral}
Z_s^{\mathrm{al}} = Z_s\,(C_s + \lambda I)^{-1/2}\,(C_t + \lambda I)^{1/2}, \qquad C_R = \frac{1}{n_R} \sum_{i=1}^{n_R} (z_i - \bar{z}_R)(z_i - \bar{z}_R)^{\top},
```

with $`\lambda = 10^{-5}`$ (ddof 0). Both means are zero after [#eq:zscore], so the general map's
mean terms vanish. Matrix powers use a symmetric eigendecomposition, eigenvalues floored at
$`10^{-12}`$. Critically **the transform is applied to the source
only**; the target stays at $`Z_t`$, and the classifier is refitted on $`Z_s^{\mathrm{al}}`$. Neither
variant sees a target label, and both are verified label-blind at run time. λ sensitivity was assessed over nine
values on four of the twenty directions, moving transfer AUC by at most 0.014, and no value of λ was
selected on performance; the λ = 1 of the original CORAL formulation lies outside that sweep, while
the value used throughout remains λ = 10⁻⁵ (Section S1.2).

# S5 Target-label recovery curve

## S5.1 Purpose

The main text establishes that label-free alignment does not close the transfer gap. The natural
constructive question is what a small number of target labels buys, since that is the resource
label-free methods cannot substitute for. This analysis prices the failure; it is not a proposed
method and not an operational claim, because the labels it uses come from the event being predicted.
It covers three of the five regions (Manavgat, Bejís and Muğla), all six directions among them.
Source: the pipeline's few-shot recovery diagnostic on the corrected label, analysis
`7348dfe7…`, released in `paper/labelfix_rerun/exports/few_shot_recovery_7348dfe7/`
(`recovery_curve.csv`, `repeat_metrics.csv`, `report.md`); every value below is read from it.

## S5.2 Design

The unit of labelling effort is one 10-cell (≈5 km) spatial block of the target. For a budget of k
blocks, k target blocks are drawn from the training folds of a 5-fold spatially blocked split of the
target, their labels are added to the source training set, and the refitted model is scored on the
held-out target folds. Budgets are 0, 1, 2, 4, 8, 16 and 32 blocks, with ten repeats of the block
draw for every k > 0. Budget 0 is raw transfer. The **ceiling** is a target-only model at the same
10-cell blocking (0.777 for Muğla, 0.824 for Bejís and 0.882 for Manavgat), which reproduces the
pipeline's own large-block values exactly. The **recovered fraction** is (few-shot − raw) / (ceiling
− raw), the share of the gap between raw transfer and the ceiling that the labels close; it is signed
and unclipped. Intervals are **selection intervals**, the 2.5th and 97.5th percentiles over the ten
block draws; they describe which blocks were drawn and nothing else, and no hypothesis test is made.

## S5.3 Result

**Table S22. Few-shot recovery of target ROC-AUC, thermal model, natural-vegetation population.** Raw
= source-only transfer (budget 0); ceiling = target-only model at the same 10-cell blocking. Values
are the mean over ten block-selection repeats.

| Direction | Raw | 1 blk | 2 blk | 4 blk | 8 blk | 16 blk | 32 blk | Ceiling | Gap closed at 32 |
|---|---|---|---|---|---|---|---|---|---|
| Bejís → Manavgat | 0.314 | 0.518 | 0.565 | 0.659 | 0.698 | 0.750 | 0.820 | 0.882 | 89 % |
| Muğla → Bejís | 0.583 | 0.578 | 0.603 | 0.625 | 0.666 | 0.743 | 0.789 | 0.824 | 85 % |
| Manavgat → Bejís | 0.396 | 0.447 | 0.456 | 0.541 | 0.598 | 0.690 | 0.752 | 0.824 | 83 % |
| Muğla → Manavgat | 0.345 | 0.358 | 0.380 | 0.407 | 0.437 | 0.505 | 0.624 | 0.882 | 52 % |
| Manavgat → Muğla | 0.438 | 0.447 | 0.453 | 0.468 | 0.490 | 0.532 | 0.571 | 0.777 | 39 % |
| Bejís → Muğla | 0.618 | 0.576 | 0.577 | 0.578 | 0.598 | 0.637 | 0.666 | 0.777 | 30 % |

**At 32 blocks three of six directions close 83 to 89 % of the gap to the ceiling**, two of which
started below chance; the other three close 30 to 52 %. Thirty-two blocks carry 2,740 to 2,970
labelled cells, 7 to 20 % of the target's natural-vegetation population. That is not a modest
budget: into Bejís the labelled blocks at 32 carry on average 880 of the region's 1,100 burned cells,
and into Manavgat about 1,800 of 2,935.

**Recovery is slow where transfer is worst.** Muğla → Manavgat, whose raw transfer sits furthest
below its ceiling, is still below 0.5 after 8 labelled blocks and closes 52 % at 32.

**Small budgets hurt the direction that already transfers.** Bejís → Muğla transfers above chance
raw (0.618), and few-shot recalibration helps it least: the curve is below raw at 1, 2, 4 and 8
blocks (0.576 to 0.598), overtakes raw only at 16, and closes 30 % at 32. Where the source model
already carries a usable relationship, a small target sample perturbs it before it can replace it.

## S5.4 Limits

1. **Three regions, six directions.** Evia and Montiferru are absent, so this covers six of the
   twenty directions and cannot speak to the five-region scope; six directions cannot support a
   general label budget, so none is offered.
2. **It requires labelled target cells** from the event being predicted. Nothing here is a
   label-free method, and nothing here weakens the negative result about label-free alignment.
   Whether labels from earlier fires in the same region would serve is not tested.
3. **The interval is a selection interval, and at the top budgets it narrows because the pool is
   exhausted, not because the value is well estimated.** Per outer fold the target holds on average
   about 12 blocks containing both classes in Bejís, 29 in Manavgat and 48 in Muğla, so at 16 and 32
   blocks the draw has nearly exhausted the both-class blocks and repeats select almost the same set
   (`direction_budget_feasibility.csv`).
4. **The ceiling is the 10-cell target-only value**, not the ≈1 km within-region figure of Table 1,
   and is correspondingly lower. The recovered fractions are only interpretable against this
   matched-blocking ceiling, and on the frames as drawn, which Section 4.4 shows are not comparable
   across regions.

# S6 Code

The analysis code is public at <https://github.com/dryuemco/thermal-twin> under the MIT licence;
this section is a guide to it, and the repository's README gives the same information. The
satellite processing pipeline is a separate public repository,
<https://github.com/emrehann17/satellite-thermal-digital-twin> (MIT licence), at commit `6381f4c`
for the re-frozen Manavgat outputs; the other regions' outputs were produced at earlier commits of
that repository and are reproduced by it (Section S3.6.2).

| Path | Role |
|---|---|
| `paper/code/` | Analysis and verification scripts. `_canonical.py` loads every modelling dataset, verifies its SHA-256 and asserts the leakage exclusions of Section 3.13 at every fit. |
| `paper/code/appendix_tables.py` | Rebuilds Tables S2 to S7 and S9 to S18 row by row from source files whose SHA-256 values are pinned in `paper/labelfix_rerun/round5/tables/SOURCES.sha256`, and compares them with this document. |
| `paper/figures/` | One script per figure. Each asserts every plotted value against the frozen outputs and the manuscript text, and checks its layout. |
| `paper/figures/check_all.py` | Runs all figure scripts and `appendix_tables.py`, restores the committed outputs byte for byte, and exits 0 when everything passes. |
| `paper/tex/` | Builds the manuscript and this document from their Markdown sources and checks the port: every number survives, and every cross-reference, citation and supplementary reference resolves. |
| `paper/labelfix_rerun/` | The corrected-label outputs from which every corrected number is read: `code/`, `geometry/`, `inference/`, `labels/` and `round3/` to `round7/` hold the analysis outputs, `pipeline/` the re-frozen pipeline outputs for Manavgat, and `exports/` the released pipeline diagnostics (few-shot recovery, CORAL λ sweep, window closure), each with its SHA-256 in `exports/SHA256SUMS.txt`. |

All commands run from the repository root. The environment is Python 3.12.10 with NumPy 2.4.4,
pandas 3.0.2 and scikit-learn 1.9.0, pinned in `ENVIRONMENT.md`; point estimates depend on the
scikit-learn version (Section S3.5(vi)). Fig. 1 additionally needs cartopy; without it
`check_all.py` reports that figure as skipped. Tables S1, S20 to S34 and the prose values are not
covered by `appendix_tables.py`; they name their source files in their captions or text.

# S7 Data

All satellite inputs are public and were retrieved through Google Earth Engine (Table S20). No
proprietary or restricted data were used.

The five modelling datasets the analyses read are in the analysis repository, one per region, as
`paper/data/<region>/step8a_500m_modeling_dataset.parquet`, each verified on load against the SHA-256
recorded in `paper/code/_canonical.py`. For Bejís, Muğla, North Evia and Montiferru that hash equals
the pipeline's canonical-input record. For Manavgat the file is the corrected-label re-freeze
(SHA-256 `5a5e876c…`; Section S3.1.2); the pipeline's record still names the original-label table
(SHA-256 `054a1961…`), which is not in the repository and is regenerated by the pipeline. The frozen
numeric outputs every table and figure is built from are in the same repository, identified by the
paths and hashes named in the table captions and in `SOURCES.sha256`. The data derived from Landsat,
MODIS, the Copernicus DEM and ESA WorldCover remain subject to those products' terms, which the
Declarations reproduce.
