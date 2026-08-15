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

North Evia is analysed on an extended AOI. Relative to the legacy box, the extended box leaves the
burned scar essentially unchanged while cutting overall prevalence from 0.361 to 0.122 and TSG
prevalence from 0.676 to 0.287. The effect of that choice on transfer is reported in Appendix A(a).

## 4.2 Within-region: the thermal increment replicates in five regions

Adding the six thermal predictors to the baseline raises spatially blocked out-of-fold ROC-AUC in
every region. The increment's bootstrap interval excludes zero in all five regions at 1 km and at
5 km blocking (Fig. 3). Those are the two scales this design supports as intervals. At 10 km the point
estimates hold, from +0.048 to +0.154. They rest on 6 to 33 positive-carrying blocks, so they are
reported as indicative rather than as intervals. The table note gives the reason.

**Table 1. Within-region baseline versus thermal performance and block-size robustness.** Primary
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
interval's reliability is the number of blocks carrying at least one burned cell, and those counts
fall quickly as blocks coarsen: 235, 302, 843, 716 and 192 at 2 cells; 28, 19, 70, 41 and 16 at 10
cells; and **12, 6, 33, 15 and 6** at 20 cells, out of 60, 48, 167, 50 and 12 blocks. No bootstrap
replicate was invalid at any block size except Bejís at 20 cells, where 5 of 1000 were single-class
— the symptom of the six positive-carrying blocks just reported. An equal-tailed percentile interval
built on six positive-carrying blocks has no meaningful coverage, and Montiferru at 20 cells feeds
only 12 groups into a 5-fold grouped split, so its models train on about ten blocks each. **The
20-cell row of this table should be read as indicative rather than as an interval.** The 10-cell row
is the coarsest blocking this design supports properly, every region there having 16 to 70
positive-carrying blocks, and the increment holds at that scale in all five regions. Source:
`paper/referee2_numbers.md`, block C.

This within-region result is not itself novel. It is reported because the transfer arms below are
measured against it.

## 4.3 What the evaluation frame is worth, within one region

This section isolates the effect Section 4.4 applies between regions. It comes first because it is
measured on one model in one region with no transfer involved, so nothing the transfer arms do can
explain it.

**Where the skill is lost, on a matched comparison.** Four evaluations are reported. The last three
are scored on **identical cells**, so they differ only in what the model was trained on; the first
shows why an unmatched comparison misleads. Each uses the transfer protocol unchanged: fit, then
apply with no refit, no recalibration and no threshold selection. The held-out unit is a burned
connected component of at least 50 cells together with all cells within 2 km of it.

What makes that a harder problem than a whole region is the composition of its negatives, not its
burned fraction, and that can be shown rather than argued. Taking the same fitted model and the same
out-of-fold predictions and scoring them on a random sample of region cells drawn at the scar area's
own burned fraction gives **0.782 against the region-wide 0.782**: matching the prevalence changes
nothing, at −0.000 [−0.003, +0.002] over the nine scars. Scoring the same predictions on the scar
area itself gives 0.627, a fall of **+0.155 [+0.093, +0.217]**. The whole effect is the negative
pool. Every negative in a scar collar is fire-adjacent, sharing the terrain, land cover and synoptic
conditions of the positives, whereas a region's negatives include its easy far field. The burned
fraction, 34 to 87 % against 3.8 to 28.7 % for a region, is a symptom of that construction, and
ROC-AUC is in any case invariant to class balance at fixed class-conditional distributions.

**Table 2. The four evaluations, scored on identical cells.** Primary natural-vegetation population.
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
**32** scar-by-source combinations running from 0.374 to 0.724, with **ten below chance** and a mean
spread of 0.171 across the four sources for a given scar (Appendix A, Table A3). The pooled 0.555 is
therefore not a statement that any foreign model does as well as a same-region one, but that the
*average* one does, and the variation it averages over is exactly the pair-specific instability that
the rest of Section 4 is about.

One confound must be stated. Holding out a region's only large scar also removes most of its
positives: the source model retains 11 positives in Evia, 88 in Manavgat and 97 in Montiferru,
against about 2,000 in Muğla, which has four separate scars. Those four non-Muğla arms average 0.525
and the four Muğla arms 0.579. Three of the four are genuinely starved — the fourth, Montiferru's
second component, retains 472 source positives — so row C mixes "the fire was withheld" with "almost
all the positives were withheld". Restricted to Muğla, C is 0.579 and D is 0.597, and the C-to-D
comparison still shows nothing. **With eight scars, three of them starved, this design cannot
establish a fire-specific residual, only bound it at about 0.18.**

What this establishes is bounded rather than positive. Rows C and D both sit close to chance, so the
comparison between them has little dynamic range, and neither the fire's identity nor the region
boundary is shown to cost anything here. What is measurable is the change of evaluation geometry
between rows A and B. Nor does it establish the
fire event as the unit, because the held-out patch is defined by the labels, so its identity cannot
be separated from its location. The within-region half-split, which does see half of the target
scar, returns 0.574 against leave-one-scar-out's 0.552, with overlapping intervals.

**The result is robust to how the held-out patch is defined.** Sweeping the two parameters that
define it — minimum burned-component size over 25, 50, 100 and 200 cells, and connectivity over the
4- and 8-neighbourhoods — moves the row-C mean between **0.545 and 0.566** across all eight settings,
against the 0.552 of the reported configuration, which the sweep reproduces to 0.001
(`scar_definition_sweep.csv`, `paper/code/scar_definition_sweep.py`). The number of qualifying scars
falls from eleven to seven as the size threshold rises, which is what moves the mean; connectivity
changes it by at most 0.001 at any threshold. The result is also flat across buffers
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


## 4.4 The same effect between regions, applied to our own matrix

Section 4.3's effect applies with equal force between regions, and this section reports that test
before the transfer matrix rather than after it, because it changes what Sections 4.5 and 4.7 can
claim. It withdraws nothing in Section 4.3, which is what the test is built from. Sources:
`aoi_frame_auc.csv`, `aoi_frame_transfer.csv`, `collar_frame_bootstrap.csv`,
`diagnostics_collar_frame.csv` and the code under `paper/code/`.

**The five areas of interest are not comparable frames.** Each is a rectangle drawn around a fire,
and they differ by an order of magnitude in how much unburnt far field they enclose: the share of
modelled cells beyond 10 km of any burned cell runs from **2.1 %** in Montiferru to **63.1 %** in
Bejís (Appendix B, Table B6). That far field is not a neutral addition — in Manavgat the median
elevation of modelled cells rises from 472 m within 5 km of the fire to 1,273 m at 20 to 50 km,
against 512 m for the burned cells themselves.

**Under an equalised frame the sign reversals of Appendix A(s) do not survive.** Restricting every
region to cells within 10 km of any burned cell removes only far-field negatives; every burned cell
is at distance zero and is retained at any radius, so the protection against choosing a flattering
radius is the sweep below, not the retention of positives. On the equalised frame all five regions
agree in sign on elevation, on LST and on TVDI, and both bootstrap-supported elevation reversals of
Table B3 disappear. Under this paper's own criterion from Section 3.10 — each region's own 10-cell
block-bootstrap interval must exclude 0.5 — **no reversal remains bootstrap-supported**. Two features
straddle 0.5 at the point estimate and neither is supported: `lst_anomaly_mean` at 0.392 [0.324,
0.460] in Bejís against 0.584 [**0.497**, 0.669] in Evia, where Evia's interval includes 0.5 by
0.003; and `tvdi_difference_mean` at 0.509 [0.417, 0.597] in Muğla against 0.384 [0.288, 0.504] in
Montiferru, where no region's interval excludes 0.5. These are the two internally differenced
channels. An earlier draft treated the first as uniquely informative because it carries no lapse-rate
signal; that does not hold, since the second is equally decorrelated from elevation and behaves the
same way.

**A weaker instrument does support the anomaly result.** Table B3's note commits this paper to a
difference interval on the pair as the sharper test. Applied under the collar, four pairs have
opposite-sided point estimates **and** a difference interval excluding zero, all on
`lst_anomaly_mean` and three of the four involving Evia (Appendix A(l), Table A6). Three caveats keep
it weak: nine of ninety feature-by-pair differences clear zero against about 4.5 expected under the
null with no multiplicity correction, the nine features are effectively two to three dimensions, and
Evia's own interval-support status turns on 0.003. **The honest statement is that no reversal meets
this paper's strict criterion under the collar, and that the LST anomaly differs between regions on
the weaker difference instrument.** Elevation under the collar is above 0.5 in all five regions but
individually supported in only two.

**The sign the five regions agree on is not the one the dryness framing predicts.** In every region
a hotter pre-fire surface is associated with **less** burning, and the same holds for TVDI. It is
neither a lapse-rate artefact nor greenness acting through fuel load: on mutual adjustment the
surviving channel is LST, not NDVI. Two caveats bound it — in two regions it is a residual spatial
gradient that disappears when distance to the nearest burned cell is stratified inside the collar,
and interval support is not uniform, so "all five agree" is a statement about point estimates. What
we can defend is that the absolute thermal channels behave here as **static land-surface
descriptors** rather than as a dryness index, and that the two internally differenced channels carry
no consistent cross-region direction at all. Compositing depth was not tested and remains an open
alternative. Per-region values are in Appendix A(k); Section 5.2 states the consequence for the
moisture-stress motivation of Section 1.2.

**The same test determines what the diagnostics of Section 4.6 can establish.** The only two
candidates there with intervals excluding zero measure agreement in the sign of each predictor's
association between source and target, counted over features interval-supported in both. Those are
built out of exactly the signed AUCs this section has shown to be frame artefacts, and in Section
4.6 they are correlated against transfer measured on the same unequal frames. Recomputing both sides under the 10 km collar:

**Table 3. The diagnostics that ordered transfer, recomputed on an equalised frame.** Spearman ρ
against target ROC-AUC over the ordered directions in which each is defined. The first two rows are
the two variants that cleared zero in Table B1; the third is the all-feature cosine, which did not
and is shown for contrast. Both sides are recomputed here under one bootstrap setting, 1000
replicates, seed 42. Source `diagnostics_collar_frame.csv` and `collar_increment_and_cosine.csv`.

| Diagnostic | Full frame | 10 km collar |
|---|---|---|
| Sign-agreement fraction, supported features | ρ = +0.86 (p = 0.0001, n = 14) | **1.0 in all 18 directions, variance exactly 0 — degenerate** |
| Cosine, supported features | ρ = +0.81 (p = 0.0005, n = 14) | **ρ = −0.06 (p = 0.82, n = 18)**, variance 0.00014 |
| Cosine, all nine features | ρ = +0.50 (p = 0.023, n = 20) | ρ = +0.12 (p = 0.61, n = 20) |

The two fail differently and both fail. Once frames are equalised every region pair agrees in sign
on every jointly supported feature, so the agreement fraction has no variance left. The supported
cosine keeps a trace of variance — unanimous signs fix directions but not magnitudes — and simply
stops tracking transfer. This is not a marginal shift: features supported in both regions *rise*
from 1.20 to 3.40 per direction, so the diagnostics are better determined and unanimous. The
disagreements they were reading were the far fields.

Two scope statements belong with the table and are given in Appendix A(o): the full-frame values
here are not numerically the published ones, because the support test is itself bootstrap-dependent;
and only these diagnostics were recomputed on the collar, so the other eighteen are unknown against
the equalised transfer vector rather than shown to be null.

This settles what Contribution 3 can claim. It is not that conditional similarity orders transfer
where marginal similarity fails; it is that **no diagnostic tested here has been shown to order
transfer**. The eighteen marginal, niche and regime candidates do not order it on the frames as
drawn, and the two conditional variants that do stop doing so once the frames are comparable,
because what they were reading is how the study rectangles were drawn. The practitioner's position
is therefore worse than the as-drawn analysis suggests, not better: there is no screen, and the
apparent exception is an artefact. Section 4.6 reports its numbers as computed under the
pre-registered protocol, which is what a reader following that protocol would obtain.

**The same-geography arm of Appendix A(m2) does not survive either, and it is the most extreme case in
the cohort.** A fixed study area is not a fixed evaluation frame: its 2022 arm has 93.2 % of cells
beyond 10 km of any burned cell against 55.3 % for 2021. Under the same collar the 2021 figure barely
moves while the 2022 figure crosses to the same side of 0.5 with an interval covering chance, so
**no bootstrap-supported sign reversal survives anywhere in this paper once evaluation frames are
equalised**, between regions or between two fires in one region. Values in Appendix A(m).

**The within-region increment survives the same correction**, remaining positive in all five
regions on the equalised frame with a mean of +0.077 against +0.086 as drawn, and halving but
staying positive in all five at a 5 km collar. The paper's one surviving predictor-level positive
claim therefore holds on the frame it argues is the correct one. Per-region values are in Appendix
A(r).

**The transfer matrix moves as well.** Restricting source and target to the same collar:

**Table 4. Cross-region transfer under equalised evaluation frames.** Primary natural-vegetation
population, thermal model, twenty ordered directions per row. Above/below chance are point counts;
the supported counts use the same 10-cell (≈5 km) spatial-block bootstrap on the target as Table B9,
1000 replicates, seed 42. Per-direction bounds are in `aoi_frame_transfer.csv`.

| Source frame | Target frame | Mean target AUC | Above chance | Below chance | Supported above / below | Paired thermal delta |
|---|---|---:|---:|---:|---:|---:|
| full | full (**Table B9**) | 0.540 | 14 of 20 | **6** | 9 / **4** | +0.003 |
| full | 10 km | 0.575 | 17 of 20 | 3 | 11 / 1 | +0.002 |
| 10 km | full | 0.571 | 17 of 20 | 3 | 11 / 3 | +0.014 |
| **10 km** | **10 km** | **0.617** | **19 of 20** | **1** | **15 / 1** | **+0.023** |
| 5 km | 5 km | 0.608 | 18 of 20 | 2 | 12 / 0 | +0.014 |

The reference arm reproduces the frozen matrix, at 0.540 against Table B9's 0.541 and 14 of 20
exactly, so this is measuring the same quantity. **The baseline control moves with it and must be
restated on this frame**: the static baseline transfers at 0.593 against the thermal model's 0.617,
a paired difference of +0.023 rather than the +0.003 of the frame as drawn. The control still holds
in kind — the static predictor class is not the portable one either — but the gap between them is
eight times larger once frames are comparable, and Sections 1, 5 and 6 quote only the as-drawn
pair. The above- and below-chance counts in this table
are point counts. Under the same 10-cell block bootstrap used for Table B9, at 1000
replicates, the full frame gives nine directions above chance and four below with interval support,
and the collar frame fifteen above and one below, so the headline movement is six to one at the
point estimate and **four to one with interval support** (`aoi_frame_transfer.csv`, which carries
the per-direction bounds). The largest movers are Bejís to Evia, 0.383 to
0.602, and Bejís to Manavgat, 0.440 to 0.601.

**What this settles, and what it leaves standing.** Five quantities reported in the sections that
follow are properties of the frames rather than of the predictor-burning relationship, and are
identified as such where they appear: the count of six anti-predictive directions, which becomes
one; the sign reversal of elevation, LST and TVDI as a mechanism; the sign-agreement diagnostic of
Section 4.6; the same-geography arm of Appendix A(m2); and the paired thermal contribution, which is
+0.004 as drawn and +0.023 equalised. What the correction leaves standing is the central negative
result, and its size must be stated on a matched comparison. Setting the equalised transfer mean of
0.617 against a within-region reference of about 0.87 would compare a 10 km-collar number with a
full-rectangle one at 1 km blocking, which is the most generous reference in the paper and the very
figure Section 4.3 argues is an upper bound. Recomputing the within-region
reference on the same frame and at the 5 km blocking this design defends
(`matched_frame_gap.csv`, `paper/code/verify_matched_gap.py`):

| Frame | Within-region (5 km blocking) | Mean transfer | Gap |
|---|---:|---:|---:|
| full rectangle | 0.798 | 0.540 | 0.258 |
| 10 km collar | **0.772** | **0.617** | **0.155** |
| 5 km collar | 0.737 | 0.608 | 0.129 |

Paired by target region, the collar shortfall is **+0.155 [+0.094, +0.217]** (Student *t* over the
five target regions; per-region +0.086 Montiferru, +0.127 Manavgat, +0.161 Muğla, +0.196 Bejís,
+0.206 Evia), which reproduces the point estimate above and excludes zero. The shortfall therefore
survives on every matched row, but it is **0.155 at the collar, not the 0.25 the unmatched
comparison implies**, and it shrinks as the frame approaches the fire —
which is where a susceptibility surface is actually used.

This is Section 4.3's effect acting between regions rather than within one, on frames whose
fire-adjacent share ranges from 37 % to 98 %. Section 5.9(x) records the frame as a limitation of
this cohort rather than of the method.

## 4.5 Cross-region transfer, and what label-free adaptation does to it


**Everything in this section is computed on the frames as drawn, and should be read against Section
4.4.** That section has already shown the frames are not comparable, that equalising them lifts mean
transfer from 0.540 to 0.617 and leaves **one** direction below chance rather than six, and that the
within-region reference used below is itself frame-dependent. The as-drawn matrix is reported in
full because it is what the pre-registered protocol yields and what a reader following that protocol
would obtain; the corrections are not repeated at each number.

**Raw transfer is heterogeneous and includes anti-predictive directions.** Raw target AUC spans
0.326 to 0.686 (Fig. 4). Twelve of 20 directions are above chance with CI support. Six are *below*
chance with CI support: both directions of Manavgat to Bejís and of Manavgat to Muğla, plus Bejís to
Evia and Evia to Bejís — of which only Manavgat to Bejís survives frame equalisation. Two intervals
span 0.5. Even the best raw transfer, Evia to Manavgat at 0.686, stays far below that target's own
within-region thermal performance of 0.870. Across all directions the raw deficit against the
within-region reference is 0.184 to 0.592 AUC. That reference is a region-level blocked estimate,
and Section 4.3 shows it is not matched to a transfer evaluation.

Those counts belong to the 2-cell blocking of Table B9. At the more conservative 10-cell blocking the
same points give 9 above, 4 below and 7 uncertain, and no direction changes side of the chance line
(Appendix A(v)). Four of the six below-chance directions keep their support there. Bejís to Manavgat
and Manavgat to Muğla lose it and carry no verdict. The qualitative statement is unchanged. The
counts should not be read as exact.

**In precision terms the transfer is worse than the ROC figures suggest.** A susceptibility surface
is used as a ranked area budget, so precision-recall is the operational quantity. Across the twenty
directions the thermal model's PR-AUC averages **0.156 against a no-skill baseline of 0.136**. **Six
of the twenty fall below their own no-skill baseline at the point estimate, five of them with
intervals entirely below it**; the exception is Bejís to Manavgat, whose interval covers its
baseline. Only one direction exceeds twice its baseline. These are frame-as-drawn quantities and the
PR arm was not recomputed on the collar. Per-direction values are in Appendix B, Table B4.

**The static baseline does not transfer either.** The same twenty directions were run with the
terrain, fuel and greenness baseline alone, giving a mean target AUC of **0.537** against **0.541**
for the thermal model. Static attributes of a place are the class Dimarco et al. transfer
successfully and the class this paper's framing treats as portable; here that class is itself barely
above chance. The transfer failure below is therefore not specific to the dynamic block: a baseline
that does not travel, plus pre-fire thermal state, gives a model that does not travel.

**The thermal block's paired contribution to transfer, with its interval.** Differencing the two
matrices direction by direction gives a mean of **+0.004**, but the mean is not the informative
statistic. The individual contributions span **−0.148 to +0.133**, twelve positive and eight
negative, so the spread is thirty times the mean and the sign belongs to the pair rather than to the
block; a mean near zero records cancellation, not consistent absence of effect. The directions are
not independent, since each region appears in eight of the twenty, so the interval depends on the
resampling unit — **all four units the design permits give the same answer**, from [−0.027, +0.034]
treating directions as independent to [−0.037, +0.046] jackknifing regions, and none propagates
within-direction sampling variability (Appendix A(o)). The leave-one-region-out jackknife shows how
little the mean is anchored: **dropping Evia alone reverses its sign.**

**On the frames as drawn, six directions are below chance with interval support**, the sharpest at
0.326 [0.305, 0.349]. Section 4.4 has shown most of that count is a property of the frames:
equalising them leaves **one**, Manavgat to Bejís at 0.417 [0.349, 0.488], supported at the 10 km
collar though its interval covers chance at 5 km. That direction still needs a mechanism acting on
the direction of the relationship, because no account of merely lost skill produces a reliably
reversed ranking, and Section 4.6 pursues it. Everything below this point is computed on the
frames as drawn and should be read against Section 4.4. Per-split and per-scar detail is in Appendix
A(i); per-direction values for all twenty directions, raw and under both adaptations, are in
Appendix B, Table B9.

**Label-blind adaptation compresses the matrix toward chance rather than repairing it.** Under
region-wise z-scoring the twenty directions span 0.431 to 0.630 and under CORAL 0.443 to 0.624,
roughly half the raw spread, with no adapted direction exceeding 0.631 against the unmatched within-region
references of 0.859 to 0.918. Adaptation raises the failing directions and degrades most of those
that already transferred. Taking the better of the two adaptations per direction, 14 of the 20 end
closer to chance than they began and 6 end further from it; five of those six involve Montiferru,
the smallest and last-added region, and move upward, while the sixth is Manavgat→Muğla moving
downward from 0.470 to 0.443. The 14 to 6 split should be read at the precision of limitation (ix) in
Section 5.9, since Bejís→Manavgat is counted as compressed on a margin of 0.001.

The per-direction decomposition is in Appendix A(j), Table A5; two figures from it matter here and
are used below.

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
already incurred inside the region, so it should not be read as a measure of concept shift. On the four-AOI twelve-direction subset for which the decomposition is defined (Appendix A(j)),
seven directions show *negative* recovery, meaning adaptation moves the score
away from the reference; in six of those raw transfer was already above chance and adaptation
destroyed that advantage. Label-free alignment therefore does not act as a repair mechanism.

## 4.6 Transferability diagnostics: what appears to order transfer, and why it does not

Twenty candidate diagnostics from five families were each rank-correlated with the same target
quantity, the raw thermal transfer AUC over the twenty ordered directions, under one common
pair-based bootstrap.

**Table 5. Transferability diagnostics versus raw thermal transfer, by family.** Spearman ρ against
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

Geographic separation does not order the matrix on either construction: over all twenty directions
the Spearman correlation between centroid separation and transfer is −0.32, and on the
twelve-direction common subset −0.24, both spanning zero. The two nearest directions are among the
worst on the frames as drawn, while the 2,802 km pair returns 0.326 and 0.444, so the transfer mean
of 0.541 is not the value at any one separation.

**Only two diagnostics have intervals excluding zero, and both are conditional**: the sign-agreement
fraction over interval-supported features at ρ = +0.84 [+0.58, +0.88], and its cosine variant at
+0.81. No marginal measure was shown to order the matrix, including area-of-applicability
dissimilarity, climatic distance and geographic distance, and neither were the niche-overlap and
regime families. The learned domain classifier is at ceiling, separating source from target at
AUC ≥ 0.96 for every pair; it always succeeds, which is why it carries no ordering information.

Four limits are stated with the result rather than after it. **Size**: the index's tie structure caps
the achievable Spearman at +0.861, so the observed +0.840 sits on that ceiling, and its exact
one-sided permutation p of 0.0060 is the smallest that structure can produce against a Bonferroni
threshold of 0.0026 over nineteen computed variants — **no outcome of this diagnostic could have
cleared family-wise correction on ten effective pairs**. **Labels**: signed associations need burned
labels in both regions, so the family that appears to work is not available before deployment while
the family that fails is. **Selection**, the sharpest of the three: the two rows that clear zero are
the *supported-feature* variants, whose subset is chosen by whether two regions' bootstrap intervals
happen to be disjoint — a data-dependent selection made on the same data, with no correction. Their
unselected counterparts over all nine features are ρ = +0.50 [−0.17, +0.83] and +0.18 [−0.40, +0.72],
both spanning zero, so the result lives in the selection step and is reported as such.

The families sit on unequal samples — twelve directions for the marginal, applicability, climatic and
geographic rows, sixteen for the supported-conditional rows, twenty for the rest — so every row was
recomputed on the common twelve. Published values reproduce to 4.8 × 10⁻⁵, the conditional rows still
lead at +0.87 [+0.65, +0.88] and +0.85 [+0.43, +0.88], and every marginal row still spans zero. The
ordering is not an artefact of unequal samples.

**A fourth limit, established in Section 4.4, removes the result entirely.** The index is built from
signed associations that Section 4.4 shows to be frame artefacts, and was correlated against transfer
measured on the same frames. Recomputed on an equalised frame it is unanimous, with no variance left
to correlate. Everything in this section is what the original protocol yields; the conclusion that
survives is that **no diagnostic tested here was shown to order transfer once the frames are
comparable**.

## 4.7 Further arms, in brief

Six further arms bear on the findings above without changing them, and are reported in full in
Appendix A. **The contrast pair** (A(s)): the most environmentally similar pair in the matrix is
among the weakest in transfer and the least similar among the stronger, so high envelope overlap
does not buy transfer — an ordinal claim, not one about the endpoints. **Interventions** (A(n)):
pooling four regions into one training set does not recover what single-source transfer loses, and
removing the two reversing predictors costs −0.081 of within-region AUC while returning +0.014
[−0.017, +0.045] on transfer, so a local cost is measured and no compensating transfer gain is.
**Sensitivity** (A(a)–A(h)): eight design choices were varied with everything else held fixed; none
changes a conclusion above, except arm (f), which tests a claim of Section 1.2 and does not uphold
it. **The same geography, a second fire** (A(m)): the one arm that held
place fixed shows a reversal on the frame as drawn, which Section 4.4 withdraws. **Distance**
(A(t)): within a single region the model is already at chance by 10 to 20 km from its training
cells, which bounds how far a surface of this kind can be carried but cannot be turned into an
attribution, for the reason given there. **The price of labels** (A(u)): thirty-two labelled 5 km
blocks recover 85 to 89 % of the target's matched ceiling in three of six directions and 30 to 57 %
in the rest, which is 7 to 20 % of the target's natural-vegetation population and not a cheap
answer. Two limits bound it: at the top budget the selection pool is nearly exhausted, so the narrow
upper-budget intervals reflect saturation rather than precision, and **the labelled blocks are drawn
from the event being predicted, which is not a resource available before that event burns**.
