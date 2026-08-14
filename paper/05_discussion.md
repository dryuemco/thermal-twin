# 5. Discussion

> **Rewritten 2026-08-14 in the split.** This section was 9,372 words, of which 5,409 were
> limitations. It now discusses the three findings of Section 1.4 and carries the limitations that
> bear on them. Six limitations concerning the observational layer, meaning cell geometry,
> compositing, predictor redundancy and the coordinate channels, MODIS quality screening, label
> noise and the safeguards, move with their evidence to the companion paper.

## 5.1 Principal findings

Three results carry this paper. First, the pre-fire thermal block raises spatially blocked
within-region ROC-AUC by +0.056 to +0.153 in every one of five Mediterranean regions, with bootstrap
support at 1 km and 5 km blocking, and contributes +0.004 on average across twenty ordered transfer
directions with an interval spanning zero and an unstable sign. Removing the two reversing
predictors costs −0.081 of within-region skill, supported in every region, and buys +0.014 of
transfer whose interval spans zero. Second, of twenty candidate transferability diagnostics only two
have intervals excluding zero and both are conditional, while every marginal measure fails,
including the area-of-applicability family that is the only one runnable before deployment. Third,
the mechanism is a reversal in the sign of the predictor-burning association, and it persists inside
one study area across two fires.

## 5.2 Why the thermal increment is real but local

The within-region increment is not an artefact to be explained away. It replicates in five
independent regions, survives coarsening of the spatial blocks to ~5 km with its interval intact,
persists in the secondary all-valid population, and strengthens rather than weakens when the
predictor window is closed earlier. The transfer failure is therefore not evidence that the thermal
signal is spurious. It is evidence that the fitted relationship is *local*.

The natural objection is that different Mediterranean regions are simply different systems, with
distinct fuels, terrain and fire histories, so that a predictor meaning one thing in one place and
another elsewhere is not instability but a comparison of two different systems. The two Muğla events
speak directly to that. Region, AOI, analysis grid, feature registry and processing chain are
identical, and the static predictors are identical cell by cell, yet elevation's association with
burning reverses with disjoint intervals, 0.611 [0.532, 0.690] in 2021 against 0.296 [0.230, 0.355]
in 2022, a difference of −0.317 [−0.414, −0.220]. Holding geography fixed does not stabilise the
direction of the relationship.

The mechanism there is physical rather than statistical. The 2021 season burned as a dispersed
complex across the region's full relief; the 2022 event was a single compact scar confined to lower
ground. Two caveats attach and neither is dismissed. Season and year are confounded, because the
2022 event ignites about six weeks earlier, and **that confound cannot be resolved in this study
area**: the two events sit 42 days apart in median burn day-of-year, neither year contains a second
event at the other's phase, and a calendar-matched arm would carry nine burned cells against a gate
minimum of thirty. Separating year from seasonal phase needs a region with two events at a matching
phase in different years, and no region here has one. The design also does not hold the population
fixed, since the 2022 arm is the 2021 arm with the 2021 scar removed, which Section 4.8 states in
full. What survives both caveats is the narrower reading that *something* reverses the
elevation-burning association with geography, grid and pipeline held fixed.

The sharpest supported reversal belongs to elevation, a static predictor, so instability is a
property of the predictor-to-burning mapping generally rather than of thermal channels specifically.
The thermal block is where the trade-off is *costly*, not where instability is worst.

## 5.3 Why the similarity-based diagnostics fail

A diagnostic built on distance in predictor space asks whether the target's predictor values look
like the training data's. That question is orthogonal to the one that matters when the failure is
conditional. A target region can sit deep inside the training envelope while the relationship
between those predictors and burning points the other way, and Manavgat to Muğla is exactly that
case: 0.875 of target cells inside the weighted area of applicability, and transfer below chance.

The same holds for the niche-overlap and regime families. The pair with the highest burned-niche
overlap in the matrix fails in both directions while the pair with the lowest transfers in both, so
no monotone function of overlap can order the outcomes. The domain classifier is at ceiling for
every pair, which is informative in itself: the regions are trivially separable in predictor space
whether or not their transfer works, so separability carries no ordering information here.

## 5.4 What the conditional diagnostic is, and what it is not

The sign-agreement index reaches ρ = +0.84 [+0.58, +0.88] against observed transfer, and it is
reported with three limits attached rather than after the fact. Its tie structure caps the achievable
Spearman at +0.861, so the observed value sits essentially on its own ceiling and the ranking it
supports is coarse. Its exact one-sided permutation p is 0.0060, the smallest that tie structure can
produce, against a Bonferroni threshold of 0.0026 over nineteen computed variants, so no outcome
could have cleared family-wise correction on ten effective pairs. And it needs burned labels in both
regions, which makes it a mechanism diagnosis rather than a pre-deployment screen.

That last limit is the substantive one, and it is why the paper's practical conclusion is not "use
this index instead". It is that the family of diagnostics that can be run before deployment is the
family that fails here, and the information that would order transfer is the information a
practitioner does not have when the decision is made. The honest statement is that these twenty
candidates were **not shown to order transfer**, not that they are shown incapable of it.

## 5.5 Interventions obey a conservation pattern

Both interventions show the same shape. Pooling four regions never beats the best single-source
transfer for any target and stays 0.28 to 0.50 below the within-region ceiling, so aggregation does
not manufacture the missing conditional information. Removing the reversing predictors buys a little
transfer and pays for it locally, at about six times the cost in within-region skill at the point
estimates, though the transfer side's interval spans zero so no exchange rate is claimed. What
transfer gains, the within-region model pays for.

## 5.6 The regime hypothesis, reported as it happened

A regime-structure explanation was stated in advance and the data confirmed the null. The
regime-distance correlation has the wrong sign at the point estimate, the most regime-similar pair
fails in both directions, and the most regime-different pair transfers above chance. One mundane
explanation can be set aside: Muğla has by far the largest population, but cutting it to Manavgat's
cell count, and separately to Manavgat's positive count as well, leaves its transfer behaviour
inside the subsampling range in both roles. The error was in the hypothesised grouping, not in the
data, and with ten pairs this cannot refute regime typology [@Archibald2013] in general.

## 5.7 The empirical contrast with Dimarco et al.

Dimarco et al. [@Dimarco2026] transfer successfully across a comparable Mediterranean design and we
do not, and the two results are not in conflict. Their predictors are attributes of a place, ours
describe the state of a surface in one season. Read together they suggest that the relationship
between domain similarity and transfer success is predictor-class dependent. We present that as a
live disagreement, since species distribution modelling aligns with it and the fire literature does
not, and it is a reading our data support without proving.

## 5.8 Implications

For practice, transfer skill has to be *measured* rather than inferred from similarity, and the
pre-deployment diagnostics currently used for that inference did not order it here. Where a model
must be moved, the resource that closes the gap is target labels: thirty-two labelled 5 km blocks
recover 85 to 89 % of the target's own ceiling in three of six directions, and 30 to 57 % in the
rest. That is a real answer and not a cheap one, being 7 to 20 % of the target's natural-vegetation
population, and at small budgets the same intervention damages the direction that already transfers
best.

For method development, the results point away from better unsupervised alignment. Two label-free
methods applied carefully moved fourteen of twenty directions towards chance, and every direction
they improved involves the smallest region. A sign reversal is not a distribution mismatch, and no
realignment of inputs can repair it.

## 5.9 Limitations

The transfer failure is a finding, not a limitation. The limitations are the boundaries on how far
it generalises.

(i) **No meteorological covariates** enter the models, so we cannot say how the trade-off behaves
for a mixed thermal-plus-weather predictor set.

(ii) **Temporal transfer is measured for one region only**, and even there year and seasonal phase
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
diagnosis bites hardest and where feature removal recovers most. The explanation we could test, that
its predictor window was meteorologically extreme, is not supported; the companion paper reports a
second candidate, a quality-screening difference in its coarse thermal input whose induced change
correlates with elevation. With one fire season per region the remaining candidates are not
separable in this design.

(ix) **The interval-support counts are less stable than the point estimates behind them.** Several
verdicts sit within a thousandth of their reference value, and at 1 km blocking the published split
of ten positive, seven negative and three uncertain turns on a lower bound of −0.00045. The point
estimates and the sign pattern are stable; the counts are not. Every sentence in this paper that
leans on an exact count of supported directions should be read at that precision.
