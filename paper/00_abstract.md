# Abstract

> **Drafting note.** Every number traces to `04_results.md`; no value appears here that is not
> established there. Structural rules applied: the load-bearing sentence is the contrast-pair
> evidence (exempt from sample-size objections); the narrative is a diagnostic question asked and
> answered, not a negative result; the label requirement of the conditional index is stated
> explicitly. **Trimmed 2026-08-13 from 271 to ~250 words**, and the same-geography two-event
> control (§4.8) was added — it is the strongest answer to the "different places are simply
> different systems" objection and was missing from the previous version.
>
> **Style, from 2026-08-13.** Rewritten under the house rule in `paper/STYLE.md`: no em or en
> dashes, short simple sentences, passive voice where it reads naturally, plain words except for
> technical terms that cannot be simplified without losing meaning. Current measurements: 250
> words, 0 dashes, mean sentence 12 words, longest 20.
>
> **Consistency pass 2026-08-13.** Two corrections. (i) The diagnostics paragraph contradicted
> itself: it said none of the twenty candidates ordered transfer and then named the conditional
> index that does. It now states what §4.4 states, that only two of the twenty had bootstrap
> intervals excluding zero and both are conditional, and that the marginal, niche-overlap and regime
> families failed to order the matrix. (ii) "Static terrain and fuel baseline" was inaccurate,
> because the vegetation-index predictor is a predictor-window median composite (§3.4). It is now a
> "static and near-static terrain, fuel and greenness baseline". No number changed.
>
> **Blocking-scale pass 2026-08-13.** "Ten directions improved with bootstrap support and seven
> degraded" was the 2-cell (~1 km) split. `paper/transfer_ci_blocksize.md` shows it becomes 6 / 4 /
> 10 at 10-cell (~5 km) blocking, and that even at 2-cell the boundary between 10 and 11 positive
> turns on a bound of −0.00045. No count is now quoted in the abstract at all. The sentence rests on
> the sign instability instead, which §4.7g shows to be invariant to the blocking. "only +0.004" lost
> its "only" to stay inside the word limit. Recount: 250 words.
>
> **Referee round 2, 2026-08-14. Now 322 words, and that is a deliberate decision that must be
> revisited once the guide is read.** Six changes, each closing a point raised by the internal panel.
> (i) "+0.004" now carries "with an interval spanning zero", because the paper's headline quantity
> had no interval anywhere. (ii) The blocking-invariant result is stated: paired deltas −0.148 to
> +0.132, twelve positive and eight negative. (iii) The feature-removal debit (−0.081 within-region,
> supported in every region) is given, because it is the only measured debit in the paper and the
> trade-off claim needs one; the +0.014 transfer side is stated with its interval, which spans zero,
> so no exchange rate is asserted (referee round 3, item 1.1). (iv) The Muğla two-event sentence no longer says the failure is "not
> caused by comparing different places"; it says place is what the design holds fixed, and names the
> season/year confound. (v) The niche-overlap contrast is marked as a point-estimate statement, which
> §4.5, §5.3 and §6 already do. (vi) The label taxonomy is corrected: niche and regime measures need
> target labels too, so the marginal family is the only pre-deployment family, and it is the one that
> fails. The few-shot recovery result was added because it is now §4.10 rather than supplementary
> only. **If the limit turns out to be 250, cut in this order:** the paired-delta span, the
> recovery-curve sentence, then the season/year clause. Do not cut the interval on +0.004 or the
> point-estimate qualifier.
>
> **Round 3 application, 2026-08-14. Now 329 words.** Three corrections entered and the length was
> held near the previous deliberate 322 by trimming elsewhere. (i) The two-event sentence no longer
> implies only the event differs: season, year *and population* differ, because the 2022 arm is the
> 2021 arm with the 2021 scar removed (Tier 0.5). (ii) "Only pushed transfer towards chance" is
> replaced by the counted statement, fourteen of twenty (Tier 0.3); the five upward exceptions all
> involve Montiferru and the sixth, Manavgat to Muğla, moves downward, which is why the abstract
> gives the count rather than a universal. (iii) The paired-delta span was cut per the documented cut
> order, and the recovery-curve sentence was folded into the closing paragraph rather than dropped,
> because the closing claim about the price of the failure needs it. **If the limit turns out to be
> 250, cut next:** the niche-overlap point-estimate sentence, then the recovery figures in the last
> sentence. Do not cut the interval on +0.004, the fourteen-of-twenty count, or the population clause
> in the two-event sentence.
>
> **Rewritten 2026-08-14 for the three-finding structure.** 319 words. Each finding now carries its
> own signposted paragraph, which is what the cut manuscript is organised around. **If the limit turns
> out to be 250, cut in this order:** the niche-overlap sufficiency clause, then the recovery figures
> in the closing sentence, then "with an unstable sign". Do not cut the interval on +0.004, the
> feature-removal exchange, or the disjoint-intervals clause in the third finding.
>
> **Referee round 4, 2026-08-14. Now ~340 words.** Four independent referees; every claim applied
> here was re-derived from the frozen artefacts first (13 checked, 13 confirmed, 0 refuted — see
> `REFEREE_ROUND_4.md`). Six changes. (i) The heading no longer says the block "buys" and "spends":
> with the transfer side a null, there are two nulls on the portability axis and no exchange, so the
> paragraph now states a measured local cost and no measured transfer gain. (ii) **The baseline
> transfer mean enters the abstract** (0.537 against 0.541). It was absent from the whole manuscript
> and it is the decisive control for the thesis: the static predictor class the paper argues should
> travel does not travel either. (iii) The two removed predictors are named, and elevation's
> dominance of the −0.081 is stated, because elevation is a *baseline* variable and a reader would
> otherwise attribute the whole debit to the thermal block. (iv) Both feature-removal figures are
> marked post-selection. (v) The two-event arm is downgraded to corroborating and its eleven
> positive-carrying blocks are stated, because Table 3's own note sets sixteen as the floor. (vi) The
> niche-overlap sentence gains the point-estimate qualifier that §4.5 and §6 already carry, and
> ρ = 0.84 is correctly attributed to sixteen directions rather than eight pairs (the eight-pair
> value is 0.866). **If the limit turns out to be 250, cut in this order:** the post-selection
> sentence, then the recovery figures, then the baseline-transfer clause — but the baseline number is
> the last of the three to go, since it is the control the panel most faulted its absence.
>
> **Word limit not verified.** Both the Elsevier and ScienceDirect guide-for-authors pages return
> HTTP 403 to automated fetching. A web search reports 400 words for *Ecological Informatics*, but
> that was not corroborated by a second source and is not quoted from the guide itself. 250 is
> therefore used as a deliberately safe target: it satisfies a 400-word limit and a 250-word one
> alike. **Check the guide before submission**; if 400 is confirmed, there is room to restore the
> per-region robustness detail and the domain-classifier ceiling.

Pre-fire thermal dryness separates a fire year from a normal year. Models built on it are rarely
tested outside the region they were fitted in. Five Mediterranean wildfire regions were analysed
here, on about 500 m cells, with MCD64A1 labels and spatially blocked validation. Six pre-fire
thermal predictors were added to a terrain, fuel and greenness baseline.

**The local skill does not travel, and almost all of it is lost before the region changes.**
Within-region ROC-AUC rose by +0.056 to +0.153 in every region. Across twenty ordered transfer directions the same
block contributed +0.004 [−0.028, +0.036]. That is not distinguishable from zero, and its sign
changes from pair to pair. The static baseline transferred no better, at 0.537 against 0.541. Four evaluations
differing in one respect at a time give 0.797 for blocked cross-validation, 0.574 for a
within-region half-split on the same fire, 0.552 for a fire held out inside its own region, and
0.541 across regions. **The fall of 0.223 occurs with the fire held constant**, and withholding the
fire and then changing the region add 0.022 and 0.011. Separation does not order the matrix either,
at ρ = −0.32 with an interval spanning zero, the nearest pair being among the worst. A fire held out
inside its own region cannot be distinguished from a region 2,800 km away. Two predictors
reverse their association between regions: elevation and the LST anomaly. Removing them cost −0.081
of within-region skill, supported in every region and mostly due to elevation. It changed transfer
by +0.014 [−0.017, +0.045]. Both figures are post-selection estimates. A local cost is measured. No
compensating transfer gain is.

**The failure is invisible to the diagnostics that can be run before deployment.** Twenty candidate
diagnostics were rank-correlated against observed transfer. Only two had intervals excluding zero,
and both were conditional. The stronger one measures agreement in the sign of each predictor's
association (Spearman ρ = 0.84 over sixteen directions). No marginal measure was shown to order the
matrix, including predictor-space dissimilarity. At the point estimates, the pair with the highest
burned-niche overlap failed in both directions, while the lowest transferred in both. Signed
associations need labels on both sides. The family that works is therefore the one a practitioner
does not have.

**The mechanism is a reversal of sign.** Predictors do not weaken across regions. They reverse the
direction of their association with burning. A distance in predictor space cannot see that. The same
reversal appears inside one study area, between two fires eleven months apart on an identical grid.
That arm rests on one fire and eleven positive-carrying blocks, so it corroborates rather than
establishes.

Label-free alignment pushed fourteen of twenty directions towards chance rather than repairing them.
Transfer skill has to be measured, not inferred from similarity. The price is target labels:
thirty-two labelled 5 km blocks recovered 85 to 89 % of the target's matched ceiling in three of six
directions.
