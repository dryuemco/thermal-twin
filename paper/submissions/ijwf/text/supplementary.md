# Supplementary Material

Supplementary material for *Evaluation area and the limits of cross-region transfer of single-season wildfire models in five Mediterranean fires*.

This supplement holds the checks, the per-scar and per-region detail, the full tables, the formal definitions and the derivations that the main text refers to. The figures carry most of these results, and the text adds what they do not show. Sections, tables and figures numbered with S are in this supplement, and those without S are in the main text. Every value is read from a released output of the public repository named in the Data availability statement of the main text, and values computed under the original Manavgat label are marked "original label".

## Contents

- S1 Robustness checks
  - S1.1 The within-region gain
  - S1.2 Cross-region transfer
  - S1.3 Resampling units
  - S1.4 Further checks
- S2 The evaluation frame within a region
  - S2.1 Scar by scar
  - S2.2 Distance from the training cells
  - S2.3 Distance bands
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
  - S4.6 A check against earlier burns
- S5 Data and methods
  - S5.1 Label, grid, gate and the Manavgat correction
  - S5.2 Study areas and windows
  - S5.3 Predictors
  - S5.4 Resampling units
  - S5.5 Gap decomposition and reversal criterion
  - S5.6 Label-free adaptation
  - S5.7 Reproduction, code and data
  - S5.8 Populations and classifier
  - S5.9 Evaluation frames

# S1 Robustness checks

## S1.1 The within-region gain

Fig. S1 sets the within-region thermal gain under each check beside the gain it was compared with.
The only interval that includes zero is that of Montiferru with aspect added, +0.020 [−0.025,
+0.066], against +0.099 without aspect. The main text gives the collar means of the gain without intervals. With
Student *t* intervals over regions they are +0.083 [+0.037, +0.129] on the 10 km collar and +0.087
[+0.037, +0.136] as drawn, and on the 5 km collar the mean halves to +0.042.

![**Fig. S1. The within-region thermal gain under each check, by region.** Thermal minus baseline
ROC-AUC. Open dots are the reference that a check is compared with (italic headings), which is the 5
km-blocked gain, the 1 km-blocked gain of the random forest of the main text or the pipeline's own
window diagnostic. Filled dots are the gain with the check, and lines are 95 % block-bootstrap
intervals where one was computed.](figures/figS1_within_checks.png){width=100%}

Some details are not in the figure. The VNP64A1 and MCD64A1 labels agree at a Jaccard index of 0.865
(Montiferru) to 0.978 (Evia). WorldCover v200 is built from 2021 images, which is after the fire for the four 2021 events, so we repeated all analyses with the 2020 map (WorldCover v100 [@Zanaga2021]). It changed the population by at most 43 burned cells in four regions, but added 142 burned cells in Montiferru, and no conclusion changed. With the 2020 map, the share of burned Montiferru
cells with at least half natural vegetation rises from 0.773 to 0.977 on the modelled cells, whereas
the gate fraction of Table 1 comes from the gate's own inputs. In Bejís, 48 cells burned inside the
predictor window, and ten of these 48 are labelled burned. Removing all 48 cells changes transfer in
the eight Bejís directions by at most 0.015. Rebuilding the Manavgat chain from a quality-screened MODIS input
moved the gain from +0.067 to +0.068 and no signed association by more than 0.005, although the two versions also differ in pipeline code. The secondary population of all valid cells (Section S5.8), which exists only in Manavgat and Bejís, gives gains of +0.048 to +0.061 over
the two regions and three block sizes, every interval above zero, against +0.045 to +0.067 in the primary population.

## S1.2 Cross-region transfer

Fig. S2 repeats the transfer analysis under each check. Mean transfer ranges from 0.481 (penalised
logistic regression) to 0.566 (the twelve directions without Manavgat), against 0.527 as drawn, and
every interval of the thermal gain includes zero. Without Manavgat, mean transfer on the 10 km
collar is 0.631, with no direction below chance. The three simpler estimators of Fig. S2 are a forest of depth 6 with at least 50 cells per leaf, a forest with at least 200 cells per leaf and a penalised logistic regression. They reached 0.527, 0.522 and 0.481, and their thermal contributions to transfer were −0.011, −0.019 and −0.021, all with pair-cluster intervals that include zero.

![**Fig. S2. Mean cross-region transfer under each check.** (a) Mean thermal ROC-AUC over the
twenty directions (twelve without Manavgat). (b) Mean thermal minus baseline ROC-AUC, which for the
three predictor sets is taken against the baseline-only model (0.519). Lines are pair-cluster 95 %
intervals where computed, and thick bars are ranges over ten random-forest seeds. The last three
target frames use no target label and are the cells inside the source's predictor range or area of
applicability [@Meyer2021], or a 20 km square at the centre of each study area.](figures/figS2_transfer_checks.png){width=100%}

The main text compares the two anomaly channels with the four absolute channels in transfer (mean 0.524 against 0.531). Per direction the difference averaged −0.006, was positive in 11 of 20 directions and ranged from −0.099 to +0.087. Within regions the two sets were almost equal (0.862 and 0.864), and both lie between the baseline (0.797) and all ten predictors (0.896). Between the two Muğla fires the anomaly
channels keep their direction and the absolute channels do not (Section S3.5), but
`lst_anomaly_mean` reverses between regions (Table S3), so normalisation protects a channel against
a change of season in one place and fails across places.

The main text gives the mean effect of removing elevation and the LST anomaly together (Fig. 7). The pair-t interval plotted in Fig. 7 is +0.014 [−0.028, +0.056], against +0.014 [−0.018, +0.049] under the primary pair-cluster bootstrap. We also removed each predictor alone, and we did not repeat the selection of the two predictors under the corrected label (Table S3). By
region the within-region change is −0.035, −0.130, −0.073, −0.063 and −0.079 (Manavgat, Bejís,
Muğla, Evia and Montiferru), with every interval below zero. About three
quarters of this cost comes from elevation, because without it alone the mean falls from 0.896 to
0.840, and without the LST anomaly alone to 0.883.

The extended North Evia rectangle kept the burned scar almost unchanged and gave a burned prevalence of 0.287 in the primary population. On the earlier, smaller Evia rectangle, whose burned prevalence is higher, the raw transfers between
Evia and Bejís, Manavgat and Muğla moved by up to 0.134 (Evia to Manavgat, 0.543 against 0.677), and
none changed side of chance.

CORAL hardly depends on its regularisation. Over nine values of λ from 0 to 10⁻¹ on four directions,
transfer moved by at most 0.014, and the Manavgat and
Bejís pair, whose adapted result depended on λ under the original label, stays below chance in both
directions at every λ from 10⁻⁵ to 1. A stronger regularisation (λ = 1, mean 0.512) did not help. The main text reports a placebo that aligns each source with a third region instead of the target (15 of 20 directions moved toward chance, mean 0.507), and CORAL on two thermal principal components gives a mean of 0.523.

## S1.3 Resampling units

Fig. S3 gives the interval of the paired thermal contribution under every resampling unit that can be computed. The directions are not independent, because each region appears in eight of them. On the study areas as drawn, all six resampling units that can be computed gave intervals that include zero, from [−0.006, +0.022] (clustering by target region) to [−0.028, +0.045] (pigeonhole bootstrap). A crossed random-effects model with source and target intercepts gave the widest interval, +0.007 [−0.035, +0.050]. It is a more conservative analysis of the same directions and does not confirm the result independently. On the 10 km collar the two units that exclude zero are the clusters by target region,
[+0.010, +0.040], and by source region, [+0.010, +0.042], but with five regions a percentile
bootstrap over regions has at most 126 distinct resamples, so both are coarse. The two-way cluster
and dyadic-robust estimators give negative variances and are undefined. In an exploratory equivalence test with a margin of ±0.05, the gain was within the margin under all six units that can be computed on the original areas and under four of six on the collar. The margin was set after the results and is close to the smallest within-region gain (+0.045), so the test does not show that the transfer gain is negligible relative to local gains. The 90 % upper bounds as drawn are 0.021 to 0.037, and no unit keeps the gain within a
narrower margin of 0.02. The two units that exceed the margin of 0.05 on the collar are the
pigeonhole bootstrap and the region jackknife (upper bounds 0.052 and 0.055). Leaving out one region
at a time moves the mean contribution between +0.0010 (without Evia) and +0.0148 (without Manavgat),
and its sign never changes. The difference between the within-region and transfer gains (W − T in Table 4) was positive on the original areas and on the 10 km collar, but not on the 5 km collar.

![**Fig. S3. The paired thermal contribution to transfer, by resampling unit.** Mean thermal minus
baseline ROC-AUC over the twenty directions (dot) and its 95 % interval (line), (a) on the study
areas as drawn and (b) on the 10 km collar, with 20,000 replicates where resampled. Blue is the
pair-cluster bootstrap, the primary unit of the main text, whose interval as drawn is [−0.020,
+0.038] at the 1000 replicates used there.](figures/figS3_units.png){width=100%}

## S1.4 Further checks

Table S1 lists the checks that are not plotted. Like those of Figs. S1 to S3, they were run after the
main results, and none was used to choose a reported configuration.

**Table S1. Further checks.** Each row gives one check and its result.

| Check | Result |
|---|---|
| Scar edge | Excluding 0, 1 or 2 edge cells from the scar frame leaves the frame cost (A − B, nine scars) at 0.147 [0.086, 0.208], 0.137 [0.069, 0.205] and 0.129 [0.055, 0.204]; with the region as unit 0.160, 0.150 and 0.145, every interval above zero |
| Placebo collars | The burned cells of a scar scored against the unburned cells of a same-shaped collar placed away from any burned cell reproduce A (A − placebo −0.002 [−0.056, +0.052], eight scars); the real collar costs +0.155 [+0.108, +0.202] more |
| Distant cells | The frame cost does not grow with the share of cells beyond 10 km: region-level slope 0.005 [−0.41, +0.42], r = 0.02 (n = 5); scar-level slope −0.049 [−0.34, +0.24] (n = 9, scars not independent) |
| Other metrics | Region-wide minus scar frame over nine scars: partial AUC (FPR ≤ 0.1) 0.088 [0.048, 0.128]; average precision −0.342 [−0.477, −0.206], higher on the scar frame because its prevalence is higher |
| Ten forest seeds | The seed-to-seed standard deviation of a direction has a median of 0.005 (maximum 0.015), and no direction changes side of chance as drawn; on the 10 km collar one does (Montiferru to Manavgat). Averaging the ten forests gives 0.527 (gain +0.006) as drawn and 0.590 (+0.025) on the collar |
| Capture of burned cells | In transfer, the 10 % of target cells with the highest thermal scores hold 10.3 % of the burned cells on average (0.7 % to 27.1 %), as a random ranking would, and eight of twenty directions fall below that; the top 20 % hold 19.9 %. Within regions (5 km blocking) the top 10 % hold 35.5 % (18.9 % to 44.5 %) and the top 20 % 55.7 % |
| Weather reference | Across the five regions the mean Landsat LST anomaly follows the ERA5-Land air-temperature anomaly of the predictor window (Spearman ρ = 0.8) but not the relative-humidity anomaly (ρ = 0.0), and neither does the TVDI difference (ρ = 0.0); with five regions this is descriptive |
| Missing thermal values | 1.7 %, 6.5 %, 3.2 %, 4.5 % and 0.1 % of the modelled cells (Manavgat, Bejís, Muğla, Evia, Montiferru) lack at least one thermal channel; this flag scores 0.493 to 0.512 against burning |
| Residual spatial correlation | Out-of-fold residuals of cell pairs correlate at 0.58 to 0.83 below 1 km and 0.15 to 0.48 at 5 to 10 km (Montiferru −0.01); the correlation falls below 0.05 at 10 to 20 km in Manavgat, Bejís and Muğla, at 20 to 40 km in Evia and at 5 to 10 km in Montiferru, so 5 km intervals may be too narrow, most of all in Evia |
| Pooled against fold AUC | The mean of the five fold AUCs is 0.004 to 0.018 above the pooled out-of-fold AUC in every region (thermal model, 5 km blocking) |

# S2 The evaluation frame within a region

## S2.1 Scar by scar

Fig. S4 shows the four evaluations of Table 3 for each scar. Manavgat and Bejís have no row C,
because each has one burned area and withholding it would leave nothing to train on. The three
controls reuse the predictions of A and are averaged over 20 draws without replacement. The
prevalence-matched sample draws $`|H_K^{+}|`$ burned and $`|H_K^{-}|`$ unburned region cells, the
negative-pool swap keeps the drawn burned cells and takes the unburned cells of the scar,
$`H_K^{-}`$, and the positive-pool swap does the opposite.

Over nine scars the prevalence-matched sample (A′) scores 0.793 against 0.791 for the whole region,
as ROC-AUC should, so the fall to 0.644 on the scar area (B) is not an effect of prevalence. The pool swaps of the main text place the cost in the unburned cells next
to the fire, which share its terrain, land cover and weather. Row A repeats one region value for
each scar of a region, so the Student *t* intervals of Table 3 for row A, A − B and A − C are too narrow. With the region as the unit, the frame cost was +0.160 [+0.090, +0.230] over five regions and +0.137 [+0.048, +0.226] over the three regions of Table 3, and the fall from A to C was +0.266 [−0.022, +0.553], so only the frame cost is established at the region level. Across regions, the cost showed no relation to the share of distant cells in the study area (Table S1), although this test has little power. Row C
depends little on how a scar is defined. Over a range of minimum sizes and buffers it
ranges from 0.541 to 0.561 on nine to six scars. For a single
scar, row D depends on which region is the source (over the 36 source-scar combinations the mean is 0.556, and ten are below chance).

The test of withholding the scar and of moving the model is weak. In Evia, withholding the scar left only 11 burned cells for training. In Muğla alone, where every held-out case kept a well-trained model, C and D were 0.579 and 0.586. With region-level clustering the intervals widened strongly (for example, the difference in thermal gain between rows C and D widened from [−0.061, +0.094] to [−0.154, +0.186]), so effects of up to about 0.2 cannot be excluded.

Fig. S4b breaks down the thermal gains of the main text by scar. Over the seven scars at 5 km blocking, with Muğla counted four times, they average +0.095 on the whole region, +0.021 on the scar area, +0.024 with the scar withheld and
+0.008 from a foreign region. Scar area minus withheld is −0.004 [−0.070, +0.063] (+0.031 [−0.027,
+0.090] at 1 km), and whole region minus scar area +0.074 [−0.009, +0.157], but with three regions
no reliable region-level interval exists for these differences. Changing the training data therefore moved the gain little once the scored cells had changed, but with effects of up to about 0.2 not excluded, the data do not resolve this. A
half-split of each region gives a gain of +0.028, positive in 13 of 18 splits, although a straight
cut leaves unequal numbers of burned cells in the two halves.

![**Fig. S4. The four evaluations of Table 3, scar by scar.** (a) Thermal ROC-AUC of one region model
scored on the whole region (A) and on the scar area (B), of a model fitted without the scar (C) and
of the models of the other four regions (D, mean of the four). Each grey line is one scar, and the
dark line is the mean, whose value is printed under each design. Manavgat and Bejís have no row C,
and the horizontal line marks chance. (b) Thermal minus baseline ROC-AUC under A, B, C and D for the
seven scars with a row C. Natural-vegetation population, 5 km blocking, 2 km collar.](figures/figS4_scars.png){width=100%}

## S2.2 Distance from the training cells

Fig. S5 draws the distance curve of the main text, in which the distance bins have no intervals, and this section
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
306 to 2,802 km apart.](figures/figS5_distance.png){width=65%}

<!-- IJWF:S2.3 -->
## S2.3 Distance bands

The frame cost can also be read as a gradient. Table S16 scores the out-of-fold predictions of each region model (row A of Table 3) against the unburned cells of one distance band at a time, with all burned cells of the region as positives. The mean AUC over the five regions rises from 0.641 against the unburned cells within 0.5 km of a burned cell to 0.769 at 2 to 5 km and 0.845 beyond 10 km, against 0.814 over all unburned cells. Like the other frame analyses, the bands were computed after the first results and are exploratory.

**Table S16. AUC of the region models by the distance of the unburned cells from the fire.** Thermal model, out-of-fold predictions of 5-fold blocked cross-validation at 5 km blocking. All burned cells of the region are scored against the unburned cells whose distance to the nearest burned cell lies in the band. The last column uses all unburned cells and equals the 10-cell rows of Table 2.

| Region | 0 to 0.5 km | 0.5 to 1 km | 1 to 2 km | 2 to 5 km | 5 to 10 km | beyond 10 km | all |
|---|---:|---:|---:|---:|---:|---:|---:|
| Manavgat | 0.692 | 0.739 | 0.758 | 0.797 | 0.848 | 0.915 | 0.882 |
| Bejís | 0.551 | 0.559 | 0.599 | 0.667 | 0.806 | 0.867 | 0.824 |
| Muğla | 0.656 | 0.670 | 0.686 | 0.744 | 0.763 | 0.798 | 0.777 |
| Evia | 0.744 | 0.771 | 0.782 | 0.890 | 0.888 | 0.864 | 0.864 |
| Montiferru | 0.562 | 0.604 | 0.641 | 0.748 | 0.764 | 0.783 | 0.720 |
| Mean | 0.641 | 0.668 | 0.693 | 0.769 | 0.814 | 0.845 | 0.814 |

<!-- /IJWF:S2.3 -->

# S3 Signed associations and the frame test

## S3.1 Signed associations and reversals

Table S2 gives the signed association of each predictor with burning in each region, and Table S3
the pairs of regions that reverse under the strict, per-comparison criterion of the main text. This criterion is
stricter than disjoint intervals. For `current_lst_mean` the Manavgat and Bejís intervals are
disjoint ([0.608, 0.719] against [0.401, 0.547]), but the Bejís interval includes 0.5, so the pair
reverses at the point estimate only.

**Table S2. Signed univariate AUC of each predictor against `burned`, by region.** Natural-vegetation
population, with a 10-cell (~5 km) spatial-block bootstrap (1000 replicates, seed 42). The AUC is
not folded to max(AUC, 1 − AUC), so a value below 0.5 means that lower values rank burned cells
higher. Bold marks a region whose own interval excludes 0.5.

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
Difference intervals come from a paired 10-cell block bootstrap (1000 replicates), which flags the same fourteen pairs.

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
elevation and the LST anomaly, the two predictors that the feature-removal analysis removes. Twenty-six further pairs reverse at the point estimate only. None of the fourteen is corrected
for multiplicity (Table S5 gives the corrected counts).

## S3.2 The 10 km collar

This section gives the reversal tests and the transfer detail behind the 10 km collar of the main text. The study areas differ in the terrain of their distant cells. In Manavgat, the median elevation of the modelled cells rose from 330 m within 5 km of the fire to 1,273 m at 20 to 50 km, while the burned cells had a median of 287 m. In Muğla one burned area touches the eastern edge of the study area (15 burned cells on
the edge), where its collars are cut (Fig. 1b). The interval criterion was applied at 10 km, and the
5 and 10 km radii agree at the point estimate. The collar removes many cells in two regions, so part
of any lost support is lost power. On average 2.3 features per direction are supported in both
regions as drawn and 2.2 on the collar. Table S4 compares the three associations that straddle 0.5
on both frames.

**Table S4. Signed univariate AUC as drawn and on the 10 km collar.** Point estimates, signed as in
Table S2. The collar removes no burned cell. On every row Manavgat lies on the other side of 0.5 from the other regions, except from Bejís for the current TVDI on the full frame (0.517).

| Signed univariate AUC | Manavgat | Bejís | Muğla | Evia | Montiferru | straddles 0.5 |
|---|---:|---:|---:|---:|---:|---|
| elevation, full frame (Table S2) | **0.232** | 0.643 | 0.611 | 0.541 | 0.584 | **yes** |
| elevation, 10 km collar | **0.376** | 0.614 | 0.606 | 0.648 | 0.581 | **yes** |
| current LST, full frame | **0.665** | 0.477 | 0.325 | 0.377 | 0.370 | **yes** |
| current LST, 10 km collar | **0.522** | 0.405 | 0.332 | 0.286 | 0.376 | **yes** |
| current TVDI, full frame | **0.677** | 0.517 | 0.336 | 0.362 | 0.356 | **yes** |
| current TVDI, 10 km collar | **0.527** | 0.454 | 0.342 | 0.250 | 0.361 | **yes** |

Table S5 counts how many of the ninety feature-by-pair comparisons of each frame pass each test. The two reversals supported on the collar were not the same pairs as on the original areas. Manavgat against Muğla was supported on both frames. Manavgat against Evia became supported on the collar, because the Evia interval excluded 0.5 only there. Manavgat against Bejís lost support narrowly (the Bejís interval, [0.496, 0.722], missed 0.5 by 0.004). Of the two collar reversals, both on elevation, the one against Evia has a Holm
intersection-union adjusted *p* of 0.33 and the one against Muğla 0.79 (normal approximation).

**Table S5. Reversal tests, ninety feature-by-pair comparisons per frame.** Counts of comparisons that pass each criterion.

| Criterion | Full frame | 10 km collar |
|---|---:|---:|
| Difference interval excludes zero | 39 | 27 |
| … with opposite-sided point estimates | 31 | 21 |
| Per-comparison criterion (each region's own interval excludes 0.5, opposite sides) | 14 | 2 |
| Holm, normal approximation, difference test | 27 | 12 |
| Holm intersection-union (both regions' tests) | 5 | 0 |

With only the target or only the source restricted to the collar, mean transfer is 0.559 and 0.546, while Table 4 gives the matched frames. On these frames
the within-region reference at 5 km blocking is 0.814 as drawn, 0.786 on the 10 km collar and 0.759 on the 5 km collar, so transfer falls short of it by 0.287, 0.197 and 0.169. On the 10 km collar the interval of the shortfall is [+0.091, +0.303] (Student *t* over the five targets), and Manavgat had the largest shortfall (+0.319).

Of the twenty similarity measures, only the two built from signed associations were recomputed on the collar. The sign-agreement fraction did not predict transfer on the original areas (ρ = +0.52 [−0.27, +0.87]) or on the collar (ρ = +0.38). Its all-feature cosine predicted collar transfer at ρ = +0.57 [+0.05, +0.88], and it is the only interpreted similarity measure whose interval excludes zero under the corrected label. Besides being one of more than forty uncorrected similarity tests (twenty under each Manavgat label and two on the collar), it rests on twenty directions that share regions and needs
target labels twice, because the collar is drawn from the burned cells.

After the frozen tables were computed, a quality-screening rebuild overwrote the Manavgat and Muğla
modelling datasets at the pipeline path with new values of the downscaled and fused LST. Every collar analysis therefore reads each region from its frozen copy, whose SHA-256 hash is checked on load, and reads Manavgat from the corrected re-freeze.

## S3.3 The temperature sign with terrain held

Table S6 holds one variable at a time in the LST association of the main text. In Manavgat the raw
association is above 0.5 and falls below it once elevation is held, so its positive raw signal comes
from terrain. The detrending there removes a linear effect of elevation of −5.6 K per km, and the detrended value on the collar is 0.409 [0.350, 0.475]. On the original study area the two held Manavgat values are 0.455 and 0.446, with the intervals [0.396, 0.509] within elevation deciles and [0.387, 0.502] after detrending, which include 0.5. In the other four regions the sign stays below 0.5 within
NDVI deciles everywhere and within elevation deciles in three of them. NDVI reverses in two regions
once LST is held, while LST reverses in none once NDVI is held. Holding northness through deciles
leaves the sign unchanged in every region, at 0.652, 0.482, 0.317, 0.376 and 0.417 against 0.665,
0.478, 0.324, 0.377 and 0.370 raw (with missing values filled by the
median, so the raw values differ from Table S2 in the third decimal). In Manavgat, cells that burned
in the first four days lie at a median of 219 m, later burns at 512 m and unburned cells at 1,004 m,
so burn timing and elevation are confounded.

**Table S6. The LST association with one variable held, 10 km collar.** Signed AUC against `burned`.
The held columns pool the concordance within deciles of the named variable, each decile weighted by
its burned-unburned pairs, and "detrended" removes the linear dependence of LST on elevation in the
region. Bold marks the values discussed in the text.

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
reversal remains on the collar, and transfer is below chance in both directions on
both frames, 0.438 and 0.345 as drawn and 0.493 and 0.433 under the collar, where the interval of
Muğla to Manavgat, [0.381, 0.491], excludes chance. The most similar pair is among the weakest in
the matrix but not the weakest. On the collar the weakest direction is Manavgat to Bejís at 0.407
and the strongest Muğla to Evia at 0.728. Bejís and Montiferru hardly overlap on any measure and
transfer above chance in both directions, though at the point estimate only. On these two pairs high
niche overlap did not ensure transfer and low overlap did not prevent it, and Section S4.5 tests the
correlation across all pairs.

**Table S7. The most and least similar pairs, on both frames.** Schoener's *D* uses burned cells only
and does not change with the collar. Transfer values are the two ordered directions of a pair, and
ranks are out of the twenty directions on the collar. AoA is the area of applicability of the source.

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
fixed and changes the fire. The 2022 population has 38,790 cells with 331 burned, against 41,730 with 2,911 burned in 2021. It is the 2021 population without the 2021 scar, apart from small differences between the masks of the two exports (the 2021 population has 38,819 unburned cells). The two populations share 38,789 cells, and the 2022 fire started about six weeks earlier in its season, so year and seasonal phase are confounded. As drawn,
elevation reverses with bootstrap support, from 0.611 [0.532, 0.690] in 2021 to 0.296 [0.230, 0.355]
in 2022, and the four absolute thermal channels cross 0.5 at the point estimate (current LST 0.325
to 0.515) while the two anomaly channels do not (LST anomaly 0.485 to 0.380).
The collar removes the elevation reversal. The 2022 scar is compact, so 93.2 % of the 2022 cells lie
more than 10 km from it, and on the collar the 2022 value moves to 0.565, on the 2021 side of 0.5,
with an interval that includes chance. Only elevation and slope can be evaluated on the collar,
because the modelling export of the 2022 fire is not in this repository and the rebuilt 2022 data
differ from it on every seasonal channel.

# S4 Transfer, adaptation and similarity

## S4.1 The transfer matrix

Table S8 gives all twenty directions with and without label-free adaptation, as plotted in Figs. 4
and 5, with intervals at 2-cell blocking. At that blocking eleven directions are above chance with
interval support and seven below (both directions between Manavgat and Bejís, between Manavgat and
Muğla and between Bejís and North Evia, and Montiferru to Manavgat). At the 10-cell blocking of the main text, where the intervals are wider, Manavgat to Muğla loses its support, and no direction changes side of chance. The
paired thermal contribution goes from twelve positive, seven negative and one uncertain verdict at
1 km to six, five and nine at 5 km, so coarser blocking removed support from eight verdicts and
added none. Across five bootstrap seeds, every transfer verdict at 1 km blocking is stable, whereas at 5 km three verdicts change. They are the level verdict of Evia to Bejís and the paired verdicts of Manavgat to Muğla and Evia to
Montiferru, which makes the counts of supported directions the least stable numbers of the paper.

Under region-wise z-scoring the twenty directions ranged from 0.302 to 0.630, and under CORAL from 0.406 to 0.624. Choosing the better method in each direction gave a mean of 0.523, but this choice uses target labels. With the better of the two adaptation methods in each direction, 15 directions end closer to chance
and 5 further from it, namely four Montiferru directions that move up and Manavgat to Muğla, which
moves down from 0.438 to 0.427.

**Table S8. The transfer matrix, thermal model, natural-vegetation population.** Target ROC-AUC with
2-cell spatial-block bootstrap 95 % intervals (1000 replicates). CORAL follows region-wise z-scoring
(λ = 10⁻⁵).

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
that the better label-free method recovers and the rest. The decomposition was computed before Montiferru was added and covers the twelve directions among the other four regions (Section S5.5 gives its definition). Seven directions showed negative recovery, five of them with intervals below zero. Among the directions that started below chance the recovered fraction is at most +0.28 (Bejís to Evia). The within-region reference is not matched to a transfer evaluation, and the raw column depends on the study area, so the fractions hold only within this protocol.

**Table S9. Transfer-gap decomposition, four regions, 12 directions.** Within = within-region thermal AUC of the target at 1 km blocking. Best adapted = the better of z-score and CORAL, a choice that uses target labels.
Recovered fraction = (adapted − raw)/(within − raw), signed and not clipped, with a paired bootstrap
interval (1000 replicates, 2-cell blocks). Status uses the 2-cell intervals of Table S8. Montiferru is not part of this decomposition.

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

Precision-recall AUC (PR-AUC) reflects how a susceptibility map is used when burned cells are rare [@Sofaer2019]. At target prevalences of 7.0 to 28.7 %, precision and recall can tell a different story from ROC-AUC, so Table S10 gives the PR-AUC of every direction against its no-skill baseline, which is the burned prevalence of the target (0.070 to 0.287). PR-AUC averaged 0.181, against a mean no-skill baseline of 0.157, and the median lift over the baseline was 1.18. The seven
directions below their own baseline are the seven below chance on ROC-AUC, and at 1 km blocking all
seven have intervals below the baseline. The two that keep this at 5 km, both into Manavgat, are Bejís to Manavgat, [0.067, 0.132], and Muğla to Manavgat, [0.071, 0.135], against a baseline of 0.143.

**Table S10. Thermal transfer as PR-AUC against the no-skill baseline.** The baseline is the burned
prevalence of the target, and lift is PR-AUC divided by it, so a lift of 1 is a random ranking.
Ordered by lift.

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
target the pooled model stays 0.20 to 0.48 AUC below the within-region ceiling at 1 km blocking, and for Manavgat and
Bejís it is below chance, with interval support only for Manavgat, at 0.426 [0.369, 0.486].

## S4.5 Similarity measures

The twenty similarity measures fall into five families, and Table S11 gives each one against raw thermal transfer. The marginal family compares the predictor distributions. Its measures are dissimilarity in predictor space and the share of target cells inside the source's area of applicability [@Meyer2021], climatic distance, and the accuracy of a domain classifier that separates source from target cells. The other families are geographic distance, niche overlap of the burned cells (Schoener's *D* and Warren's *I* [@Schoener1968; @Warren2008]), the burned-patch regime, and the agreement of the signed associations between the two regions. We rank-correlated each measure with the raw thermal transfer AUC over the directions on which it is defined (Spearman's ρ), with one pair-cluster bootstrap for all measures (2000 replicates, seed 42) and a permutation test over the 120 orderings of the five regions. Only the marginal measures and geographic distance can be computed before a fire. The pair-cluster bootstrap resamples unordered pairs with
replacement and keeps both directions of each pair. The area-of-applicability dissimilarity is
computed in scaled, importance-weighted predictor space [@Meyer2021; @Meyer2022; @Ludwig2023], and
the conditional family counts sign agreement over all predictors and over those with interval
support. The dated record of the measures (8 August 2026), with their results under the original
label, is commit abd6a4b on the `history-archive` branch of the public repository, and it was not pre-registered. Under the original label, the agreement fraction and the cosine over supported features gave ρ = +0.84 [+0.58, +0.88] and +0.81 [+0.33, +0.88] on 16 directions.

The conditional family comes closest to an interval that excludes zero, at +0.52 and +0.49.
Geographic distance does not order the matrix, and the domain classifier separates source from
target at an AUC of at least 0.96 for every pair, so it gives no ordering. Over all 120 permutations
of the five region labels the smallest two-sided *p*-value is 0.10 (vector Spearman, six directions)
and the two supported-feature measures give 0.125 and 0.15, where the smallest attainable value is 1/120. Directions on which a measure is undefined are dropped before permuting, so a row with fewer than twenty directions is tested on the directions it has. On the twelve directions common to all families, every interpretable row still includes zero. The measures based on interval support are unstable, because five to six interval bounds lie within 0.01 of 0.5 and one changed flag moved a correlation by about 0.2. The flag behind this instability is the NDVI of Manavgat, which moved the
supported-feature cosine from ρ = 0.49 to 0.70 when two equally valid bootstrap streams disagreed on
it.

**Table S11. Similarity measures against raw thermal transfer.** Spearman ρ with pair-based bootstrap
95 % intervals. Exp. = expected sign. Rows with n = 12 cover the four regions other than Montiferru,
for which these measures were not produced, and the supported conditional rows use the 18 directions
with at least one supported feature. ‡ The last row belongs to
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

<!-- IJWF:S4.6 -->
## S4.6 A check against earlier burns

The main text recommends that a transferred model is tested in the target region. A burned-area record of earlier years is the only local label that exists before a fire season, so we tried it as such a test. This analysis was added after all other results and is exploratory. For each target, the cells that MCD64A1 marks as burned in the five calendar years before the event year (Table S12) were taken as the earlier burns. Manavgat has none, which leaves 16 directions into four targets, with 58 to 366 earlier-burn cells per target. Each transferred thermal model scored the target cells once, and the scores were compared with the earlier burns (the check) and with the event (the outcome). The models were refitted for this analysis and reproduce the raw column of Table S8 to within 0.0015 in all twenty directions.

The check did not predict the outcome (Table S17). Against the earlier burns the 16 transfers averaged an AUC of 0.454, below chance, against 0.550 for the event. Over the 16 directions the two AUCs were not positively related (Spearman ρ = −0.39 [−0.77, +0.15], pair-cluster bootstrap with 2000 replicates), and they fell on the same side of chance in 5 of 16 directions. When the earlier burns that burned again in the event were left out, ρ was −0.28 [−0.76, +0.24]. For every target the check ranked the Manavgat model first. That source was the best of the four for one target (Evia) and the worst for the other three, and on average the source picked by the check scored 0.048 below the mean of the four sources. A likely reason is that land burned in the previous five years carries less fuel than its surroundings and appears to the predictors as a recent scar, so a short record of this kind tests a different question from the one a new large fire poses. A longer record was not available here and was not tested.

**Table S17. Transferred models scored against earlier burns and against the event.** Thermal model, natural-vegetation population, no target label used in fitting. Earlier burns are the cells burned in the five calendar years before the event year.

| Direction | Earlier-burn cells | Of which burned in the event | AUC against earlier burns | AUC against the event |
|---|---:|---:|---:|---:|
| Manavgat→Bejís | 163 | 0 | 0.742 | 0.396 |
| Muğla→Bejís | 163 | 0 | 0.352 | 0.583 |
| Evia→Bejís | 163 | 0 | 0.481 | 0.448 |
| Montiferru→Bejís | 163 | 0 | 0.348 | 0.548 |
| Manavgat→Muğla | 194 | 25 | 0.723 | 0.438 |
| Bejís→Muğla | 194 | 25 | 0.306 | 0.618 |
| Evia→Muğla | 194 | 25 | 0.532 | 0.577 |
| Montiferru→Muğla | 194 | 25 | 0.416 | 0.619 |
| Manavgat→Evia | 366 | 88 | 0.596 | 0.654 |
| Bejís→Evia | 366 | 88 | 0.399 | 0.383 |
| Muğla→Evia | 366 | 88 | 0.383 | 0.653 |
| Montiferru→Evia | 366 | 88 | 0.473 | 0.586 |
| Manavgat→Montiferru | 58 | 32 | 0.759 | 0.518 |
| Bejís→Montiferru | 58 | 32 | 0.227 | 0.594 |
| Muğla→Montiferru | 58 | 32 | 0.282 | 0.531 |
| Evia→Montiferru | 58 | 32 | 0.249 | 0.647 |
| Mean | | | 0.454 | 0.550 |

<!-- /IJWF:S4.6 -->

# S5 Data and methods

## S5.1 Label, grid, gate and the Manavgat correction

This section adds pipeline detail on the label, the analysis grid and the gate. We sampled the MCD64A1 monthly burn-date layer (Earth Engine asset `MODIS/061/MCD64A1` [@Gorelick2017]) onto the 30 m EPSG:4326 reference grid of the processing pipeline by nearest neighbour, so each ~500 m observation is repeated over the 30 m pixels below it, and built the analysis grid from this grid in blocks of 17 × 17 pixels. A cell is therefore about 510 m from north to south and 390 to 407 m from east to west, with an area of 0.199 to 0.208 km² (a MODIS cell is 0.215 km²). The population filter of Section S5.8 removes water cells. The cell is square in degrees, so it approximates the MODIS cell without reproducing
it. Block sizes refer to its north-south edge, and the collar step of 0.45 km per cell lies between
the two edges, which is why collar radii are nominal to within about 15 %. The burn date of a cell
is the modal sub-pixel day of year, and the label never decides whether a cell is modelled. The gate
reads the ESA WorldCover classes of the same cells, and it separates burning of natural fuel from
stubble burning after harvest, which MCD64A1 does not distinguish. We admitted a region if the fraction of burned cells covered mainly by natural vegetation was at least 0.50 and at least 30 cells burned, and we rejected it as a cropland control if the cropland fraction was at least 0.50. The five admitted regions had fractions of 0.723 to 0.991. The negative control, Kozan 2023, had a natural-vegetation fraction of 0.017 and was excluded. The gate therefore separated the cases clearly, although one negative control cannot show that it always works.

Table S12 counts earlier burning region by region. We removed cells that burned in the predictor window in Muğla (49 cells), North Evia (16) and Montiferru (61), while Manavgat had no burning in that window. Reports place the start of the Montiferru fire in the late afternoon of 23 July [@Almeida2023] or on 24 July. Landsat 8 and Terra pass over in the morning, so no predictor observation shows the fire, and any cell that MCD64A1 dates to 23 July is among the 61 removed. In Bejís this removal was not applied, so 48 cells that burned before the label window were kept. We did not screen burning in the five previous years in any region. When we excluded those cells, the mean transfer gain fell from +0.007 to +0.003, while the within-region gain stayed positive in all regions (Figs. S1 and S2). The only
historical exclusion applied by design removes the 2021 Muğla scar from the 2022 population of
Section S3.5.

**Table S12. Earlier burning by region, natural-vegetation population.** Pre-label burning lies
inside the predictor window and historical burning in the five previous years. Recomputed from the MCD64A1 export of each region.

| Region | Pre-label cells removed | Pre-label burned cells retained | Historical-burn cells (five years) | … of which burned again in the event |
|---|---:|---:|---:|---:|
| Manavgat 2021 | none needed (no pre-label burning) | 0 | 0 | 0 |
| Bejís 2022 | exclusion not applied | 48 (49 in all valid cells; 10 burned again) | 163 | 0 |
| Muğla 2021 | 49 | 0 | 194 | 25 |
| North Evia 2021 | 16 | 0 | 366 | 88 |
| Montiferru 2021 | 61 | 0 | 58 | 32 |

The label first used for Manavgat 2021, which missed the first four days of the fire, was exported on 8 July 2026, before the month-alignment fix of the MCD64A1 query in the pipeline
(commit 183be42, 11 July), and was not renewed. The code itself was correct. The corrected label
changes no predictor or validity flag. With it the Manavgat rows of Table 2 become stronger, as
absolute AUCs rise by 0.04 to 0.11 and the 1 km interval narrows from [+0.055, +0.079] to [+0.060,
+0.073], because 814 blocks of 2 cells now hold burned cells instead of 235. The outputs were
re-frozen with the pipeline at commit 6381f4c, with the two changes given in Section S5.7. A control
run re-froze the original label with the same code and reproduced the published outputs to within
10⁻⁵, apart from the exceptions listed in the manifest, so differences between the runs come from
the label alone. The correction, the re-freeze and the control run were carried out by the
corresponding author with code written with Claude (see the statement on the use of generative AI in
the main text) and were not repeated by the author of the pipeline. The manifest, hashes and scripts are released with the analysis code.

## S5.2 Study areas and windows

Table S13 gives the bounding box and the windows of each study area, and Section S1.2 gives transfer on the first, smaller Evia rectangle. Predictor windows were 57 to 61 days long and label windows 35 to 59 days. The Manavgat fire burned 58,798 ha, 64 % of it in pure Turkish pine (*Pinus brutia*) stands. The Muğla study area contains all or part of several fires of the same weeks, among them those near Milas (17,164 ha), Marmaris (12,158 ha) and Köyceğiz–Dalaman (11,074 ha), each burning mainly Turkish pine [@Eker2024]. The North Evia fire burned 51,245 ha of pine and oak forest and of rural and urban land [@Almeida2023]. The Bejís fire burned 18,058 ha of Aleppo pine (*Pinus halepensis*) forest, holm oak (*Quercus ilex*) woodland and shrubland [@FernandezGuisuraga2023]. The Montiferru fire burned about 13,200 ha, mostly herbaceous vegetation (39.5 %) and low shrubs (24.2 %), while holm oak woodland is the main forest type there [@Almeida2023]. The 2022 Muğla windows of Section S3.5 are set relative to the
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

Table S14 lists the inputs of the ten predictors, and this section describes how the
pipeline derives them. The Landsat 8 channels (NDVI, current LST, the LST anomaly and the two TVDI
channels) are screened per pixel with `QA_PIXEL`, and the water bit is kept. Elevation uses the
EGM2008 geoid heights of the Copernicus DEM without datum conversion. The LST anomaly is a z-score
of the current LST median against the four baseline years, set to no-data where the baseline
standard deviation is below 1.0 °C. TVDI [@Sandholt2002] uses wet and dry edges at the 2nd and 98th
LST percentiles within twenty NDVI bins of each study area and window, and the TVDI difference is
its raw anomaly against the same four years. Downscaled LST comes from a MODIS-to-Landsat model that
takes coordinates as inputs, which is the only route by which coordinates enter a feature set
(Fig. S1 gives the gain without it). Fused LST keeps the observed Landsat LST wherever it is valid
and fills the remaining cells from the downscaled surface. Both use MODIS MOD11A1 v061 daytime LST (Terra, about 10:30 local time) [@MOD11A1] and a random-forest downscaling model to fill gaps in Landsat (0.11 % to 9.70 % of pixels, depending on the region).

The six thermal channels carry about two signals. Current, fused and downscaled LST are correlated at 0.97 to 1.00 in every region, current LST and TVDI at 0.88 to 0.98, and the two anomaly channels at 0.71 to 0.94. Two principal components explain 92 % to 98 % of their variance, so we read counts over the nine numeric predictors with care. The median pixel had three to six clear Landsat observations in the predictor window, and one to seven in each baseline year (Table S15), which adds noise to the four-year baseline.

To test whether normalised channels transfer better, the baseline was also fitted with only the two anomaly channels, which are normalised against each region's own baseline years, and with only the four channels of absolute surface state (Section S1.2). These four are current LST, current TVDI, downscaled LST and fused LST. The current TVDI is normalised within each scene but not against the baseline, so it belongs to the second set. As a descriptive weather reference, we compared the regional mean LST anomaly and TVDI difference with the ERA5-Land [@MunozSabater2021] anomalies of air temperature and relative humidity in the predictor window (Table S1).

**Table S14. Input data.** All retrieved through Google Earth Engine.

| Input | Product and version | Native resolution | Use | Reference |
|---|---|---|---|---|
| Burned area | MODIS MCD64A1 Collection 6.1 (`MODIS/061/MCD64A1`) | 500 m, monthly | label | [@Giglio2018; @MCD64A1] |
| Surface reflectance and temperature | Landsat 8 Collection 2 Level-2 (`LANDSAT/LC08/C02/T1_L2`), `QA_PIXEL` screening, water bit preserved | 30 m | NDVI, current LST, anomaly, TVDI | [@LandsatC2L2] |
| Coarse LST | MODIS MOD11A1 v061 (`MODIS/061/MOD11A1`) | 1 km, daily | downscaled and fused LST (gap-fill 0.11 % to 9.70 %) | [@MOD11A1] |
| Terrain | Copernicus DEM GLO-30 (EGM2008 heights) | 30 m | elevation, slope | [@CopernicusDEM] |
| Land cover | ESA WorldCover v200 (2021) | 10 m | dominant class, gate, population | [@Zanaga2022] |

**Table S15. Landsat 8 observations per window.** Scenes that intersect the study area, and clear
observations per pixel after the pipeline's QA mask, median and 10th to
90th percentile at 300 m. The pipeline also filters by calendar month, so its counts can be slightly
lower. Landsat 9 is not used.

| Region | Predictor window scenes | Clear observations, predictor window | Clear observations, baseline years (medians) |
|---|---:|---|---|
| Manavgat 2021 | 14 | 6 [3 to 10] | 7, 7, 6, 6 |
| Bejís 2022 | 16 | 3 [2 to 6] | 4, 4, 3, 2 |
| Muğla 2021 | 18 | 6 [3 to 10] | 6, 6, 6, 6 |
| North Evia 2021 | 8 | 4 [3 to 4] | 4, 3, 2, 1 |
| Montiferru 2021 | 4 | 3 [2 to 4] | 4, 3, 2, 3 |

## S5.4 Resampling units

This section writes out the blocking, the metric and the resampling. Cell $`i`$ at grid position $`(r_i, c_i)`$ is assigned to the block

```math {#eq:block}
b_k(i) = \left( \lfloor r_i / k \rfloor,\; \lfloor c_i / k \rfloor \right).
```

Five folds are drawn over whole blocks, stratified by label, with block sizes of $`k`$ = 2, 10 and 20 cells. Every score is a ROC-AUC on a named set of cells $`F`$, its evaluation frame. With $`F^{+}`$ the burned and $`F^{-}`$ the unburned cells of $`F`$, and $`s_i`$ the predicted score,

```math {#eq:auc}
\mathrm{AUC}(s; F) = \frac{1}{|F^{+}|\,|F^{-}|} \sum_{i \in F^{+}} \sum_{j \in F^{-}} \left[ \mathbf{1}(s_i > s_j) + \tfrac{1}{2}\,\mathbf{1}(s_i = s_j) \right].
```

The out-of-fold residuals stay spatially correlated beyond 5 km, in North Evia up to 20 to 40 km (Table S1), so intervals at 5 km blocking may be too narrow, and we give the 10 km results as a check. With $`\beta_1, \dots, \beta_M`$ the blocks
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

Clustering by target region replaces $`\pi_p`$ by the four directions that share a target. The pair-cluster bootstrap is the primary resampling unit for direction-level intervals, differences are paired within each replicate, and the block size is given with every result. The five further units compared in Section S1.3 are the naive bootstrap over directions, clustering by target region and by source region, a pigeonhole bootstrap that resamples sources and targets independently, and a leave-one-region-out jackknife. The effective sample is therefore ten pairs or five regions for direction-level intervals, and at most seven scars from three regions for scar-level intervals. A change with one value per region pair gets a *pair-t* interval, a Student *t* interval over the ten pairs. A quantity with one value per held-out scar or target region gets a Student *t* interval over its $`n`$
units, computed as

```math {#eq:tint}
\bar{x} \pm t_{0.975,\,n-1}\, s_x / \sqrt{n}.
```

## S5.5 Gap decomposition and reversal criterion

For a direction into a target, let $`A_{\mathrm{w}}`$ be the within-region thermal AUC of the target, $`A_{\mathrm{raw}}`$ the raw transfer AUC and $`A_{\mathrm{ad}}`$ the transfer AUC after adaptation method $`m`$, all on the same target cells. We split the gap as

```math {#eq:decomp}
G = A_{\mathrm{w}} - A_{\mathrm{raw}}, \qquad R_m = A_{\mathrm{ad}} - A_{\mathrm{raw}}, \qquad U_m = A_{\mathrm{w}} - A_{\mathrm{ad}}, \qquad f_m = R_m / G,
```

so that $`R_m + U_m = G`$. The recovered fraction $`f_m`$ is signed and is not clipped, so when adaptation lowers AUC, the recovery is negative and we report it as negative. Intervals come from the paired bootstrap of Section S5.4. The recovered fraction describes what the two tested methods achieved, with the better one chosen using target labels, and much of the remaining gap already appears inside one region, so it is not a concept-shift residual. Its bootstrap drops replicates with $`|G| < 10^{-6}`$. The reversal criterion of the main text uses the 10-cell interval of each region (Section S3.1). A marginal reversal can also arise when the predictors are distributed differently in two regions, so it is not a direct test of a change in the predictor-burning relationship.

## S5.6 Label-free adaptation

This section gives the two label-free adaptation methods in full. Region-wise z-scoring takes
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
stays at $`Z_t`$, and the classifier is refitted on $`Z_s^{\mathrm{al}}`$. We did not choose λ by performance. A run-time check confirms that neither method uses a target label, and Section S1.2 gives the effect of other values of λ.

## S5.7 Reproduction, code and data

This section gives the detail behind the leakage control, the reproduction checks and the Data availability statement. We checked a list of forbidden columns at every model fit (coordinates, all burn-date and label-provenance columns, and the agreement fraction). The vegetation mask defines the population and is never used as a predictor. All randomness uses seed 42. Because the random-forest seed is fixed, direction-level intervals are conditional on one fitted source model. Refitting with ten seeds changed mean transfer by at most 0.003, but single directions by up to 0.049 (seed-to-seed standard deviation at most 0.015, Table S1), and this variation is not part of the direction-level intervals. Refitting every within-region model and all twenty CORAL transfers reproduced the frozen pipeline outputs exactly within regions and to within 1.3×10⁻⁸ in transfer. The transfer analysis runs in an environment separate from the pipeline, so
the repository refits every within-region model and all twenty CORAL transfers and compares them
with the frozen pipeline output, for Manavgat the output re-frozen at pipeline commit 6381f4c
(Section S5.1). The two changes that this re-freeze needed are a one-line patch that lets the
window-closure module accept a population column added by the corrected label (its diff is released
with the re-freeze) and a runtime setting that points the Earth Engine calls at the authors' own project. The transfer agreement of 1.3×10⁻⁸ is below the tolerance of 10⁻⁶. The collar transfer analysis fits its forests in parallel, so its values vary between runs by up to 2×10⁻⁶,
within the tolerance of 10⁻⁵ applied to it. Under scikit-learn 1.5.2 instead of 1.9.0, single
directions move by up to 0.023 for the thermal model and 0.047 for the baseline, means by at most
0.003, and one direction changes interval support on each frame, so exact reproduction needs the archived environment. The leakage check is an assertion in the code, and the coordinate columns it excludes are longitude, latitude, row, column and their normalised forms.

The analysis code is under the MIT licence, the version used here has the Zenodo DOI
https://doi.org/10.5281/zenodo.23070876, and the repository describes each folder, the fixed environment and the five modelling datasets. The pipeline can regenerate the original-label Manavgat table that its own record still names. The data derived from
the public satellite inputs (Table S14) remain under the terms of their products.

## S5.8 Populations and classifier

Cell values are means over the valid 30 m pixels of the cell. A cell is valid for modelling when NDVI, elevation and slope are available for at least 30 % of the cell and at least one land-cover pixel is valid, but thermal completeness is not required. The primary population contains the valid cells in which tree, shrub and grass cover together reach 0.50, so cropland and water are excluded. In this population, 0.1 % to 6.5 % of cells have at least one missing thermal value, depending on the region. We filled these values inside the model pipeline, and missingness was not related to burning (AUC 0.49 to 0.51 in every region, Table S1). We used a secondary population of all valid cells only as a within-region sensitivity analysis in two regions (Section S1.1).

We one-hot encoded land cover and replaced missing numeric values by the median and missing land cover by the most frequent class. We fitted these values inside each training fold, and on the source region only in transfer, so no test data were used in fitting (the adapted models of Section S5.6 are the only exception). The random forest [@Breiman2001] has 300 trees, unlimited depth, `min_samples_leaf = 3`, balanced class weights and `random_state = 42`.

## S5.9 Evaluation frames

This section gives the formal definitions of the evaluation frames. Let $`V_R`$ be the primary population of region $`R`$ and $`P_R \subset V_R`$ its burned cells. The region-wide frame is $`V_R`$, the rectangle as drawn. A scar is an 8-connected group $`K`$ of at least 50 burned cells. Its scar frame is

```math {#eq:scar}
H_K = \Big\{ i \in V_R : \min_{j \in K} \big( |r_i - r_j| + |c_i - c_j| \big) \le m \Big\},
```

with $`m = 4`$ grid steps. On this grid the collar is therefore about 1.6 to 2.0 km wide along the axes and about 1.3 km along the diagonals, and all its unburned cells are next to the fire. Of the four evaluations of Table 3, A scores the out-of-fold predictions of 5-fold blocked cross-validation ($`k = 10`$) on $`V_R`$, and B scores the same predictions on $`H_K`$. C is leave-one-scar-out, in which a model fitted on $`V_R \setminus H_K`$ is scored on $`H_K`$. D averages, over the four other regions, a model fitted on that region and scored on $`H_K`$. Three controls reuse the predictions of A, namely a prevalence-matched sample, a negative-pool swap and a positive-pool swap (Section S2.1). Two further controls address the label errors at scar edges. The first excludes up to two cells at the scar edge, and the second is a placebo collar of the same shape placed away from any burned cell (Table S1).

The distance to the nearest burned cell and the collar of radius $`r`$ (5 or 10 km) are

```math {#eq:collar}
d_i = 0.45 \min_{j \in P_R} \big\lVert (r_i, c_i) - (r_j, c_j) \big\rVert_2, \qquad F_R(r) = \{ i \in V_R : d_i \le r \}.
```

The 0.45 km step is a single value for both axes (Section S5.1). Every burned cell has $`d_i = 0`$ and is kept, so only distant unburned cells are removed. In transfer, we fitted the model on $`F_s(r_s)`$ and scored it on $`F_t(r_t)`$. To see how skill falls with distance inside one region, we fitted a model on one half of a region and scored the cells of the other half, grouped by their distance from the training cells (Section S2.2).
