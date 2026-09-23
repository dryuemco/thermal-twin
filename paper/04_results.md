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
excluded. The separation is not marginal. The five admitted regions carry 0.723 to 0.991, so the
threshold falls in an empty interval rather than between neighbouring cases. That is consistent with
the gate separating natural-fuel combustion from post-harvest stubble burning, which MCD64A1 does not
distinguish, **though one negative control cannot establish it**. North Evia is analysed on an
extended AOI. That leaves the burned scar essentially unchanged while cutting TSG prevalence from
0.676 to 0.287; the effect on transfer is in Appendix A(a).

## 4.2 Within-region: the thermal increment replicates in five regions

Adding the six thermal predictors to the baseline raises spatially blocked out-of-fold ROC-AUC in
every region. The increment's bootstrap interval excludes zero in all five regions at 1 km and at
5 km blocking (Fig. 3), the two scales this design supports as intervals. At 10 km the point
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

*Table note (resampling units).* The bootstrap resamples spatial blocks. An interval's reliability
is therefore bounded by the number of blocks carrying at least one burned cell. Those counts fall
from 192 to 843 at 2 cells to **6 to 33** at 20 cells. An interval built on six such blocks has no
meaningful coverage, so **the 20-cell row should be read as indicative rather than as an
interval**. The 10-cell row is the coarsest blocking this design supports properly. Every region
there has 16 to 70 positive-carrying blocks, and the increment holds at that scale in all five
regions (Appendix A(c)).

The Manavgat rows are computed on the corrected label. It adds burned cells, 784 to 2,935 in the
primary population, and changes no predictor (Section 3.2). The rows strengthen rather than weaken.
Absolute AUCs rise by 0.04 to 0.11 across the three block sizes, and the increment holds at every
scale. The 1 km interval narrows from [+0.055, +0.079] to [+0.060, +0.073], because the region now
carries 814 positive-carrying 2-cell blocks rather than 235.

This within-region result is not itself novel. It is reported because the transfer arms below are
measured against it.

## 4.3 What the evaluation frame is worth, within one region

This section isolates the effect Section 4.4 applies between regions. It comes first because it is
measured on one model in one region with no transfer involved. Nothing the transfer arms do can
therefore explain it (Appendix A(i)).

**Where the skill is lost, on a matched comparison.** Four evaluations are reported. The last three
are scored on **identical cells**, so they differ only in what the model was trained on. The first
shows why an unmatched comparison misleads. The held-out unit is a burned connected component of at
least 50 cells, with all cells within 2 km of it. What makes that harder than a whole region is the
composition of its negatives, not its burned fraction, and that is measured rather than argued. The
same predictions were scored on a random sample of region cells drawn at the scar area's own burned
fraction. That gives **0.793 against the region-wide 0.791**, so matching prevalence changes
nothing, at −0.002 [−0.005, +0.001]. Scoring them on the scar area gives 0.644, a fall of **+0.149
[+0.087, +0.211]**. That swaps both pools at once, so each was swapped singly. Replacing only the
negatives costs **0.139 [0.098, 0.181]**, the whole of it. Replacing only the positives costs
**−0.002 [−0.055, +0.051]**, null on average, though the per-scar effect runs from −0.12 to +0.14.
**The effect is the negative pool.** Every negative in a scar collar is fire-adjacent and shares the
terrain, land cover and synoptic conditions of the positives, whereas a region's negatives include
its easy far field. ROC-AUC is in any case invariant to class balance at fixed class-conditional
distributions (`pool_decomposition.json`).

**Table 2. The four evaluations, scored on identical cells.** Primary natural-vegetation population.
Rows B, C and D are scored on the held-out scar area; row A is the whole region and is shown to make
the mismatch visible. Means and Student *t* intervals are over the seven held-out scars.

| Evaluation | Model trained on | Scored on | Mean AUC | 95 % CI |
|---|---|---|---:|---|
| A. Blocked cross-validation, 5 km | the region, scar included | the whole region | 0.773 | [0.729, 0.818] |
| B. Same blocked model, restricted | the region, **scar included** | the scar area | 0.640 | [0.544, 0.736] |
| C. Leave-one-scar-out | the region, **scar withheld** | the scar area | 0.546 | [0.488, 0.604] |
| D. Foreign region | another region, 306 to 2,802 km | the scar area | 0.553 | [0.495, 0.611] |

All four rows are means over the **same seven scars**. Bejís and Manavgat have no row C, because in
each the burned area is a single component, so withholding it leaves nothing to train on. Under the
corrected label the 2,151 added Manavgat burns merge into its one existing scar (2,934 of 2,935
cells). That is why the controls above are computed on nine scars and report 0.791 and 0.644 against
this table's 0.773 and 0.640. The intervals are Student *t* over the scars. That is this arm's
resampling unit, rather than the spatial-block bootstrap used elsewhere. Four scars are in Muğla, two
in Montiferru and one in Evia. **Row A is a region-level quantity repeated identically across a
region's scars, so its interval is pseudo-replicated and should not be read as coverage.** That
repetition propagates into A − B and A − C. Clustering by region, over three regions, gives
**+0.137 [+0.048, +0.226]** and **+0.266 [−0.022, +0.553]**. The first still excludes zero. The
second no longer does, and is 3.6 times wider. **The scar-level intervals on these two differences
therefore overstate precision, and on the region unit only the frame cost is established**
(Appendix A(i)).

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
positives, this design cannot establish a fire-specific residual, only bound it at about 0.20.** It
is not shown to be zero on an unseen fire; what this design establishes is that it is not
established there. Nor does it establish the fire *event* as the unit, since the held-out patch is
defined by the labels and its identity cannot be separated from its location. Appendix A(z) reports
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
transfer matrix because it changes what Section 4.5 and Appendix A(s) can claim. It withdraws
nothing in Section 4.3, which is what it is built from. Sources are `aoi_frame_auc_frozen_mugla.csv`
and `aoi_frame_transfer_frozen_mugla.csv`, which supersede the pre-correction files for the reason
given below, with `collar_frame_bootstrap.csv` and `diagnostics_collar_frame.csv`. Code is under
`paper/code/`, and the elaboration is in Appendix A(w).

**The five areas of interest are not comparable frames.** Each is a rectangle drawn around a fire,
and they differ by an order of magnitude in how much unburnt far field they enclose. The share of
modelled cells beyond 10 km of any burned cell runs from **2.1 %** in Montiferru to **63.1 %** in
Bejís (Appendix B, Table B6). That far field is not neutral. In Manavgat the median elevation of
modelled cells rises from 330 m within 5 km of the fire to 1,273 m at 20 to 50 km, against 287 m for
the burned cells themselves.

**Under an equalised frame four regions agree, and Manavgat does not.** Restricting every region to
cells within 10 km of any burned cell removes only far-field negatives. Every burned cell is at
distance zero and is retained at any radius, so the protection against a flattering radius is the
sweep, not the retention of positives. On that frame the other four regions agree in sign on
elevation, LST and TVDI, and Manavgat sits on the other side of 0.5 on all three. Its elevation
reversal survives with support: 0.376 [0.300, 0.465] against Muğla's 0.606 [0.525, 0.685] and
Evia's 0.648 [0.550, 0.740]. Under this paper's own criterion from Section 3.10, **two between-region
reversals therefore remain bootstrap-supported under the collar**, both on elevation and both
involving Manavgat. Its thermal channels move toward 0.5 without reversing with support (current LST
0.522 [0.451, 0.591]). At the point estimate, elevation, the three LST channels, TVDI and the two
internally differenced channels therefore all straddle 0.5. The weaker difference instrument that
Table B3's note commits this paper to supports three opposite-sided pairs on `lst_anomaly_mean`, with
the caveats that keep it weak. **The honest statement is that the collar removes every elevation
reversal except Manavgat's, which it leaves supported.** Two scope limits belong with it, both in
Appendix A(l) and A(w). First, the interval criterion was evaluated at the 10 km collar only, though
at the point estimate the 5 and 10 km radii agree. Second, the collar reduces two regions' cell
counts substantially, so part of any loss of support is a loss of power. Features supported in both
regions of a direction average 2.3 per direction on the full frame and 2.2 on the collar.

**The sign most regions share is not the one the dryness framing predicts.** At the point estimates
a hotter pre-fire surface burned *less* in four of five regions. On mutual adjustment temperature
survives where greenness does not, so the absolute channels behave there as static land-surface
descriptors rather than as dryness. Manavgat is the exception. Its burned cells are hotter (current
LST 0.665 on the full frame), and they are also low-lying. Within distance to the nearest burned
cell its LST signal falls to 0.454, so the thermal sign there cannot be separated from its terrain
gradient. In Montiferru the signal is attenuated to near-null. The stratifications, the correlations
and the reciprocal adjustment are in Appendix A(k). Section 5.4 takes up what Manavgat's position
may mean.

**The same test weakens a result of our own, but no longer dissolves it.** Under the frozen label,
the diagnostic that best ordered transfer in our matrix reached ρ = +0.84. That diagnostic is the
sign-agreement fraction over interval-supported features. It is built from exactly these signed AUCs
and was correlated against transfer on the same unequal frames. Under the corrected label it no
longer orders transfer on the frames as drawn (ρ = +0.52 [−0.27, +0.87]; Appendix D). Recomputed
under the collar it is no longer degenerate. It takes the values 0 and 1 across sixteen defined
directions and correlates with collar transfer at ρ = +0.38 (p = 0.15), and its cosine variant at
+0.40 (p = 0.12). The correction that once made it unanimous now leaves it weak on both frames
(`diagnostics_collar_frame.csv`, `collar_increment_and_cosine.csv`).

**Two further arms move with the frame.** The same-geography arm is the most extreme case in the
cohort. A fixed study area is not a fixed evaluation frame, and its 2022 arm has 93.2 % of cells
beyond 10 km of any burned cell, against 55.3 % for 2021. Under the collar its two arms therefore
fall on the same side of 0.5 on elevation, the feature whose reversal we had reported for Muğla. The
claim is scoped. That arm is reconstructed from the 2021 predictors, which are valid for the
year-invariant channels and **not** the seasonal ones. **Only elevation and slope therefore carry a
verdict, on both the Muğla reversal is removed, and on the thermal channels the arm is silent.** It
rests on eleven positive-carrying blocks against a floor of sixteen (Appendices A(m), A(o)). The
within-region increment, by contrast, **survives**, positive in all five regions at a mean of +0.083
against +0.087 as drawn.

**The transfer matrix moves as well.** Restricting source and target to the same collar:

**Table 3. Cross-region transfer under equalised evaluation frames.** Primary natural-vegetation
population, thermal model, twenty ordered directions per row. Above/below chance are point counts.
The supported counts use a 10-cell (≈5 km) spatial-block bootstrap on the target, 1000 replicates,
seed 42. **Table B9 reports the same matrix under 2-cell (≈1 km) blocking**, which is why its
supported counts are the larger 11 and 7 (Section 4.5). Per-direction bounds are in
`aoi_frame_transfer_frozen_mugla.csv`.

| Source frame | Target frame | Mean target AUC | Above chance | Below chance | Supported above / below | Paired thermal delta |
|---|---|---:|---:|---:|---:|---:|
| full | full (**Table B9**) | 0.527 | 13 of 20 | **7** | 9 / **6** | +0.007 |
| full | 10 km | 0.559 | 14 of 20 | 6 | 10 / 2 | +0.008 |
| 10 km | full | 0.546 | 14 of 20 | 6 | 10 / 5 | +0.014 |
| **10 km** | **10 km** | **0.589** | **15 of 20** | **5** | **13 / 2** | **+0.024** |
| 5 km | 5 km | 0.591 | 16 of 20 | 4 | 11 / 0 | +0.017 |

**A data-provenance defect in this arm was found and corrected.** One region's predictor file at the
canonical path had come to differ from the one the frozen tables were computed on, so every arm here
was re-run against the frozen export. The correction moves forty of a hundred per-direction values by
up to 0.022. It leaves **every headline quantity above unchanged to within 0.0012**, and the signed
AUCs of that region's two channels move by at most 0.008, with no verdict changing (Appendix A(w)).
The table reports the corrected values, and reproduces Table B9's as-drawn mean of 0.527 and 13 of
20. **The baseline control must be restated on this frame.** The static baseline transfers at 0.565
against 0.589, a paired difference of +0.024 rather than +0.007. The control therefore holds in kind,
but the gap is about three times larger once frames are comparable, and about twice as large at the
5 km collar.

**What this settles, and what it leaves standing.** Four quantities reported below are properties of
the frames rather than of the predictor-burning relationship, and are identified as such where they
appear. They are the count of below-chance directions, which falls from seven to five; the
sign-agreement diagnostic; the same-geography arm; and the paired thermal contribution, +0.007 as
drawn against +0.024 equalised. One is not: Manavgat's elevation reversal, which the collar leaves
supported. The paired contribution carries the portability null, so it is given an interval on the
frame this section argues for: **+0.024 [−0.004, +0.049]** under the pair-cluster resampling of
Appendix A(o). It still spans zero, so the null survives the correction, but only just. Under the
alternative admissible unit, clustering by target region, it does not ([+0.011, +0.040]; Appendix
A(w)). What survives is the central negative result, and its size must be stated on a matched
comparison. Setting 0.589 against a within-region reference of about 0.90 would compare a collar
number with a full-rectangle one at 1 km blocking. Recomputed on the same frame at 5 km blocking,
that reference is 0.786. The shortfall is therefore **+0.197 [+0.091, +0.303]**, a Student *t*
interval over the five target regions rather than the spatial-block bootstrap used elsewhere.
Manavgat contributes the largest per-region shortfall to it (+0.319; Appendix A(w)). The shortfall
is real, and it is 0.197 rather than the 0.29 an unmatched comparison implies. Appendix C.5(ix)
records the frame as a limitation of this cohort rather than of the method.

## 4.5 Cross-region transfer, and what label-free adaptation does to it

**Everything in this section is computed on the frames as drawn and should be read against Section
4.4.** That section has shown the frames are not comparable, and that the within-region reference
used here is itself frame-dependent. The as-drawn matrix is reported because it is what the original
analysis protocol yields. Per-direction values are in Appendix B, Table B9, and the supporting arms
in Appendix A(ix).

**Raw transfer is heterogeneous and includes anti-predictive directions.** Target AUC spans 0.314 to
0.677, and Fig. 4 gives the matrix direction by direction. The support counts depend on the blocking
scale, so both are reported. At 2-cell (≈1 km) blocking, eleven of twenty directions are above chance
with interval support and seven below. At the 10-cell (≈5 km) blocking this design defends, nine are
above and six below with five uncertain; these are the counts Table 3 uses. Of the below-chance
directions, two keep interval support after frame equalisation, Manavgat to Bejís and Muğla to
Manavgat. Across five bootstrap seeds every 2-cell verdict is stable. At 10 cells, one level verdict
and two paired-delta verdicts are not (`transfer_ci_blocksize.csv`). Even the best raw transfer sits
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
recomputed on the collar (Appendix B, Table B4).

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
to [−0.028, +0.045], and none propagates within-direction sampling variability. The
leave-one-region-out jackknife shows the mean is not carried by any single region. Dropping one
region at a time moves it between +0.001 (without Evia) and +0.015 (without Manavgat), and never
reverses its sign.

**Label-blind adaptation compresses the matrix toward chance rather than repairing it** (Fig. 5).
Under region-wise z-scoring the twenty directions span 0.302 to 0.630, and under CORAL 0.406 to
0.624. Sixteen of twenty move closer to chance, which helps the directions that failed and harms
those that worked. The committed-in-advance CORAL arm averages **0.517**. Taking whichever method
scores better per direction gives 0.523, but that selection uses the target labels the protocol
forbids. It is therefore **an oracle upper bound rather than an achievable result**. Even the oracle
stays below the reference a model reaches on an unseen scar (Section 4.3, row C, 0.546). Alignment is
thus regressing the matrix toward that reference rather than exceeding it. A sign reversal is not a
distribution mismatch that realigning inputs would repair. Appendix A(ix) reports the recovery
fractions, including the seven directions with *negative* recovery.

## 4.6 Further arms

Six further arms bear on the findings above without changing them. They are the contrast pair
(A(s), Fig. 8), the two interventions (A(n)), the sensitivity summary (A(v)), the same-geography two-event
arm (A(m)), the distance curve (A(t)) and the label-budget curve (A(u)). Each is stated there with
its own limits. Two are plotted here because the shape of the result is the argument. Pooling every
other region never beats the best single source for any target (Fig. 6). Removing the
direction-reversing features costs within-region skill and returns nothing measurable on transfer
(Fig. 7).

Two arms bear directly on Sections 5.3 and 5.6. The first is the interventions. There a local cost
of −0.076 is measured against a transfer return of +0.014 [−0.028, +0.056], whose interval spans
zero. The two removed features were fixed from the frozen label's supported reversals, and are kept,
not re-selected. The second is the label budget. Thirty-two labelled 5 km blocks recover 83 to 89 %
of the target's matched ceiling in three of six directions, and 30 to 52 % in the rest. Those blocks
are 7 to 20 % of the target's population, drawn from the event being predicted, which is not a
resource available before that event burns.

No diagnostic among the twenty fixed in advance orders transfer with an interval excluding zero
(Appendix D). One of them, the supported-feature vector Spearman, is defined on only six directions
and was not evaluated as a diagnostic.
