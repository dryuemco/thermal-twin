# 4. Results

> **Rewritten 2026-08-14 in the split.** This section was 14,841 words and fifteen tables. It now
> reports the four contributions of Section 1.4 and the evidence they rest on, in six tables. The
> sensitivity analyses of the observational layer moved to the companion paper; the remaining
> supporting tables move to the supplement. Every table below is carried verbatim from the
> pre-split text, so no number was retyped.

## 4.1 Study regions and the admissibility gate

All five candidate regions pass the burned-landcover gate as wildfire candidates and the negative
control fails it as intended. Kozan 2023 returns a natural-vegetation fraction of 0.017 against the
0.50 threshold and is excluded from all modelling. The separation is not marginal: the five admitted
regions carry fractions of 0.723 to 0.991, so the threshold falls in an empty interval rather than
between neighbouring cases. That is consistent with the gate separating burned area produced by
natural-fuel combustion from post-harvest stubble burning, which MCD64A1 does not distinguish,
though one negative control cannot establish it.

**Table 2. Region summary: populations and gate outcomes.** Counts from each
region's Step 8A dataset statistics; gate fractions from each region's burned-landcover gate output.
TSG = the primary natural-vegetation population. The TSG columns use the canonical modelled
population, `burnable_tree_shrub_grass` **and** `valid_for_modeling == True`, which is the
population every model in this paper was fitted and scored on.

| Region | Total cells | Valid cells | Burned | Prevalence (all valid) | TSG cells | Burned in TSG | TSG prevalence | Burned natural-veg fraction | Gate verdict |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat 2021 | 24,150 | 24,087 | 796 | 0.033 | 20,511 | 784 | 0.038 | 0.984 | pass |
| Bejís 2022 | 15,759 | 15,759 | 1,103 | 0.070 | 15,190 | 1,100 | 0.072 | 0.991 | pass |
| Muğla 2021 | 73,098 | 73,045 | 3,026 | 0.041 | 41,730 | 2,911 | 0.070 | 0.958 | pass |
| North Evia 2021 (extended) | 22,925 | 22,906 | 2,788 | 0.122 | 9,298 | 2,664 | 0.287 | 0.945 | pass |
| Montiferru 2021 | 3,234 | 3,173 | 697 | 0.220 | 2,544 | 539 | 0.212 | 0.723 | pass |

North Evia is analysed on an extended AOI. Relative to the legacy box, the extended box leaves the
burned scar essentially unchanged while cutting overall prevalence from 0.361 to 0.122 and TSG
prevalence from 0.676 to 0.287. The effect of that choice on transfer is reported in Appendix A(a).

## 4.2 Within-region: the thermal increment replicates in five regions

Adding the six thermal predictors to the baseline raises spatially blocked out-of-fold ROC-AUC in
every region. The increment's bootstrap interval excludes zero in all five regions at 1 km and at
5 km blocking (Fig. 3). Those are the two scales this design supports as intervals. At 10 km the point
estimates hold, from +0.048 to +0.154. They rest on 6 to 33 positive-carrying blocks, so they are
reported as indicative rather than as intervals. The table note gives the reason.

**Table 3. Within-region baseline versus thermal performance and block-size robustness.** Primary
(TSG) population; spatially blocked 5-fold CV (Section 3.7); paired spatial-block bootstrap, 1000
replicates. Block sizes 2/10/20 cells ≈ 1/5/10 km.

| Region | Block (≈ scale) | Baseline AUC | Thermal AUC | ΔAUC | ΔAUC 95% CI |
|---|---|---|---|---|---|
| Manavgat 2021 | 2 (~1 km) | 0.803 | 0.870 | +0.067 | [+0.055, +0.079] |
| | 10 (~5 km) | 0.748 | 0.797 | +0.050 | [+0.023, +0.077] |
| | 20 (~10 km) | 0.683 | 0.731 | +0.048 | [+0.014, +0.085] |
| Bejís 2022 | 2 (~1 km) | 0.862 | 0.918 | +0.056 | [+0.048, +0.065] |
| | 10 (~5 km) | 0.779 | 0.825 | +0.045 | [+0.018, +0.069] |
| | 20 (~10 km) | 0.739 | 0.795 | +0.057 | [+0.031, +0.090] |
| Muğla 2021 | 2 (~1 km) | 0.743 | 0.859 | +0.116 | [+0.106, +0.125] |
| | 10 (~5 km) | 0.698 | 0.777 | +0.079 | [+0.050, +0.105] |
| | 20 (~10 km) | 0.673 | 0.733 | +0.061 | [+0.030, +0.094] |
| North Evia 2021 (ext.) | 2 (~1 km) | 0.759 | 0.912 | +0.153 | [+0.142, +0.166] |
| | 10 (~5 km) | 0.716 | 0.864 | +0.148 | [+0.119, +0.183] |
| | 20 (~10 km) | 0.679 | 0.833 | +0.154 | [+0.124, +0.189] |
| Montiferru 2021 | 2 (~1 km) | 0.781 | 0.883 | +0.101 | [+0.080, +0.125] |
| | 10 (~5 km) | 0.620 | 0.720 | +0.100 | [+0.017, +0.186] |
| | 20 (~10 km) | 0.555 | 0.681 | +0.126 | [+0.053, +0.228] |

*Table note (resampling units).* The bootstrap resamples spatial blocks, so what bounds an
interval's reliability is the number of blocks that carry at least one burned cell. Those counts
fall quickly as blocks coarsen. At 2 cells they are 235 (Manavgat), 302 (Bejís), 843 (Muğla), 716
(Evia) and 192 (Montiferru), out of 5 439, 3 967, 11 316, 2 566 and 743 blocks. At 10 cells they are
28, 19, 70, 41 and 16, out of 237, 176, 576, 155 and 35. At 20 cells they are **12, 6, 33, 15 and
6**, out of 60, 48, 167, 50 and 12. No bootstrap replicate was invalid at any block size, with one exception. At 20 cells Bejís had 5
of 1000 replicates single-class. That is the symptom of the six positive-carrying blocks just
reported, and a further reason to read the row as indicative. An equal-tailed percentile interval
built on six positive-carrying blocks has no meaningful coverage. Montiferru at 20 cells also feeds
only 12 groups into a 5-fold grouped split, so its models train on about ten blocks each. **The
20-cell row of this table should be read as indicative rather than as an interval.** The 10-cell row
is the coarsest blocking this design supports properly, because every region there has 16 to 70
positive-carrying blocks. The increment holds at that scale in all five regions. Source: `paper/referee2_numbers.md`, block C, counted from the frozen per-cell
prediction tables.

This within-region result is not itself novel. It is reported because the transfer arms below are
measured against it.

## 4.3 Cross-region transfer, and what label-free adaptation does to it

**Raw transfer is heterogeneous and includes anti-predictive directions.** Raw target AUC spans
0.326 to 0.686 (Fig. 4). Twelve of 20 directions are above chance with CI support. Six are *below* chance
with CI support: both directions of Manavgat to Bejís and of Manavgat to Muğla, plus Bejís to Evia
and Evia to Bejís. Two intervals span 0.5. Even the best raw transfer, Evia to Manavgat at 0.686,
stays far below that target's own within-region thermal performance of 0.870. Across all directions
the raw deficit against the within-region reference is 0.184 to 0.592 AUC. That reference is a
region-level blocked estimate; the controls below show it is not matched to a transfer evaluation.

Those counts belong to the 2-cell blocking of Table 4. At the more conservative 10-cell blocking the
same points give 9 above, 4 below and 7 uncertain, and no direction changes side of the chance line
(Section 4.7). Four of the six below-chance directions keep their support there. Bejís to Manavgat
and Manavgat to Muğla lose it and carry no verdict. The qualitative statement is unchanged. The
counts should not be read as exact.

**In precision terms the transfer is worse than the ROC figures suggest.** ROC-AUC is the metric
used throughout this paper, for comparability with the literature, but a susceptibility surface is
used as a ranked area budget, so precision-recall is the operational quantity. Across the twenty
directions the thermal model's PR-AUC averages **0.156 against a no-skill baseline of 0.136**. The
mean of the twenty per-direction lifts is 1.16; the ratio of the two means just quoted is 1.146.
**Six of the twenty fall below their own no-skill baseline at the point estimate, and five of those
six have intervals entirely below it.** The exception is Bejís to Manavgat, at 0.034 [0.029, 0.042]
against a baseline of 0.038, whose interval covers the baseline and which is therefore a
point-estimate case only. Only one direction, Evia to Manavgat, exceeds twice its baseline, at 0.094
against 0.038. A transferred model therefore ranks burned cells about a sixth better than random on
average, and worse than random in five directions with interval support and a sixth at the point. This is a
sharper statement than the ROC means support and it should be the one a practitioner reads.

**The static baseline does not transfer either.** This is the control for the reading the rest of
the paper invites, and it constrains that reading sharply. The same twenty directions were run with
the terrain, fuel and greenness baseline alone. The mean target AUC is **0.537**, against **0.541**
for the thermal model. Static attributes of a place are the class Dimarco et al. transfer
successfully, and are the class this paper's framing treats as portable. Here that class is itself
barely above chance. The paired per-direction contrast is given in Section 4.6b. What matters here
is that the transfer failure below is not specific to the dynamic block. A baseline that does not
travel, plus pre-fire thermal state, gives a model that does not travel.

**The thermal block's paired contribution to transfer, with its interval.** The two matrices were
differenced direction by direction. The mean is **+0.004**, but the mean is not the informative
statistic here. The individual paired contributions span **−0.148 to +0.133**, with **twelve
positive and eight negative** (`baseline_vs_thermal_transfer.csv`). The spread is thirty times the
mean, and the sign is not a property of the block but of the pair it is asked to cross: the same six
predictors that add +0.133 in one direction subtract 0.148 in another. A mean near zero here records
cancellation, not consistent absence of effect. The directions are not independent,
because each region appears in eight of the twenty. The interval therefore depends on what is
treated as the resampling unit. All four units the design permits give the same answer:

| Resampling unit | n | 95 % interval on the mean paired contribution |
|---|---:|---|
| Directions, naive | 20 | [−0.027, +0.034] |
| Unordered pairs, cluster bootstrap | 10 | [−0.028, +0.036] |
| Unordered pairs, t on pair means | 10 | [−0.034, +0.042] |
| Regions, leave-one-out jackknife | 5 | [−0.037, +0.046] |

Every interval spans zero, and the point estimate is a small fraction of each width. The per-region
jackknife shows how little the mean is anchored. Holding out Manavgat, Bejís, Muğla, Evia and
Montiferru in turn gives +0.0148, +0.0021, +0.0065, **−0.0081** and +0.0060. **Dropping Evia alone
reverses the sign of the headline.** None of these four units propagates within-direction sampling
variability. They resample between directions only.

**Where the skill is lost, on a matched comparison.** Four evaluations are reported. The last three
are scored on **identical cells**, so they differ only in what the model was trained on, and the
first is included to show why an unmatched comparison misleads. Each uses the transfer protocol
unchanged: fit, then apply with no refit, no recalibration and no threshold selection.

The held-out unit is a burned connected component of at least 50 cells together with all cells
within 2 km of it. What makes that a harder discrimination problem than a whole region is the
composition of its negatives, not its burned fraction, and that can be shown rather than argued.
Taking the same fitted model and the same out-of-fold predictions, and scoring them on a random
sample of region cells drawn at the scar area's own burned fraction, gives **0.782 against the
region-wide 0.782**: matching the prevalence changes nothing, at −0.000 [−0.003, +0.002] over the
nine scars. Scoring the same predictions on the scar area itself gives 0.627, a fall of **+0.155
[+0.093, +0.217]**. The whole effect is therefore the negative pool. Every negative in a scar collar
is fire-adjacent, sharing the terrain, land cover and synoptic conditions of the positives, whereas a
region's negatives include its easy far field. The burned fraction, 34 to 87 % against 3.8 to 28.7 %
for a region, is a symptom of that construction, and ROC-AUC is in any case invariant to class
balance at fixed class-conditional distributions.

**Table 5. The four evaluations, scored on identical cells.** Primary natural-vegetation population.
Rows B, C and D are scored on the held-out scar area; row A is the whole region and is shown to make
the mismatch visible. Means and Student *t* intervals are over the eight held-out scars.

| Evaluation | Model trained on | Scored on | Mean AUC | 95 % CI |
|---|---|---|---:|---|
| A. Blocked cross-validation, 5 km | the region, scar included | the whole region | 0.776 | [0.738, 0.814] |
| B. Same blocked model, restricted | the region, **scar included** | the scar area | 0.634 | [0.552, 0.716] |
| C. Leave-one-scar-out | the region, **scar withheld** | the scar area | 0.552 | [0.501, 0.602] |
| D. Foreign region | another region, 306 to 2,802 km | the scar area | 0.555 | [0.495, 0.616] |

All four rows are means over the **same eight scars**. A ninth burned component, Bejís, is excluded
throughout: it is that region's only component of any size, so holding it out leaves no usable
source model and there is no row C for it. Rows A, B and D are reported here on the eight so that the differences are
paired, and the intervals are Student *t* over those eight, which is the resampling unit for this arm rather than the spatial-block bootstrap used
elsewhere in the paper. Eight is a small number and the intervals are wide accordingly. Four of the
eight scars are in Muğla and two in Montiferru, so they are not independent; row A in particular is
a region-level quantity repeated across the scars of a region, and its interval is pseudo-replicated
and should not be read as coverage. The two differences are computed per scar and paired, which is
what they are reported for.

**The same model, scored two ways on the same region, differs by 0.143 AUC.** Rows A and B are one
model. The only change is which cells it is scored on: the whole region, or the burn scar and its
2 km collar. That change alone costs **0.143 [+0.077, +0.208]** of the 0.225 [+0.157, +0.293] fall from A to C,
about two thirds, and it is the size of the entire increment this literature usually reports. Both
intervals are Student *t* over the eight scars, so the "two thirds" is a ratio of two estimates and
is compatible with anything from roughly a third to nine tenths; the point of the comparison is the
size of the numerator, not the precision of the fraction. A region-wide blocked figure is
therefore an upper bound on what the same model achieves where the fire actually is, and the
difference is not small enough to ignore. Any comparison of a scar-level result against a region-level
reference inherits that, and the region-level reference is what a paper of this kind normally
reports.

**Neither withholding the fire nor moving 2,800 km has a measurable cost.** B minus C, the
fire-specific residual on identical cells, is **+0.082 [−0.011, +0.175]**, which spans zero. C minus
D, the effect of replacing a same-region model with one fitted between 306 and 2,802 km away, is
**−0.003 [−0.075, +0.069]**, which also spans zero and is an order of magnitude smaller. The second
is the cleaner result: on the same cells, a model fitted in another country does as well as one
fitted in the same region with the scar withheld, and it survives restriction to Muğla, the only
region where holding out one scar still leaves the source model properly trained, at 0.579 against
0.597.

**Row D is a mean over four foreign models, and the spread behind it is large.** Decomposing it gives
**32** scar-by-source combinations, eight scars by four foreign sources, running from 0.374 to 0.724,
with **ten of the 32 below chance** and a mean spread of 0.171 across the four sources for a given
scar, reaching 0.329 for one. The pooled
0.555 is therefore not a statement that any foreign model does as well as a same-region one. It is a
statement that the *average* foreign model does, and the variation it averages over is the
pair-specific sign instability that Sections 4.4 to 4.8 are about. Both facts belong together: a
region boundary costs nothing on average, and which side of that average a particular pair lands on
is not predictable from anything measured here.

The first difference should not be over-read, and one confound has to be stated. Holding out a
region's only large scar also removes most of its positives: the source model retains 11 positives
in Evia, 88 in Manavgat and 97 in Montiferru, against about 2,000 in Muğla, which has four separate
scars. Those four non-Muğla arms average 0.525 and the four Muğla arms 0.579. Three of the four are
genuinely starved; the fourth, Montiferru's second component, retains 472 source positives, so the
shortfall there is not a training-size effect. so row C mixes "the fire
was withheld" with "almost all the positives were withheld". Restricted to Muğla, C is 0.579 and D
is 0.597, and the C to D comparison still shows nothing. With eight scars, three of them starved, this
design cannot establish a fire-specific residual, only bound it at about 0.18 against the 0.143 that
separates row A from row B on the same model.

What this establishes is bounded rather than positive. Rows C and D both sit close to chance, so a
comparison between them has little dynamic range, and neither the fire's identity nor the region
boundary is shown to cost anything on this evaluation. What is measurable is the change of
evaluation geometry between rows A and B. What it does not establish
is the fire event as the unit, because the held-out patch is defined by the labels, so its identity
cannot be separated from its location. Two further observations point the same way: a model trained
on the other half of the same fire is no better at matched sample size, and the within-region
half-split, which does see half of the target scar, returns 0.574 against leave-one-scar-out's 0.552
with overlapping intervals.

Separation does not order the twenty-direction matrix either. The Spearman correlation between
centroid separation and transfer AUC is −0.32 with an interval spanning zero, and the two nearest
directions, Manavgat and Muğla at 306 km, are among the worst at 0.470 and 0.401. This is a
different quantity from Table 7's geographic-distance row, computed on the twelve-direction subset,
which gives −0.24; both span zero. The transfer mean of 0.541 is over all twenty directions and is
not the value at any one separation: the 2,802 km pair returns 0.326 and 0.444.

**The result is robust to how the held-out patch is defined**, at 0.543 to 0.565 across minimum
component sizes from 25 to 200 cells and under both 4- and 8-connectivity, and flat across buffers
of 2, 5 and 10 km.

**The increment declines with the holdout, and is not established once the fire is withheld.**
Contribution 1 is about the paired thermal-minus-baseline difference, so the same evaluations were
run on it.

| Evaluation | Thermal increment | Interval |
|---|---:|---|
| Blocked cross-validation, per region | +0.056 to +0.153 | every interval above zero |
| Within-region half-split | +0.027 | positive in 13 of 18 splits |
| Leave-one-scar-out | **+0.022** | **[−0.032, +0.077]** |
| Cross-region, twenty directions | +0.004 | [−0.028, +0.036] |

The point estimate falls monotonically as the holdout hardens, and the last two intervals span zero.
Under leave-one-scar-out the increment is positive in six of eight scars and averages +0.022, against
a baseline of 0.529 and a thermal 0.552 that are both close to chance on that evaluation; restricted
to Muğla it is +0.009 [−0.051, +0.070]. **The within-region increment of +0.056 to +0.153 is
therefore substantially a property of interleaved holdout.** It is not shown to be zero on an unseen
fire, and eight scars cannot show that; what this design establishes is that it is not established
there.

**On the frames as drawn, six directions are below chance with interval support**, the sharpest at
0.326 [0.305, 0.349]. No account of merely lost skill produces a reliably reversed ranking, so on
this evidence those six would need a mechanism acting on the direction of the relationship, and
Sections 4.4 to 4.8 pursue one. **Section 4.9 then shows that most of this count is an artefact of
the evaluation frames: equalising them leaves one direction below chance, not six.** The reader
should carry that forward through the intervening sections, whose reversal evidence is computed on
the frames as drawn. Per-split
and per-scar detail is in Appendix A(i).

**Table 4. Cross-region transfer matrix, thermal model, TSG population.** Target ROC-AUC with 2-cell
spatial-block bootstrap 95% CIs (1000 replicates). CORAL is applied after region-wise z-scoring (λ =
10⁻⁵).

| Direction | Raw | Region-wise z-score | CORAL |
|---|---|---|---|
| Manavgat→Bejís | 0.326 [0.305, 0.349] | 0.477 [0.451, 0.502] | 0.511 [0.484, 0.534] |
| Bejís→Manavgat | 0.444 [0.408, 0.480] | 0.457 [0.420, 0.497] | 0.555 [0.528, 0.583] |
| Manavgat→Muğla | 0.470 [0.451, 0.488] | 0.431 [0.411, 0.449] | 0.443 [0.423, 0.461] |
| Muğla→Manavgat | 0.401 [0.378, 0.426] | 0.559 [0.531, 0.587] | 0.560 [0.535, 0.587] |
| Manavgat→Evia | 0.613 [0.593, 0.631] | 0.542 [0.520, 0.565] | 0.539 [0.518, 0.561] |
| Evia→Manavgat | 0.686 [0.653, 0.716] | 0.516 [0.489, 0.544] | 0.527 [0.500, 0.553] |
| Bejís→Muğla | 0.618 [0.601, 0.635] | 0.518 [0.501, 0.535] | 0.507 [0.489, 0.524] |
| Muğla→Bejís | 0.583 [0.561, 0.607] | 0.535 [0.512, 0.557] | 0.560 [0.538, 0.581] |
| Bejís→Evia | 0.383 [0.363, 0.402] | 0.532 [0.509, 0.551] | 0.499 [0.479, 0.518] |
| Evia→Bejís | 0.448 [0.426, 0.470] | 0.549 [0.524, 0.575] | 0.549 [0.525, 0.573] |
| Muğla→Evia | 0.653 [0.636, 0.671] | 0.561 [0.543, 0.580] | 0.563 [0.545, 0.582] |
| Evia→Muğla | 0.577 [0.560, 0.593] | 0.501 [0.485, 0.518] | 0.530 [0.515, 0.546] |
| Montiferru→Manavgat | 0.567 [0.539, 0.594] | 0.573 [0.538, 0.609] | 0.606 [0.574, 0.639] |
| Manavgat→Montiferru | 0.533 [0.488, 0.580] | 0.586 [0.540, 0.629] | 0.592 [0.550, 0.631] |
| Montiferru→Bejís | 0.548 [0.521, 0.578] | 0.574 [0.552, 0.596] | 0.569 [0.548, 0.591] |
| Bejís→Montiferru | 0.594 [0.560, 0.631] | 0.550 [0.500, 0.601] | 0.574 [0.530, 0.621] |
| Montiferru→Muğla | 0.619 [0.604, 0.634] | 0.576 [0.562, 0.589] | 0.565 [0.550, 0.579] |
| Muğla→Montiferru | 0.531 [0.495, 0.568] | 0.587 [0.549, 0.624] | 0.584 [0.547, 0.623] |
| Montiferru→Evia | 0.586 [0.565, 0.606] | 0.630 [0.611, 0.649] | 0.624 [0.605, 0.641] |
| Evia→Montiferru | 0.647 [0.608, 0.682] | 0.568 [0.528, 0.609] | 0.581 [0.539, 0.623] |

**Label-blind adaptation compresses the matrix toward chance rather than repairing it.** Under
region-wise z-scoring the twenty directions span 0.431 to 0.630 and under CORAL 0.443 to 0.624,
roughly half the raw spread, with no adapted direction exceeding 0.631 against the unmatched within-region
references of 0.859 to 0.918. Adaptation raises the failing directions and degrades most of those
that already transferred. Taking the better of the two adaptations per direction, 14 of the 20 end
closer to chance than they began and 6 end further from it; five of those six involve Montiferru,
the smallest and last-added region, and move upward, while the sixth is Manavgat→Muğla moving
downward from 0.470 to 0.443. The 14 to 6 split should be read at the precision of limitation (ix) in
Section 5.9, since Bejís→Manavgat is counted as compressed on a margin of 0.001.

**Table 6. Transfer-gap decomposition (four-AOI set, 12 directions).** Within = target's
within-region thermal AUC; best adapted = the better of z-score/CORAL; recovered fraction = (adapted
− raw)/(within − raw), signed and unclipped, with paired bootstrap CI (1000 replicates). Montiferru
directions are not part of this decomposition (per-pair absolute decompositions exist without
fraction CIs). The status column asks whether the *adapted* value clears chance and uses the 2-cell
adapted intervals of Table 4. The adapted arms were not recomputed at the coarser blocking of
Appendix A(c), which covers the raw arm and the paired delta only.

| Direction | Within | Raw | Best adapted (method) | Recovered fraction [CI] | Status |
|---|---|---|---|---|---|
| Manavgat→Bejís | 0.918 | 0.326 | 0.511 (CORAL) | +0.31 [+0.28, +0.34] | recovery, chance not excluded |
| Bejís→Manavgat | 0.870 | 0.444 | 0.555 (CORAL) | +0.26 [+0.18, +0.34] | recovery above chance |
| Muğla→Manavgat | 0.870 | 0.401 | 0.560 (CORAL) | +0.34 [+0.28, +0.40] | recovery above chance |
| Bejís→Evia | 0.912 | 0.383 | 0.532 (z-score) | +0.28 [+0.23, +0.32] | recovery above chance |
| Evia→Bejís | 0.918 | 0.448 | 0.549 (z-score) | +0.22 [+0.16, +0.27] | recovery above chance |
| Manavgat→Muğla | 0.859 | 0.470 | 0.443 (CORAL) | −0.07 [−0.12, −0.03] | **negative recovery** |
| Muğla→Bejís | 0.918 | 0.583 | 0.560 (CORAL) | −0.07 [−0.16, +0.01] | **negative recovery** |
| Manavgat→Evia | 0.912 | 0.613 | 0.542 (z-score) | −0.23 [−0.32, −0.14] | **negative recovery** |
| Evia→Manavgat | 0.870 | 0.686 | 0.527 (CORAL) | −0.86 [−1.18, −0.60] | **negative recovery** |
| Evia→Muğla | 0.859 | 0.577 | 0.530 (CORAL) | −0.17 [−0.22, −0.11] | **negative recovery** |
| Muğla→Evia | 0.912 | 0.653 | 0.563 (CORAL) | −0.35 [−0.43, −0.27] | **negative recovery** |
| Bejís→Muğla | 0.859 | 0.618 | 0.518 (z-score) | −0.42 [−0.51, −0.34] | **negative recovery** |

**Against the right reference, adaptation is not failing** (Fig. 5). The three controls above give an
achievable reference for a model applied to a fire it has not seen: 0.574 for the half-split, 0.552
for the leave-one-scar-out. CORAL, committed to in advance, averages **0.552** across the twenty
directions against 0.541 raw, which is exactly that reference. Taking whichever of the two
adaptations scores higher per direction gives 0.556, but that selection uses the target labels the
protocol forbids, so it is an oracle upper bound rather than an achievable result and is reported
as one. What it does is
regress the matrix towards that value: fourteen of twenty directions move closer to chance, which
harms the directions that already worked and helps the ones that did not. The verdict that follows
is narrower than "alignment fails". Alignment cannot exceed what a model can achieve on an unseen
fire, and it does not.

In the six directions where raw transfer was below chance, the best label-free method recovers at
most 34 % of the gap to the within-region reference, so the remaining unrecovered fraction is at
least 0.66 everywhere. The half-split control above shows that the larger part of that remainder is
already incurred inside the region, so it should not be read as a measure of concept shift. Seven directions show *negative* recovery, meaning adaptation moves the score
away from the reference; in six of those raw transfer was already above chance and adaptation
destroyed that advantage. Label-free alignment therefore does not act as a repair mechanism.

## 4.4 Transferability diagnostics: what appears to order transfer, and why it does not

Twenty candidate diagnostics from five families were each rank-correlated with the same target
quantity, the raw thermal transfer AUC over the twenty ordered directions, under one common
pair-based bootstrap.

**Table 7. Transferability diagnostics versus raw thermal transfer, by family.** Spearman ρ against
raw transfer AUC with pair-based bootstrap 95 % CIs. Exp. is the sign expected if the diagnostic
orders transfer. The member named is the one with the largest absolute correlation in its family,
which is not always in the expected direction. All twenty individual diagnostics are in Appendix B,
Table B1.

| Family | Diagnostics | Exp. | Largest correlation in family | Sign as expected | Any CI excluding 0 |
|---|---:|:---:|---|:---:|---|
| **P(y\|x) conditional** | 6 | + | **+0.84 [+0.58, +0.88]** agreement fraction, supported features | yes | **yes, 2 of 6** |
| P(x\|y=1) niche overlap | 5 | + | +0.24 [−0.45, +0.74] Schoener's D, 1-D mean | yes | no |
| P(x) marginal | 6 | − | −0.32 [−0.78, +0.33] domain-classifier AUC | yes | no |
| P(y) regime structure | 2 | − | +0.29 [−0.38, +0.74] log effective-N distance | **no** | no |
| geographic | 1 | − | −0.24 [−0.84, +0.73] centroid geodesic distance | yes | no |

**Only two diagnostics have intervals excluding zero, and both are conditional.** The stronger is
the sign-agreement fraction over interval-supported features, at ρ = +0.84 [+0.58, +0.88]. The
cosine variant reaches +0.81. No marginal measure was shown to order the matrix. That includes
area-of-applicability-style dissimilarity in predictor space, climatic distance and geographic
distance. The niche-overlap and regime families were not shown to order it either. The learned
domain classifier is at ceiling, separating source from target at AUC ≥ 0.96 for every pair. It
always succeeds, which is why it carries no ordering information.

Two limits are stated with the result rather than after it. The first is size. The index's tie
structure caps the achievable Spearman at +0.861, so the observed +0.840 sits essentially on that
ceiling. Its exact one-sided permutation p is 0.0060, the smallest this tie structure can produce,
against a Bonferroni threshold of 0.0026 over the nineteen computed variants. No outcome of this
diagnostic could have cleared family-wise correction on ten effective pairs. The second limit is
labels. Signed associations need burned labels in both regions, so the family that appears to work
is not available before deployment, while the family that fails is.

**A fourth limit removes the result entirely, and is reported in Section 4.9.** The sign-agreement
index is built from the signed associations that Section 4.9 shows to be artefacts of the evaluation
frames, and it was correlated against transfer measured on those same frames. Recomputed on an
equalised frame it is unanimous, taking the value 1.0 in every direction with no variance left to
correlate, while the continuous cosine variant falls from ρ = +0.50 to +0.12. Everything in this
section is therefore reported as what the original protocol yields, and the conclusion that survives
is that **no diagnostic tested here was shown to order transfer once the frames are comparable**.

A third limit is about selection, and it is the sharpest of the three. The two rows that clear zero
are the *supported-feature* variants. Their feature subset is chosen by whether two regions'
bootstrap intervals happen to be disjoint. That is a data-dependent selection, made on the same
data, with no correction. The unselected counterparts over all nine features are ρ = +0.50
[−0.17, +0.83] for the cosine and ρ = +0.18 [−0.40, +0.72] for the agreement count. Both span zero.
The result lives in the selection step, and is reported as such.

**The families are compared on unequal samples, and equalising them does not change the ordering.**
The marginal, applicability, climatic and geographic rows sit on twelve directions, because those
diagnostics exist only for the four-region subset. The supported-conditional rows sit on sixteen and
the rest on twenty. A reader may reasonably ask whether the marginal family's failure is a statement
about power rather than about diagnostics. Every row was therefore recomputed on the common twelve
directions. The published values reproduce to 4.8 × 10⁻⁵. The conditional rows still lead, at +0.87
[+0.65, +0.88] and +0.85 [+0.43, +0.88], and every marginal row still spans zero. The ordering is not
an artefact of unequal samples.

## 4.5 The contrast pair: similarity is not sufficient

The clearest single view of Table 7 needs no ranking at all (Fig. 8). Manavgat and Muğla lie in the same
country and the same fire year. They are 306 km apart by the centroid geodesic distance this paper
uses as a diagnostic, and their nearest boundaries are 191 km apart. Their burned cells occupy the
most similar environmental envelope of any pair in the matrix, with per-feature Schoener's D of 0.77
to 0.89. Yet on the frames as drawn five of nine feature-response directions point opposite ways. Elevation
is one of them, at a signed AUC of 0.374 [0.289, 0.471] in Manavgat against 0.611 [0.532, 0.690] in
Muğla, with disjoint intervals, and all four absolute thermal channels are among the others.
**Section 4.9 withdraws that reading**: this is the pair whose Manavgat arm is 60 % far field, and
under a 10 km collar the elevation figure moves to 0.561 against 0.606, on the same side of 0.5. The
contrast that survives is the transfer result itself, not the reversal count that was offered to
explain it. Transfer is below
chance in both directions at the point estimate, at 0.470 and 0.401. Both directions also sit inside
the nominal area of applicability, at 0.875 and 0.531 of target cells.

Bejís and Montiferru sit at the opposite extreme. Their burned envelopes barely overlap, and they
carry the most dissimilar values on every overlap measure. They transfer above chance in both
directions. That half of the contrast rests on point estimates: neither direction carries a verdict
at 5 km blocking, and the marginal applicability audit was never produced for Montiferru. The claim
is one of *sufficiency*. Similarity does not guarantee transfer, and dissimilarity does not preclude
it. The claim rests on two coexisting counterexamples, so it does not depend on the number of pairs
available.

## 4.6 Interventions: pooling and feature removal

**(a) Pooled multi-region training** (Fig. 6). At the point estimate, training on the pooled primary
populations of the other four regions never beats the best single-source transfer for any target,
with shortfalls of 0.02 to 0.22, and it stays 0.28 to 0.50 AUC below the within-region ceiling; for two targets it falls below the pairwise mean and below chance, though
only Bejís is below chance with interval support, at 0.417 [0.369, 0.467]. Aggregation does not recover what single-source
transfer loses.

**(b) Removing the direction-reversing features.** The two predictors whose signed association
reverses between regions **with bootstrap support on the frames as drawn** are **`elevation_mean` and
`lst_anomaly_mean`**. Section 4.9 withdraws that support under an equalised frame, so this selection
rule is frame-dependent and the arm below measures what the removal costs under the original
protocol, not a consequence of an established reversal.
The per-region signed associations and the three pair-level reversals that meet that criterion are in
Appendix B, Tables B2 and B3. Retraining without them
costs **−0.081** of mean within-region AUC, supported in every region (per-region deltas −0.060,
−0.130, −0.074, −0.063, −0.079, every interval entirely below zero), and changes mean transfer by
**+0.014 [−0.017, +0.045]**, which spans zero.

Two qualifications belong with those numbers rather than after them. First, the debit is not the
thermal block's. Dropping elevation alone accounts for −0.061 of it, from 0.888 to 0.827. Dropping
the LST anomaly alone accounts for −0.013, from 0.888 to 0.875. Roughly three quarters of the cost
is therefore the removal of a **baseline** terrain variable, not of a thermal channel. Second, both
figures are post-selection. The two predictors were chosen because they reverse, using the same data
on which the −0.081 and the +0.014 are then estimated. No correction for that selection is applied.

| Configuration | Mean within-region AUC | Mean transfer AUC |
|---|---|---|
| full | 0.888 | 0.541 |
| drop `elevation_mean` | 0.827 | 0.546 |
| drop `lst_anomaly_mean` | 0.875 | 0.544 |
| drop both | 0.807 | 0.556 |

Figure 7 shows the four configurations together. What this measures is a local cost with no
compensating transfer gain. It does not measure an
exchange, because the transfer side is a null on both arms. The thermal block's own contribution to
transfer is +0.004, with an interval spanning zero (Section 4.3). Removing the reversing predictors
returns +0.014, with an interval spanning zero. Two nulls on the portability axis are not a price
paid.

## 4.7 Sensitivity analyses

Eight design choices were varied with everything else held fixed. They are the Evia AOI and its
prevalence, the CORAL regularisation constant, the blocking scale, the closure date of the predictor
window, the quality screening of the coarse thermal input, the contrast between the normalised and
the absolute dryness channels, the removal of the coordinate-informed channels, and the capacity of
the classifier. None changes a conclusion above. Two
bound how the results should be read, so they are carried into the main text here.

Coarsening the blocks from 1 km to 5 km moves the **paired thermal-minus-baseline delta** verdicts
from ten positive, seven negative and three uncertain to six, four and ten. The above-chance
verdicts on the thermal arm itself, a different quantity, move from twelve, six and two to nine,
four and seven. Support is removed from seven verdicts and added to none.
The point estimates are unchanged, but that is an identity rather than a result. The blocking scale
is the resampling unit, and it cannot move an estimate computed once over all target cells.

Manavgat's whole downstream chain was then rebuilt from a quality-screened MODIS input. That changes
the downscaled surface on 22,304 of 24,150 cells, by up to 10.9 °C. No signed univariate association
moves by more than +0.0003. This closes the one processing-artefact candidate for that region's
behaviour. Appendix A reports all eight arms, including one that tests a claim of Section 1.2 and does not uphold it.

## 4.8 The same geography, a second fire: reversal with place held constant

Every result above compares different places. Muğla admits a stricter test, because a second fire
burned inside the identical AOI on the identical analysis grid. The 2021 event has a predictor
window closing on 28 July. The 2022 event has a matched window closing on 20 June. Region, bounding
box, cell definition, feature registry and processing chain are the same in both arms. The design
holds place fixed. It does not hold season fixed, because the 2022 fire ignites about six weeks
earlier, and it does not hold the population fixed, because the 2022 arm is defined by removing the
2021 scar.

**Table 8. Signed univariate feature-burned AUC, Muğla 2021 versus 2022.** Raw AUC against
`burned`, never folded to max(AUC, 1 − AUC); 10-cell (≈ 5 km) spatial-block bootstrap, 1,000
replicates, seed 42 (Section 3.15). Analysis population 41,730 rows / 2,911 burned (2021) and
38,790 rows / 331 burned (2022). **Positive-carrying 5 km blocks: 70 for the 2021 arm and 11 for the
2022 arm.** Table 3's note sets sixteen as the floor this design supports at that blocking, so the
2022 intervals here fall below the paper's own standard and are read as indicative, exactly as the
20-cell row of Table 3 is. The 2022 arm is additionally a single compact scar, so its eleven blocks
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

**Elevation reverses with bootstrap support.** In 2021 higher ground burned preferentially, at 0.611
with its interval entirely above 0.5; in 2022 lower ground did, at 0.296 with its interval entirely
below. The two intervals are disjoint, 0.532 against 0.355, and the difference is −0.317 [−0.414,
−0.220]. The same predictor, the same region, the same grid, and an association that points the
opposite way in two fires eleven months apart. The four absolute thermal channels change side as
well, from bootstrap-supported lower-values-burn in 2021 to higher-values-burn point estimates in
2022.

Two structural properties must be read alongside these numbers, because they have no analogue in the
twenty-direction matrix. The two arms are not disjoint samples: they share 38,789 of the 2022 arm's
38,790 cells, and elevation, slope and land cover are identical to the digit across all 73,098 grid
cells, so only NDVI and the six thermal channels carry new information between them. And the removal
is the target's own positive class, so in the 2022 to 2021 direction not one target positive is
present in the source training population while 38,789 of 38,819 target negatives are, and
membership of the source training set alone separates the 2021 target's classes at ROC-AUC 0.9996.
We therefore cannot bound what that asymmetry does to a transfer estimate between the two arms,
which is why none is reported here, only state that a
direction with this structure is not comparable to the twenty between-region directions. The
elevation reversal is the finding; the structural asymmetry is a competing explanation this design
cannot exclude. The known part of the bias runs the safe way: the removed cells are high, with a
median of 563 m, and unburned in 2022, so removing them raises the 2022 elevation AUC and makes the
reversal smaller rather than larger.

## 4.9 The evaluation frame, applied to our own matrix

Section 4.3 established that swapping a region's negatives for fire-adjacent ones moves ROC-AUC by
+0.155 [+0.093, +0.217] with the model held fixed. That result was obtained inside one region. It
applies with equal force between regions, and applying it changes what Sections 4.3 and 4.5 can
claim. This section reports that test. Source: `aoi_frame_auc.csv`, `aoi_frame_transfer.csv`,
`paper/code/verify_aoi_frame.py`, `paper/code/verify_aoi_transfer.py`.

**The five areas of interest are not comparable frames.** Each region is a rectangle drawn around a
fire, and the rectangles differ by an order of magnitude in how much unburnt far field they enclose.

**Table 10. Evaluation-frame geometry of the five study regions.** Primary natural-vegetation
population. Distance is Euclidean to the nearest burned cell on the 500 m grid, at 0.45 km per cell.
Source `aoi_frame_auc.csv`; recomputable by `paper/code/verify_aoi_frame.py`.

| Region | cells | burned | median distance to burned | share beyond 10 km |
|---|---:|---:|---:|---:|
| Manavgat | 20,511 | 784 | 13.4 km | **60.1 %** |
| Bejís | 15,190 | 1,100 | 13.5 km | **63.1 %** |
| Muğla | 41,730 | 2,911 | 11.3 km | 55.3 % |
| Evia | 9,298 | 2,664 | 8.0 km | 43.7 % |
| Montiferru | 2,544 | 539 | 2.7 km | **2.1 %** |

Montiferru's frame is fire-scale; Manavgat's and Bejís's are roughly three-fifths far field. The
far field is not a neutral addition. In Manavgat the median elevation of modelled cells rises from
472 m within 5 km of the fire to 955 m at 10 to 20 km and 1,273 m at 20 to 50 km, against 512 m for
the burned cells themselves, in Taurus terrain that no plausible spread model would place at risk.

**Under an equalised frame the sign reversals of Section 4.5 do not survive.** Restricting every
region to cells within 10 km of any burned cell drops **no positives**, only far-field negatives.

**Table 11. Signed univariate AUC, frame as drawn against a 10 km collar.** Point estimates; the
intervals that decide the reversal question are given in the text below and in
`collar_frame_bootstrap.csv` (10-cell blocks, 1000 replicates, seed 42). Signed and never folded to
max(AUC, 1 − AUC), so a value below 0.5 is a direction, not weakness. The collar drops no burned
cells in any region.

| Signed univariate AUC | Manavgat | Bejís | Muğla | Evia | Montiferru | straddles 0.5 |
|---|---:|---:|---:|---:|---:|---|
| elevation, full frame (Table B2) | **0.374** | 0.643 | 0.611 | 0.541 | 0.584 | **yes** |
| elevation, 10 km collar | 0.561 | 0.614 | 0.606 | 0.648 | 0.581 | no |
| current LST, full frame | **0.538** | 0.477 | 0.325 | 0.377 | 0.370 | **yes** |
| current LST, 10 km collar | 0.386 | 0.405 | 0.332 | 0.286 | 0.376 | no |
| current TVDI, full frame | **0.552** | 0.517 | 0.336 | 0.362 | 0.356 | **yes** |
| current TVDI, 10 km collar | 0.392 | 0.454 | 0.342 | 0.250 | 0.361 | no |

On the equalised frame all five regions agree in sign on elevation, on LST and on TVDI, and both
bootstrap-supported elevation reversals of Table B3 disappear. Applying this paper's own criterion
from Section 3.10, which requires each region's own 10-cell block-bootstrap interval to exclude 0.5,
**no reversal remains bootstrap-supported in the collar frame** (`collar_frame_bootstrap.csv`). Two
features straddle 0.5 at the point estimate and neither is supported. `lst_anomaly_mean` runs 0.392
[0.324, 0.460] in Bejís against 0.584 [**0.497**, 0.669] in Evia, so the point estimates fall on
opposite sides but Evia's interval includes 0.5 by 0.003. `tvdi_difference_mean` straddles as well,
at 0.509 [0.417, 0.597] in Muğla against 0.384 [0.288, 0.504] in Montiferru, and no region's
interval excludes 0.5. These are the two internally differenced channels, and an earlier draft of
this section treated the first as uniquely informative because it carries no lapse-rate signal; that
argument does not hold, because the second is equally decorrelated from elevation and behaves the
same way. Both are point reversals, not supported ones. We state it that way rather than quoting the point
estimates alone, because the alternative would be to apply a looser standard to the arm that
supersedes Table B3 than to Table B3 itself. Elevation under the collar is above 0.5 in all five
regions but individually supported in only two, Muğla at 0.606 [0.525, 0.685] and Evia at 0.648
[0.550, 0.740].

**The sign the five regions agree on is not the one the dryness framing predicts.** For LST the
common direction is *below* 0.5 in every region, at 0.386, 0.405, 0.332, 0.286 and 0.376: a hotter
pre-fire surface is associated with **less** burning, not more, and the same holds for TVDI. This is
not a lapse-rate artefact. Pooling concordance within elevation deciles leaves LST at 0.402, 0.509,
0.363, 0.327 and 0.392, still below 0.5 in four of five regions, and within NDVI deciles at 0.440,
0.486, 0.404, 0.279 and 0.368, below 0.5 in all five, despite r(LST, NDVI) reaching −0.92. The
likely reading is that fuel availability dominates surface dryness at this scale in this cohort:
NDVI itself is the most consistently supported single predictor under the collar, at 0.582 to 0.663
with intervals excluding 0.5 in four of five regions, more than any other feature, though in Muğla
and Evia the absolute thermal channels are further from 0.5, so greener and therefore more fuel-rich cells burn more,
while the hottest cells are the sparse, rocky ones with little to burn. Section 1.2 motivates the
thermal block from moisture-stress physics; that motivation is not what the signed associations
show, and Section 5.2 states the consequence.

**The same test destroys the one diagnostic that appeared to work.** Section 4.4's only diagnostic
with an interval excluding zero is the fraction of features whose signed association points the same
way in source and target, counted over features interval-supported in both. That statistic is built
out of exactly the signed AUCs this section has just shown to be frame artefacts, and it was
correlated against transfer measured on the same unequal frames. Recomputing both sides under the
10 km collar (`diagnostics_collar_frame.csv`, `paper/code/verify_diag_collar.py`):

**Table 12. The two diagnostics that ordered transfer, recomputed on an equalised frame.** Spearman
ρ against target ROC-AUC over the ordered directions in which the diagnostic is defined. Source
`diagnostics_collar_frame.csv`; recomputable by `paper/code/verify_diag_collar.py`.

| Diagnostic | Full frame | 10 km collar |
|---|---|---|
| Sign-agreement fraction over supported features | ρ = +0.86 (p = 0.0001, n = 14), values {0, 0.5, 1} | **1.0 in all 18 defined directions, variance exactly 0 — degenerate** |
| Cosine similarity over all nine signed AUCs | ρ = +0.50 (p = 0.023, n = 20) | ρ = +0.12 (p = 0.61, n = 20) |

Once the frames are equalised every region pair agrees in sign on every jointly supported feature,
so the diagnostic has no variance left and its correlation with transfer is undefined rather than
weak. This is not a marginal shift: the number of features supported in both regions *rises* from
1.20 to 3.40 per direction, so the diagnostic is better determined and unanimous. The disagreements
it was reading were the far fields.

**Contribution 3 is therefore restated, and it becomes a stronger negative result.** The finding is
not that conditional similarity orders transfer where marginal similarity fails. It is that **no
diagnostic tested here, marginal or conditional, orders transfer once the evaluation frames are
equalised** — and the one that appeared to was measuring how the study rectangles were drawn. The
practitioner's position is worse than Section 4.4 implied, not better: there is no screen, and the
apparent exception was an artefact. Section 4.4's numbers are retained as computed, on the frames as
drawn, because they are what a reader following the original protocol would obtain; this section is
the correction.

Three further points bound how many independent reversals could have been counted. Within the
collar, `fused_lst_mean` correlates with `current_lst_mean` at 0.99 to 1.00 and
`downscaled_lst_mean` at 0.97 to 0.99, and `current_tvdi_mean` at 0.87 to 0.98. The four absolute
channels are close to one axis, and the two anomaly channels correlate at 0.64 to 0.94, so the "five
of nine directions reverse" count of Section 4.5 is a count of features, not of independent
quantities; in effective dimensions it is closer to two.
The channels whose reversal vanishes are the ones that were partly measuring terrain. Current LST
correlates with elevation at r = −0.695, −0.125, −0.404, −0.511 and −0.507 across the five regions,
and TVDI at −0.722 to −0.298, so their proxy strength varies fivefold between regions and a frame
that shifts the elevation distribution shifts them with it. The two internally differenced channels
are decorrelated from elevation by construction — the LST anomaly at −0.195 to +0.256 — and neither
of them yields a supported reversal either, so this explains which reversals were manufactured
without licensing a claim that any survived.

**The transfer matrix moves as well.** Restricting source and target to the same collar:

**Table 9. Cross-region transfer under equalised evaluation frames.** Primary natural-vegetation
population, thermal model, twenty ordered directions per row. Above/below chance are point counts;
the supported counts use the same 10-cell (≈5 km) spatial-block bootstrap on the target as Table 4,
1000 replicates, seed 42. Per-direction bounds are in `aoi_frame_transfer.csv`.

| Source frame | Target frame | Mean target AUC | Above chance | Below chance | Supported above / below | Paired thermal delta |
|---|---|---:|---:|---:|---:|---:|
| full | full (**Table 4**) | 0.540 | 14 of 20 | **6** | 9 / **4** | +0.003 |
| full | 10 km | 0.575 | 17 of 20 | 3 | 11 / 1 | +0.002 |
| 10 km | full | 0.571 | 17 of 20 | 3 | 11 / 3 | +0.014 |
| **10 km** | **10 km** | **0.617** | **19 of 20** | **1** | **15 / 1** | **+0.023** |
| 5 km | 5 km | 0.608 | 18 of 20 | 2 | 12 / 0 | +0.014 |

The reference arm reproduces the frozen matrix, at 0.540 against Table 4's 0.541 and 14 of 20
exactly, so this is measuring the same quantity. The above- and below-chance counts in this table
are point counts. Under the same 10-cell block bootstrap used for Table 4, at 1000
replicates, the full frame gives nine directions above chance and four below with interval support,
and the collar frame fifteen above and one below, so the headline movement is six to one at the
point estimate and **four to one with interval support** (`aoi_frame_transfer.csv`, which carries
the per-direction bounds). The largest movers are Bejís to Evia, 0.383 to
0.602, and Bejís to Manavgat, 0.440 to 0.601.

**What this does and does not change.** Three claims do not survive and are withdrawn here rather
than defended. The count of six anti-predictive directions becomes one. The sign reversal of
elevation, LST and TVDI as the mechanism of the residual is a property of the frames, not of the
predictor-burning relationship. And the paired thermal contribution is not stable at +0.004: it
rises to +0.023 once frames are equalised, so the claim that the block contributes nothing between
regions is frame-dependent too. What survives is the central negative result, and it survives with
room to spare: equalised transfer of 0.617 against within-region skill of about 0.87 leaves most of
the gap intact. Section 5.9 records the frame as a limitation of the cohort rather than of the
method, since equalising it is cheap and we recommend it.

This is the paper's own Contribution 1 turned on the paper's own matrix. We had measured that the
composition of the negative pool moves ROC-AUC by more than the effects this literature reports, and
had then computed a five-region transfer matrix, and a mechanism, on frames whose fire-adjacent
share ranges from 37 % to 98 %. We report it because it is the strongest available demonstration that
the reporting standard of Section 5.8 is not a technicality.

## 4.10 What target labels cost: the recovery curve

Everything above measures a failure; this prices it. Label-free alignment does not close the residual
gap, so the missing resource is information about the target that alignment cannot synthesise, and
the direct way to supply it is target labels. A frozen labelled-budget diagnostic answers how many, for
three regions across all six ordered directions, using one 10-cell (~5 km) spatial block as the unit
of labelling effort and reading recovery against a matched target-only ceiling of 0.777 to 0.824.

Thirty-two labelled blocks recover **85 to 89 % of that ceiling in three of the six directions**, two
of which started below chance; 51 to 57 % in two more, the directions where the conditional gap is
widest; and 30 % in the sixth. That budget is 7 to 20 % of the target's natural-vegetation
population, which at the 2,700 to 3,000 labelled cells those blocks carry (S1.3) and this grid's
effective cell area of 0.199 to 0.208 km² (Appendix C) is roughly **540 to 620 km²**, so it is a real
answer and not a cheap one. Two properties of the
measurement bound it and are stated in the supplement rather than buried: at the top budget the
selection pool is nearly exhausted, so the narrow upper-budget intervals reflect saturation rather
than precision, and the labelled blocks are drawn from the event being predicted, which is not a
resource available before that event burns. The protocol, the full curve and the limits are in
Supplement S1.

Two limits belong with the number. At small budgets the same intervention damages the direction that
already transfers best without any labels. And six directions in three regions cannot support a
general label budget, so none is offered.
