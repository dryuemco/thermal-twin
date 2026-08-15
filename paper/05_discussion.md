# 5. Discussion

> **Rewritten 2026-08-14 in the split.** This section was 9,372 words, of which 5,409 were
> limitations. It now discusses the four contributions of Section 1.4 and carries the limitations that
> bear on them. Six limitations concerning the observational layer, meaning cell geometry,
> compositing, predictor redundancy and the coordinate channels, MODIS quality screening, label
> noise and the safeguards, move with their evidence to the companion paper.

## 5.1 Principal findings

Four results carry this paper. First, the pre-fire thermal block raises spatially blocked
within-region ROC-AUC by +0.056 to +0.153 in every one of five Mediterranean regions, with bootstrap
support at 1 km and 5 km blocking, and contributes +0.004 [−0.028, +0.036] across twenty ordered
transfer directions, indistinguishable from zero and with a sign that varies by pair. The static
baseline transfers no better, at a mean of 0.537 against 0.541, so the failure is not a property of
the dynamic block specifically. Nor is it attributable to region crossing. On identical
cells, withholding the burn scar from training costs +0.082 [−0.011, +0.175] and moving the training
data 306 to 2,802 km away costs −0.003 [−0.075, +0.069]. The failure is a property of contiguous
spatial holdout. The six below-chance directions are a separate matter, since no account of
merely lost skill produces a reliably reversed ranking. Removing the two reversing predictors,
elevation and the LST anomaly, costs −0.081 of within-region skill, supported in every region and
three quarters attributable to elevation, and changes transfer by +0.014 [−0.017, +0.045], which
also spans zero. Second, of twenty candidate transferability diagnostics only two have intervals excluding zero and
both are conditional, while no marginal measure was shown to order the matrix. The marginal family,
which includes area-of-applicability dissimilarity, is the only one runnable before deployment. Third,
the mechanism is a reversal in the sign of the predictor-burning association, and it persists inside
one study area across two fires.

## 5.2 Why the thermal increment is real but local

A distinction has to be drawn before this section can say anything useful. The within-region
increment and the transfer failure are measured at different separations, and Section 4.3 shows that
most of the difference between them is already present inside a single region. What follows
therefore reads the increment as local in a specific sense: it holds where the held-out cells are interleaved with
training cells, and most of it is gone once they are not, before the fire or the region changes. What that does not explain is why the directions differ from each
other, and in particular why six of them are anti-predictive.

The within-region increment is not an artefact to be explained away, but it is measured under a
holdout that Section 4.3 shows is generous. Withholding a whole burn scar reduces it to +0.022
[−0.032, +0.077], so what follows describes an increment that is established under interleaved
validation and not established beyond it. It replicates in five
independent regions, survives coarsening of the spatial blocks to ~5 km with its interval intact,
persists in the secondary all-valid population, and survives a predictor window closed 7 and 14 days
earlier in all five regions. The direction of that last result is region-specific and should not be
overstated: the contribution strengthens in Bejís (0.058 → 0.079 at 14 days) and Muğla (0.115 →
0.128), is flat in Montiferru, and **weakens monotonically in Evia** (0.156 → 0.149 → 0.135). What
holds everywhere is survival, not improvement. The transfer failure is therefore not evidence that
the thermal signal is spurious. It is evidence that the fitted relationship is *local*.

The natural objection is that different Mediterranean regions are simply different systems, so that
a predictor meaning one thing in one place and another elsewhere is not instability but a comparison
of two different systems. The two Muğla events answer it directly: region, AOI, grid, feature
registry and processing chain identical, static predictors identical cell by cell, and elevation's
association with burning reversing from 0.611 [0.532, 0.690] to 0.296 [0.230, 0.355], a difference of
−0.317 [−0.414, −0.220] (Section 4.8). Holding geography fixed does not stabilise the direction of
the relationship.

Three caveats attach and none is dismissed. Season and year are confounded, and **that confound
cannot be resolved in this study area**: the events sit 42 days apart in median burn day-of-year,
neither year contains a second event at the other's phase, and a calendar-matched arm would carry
nine burned cells against a gate minimum of thirty. The population is not held fixed either, the
2022 arm being the 2021 arm with the 2021 scar removed. And the 2022 arm rests on one compact scar
and eleven positive-carrying 5 km blocks. What survives all three is the narrower reading that
*something* reverses the elevation-burning association with geography, grid and pipeline held fixed,
which is why Section 4.8 is reported as corroboration rather than as the load-bearing evidence for
the mechanism.

The sharpest supported reversal belongs to elevation, a static predictor, so instability is a
property of the predictor-to-burning mapping generally rather than of thermal channels specifically.
This is the same conclusion the baseline transfer arm reaches from the other direction: the
instability is not the thermal block's peculiarity.

## 5.3 Why the similarity-based diagnostics fail

A diagnostic built on distance in predictor space asks one question: do the target's predictor
values look like the training data's? That is not the question that matters when the failure is
conditional. A target region can sit well inside the training envelope while the relationship
between those predictors and burning points the other way. Manavgat to Muğla is exactly that case,
with 0.875 of target cells inside the weighted area of applicability and transfer below chance.

The same holds for the niche-overlap and regime families. At the point estimates, the pair with the
highest burned-niche overlap in the matrix fails in both directions while the pair with the lowest
transfers in both, so no monotone function of overlap can order the outcomes. The qualifier is not
decorative: at the 5 km blocking this paper otherwise defends, neither Bejís↔Montiferru direction
carries a verdict and Manavgat→Muğla loses its below-chance support, so this contrast is a
statement about point estimates and is made as one. The domain classifier is at ceiling for
every pair, which is informative in itself: the regions are trivially separable in predictor space
whether or not their transfer works, so separability carries no ordering information here.

## 5.4 What the conditional diagnostic is, and what it is not

The sign-agreement index reaches ρ = +0.84 [+0.58, +0.88] against observed transfer. Three limits
are reported with it rather than after it, and the sharpest is a selection: the two rows that clear
zero are supported-feature variants whose subset is chosen on the same data, and their
all-nine-feature counterparts span zero. Its tie structure caps the achievable Spearman at +0.861,
so the observed value sits essentially on its own ceiling and the ranking it supports is coarse. Its
exact one-sided permutation p is 0.0060, the smallest that tie structure can produce, against a
Bonferroni threshold of 0.0026 over nineteen computed variants. No outcome could have cleared
family-wise correction on ten effective pairs. And it needs burned labels in both regions, which
makes it a mechanism diagnosis rather than a pre-deployment screen.

That last limit is the substantive one, and it is why the paper's practical conclusion is not "use
this index instead". It is that the family of diagnostics that can be run before deployment is the
family that fails here, and the information that would order transfer is the information a
practitioner does not have when the decision is made. The honest statement is that these twenty
candidates were **not shown to order transfer**, not that they are shown incapable of it.

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
label-free methods applied carefully moved fourteen of twenty directions towards chance, and every
direction they improved involves the smallest region. But their mean, 0.556, is at the reference a
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
successes and the failures of Section 4.4 should be read at that power.

(viii) **Manavgat's atypical transfer behaviour remains unexplained.** It is where the conditional
diagnosis bites hardest and where feature removal recovers most. Two candidates have now been tested
and neither survives. The first was its meteorology: the predictor window was not extreme. The second
was the quality-screening difference in its coarse thermal input. It was the
more worrying of the two, because the change it induces correlates with elevation at +0.615. It does
not propagate. The region's entire downstream chain was rebuilt from a quality-screened MODIS input.
That changes the downscaled surface on 22,304 of 24,150 cells, by up to 10.9 °C. No signed
univariate association moves by more than +0.0003. Elevation's is identical in both arms, at 0.374, and the population is unchanged. The result is structural rather than fortunate. Elevation is
a DEM variable the screening cannot touch, and fusion falls back on the MODIS-derived surface across
only 2.14 percentage points of coverage. With one fire
season per region the remaining candidates are not separable in this design.

(ix) **The interval-support counts are less stable than the point estimates behind them.** Several
verdicts sit within a thousandth of their reference value, and at 1 km blocking the published split
of ten positive, seven negative and three uncertain turns on a lower bound of −0.00045. The point
estimates and the sign pattern are stable; the counts are not. Every sentence in this paper that
leans on an exact count of supported directions should be read at that precision.
(x) **One classifier family.** The headline numbers use a random forest with unlimited depth, the
configuration most able to encode local structure and least able to extrapolate. Appendix A(h) shows
the transfer result does not depend on that choice: a depth-6 forest, a leaf-200 forest and a
penalised logistic regression transfer at 0.556, 0.550 and 0.510 against the canonical 0.541, all
four place exactly fourteen of twenty directions above chance, and the linear model, the one built
to extrapolate, transfers worst. Regularisation costs within-region skill, 0.888 down to 0.741,
without buying portability, and it drives the thermal block's cross-region contribution negative.
Other model families were not tried, and a fundamentally different inductive bias might behave
differently, but within this family the negative result is a property of the predictors rather than
of an unregularised estimator.

