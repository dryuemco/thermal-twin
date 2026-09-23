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

## A(kk). Appendix A(w) and the Section 4.4 provenance paragraph, frozen label

Superseded 2026-09-23, when A(w) was aligned with the corrected Manavgat label. Kept as it stood.
Its provenance paragraph sized the correction after re-reading Muğla alone and stated that
Manavgat's replacement file agreed with the published one; the second statement is wrong
(both replaced files differ from their frozen copies), so its size estimate is withdrawn.

### Section 4.4, provenance paragraph

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

### Appendix A(w)

#### A(w). The frame test, elaborated

Section 4.4 states these results; the paragraphs it condensed are here.

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
block-bootstrap interval must exclude 0.5 — **no between-region reversal remains
bootstrap-supported**. The qualifier matters: this arm covers the five regions, and the
same-geography two-fire arm is treated separately in Appendix A(o), where only the year-invariant
channels can be given a verdict at all. Two features
straddle 0.5 at the point estimate and neither is supported: `lst_anomaly_mean` at 0.392 [0.324,
0.460] in Bejís against 0.584 [**0.497**, 0.669] in Evia, where Evia's interval includes 0.5 by
0.003; and `tvdi_difference_mean` at 0.509 [0.417, 0.597] in Muğla against 0.384 [0.288, 0.504] in
Montiferru, where no region's interval excludes 0.5. These are the two internally differenced
channels. An earlier draft treated the first as uniquely informative because it carries no lapse-rate
signal; that does not hold, since the second is equally decorrelated from elevation and behaves the
same way.

**A weaker instrument does support the anomaly result.** Table B3's note commits this paper to a
difference interval on the pair as the sharper test; applied under the collar, four pairs have
opposite-sided point estimates **and** a difference interval excluding zero, all on
`lst_anomaly_mean` and three of the four involving Evia. Three caveats keep it weak: nine of ninety
feature-by-pair differences clear zero against about 4.5 expected under the null with no
multiplicity correction, the nine features are effectively two to three dimensions, and Evia's
support status turns on 0.003. **The honest statement is that no reversal meets this paper's strict
criterion under the collar, and that the LST anomaly differs between regions on the weaker
instrument** (Appendix A(l)).

**The sign the five regions now agree on is not the one the dryness framing predicts.** In every
region a hotter pre-fire surface is associated with **less** burning, and the same holds for TVDI.
It is neither a lapse-rate artefact nor greenness acting through fuel load: on mutual adjustment the
surviving channel is LST, not NDVI. Two caveats bound it — in two regions it is a residual spatial
gradient that disappears when distance to the nearest burned cell is stratified inside the collar,
and interval support is not uniform, so "all five agree" is a statement about point estimates. The
absolute thermal channels therefore behave here as **static land-surface descriptors** rather than
as a dryness index, and the two internally differenced channels carry no consistent cross-region
direction at all. Compositing depth was not tested and remains an open alternative. Per-region
values are in Appendix A(k); Section 5.2 states the consequence for the motivation of Section 1.2.

**The same test determines what the diagnostics of Appendix D can establish.** The only two
candidates there with intervals excluding zero measure agreement in the sign of each predictor's
association between source and target, counted over features interval-supported in both. Those are
built out of exactly the signed AUCs this section has shown to be frame artefacts, and in Section
4.6 they are correlated against transfer measured on the same unequal frames. Recomputing both sides under the 10 km collar gives Table 3 of the body (Section 4.4), which is not
repeated here.

The two fail differently and both fail. Once frames are equalised every region pair agrees in sign
on every jointly supported feature, so the agreement fraction has no variance left. The supported
cosine keeps a trace of variance — unanimous signs fix directions but not magnitudes — and simply
stops tracking transfer. This is not a marginal shift: features supported in both regions *rise*
from 1.40 to 3.40 per direction, so the diagnostics are better determined and unanimous. The
disagreements they were reading were the far fields.

Two scope statements belong with Table 3 and are given in Appendix A(o): the full-frame values
here are not numerically the published ones, because the support test is itself bootstrap-dependent;
and only these diagnostics were recomputed on the collar, so the other eighteen are unknown against
the equalised transfer vector rather than shown to be null.

This settles what Contribution 3 can claim. It is not that conditional similarity orders transfer
where marginal similarity fails; it is that **no diagnostic tested here has been shown to order
transfer**. The eighteen marginal, niche and regime candidates do not order it on the frames as
drawn, and the two conditional variants that do stop doing so once the frames are comparable,
because what they were reading is how the study rectangles were drawn. The practitioner's position
is therefore worse than the as-drawn analysis suggests, not better: there is no screen, and the
apparent exception is an artefact. Appendix D reports its numbers as computed under the
original analysis protocol, which is what a reader following that protocol would obtain.

**The same-geography arm of Appendix A(m) does not survive either, and it is the most extreme case in
the cohort.** A fixed study area is not a fixed evaluation frame: its 2022 arm has 93.2 % of cells
beyond 10 km of any burned cell against 55.3 % for 2021. Under the same collar the 2021 elevation figure barely
moves while the 2022 figure crosses to the same side of 0.5 with an interval covering chance, so the
elevation reversal does not survive equalisation. **This does not generalise across features**: on
the same arm two absolute thermal channels become supported reversals under the collar that were not
reversals as drawn, so equalisation moves this arm's reversal rather than removing it. The
seven-feature table is in Appendix A(o); values in Appendix A(m).

**The within-region increment survives the same correction**, remaining positive in all five
regions on the equalised frame with a mean of +0.077 against +0.086 as drawn, and halving but
staying positive in all five at a 5 km collar. The paper's one surviving predictor-level positive
claim therefore holds on the frame it argues is the correct one. Per-region values are in Appendix A(o).

**The data-provenance correction.** Muğla's 500 m modelling dataset at the canonical path had been
overwritten by a quality-screening rebuild after the frozen tables were computed, so this section's
scripts had read a version of that one region differing from Tables 1 and B9 in
`downscaled_lst_mean` and `fused_lst_mean`. The two files agree on every other column, and which of them is
canonical is not a matter of inference: the pipeline records a SHA-256 for each region's modelling
dataset, and that hash identifies the frozen copy and not the file that had replaced it. The
difference is the data and not the fitting, since both give a within-region baseline of 0.6980 at
10-cell blocking while the thermal arm gives 0.7834 against the frozen 0.7773. The pipeline's own
frozen 10-cell ceiling for this region, computed independently in a separate robustness namespace,
is 0.6980 and 0.7773, which is the frozen file. Two regions' files carry the rebuild's
timestamp, Manavgat's and Muğla's, so both were replaced; the distinction that matters is whether
the replacement agrees with what was published. Manavgat's does, reproducing its Table 1 row to the
printed precision at 0.748 and 0.797, as does the rebuild's own reported increment interval. Muğla's
does not. Bejís, Evia and Montiferru were not touched. Every arm of Section 4.4 was therefore re-run
with Muğla read from the surviving frozen copy and the other four regions as they stand, which is
the configuration Tables 1 and B9 were computed under. The correction moves forty of the hundred per-direction transfer values by
up to 0.022, the largest being Muğla to Montiferru at 0.509 → 0.531. It leaves every headline
quantity of Table 3 unchanged to within 0.0012, the largest being the full-to-10 km paired delta at
+0.0021 against +0.0033: the equalised mean 0.6163 against 0.6166, its paired
delta +0.0231 against +0.0234, and the above-chance counts identical in four rows of five, the 5 km
row moving from 18 to 19 as one direction crosses 0.5. The signed-AUC results are unaffected in
substance — only Muğla's two channels move, by at most 0.008, and the same two features straddle 0.5
on each frame. Sources `aoi_frame_transfer_frozen_mugla.csv`, `aoi_frame_auc_frozen_mugla.csv`,
`frozen_mugla_recheck.json`; code `code/frozen_mugla_verify_aoi_transfer.py`.

**The transfer matrix moves as well.** Restricting source and target to the same collar gives Table 3 of the body (Section 4.4), which is
not repeated here.

The reference arm reproduces the frozen matrix, at 0.541 against Table B9's 0.541 and 14 of 20
exactly, so this is measuring the same quantity. **The baseline control moves with it and must be
restated on this frame**: the static baseline transfers at 0.593 against the thermal model's 0.616,
a paired difference of +0.023 rather than the +0.004 of the frame as drawn. The control still holds
in kind — the static predictor class is not the portable one either — but the gap between them is
about six times larger once frames are comparable, and Sections 1, 5 and 6 quote only the as-drawn
pair. Table 3's above- and below-chance counts are point counts. Under the same 10-cell block bootstrap used for Table B9, at 1000
replicates, the full frame gives nine directions above chance and four below with interval support,
and the collar frame fifteen above and one below, so the headline movement is six to one at the
point estimate and **four to one with interval support** (`aoi_frame_transfer.csv`, which carries
the per-direction bounds). The largest movers are Bejís to Evia, 0.383 to
0.602, and Bejís to Manavgat, 0.440 to 0.601.

**What this settles, and what it leaves standing.** Five quantities reported in the sections that
follow are properties of the frames rather than of the predictor-burning relationship, and are
identified as such where they appear: the count of six anti-predictive directions, which becomes
one; the sign reversal of elevation, LST and TVDI as a mechanism; the sign-agreement diagnostic of
Appendix D; the same-geography arm of Appendix A(m); and the paired thermal contribution, which is
+0.004 as drawn and +0.023 equalised. What the correction leaves standing is the central negative
result, and its size must be stated on a matched comparison. Setting the equalised transfer mean of
0.616 against a within-region reference of about 0.87 would compare a 10 km-collar number with a
full-rectangle one at 1 km blocking, which is the most generous reference in the paper and the very
figure Section 4.3 argues is an upper bound. Recomputing the within-region
reference on the same frame and at the 5 km blocking this design defends
(`matched_frame_gap.csv`, `paper/code/verify_matched_gap.py`):

| Frame | Within-region (5 km blocking) | Mean transfer | Gap |
|---|---:|---:|---:|
| full rectangle | 0.798 | 0.540 | 0.258 |
| 10 km collar | **0.772** | **0.616** | **0.155** |
| 5 km collar | 0.737 | 0.608 | 0.129 |

Paired by target region, the collar shortfall is **+0.155 [+0.094, +0.217]** (Student *t* over the
five target regions; per-region +0.086 Montiferru, +0.127 Manavgat, +0.161 Muğla, +0.196 Bejís,
+0.206 Evia), which reproduces the point estimate above and excludes zero. The shortfall therefore
survives on every matched row, but it is **0.155 at the collar, not the 0.25 the unmatched
comparison implies**, and it shrinks as the frame approaches the fire —
which is where a susceptibility surface is actually used.

This is Section 4.3's effect acting between regions rather than within one, on frames whose
fire-adjacent share ranges from 37 % to 98 %. Appendix C.5(ix) records the frame as a limitation of
this cohort rather than of the method.
