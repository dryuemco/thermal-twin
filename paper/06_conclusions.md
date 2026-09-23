# 6. Conclusions


Where a fire model is scored decides what it appears to know. Model, predictors and fitting were
held fixed, and only the scored cells changed. Moving from a whole study region to the burn scar and
its 2 km collar costs **0.133 ROC-AUC**. A control measures the cause as the composition of the
negative pool rather than class balance. A region-wide validation figure should therefore be read as an upper bound
on what a model achieves where fire actually occurs, and reported as one.

That correction is not only other people's problem. Applied to our own five-region matrix, it shows
four of our own quantities to be properties of the frames. The study areas enclose very unequal far
fields. Equalising them to a 10 km collar lifts mean transfer from 0.527 to 0.589 and reduces the
directions below chance. It removes every supported elevation reversal but one, Manavgat's, which
survives. The same correction applies to the one arm that held place fixed, two fires in one study
area eleven months apart. We had wrongly exempted it, because its geography was constant while its
evaluation frame was not. Its elevation reversal does not survive equalisation, and that arm can
speak only for the year-invariant channels. Much of what had looked like a reversed
predictor-burning relationship was a statement about how five rectangles were drawn.

What survives is the central result. Pre-fire thermal predictors add a real and repeatable
within-region increment in all five regions. It survives spatial blocking at about 5 km, and a
predictor window closed up to two weeks before the first labelled burning. It does not travel. On
matched frames and blocking, equalised transfer of 0.589 falls 0.197 short of the within-region
reference. The paired cross-region contribution spans zero on both frames under the resampling unit
we treat as primary, though not when clustered by target region (Section 4.4), and its sign varies
by pair. Label-free alignment compresses most directions towards chance rather than
repairing them.

Two limits belong with all of this. The thermal direction shared by most regions is the opposite of
the one the dryness framing predicts. Hotter pre-fire surfaces burned less in four of five regions,
and holding greenness does not remove it, while holding temperature reverses greenness in two
regions. On this cohort the absolute channels therefore behave as static land-surface descriptors
rather than as a dryness index. Manavgat is the exception, and there its thermal sign cannot be
separated from its terrain. And with one fire per region, and the single arm that held place fixed
now withdrawn, this design measures a transfer shortfall but cannot attribute it to region rather
than to event.

Three practical consequences follow. Report local skill and portability separately, since a
predictor block worth a large within-region increment may contribute nothing distinguishable from
zero across regions. Fix the evaluation frame by an explicit accessible-area rule before any
predictor is computed, because a frame chosen for convenience can manufacture both a transfer
failure and a mechanism to explain it. And do not screen for transfer by similarity. None of the
twenty diagnostics fixed in advance was shown to order transfer. At the point estimates, the most
similar pair failed in both directions while the least similar transferred above chance. Without
labels from the target region, a model's skill there is unknown, and no measure computed beforehand
stands in for it. With them, skill can be measured and the model recalibrated, but the price depends
on the direction. Thirty-two labelled 5 km blocks recover 83 to 89 % of the target's matched ceiling
in three of six directions, and only 30 to 52 % in the other three (Section S1.19). Those labels
came from the event being predicted, so the curve prices the gap rather than offering a way to close
it before a fire. Whether labels from earlier fires in the same region would serve is not tested
here. Three extensions are left for future work: temporal transfer, meteorological covariates, and
physically normalised dryness variables.
