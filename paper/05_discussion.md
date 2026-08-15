# 5. Discussion

> **Rewritten 2026-08-14 in the split.** This section was 9,372 words, of which 5,409 were
> limitations. It now discusses the four contributions of Section 1.4 and carries the limitations that
> bear on them. Six limitations concerning the observational layer, meaning cell geometry,
> compositing, predictor redundancy and the coordinate channels, MODIS quality screening, label
> noise and the safeguards, move with their evidence to the companion paper.

## 5.1 Reading the three findings together

Section 1.4 states the three findings and Section 4 establishes them; this section argues from them
rather than restating them. One relation between them does need saying, because it is what makes the
paper cohere: the first finding is not a caveat attached to the other two, it is the instrument that
sets their size. Applied to our own matrix it withdrew three claims we had made, and what it left
standing is a shortfall in transferred skill, not a reversed relationship.

## 5.2 Why the thermal increment is real but local

The within-region increment and the transfer failure are measured at different separations, and
Section 4.3 shows that most of the difference between them is already present inside a single
region. The increment should therefore be read as local in a specific sense: it holds where held-out
cells are interleaved with training cells, and most of it is gone once they are not, before the fire
or the region changes. It is not an artefact to be explained away — it replicates in five
independent regions, survives coarsening of the blocks to about 5 km with its interval intact,
persists in the secondary population, and survives a predictor window closed up to two weeks earlier
— but it is established under interleaved validation and not established beyond it. The
window-closure result is region-specific and should not be overstated: the contribution strengthens
in Bejís and Muğla, is flat in Montiferru, and **weakens monotonically in Evia**, so what holds
everywhere is survival, not improvement (Appendix A(d)).

The natural objection is that different Mediterranean regions are simply different systems, so that
a predictor meaning one thing in one place and another elsewhere is a comparison of two systems
rather than instability. **We designed the two-Muğla-events arm to answer that objection and it does not answer it.** On the
frames as drawn it looked decisive — region, grid and processing chain identical, static predictors
identical cell by cell, and elevation's association reversing between the two fires — but Sections
4.4 and 4.10 show it is instead the most extreme frame artefact in the cohort, and under the collar
the two arms fall on the same side of 0.5.

The objection therefore stands unanswered, and three further confounds were never resolved in any
case. Season and year are confounded, and **that confound cannot be resolved in this study area**:
the events sit 42 days apart in median burn day-of-year, neither year contains a second event at the
other's phase, and a calendar-matched arm would carry nine burned cells against a gate minimum of
thirty. The population is not held fixed either, the 2022 arm being the 2021 arm with the 2021 scar
removed. And the 2022 arm rests on eleven positive-carrying 5 km blocks against this design's own
floor of sixteen. With one fire per region everywhere else, and the one arm that held place fixed now
withdrawn, **this cohort provides no evidence that the transfer shortfall is regional rather than
event-specific**, and Section 5.9(v) is a substantive limit rather than a formality. Section 4.11 adds a length scale for the
within-region decay — the model is already at chance by 10 to 20 km from its training cells — but
explains why that cannot be turned into an attribution: once the curve reaches the chance floor, any
cross-region mean near 0.5 lies on its continuation by construction.

One conclusion does survive from the other direction. On the frames as drawn the sharpest supported
reversal belonged to elevation, a *baseline* terrain variable, and the static baseline transfers no
better than the dynamic block. Whatever the shortfall is, it is not the thermal block's peculiarity.

## 5.3 Why the similarity-based diagnostics fail

A diagnostic built on distance in predictor space asks one question: do the target's predictor
values look like the training data's? That is not the question that matters when the failure is
conditional. A target region can sit well inside the training envelope while the relationship
between those predictors and burning points the other way. Manavgat to Muğla is exactly that case, with 0.875 of
target cells inside the weighted area of applicability and transfer among the weakest in the matrix. On the frames as drawn that pair is below chance in both directions; on the equalised frame it is
0.551 and 0.510, above chance but still among the weakest in the matrix, while the least similar
pair reaches 0.669 and 0.624 (Section 4.7). The point does not need anti-prediction: high overlap does not buy
transfer.

The same holds for the niche-overlap and regime families. At the point estimates, the pair with the
highest burned-niche overlap in the matrix fails in both directions while the pair with the lowest
transfers in both, so no monotone function of overlap can order the outcomes. The qualifier is not
decorative: at the 5 km blocking this paper otherwise defends, neither Bejís↔Montiferru direction
carries a verdict and Manavgat→Muğla loses its below-chance support, so this contrast is a
statement about point estimates and is made as one. The domain classifier is at ceiling for
every pair, which is informative in itself: the regions are trivially separable in predictor space
whether or not their transfer works, so separability carries no ordering information here.

## 5.4 What the conditional diagnostic is, and what it is not

The sign-agreement index was the paper's one diagnostic with an interval excluding zero, and Section 4.6 states three limits with the result: it sits essentially on its own tie-structure ceiling, it
could not have cleared family-wise correction on ten effective pairs whatever it returned, and its
feature subset is chosen on the same data, its all-nine-feature counterparts spanning zero. A fourth
is that signed associations need burned labels in both regions, so it is a mechanism diagnosis
rather than a pre-deployment screen.

A fifth limit removes it altogether. The index is built from signed associations that Section 4.4
shows to be artefacts of the evaluation frames, and recomputing it on an equalised frame leaves it
unanimous and variance-free, while the second variant that cleared zero loses its correlation
entirely, from ρ = +0.81 to −0.06. So the practical conclusion is not "use this index instead", and
it is not even "the index works but needs labels". It is that **none of the twenty candidates was
shown to order transfer**, and the two that appeared to were reading how the study rectangles were
drawn. That
is a worse position for a practitioner than Section 4.6 alone suggests, and it is the honest one. As
always these are nulls on ten effective pairs: not shown to order transfer, rather than shown
incapable of it.

## 5.5 What the two interventions do and do not show

Both interventions show the same shape. Pooling four regions never beats the best single-source
transfer for any target and stays 0.28 to 0.50 below the within-region ceiling, so aggregation does
not manufacture the missing conditional information. Removing the reversing predictors costs −0.081
of within-region skill with interval support in every region, and changes mean transfer by
+0.014 [−0.017, +0.045], which is not distinguishable from zero.

That pair of numbers is easy to read as an exchange, and it is not one. The thermal block's own
contribution to transfer is +0.004, with an interval spanning zero. Removing the reversing
predictors returns +0.014, with an interval spanning zero. Both arms are null on the portability
axis. What the interventions measure is a local cost and no compensating transfer gain. That is not
a conservation law, and it is not a rate at which local skill can be sold for portability. No such
rate is estimated here.

## 5.6 The regime hypothesis, reported as it happened

A regime-structure explanation was stated in advance and the data confirmed the null. The
regime-distance correlation has the wrong sign at the point estimate, the most regime-similar pair
fails in both directions, and the most regime-different pair transfers above chance. One mundane
explanation can be set aside: cutting Muğla, by far the largest population, to Manavgat's cell count
and separately to its positive count leaves Muğla's transfer behaviour inside the subsampling range
in both roles. The error was in the hypothesised grouping, not in the data, and with ten pairs this
cannot refute regime typology [@Archibald2013] in general.

## 5.7 The empirical contrast with Dimarco et al.

Dimarco et al. [@Dimarco2026] transfer successfully across a comparable Mediterranean design and we
do not, and the two results are not in conflict. Their predictors are attributes of a place, ours
describe the state of a surface in one season, which suggests that the relationship between domain
similarity and transfer success is predictor-class dependent.

That reading is one of at least two, and we cannot separate them here. Their response variable is
human-driven **ignition**; ours is burned **area**. Ignition likelihood is dominated by human access
and activity, stable and near-universal drivers, whereas burned extent is dominated by spread. A
predictor-class explanation and a response-variable explanation are therefore confounded in this
comparison. Our own data speak against a simple predictor-class reading in any case: the static
baseline transfers at a mean of 0.537 here, so within this cohort the place-attribute class does not
travel either.

## 5.8 Implications

For practice, one number should be stated before any other. In precision-recall terms, which is how
a susceptibility surface is actually used, transferred models average a PR-AUC of 0.156 against a
no-skill baseline of 0.136, and six of twenty directions fall below their own baseline. Whatever
the ROC figures suggest, a model moved to a region it was not fitted in does not usefully rank
burned cells there.

This paper also supports one concrete change in what is reported. Alongside a spatially
blocked within-region figure, report skill on a held-out burn scar and its surroundings, or on a
held-out fire event. On these five regions the two differ by about 0.14 ROC-AUC on the same model,
which is the size of the effect such papers usually claim, so a blocked figure alone should be read
as an upper bound. Transfer skill likewise has to be *measured* rather than inferred from similarity,
and the pre-deployment diagnostics currently used for that inference did not order it here. Where a model
must be moved, the resource that closes the gap is target labels: thirty-two labelled 5 km blocks
recover 85 to 89 % of the target's matched ceiling in three of six directions, and 30 to 57 % in the
rest. That is a real answer and not a cheap one, being 7 to 20 % of the target's natural-vegetation
population, and at small budgets the same intervention damages the direction that already transfers
best.

For method development, the results bound what unsupervised alignment can be asked to do. Two
label-free methods applied carefully moved fourteen of twenty directions towards chance, and five of
the six they moved upward involve Montiferru, the smallest region; the sixth, Manavgat to Muğla,
moves downward. The committed-in-advance CORAL arm reaches a mean of 0.552, and taking whichever of
the two methods scores better per direction reaches 0.556 — but that selection uses the target
labels the protocol forbids, so it is an oracle upper bound rather than an achievable result
(Section 4.5). Even the oracle only reaches the reference a
model can reach on an unseen scar at all (Section 4.3), so they are not failing far below an
achievable target; they are regressing the matrix onto it, which costs the directions that already
worked. What alignment cannot do is exceed that reference, and a sign reversal is not a distribution
mismatch that realigning inputs would repair.

## 5.9 Limitations

The transfer failure is a finding, not a limitation. The limitations are the boundaries on how far
it generalises.

(i) **No meteorological covariates** enter the models, so we cannot say how local skill and
portability behave for a mixed thermal-plus-weather predictor set.

(ii) **The same-geography comparison covers one region only**, and even there year and seasonal phase
are confounded, a confound that cannot be resolved in this study area for the reason given in
Section 5.2. Its 331 burned cells also leave the thermal reversals unresolved at interval level, and
the pair holds place fixed but not population. Those two arms are additionally the only transfer
directions here computed by us rather than read from the pipeline author's frozen export, with his
unmodified code and the same pinned environment.

(iii) **All labels derive from a single burned-area product**, MCD64A1 [@Giglio2018], whose omission
and commission characteristics [@Boschetti2019] bound every model evaluated here. No second
burned-area product covers 2021 and 2022 at this resolution; the companion paper reports what an
independent active-fire observation says about the omission concern.

(iv) **Evia remains the most imbalance-atypical population** even after the AOI extension, at a TSG
prevalence of 0.287 against 0.038 to 0.072 in three of the others.

(v) **Each region contributes one fire season**, so regional concept shift is confounded with event
meteorology, and distinguishing them requires multi-year labels.

(vi) **Cross-region point estimates carry an implementation tolerance** of roughly ±0.02 to 0.03
across scikit-learn versions. All reported numbers are fixed to one verified version, but exact
reproduction elsewhere requires the archived environment.

(vii) **The diagnostic correlations rest on an effective sample of ten region pairs.** Both the
successes and the failures of Section 4.6 should be read at that power.

(viii) **Manavgat's atypical transfer behaviour remains unexplained.** It is where the conditional
diagnosis bites hardest and where feature removal recovers most. Three candidates have now been tested and none survives: its meteorology, which was not extreme;
the quality screening of its coarse thermal input, which propagates widely but moves no signed
association by more than +0.0003 (Section 4.9, Appendix A(e)); and the evaluation frame, which
explains its elevation figure but not its transfer behaviour (Section 4.4). With one fire season per
region the remaining candidates are not separable in this design.

(ix) **The interval-support counts are less stable than the point estimates behind them.** Several
verdicts sit within a thousandth of their reference value, and at 1 km blocking the published split
of ten positive, seven negative and three uncertain turns on a lower bound of −0.00045. The point
estimates and the sign pattern are stable; the counts are not. Every sentence in this paper that
leans on an exact count of supported directions should be read at that precision.
(x) **The five areas of interest are not comparable frames, and this cohort cannot fully repair it**
(Section 4.4). We report the equalised arm alongside the frame-as-drawn arm rather than replacing one
with the other, because the collar radius is itself a choice and 5 km and 10 km do not agree exactly
(0.608 against 0.617). The deeper limitation is that the frames were fixed upstream of this work, in
`repo/`, so we can restrict them but not extend them; a region whose rectangle is already fire-scale,
Montiferru, cannot be given a far field for symmetry. Any future cohort should fix the frame by an
explicit accessible-area rule [@Barve2011] before any predictor is computed, and we treat that as the
main design lesson of this paper.

(xi) **One classifier family.** The headline numbers use a random forest with unlimited depth, the
configuration most able to encode local structure and least able to extrapolate. Appendix A(h) shows the transfer result is not an artefact of that
choice: three further estimators, including a penalised linear one, all land between 0.510 and 0.556
and all place fourteen of twenty directions above chance. Those are point estimates without
intervals, so the ordering among them is not claimed as a result. Other model families were not
tried, and a different inductive bias might behave differently, but within this family the negative
result is a property of the predictors rather than of an unregularised estimator.

