# Results

We first report the thermal gain within regions, which is the reference for what follows, and then answer the three questions in turn.

## The thermal gain within regions

Adding the thermal predictors to the baseline raised the spatially blocked out-of-fold AUC in every region (Fig. 3 and Table 2). The interval of the gain excluded zero in all five regions at 1 km and at 5 km blocking. At 10 km blocking the point estimates stayed positive, from +0.047 to +0.154, but they rested on only 6 to 33 blocks that contain burned cells, so they are indicative. The gain kept interval support in all five regions when the predictor window was closed up to two weeks earlier, and it stayed positive at the point estimates with labels from VIIRS VNP64A1 instead of MCD64A1 (Supplementary Fig. S1). When terrain aspect was added to both feature sets, the gain stayed supported in four regions (+0.044 to +0.139) but fell to +0.020 [−0.025, +0.066] in Montiferru.

**Table 2. Within-region baseline versus thermal performance and block-size robustness.** Primary (natural-vegetation) population, spatially blocked 5-fold cross-validation and a paired spatial-block bootstrap with 1000 replicates. Block sizes of 2, 10 and 20 cells correspond to about 1, 5 and 10 km. The Baseline and Thermal columns are ROC-AUC, and the 95 % confidence interval (CI) belongs to ΔAUC.

| Region | Block | Baseline | Thermal | ΔAUC | 95% CI |
|---|---|---|---|---|---|
| Manavgat 2021 | 2 | 0.841 | 0.908 | +0.067 | [+0.060, +0.073] |
| | 10 | 0.820 | 0.882 | +0.062 | [+0.040, +0.082] |
| | 20 | 0.798 | 0.845 | +0.047 | [+0.016, +0.081] |
| Bejís 2022 | 2 | 0.862 | 0.918 | +0.056 | [+0.048, +0.065] |
| | 10 | 0.779 | 0.824 | +0.045 | [+0.018, +0.069] |
| | 20 | 0.739 | 0.795 | +0.057 | [+0.031, +0.090] |
| Muğla 2021 | 2 | 0.743 | 0.859 | +0.116 | [+0.106, +0.125] |
| | 10 | 0.698 | 0.777 | +0.079 | [+0.050, +0.105] |
| | 20 | 0.673 | 0.733 | +0.061 | [+0.030, +0.094] |
| North Evia 2021 (ext.) | 2 | 0.759 | 0.912 | +0.153 | [+0.142, +0.166] |
| | 10 | 0.716 | 0.864 | +0.148 | [+0.119, +0.182] |
| | 20 | 0.679 | 0.833 | +0.154 | [+0.124, +0.189] |
| Montiferru 2021 | 2 | 0.781 | 0.883 | +0.101 | [+0.080, +0.125] |
| | 10 | 0.620 | 0.720 | +0.099 | [+0.017, +0.186] |
| | 20 | 0.555 | 0.681 | +0.126 | [+0.053, +0.228] |

*Table note.* At 10 cells (about 5 km), every region has 16 to 70 blocks with burned cells, so this is the coarsest blocking that the design supports. The 20-cell rows are indicative. Block counts are given in Supplementary Section S5.4.

## The evaluation frame within one region

Within one region, we compared four evaluations (Table 3). The last three were scored on the same cells and differed only in their training data.

**Table 3. The four evaluations of the frame test.** Primary population, 5 km blocking. Rows B, C and D are scored on the scar frame. Row A is the whole region and is shown to make the difference visible. Means and Student *t* intervals are over the seven scars that allow row C (four in Muğla, two in Montiferru and one in Evia). The *t* intervals treat scars as independent, and region-level estimates are given in the text. Each scar is shown in Supplementary Fig. S4. In Evia the model of row C was trained on 11 burned cells (Supplementary Section S2.1).

| Evaluation | Model trained on | Scored on | Mean AUC | 95 % CI |
|---|---|---|---:|---|
| A. Blocked cross-validation | the region, scar included | the whole region | 0.773 | [0.729, 0.818] |
| B. Same blocked model, restricted | the region, scar included | the scar area | 0.640 | [0.544, 0.736] |
| C. Leave-one-scar-out | the region, scar withheld | the scar area | 0.546 | [0.488, 0.604] |
| D. Foreign region | another region, 306 to 2,802 km away | the scar area | 0.553 | [0.495, 0.611] |

The same model scored lower on the scar frame, although rows A and B used the same predictions. Over the seven scars of Table 3, A minus B was 0.133 [+0.060, +0.207]. The primary estimate uses all nine scars, including the single scars of Manavgat and Bejís, which have no row C (Supplementary Fig. S4). With the region as the unit, the change then cost +0.160 [+0.090, +0.230] over five regions. The region-wide score was the more optimistic of the two in all nine scars.

The cost came from the unburned cells next to the fire. Over nine scars, scoring the predictions on a random sample with the same burned fraction as the scar frame changed nothing (−0.002 [−0.005, +0.001]), as expected, because AUC does not depend on class balance. Scoring them on the scar frame instead of this sample cost +0.149 [+0.087, +0.211]. Replacing only the unburned cells explained 0.139 [0.098, 0.181] of this, and replacing only the burned cells −0.002 [−0.055, +0.051]. A placebo collar of the same shape, placed away from any burned cell, reproduced the region-wide score. Excluding up to two cells at the scar edge left the cost at 0.145 or more with the region as the unit (Supplementary Table S1). The cost grew as the unburned cells came closer to the fire. Against the unburned cells of one distance band at a time, the same predictions gave a mean AUC of 0.641 within 0.5 km of a burned cell, 0.769 at 2 to 5 km and 0.845 beyond 10 km (Supplementary Table S16).

Withholding the fire or moving the model had no measurable cost, but the test was weak. The effect of withholding the scar (B minus C) was +0.094 [−0.012, +0.200], and that of using a model from 306 to 2,802 km away (C minus D) was −0.007 [−0.070, +0.057]. Both evaluations were close to chance, and with region-level clustering effects of up to about 0.2 cannot be excluded (Supplementary Section S2.1).

On the scar frame, the thermal gain was not established. Averaged over the seven scars at 5 km blocking, the region-wide gain was +0.095. On the scar frame the same predictions gave +0.021 [−0.059, +0.100], leave-one-scar-out +0.024 [−0.040, +0.089], and a foreign model +0.008 [−0.021, +0.038]. At the point estimates, most of the fall therefore came with the change of scored cells.

## Cross-region transfer

Transfer varied widely, and some directions were below chance. On the original study areas, target AUC ranged from 0.314 to 0.677 with a mean of 0.527 (Fig. 4 and Supplementary Table S8). At 5 km blocking, nine of twenty directions were above chance with interval support, six were below and five were uncertain. Manavgat was the weakest target, with a mean of 0.435 against 0.494 to 0.572 for the other targets. Without the eight directions that involve Manavgat, mean transfer was 0.566, which is still far below within-region skill (Supplementary Fig. S2).

In map terms, the 10 % of target cells with the highest scores contained on average 10.3 % of the burned cells, which is what a random ranking gives, and eight of twenty directions did worse. Within regions, the same share was 35.5 % (Supplementary Table S1, Supplementary Section S4.3).

The static baseline did not transfer either (mean 0.519, against 0.527 for the thermal model), so the failure is not specific to the thermal predictors. Three simpler models did not transfer better (Supplementary Fig. S2). The paired thermal gains ranged from −0.148 to +0.132, with twelve positive and eight negative, and a mean of +0.007. All six resampling units that can be computed on this frame gave intervals that include zero (Supplementary Fig. S3). The normalised channels did not transfer better than the absolute ones. Added to the baseline, the two anomaly channels gave a mean transfer AUC of 0.524 and the four absolute channels 0.531.

The two label-free adaptation methods moved transfer toward chance (Fig. 5). Under CORAL, sixteen of twenty directions moved closer to chance, which helped the directions that failed and harmed those that worked, so the mean fell from 0.527 to 0.517. A movement toward chance is also what any loss of information would produce. Aligning the source with the covariance of a third, unrelated region moved 15 of 20 directions toward chance as well (mean 0.507). These results therefore do not show that the methods removed a distribution shift (Supplementary Sections S1.2 and S4.2).

The study areas differed strongly in their share of distant unburned cells, from 2.1 % of cells more than 10 km from any burned cell in Montiferru to 63.1 % in Bejís (Fig. 1b and Table 1). To make them comparable, we restricted every region to cells within 10 km of any burned cell (Table 4). Mean transfer rose from 0.527 to 0.589, and the number of directions below chance fell from seven to five. The thermal gain rose from +0.007 to +0.024, and the static baseline rose with it, from 0.519 to 0.565. Two below-chance directions, Manavgat to Bejís and Muğla to Manavgat, kept interval support on the collar.

**Table 4. Cross-region transfer on the original study areas and on the distance collars.** Twenty ordered directions, primary population, thermal feature set unless stated. The below-chance count is a point count. "Supported above / below" counts directions whose interval excludes 0.5, from a 10-cell (about 5 km) target-block bootstrap. Δ is the paired thermal-minus-baseline difference with a pair-cluster bootstrap interval, 1000 replicates (with 20,000 replicates, as in Supplementary Fig. S3, the collar interval is [−0.003, +0.051]). W − T is the within-region thermal gain minus the transfer gain, averaged by target region, with a Student *t* interval over the five targets.

| Frame (source and target) | Mean thermal AUC | Mean baseline AUC | Δ [95 % CI] | Below 0.5 (point) | Supported above / below | W − T [95 % CI] |
|---|---:|---:|---|---:|---|---|
| As drawn | 0.527 | 0.519 | +0.007 [−0.020, +0.038] | 7 | 9 / 6 | +0.079 [+0.014, +0.145] |
| 10 km collar | 0.589 | 0.565 | +0.024 [−0.004, +0.049] | 5 | 13 / 2 | +0.059 [+0.007, +0.110] |
| 5 km collar | 0.591 | 0.574 | +0.017 [−0.004, +0.036] | 4 | 11 / 0 | +0.026 [−0.012, +0.063] |

The thermal gain in transfer was small on every frame. On the 10 km collar its interval included zero under the primary resampling unit, although two of the five other units excluded zero (Supplementary Section S1.3). The within-region gain survived the collar and stayed positive in all five regions, with a mean of +0.083 against +0.087 on the original areas. The transfer shortfall remained on matched frames. On the 10 km collar at 5 km blocking, the within-region reference was 0.786, and transfer was +0.197 [+0.091, +0.303] below it. Skill also fell with distance inside one region. A model fitted on one half of a region reached a mean target AUC of 0.709 within 5 km of its training cells, 0.570 at 5 to 10 km and 0.519 at 10 to 20 km (Supplementary Fig. S5).

The signed associations differed between regions. In four of five regions, a hotter pre-fire surface was associated with *less* burning at the point estimates, the opposite of what the dryness idea predicts. In Manavgat the burned cells were hotter (current LST 0.665 on the original area and 0.522 on the collar), but they were also low-lying. When elevation was held constant through deciles, the Manavgat LST association fell to 0.403 [0.343, 0.464] on the collar (Supplementary Section S3.3). With elevation held, the sign stayed below 0.5 in three of the other four regions and moved to 0.509 in Bejís (Supplementary Table S6). The elevation association of Manavgat on the collar was 0.376 [0.300, 0.465], against 0.606 [0.525, 0.685] in Muğla and 0.648 [0.550, 0.740] in Evia. Under the per-comparison criterion, two reversals were supported on the collar, both on elevation and both involving Manavgat. Neither survived a Holm correction over the ninety feature-by-pair comparisons (adjusted *p* = 0.33 and 0.79, Supplementary Section S3.2).

## Pooling, feature removal and similarity

Neither intervention improved transfer measurably. A model trained on the other four regions together was better than the mean single-source model for one target of five, Evia (0.715 [0.668, 0.757] against 0.569), and worse for the other four at the point estimates (Fig. 6). Removing the two reversing features lowered within-region AUC by 0.076 at 1 km blocking and changed transfer by +0.014 [−0.018, +0.049] under the primary pair-cluster bootstrap, which includes zero (Fig. 7).

The twenty similarity measures were not changed after the label correction. On the original study areas, none predicted transfer with an interval that excludes zero (Supplementary Table S11), and in a permutation test over all 120 orderings of the five regions no measure reached p < 0.10. Under the original Manavgat label, the two largest conditional measures, the sign-agreement fraction and its cosine, had intervals that excluded zero (+0.84 and +0.81). After the label correction they did not, so this null result depends on the correction (Supplementary Section S4.5). On the 10 km collar, the cosine of the signed associations predicted transfer at ρ = +0.57 [+0.05, +0.88]. However, this is one of more than forty uncorrected similarity tests, on a frame defined by the labels, so we report it but do not use it (Supplementary Section S3.2).

The contrast pairs illustrate the similarity result at the point estimates (Fig. 8). Manavgat and Muğla have the highest niche overlap in the cohort (mean one-dimensional Schoener's *D* = 0.80), but transfer was below chance in both directions, at 0.438 and 0.345. Conversely, Bejís and Montiferru have the lowest overlap (*D* = 0.48), but transfer was above chance in both directions, at 0.594 and 0.548.
