# 6. Conclusions


Where a fire model is scored decides what it appears to know. Holding the model, its predictors and
its fitting fixed and changing only which cells are scored, moving from a whole study region to the
burn scar and its 2 km collar costs **0.143 ROC-AUC [+0.077, +0.208]**. A control isolates the cause:
matching prevalence changes nothing, at −0.000 [−0.003, +0.002], while scoring the same predictions
on the scar area costs +0.155 [+0.093, +0.217]. It is the composition of the negative pool, not
class balance. The effect is larger than the predictor-block increments this literature publishes as
findings, so a region-wide validation figure should be read as an upper bound on what a model
achieves where fire actually occurs, and reported as one.

That correction is not only other people's problem. Applied to our own five-region matrix it
withdraws three of our claims. The study areas enclose very different far fields, from 2 % to 63 %
of cells beyond 10 km of any fire, and that far field is higher ground. Equalising them to a 10 km
collar, which drops no burned cells, lifts mean transfer from 0.540 to 0.617, reduces the directions
below chance from six to one, and makes all five regions agree in sign on elevation, LST and TVDI.
The sign reversal we had offered as the mechanism of the transfer residual is therefore mostly a
property of how five rectangles were drawn. Under our own criterion no reversal then remains
bootstrap-supported. The sign the five regions agree on is also not the one the dryness framing
predicts: hotter pre-fire surfaces burned less everywhere, surviving stratification within elevation
and greenness, so on this cohort the thermal block behaves as a proxy for fuel availability.

What survives the correction is the central result. Pre-fire thermal dryness adds a real and
repeatable within-region increment, +0.06 to +0.15 ROC-AUC over a static and near-static baseline in
all five regions, surviving spatial blocking at about 5 km and a predictor window closed up to two
weeks before the first labelled burning. It does not travel. Equalised transfer of 0.617 against
within-region skill near 0.87 leaves most of the gap intact; the paired cross-region contribution is
+0.004 [−0.028, +0.036] with a sign that varies by pair; and the static baseline transfers at 0.537
against the thermal model's 0.541, so this is not a peculiarity of dynamic predictors. Removing the
two reversing predictors costs −0.081 of within-region skill, three quarters of it elevation, and
changes transfer by +0.014, whose interval spans zero: a local cost is measured, no compensating
transfer gain is, and no exchange between them is demonstrated.

The shortfall cannot be anticipated. None of the twenty diagnostics tested ordered the matrix on the
marginal, niche or regime families, and on ten effective pairs those nulls mean not shown to order
transfer rather than shown not to. Two conditional variants did carry intervals excluding zero, but
they rest on a data-selected subset of predictors, require burned labels on both sides, and — on the
equalised frames of the first finding — become unanimous and variance-free, so they were reading the
study rectangles rather than the transfer. No diagnostic tested here has been shown to work as a screen. Label-free
alignment compresses fourteen of twenty directions towards chance rather than repairing them, and
pooled multi-region training does not escape it either. Supervised recalibration works but is not
cheap: thirty-two labelled 5 km blocks recover 85 to 89 % of the target's matched ceiling in three
of six directions, and at the top budget the labelled set already holds most of one region's burned
cells.

Two practical consequences follow. Report local skill and portability separately, since a predictor
block worth a large within-region increment may contribute nothing distinguishable from zero across
regions. And fix the evaluation frame by an explicit accessible-area rule before any predictor is
computed, because a frame chosen for convenience can manufacture both a transfer failure and a
mechanism to explain it. Three extensions are left for future work: temporal transfer,
meteorological covariates, and physically normalised dryness variables. Each is a step towards the
self-calibrating thermal monitoring system that motivated this study.
