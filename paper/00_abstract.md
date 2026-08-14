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
> **Word limit not verified.** Both the Elsevier and ScienceDirect guide-for-authors pages return
> HTTP 403 to automated fetching. A web search reports 400 words for *Ecological Informatics*, but
> that was not corroborated by a second source and is not quoted from the guide itself. 250 is
> therefore used as a deliberately safe target: it satisfies a 400-word limit and a 250-word one
> alike. **Check the guide before submission**; if 400 is confirmed, there is room to restore the
> per-region robustness detail and the domain-classifier ceiling.

Pre-fire thermal dryness, measured by land surface temperature, its anomalies and dryness indices,
separates a fire year from a normal year. Models built on it are rarely tested outside their
training region.

Five Mediterranean wildfire regions were analysed on about 500 m cells, with MCD64A1 labels and
spatially blocked validation. Six pre-fire thermal predictors were added to a static and near-static
terrain, fuel and greenness baseline. Within every region, ROC-AUC rose by +0.06 to +0.15, and the
gain survived coarser blocks and an earlier predictor window.

The same predictors were then transferred between regions. Their mean contribution over twenty
ordered directions was +0.004, with an interval spanning zero. Removing the two reversing predictors
cost −0.081 of within-region skill, supported in every region, and changed mean transfer by +0.014,
whose pair-clustered interval spans zero. The debit is measured and the credit is not.

The failure is conditional. Inside one study area, two fires eleven months apart reversed the
elevation-burning link, with disjoint bootstrap intervals. Season, year and population all differ
there, so place alone is what the design holds fixed.

Twenty candidate diagnostics were rank-correlated against observed transfer. Only two had bootstrap
intervals excluding zero, both conditional, the stronger being agreement in the sign of each
predictor's association (Spearman ρ = 0.84 over eight pairs). No marginal, niche-overlap or regime
measure ordered the matrix; at the point estimate the highest-overlap pair failed both ways and the
lowest transferred both ways. Label-blind adaptation by standardisation and CORAL pushed transfer
towards chance in fourteen of the twenty directions. Niche and regime measures need labels in both
regions too, so only the marginal family can run before deployment, and it fails.

Transfer skill therefore has to be measured, not inferred from similarity. What carries the
information is conditional, so the price is target labels, not better unsupervised alignment:
thirty-two labelled target blocks recovered 85 to 89 % of the ceiling in three of six directions
and 30 to 57 % in the rest.
