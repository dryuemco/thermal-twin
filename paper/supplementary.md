# Supplementary Material

Supplementary material for *Evaluation area and the limits of cross-region transfer of single-season wildfire models with pre-fire thermal predictors: five large Mediterranean fires*.

This supplement holds the checks, the per-scar and per-region detail, the full tables and the
derivations that the main text refers to. The figures carry most of these results, and the text adds
what they do not show. Every value is read from a released output of the repository
<https://github.com/dryuemco/thermal-twin>, and each figure and table names its source. File paths
that do not start with `paper/` are under `paper/labelfix_rerun/`, which holds the corrected-label
outputs, and values computed under the original Manavgat label are marked "original label".

## Contents

- S1 Robustness checks
  - S1.1 The within-region gain
  - S1.2 Cross-region transfer
  - S1.3 Resampling units
  - S1.4 Further checks
- S2 The evaluation frame within a region
  - S2.1 Scar by scar
  - S2.2 Distance from the training cells
- S3 Signed associations and the frame test
  - S3.1 Signed associations and reversals
  - S3.2 The 10 km collar
  - S3.3 The temperature sign with terrain held
  - S3.4 The contrast pair
  - S3.5 The two Muğla fires
- S4 Transfer, adaptation and similarity
  - S4.1 The transfer matrix
  - S4.2 The transfer-gap decomposition
  - S4.3 Precision and recall
  - S4.4 Pooled training
  - S4.5 Similarity measures
- S5 Data and methods
  - S5.1 Label, grid, gate and the Manavgat correction
  - S5.2 Study areas and windows
  - S5.3 Predictors
  - S5.4 Resampling units
  - S5.5 Gap decomposition and reversal criterion
  - S5.6 Label-free adaptation
  - S5.7 Reproduction, code and data

# S1 Robustness checks

## S1.1 The within-region gain

Fig. S1 sets the within-region thermal gain under each check beside the gain it was compared with.
The only interval that includes zero is that of Montiferru with aspect added, +0.020 [−0.025,
+0.066], against +0.099 without aspect. Section 3.4 gives the collar means without intervals. With
Student *t* intervals over regions they are +0.083 [+0.037, +0.129] on the 10 km collar and +0.087
[+0.037, +0.136] as drawn, and on the 5 km collar the mean halves to +0.042.

![**Fig. S1. The within-region thermal gain under each check, by region.** Thermal minus baseline
ROC-AUC. Open dots are the reference that a check is compared with (italic headings), which is the 5
km-blocked gain, the 1 km-blocked gain of the random forest of the main text or the pipeline's own
window diagnostic. Filled dots are the gain with the check, and lines are 95 % block-bootstrap
intervals where the source gives one. Drawn by `paper/figures/figS1_within_checks.py` from
`inference/ladder_summary.json`, `round8/` (r8b, r8j, r8m, r8n), `labels/r2_history.json`,
`round3/no_coord_channels.json`, `code/model_capacity.json` and
`exports/window_closure_<region>/`.](figures/figS1_within_checks.png){width=100%}

Some details are not in the figure. The VNP64A1 and MCD64A1 labels agree at a Jaccard index of 0.865
(Montiferru) to 0.978 (Evia). With WorldCover 2020 (Section 2.4), the share of burned Montiferru
cells with at least half natural vegetation rises from 0.773 to 0.977 on the modelled cells, whereas
the gate fraction of Table 1 comes from the gate's own inputs. In Bejís, 48 cells burned inside the
predictor window, and ten of these 48 are labelled burned. Removing all 48 cells changes transfer in
the eight Bejís directions by at most 0.015. Rebuilding the Manavgat chain from a quality-screened MODIS input
moved the gain from +0.067 to +0.068 and no signed association by more than 0.005
(`round6/qc/qc_compare_manavgat_corrected.json`), although the two versions also differ in pipeline
code, because the current step7 refuses the unscreened raster. The secondary population of all valid
cells (Section 2.5), which exists only in Manavgat and Bejís, gives gains of +0.048 to +0.061 over
the two regions and three block sizes, every interval above zero, against +0.045 to +0.067 in the
primary population (`pipeline/robustness/step8_large_block_primary_all_valid/`).

## S1.2 Cross-region transfer

Fig. S2 repeats the transfer analysis under each check. Mean transfer ranges from 0.481 (penalised
logistic regression) to 0.566 (the twelve directions without Manavgat), against 0.527 as drawn, and
every interval of the thermal gain includes zero. Without Manavgat, mean transfer on the 10 km
collar is 0.631, with no direction below chance (`round8/r8d_summary.json`).

![**Fig. S2. Mean cross-region transfer under each check.** (a) Mean thermal ROC-AUC over the
twenty directions (twelve without Manavgat). (b) Mean thermal minus baseline ROC-AUC, which for the
three predictor sets is taken against the baseline-only model (0.519). Lines are pair-cluster 95 %
intervals where computed, and thick bars are ranges over ten random-forest seeds. The last three
target frames use no target label and are the cells inside the source's predictor range or area of
applicability [@Meyer2021], or a 20 km square at the centre of each study area. Drawn by
`paper/figures/figS2_transfer_checks.py`, which lists its sources.](figures/figS2_transfer_checks.png){width=100%}

Section 3.5 compares the anomaly and the absolute channels in transfer. Within regions both sets lie
between the baseline (0.797) and all ten predictors (0.896). Between the two Muğla fires the anomaly
channels keep their direction and the absolute channels do not (Section S3.5), but
`lst_anomaly_mean` reverses between regions (Table S3), so normalisation protects a channel against
a change of season in one place and fails across places.

Section 3.6 gives the mean effect of removing elevation and the LST anomaly together (Fig. 7). By
region the within-region change is −0.035, −0.130, −0.073, −0.063 and −0.079 (Manavgat, Bejís,
Muğla, Evia and Montiferru), with every interval below zero (`round8/r8q_summary.json`). About three
quarters of this cost comes from elevation, because without it alone the mean falls from 0.896 to
0.840, and without the LST anomaly alone to 0.883.

On the earlier, smaller Evia rectangle, whose burned prevalence is higher, the raw transfers between
Evia and Bejís, Manavgat and Muğla moved by up to 0.134 (Evia to Manavgat, 0.543 against 0.677), and
none changed side of chance (`round7/r7f_evia_legacy.csv`).

CORAL hardly depends on its regularisation. Over nine values of λ from 0 to 10⁻¹ on four directions,
transfer moved by at most 0.014 (`exports/coral_lambda_sensitivity_b74d643e/`), and the Manavgat and
Bejís pair, whose adapted result depended on λ under the original label, stays below chance in both
directions at every λ from 10⁻⁵ to 1 (`step10/coral_lambda_sensitivity.csv`). Section 3.5 reports
CORAL with λ = 1 and a placebo that aligns each source with a third region instead of the target.
Both come from `round8/r8c_summary.json`, which also gives CORAL on two thermal principal
components, at a mean of 0.523.

## S1.3 Resampling units

Fig. S3 gives the interval of the paired thermal contribution under every resampling unit that can
be computed. On the 10 km collar the two units that exclude zero are the clusters by target region,
[+0.010, +0.040], and by source region, [+0.010, +0.042], but with five regions a percentile
bootstrap over regions has at most 126 distinct resamples, so both are coarse. The two-way cluster
and dyadic-robust estimators give negative variances and are undefined. In the equivalence test of
Section 3.4, the 90 % upper bounds as drawn are 0.021 to 0.037, and no unit keeps the gain within a
narrower margin of 0.02. The two units that exceed the margin of 0.05 on the collar are the
pigeonhole bootstrap and the region jackknife (upper bounds 0.052 and 0.055). Leaving out one region
at a time moves the mean contribution between +0.0010 (without Evia) and +0.0148 (without Manavgat),
and its sign never changes (`code/transfer_delta_ci.json`).

![**Fig. S3. The paired thermal contribution to transfer, by resampling unit.** Mean thermal minus
baseline ROC-AUC over the twenty directions (dot) and its 95 % interval (line), (a) on the study
areas as drawn and (b) on the 10 km collar, with 20,000 replicates where resampled. Blue is the
pair-cluster bootstrap, the primary unit of the main text, whose interval as drawn is [−0.020,
+0.038] at the 1000 replicates used there. Drawn by `paper/figures/figS3_units.py` from
`round8/r8d_summary.json`, `inference/units.json`, `code/transfer_delta_ci.json` and
`round8/r8l_summary.json`.](figures/figS3_units.png){width=100%}

## S1.4 Further checks

Table S1 lists the checks that are not plotted. Like those of Figs. S1 to S3, they were run after the
main results, and none was used to choose a reported configuration.

**Table S1. Further checks.** Sources in `geometry/` (a1 to a5) and `round8/` (R8 labels).

| Check | Result |
|---|---|
| Scar edge (a1) | Excluding 0, 1 or 2 edge cells from the scar frame leaves the frame cost (A − B, nine scars) at 0.147 [0.086, 0.208], 0.137 [0.069, 0.205] and 0.129 [0.055, 0.204]; with the region as unit 0.160, 0.150 and 0.145, every interval above zero |
| Placebo collars (a2) | The burned cells of a scar scored against the unburned cells of a same-shaped collar placed away from any burned cell reproduce A (A − placebo −0.002 [−0.056, +0.052], eight scars); the real collar costs +0.155 [+0.108, +0.202] more |
| Distant cells (a3) | The frame cost does not grow with the share of cells beyond 10 km: region-level slope 0.005 [−0.41, +0.42], r = 0.02 (n = 5); scar-level slope −0.049 [−0.34, +0.24] (n = 9, scars not independent) |
| Other metrics (a5) | Region-wide minus scar frame over nine scars: partial AUC (FPR ≤ 0.1) 0.088 [0.048, 0.128]; average precision −0.342 [−0.477, −0.206], higher on the scar frame because its prevalence is higher |
| Ten forest seeds (R8a) | The seed-to-seed standard deviation of a direction has a median of 0.005 (maximum 0.015), and no direction changes side of chance as drawn; on the 10 km collar one does (Montiferru to Manavgat). Averaging the ten forests gives 0.527 (gain +0.006) as drawn and 0.590 (+0.025) on the collar |
| Capture of burned cells (R8b, R8g) | In transfer, the 10 % of target cells with the highest thermal scores hold 10.3 % of the burned cells on average (0.7 % to 27.1 %), as a random ranking would, and eight of twenty directions fall below that; the top 20 % hold 19.9 %. Within regions (5 km blocking) the top 10 % hold 35.5 % (18.9 % to 44.5 %) and the top 20 % 55.7 % |
| Weather reference (R8o) | Across the five regions the mean Landsat LST anomaly follows the ERA5-Land air-temperature anomaly of the predictor window (Spearman ρ = 0.8) but not the relative-humidity anomaly (ρ = 0.0), and neither does the TVDI difference (ρ = 0.0); with five regions this is descriptive |
| Missing thermal values (R8p) | 1.7 %, 6.5 %, 3.2 %, 4.5 % and 0.1 % of the modelled cells (Manavgat, Bejís, Muğla, Evia, Montiferru) lack at least one thermal channel; this flag scores 0.493 to 0.512 against burning |
| Residual spatial correlation (R8l) | Out-of-fold residuals of cell pairs correlate at 0.58 to 0.83 below 1 km and 0.15 to 0.48 at 5 to 10 km (Montiferru −0.01); the correlation falls below 0.05 at 10 to 20 km in Manavgat, Bejís and Muğla, at 20 to 40 km in Evia and at 5 to 10 km in Montiferru, so 5 km intervals may be too narrow, most of all in Evia |
| Pooled against fold AUC (R8l) | The mean of the five fold AUCs is 0.004 to 0.018 above the pooled out-of-fold AUC in every region (thermal model, 5 km blocking) |

# S2 The evaluation frame within a region

## S2.1 Scar by scar

Fig. S4 shows the evaluations of Section 3.3 for each scar. Manavgat and Bejís have no row C,
because each has one burned area and withholding it would leave nothing to train on. The three
controls reuse the predictions of A and are averaged over 20 draws without replacement. The
prevalence-matched sample draws $`|H_K^{+}|`$ burned and $`|H_K^{-}|`$ unburned region cells, the
negative-pool swap keeps the drawn burned cells and takes the unburned cells of the scar,
$`H_K^{-}`$, and the positive-pool swap does the opposite.

Over nine scars the prevalence-matched sample (A′) scores 0.793 against 0.791 for the whole region,
as ROC-AUC should, so the fall to 0.644 on the scar area (B) is not an effect of prevalence. The
pool swaps of Section 3.3 (`code/pool_decomposition.json`) place the cost in the unburned cells next
to the fire, which share its terrain, land cover and weather. Row A repeats one region value for
each scar of a region, so the Student *t* intervals of Table 3 for row A, A − B and A − C are too
narrow, and the region-level estimates of Section 3.3 come from `round7/round7_summary.json`. Row C
depends little on how a scar is defined. Over a range of minimum sizes and buffers it
ranges from 0.541 to 0.561 on nine to six scars (`code/scar_definition_sweep.csv`). For a single
scar, row D depends on which region is the source (over the 36 source-scar combinations the mean is
0.556, and ten are below chance).

Fig. S4b breaks down the thermal gains of Section 3.3 by scar. Over the seven scars at 5 km blocking
they average +0.095 on the whole region, +0.021 on the scar area, +0.024 with the scar withheld and
+0.008 from a foreign region. Scar area minus withheld is −0.004 [−0.070, +0.063] (+0.031 [−0.027,
+0.090] at 1 km), and whole region minus scar area +0.074 [−0.009, +0.157], but with three regions
no reliable region-level interval exists for these differences (`inference/ladder_summary.json`). A
half-split of each region gives a gain of +0.028, positive in 13 of 18 splits, although a straight
cut leaves unequal numbers of burned cells in the two halves (`code/positive_control.json`).

![**Fig. S4. The evaluations of Section 3.3, scar by scar.** (a) Thermal ROC-AUC of one region model
scored on the whole region (A) and on the scar area (B), of a model fitted without the scar (C) and
of the models of the other four regions (D, mean of the four). Each grey line is one scar, and the
dark line is the mean, whose value is printed under each design. Manavgat and Bejís have no row C,
and the horizontal line marks chance. (b) Thermal minus baseline ROC-AUC under A, B, C and D for the
seven scars with a row C. Natural-vegetation population, 5 km blocking, 2 km collar. Drawn by
`paper/figures/figS4_scars.py` from `code/matched_holdout.json`, `code/prevalence_control.json`,
`code/d_per_source.json` and `inference/ladder_summary.json`.](figures/figS4_scars.png){width=100%}

## S2.2 Distance from the training cells

Fig. S5 draws the distance curve of Section 3.5 (`paper/code/distance_curve.py`), and this section
gives its caveats. The far bins hold few cells, so the rise at 40 to 80 km is not evidence of an
effect, and the near bins keep the spatial autocorrelation that blocked validation removes, so 0.709
is an upper bound. The two distance ranges do not overlap (2 to 86 km within regions, 306 km and
more across them), and distance is not separated from the land cover, terrain and fire history that
change with it, so the curve gives a length scale and no cause. Once the curve reaches chance, any
cross-region mean near 0.5 lies on its continuation, so this comparison cannot show that the
cross-region failure is only an effect of distance. A model without information gives no reliably
reversed ranking, yet Manavgat to Bejís is below chance with interval support on both frames. A
leave-one-block-out reference with a 10 km buffer was tried and is not reported, because its pooled
AUC mixed models with different calibration.

![**Fig. S5. Within-region skill by distance from the training cells.** Mean target ROC-AUC,
unweighted over the distance bins of the five regions. The number of bins is under each class, and a
bin holds 1 to 1,067 burned cells. The open dot is the mean of the twenty cross-region directions,
306 to 2,802 km apart. Drawn by `paper/figures/figS5_distance.py` from
`round7/r7h_distance_curve.csv`.](figures/figS5_distance.png){width=65%}

# S3 Signed associations and the frame test

## S3.1 Signed associations and reversals

Table S2 gives the signed association of each predictor with burning in each region, and Table S3
the pairs of regions that reverse under the strict criterion of Section 2.10. This criterion is
stricter than disjoint intervals. For `current_lst_mean` the Manavgat and Bejís intervals are
disjoint ([0.608, 0.719] against [0.401, 0.547]), but the Bejís interval includes 0.5, so the pair
reverses at the point estimate only.

**Table S2. Signed univariate AUC of each predictor against `burned`, by region.** Natural-vegetation
population, with a 10-cell (~5 km) spatial-block bootstrap (1000 replicates, seed 42). The AUC is
not folded to max(AUC, 1 − AUC), so a value below 0.5 means that lower values rank burned cells
higher. Bold marks a region whose own interval excludes 0.5. Source
`round5/tables/step9g_multi_aoi_feature_stability.csv` (the pipeline's Step9G synthesis, sha256
c864cd7d…).

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

**Table S3. Cross-region reversals that meet the strict criterion.** From the intervals of Table S2.
Difference intervals from the paired 10-cell block bootstrap of
`paper/code/ems_inference_multiplicity.py` (`inference/reversal_family_holm.csv`, 1000 replicates),
which flags the same fourteen pairs.

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

Thirteen of the fourteen reversals involve Manavgat. Under the original label there were three, on
elevation and the LST anomaly, the two predictors that the feature-removal analysis of Section 2.11
removes. Twenty-six further pairs reverse at the point estimate only. None of the fourteen is corrected
for multiplicity (Table S5 gives the corrected counts).

## S3.2 The 10 km collar

This section gives the reversal tests and the transfer detail behind the 10 km collar of
Section 3.4. In Muğla one burned area touches the eastern edge of the study area (15 burned cells on
the edge), where its collars are cut (Fig. 1b). The interval criterion was applied at 10 km, and the
5 and 10 km radii agree at the point estimate. The collar removes many cells in two regions, so part
of any lost support is lost power. On average 2.3 features per direction are supported in both
regions as drawn and 2.2 on the collar. Table S4 compares the three associations that straddle 0.5
on both frames.

**Table S4. Signed univariate AUC as drawn and on the 10 km collar.** Point estimates, signed as in
Table S2. The collar removes no burned cell. As drawn from the source of Table S2, collar from
`code/aoi_frame_auc_frozen_mugla.csv`, with 10-cell intervals in `code/collar_frame_bootstrap.csv`. On
every row Manavgat lies on the other side of 0.5 from the other regions.

| Signed univariate AUC | Manavgat | Bejís | Muğla | Evia | Montiferru | straddles 0.5 |
|---|---:|---:|---:|---:|---:|---|
| elevation, full frame (Table S2) | **0.232** | 0.643 | 0.611 | 0.541 | 0.584 | **yes** |
| elevation, 10 km collar | **0.376** | 0.614 | 0.606 | 0.648 | 0.581 | **yes** |
| current LST, full frame | **0.665** | 0.477 | 0.325 | 0.377 | 0.370 | **yes** |
| current LST, 10 km collar | **0.522** | 0.405 | 0.332 | 0.286 | 0.376 | **yes** |
| current TVDI, full frame | **0.677** | 0.517 | 0.336 | 0.362 | 0.356 | **yes** |
| current TVDI, 10 km collar | **0.527** | 0.454 | 0.342 | 0.250 | 0.361 | **yes** |

Table S5 counts how many of the ninety feature-by-pair comparisons of each frame pass each test. Of
the two collar reversals of Section 3.4, both on elevation, the one against Evia has a Holm
intersection-union adjusted *p* of 0.33 and the one against Muğla 0.79 (normal approximation).

**Table S5. Reversal tests, ninety feature-by-pair comparisons per frame.** Source
`inference/reversal_family_holm.csv` and `inference/reversal_per_region.csv`.

| Criterion | Full frame | 10 km collar |
|---|---:|---:|
| Difference interval excludes zero | 39 | 27 |
| … with opposite-sided point estimates | 31 | 21 |
| Per-comparison criterion (each region's own interval excludes 0.5, opposite sides) | 14 | 2 |
| Holm, normal approximation, difference test | 27 | 12 |
| Holm intersection-union (both regions' tests) | 5 | 0 |

With only the target or only the source restricted to the collar, mean transfer is 0.559 and 0.546
(`round5/collar/aoi_frame_transfer.csv`), while Table 4 gives the matched frames. On these frames
the within-region reference at 5 km blocking is 0.814 as drawn, 0.786 on the 10 km collar and 0.759
on the 5 km collar (`paper/code/verify_matched_gap.py`), so transfer falls short of it by 0.287,
0.197 and 0.169.

Of the twenty similarity measures, only the two built from signed associations were recomputed on
the collar (`round6/diag_collar/`, `round7/r7g_collar_diagnostics.json`). The all-feature cosine of
Section 3.4 is the only similarity measure in the study whose interval excludes zero. Besides being
one of about forty uncorrected tests, it rests on twenty directions that share regions and needs
target labels twice, because the collar is drawn from the burned cells.

After the frozen tables were computed, a quality-screening rebuild overwrote the Manavgat and Muğla
modelling datasets at the pipeline path with new values of `downscaled_lst_mean` and
`fused_lst_mean`. Every analysis of Section 3.4 therefore reads each region through
`paper/code/_canonical.py`, which checks the SHA-256 of the frozen copy, and reads Manavgat from the
corrected re-freeze (`5a5e876c…`).

## S3.3 The temperature sign with terrain held

Table S6 holds one variable at a time in the LST association of Section 3.4. In Manavgat the raw
association is above 0.5 and falls below it once elevation is held, so its positive raw signal comes
from terrain. The detrending there removes a linear effect of elevation of −5.6 K per km. On the
original study area the two held Manavgat values of Section 3.4 have the intervals [0.396, 0.509]
within elevation deciles and [0.387, 0.502] after detrending
(`round8/r8e_stratified_intervals.csv`). In the other four regions the sign stays below 0.5 within
NDVI deciles everywhere and within elevation deciles in three of them. NDVI reverses in two regions
once LST is held, while LST reverses in none once NDVI is held. Holding northness through deciles
leaves the sign unchanged in every region, at 0.652, 0.482, 0.317, 0.376 and 0.417 against 0.665,
0.478, 0.324, 0.377 and 0.370 raw (`round8/r8m_summary.json`, with missing values filled by the
median, so the raw values differ from Table S2 in the third decimal). In Manavgat, cells that burned
in the first four days lie at a median of 219 m, later burns at 512 m and unburned cells at 1,004 m,
so burn timing and elevation are confounded.

**Table S6. The LST association with one variable held, 10 km collar.** Signed AUC against `burned`.
The held columns pool the concordance within deciles of the named variable, each decile weighted by
its burned-unburned pairs, and "detrended" removes the linear dependence of LST on elevation in the
region. Bold marks the values discussed in the text. Sources `code/matched_frame_gap.csv`
(recomputed by `paper/code/verify_matched_gap.py`) and `round7/r7b_lst_given_terrain.csv`, with
intervals for every cell in `round8/r8e_stratified_intervals.csv`.

| Region | LST raw | LST within elevation | LST detrended on elevation | LST within NDVI | LST within distance | NDVI raw | NDVI within LST |
|---|---:|---:|---:|---:|---:|---:|---:|
| Manavgat | 0.522 | **0.403** | **0.409** | 0.556 | 0.454 | 0.551 | 0.550 |
| Bejís | 0.405 | 0.509 | 0.411 | 0.486 | 0.350 | 0.618 | 0.574 |
| Muğla | 0.332 | 0.363 | 0.365 | 0.404 | 0.367 | 0.652 | 0.547 |
| Evia | 0.286 | 0.327 | 0.312 | 0.279 | 0.319 | 0.663 | **0.380** |
| Montiferru | 0.376 | 0.392 | 0.416 | 0.368 | 0.485 | 0.582 | **0.405** |

## S3.4 The contrast pair

Manavgat and Muğla, 306 km apart in one country and one fire year, have the most similar burned-cell
environmental range of any pair, and Bejís and Montiferru the least similar (Fig. 8 and Table S7).
For Manavgat and Muğla as drawn, seven of nine feature-response directions point opposite ways, and
all six features supported in both regions have opposite signs, elevation included. The elevation
reversal remains on the collar (Section 3.4), and transfer is below chance in both directions on
both frames, 0.438 and 0.345 as drawn and 0.493 and 0.433 under the collar, where the interval of
Muğla to Manavgat, [0.381, 0.491], excludes chance. The most similar pair is among the weakest in
the matrix but not the weakest. On the collar the weakest direction is Manavgat to Bejís at 0.407
and the strongest Muğla to Evia at 0.728. Bejís and Montiferru hardly overlap on any measure and
transfer above chance in both directions, though at the point estimate only. On these two pairs high
niche overlap did not ensure transfer and low overlap did not prevent it, and Section S4.5 tests the
correlation across all pairs.

**Table S7. The most and least similar pairs, on both frames.** Schoener's *D* uses burned cells only
and does not change with the collar. Transfer values are the two ordered directions of a pair, and
ranks are out of the twenty directions on the collar. *D* and transfer as drawn from
`round5/out_official/figure_contrast_pairs.json` (the source of Fig. 8), collar transfer and ranks
from `round5/collar/aoi_frame_transfer.csv`, and the AoA shares from
`round5/collar/aoa_directed_pair_summary.csv`. The script `paper/figures/fig8_contrast_pairs.py`
checks every cell.

| | Manavgat and Muğla | Bejís and Montiferru |
|---|---|---|
| Schoener's *D*, mean 1-D | **0.799** (highest) | **0.479** (lowest) |
| per-feature *D* | 0.74 to 0.87 | 0.23 to 0.77 |
| transfer, frames as drawn | 0.438, 0.345 | 0.594, 0.548 |
| transfer, 10 km collar | 0.493, 0.433 | 0.669, 0.624 |
| rank of 20 on the collar, from the bottom | 4th, 2nd | 16th, 12th |
| target cells inside the AoA | 0.876, 0.531 | n/a |

## S3.5 The two Muğla fires

Muğla burned in 2021 and again eleven months later, on the same grid, so this pair holds the place
fixed and changes the fire. The 2022 population is the 2021 population without the 2021 scar (38,790
cells with 331 burned, against 41,730 with 2,911), the two share 38,789 cells, and the 2022 fire
started about six weeks earlier in its season, so year and seasonal phase are confounded. As drawn,
elevation reverses with bootstrap support, from 0.611 [0.532, 0.690] in 2021 to 0.296 [0.230, 0.355]
in 2022, and the four absolute thermal channels cross 0.5 at the point estimate (current LST 0.325
to 0.515) while the two anomaly channels do not (LST anomaly 0.485 to 0.380,
`paper/step9g_raw/step9g_univariate_feature_auc_direction_reversal/mugla_2021__mugla_2022_event_relative/`).
The collar removes the elevation reversal. The 2022 scar is compact, so 93.2 % of the 2022 cells lie
more than 10 km from it, and on the collar the 2022 value moves to 0.565, on the 2021 side of 0.5,
with an interval that includes chance (`code/mugla_two_event_collar.csv`,
`paper/code/verify_mugla_collar.py`). Only elevation and slope can be evaluated on the collar,
because the modelling export of the 2022 fire is not in this repository and the rebuilt 2022 data
differ from it on every seasonal channel.

# S4 Transfer, adaptation and similarity

## S4.1 The transfer matrix

Table S8 gives all twenty directions with and without label-free adaptation, as plotted in Figs. 4
and 5, with intervals at 2-cell blocking. At that blocking eleven directions are above chance with
interval support and seven below (both directions between Manavgat and Bejís, between Manavgat and
Muğla and between Bejís and North Evia, and Montiferru to Manavgat). At the 10-cell blocking of
Section 3.5, Manavgat to Muğla loses its support, and no direction changes side of chance. The
paired thermal contribution goes from twelve positive, seven negative and one uncertain verdict at
1 km to six, five and nine at 5 km, so coarser blocking removed support from eight verdicts and
added none. The three verdicts that change at 5 km across five bootstrap seeds (Section 2.13) are
the level verdict of Evia to Bejís and the paired verdicts of Manavgat to Muğla and Evia to
Montiferru, which makes the counts of supported directions the least stable numbers of the paper
(`round5/out_official/transfer_ci_blocksize.csv`, `round6/seed_stability.json`).

With the better of the two adaptation methods in each direction, 15 directions end closer to chance
and 5 further from it, namely four Montiferru directions that move up and Manavgat to Muğla, which
moves down from 0.438 to 0.427 (`round5/matrix20_official.csv`).

**Table S8. The transfer matrix, thermal model, natural-vegetation population.** Target ROC-AUC with
2-cell spatial-block bootstrap 95 % intervals (1000 replicates). CORAL follows region-wise z-scoring
(λ = 10⁻⁵). Generated by `paper/code/table_b9.py` from `round5/matrix20_official.csv`.

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

## S4.2 The transfer-gap decomposition

Table S9 splits the gap between the within-region skill of the target and raw transfer into the part
that the better label-free method recovers and the rest. Among the directions that started below
chance the recovered fraction is at most +0.28 (Bejís to Evia). The within-region reference is not
matched to a transfer evaluation (Section 3.3), and the raw column depends on the study area
(Section 3.4), so the fractions hold only within this protocol.

**Table S9. Transfer-gap decomposition, four regions, 12 directions.** Within = within-region thermal
AUC of the target. Best adapted = the better of z-score and CORAL, a choice that uses target labels.
Recovered fraction = (adapted − raw)/(within − raw), signed and not clipped, with a paired bootstrap
interval (1000 replicates, 2-cell blocks). Status uses the 2-cell intervals of Table S8. Montiferru is
not part of this decomposition. Source `four_aoi_decomposition.csv` in
`round5/tables/corrected/`.

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

## S4.3 Precision and recall

At target prevalences of 7.0 to 28.7 %, precision and recall can tell a different story from
ROC-AUC, so Table S10 gives the PR-AUC of every direction against its no-skill baseline. The seven
directions below their own baseline are the seven below chance on ROC-AUC, and at 1 km blocking all
seven have intervals below the baseline. The two that keep this at 5 km (Section 3.5) are Bejís to
Manavgat, [0.067, 0.132], and Muğla to Manavgat, [0.071, 0.135], against a baseline of 0.143.

**Table S10. Thermal transfer as PR-AUC against the no-skill baseline.** The baseline is the burned
prevalence of the target, and lift is PR-AUC divided by it, so a lift of 1 is a random ranking.
Ordered by lift. From the step9b exports (`round5/tables/corrected/*/step9b_metrics.json`), with
intervals at 2-cell and 10-cell blocking in `round7/r7a_pr_auc_10cell.csv`.

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

## S4.4 Pooled training

A model trained on the pooled populations of the other four regions (Fig. 6) beats the mean of the
four single-source models for one target of five, Evia, at 0.715 [0.668, 0.757] against a mean
of 0.569, and falls short of this mean for the other four targets by 0.009 to 0.057. It beats the best
single source only for Evia (0.654), and that source can only be chosen with target labels. For every
target the pooled model stays 0.20 to 0.48 AUC below the within-region ceiling, and for Manavgat and
Bejís it is below chance, with interval support only for Manavgat, at 0.426 [0.369, 0.486]
(`code/loro_all.json`, `round7/r7d_pooled_vs_single.csv`).

## S4.5 Similarity measures

Section 2.8 defines the twenty similarity measures and their five families, and Table S11 gives each
one against raw thermal transfer. The pair-cluster bootstrap resamples unordered pairs with
replacement and keeps both directions of each pair. The area-of-applicability dissimilarity is
computed in scaled, importance-weighted predictor space [@Meyer2021; @Meyer2022; @Ludwig2023], and
the conditional family counts sign agreement over all predictors and over those with interval
support. The dated record of the measures (8 August 2026), with their results under the original
label, is commit abd6a4b on the `history-archive` branch of the public repository, and it was not
pre-registered.

The conditional family comes closest to an interval that excludes zero, at +0.52 and +0.49.
Geographic distance does not order the matrix, and the domain classifier separates source from
target at an AUC of at least 0.96 for every pair, so it gives no ordering. Over all 120 permutations
of the five region labels the smallest two-sided *p*-value is 0.10 (vector Spearman, six directions)
and the two supported-feature measures give 0.125 and 0.15, where the smallest attainable value is
1/120 (`round8/r8d_summary.json`). On the twelve directions common to all families, every
interpretable row still includes zero (`round5/out_official/diagnostics_common_subset.json`). The
interval flag behind the instability noted in Section 4.6 is the NDVI of Manavgat, which moved the
supported-feature cosine from ρ = 0.49 to 0.70 when two equally valid bootstrap streams disagreed on
it.

**Table S11. Similarity measures against raw thermal transfer.** Spearman ρ with pair-based bootstrap
95 % intervals. Exp. = expected sign. Rows with n = 12 cover the four regions other than Montiferru,
for which these measures were not produced, and the supported conditional rows use the 18 directions
with at least one supported feature. Source `round5/s6_diagnostics_20.csv`. ‡ The last row belongs to
the set fixed in advance and stays in the table, but it is defined on six directions and its interval
is degenerate (the upper bound equals the point estimate), so it is not interpreted.

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

# S5 Data and methods

## S5.1 Label, grid, gate and the Manavgat correction

This section adds pipeline detail to Sections 2.2 and 2.3. The label is read from the Earth Engine
asset `MODIS/061/MCD64A1` [@Gorelick2017] and copied onto the 30 m EPSG:4326 grid of the pipeline,
and the analysis cells are blocks of `round(500 / 30) = 17 × 17` pixels, identified by `row_500m`
and `col_500m`. The cell is square in degrees, so it approximates the MODIS cell without reproducing
it. Block sizes refer to its north-south edge, and the collar step of 0.45 km per cell lies between
the two edges, which is why collar radii are nominal to within about 15 %. The burn date of a cell
is the modal sub-pixel day of year, and the label never decides whether a cell is modelled. The gate
reads the ESA WorldCover classes of the same cells, and it separates burning of natural fuel from
stubble burning after harvest, which MCD64A1 does not distinguish.

Table S12 counts the earlier burning that Section 2.2 describes, region by region. The only
historical exclusion applied by design removes the 2021 Muğla scar from the 2022 population of
Section S3.5.

**Table S12. Earlier burning by region, natural-vegetation population.** Pre-label burning lies
inside the predictor window and historical burning in the five previous years. Recomputed from the
MCD64A1 export of each region by `paper/code/ems_labels_1_prelabel.py` and `ems_labels_2_history.py`
(`labels/r1_prelabel.json`, `labels/r2_history.json`).

| Region | Pre-label cells removed | Pre-label burned cells retained | Historical-burn cells (five years) | … of which burned again in the event |
|---|---:|---:|---:|---:|
| Manavgat 2021 | none needed (no pre-label burning) | 0 | 0 | 0 |
| Bejís 2022 | exclusion not applied | 48 (49 in all valid cells; 10 burned again) | 163 | 0 |
| Muğla 2021 | 49 | 0 | 194 | 25 |
| North Evia 2021 | 16 | 0 | 366 | 88 |
| Montiferru 2021 | 61 | 0 | 58 | 32 |

The label first used for Manavgat 2021, which missed the first four days of the fire (Section 2.2),
was exported on 8 July 2026, before the month-alignment fix of the MCD64A1 query in the pipeline
(commit 183be42, 11 July), and was not renewed. The code itself was correct. The corrected label
changes no predictor or validity flag. With it the Manavgat rows of Table 2 become stronger, as
absolute AUCs rise by 0.04 to 0.11 and the 1 km interval narrows from [+0.055, +0.079] to [+0.060,
+0.073], because 814 blocks of 2 cells now hold burned cells instead of 235. The outputs were
re-frozen with the pipeline at commit 6381f4c, with the two changes given in Section S5.7. A control
run re-froze the original label with the same code and reproduced the published outputs to within
10⁻⁵, apart from the exceptions listed in the manifest, so differences between the runs come from
the label alone. The correction, the re-freeze and the control run were carried out by the
corresponding author with code written with Claude (see the statement on the use of generative AI in
the main text) and were not repeated by the author of the pipeline. The manifest, hashes and scripts
are in `paper/data/manavgat_2021/refreeze/`.

## S5.2 Study areas and windows

Table S13 gives the bounding box and the windows of each study area, and Section S1.2 gives transfer
on the first, smaller Evia rectangle. The 2022 Muğla windows of Section S3.5 are set relative to the
2022 fire with the 2021 lengths, which gives a 58-day predictor window that ends the day before
ignition and a 49-day label window that opens on it.

**Table S13. Study regions, study areas and time windows.** Bounding boxes in EPSG:4326, as recorded.
Day counts include both ends. The baseline years are the four years before each predictor window,
on the same calendar dates.

| Region | Bounding box (lon min, lat min, lon max, lat max) | Predictor window | Label window | Baseline years |
|---|---|---|---|---|
| Manavgat 2021 (Türkiye) | 31.05, 36.72, 31.85, 37.35 | 2021-06-01 to 2021-07-27 (57 d) | 2021-07-28 to 2021-08-31 (35 d) | 2017, 2018, 2019, 2020 |
| Bejís 2022 (Spain) | -1.05, 39.68, -0.35, 40.15 | 2022-06-15 to 2022-08-14 (61 d) | 2022-08-15 to 2022-09-30 (47 d) | 2018, 2019, 2020, 2021 |
| Muğla 2021 (Türkiye) | 27.1, 36.6, 28.9, 37.45 | 2021-06-01 to 2021-07-28 (58 d) | 2021-07-29 to 2021-09-15 (49 d) | 2017, 2018, 2019, 2020 |
| North Evia 2021 (Greece) | 23.05, 38.55, 23.85, 39.15 | 2021-06-05 to 2021-08-02 (59 d) | 2021-08-03 to 2021-09-30 (59 d) | 2017, 2018, 2019, 2020 |
| Montiferru 2021 (Italy) | 8.45, 40.05, 8.75, 40.27 | 2021-05-25 to 2021-07-23 (60 d) | 2021-07-24 to 2021-08-31 (39 d) | 2017, 2018, 2019, 2020 |

## S5.3 Predictors

Table S14 lists the inputs of the ten predictors of Section 2.4, and this section describes how the
pipeline derives them. The Landsat 8 channels (NDVI, current LST, the LST anomaly and the two TVDI
channels) are screened per pixel with `QA_PIXEL`, and the water bit is kept. Elevation uses the
EGM2008 geoid heights of the Copernicus DEM without datum conversion. The LST anomaly is a z-score
of the current LST median against the four baseline years, set to no-data where the baseline
standard deviation is below 1.0 °C. TVDI [@Sandholt2002] uses wet and dry edges at the 2nd and 98th
LST percentiles within twenty NDVI bins of each study area and window, and the TVDI difference is
its raw anomaly against the same four years. Downscaled LST comes from a MODIS-to-Landsat model that
takes coordinates as inputs, which is the only route by which coordinates enter a feature set
(Fig. S1 gives the gain without it). Fused LST keeps the observed Landsat LST wherever it is valid
and fills the remaining cells from the downscaled surface.

The correlations and principal components of the six thermal channels quoted in Section 2.4 come
from `labels/r4_dimensionality.json`. The anomaly channels rest on one to seven clear Landsat
observations per pixel and year (Table S15), which adds noise to the four-year baseline.

**Table S14. Input data.** All retrieved through Google Earth Engine.

| Input | Product and version | Native resolution | Use | Reference |
|---|---|---|---|---|
| Burned area | MODIS MCD64A1 Collection 6.1 (`MODIS/061/MCD64A1`) | 500 m, monthly | label | [@Giglio2018; @MCD64A1] |
| Surface reflectance and temperature | Landsat 8 Collection 2 Level-2 (`LANDSAT/LC08/C02/T1_L2`), `QA_PIXEL` screening, water bit preserved | 30 m | NDVI, current LST, anomaly, TVDI | [@LandsatC2L2] |
| Coarse LST | MODIS MOD11A1 v061 (`MODIS/061/MOD11A1`) | 1 km, daily | downscaled and fused LST (gap-fill 0.11 % to 9.70 %) | [@MOD11A1] |
| Terrain | Copernicus DEM GLO-30 (EGM2008 heights) | 30 m | elevation, slope | [@CopernicusDEM] |
| Land cover | ESA WorldCover v200 (2021) | 10 m | dominant class, gate, population | [@Zanaga2022] |

**Table S15. Landsat 8 observations per window.** Scenes that intersect the study area, and clear
observations per pixel after the pipeline's QA mask (`src/step3_landsat_lst.py`), median and 10th to
90th percentile at 300 m. The pipeline also filters by calendar month, so its counts can be slightly
lower. Landsat 9 is not used. Source `round8/r8k_landsat_observations.csv`.

| Region | Predictor window scenes | Clear observations, predictor window | Clear observations, baseline years (medians) |
|---|---:|---|---|
| Manavgat 2021 | 14 | 6 [3 to 10] | 7, 7, 6, 6 |
| Bejís 2022 | 16 | 3 [2 to 6] | 4, 4, 3, 2 |
| Muğla 2021 | 18 | 6 [3 to 10] | 6, 6, 6, 6 |
| North Evia 2021 | 8 | 4 [3 to 4] | 4, 3, 2, 1 |
| Montiferru 2021 | 4 | 3 [2 to 4] | 4, 3, 2, 3 |

## S5.4 Resampling units

This section writes out the resampling of Section 2.7. With $`\beta_1, \dots, \beta_M`$ the blocks
of [#eq:block] that contain cells of $`F`$, replicate $`b`$ draws $`M`$ indices $`u_{bm}`$ uniformly
with replacement, which gives

```math {#eq:boot}
F^{*b} = \biguplus_{m=1}^{M} \beta_{u_{bm}}, \qquad \mathrm{CI}_{95} = \left[ Q_{0.025}\{\theta(F^{*b})\}_{b},\; Q_{0.975}\{\theta(F^{*b})\}_{b} \right].
```

Here $`\theta`$ is the statistic and $`Q`$ gives the 2.5 and 97.5 percentiles over 1000 replicates,
seed 42, unless another number is given. A replicate with one class only is dropped. The reliability
of an interval depends on the number of blocks with at least one burned cell, which is 192 to 843
per region at 2 cells, 16 to 70 at 10 cells and 6 to 33 at 20 cells.

Each region appears in eight of the twenty directions, so the *pair-cluster bootstrap* resamples the
ten unordered region pairs, each carrying its set $`\pi_p`$ of ordered directions, and the mean
contribution of a replicate is

```math {#eq:pair}
\bar{\delta}^{*b} = \frac{\sum_{m=1}^{10} \sum_{(s,t) \in \pi_{u_{bm}}} \delta_{st}}{\sum_{m=1}^{10} |\pi_{u_{bm}}|}.
```

Clustering by target region replaces $`\pi_p`$ by the four directions that share a target. A
quantity with one value per held-out scar or target region gets a Student *t* interval over its $`n`$
units, computed as

```math {#eq:tint}
\bar{x} \pm t_{0.975,\,n-1}\, s_x / \sqrt{n}.
```

## S5.5 Gap decomposition and reversal criterion

Section 2.10 defines the recovered fraction and the reversal criterion. The recovered fraction
describes what the two tested methods achieved, with the better one chosen using target labels, and
much of the remaining gap already appears inside one region (Section 3.3), so it is not a
concept-shift residual. Its bootstrap drops replicates with $`|G| < 10^{-6}`$. The reversal
criterion uses the 10-cell interval of each region (Section S3.1), and
`conditional_similarity_transfer.json` stores the rule as metadata.

## S5.6 Label-free adaptation

This section gives the two adaptation methods of Section 2.9 in full. Region-wise z-scoring takes
source statistics from source data and target statistics from target data and never pools them. For
feature $`j`$ in region $`R`$,

```math {#eq:zscore}
z_{ij} = \frac{x_{ij} - \mu_j^{R}}{\sigma_j^{R}}, \qquad \mu_j^{R} = \frac{1}{n_j^{R}} \sum_{i \in O_j^{R}} x_{ij}, \qquad \sigma_j^{R} = \Big( \frac{1}{n_j^{R}} \sum_{i \in O_j^{R}} (x_{ij} - \mu_j^{R})^2 \Big)^{1/2},
```

where $`O_j^{R}`$ contains the $`n_j^{R}`$ cells with an observed value (ddof 0). A missing value is
first set to $`\mu_j^{R}`$, so it becomes zero, and $`\sigma_j^{R} < 10^{-12}`$ is replaced by 1.
Land cover is not transformed. The classifier is refitted on the z-scored source and applied to the
z-scored target, which removes differences in the mean and variance of each feature.

CORAL then aligns the source covariance to the target covariance with the standard whitening and
recolouring map [@Sun2016]. With $`Z_R`$ the $`n_R \times d`$ matrix of z-scored numeric features,
one row per cell,

```math {#eq:coral}
Z_s^{\mathrm{al}} = Z_s\,(C_s + \lambda I)^{-1/2}\,(C_t + \lambda I)^{1/2}, \qquad C_R = \frac{1}{n_R} \sum_{i=1}^{n_R} (z_i - \bar{z}_R)(z_i - \bar{z}_R)^{\top},
```

with $`\lambda = 10^{-5}`$ throughout (ddof 0). Both means are zero after [#eq:zscore], so the mean
terms of the general map are zero, and matrix powers use a symmetric eigendecomposition with
eigenvalues set to at least $`10^{-12}`$. The transform is applied to the source only. The target
stays at $`Z_t`$, and the classifier is refitted on $`Z_s^{\mathrm{al}}`$. A run-time check confirms
that neither method uses a target label, and Section S1.2 gives the effect of other values of λ.

## S5.7 Reproduction, code and data

This section gives the detail behind the reproduction checks of Section 2.13 and the Data and Code
availability statements. The transfer analysis runs in an environment separate from the pipeline, so
the repository refits every within-region model and all twenty CORAL transfers and compares them
with the frozen pipeline output, for Manavgat the output re-frozen at pipeline commit 6381f4c
(Section S5.1). The two changes that this re-freeze needed are a one-line patch that lets the
window-closure module accept a population column added by the corrected label (its diff is released
with the re-freeze) and a runtime setting that points the Earth Engine calls at the project
`thermaltwin`. The transfer agreement of 1.3×10⁻⁸ is below the tolerance of 10⁻⁶. The frame-transfer
script of Section 3.4 fits its forests in parallel, so its values vary between runs by up to 2×10⁻⁶,
within the tolerance of 10⁻⁵ applied to it. Under scikit-learn 1.5.2 instead of 1.9.0, single
directions move by up to 0.023 for the thermal model and 0.047 for the baseline, means by at most
0.003, and one direction changes interval support on each frame
(`round7/sklearn152/compare_vs_1_9_0.json`). The leakage check of Section 2.13 is an assertion in
the code, and the coordinate columns it excludes are `lon`, `lat`, `row`, `col` and their normalised
forms.

The analysis code is under the MIT licence, the version used here has the Zenodo DOI
https://doi.org/10.5281/zenodo.23070876, and the README of the repository describes each folder. The
environment is fixed in `ENVIRONMENT.md`. The five modelling datasets are in
`paper/data/<region>/step8a_500m_modeling_dataset.parquet`, and the pipeline can regenerate the
original-label Manavgat table (`054a1961…`) that its own record still names. The data derived from
the public satellite inputs (Table S14) remain under the terms of their products.