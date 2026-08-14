# 6. Conclusions


Pre-fire thermal dryness adds a real and repeatable increment to burned-area discrimination. Across
five Mediterranean regions, ROC-AUC was raised by +0.06 to +0.15 over a static and near-static
terrain, fuel and greenness baseline. That baseline's only time-varying member is the
vegetation-index composite. The gain
survived spatial blocking at about 5 km, the coarsest scale this design supports as an interval. It
also survived a predictor window closed up to two weeks
before the first labelled burning.

That skill is local. Paired per direction, the same predictor block adds nothing distinguishable
from zero to cross-region transfer. The mean is +0.004 over twenty directions and its interval spans
zero under all four between-direction resampling units we computed. Its contribution changes sign
from one direction to another. The paired deltas run from −0.148 to +0.132, twelve positive and eight
negative. At the conservative 5 km blocking, five to six directions are helped and three to four are
harmed with interval support, with the rest carrying no verdict. The block is also the swing factor
at the chance line.

Two controls fix the meaning of all this. The baseline arm transfers at a mean of 0.537 against the
thermal model's 0.541, so the static predictor class is not portable here either. And four evaluations differing in one respect
at a time locate where it goes: 0.797 under blocked cross-validation, 0.574 on a half-split of the
**same fire**, 0.552 on a fire held out inside its own region, and 0.541 across regions. The honest
summary is therefore not that these predictors fail to cross regions. **Almost all of the loss, 0.223
of 0.256, occurs with the fire held constant**, as soon as the held-out cells stop being interleaved
with training cells; withholding the fire and then changing the region add 0.022 and 0.011. Those
last three are not distinguishable by this design, which rests on eight scar arms with no interval
and one region that supports the control cleanly. Six directions are nonetheless anti-predictive with
interval support, which no account of merely lost skill explains. The one-event-per-region design
also means that a fire cannot be separated here from the season and meteorology that produced it.

Removing the two reversing predictors, elevation and the LST anomaly, costs −0.081 of mean
within-region skill, with interval support in every region and roughly three quarters of it
attributable to elevation, a baseline terrain variable; it changes mean transfer by +0.014, an
estimate whose interval spans zero. A local cost is measured. No compensating transfer gain is, on
either arm, so no exchange between the two is demonstrated.

The relationship itself is also unstable, and that is a separate finding. The direction of the link
between dryness and burning changes from one region to another, with bootstrap support for two
predictors. This is measured on univariate associations and does not depend on any fitted model, so
the distance result above neither establishes it nor removes it. What the two together rule out is
the comfortable reading in which regional concept shift explains the whole transfer matrix. Most of
its *level* is reached without leaving a region. What varies around that level, including six
anti-predictive directions, is not explained by separation and is where the instability matters.

None of the similarity diagnostics tested here ordered the transfer matrix: predictor-space distance,
domain separability, niche overlap and regime structure all failed. On ten effective pairs those null
results mean not shown to order transfer, rather than shown not to. Label-blind adaptation compresses
transfer towards chance instead of repairing it, and pooled multi-region training does not escape
it.

The practical implication is a change in what is checked before a dynamic-state fire model is
transferred. The question is not whether the target region lies inside the source's environmental
envelope. In our matrix, the pair with the highest envelope overlap failed in both directions, and
the pair with the lowest overlap transferred in both. Both statements are made at the point
estimate. The question is whether the signed feature-response directions agree.

That check requires a labelled probe in the target region, and so, on inspection, do the niche and
regime diagnostics. Only the marginal family can be computed before any target label exists, and it
is the family that failed. How large the probe has to be is not established here, so no label budget
is claimed. A signed association with a usable interval may
need fewer labels than a refitted model, but that was not tested. What is clear is that the
supervised recalibration that label-free alignment cannot deliver is not cheap. Section 4.9 prices
it for three regions: thirty-two labelled 5 km blocks recovered 85 to 89 % of the target ceiling in
three of six directions, 51 to 57 % in two more and 30 % in the sixth, and at its top budget the
labelled set already holds most of one target region's burned cells. Where no target labels exist, the transfer performance of such
models should be treated as unknown rather than inferred from similarity.

For model builders, local skill and portability should be reported separately rather than assumed to
travel together. A predictor block worth a large within-region increment may contribute nothing
distinguishable from zero across regions, with a sign that varies by pair, and reporting only
within-region validation hides that completely. Three extensions are left for future work: temporal transfer,
meteorological covariates, and physically normalised dryness variables. Each is a step towards the
self-calibrating thermal monitoring system that motivated this study.
