# 5. Discussion

> **Rewritten 2026-08-14 in the split.** This section was 9,372 words, of which 5,409 were
> limitations. It now discusses the four contributions of Section 1.4 and carries the limitations that
> bear on them. Six limitations concerning the observational layer, meaning cell geometry,
> compositing, predictor redundancy and the coordinate channels, MODIS quality screening, label
> noise and the safeguards, move with their evidence to the companion paper.

## 5.1 Reading the three findings together

Section 1.4 states the three findings and Section 4 establishes them; this section argues from them.
One relation between them makes the paper cohere: the first finding is not a caveat attached to the
other two, it is the instrument that sets their size. Applied to our own matrix it withdrew five
claims we had made, and what it left standing is a shortfall in transferred skill, not a reversed
relationship.

## 5.2 Why the thermal increment is real but local

The within-region increment and the transfer failure are measured at different separations, and
Section 4.3 shows most of the difference between them is already present inside a single region. The
increment is local in a specific sense: it holds where held-out cells are interleaved with training
cells and most of it is gone once they are not, before the fire or the region changes. It is not an
artefact to be explained away, surviving every robustness arm of Section 4.2, but it is established
under interleaved validation and not beyond it.

The natural objection is that Mediterranean regions are simply different systems, so a predictor
meaning one thing in one place and another elsewhere is a comparison of two systems rather than
instability. **We designed the two-Muğla-events arm to answer that objection and it does not
answer it**: Section 4.4 shows it is the most extreme frame artefact in the cohort. The objection
therefore stands unanswered, and three further confounds were never resolved in any case: season and
year, which **cannot be resolved in this study area**, an unfixed population, and a positive-block
count below this design's own floor (Appendix C.5(ii)). With one fire per region everywhere else and
the one place-fixed arm withdrawn, **this cohort provides no evidence that the transfer shortfall is
regional rather than event-specific**. Appendix A(t) adds a length scale for the within-region decay
but cannot turn it into an attribution either.

One conclusion survives from the other direction: the static baseline transfers no better than the
dynamic block, so whatever the shortfall is, it is not the thermal block's peculiarity.

## 5.3 Why the diagnostics fail, and what the conditional one is not

A diagnostic built on distance in predictor space asks whether the target's predictor values look
like the training data's, which is not the question that matters when the failure is conditional: a
target region can sit well inside the training envelope while the relationship between those
predictors and burning points the other way. Manavgat to Muğla is exactly
that case, with 0.875 of target cells inside the weighted area of applicability and transfer among
the weakest in the matrix, while the least similar pair transfers better (Appendix A(s)). High
overlap does not buy transfer. **The qualifier is not decorative**: at the 5 km blocking this paper
otherwise defends neither contrasted direction carries a verdict, so this is a statement about point
estimates and is made as one. The domain classifier is at ceiling for every pair, so
separability carries no ordering information.

The two conditional variants that did clear zero are not a remedy. Section 4.6 states four limits
with them: a tie-structure ceiling, a family-wise threshold **no outcome could have cleared**, a
feature subset selected on the same data, and a label requirement making it a mechanism diagnosis
rather than a screen. A fifth removes it altogether, since the index is built
from signed associations Section 4.4 shows to be frame artefacts. So the practical
conclusion is not "use this index instead", nor even "it works but needs labels": **none of the
twenty candidates was shown to order transfer**, and the two that appeared to were reading how the
rectangles were drawn. As always these are nulls on ten effective pairs: not shown to order
transfer, rather than shown incapable of it.

## 5.4 What the two interventions do and do not show

Both interventions show the same shape. Pooling four regions never beats the best single-source
transfer for any target and stays well below the within-region ceiling (Appendix A(n)), so
aggregation does not manufacture the missing conditional information. Removing the reversing
predictors costs −0.081 of within-region skill with interval support in every region, and changes
mean transfer by +0.014 [−0.017, +0.045], not distinguishable from zero.

That pair of numbers is easy to read as an exchange, and it is not one. Both arms are null on the
portability axis — the thermal block's own contribution to transfer is +0.004 and removal returns
+0.014, both intervals spanning zero — so what the interventions measure is a local cost and no
compensating transfer gain. That is not a conservation law, and it is not a rate at which local
skill can be sold for portability. No such rate is estimated here.

## 5.5 The regime hypothesis, reported as it happened

A regime-structure explanation was stated in advance and the data confirmed the null. The
regime-distance correlation has the wrong sign at the point estimate, the most regime-similar pair
fails in both directions, and the most regime-different pair transfers above chance. One mundane
explanation can be set aside: subsampling Muğla, by far the largest population, to Manavgat's cell
count and separately to its positive count leaves its transfer behaviour inside the subsampling
range in both roles. The error was in the hypothesised grouping, not in the data, and with ten pairs
this cannot refute regime typology [@Archibald2013] in general.

## 5.6 The empirical contrast with Dimarco et al.

Dimarco et al. [@Dimarco2026] transfer successfully across a comparable Mediterranean design and we
do not, and the two results are not in conflict. Their predictors are attributes of a place, ours
the state of a surface in one season, which suggests the relation between domain similarity and
transfer success is predictor-class dependent.

That reading is one of at least two, and we cannot separate them here: their response variable is
human-driven **ignition**, dominated by access and activity, while ours is burned **area**, dominated
by spread, so a predictor-class explanation and a response-variable explanation are confounded in
this comparison. Our own data speak against a simple predictor-class reading in any case: the static
baseline transfers at a mean of 0.537 here, so within this cohort the place-attribute class does not
travel either.

## 5.7 Implications

In precision-recall terms, which is how a susceptibility surface is used, transferred models average a PR-AUC of 0.156 against a no-skill
baseline of 0.136 (Section 4.5). Whatever the ROC figures suggest, a model moved to a region it was
not fitted in does not usefully rank burned cells there.

The paper supports one concrete change in reporting: alongside a spatially blocked within-region
figure, report skill on a held-out burn scar and its surroundings. On these five regions the two
differ by about 0.14 ROC-AUC on the same model, the size of the effect such papers usually claim, so
a blocked figure alone should be read as an upper bound. Transfer skill likewise has to be
*measured* rather than inferred from similarity, since the diagnostics used for that inference did
not order it here. Where a model must be moved, the resource that closes the gap is target labels,
priced in Appendix A(u): a real answer, but not a cheap one, and drawn from the event being
predicted.

For method development, the results bound what unsupervised alignment can be asked to do. Even the
oracle selection — which uses the target labels the protocol forbids — only reaches the reference a
model can reach on an unseen scar (Section 4.5). Alignment is not failing far below an achievable
target; it is regressing the matrix onto it, which costs the directions that already worked. A sign
reversal is not a distribution mismatch that realigning inputs repairs.

## 5.8 Limitations

Eleven limitations are stated in full in Appendix C.5; four bind the conclusions above. **The frames
are not comparable and this cohort cannot fully repair it** (Section 4.4): the collar radius is
itself a choice — 5 km and 10 km give 0.608 against 0.617 — and the frames were fixed upstream, so
we can restrict them but not extend them. Any future cohort should fix the frame
by an explicit accessible-area rule [@Barve2011] before any predictor is computed, and we treat that
as the main design lesson of this paper. **Each region contributes one fire season**, so regional
concept shift is confounded with event meteorology and the shortfall cannot be attributed to region
rather than event (Section 5.2). **The diagnostic correlations rest
on an effective sample of ten region pairs**, so both the successes and failures of Section 4.6 read
at that power. And **the interval-support counts are less stable than the point
estimates behind them**: the published split turns on a lower bound of −0.00045. The remaining seven — from the absent meteorological
covariates to the single classifier family, whose capacity sweep is in Appendix A(h) — bear on
scope rather than on the conclusions above.
