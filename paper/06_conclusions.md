# 6. Conclusions

> **Drafting note.** Deliberately short; states conclusions and the practical recipe without
> re-arguing the Discussion. Every number traces to `04_results.md`.

Pre-fire thermal dryness adds a real, replicable increment to burned-area discrimination: +0.06
to +0.15 ROC-AUC over a static baseline in five Mediterranean regions, surviving ~10 km spatial
blocking and a predictor window closed up to two weeks before the first labelled burning. That
skill is local. Paired per direction, the same predictor block contributes nothing on average to
cross-region transfer (+0.004 over twenty directions), harms seven directions with bootstrap
support, and is the swing factor at the chance line. The failure is conditional — the direction
of the dryness-burning relationship changes between regions — which is why it is invisible to
every label-free similarity diagnostic we tested (predictor-space distance, domain separability,
niche overlap, regime structure), why label-blind adaptation compresses transfer towards chance
instead of repairing it, and why pooled multi-region training does not escape it.

The practical implication is a change in what one checks before transferring a dynamic-state
fire model. The question is not whether the target region lies inside the source's environmental
envelope — the pair with the highest envelope overlap in our matrix failed in both directions,
and the pair with the lowest transferred in both — but whether the signed feature-response
directions agree. That check requires a labelled probe in the target: a modest burned-area
record is sufficient to compute signed associations, and the same labels then support the
supervised recalibration that label-free alignment cannot deliver. Where no target labels exist,
transfer performance of such models should be treated as unknown rather than inferred from
similarity.

For model builders, the trade-off should be priced explicitly: predictor blocks that maximise
within-region skill can carry the largest transfer cost, and reporting only within-region
validation conceals that cost entirely. Extending the test to temporal transfer, meteorological
covariates and physically normalised dryness variables — steps towards the self-calibrating
thermal monitoring system that motivated this work — remains for future studies.
