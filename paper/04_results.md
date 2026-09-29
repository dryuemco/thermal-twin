# 4. Results

## 4.1 Study regions and the admissibility gate

All five regions passed the burned-landcover gate, while the negative control failed it. Kozan 2023
had a natural-vegetation fraction of 0.017 against the threshold of 0.50 and was excluded, whereas the
five admitted regions had fractions of 0.723 to 0.991. The gate therefore separates the cases
clearly, although one negative control cannot show that it always works. The extended North Evia
rectangle kept the burned scar almost unchanged and gave a burned prevalence of 0.287 in the primary
population (Section S1.1).

## 4.2 The thermal gain within regions

Adding the thermal predictors to the baseline raised the spatially blocked out-of-fold ROC-AUC in
every region (Fig. 3; Table 1). The interval of the gain excluded zero in all five regions at 1 km
and at 5 km blocking. At 10 km blocking the point estimates stayed positive, from +0.047 to +0.154,
but they rest on only 6 to 33 blocks that contain burned cells, so they are indicative. The gain also stayed positive, with interval support in all five regions, when the predictor window
was closed up to two weeks earlier (Section S1.4). With labels from VIIRS VNP64A1 instead of
MCD64A1, the gain stayed positive in all five regions at the point estimates (Section S1.23). When terrain aspect was added to both feature sets, the
gain stayed supported in four regions (+0.044 to +0.139) but fell to +0.020 [−0.025, +0.066] in
Montiferru (Section S1.23).

**Table 1. Within-region baseline versus thermal performance and block-size robustness.** Primary
(natural-vegetation) population; spatially blocked 5-fold CV (Section 3.7); paired spatial-block
bootstrap, 1000 replicates. Block sizes of 2, 10 and 20 cells correspond to about 1, 5 and 10 km.
The Baseline and Thermal columns are ROC-AUC, and the 95 % CI belongs to ΔAUC. Source files are
listed in the Supplementary Material.

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

*Table note.* At 10 cells (about 5 km), every region has 16 to 70 blocks with burned cells, so this is
the coarsest blocking that the design supports. The 20-cell rows are indicative. Block counts are
given in Section S1.3.

## 4.3 The effect of the evaluation frame within one region

This section measures the effect of the evaluation frame on one model in one region, so no transfer
is involved. Four evaluations are compared (Table 2). The last three are scored on **the same cells**,
so they differ only in the training data. The held-out unit is a scar of at least 50 burned cells
together with its 2 km collar.

**Table 2. The four evaluations of the frame test.** Primary population, 5 km blocking. Rows B, C
and D are scored on the scar frame. Row A is the whole region and is shown to make the difference
visible. Means and Student *t* intervals over the seven scars that allow row C: four in Muğla, two in
Montiferru and one in Evia. The *t* intervals treat scars as independent; region-level estimates are
given in the text. Cell counts per scar are in Table S1.

| Evaluation | Model trained on | Scored on | Mean AUC | 95 % CI |
|---|---|---|---:|---|
| A. Blocked cross-validation | the region, scar included | the whole region | 0.773 | [0.729, 0.818] |
| B. Same blocked model, restricted | the region, **scar included** | the scar area | 0.640 | [0.544, 0.736] |
| C. Leave-one-scar-out | the region, **scar withheld** | the scar area | 0.546 | [0.488, 0.604] |
| D. Foreign region | another region, 306 to 2,802 km away | the scar area | 0.553 | [0.495, 0.611] |

**The same model scores lower on the scar frame.** Rows A and B use one model and one set of
predictions, and only the scored cells differ. Over the seven scars of Table 2, A minus B is 0.133
[+0.060, +0.207]. The primary estimate uses all nine scars, including the single scars of Manavgat
and Bejís, which have no row C (Tables S1 and S5). With the region as the unit, the change then
costs **+0.160 [+0.090, +0.230]** over five regions, and +0.137 [+0.048, +0.226] over the three
regions of Table 2. The seven-scar interval is too narrow, because row A is repeated for each scar of a region. With the region as the unit, the
fall from A to C is +0.266 [−0.022, +0.553]. **Only the frame cost is therefore established at the
region level.** The two frames answer different questions (Section 3.12), so the region-wide score is
not a biased version of the scar score. It is, however, the more optimistic of the two, and it holds
in all nine scars.

**The cost comes from the unburned cells next to the fire.** Over nine scars, scoring the predictions
on a random sample with the same burned fraction as the scar frame changed nothing (−0.002 [−0.005,
+0.001]). This is expected, because ROC-AUC does not depend on class balance. Scoring them on the scar
frame cost +0.149 [+0.087, +0.211]. Replacing only the unburned cells explained 0.139 [0.098, 0.181]
of this, and replacing only the burned cells −0.002 [−0.055, +0.051] (Section S1.9.1). A placebo
collar of the same shape, placed away from any burned cell, reproduced the region-wide score, and
excluding up to two cells at the scar edge left the cost at 0.145 or more with the region as the
unit (Table S21). Across regions, the cost showed no relation to the share of distant cells in the study area (slope
0.005 [−0.41, +0.42], n = 5), although this test has little power. The pool swaps and the placebo
collar show that the cost comes from the unburned cells next to the fire.

**Withholding the fire or moving the model had no measurable cost, but the test is weak.** B minus
C, the effect of withholding the scar, is +0.094 [−0.012, +0.200]. C minus D, the effect of using a
model from 306 to 2,802 km away, is −0.007 [−0.070, +0.057]. Both intervals include zero, and both
evaluations are close to chance. In Evia, however, withholding the scar leaves only 11 burned cells
for training. In Muğla alone, where every held-out case keeps a well-trained model, C and D are 0.579
and 0.586. With region-level clustering the intervals widen strongly. For example, the difference in
thermal gain between rows C and D widens from [−0.061, +0.094] to [−0.154, +0.186]. Effects of up to
about 0.2 therefore cannot be excluded.

**On the scar frame, the thermal gain is not established.** The same four evaluations were applied to
the thermal gain at 5 km blocking. Averaged over the seven scars, with Muğla counted four times, the
region-wide gain is +0.095. On the scar frame the same predictions give +0.021 [−0.059, +0.100].
Leave-one-scar-out gives +0.024 [−0.040, +0.089], and a foreign model +0.008 [−0.021, +0.038]. The
fall from +0.095 therefore occurs when the frame changes, not when the training data change (Section
S1.9.3).

## 4.4 The frame effect between regions

The five study areas differ strongly in how many distant unburned cells they contain. The share of
cells more than 10 km from any burned cell is **2.1 %** in Montiferru and **63.1 %** in Bejís (Table
S13). In Manavgat, the median elevation of the modelled cells rises from 330 m within 5 km of the fire to
1,273 m at 20 to 50 km, while the burned cells have a median of 287 m.

**Comparable study areas.** Every region was restricted to cells within 10 km of any burned cell.
This removes only distant unburned cells. Table 3 compares transfer on these collars with transfer on
the original areas. Mean transfer rose from 0.527 to 0.589, and the number of directions below chance
fell from seven to five. The thermal gain rose from +0.007 to +0.024, and the static baseline rose
with it, from 0.519 to 0.565. Because the collars are defined from burned cells, they cannot be drawn
before a fire (Section 3.12).

**Table 3. Cross-region transfer on the original study areas and on the distance collars.** Twenty
ordered directions, primary population, thermal feature set unless stated. The below-chance count is
a point count. "Supported above / below" counts directions whose interval excludes 0.5, from a 10-cell
(about 5 km) target-block bootstrap. Δ is the paired thermal-minus-baseline difference with a
pair-cluster bootstrap interval, 1000 replicates (with 20,000 replicates, as in Table S31, the collar
interval is [−0.003, +0.051]). W − T is the within-region thermal gain minus the
transfer gain, averaged by target region, with a Student *t* interval over the five targets.

| Frame (source and target) | Mean thermal AUC | Mean baseline AUC | Δ [95 % CI] | Below 0.5 (point) | Supported above / below | W − T [95 % CI] |
|---|---:|---:|---|---:|---|---|
| As drawn | 0.527 | 0.519 | +0.007 [−0.020, +0.038] | 7 | 9 / 6 | +0.079 [+0.014, +0.145] |
| 10 km collar | 0.589 | 0.565 | +0.024 [−0.004, +0.049] | 5 | 13 / 2 | +0.059 [+0.007, +0.110] |
| 5 km collar | 0.591 | 0.574 | +0.017 [−0.004, +0.036] | 4 | 11 / 0 | +0.026 [−0.012, +0.063] |

**The thermal gain in transfer is small on every frame.** On the 10 km collar its interval includes
zero under the primary resampling unit. Of the five other units that can be computed, two exclude
zero: clustering by target region and clustering by source region (Section S1.22). In an exploratory equivalence test with a margin of ±0.05, set after the results, the gain on the
original study areas was within the margin under all six units that can be computed, and the collar
gain under four of six. It was not within the margin under the pigeonhole bootstrap or the region
jackknife, whose 90 % upper bounds are 0.052 and 0.055. The difference between the within-region and
transfer gains (W − T) is positive on the original areas and on the 10 km collar, but not on the 5 km
collar (Table 3).

**Associations on the collar.** On the collar, four regions agree in sign on elevation, LST and TVDI,
and Manavgat is on the other side of 0.5 on all three. Its elevation association is 0.376 [0.300,
0.465], against 0.606 [0.525, 0.685] in Muğla and 0.648 [0.550, 0.740] in Evia (Bejís and Montiferru
in Table S14). Under the per-comparison criterion of Section 3.10, **two reversals are supported on the collar.
Both are on elevation, and both involve Manavgat.** They are not the same pairs as on the original
areas. Manavgat against Muğla is supported on both frames. Manavgat against Evia becomes supported on
the collar, because the Evia interval excludes 0.5 only there. Manavgat against Bejís loses support
narrowly: the Bejís interval, [0.496, 0.722], misses 0.5 by 0.004. Neither collar reversal survives
a Holm correction over the ninety feature-by-pair comparisons (adjusted *p* = 0.33 and 0.79; Section
S1.19).

**Hotter surfaces burned less at the point estimates.** In four of five regions, a hotter pre-fire
surface was associated with *less* burning, which is the opposite of what the dryness idea predicts.
In Manavgat the burned cells are hotter (current LST 0.665 on the original area), but they are also
low-lying. When elevation is held constant through deciles, the Manavgat LST association falls to 0.403
[0.343, 0.464] on the collar, and after the linear effect of elevation is removed it is 0.409 [0.350,
0.475]. On the original area the same values are 0.455 and 0.446, with intervals that include 0.5
(Sections S1.11 and S1.23). These results
indicate that the absolute thermal channels behaved here mainly as land-surface descriptors rather
than as a dryness index.

**Similarity measures on the collar.** Two similarity measures are built from these signed
associations. The sign-agreement fraction did not predict transfer on the original areas (ρ = +0.52
[−0.27, +0.87]) or on the collar (ρ = +0.38). Its cosine version predicted collar transfer at
ρ = +0.57 [+0.05, +0.88]. However, this is one of about forty uncorrected tests, on a frame defined by
the labels, so it is reported but not used (Section S1.19).

**Two further results depend on the frame.** In the Muğla two-fire comparison, 93.2 % of the 2022
cells lie more than 10 km from a burned cell, against 55.3 % in 2021, and on the collar the Muğla
elevation reversal disappears (Section S1.13). By contrast, the within-region gain stays positive in
all five regions on the collar, with a mean of +0.083 against +0.087 on the original areas.

**The transfer shortfall remains on matched frames.** A fair comparison needs the same frame and the
same blocking. On the 10 km collar at 5 km blocking, the within-region reference is 0.786, and
transfer is **+0.197 [+0.091, +0.303]** below it (Student *t* over the five targets). Manavgat has the
largest shortfall (+0.319).

## 4.5 Cross-region transfer on the original study areas

The results in this section use the original study areas and should be read together with Section
4.4. Values for each direction are given in Table S16.

**Transfer varied widely, and some directions were below chance.** Target AUC ranged from 0.314 to
0.677 (Fig. 4). At 5 km blocking, nine of twenty directions were above chance with interval support,
six were below and five were uncertain; at 1 km blocking the intervals are narrower (Section S1.20).
Two below-chance directions keep interval support on the collar: Manavgat to Bejís and Muğla to
Manavgat. Manavgat was the weakest target, with a mean of 0.435 against 0.494 to 0.572 for the other
targets. Without the eight directions that involve Manavgat, mean transfer was 0.566, which is still
far below within-region skill (Section S1.23).

**In precision terms, transfer is weaker still.** Precision-recall AUC averaged **0.181, against a
no-skill baseline of 0.157**; the baseline of each target is its burned prevalence, which ranges from
0.070 to 0.287. The median lift over the baseline was 1.18. Seven of twenty directions were below their own
baseline. At 5 km blocking, two of these seven had intervals below the baseline, both into Manavgat (Table
S11). In map terms, the 10 % of target cells with the highest scores contained on average 10.3 % of
the burned cells, which is what a random ranking gives, and eight of twenty directions did worse.
Within regions, the same share was 35.5 % (Section S1.23).

**The static baseline did not transfer either.** Its mean was **0.519**, against **0.527** for the
thermal model, so the failure is not specific to the thermal predictors.

**The thermal gain varies in sign between pairs.** The paired gains ranged from **−0.148 to +0.132**,
with twelve positive and eight negative, and a mean of +0.007. The directions are not independent,
because each region appears in eight of them. Accordingly, all six resampling units that can be computed on this frame give intervals that include
zero, from [−0.006, +0.022] (clustering by target region) to [−0.028, +0.045] (pigeonhole bootstrap;
Sections S1.15 and S1.23).

**The two label-free adaptation methods moved transfer toward chance** (Fig. 5). Under region-wise
z-scoring the twenty directions ranged from 0.302 to 0.630, and under CORAL from 0.406 to 0.624. Under
CORAL, sixteen of twenty directions moved closer to chance. This helped the directions that failed
and harmed those that worked, so the mean fell from 0.527 to **0.517**. Choosing the better method in
each direction gave 0.523, but this choice uses target labels. The gap decomposition covers the twelve directions among Manavgat, Bejís, Muğla and Evia. It was
computed before Montiferru was added to the cohort and does not include it.
There, seven directions showed negative recovery, five of them with intervals below zero (Section
S1.10). A movement toward chance is also what any loss of information would produce. Indeed, aligning the
source with the covariance of a third, unrelated region moved 15 of 20 directions toward chance as
well (mean 0.507). CORAL with a stronger regularisation (λ = 1, mean 0.512) or on two thermal
components (0.523) did not help either (Section S1.23). These results therefore do not show that
the methods removed a distribution shift.

## 4.6 Further results

**Pooling.** A model trained on the other four regions together was better than the mean
single-source model for one target of five, Evia (0.715 [0.668, 0.757] against 0.569), and worse
for the other four at the point estimates (Fig. 6).

**Feature removal.** Removing the two reversing features lowered within-region AUC by 0.076 and changed transfer by
+0.014 [−0.028, +0.056], which includes zero (Fig. 7); the primary pair-cluster bootstrap gives
[−0.018, +0.049] (Section S1.14).

**Target labels.** With 32 labelled 5 km blocks from the target, the gap between raw transfer and the
target's own ceiling was closed by 83 to 89 % in three of six directions, and by 30 to 52 % in the
other three. However, these blocks are 7 to 20 % of the target population and contain most of its
burned cells, for example 880 of 1,100 in Bejís. They also come from the fire that is predicted, so
they are not available before that fire (Section S4).

**Similarity measures.** Twenty similarity measures were recorded on 8 August 2026 and were not
changed after the label correction. On the original study areas, none predicted transfer with an interval that excludes zero (Table
S17), and in a permutation test over all 120 orderings of the five regions no measure reached
p < 0.10 (Section S1.23). One measure is defined on only six directions and is not interpreted. The contrast pairs illustrate this at the point estimates (Fig. 8). Manavgat and Muğla
have the highest niche overlap in the cohort (mean one-dimensional Schoener's *D* = 0.80), but
transfer was below chance in both directions, at 0.438 and 0.345. Conversely, Bejís and Montiferru
have the lowest overlap (*D* = 0.48), but transfer was above chance in both directions, at 0.594 and
0.548. At 5 km blocking only Muğla to Manavgat keeps interval support (Section S1.16).
