# 6. Conclusions

> **Drafting note.** Deliberately short; states conclusions and the practical recipe without
> re-arguing the Discussion. Every number traces to `04_results.md`.
> **Style pass 2026-08-13** (`paper/STYLE.md`): no dashes, short sentences, passive where it reads
> naturally. Every number and every hedge is unchanged.

Pre-fire thermal dryness adds a real and repeatable increment to burned-area discrimination. Across
five Mediterranean regions, ROC-AUC was raised by +0.06 to +0.15 over a static baseline. The gain
survived spatial blocking at about 10 km. It also survived a predictor window closed up to two
weeks before the first labelled burning.

That skill is local. Paired per direction, the same predictor block adds nothing on average to
cross-region transfer, at +0.004 over twenty directions. Seven directions are harmed with bootstrap
support. The block is also the swing factor at the chance line.

The failure is conditional. The direction of the link between dryness and burning changes from one
region to another. This is why the failure is invisible to every label-free similarity diagnostic
tested here, including predictor-space distance, domain separability, niche overlap and regime
structure. It is also why label-blind adaptation compresses transfer towards chance instead of
repairing it, and why pooled multi-region training does not escape it.

The practical implication is a change in what is checked before a dynamic-state fire model is
transferred. The question is not whether the target region lies inside the source's environmental
envelope. In our matrix, the pair with the highest envelope overlap failed in both directions,
while the pair with the lowest overlap transferred in both. The question is whether the signed
feature-response directions agree.

That check requires a labelled probe in the target region. A modest burned-area record is enough to
compute signed associations. The same labels then support the supervised recalibration that
label-free alignment cannot deliver. Where no target labels exist, the transfer performance of such
models should be treated as unknown rather than inferred from similarity.

For model builders, the trade-off should be priced openly. Predictor blocks that give the largest
within-region skill can carry the largest transfer cost, and reporting only within-region validation
hides that cost completely. Three extensions are left for future work: temporal transfer,
meteorological covariates, and physically normalised dryness variables. Each is a step towards the
self-calibrating thermal monitoring system that motivated this study.
