# 6. Conclusions


Pre-fire thermal dryness adds a real and repeatable increment to burned-area discrimination. Across
five Mediterranean regions, ROC-AUC was raised by +0.06 to +0.15 over a static and near-static
terrain, fuel and greenness baseline. That baseline's only time-varying member is the
vegetation-index composite. The gain
survived spatial blocking at about 10 km. It also survived a predictor window closed up to two weeks
before the first labelled burning.

That skill is local. Paired per direction, the same predictor block adds nothing distinguishable
from zero to cross-region transfer. The mean is +0.004 over twenty directions and its interval spans
zero under every resampling unit the design permits. Its contribution changes sign from one
direction to another. The paired deltas run from −0.148 to +0.132, twelve positive and eight
negative, at either blocking scale. At the conservative 5 km blocking, five to six directions are
helped and three to four are harmed with interval support, with the rest carrying no verdict. The
block is also the swing factor at the chance line. Removing the two reversing predictors buys +0.014
of mean transfer for −0.081 of mean within-region skill, which is the exchange rate of the
trade-off.

The failure is conditional. The direction of the link between dryness and burning changes from one
region to another. None of the similarity diagnostics tested here ordered the transfer
matrix: predictor-space distance, domain separability, niche overlap and regime structure all
failed. On ten effective pairs those null results mean not shown to order transfer, rather than
shown not to. It is also why label-blind adaptation compresses transfer towards chance instead of
repairing it, and why pooled multi-region training does not escape it.

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
supervised recalibration that label-free alignment cannot deliver is not cheap. Section 4.10 prices
it for three regions: thirty-two labelled 5 km blocks recovered 85 to 89 % of the target ceiling in
four of six directions, and at its top budget the labelled set already holds most of one target
region's burned cells. Where no target labels exist, the transfer performance of such
models should be treated as unknown rather than inferred from similarity.

For model builders, the trade-off should be priced openly. A predictor block that buys large
within-region skill can carry a transfer cost of the opposite sign. Reporting only within-region
validation hides that cost completely. Three extensions are left for future work: temporal transfer,
meteorological covariates, and physically normalised dryness variables. Each is a step towards the
self-calibrating thermal monitoring system that motivated this study.
