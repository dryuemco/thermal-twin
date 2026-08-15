# 4. Results

> **Rewritten 2026-08-14 in the split.** This section was 14,841 words and fifteen tables. It now
> reports the four contributions of Section 1.4 and the evidence they rest on, in six tables. The
> sensitivity analyses of the observational layer moved to the companion paper; the remaining
> supporting tables move to the supplement. Every table below is carried verbatim from the
> pre-split text, so no number was retyped.

## 4.1 Study regions and the admissibility gate

All five candidate regions pass the burned-landcover gate and the negative control fails it as
intended: Kozan 2023 returns a natural-vegetation fraction of 0.017 against the 0.50 threshold and is
excluded. The separation is not marginal, the five admitted regions carrying 0.723 to 0.991, so the
threshold falls in an empty interval rather than between neighbouring cases. That is consistent with
the gate separating natural-fuel combustion from post-harvest stubble burning, which MCD64A1 does not
distinguish, **though one negative control cannot establish it**. North Evia is analysed on an
extended AOI, which leaves the burned scar essentially unchanged while cutting TSG prevalence from
0.676 to 0.287; the effect on transfer is in Appendix A(a).

## 4.2 Within-region: the thermal increment replicates in five regions

Adding the six thermal predictors to the baseline raises spatially blocked out-of-fold ROC-AUC in
every region, the increment's bootstrap interval excluding zero in all five at 1 km and at 5 km
blocking (Fig. 3) — the two scales this design supports as intervals. At 10 km the point estimates
hold, from +0.048 to +0.154, but rest on 6 to 33 positive-carrying blocks and are indicative.

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

*Table note (resampling units).* The bootstrap resamples spatial blocks, so an interval's
reliability is bounded by the number of blocks carrying at least one burned cell, and those counts
fall from 192 to 843 at 2 cells to **6 to 33** at 20 cells. An interval built on six such blocks has
no meaningful coverage, so **the 20-cell row should be read as indicative rather than as an
interval**. The 10-cell row is the coarsest blocking this design supports properly, every region
there having 16 to 70 positive-carrying blocks, and the increment holds at that scale in all five
regions (Appendix A(c)).

This within-region result is not itself novel; it is reported because the transfer arms below are
measured against it.

## 4.3 What the evaluation frame is worth, within one region

This section isolates the effect Section 4.4 applies between regions. It comes first because it is
measured on one model in one region with no transfer involved, so nothing the transfer arms do can
explain it (Appendix A(i)).

**Where the skill is lost, on a matched comparison.** Four evaluations are reported; the last three
are scored on **identical cells**, so they differ only in what the model was trained on, and the
first shows why an unmatched comparison misleads. The held-out unit is a burned connected component
of at least 50 cells with all cells within 2 km of it. What makes that harder than a whole region is
the composition of its negatives, not its burned fraction, and that is measured rather than argued.
Scoring the same predictions on a random sample of region cells drawn at the scar area's own burned
fraction gives **0.782 against the region-wide 0.782**, so matching prevalence changes nothing, at
−0.000 [−0.003, +0.002]; scoring them on the scar area gives 0.627, a fall of **+0.155
[+0.093, +0.217]**. That swaps both pools at once, so each was swapped singly: replacing only the
negatives costs **0.147 [0.104, 0.191]**, the whole of it, and replacing only the positives costs
**0.002 [−0.052, +0.048]**, null on average though the per-scar effect runs from −0.12 to +0.12.
**The effect is the negative pool** — every negative in a scar collar is fire-adjacent, sharing the
terrain, land cover and synoptic conditions of the positives, whereas a region's negatives include
its easy far field — and ROC-AUC is in any case invariant to class balance at fixed class-conditional
distributions (`pool_decomposition.json`).

**Table 2. The four evaluations, scored on identical cells.** Primary natural-vegetation population.
Rows B, C and D are scored on the held-out scar area; row A is the whole region and is shown to make
the mismatch visible. Means and Student *t* intervals are over the eight held-out scars.

| Evaluation | Model trained on | Scored on | Mean AUC | 95 % CI |
|---|---|---|---:|---|
| A. Blocked cross-validation, 5 km | the region, scar included | the whole region | 0.776 | [0.738, 0.814] |
| B. Same blocked model, restricted | the region, **scar included** | the scar area | 0.634 | [0.552, 0.716] |
| C. Leave-one-scar-out | the region, **scar withheld** | the scar area | 0.552 | [0.501, 0.602] |
| D. Foreign region | another region, 306 to 2,802 km | the scar area | 0.555 | [0.495, 0.616] |

All four rows are means over the **same eight scars**, and Bejís has no row C because it is its
region's only component of any size, which is why the controls above are computed on nine and report
0.782 and 0.627 against this table's 0.776 and 0.634. The intervals are Student *t* over the scars,
this arm's resampling unit rather than the spatial-block bootstrap used elsewhere. Four scars are in
Muğla and two in Montiferru, and **row A is a region-level quantity repeated identically across a
region's scars, so its interval is pseudo-replicated and should not be read as coverage**. That
repetition propagates into A − B and A − C; clustering by region gives **+0.155 [+0.082, +0.228]**
and **+0.251 [+0.093, +0.409]**, both still excluding zero but the second 2.3 times wider, so **the
scar-level intervals on these two differences overstate precision** (Appendix A(i)).

**The same model, scored two ways on the same region, differs by 0.143 AUC.** Rows A and B are one
model and one set of out-of-fold predictions; the only change is which cells they are scored on.
That change alone costs **0.143 [+0.077, +0.208]** of the 0.225 [+0.157, +0.293] fall from A to C,
about two thirds — a ratio of two estimates, compatible with anything from roughly a third to nine
tenths, so the point is the size of the numerator rather than the precision of the fraction. It is
the size of the predictor-block increments this design itself measures, so a region-wide
blocked figure is an upper bound on what the same model achieves where the fire actually is.

**Neither withholding the fire nor moving 2,800 km has a measurable cost.** B minus C, the
fire-specific residual on identical cells, is **+0.082 [−0.011, +0.175]**; C minus D, the effect of
replacing a same-region model with one fitted 306 to 2,802 km away, is **−0.003 [−0.075, +0.069]**.
Both span zero and both arms sit close to chance, so **with eight scars, three of them starved of
positives, this design cannot establish a fire-specific residual, only bound it at about 0.18.** It
is not shown to be zero on an unseen fire; what this design establishes is that it is not established
there. Nor does it establish the fire *event* as the unit, since the held-out patch is defined by the
labels and its identity cannot be separated from its location. Appendix A(z) reports the spread
behind row D and the sweeps showing the patch definition does not drive the result.

**The increment declines with the holdout, and is not established once the fire is withheld.**
Contribution 1 is about the paired thermal-minus-baseline difference, so the same evaluations were
run on it: +0.056 to +0.153 under blocked cross-validation with every interval above zero, +0.027 on
a within-region half-split, **+0.022 [−0.032, +0.077]** under leave-one-scar-out, and +0.004
[−0.028, +0.036] across regions. The point estimate falls monotonically as the holdout hardens and
the last two intervals span zero, so **the within-region increment is substantially a property of
interleaved holdout**.

## 4.4 The same effect between regions, applied to our own matrix

Section 4.3's effect applies with equal force between regions. This test is reported before the
transfer matrix because it changes what Section 4.5 and Appendix A(s) can claim; it withdraws nothing
in Section 4.3, which is what it is built from. Sources are `aoi_frame_auc_frozen_mugla.csv` and
`aoi_frame_transfer_frozen_mugla.csv`, which supersede the pre-correction files for the reason given
below, with `collar_frame_bootstrap.csv` and `diagnostics_collar_frame.csv`; code is under
`paper/code/` and the elaboration in Appendix A(w).

**The five areas of interest are not comparable frames.** Each is a rectangle drawn around a fire,
and they differ by an order of magnitude in how much unburnt far field they enclose: the share of
modelled cells beyond 10 km of any burned cell runs from **2.1 %** in Montiferru to **63.1 %** in
Bejis (Appendix B, Table B6). That far field is not neutral — in Manavgat the median elevation of
modelled cells rises from 472 m within 5 km of the fire to 1,273 m at 20 to 50 km, against 512 m for
the burned cells themselves.

**Under an equalised frame the sign reversals do not survive.** Restricting every region to cells
within 10 km of any burned cell removes only far-field negatives — every burned cell is at distance
zero and is retained at any radius — so the protection against a flattering radius is the sweep, not
the retention of positives. On that frame all five regions agree in sign on elevation, LST and TVDI,
and both bootstrap-supported elevation reversals of Table B3 disappear. Under this paper's own
criterion from Section 3.10, **no between-region reversal remains bootstrap-supported**: the two
features straddling 0.5 at the point estimate are the internally differenced channels, and in each at
least one region's interval covers 0.5 — Evia's by 0.003. The weaker difference instrument that
Table B3's note commits this paper to does support four opposite-sided pairs on `lst_anomaly_mean`,
with three caveats that keep it weak. **The honest statement is that no between-region reversal meets
the strict criterion under the collar, and that the LST anomaly differs between regions on the weaker
one.** Two scope limits belong with it, both in Appendix A(l) and A(w): the interval criterion was
evaluated at the 10 km collar only, though at the point estimate the two radii agree exactly; and the
collar reduces two regions' cell counts substantially, so part of the loss of support is a loss of
power, against which features supported in both regions *rise* from 1.20 to 3.40 per direction.

**The sign they now agree on is not the one the dryness framing predicts**: at the point estimates a
hotter pre-fire surface burned *less* in every region, and on mutual adjustment temperature survives
where greenness does not, so the absolute channels behave here as static land-surface descriptors
rather than as dryness. Within distance to the nearest burned cell the sign crosses 0.5 in Manavgat
and is attenuated to near-null in Montiferru, so in those two it is largely the residual spatial
gradient the collar was introduced to remove. The stratifications, the correlations and the
reciprocal adjustment are in Appendix A(k).

**The same test determines what the diagnostics of Section 4.6 can establish.** Both candidates
there with intervals excluding zero measure agreement in the sign of each predictor's association
between source and target — built from exactly the signed AUCs shown above to be frame artefacts,
and correlated against transfer on the same unequal frames. Recomputing both sides under the
collar:

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

The two fail differently and both fail: the agreement fraction has no variance left once every pair
agrees, and the supported cosine keeps a trace of variance but stops tracking transfer. The
disagreements they were reading were the far fields. **Only these two were recomputed, so the other
eighteen are unknown against the equalised transfer vector rather than shown to be null**
(Appendix A(o)). This settles what Contribution 3 can claim: **no diagnostic tested here has been
shown to order transfer**, and the two that appeared to were reading how the rectangles were drawn.

**Two further arms move with the frame.** The same-geography arm is the most extreme case in the
cohort — a fixed study area is not a fixed evaluation frame, and its 2022 arm has 93.2 % of cells
beyond 10 km of any burned cell against 55.3 % for 2021 — so under the collar its two arms fall on
the same side of 0.5 on elevation, the feature whose reversal we had reported. The claim is scoped:
that arm is reconstructed from the 2021 predictors, valid for the year-invariant channels and **not**
the seasonal ones, so **only elevation and slope carry a verdict, on both the reversal is removed,
and on the thermal channels the arm is silent**; it rests on eleven positive-carrying blocks against
a floor of sixteen (Appendices A(m), A(o)). The within-region increment, by contrast, **survives**,
positive in all five regions at a mean of +0.077 against +0.086 as drawn.

**The transfer matrix moves as well.** Restricting source and target to the same collar:

**Table 4. Cross-region transfer under equalised evaluation frames.** Primary natural-vegetation
population, thermal model, twenty ordered directions per row. Above/below chance are point counts;
the supported counts use a 10-cell (≈5 km) spatial-block bootstrap on the target, 1000 replicates,
seed 42; **Table B9 reports the same matrix under 2-cell (≈1 km) blocking**, which is why its
supported counts are the larger 12 and 6 (Section 4.5). Per-direction bounds are in `aoi_frame_transfer_frozen_mugla.csv`.

| Source frame | Target frame | Mean target AUC | Above chance | Below chance | Supported above / below | Paired thermal delta |
|---|---|---:|---:|---:|---:|---:|
| full | full (**Table B9**) | 0.541 | 14 of 20 | **6** | 9 / **4** | +0.004 |
| full | 10 km | 0.576 | 17 of 20 | 3 | 11 / 1 | +0.003 |
| 10 km | full | 0.570 | 17 of 20 | 3 | 11 / 3 | +0.014 |
| **10 km** | **10 km** | **0.616** | **19 of 20** | **1** | **15 / 1** | **+0.023** |
| 5 km | 5 km | 0.608 | 19 of 20 | 1 | 12 / 0 | +0.014 |

**A data-provenance defect in this arm was found and corrected**: one region's predictor file at the
canonical path had come to differ from the one the frozen tables were computed on, so every arm here
was re-run against the frozen export. It moves forty of a hundred per-direction values by up to
0.022 and leaves **every headline quantity above unchanged to within 0.0012**, with the signed AUCs
of that region's two channels moving by at most 0.008 and no verdict changing (Appendix A(w)). The
table reports the corrected values, and reproduces the frozen matrix at 0.541 against Table B9's
0.541 and 14 of 20 exactly. **The baseline control must be restated on this frame**: the static
baseline transfers at 0.593 against 0.616, a paired difference of +0.023 rather than +0.004, so the
control holds in kind but the gap is about six times larger once frames are comparable, and about
four times at the 5 km collar.

**What this settles, and what it leaves standing.** Five quantities reported below are properties of
the frames rather than of the predictor-burning relationship, and are identified as such where they
appear: the count of six anti-predictive directions, which becomes one; the sign reversal of
elevation, LST and TVDI as a mechanism; the sign-agreement diagnostic; the same-geography arm; and
the paired thermal contribution, +0.004 as drawn against +0.023 equalised. That last quantity
carries the portability null, so it is given an interval on the frame this section argues for:
**+0.023 [−0.004, +0.048]** under the pair-cluster resampling of Appendix A(o). It still spans zero,
so the null survives the correction — but only just, and under the alternative admissible unit,
clustering by target region, it does not (Appendix A(w)). What survives is the central negative
result, and its size must be stated on a matched comparison: setting 0.616 against a within-region
reference of about 0.87 would compare a collar number with a full-rectangle one at 1 km blocking.
Recomputed on the same frame at 5 km blocking that reference is 0.772, so the shortfall is
**+0.155 [+0.094, +0.217]**, a Student *t* interval over the five target regions rather than the
spatial-block bootstrap used elsewhere, and numerically almost identical to Section 4.3's
negative-pool effect over nine scars, which is a different quantity on a different unit. It is real,
and 0.155 rather than the 0.25 an unmatched comparison implies. Appendix C.5(x) records the frame as
a limitation of this cohort rather than of the method.

## 4.5 Cross-region transfer, and what label-free adaptation does to it

**Everything in this section is computed on the frames as drawn and should be read against Section
4.4**, which has shown the frames are not comparable and that the within-region reference used here
is itself frame-dependent. The as-drawn matrix is reported because it is what the pre-registered
protocol yields; per-direction values are in Appendix B, Table B9, and the supporting arms in
Appendix A(x).

**Raw transfer is heterogeneous and includes anti-predictive directions.** Target AUC spans 0.326 to
0.686, and Fig. 4 gives the matrix direction by direction. The support counts depend on the blocking scale, so both are reported: at 2-cell (≈1 km)
blocking twelve of twenty directions are above chance with interval support and six below; at the
10-cell (≈5 km) blocking this design defends, nine are above and four below with seven uncertain,
the counts Table 4 uses. Of the below-chance directions only Manavgat to Bejís survives frame
equalisation, and two verdicts are not stable across bootstrap seeds
(`transfer_ci_blocksize.csv`). Even the best raw transfer sits far below that target's own
within-region 0.870, the raw deficit running 0.184 to 0.592 against a reference Section 4.3 shows is
not matched to a transfer evaluation.

**In precision terms it is worse than the ROC figures suggest.** A susceptibility surface is used as
a ranked area budget, so precision-recall is the operational quantity. PR-AUC averages **0.156
against a no-skill baseline of 0.136**, and **six of twenty directions fall below their own baseline
at the point estimate, five of them with intervals entirely below it**; the exception is Bejis to
Manavgat, whose interval covers its baseline. Only one direction exceeds twice its baseline. These
are frame-as-drawn quantities and the PR arm was not recomputed on the collar (Appendix B, Table B4).

**The static baseline does not transfer either**, at a mean of **0.537** against **0.541** for the
thermal model, so the failure is not specific to the dynamic block: a baseline that does not travel,
plus pre-fire thermal state, gives a model that does not travel. Section 4.4 restates this control on
the equalised frame, where it is 0.593 against 0.616.

**The thermal block's paired contribution is +0.004, and the mean is not the informative statistic.**
The individual contributions span **−0.148 to +0.133**, twelve positive and eight negative, so the
spread is thirty times the mean and the sign belongs to the pair rather than to the block; a mean
near zero records cancellation, not consistent absence of effect. The directions are not independent,
since each region appears in eight of the twenty, so the interval depends on the resampling unit —
**all four units the design permits give the same answer**, from [−0.027, +0.034] to [−0.037,
+0.046], and none propagates within-direction sampling variability. The leave-one-region-out
jackknife shows how little the mean is anchored: **dropping Evia alone reverses its sign.**

**Label-blind adaptation compresses the matrix toward chance rather than repairing it** (Fig. 5).
Under region-wise z-scoring the twenty directions span 0.431 to 0.630 and under CORAL 0.443 to 0.624,
roughly half the raw spread, and fourteen of twenty move closer to chance — which helps the
directions that failed and harms those that worked. The committed-in-advance CORAL arm averages
**0.552**; taking whichever method scores better per direction gives 0.556, but that selection uses
the target labels the protocol forbids, so it is **an oracle upper bound rather than an achievable
result**. Even the oracle only reaches the reference a model can reach on an unseen scar
(Section 4.3), so alignment is regressing the matrix onto that reference rather than failing beneath
it. What it cannot do is exceed the reference, and a sign reversal is not a distribution mismatch
that realigning inputs would repair. Appendix A(x) reports the recovery fractions, including the
seven directions with *negative* recovery.

## 4.6 Transferability diagnostics: what appears to order transfer, and why it does not

Twenty candidate diagnostics from five families were each rank-correlated with raw thermal transfer
over the twenty ordered directions, under one common pair-based bootstrap.

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

**Only two diagnostics have intervals excluding zero, and both are conditional**: the sign-agreement
fraction over interval-supported features at ρ = +0.84 [+0.58, +0.88], and its cosine variant at
+0.81. No marginal measure was shown to order the matrix, including area-of-applicability
dissimilarity, climatic distance and geographic distance, and neither were the niche-overlap and
regime families. The learned domain classifier is at ceiling, separating source from target at
AUC ≥ 0.96 for every pair, so it always succeeds and carries no ordering information. Geographic
separation is a single diagnostic here, centroid distance over the twelve directions for which the
pipeline author's export defines it, at ρ = −0.24 [−0.84, +0.73]: in the expected direction and
spanning zero.

Four limits are stated with the result. **Size**: the index's tie structure caps the achievable
Spearman at +0.861, so the observed +0.840 sits on that ceiling, and its exact one-sided permutation
p of 0.0060 — 240 of the 8! = 40,320 relabellings of the **eight** pairs on which the index is
defined — is the smallest that structure can produce, against a Bonferroni threshold of
0.05/19 = 0.0026. **No outcome of this diagnostic could have cleared family-wise correction.**
**Labels**: signed associations need burned labels in both regions, so the family that appears to
work is not available before deployment while the family that fails is. **Selection**, the sharpest:
the two rows that clear zero are the *supported-feature* variants, whose subset is chosen by whether
two regions' bootstrap intervals happen to be disjoint — a data-dependent selection on the same data,
with no correction; their unselected counterparts over all nine features are ρ = +0.50 [−0.17, +0.83]
and +0.18 [−0.40, +0.72], both spanning zero, so **the result lives in the selection step**.
**Frame**, established in Section 4.4, removes it entirely. Recomputing every row on the common
twelve directions reproduces the published values to 4.8 × 10⁻⁵ and leaves the ordering unchanged, so
it is not an artefact of unequal samples (Appendix B). Everything here is what the original protocol
yields; the conclusion that survives is that **no diagnostic tested here was shown to order transfer
once the frames are comparable**.

## 4.7 Further arms

Six further arms bear on the findings above without changing them: the contrast pair (A(s)), the two
interventions (A(n)), the sensitivity summary (A(v)), the same-geography two-event arm (A(m)), the
distance curve (A(t)) and the label-budget curve (A(u)).
Each is stated there with its own limits. Three are plotted here because the shape of the result is
the argument: pooling every other region never beats the best single source for any target (Fig. 6);
removing the direction-reversing features costs within-region skill and returns nothing measurable on
transfer (Fig. 7); and the contrast pair shows the most burned-niche overlap sitting with the weakest
transfer (Fig. 8). The two bearing directly on Sections 5.4 and 5.7 are the interventions, where a
local cost of −0.081 is measured against a transfer return of +0.014 [−0.017, +0.045] whose interval
spans zero, and the label budget, where thirty-two labelled 5 km blocks recover 85 to 89 % of the
target's matched ceiling in three of six directions and 30 to 57 % in the rest — 7 to 20 % of the
target's population, drawn from the event being predicted, which is not a resource available before
that event burns.
