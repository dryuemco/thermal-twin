# 6. Conclusions

> **Drafting note.** Deliberately short; states conclusions and the practical recipe without
> re-arguing the Discussion. Every number traces to `04_results.md`.
> **Style pass 2026-08-13** (`paper/STYLE.md`): no dashes, short sentences, passive where it reads
> naturally. Every number and every hedge is unchanged.
>
> **Consistency pass 2026-08-13.** Three changes, no numbers added or altered. (i) "A modest
> burned-area record is enough to compute signed associations" overclaimed against Supplementary
> S1, whose limit 4 shows the top budget holding 880 of Bejís's 1,100 burned cells. Two claims were
> being conflated. The size of the labelled probe needed for a signed association is nowhere
> established in this manuscript, so no budget is now claimed for it, and the supervised
> recalibration is stated as expensive with an explicit pointer to Supplementary S1. Discussion §5.5
> says the few-shot analysis is not drawn on there; the pointer here is to the supplement, not to
> §5.5. (ii) "Static baseline" became "static and near-static terrain, fuel and greenness baseline",
> since the vegetation-index predictor is a predictor-window median composite (§3.4). (iii)
> "Predictor blocks that give the largest within-region skill can carry the largest transfer cost"
> used the same untested comparative removed from §1 of the Introduction. It now says the cost can
> be of the opposite sign.
>
> **Blocking-scale pass 2026-08-13** (`paper/transfer_ci_blocksize.md`, Results §4.8g and Table
> R13). "Seven directions are harmed with bootstrap support" was the 2-cell (~1 km) count. It now
> leads with the blocking-invariant statement, the sign change and the −0.148 to +0.133 span at
> twelve positive and eight negative, and gives the conservative 5 km verdicts of six helped, four
> harmed and ten with no verdict. The envelope-overlap contrast in the practical-implication
> paragraph gained "at the point estimate", because the low-overlap pair carries no interval verdict
> at 5 km. The swing-factor sentence is unchanged, since it rests on point estimates.

Where a fire model is scored decides what it appears to know. Holding the model, its predictors and
its fitting fixed and changing only which cells are scored, moving from a whole study region to the
burn scar and its 2 km collar costs **0.143 ROC-AUC**. A control isolates the cause as the
composition of the negative pool rather than class balance. The effect is larger than the
predictor-block increments this literature publishes as findings, so a region-wide validation figure
should be read as an upper bound on what a model achieves where fire actually occurs, and reported
as one.

That correction is not only other people's problem. Applied to our own five-region matrix it
withdraws three of our claims. The study areas enclose very unequal far fields, and equalising them
to a 10 km collar lifts mean transfer from 0.540 to 0.617, reduces the
directions below chance, and leaves no sign reversal supported under our own criterion — including
the one arm that held place fixed, two fires in the same study area eleven months apart, which we
had wrongly exempted because its geography was constant while its evaluation frame was not. What had
looked like a reversed predictor-burning relationship was mostly a statement about how five
rectangles were drawn.

What survives is the central result. Pre-fire thermal dryness adds a real and repeatable
within-region increment in all five regions, surviving spatial blocking at about 5 km and a
predictor window closed up to two weeks before the first labelled burning. It does not travel: on
matched frames and matched blocking, equalised transfer of 0.617 falls 0.155 short of the
within-region reference, the paired cross-region contribution spans zero with a sign that varies by
pair, and the static baseline transfers no better than the dynamic one, so this is not a peculiarity
of thermal predictors. The shortfall also cannot be anticipated: none of twenty diagnostics from
five families was shown to order the matrix, and the two that appeared to do so require target
labels on both sides and stop ordering transfer once the frames are comparable. Label-free alignment compresses most directions
towards chance rather than repairing them, and supervised recalibration works but is not cheap.

Two limits should be read with all of this. The agreed thermal direction is the opposite of the one
the dryness framing predicts — hotter pre-fire surfaces burned less in every region, and holding
greenness does not remove it while holding temperature reverses greenness in two regions — so on
this cohort the absolute channels behave as static land-surface descriptors rather than as a dryness
index. And with one fire per region, and the single arm that held place fixed now withdrawn, this
design measures a transfer shortfall but cannot attribute it to region rather than to event.

Two practical consequences follow. Report local skill and portability separately, since a predictor
block worth a large within-region increment may contribute nothing distinguishable from zero across
regions. And fix the evaluation frame by an explicit accessible-area rule before any predictor is
computed, because a frame chosen for convenience can manufacture both a transfer failure and a
mechanism to explain it. Three extensions are left for future work: temporal transfer, meteorological
covariates, and physically normalised dryness variables.
