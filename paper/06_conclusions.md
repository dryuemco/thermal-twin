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
study rectangles rather than the transfer. No diagnostic tested here survives as a screen. Label-free
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
