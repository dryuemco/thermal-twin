# 4. Results

> **Rewritten 2026-08-14 in the split.** This section was 14,841 words and fifteen tables. It now
> reports the four contributions of Section 1.4 and the evidence they rest on, in six tables. The
> sensitivity analyses of the observational layer moved to the companion paper; the remaining
> supporting tables move to the supplement. Every table below is carried verbatim from the
> pre-split text, so no number was retyped.
>
> **Updated 2026-09-23 for the corrected Manavgat label (Section 3.2).** Every Manavgat-dependent
> quantity now comes from the re-frozen outputs; the item-by-item log is
> `paper/labelfix_rerun/round5/E1_CHANGELIST.md` §1–§13. Three statements of the frozen text no
> longer hold and are rewritten rather than softened: that the collar leaves no supported reversal,
> that hotter surfaces burned less in every region, and that the collar dissolves the conditional
> diagnostic (all §4.4).
>
> **A separate, pre-existing error, independent of the label correction.** §4.4 printed that features
> supported in both regions "rise from 1.20 to 3.40 per direction". The frozen artefacts themselves
> give **1.40**, not 1.20: `diagnostics_collar_frame.csv` in `canonical_rerun`, and the Step9G-based
> count in `conditional_similarity_transfer.json`, both 1.40 over twenty directions. The printed 1.20
> was wrong under the frozen label too. The corrected values are 2.3 (full frame) and 2.2 (collar).
>
> **Style pass 2026-09-23.** Long sentences were split to bring this section into the band of
> Sections 5 and 6. No number, interval, hedge or claim changed; `check_numbers` confirms the
> numbers.

## 4.1 Study regions and the admissibility gate

All five candidate regions pass the burned-landcover gate, and the negative control fails it as
intended. Kozan 2023 returns a natural-vegetation fraction of 0.017 against the 0.50 threshold and is
excluded.  The five admitted regions carry 0.723 to 0.991, so the
threshold falls in an empty interval rather than between neighbouring cases. That is consistent with
the gate separating natural-fuel combustion from post-harvest stubble burning, which MCD64A1 does not
distinguish, **though one negative control cannot establish it**. North Evia is analysed on an
extended AOI. That leaves the burned scar essentially unchanged while cutting TSG prevalence from
0.676 to 0.287; the effect on transfer is in Section S1.1.

## 4.2 Within-region: the thermal increment replicates in five regions

Adding the six thermal predictors to the baseline raises spatially blocked out-of-fold ROC-AUC in
every region. The increment's bootstrap interval excludes zero in all five regions at 1 km and at
5 km blocking (Fig. 3; Table 1), the two scales this design supports as intervals. At 10 km the point
estimates hold, from +0.047 to +0.154. They rest on 6 to 33 positive-carrying blocks, however, and
are indicative.

**Table 1. Within-region baseline versus thermal performance and block-size robustness.** Primary
(TSG) population; spatially blocked 5-fold CV (Section 3.7); paired spatial-block bootstrap, 1000
replicates. Block sizes 2/10/20 cells ≈ 1/5/10 km. Baseline and Thermal columns are ROC-AUC; the
95 % CI belongs to ΔAUC.

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

*Table note (resampling units).* The 10-cell row, with 16
to 70 positive-carrying blocks in every region, is the coarsest blocking this design supports
properly. The block counts and the coverage argument are in Section S1.3, *Table 1 note (resampling
units)*.

The Manavgat rows are computed on the corrected label (Section 3.2). The rows strengthen rather than
weaken; the change row by row is in Section S3.1.3.



## 4.3 What the evaluation frame is worth, within one region

This section isolates, on one model in one region, the effect Section 4.4 applies between regions.
No transfer is involved, so nothing the transfer arms do can explain it (Section S1.9).

**Where the skill is lost, on a matched comparison.** Four evaluations are reported (Table S1). The last three are scored on **identical cells**, so they differ only in what the model was
trained on. The first shows why an unmatched comparison misleads. The held-out unit is a burned
connected component of at least 50 cells, with all cells within 2 km of it. What makes that harder
than a whole region is the composition of its negatives, not its burned fraction. Matching
prevalence changes nothing, at −0.002 [−0.005, +0.001]. Scoring the same predictions on the scar
area costs **+0.149 [+0.087, +0.211]**, and replacing only the negatives costs **0.139 [0.098,
0.181]**, the whole of it. **The effect is the negative pool.** The single-pool controls are in
Section S1.9.1.



All four rows are means over the **same seven scars**, four in Muğla, two in Montiferru and one in
Evia, with Student *t* intervals over the scars. **Row A is a region-level quantity repeated
identically across a region's scars, so its interval is pseudo-replicated and should not be read as
coverage.** Clustering by region, over three regions, gives **+0.137 [+0.048, +0.226]** for A − B and
**+0.266 [−0.022, +0.553]** for A − C. **On the region unit only the frame cost is established**
(Section S1.9.2).

**The same model, scored two ways on the same region, differs by 0.133 AUC.** Rows A and B are one
model and one set of out-of-fold predictions. The only change is which cells they are scored on.
That change alone costs **0.133 [+0.059, +0.207]** of the 0.227 [+0.147, +0.308] fall from A to C,
about three fifths. That is a ratio of two estimates, so the point is the size of the numerator
rather than the precision of the fraction. It is the size of the predictor-block increments this
design itself measures. A region-wide blocked figure is therefore an upper bound on what the same
model achieves where the fire actually is.

**Neither withholding the fire nor moving 2,800 km has a measurable cost.** B minus C, the
fire-specific residual on identical cells, is **+0.094 [−0.012, +0.200]**. C minus D, the effect of
replacing a same-region model with one fitted 306 to 2,802 km away, is **−0.007 [−0.070, +0.057]**.
Both span zero and both arms sit close to chance. **With seven scars, two of them starved of
positives, this design cannot establish a fire-specific residual, only bound it at about 0.20.** Nor does it establish the fire *event* as the unit, since the held-out patch is
defined by the labels and its identity cannot be separated from its location. Section S1.23 reports
the spread behind row D, and the sweeps showing that the patch definition does not drive the result.

**The increment declines with the holdout, and is not established once the fire is withheld.**
Contribution 2 concerns the paired thermal-minus-baseline difference, so the same evaluations were
run on it. It is +0.056 to +0.153 under blocked cross-validation, with every interval above zero. It
is +0.028 on a within-region half-split, **+0.024 [−0.040, +0.089]** under leave-one-scar-out, and
+0.007 [−0.021, +0.037] across regions. The point estimate falls monotonically as the holdout
hardens, and the last two intervals span zero. **The within-region increment is therefore
substantially a property of interleaved holdout**.

## 4.4 The same effect between regions, applied to our own matrix

Section 4.3's effect applies with equal force between regions. This test is reported before the
transfer matrix because it changes what Section 4.5 and Section S1.16 can claim. It withdraws
nothing in Section 4.3, which is what it is built from. Sources, code and the elaboration are in
Section S1.20.

**The five areas of interest are not comparable frames.** Each is a rectangle drawn around a fire,
and they differ by an order of magnitude in how much unburnt far field they enclose. The share of
modelled cells beyond 10 km of any burned cell runs from **2.1 %** in Montiferru to **63.1 %** in
Bejís (Table S13). That far field is not neutral. In Manavgat the median elevation of
modelled cells rises from 330 m within 5 km of the fire to 1,273 m at 20 to 50 km, against 287 m for
the burned cells themselves.

**Under an equalised frame four regions agree, and Manavgat does not.** Restricting every region to
cells within 10 km of any burned cell removes only far-field negatives. On that frame the other four
regions agree in sign on elevation, LST and TVDI, and Manavgat sits on the other side of 0.5 on all
three. Its elevation reversal survives with support: 0.376 [0.300, 0.465] against Muğla's 0.606
[0.525, 0.685] and Evia's 0.648 [0.550, 0.740]. Under this paper's own criterion from Section 3.10,
**two between-region reversals therefore remain bootstrap-supported under the collar**, both on
elevation and both involving Manavgat. Its thermal channels move toward 0.5 without reversing with
support (current LST 0.522 [0.451, 0.591]). **The honest statement is that the collar removes every
elevation reversal except Manavgat's, which it leaves supported.** The difference instrument, the two
scope limits and the supported-feature counts are in Section S1.20, *Under an equalised frame four
regions agree, and Manavgat does not*.

**The sign most regions share is not the one the dryness framing predicts.** At the point estimates
a hotter pre-fire surface burned *less* in four of five regions. On mutual adjustment temperature
survives where greenness does not, so the absolute channels behave there as static land-surface
descriptors rather than as dryness. Manavgat is the exception. Its burned cells are hotter (current
LST 0.665 on the full frame), and they are also low-lying. Within distance to the nearest burned
cell its LST signal falls to 0.454, so the thermal sign there cannot be separated from its terrain
gradient. In Montiferru the signal is attenuated to near-null. The stratifications, the correlations
and the reciprocal adjustment are in Section S1.11. 

**The same test weakens a result of our own, but no longer dissolves it.** Under the frozen label,
the diagnostic that best ordered transfer in our matrix reached ρ = +0.84. That diagnostic is the
sign-agreement fraction over interval-supported features. It is built from exactly these signed AUCs
and was correlated against transfer on the same unequal frames. Under the corrected label it no
longer orders transfer on the frames as drawn (ρ = +0.52 [−0.27, +0.87]; Section S4). Recomputed
under the collar it is no longer degenerate. It takes the values 0 and 1 across sixteen defined
directions and correlates with collar transfer at ρ = +0.38 (p = 0.15). The correction that once made it unanimous
now leaves it weak on both frames (its cosine variant and sources in Section S1.20).

**Two further arms move with the frame.** The same-geography arm is the most extreme case in the
cohort: its 2022 arm has 93.2 % of cells beyond 10 km of any burned cell, against 55.3 % for 2021.
**Only elevation and slope carry a verdict there, on both the Muğla reversal is removed, and on the
thermal channels the arm is silent.** It rests on eleven positive-carrying blocks against a floor of
sixteen (Section S1.20). The within-region increment, by contrast, **survives**, positive in all
five regions at a mean of +0.083 against +0.087 as drawn.





**The transfer matrix moves as well** (Table S8), from 0.527 as drawn to 0.589 on the
10 km collar. A data-provenance defect in this arm was found and corrected; every arm here reads
each region's predictor file by its recorded SHA-256 (Section S1.20). **The baseline control must be
restated on this frame.** The static baseline transfers at 0.565 against 0.589, a paired difference
of +0.024 rather than +0.007. The control therefore holds in kind, but the gap is about three times
larger once frames are comparable, and about twice as large at the 5 km collar.

**What this settles, and what it leaves standing.** Four quantities reported below are properties of
the frames rather than of the predictor-burning relationship, and are identified as such where they
appear. They are the count of below-chance directions, which falls from seven to five; the
sign-agreement diagnostic; the same-geography arm; and the paired thermal contribution, +0.007 as
drawn against +0.024 equalised. One is not: Manavgat's elevation reversal, which the collar leaves
supported. The paired contribution carries the portability null, so it is given an interval on the
frame this section argues for: **+0.024 [−0.004, +0.049]** under the pair-cluster resampling of
Section S1.15. It still spans zero, so the null survives the correction, but only just. Under the
alternative admissible unit, clustering by target region, it does not ([+0.011, +0.040]; Section S1.20). What survives is the central negative result, and its size must be stated on a matched
comparison. Setting 0.589 against a within-region reference of about 0.90 would compare a collar
number with a full-rectangle one at 1 km blocking. Recomputed on the same frame at 5 km blocking,
that reference is 0.786. The shortfall is therefore **+0.197 [+0.091, +0.303]**, a Student *t*
interval over the five target regions rather than the spatial-block bootstrap used elsewhere.
Manavgat contributes the largest per-region shortfall to it (+0.319), and the unmatched comparison
of 0.29 is in Section S1.20. Section S3.5(ix) records the frame as a limitation of this cohort.

## 4.5 Cross-region transfer, and what label-free adaptation does to it

**Everything in this section is computed on the frames as drawn and should be read against Section
4.4.** The as-drawn matrix is reported because it is what the original
analysis protocol yields. Per-direction values are in Table S16, and the supporting arms
in Section S1.21.

**Raw transfer is heterogeneous and includes anti-predictive directions.** Target AUC spans 0.314 to
0.677, and Fig. 4 gives the matrix direction by direction. The support counts depend on the blocking
scale, so both are reported. At 2-cell (≈1 km) blocking, eleven of twenty directions are above chance
with interval support and seven below. At the 10-cell (≈5 km) blocking this design defends, nine are
above and six below with five uncertain; these are the counts Table S8 uses. Of the below-chance
directions, two keep interval support after frame equalisation, Manavgat to Bejís and Muğla to
Manavgat. Seed stability is in Section S1.21. Even the best raw transfer sits
far below the target's own within-region skill: Evia to Manavgat reaches 0.677 against Manavgat's
0.908. The raw deficit runs from 0.231 to 0.594, against a reference that Section 4.3 shows is not
matched to a transfer evaluation.

**Manavgat is the weakest target in the matrix**, at a mean of 0.435 over its four incoming
directions against 0.494 to 0.572 for the other targets. It is not the weakest source (0.502,
against 0.477 for Bejís). Three of its incoming directions lie between 0.314 and 0.404, while Evia to
Manavgat reaches 0.677. An exploratory split by fire phase suggests where the collapse sits; it was
not registered, and it concerns one region and one event. The corrected label's added cells burned
on 28–31 July, the fire's first four days, and the remaining 784 later. Transfer into the early cells
is lower than into the later ones in every direction: Bejís 0.276 against 0.419, Montiferru 0.351
against 0.549, Muğla 0.332 against 0.382, and Evia 0.667 against 0.704. The early cells also lie far
lower, at a median of 219 m against 512 m for the later burns and 1,004 m for unburned cells
(`paper/labelfix_rerun/round5/s4b_*`). Section 5.4 treats this as a mechanism proposal, not as
evidence.

**In precision terms it is worse than the ROC figures suggest.** A susceptibility surface is used as
a ranked area budget, so precision-recall is the operational quantity. PR-AUC averages **0.181
against a no-skill baseline of 0.157**. **Seven of twenty directions fall below their own baseline at
the point estimate, all seven with intervals entirely below it.** Only one direction, Evia to
Manavgat, exceeds twice its baseline. These are frame-as-drawn quantities, and the PR arm was not
recomputed on the collar (Table S11).

**The static baseline does not transfer either**, at a mean of **0.519** against **0.527** for the
thermal model. The failure is therefore not specific to the dynamic block. A baseline that does not
travel, plus pre-fire thermal state, gives a model that does not travel. Section 4.4 restates this
control on the equalised frame, where it is 0.565 against 0.589.

**The thermal block's paired contribution is +0.007, and the mean is not the informative statistic.**
The individual contributions span **−0.148 to +0.133**, twelve positive and eight negative. The
largest is about twenty times the mean, and the sign belongs to the pair rather than to the block. A
mean near zero records cancellation, not consistent absence of effect. The directions are not
independent, since each region appears in eight of the twenty, so the interval depends on the
resampling unit. **All four units the design permits give the same answer**, from [−0.018, +0.033]
to [−0.028, +0.045], and none propagates within-direction sampling variability.  A leave-one-region-out jackknife never reverses its sign (Section S1.21).

**Label-blind adaptation compresses the matrix toward chance rather than repairing it** (Fig. 5).
Under region-wise z-scoring the twenty directions span 0.302 to 0.630, and under CORAL 0.406 to
0.624. Sixteen of twenty move closer to chance, which helps the directions that failed and harms
those that worked. Closer is measured as distance from 0.5, so it does not mean the matrix stays on
one side of chance. Evia to Manavgat overshoots, falling from 0.677 to 0.404 under z-scoring and
0.417 under CORAL, below chance on the other side. The committed-in-advance CORAL arm averages **0.517**. Taking whichever method
scores better per direction gives 0.523, but that selection uses the target labels the protocol
forbids. It is therefore **an oracle upper bound rather than an achievable result**. Even the oracle
stays below the reference a model reaches on an unseen scar (Table S1, row C, 0.546). A sign reversal is not a
distribution mismatch that realigning inputs would repair. Section S1.10 reports the recovery
fractions, including the seven directions with *negative* recovery, five of them with intervals
entirely below zero.

## 4.6 Further arms

Six further arms bear on the findings above without changing them. They are the contrast pair
(Section S1.16, Fig. 8), the two interventions (Section S1.14), the sensitivity summary (Section S1.17), the
same-geography two-event arm (Section S1.13), the distance curve (Section S1.18) and the label-budget
curve (Section S1.19). Each is stated there with
its own limits. Pooling every other region does not beat the best single source for four of five
targets; for Evia the pooled model exceeds it (0.715 [0.668, 0.757] against 0.654; Fig. 6).
Removing the direction-reversing features costs −0.076 within region and returns nothing measurable
on transfer, +0.014 [−0.028, +0.056] (Fig. 7). The two removed features were fixed from the frozen
label's supported reversals, and are kept, not re-selected. Thirty-two labelled 5 km blocks recover 83 to 89 %
of the target's matched ceiling in three of six directions, and 30 to 52 % in the rest. Those blocks
are 7 to 20 % of the target's population, drawn from the event being predicted, which is not a
resource available before that event burns.

No diagnostic among the twenty fixed in advance orders transfer with an interval excluding zero
(Section S4). One of them, the supported-feature vector Spearman, is defined on only six directions
and was not evaluated as a diagnostic.
