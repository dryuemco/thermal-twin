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
zero under all four between-direction resampling units we computed. Its contribution changes sign
from one direction to another. The paired deltas run from −0.148 to +0.132, twelve positive and eight
negative. At the conservative 5 km blocking, five to six directions are helped and three to four are
harmed with interval support, with the rest carrying no verdict. The block is also the swing factor
at the chance line.

Two controls fix the meaning of all this. The baseline arm transfers at a mean of 0.537 against the
thermal model's 0.541, so the static predictor class is not portable here either. And three evaluations on identical cells locate
where it goes: 0.634 with the held-out burn scar in the training data, 0.552 with it withheld, and
0.555 for a model fitted 306 to 2,802 km away. The honest summary is therefore not that these
predictors fail to cross regions. **The failure is a property of contiguous spatial holdout**: the
fire-specific residual is +0.082 [−0.011, +0.175] and the 2,800 km costs −0.003 [−0.075, +0.069].
Two thirds of the apparent collapse from a region-wide 0.782 is the evaluation area itself, which is
34 to 87 per cent burned against 3.8 to 28.7 for a region. Six directions are nonetheless anti-predictive with
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
results mean not shown to order transfer, rather than shown not to. Label-blind adaptation compresses transfer towards
chance rather than repairing it, though its mean sits at the reference a model can reach on an
unseen scar, so it is regressing the matrix onto that level rather than failing beneath it. Pooled
multi-region training does not escape it either.

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
it for three regions: thirty-two labelled 5 km blocks recovered 85 to 89 % of the target's matched ceiling in
three of six directions, 51 to 57 % in two more and 30 % in the sixth, and at its top budget the
labelled set already holds most of one target region's burned cells. Where no target labels exist, the transfer performance of such
models should be treated as unknown rather than inferred from similarity.

For model builders, local skill and portability should be reported separately rather than assumed to
travel together. A predictor block worth a large within-region increment may contribute nothing
distinguishable from zero across regions, with a sign that varies by pair, and reporting only
within-region validation hides that completely. Three extensions are left for future work: temporal transfer,
meteorological covariates, and physically normalised dryness variables. Each is a step towards the
self-calibrating thermal monitoring system that motivated this study.
