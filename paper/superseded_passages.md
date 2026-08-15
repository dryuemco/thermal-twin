# Superseded passages

These are earlier, longer versions of passages that now appear in condensed form
in the manuscript. They were kept in Appendix A while the body was being cut, so
that nothing was lost mid-edit, and they are removed from the submitted paper
because the body states the same claims and the appendix sections they duplicate
(A(i), A(o), A(w), A(x), A(y), A(z)) carry the supporting detail.

Nothing here is evidence the paper relies on. It is kept in the repository so a
reader who wants the fuller wording can find it, and so the edit history is
legible without reading the git log.

Removed 2026-08-15. Each section is reproduced exactly as it stood.

## A(bb). The agreed thermal sign, in full

Section 4.4 states this result; the fuller statement is here, and Appendix A(k) carries the
stratification table it draws on.

**The sign they now agree on is not the one the dryness framing predicts**: everywhere a hotter
pre-fire surface is associated with **less** burning, and on mutual adjustment the surviving channel
is LST, not NDVI, so greenness is not the mechanism. Two caveats bound it — in two regions it is a
residual spatial gradient that disappears when distance is stratified inside the collar, and
interval support is not uniform, so "all five agree" is a point-estimate statement. The absolute
channels behave here as **static land-surface descriptors** rather than as a dryness index
(Appendix A(k); Section 5.2 draws the consequence).

## A(cc). Section 4.3's table note and residual arm, in full

The two paragraphs Section 4.3 condenses are given here in full.

All four rows are means over the **same eight scars**. A ninth burned component, Bejis, is excluded
**from this table** because it is that region's only component of any size, so holding it out leaves
no usable source model and there is no row C for it; it is *not* excluded from the arms that need no
leave-one-scar-out model, which is why the prevalence control above and Tables A3 and A4 are
computed on nine scars and report 0.782 and 0.627 against this table's 0.776 and 0.634. The
intervals are Student *t* over the eight scars, which is this arm's resampling unit rather than the
spatial-block bootstrap used elsewhere. Eight is small and the intervals are wide accordingly; four
of the eight scars are in Muğla and two in Montiferru, so they are not independent, and **row A in
particular is a region-level quantity repeated identically across the scars of a region — the four
Muğla scars all carry 0.777 and the two Montiferru scars 0.720 — so its interval is pseudo-replicated
and should not be read as coverage**. That repetition propagates into A − B and A − C, which are the
differences quoted below. Clustering by region instead of by scar gives A − B = +0.155 [+0.082,
+0.228] and A − C = +0.251 [+0.093, +0.409] on four regions: both still exclude zero, but the A − C
interval is 2.3 times wider, so **the scar-level intervals on these two differences overstate
precision** and the clustered ones should be read as the honest width. The two differences are
computed per scar and paired.

**Neither withholding the fire nor moving 2,800 km has a measurable cost.** B minus C, the
fire-specific residual on identical cells, is **+0.082 [−0.011, +0.175]**; C minus D, the effect of
replacing a same-region model with one fitted 306 to 2,802 km away, is **−0.003 [−0.075, +0.069]**.
Both span zero and both arms sit close to chance, so the comparison has little dynamic range: **with
eight scars, three of them starved of positives, this design cannot establish a fire-specific
residual, only bound it at about 0.18.** It is not shown to be zero on an unseen fire, and eight
scars cannot show that; what this design establishes is that it is not established there. Nor does
it establish the fire event as the unit, because the held-out patch is defined by the labels and its
identity cannot be separated from its location. Row D averages four foreign models over a wide
spread, 32 combinations running 0.374 to 0.724 with ten below chance, so the pooled 0.555 says the
*average* foreign model matches a same-region one, not that any particular one does. Sweeping the
two parameters that define the held-out patch — minimum component size over 25 to 200 cells and
connectivity over the 4- and 8-neighbourhoods — moves the row-C mean only between 0.545 and 0.566.
Across buffers the mean is 0.552 at 2 km, 0.540 at 5 km and 0.553 at 10 km, the last over seven
scars rather than eight because one Montiferru component has no 10 km row, so the three are close
but the 10 km figure is not strictly comparable.

## A(ff). Section 4.4's closing statements, in full

Section 4.4 condenses these two passages; they are given here as written.

**A data-provenance defect in this arm was found and corrected**: one region's predictor file at the
canonical path had come to differ from the one the frozen tables were computed on, so every arm here
was re-run against the frozen export. It moves forty of a hundred per-direction values by up to 0.022 and
leaves **every headline quantity below unchanged to within 0.0012**, and moves the signed AUCs of
one region's two channels by at most 0.008 without changing any verdict (Appendix A(w)). The table reports the corrected values. The reference arm reproduces the frozen matrix, at 0.541 against
Table B9's 0.541 and 14 of 20 exactly. **The baseline control must be restated on this frame**: the static baseline transfers at
0.593 against 0.616, a paired difference of +0.023 rather than +0.004 — the control holds in kind,
but the gap is about six times larger once frames are comparable, and about four times at the 5 km
collar, which is the less favourable of the two radii on most columns of Table 4. Both numbers in
that ratio are from the same recomputation; the frozen export's own +0.004 is the value quoted
elsewhere in this paper, and the two agree. The table's counts are point counts;
under the same 10-cell bootstrap the movement is six below chance to one at the point estimate and
**four to one with interval support**.

**What this settles, and what it leaves standing.** Five quantities reported below are properties of
the frames rather than of the predictor-burning relationship, and are identified as such where they
appear: the count of six anti-predictive directions, which becomes one; the sign reversal of
elevation, LST and TVDI as a mechanism; the sign-agreement diagnostic; the same-geography arm; and
the paired thermal contribution, +0.004 as drawn against +0.023 equalised. **That last quantity
carries the portability null, so it is given an interval on the frame this section argues for**:
+0.023 [−0.004, +0.048] under the pair-cluster resampling of Appendix A(o), which is the unit
behind the as-drawn +0.004. Recomputed here on the corrected data that unit gives the as-drawn
figure as [−0.030, +0.036] against the frozen export's [−0.028, +0.036], which is the version quoted
in the abstract and Appendix A(o); the two differ only in the third decimal of one bound. It still spans zero, so the null survives the
correction — but only just, where the as-drawn interval was centred near zero, and under the
alternative admissible unit, clustering by target region, it does not span zero at [+0.016, +0.031].
The honest reading is that **the paired contribution is not established as non-zero on the corrected
frame, and is much closer to the boundary there than the as-drawn number suggests**
(`equalised_delta_interval.json`). What survives is the
central negative result, and its size must be stated on a matched comparison: setting 0.616 against
a within-region reference of about 0.87 would compare a collar number with a full-rectangle one at
1 km blocking. Recomputed on the same frame at 5 km blocking that reference is 0.772, so the
shortfall is **+0.155 [+0.094, +0.217]**, a Student *t* interval over the five target regions rather
than the spatial-block bootstrap used elsewhere, and numerically almost identical to Section 4.3's
negative-pool effect over nine scars, which is a different quantity on a different unit. It is real,
and 0.155 rather than the 0.25 an unmatched comparison implies. Appendix C.5(x) records the frame as
a limitation of this cohort rather than of the method.

## A(gg). Section 4.3's matched comparison, in full

Section 4.3 condenses these two passages; they are given here as written.

**Where the skill is lost, on a matched comparison.** Four evaluations are reported; the last three
are scored on **identical cells**, so they differ only in what the model was trained on, and the
first shows why an unmatched comparison misleads. The held-out unit is a burned connected component
of at least 50 cells together with all cells within 2 km of it. What makes that a harder problem
than a whole region is the composition of its negatives, not its burned fraction, and that can be
shown rather than argued. Taking the same fitted model and the same out-of-fold predictions and
scoring them on a random sample of region cells drawn at the scar area's own burned fraction gives
**0.782 against the region-wide 0.782**: matching the prevalence changes nothing, at
−0.000 [−0.003, +0.002] over the nine scars. Scoring the same predictions on the scar area itself
gives 0.627, a fall of **+0.155 [+0.093, +0.217]**. That comparison swaps both pools at once, so the
two single swaps were run to say which one carries it. Replacing only the negatives, keeping region
positives at the scar's count and taking the scar's own negatives, costs **0.147 [0.104, 0.191]** —
the whole of it. Replacing only the positives costs **0.002 [−0.052, +0.048]**, null on average
though the per-scar effect runs from −0.12 to +0.12. So the attribution is measured rather than
inferred: **the effect is the negative pool** — every negative in a scar collar is fire-adjacent,
sharing the terrain, land cover and synoptic conditions of the positives, whereas a region's
negatives include its easy far field — and ROC-AUC is in any case invariant to class balance at
fixed class-conditional distributions (`pool_decomposition.json`).

**Neither withholding the fire nor moving 2,800 km has a measurable cost.** B minus C, the
fire-specific residual on identical cells, is **+0.082 [−0.011, +0.175]**; C minus D, the effect of
replacing a same-region model with one fitted 306 to 2,802 km away, is **−0.003 [−0.075, +0.069]**.
Both span zero and both arms sit close to chance, so **with eight scars, three of them starved of
positives, this design cannot establish a fire-specific residual, only bound it at about 0.18.** It
is not shown to be zero on an unseen fire, and eight scars cannot show that; what this design
establishes is that it is not established there. Nor does it establish the fire *event* as the unit,
since the held-out patch is defined by the labels and its identity cannot be separated from its
location. Row D averages four foreign models over a wide spread, so it says the *average* foreign
model matches a same-region one, not that any particular one does. The held-out patch's definition
does not drive the result: the row-C mean moves only between 0.545 and 0.566 over component size and
connectivity, and across buffers is 0.552 at 2 km, 0.540 at 5 km and 0.553 at 10 km, the last over
seven scars because one Montiferru component has no 10 km row. Appendix A(z) gives the spread and
the per-scar values.

## A(hh). Further passages condensed from Sections 4.3 and 4.4

Given here as written.

All four rows are means over the **same eight scars**; a ninth component, Bejís, has no row C
because it is its region's only component of any size, which is why the prevalence control and
Tables A3 and A4 are computed on nine and report 0.782 and 0.627 against this table's 0.776 and
0.634. The intervals are Student *t* over the eight scars, this arm's resampling unit rather than
the spatial-block bootstrap used elsewhere. Eight is small, four of the scars are in Muğla and two
in Montiferru, and **row A is a region-level quantity repeated identically across the scars of a
region — the four Muğla scars all carry 0.777 — so its interval is pseudo-replicated and should not
be read as coverage**. That repetition propagates into A − B and A − C. Clustering by region instead
of by scar gives **+0.155 [+0.082, +0.228]** and **+0.251 [+0.093, +0.409]** on four regions: both
still exclude zero, but the A − C interval is 2.3 times wider, so the scar-level intervals on these
two differences overstate precision and the clustered ones are the honest width. Appendix A(i)
carries the per-scar detail.

**Neither withholding the fire nor moving 2,800 km has a measurable cost.** B minus C, the
fire-specific residual on identical cells, is **+0.082 [−0.011, +0.175]**; C minus D, the effect of
replacing a same-region model with one fitted 306 to 2,802 km away, is **−0.003 [−0.075, +0.069]**.
Both span zero and both arms sit close to chance, so **with eight scars, three of them starved of
positives, this design cannot establish a fire-specific residual, only bound it at about 0.18.** It
is not shown to be zero on an unseen fire, and eight scars cannot show that; what this design
establishes is that it is not established there. Nor does it establish the fire *event* as the unit,
since the held-out patch is defined by the labels and its identity cannot be separated from its
location. Row D averages four foreign models over a wide spread, so it says the *average* foreign
model matches a same-region one, not that any particular one does. The patch definition does not
drive the result: the row-C mean moves only between 0.545 and 0.566 over component size and
connectivity, and across buffers is 0.552, 0.540 and 0.553 at 2, 5 and 10 km, the last over seven
scars because one component has no 10 km row (Appendix A(z)).

**Under an equalised frame the sign reversals do not survive.** Restricting every region to cells
within 10 km of any burned cell removes only far-field negatives — every burned cell is at distance
zero and is retained at any radius — so the protection against a flattering radius is the sweep, not
the retention of positives. On that frame all five regions agree in sign on elevation, LST and TVDI,
and both bootstrap-supported elevation reversals of Table B3 disappear. Under this paper's own
criterion from Section 3.10, **no between-region reversal remains bootstrap-supported**: the two
features straddling 0.5 at the point estimate are the internally differenced channels, and in each at
least one region's interval covers 0.5 — Evia's by 0.003. The weaker difference instrument that
Table B3's note commits this paper to does support four opposite-sided pairs on `lst_anomaly_mean`,
with three caveats that keep it weak (Appendix A(l)). **The honest statement is that no between-region
reversal meets the strict criterion under the collar, and that the LST anomaly differs between
regions on the weaker one.** Two scope limits belong with it. The interval criterion was evaluated at
the 10 km collar only; at the point estimate the two radii agree exactly, the same two features
straddling 0.5 at both against eight of nine on the frame as drawn, so the conclusion is not selected
by the radius (`aoi_frame_auc.csv`). And the collar reduces two regions' cell counts substantially,
so part of the loss of support is a loss of power; the counter-evidence is that features supported in
both regions *rise* from 1.20 to 3.40 per direction (Appendix B, Tables B6 and B7).

## A(ii). Passages condensed from Sections 4.5 and 4.6

Given here as written.

**Label-blind adaptation compresses the matrix toward chance rather than repairing it.** Under
region-wise z-scoring the twenty directions span 0.431 to 0.630 and under CORAL 0.443 to 0.624,
roughly half the raw spread, and fourteen of twenty move closer to chance — which helps the
directions that failed and harms those that worked. On the four-AOI twelve-direction subset for
which the decomposition is defined, the best label-free method recovers at most 34 % of the gap in
the directions that started below chance, and seven directions show *negative* recovery, six of them
having started above chance. The committed-in-advance CORAL arm averages **0.552**; taking whichever
method scores better per direction gives 0.556, but that selection uses the target labels the
protocol forbids, so it is **an oracle upper bound rather than an achievable result**. Even the
oracle only reaches the reference a model can reach on an unseen scar (Section 4.3), so alignment is
regressing the matrix onto that reference rather than failing beneath it. What it cannot do is
exceed the reference, and a sign reversal is not a distribution mismatch that realigning inputs
would repair.

Four limits are stated with the result. **Size**: the index's tie structure caps the achievable
Spearman at +0.861, so the observed +0.840 sits on that ceiling, and its exact one-sided permutation
p of 0.0060 — 240 of the 8! = 40,320 relabellings of the **eight** pairs on which the index is
defined, the two Montiferru pairs having no jointly supported feature — is the smallest that
structure can produce, against a Bonferroni threshold of 0.05/19 = 0.0026 for the nineteen computed
variants. **No outcome of this diagnostic could have cleared family-wise correction.**
**Labels**: signed associations need burned labels in both regions, so the family that appears to
work is not available before deployment while the family that fails is. **Selection**, the sharpest:
the two rows that clear zero are the *supported-feature* variants, whose subset is chosen by whether
two regions' bootstrap intervals happen to be disjoint — a data-dependent selection made on the same
data, with no correction; their unselected counterparts over all nine features are ρ = +0.50 [−0.17,
+0.83] and +0.18 [−0.40, +0.72], both spanning zero, so the result lives in the selection step.
**Frame**, established in Section 4.4, removes the result entirely. Recomputing every row on the
common twelve directions reproduces the published values to 4.8 × 10⁻⁵ and leaves the ordering
unchanged, so it is not an artefact of unequal samples (Appendix B). Everything here is what the
original protocol yields; the conclusion that survives is that **no diagnostic tested here was shown
to order transfer once the frames are comparable**.

## A(jj). Table 1's resampling-unit note, in full

Section 4.2 condenses this note; the per-region block counts are here.

*Table note (resampling units).* The bootstrap resamples spatial blocks, so an interval's
reliability is bounded by the number of blocks carrying at least one burned cell, and those counts
fall quickly as blocks coarsen: 235, 302, 843, 716 and 192 at 2 cells; 28, 19, 70, 41 and 16 at 10
cells; and **12, 6, 33, 15 and 6** at 20 cells. An equal-tailed percentile interval built on six
such blocks has no meaningful coverage, and Bejís at 20 cells returned 5 of 1000 replicates
single-class, so **the 20-cell row should be read as indicative rather than as an interval**. The
10-cell row is the coarsest blocking this design supports properly, every region there having 16 to
70 positive-carrying blocks, and the increment holds at that scale in all five regions
(`referee2_numbers.md`, block C; Appendix A(c)).
