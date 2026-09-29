# 4. Results

## 4.1 Study regions and the admissibility gate

All five regions passed the burned-landcover gate, and the negative control failed it. Kozan 2023
had a natural-vegetation fraction of 0.017 against the threshold of 0.50 and was excluded. The five
admitted regions had fractions of 0.723 to 0.991. The gate therefore separates the cases clearly,
although one negative control cannot show that it always works. The extended North Evia rectangle
kept the burned scar almost unchanged and gave a burned prevalence of 0.287 in the primary
population (Section S1.1).

## 4.2 The thermal gain within regions

Adding the thermal predictors to the baseline raised the spatially blocked out-of-fold ROC-AUC in
every region (Fig. 3; Table 1). The interval of the gain excluded zero in all five regions at 1 km
and at 5 km blocking. At 10 km the point estimates stayed positive, from +0.047 to +0.154, but they
rest on only 6 to 33 blocks that contain burned cells, so they are indicative. The gain also stayed
positive, with interval support in all five regions, when the predictor window was closed up to two
weeks earlier (Section S1.4).

**Table 1. Within-region baseline versus thermal performance and block-size robustness.** Primary
(natural-vegetation) population; spatially blocked 5-fold CV (Section 3.7); paired spatial-block
bootstrap, 1000 replicates. Block sizes 2/10/20 cells ≈ 1/5/10 km. Baseline and Thermal columns are
ROC-AUC; the 95 % CI belongs to ΔAUC. Source: the pipeline's step8b/step8c outputs (block 2) and
its large-block robustness outputs (blocks 10 and 20); Manavgat from
`paper/labelfix_rerun/pipeline/`.

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

*Table note.* The 10-cell row, with 16 to 70 blocks containing burned cells in every region, is the
coarsest blocking that this design supports. Block counts are given in Section S1.3.

## 4.3 The effect of the evaluation frame within one region

This section measures the effect of the evaluation frame on one model in one region. No transfer is
involved. Four evaluations are compared (Table 2). The last three are scored on **the same cells**,
so they differ only in the training data. The held-out unit is a group of at least 50 burned cells
with all cells within 2 km of it.

**Table 2. The four evaluations of the frame test.** Primary population, 5 km blocking. Rows B, C
and D are scored on the held-out scar area; row A is the whole region and is shown to make the
mismatch visible. Means and Student *t* intervals over the seven scars that admit row C (four in
Muğla, two in Montiferru, one in Evia). Source: `paper/labelfix_rerun/code/matched_holdout.json`.

| Evaluation | Model trained on | Scored on | Mean AUC | 95 % CI |
|---|---|---|---:|---|
| A. Blocked cross-validation | the region, scar included | the whole region | 0.773 | [0.729, 0.818] |
| B. Same blocked model, restricted | the region, **scar included** | the scar area | 0.640 | [0.544, 0.736] |
| C. Leave-one-scar-out | the region, **scar withheld** | the scar area | 0.546 | [0.488, 0.604] |
| D. Foreign region | another region, 306 to 2,802 km away | the scar area | 0.553 | [0.495, 0.611] |

**The same model loses 0.133 AUC when it is scored at the fire.** Rows A and B use one model and one
set of predictions. Only the scored cells differ. This change alone costs **0.133 [+0.060, +0.207]**,
about three fifths of the 0.227 [+0.147, +0.308] fall from A to C. Row A is repeated across the scars
of a region, so the scar-level interval is too narrow. With the region as the unit, the cost is
**+0.137 [+0.048, +0.226]** over three regions and **+0.160 [+0.090, +0.230]** over all nine scars in
five regions (`paper/labelfix_rerun/round7/round7_summary.json`). With the region as the unit, the
fall from A to C is +0.266 [−0.022, +0.553]. **Only the frame cost is established at the region
level.** A region-wide score is therefore an upper bound for the same model at the fire.

**The cost comes from the unburned cells.** Over nine scars, scoring the predictions on a random
sample with the same burned fraction as the scar area changed nothing (−0.002 [−0.005, +0.001]). This
is expected, because ROC-AUC does not depend on class balance. Scoring them on the scar area cost
+0.149 [+0.087, +0.211]. Replacing only the unburned cells explained 0.139 [0.098, 0.181] of this, and
replacing only the burned cells −0.002 [−0.055, +0.051] (Section S1.9.1). Unburned cells next to a
fire are similar to the burned cells, while a whole region also contains easy distant cells.

**Withholding the fire and moving 2,800 km cost nothing measurable.** B minus C, the effect of
withholding the scar, is **+0.094 [−0.012, +0.200]**. C minus D, the effect of using a model from
306 to 2,802 km away, is **−0.007 [−0.070, +0.057]**. Both intervals include zero, and both arms are
close to chance. With seven scars, this design can only bound a fire-specific effect at about 0.20.

**At the fire, the thermal gain is not established.** The same evaluations were applied to the
thermal gain at 5 km blocking. In the three regions of Table 2 the region-wide gain is +0.095. On the
scar area, the same predictions give +0.021 [−0.059, +0.100]. Leave-one-scar-out gives +0.024
[−0.040, +0.089], and a foreign model +0.008 [−0.021, +0.038]. The fall from +0.095 therefore happens
when the frame changes, not when the training data change (Section S1.9.3).

## 4.4 The frame effect between regions

The five study areas differ strongly in how many distant unburned cells they contain. The share of
cells more than 10 km from any burned cell is **2.1 %** in Montiferru and **63.1 %** in Bejís (Table
S13). In Manavgat the median elevation of these cells rises from 330 m within 5 km of the fire to
1,273 m at 20 to 50 km, while the burned cells have a median of 287 m.

**Comparable study areas.** Every region was restricted to cells within 10 km of any burned cell.
This removes only distant unburned cells. Table 3 compares transfer on these collars with transfer
on the original areas. Mean transfer rose from 0.527 to 0.589, and the number of directions below
chance fell from seven to five. The thermal gain rose from +0.007 to +0.024. The static baseline rose
with it, from 0.519 to 0.565.

**Table 3. Cross-region transfer as drawn and on the equalised collars.** Twenty ordered
directions, primary population, thermal feature set unless stated. Support counts use the 10-cell
(~5 km) target-block bootstrap; the paired contribution Δ (thermal minus baseline) uses the
pair-cluster bootstrap, 1000 replicates. W − T is the within-region thermal increment minus the
transfer increment, averaged by target region, with a Student *t* interval over the five targets.
Sources: `paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv`,
`paper/labelfix_rerun/code/equalised_delta_interval.json`,
`paper/labelfix_rerun/inference/equivalence.json`.

| Frame (source and target) | Mean thermal AUC | Mean baseline AUC | Δ [95 % CI] | Below 0.5 (point) | Supported above / below | W − T [95 % CI] |
|---|---:|---:|---|---:|---|---|
| As drawn | 0.527 | 0.519 | +0.007 [−0.020, +0.038] | 7 | 9 / 6 | +0.079 [+0.014, +0.145] |
| 10 km collar | 0.589 | 0.565 | +0.024 [−0.004, +0.049] | 5 | 13 / 2 | +0.059 [+0.007, +0.110] |
| 5 km collar | 0.591 | 0.574 | +0.017 [−0.004, +0.036] | 4 | 11 / 0 | +0.026 [−0.012, +0.063] |

**The thermal gain in transfer is small on every frame.** On the 10 km collar its interval still
includes zero under the primary resampling unit. Two of the five other units exclude zero
(clustering by target or by source region; Section S1.23). An equivalence test shows that the gain is
within ±0.05 of zero under four of five units, and a gain above 0.047 is not supported. The
difference between within-region and transfer gains (W − T) is positive on the original areas and on
the 10 km collar, but not on the 5 km collar (Table 3).

**Associations on the collar.** On the collar, four regions agree in sign on elevation, LST and TVDI,
and Manavgat is on the other side of 0.5 on all three. Its elevation association is 0.376 [0.300,
0.465], against 0.606 [0.525, 0.685] in Muğla and 0.648 [0.550, 0.740] in Evia. Under the per-comparison criterion of Section 3.10, **two reversals remain on the
collar. Both are on elevation, and both involve Manavgat.** Neither survives a Holm correction over the ninety
feature-by-pair comparisons (adjusted *p* = 0.33 and 0.79; Section S1.20). All other supported
elevation reversals disappear on the collar.

**Hotter surfaces burned less, and the Manavgat exception is terrain.** At the point estimates, a
hotter pre-fire surface burned *less* in four of five regions. This is the opposite of what the
dryness idea predicts. In Manavgat the burned cells are hotter (current LST 0.665 on the full frame),
but they are also low-lying. When elevation is held constant, Manavgat's LST association falls to
0.455 on the full frame and 0.403 on the collar, and to 0.446 and 0.409 after removing the linear
effect of elevation (`paper/labelfix_rerun/round7/r7b_lst_given_terrain.csv`; Section S1.11). Manavgat
therefore shares the common sign once terrain is held. The absolute thermal channels behave here as
land-surface descriptors rather than as a dryness index.

**Similarity measures on the collar.** Two similarity measures are built from these signed
associations. The sign-agreement fraction did not predict transfer on the original areas (ρ = +0.52
[−0.27, +0.87]) or on the collar (ρ = +0.38). Its cosine version predicted collar transfer at
ρ = +0.57 [+0.05, +0.88]. This is one of about forty uncorrected tests, on a frame defined by the
labels, so it is reported but not used (Section S1.20).

**Two other results depend on the frame.** In the Muğla two-fire comparison, 93.2 % of the 2022 cells
lie more than 10 km from a burned cell, against 55.3 % in 2021. On the collar the Muğla elevation
reversal disappears (Section S1.13). The within-region gain, by contrast, stays positive in all five
regions on the collar, with a mean of +0.083 against +0.087 on the original areas.

**The transfer shortfall remains on matched frames.** A fair comparison needs the same frame and the
same blocking. On the 10 km collar at 5 km blocking, the within-region reference is 0.786. Transfer
is therefore **+0.197 [+0.091, +0.303]** below it (Student *t* over the five targets). Manavgat has the
largest shortfall (+0.319).

## 4.5 Cross-region transfer on the original study areas

The results in this section use the original study areas and should be read with Section 4.4 in mind.
Per-direction values are given in Table S16.

**Transfer varied widely, and some directions were below chance.** Target AUC ranged from 0.314 to
0.677 (Fig. 4). At 1 km blocking, eleven of twenty directions were above chance with interval
support and seven below. At 5 km blocking, nine were above, six below and five uncertain. Two
below-chance directions keep interval support on the collar: Manavgat to Bejís and Muğla to
Manavgat. Manavgat was the weakest target, with a mean of 0.435 against 0.494 to 0.572 for the other
targets.

**In precision terms, transfer is weaker still.** PR-AUC averaged **0.181 against a no-skill
baseline of 0.157**. Seven of twenty directions were below their baseline. At 1 km blocking all seven
had intervals below it; at 5 km blocking two did, both into Manavgat
(`paper/labelfix_rerun/round7/r7a_pr_auc_10cell.csv`; Table S11).

**The static baseline did not transfer either.** Its mean was **0.519**, against **0.527** for the
thermal model. The failure is therefore not specific to the thermal predictors.

**The thermal gain varies in sign between pairs.** The paired gains ranged from **−0.148 to +0.132**,
with twelve positive and eight negative, and a mean of +0.007. The directions are not independent,
because each region appears in eight of them. All four resampling units that this design allows give
intervals that include zero, from [−0.018, +0.033] to [−0.028, +0.043] (Section S1.21).

**Label-blind adaptation pushed transfer toward chance** (Fig. 5). Under region-wise z-scoring the
twenty directions ranged from 0.302 to 0.630, and under CORAL from 0.406 to 0.624. Sixteen of twenty
directions moved closer to chance. This helped the directions that failed and harmed those that
worked. CORAL averaged **0.517**, against 0.527 without adaptation. Taking the better method in each
direction gave 0.523, but this choice uses target labels. Seven directions showed negative recovery,
five of them with intervals below zero (Section S1.10).

## 4.6 Further results

**Pooling.** A model trained on the other four regions together was better than the mean
single-source model for one target of five, Evia (0.715 [0.668, 0.757] against 0.569), and worse for
the other four (Fig. 6; `paper/labelfix_rerun/round7/r7d_pooled_vs_single.csv`).

**Feature removal.** Removing the two reversing features cost −0.076 AUC within regions and changed
transfer by +0.014 [−0.028, +0.056], which includes zero (Fig. 7).

**Target labels.** With 32 labelled 5 km blocks from the target, the gap between raw transfer
and the target's own ceiling was closed by 83 to 89 % in three of six directions. In the other three
it was closed by 30 to 52 %. These blocks are 7 to 20 % of the target population and come from the fire being
predicted, so they are not available before that fire (Section S5).

**Similarity measures.** Twenty similarity measures were defined on 8 August 2026 and were not
changed after the label correction. On the original study areas, none predicted transfer with an
interval excluding zero (Table S17). One measure is defined on only six directions and is not
interpreted. The contrast pairs show the result directly (Fig. 8). Manavgat and Muğla have the
highest niche overlap in the cohort (mean one-dimensional Schoener's *D* = 0.80), but transfer failed
in both directions, at 0.438 and 0.345. Bejís and Montiferru have the lowest overlap (*D* = 0.48), but
transfer was above chance in both directions, at 0.594 and 0.548. These are point estimates. At 5 km
blocking only Muğla to Manavgat keeps interval support (Section S1.16).
