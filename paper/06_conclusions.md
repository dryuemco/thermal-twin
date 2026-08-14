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
> **Blocking-scale pass 2026-08-13** (`paper/transfer_ci_blocksize.md`, Results §4.7g and Table
> R13). "Seven directions are harmed with bootstrap support" was the 2-cell (~1 km) count. It now
> leads with the blocking-invariant statement, the sign change and the −0.148 to +0.132 span at
> twelve positive and eight negative, and gives the conservative 5 km verdicts of six helped, four
> harmed and ten with no verdict. The envelope-overlap contrast in the practical-implication
> paragraph gained "at the point estimate", because the low-overlap pair carries no interval verdict
> at 5 km. The swing-factor sentence is unchanged, since it rests on point estimates.

Pre-fire thermal dryness adds a real and repeatable increment to burned-area discrimination. Across
five Mediterranean regions, ROC-AUC was raised by +0.06 to +0.15 over a static and near-static
terrain, fuel and greenness baseline. That baseline's only time-varying member is the
vegetation-index composite. The gain
survived spatial blocking at about 5 km, the coarsest scale this design supports as an interval. It
also survived a predictor window closed up to two weeks
before the first labelled burning.

That skill is local. Paired per direction, the same predictor block adds nothing distinguishable
from zero to cross-region transfer. The mean is +0.004 over twenty directions and its interval spans
zero under every resampling unit the design permits. Its contribution changes sign from one
direction to another. The paired deltas run from −0.148 to +0.132, twelve positive and eight
negative, at either blocking scale. At the conservative 5 km blocking, five to six directions are
helped and three to four are harmed with interval support, with the rest carrying no verdict. The
block is also the swing factor at the chance line. Removing the two reversing predictors costs
−0.081 of mean within-region skill, with interval support in every region, and changes mean transfer
by +0.014, an estimate whose interval spans zero. The cost of the trade-off is measured; the return
is not.

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
supervised recalibration that label-free alignment cannot deliver is not cheap. Section 4.9 prices
it for three regions: thirty-two labelled 5 km blocks recovered 85 to 89 % of the target ceiling in
three of six directions, 51 to 57 % in two more and 30 % in the sixth, and at its top budget the
labelled set already holds most of one target region's burned cells. Where no target labels exist, the transfer performance of such
models should be treated as unknown rather than inferred from similarity.

For model builders, the trade-off should be priced openly. A predictor block that buys large
within-region skill can carry a transfer cost of the opposite sign. Reporting only within-region
validation hides that cost completely. Three extensions are left for future work: temporal transfer,
meteorological covariates, and physically normalised dryness variables. Each is a step towards the
self-calibrating thermal monitoring system that motivated this study.
