# Abstract

> **Drafting note.** Every number traces to `04_results.md`; no value appears here that is not
> established there. Structural rules applied: the load-bearing sentence is the contrast-pair
> evidence (exempt from sample-size objections); the narrative is a diagnostic question asked and
> answered, not a negative result; the label requirement of the conditional index is stated
> explicitly. **Trimmed 2026-08-13 from 271 to ~250 words**, and the same-geography two-event
> control (§4.8) was added — it is the strongest answer to the "different places are simply
> different systems" objection and was missing from the previous version.
>
> **Word limit not verified.** Both the Elsevier and ScienceDirect guide-for-authors pages return
> HTTP 403 to automated fetching. A web search reports 400 words for *Ecological Informatics*, but
> that was not corroborated by a second source and is not quoted from the guide itself. 250 is
> therefore used as a deliberately safe target: it satisfies a 400-word limit and a 250-word one
> alike. **Check the guide before submission**; if 400 is confirmed, there is room to restore the
> per-region robustness detail and the domain-classifier ceiling.

Pre-fire thermal dryness — land surface temperature, its climatological anomalies and
thermal–optical dryness indices — describes the dynamic state separating a fire year from an
ordinary one, yet models built on such predictors are rarely tested outside their training region.
Across five Mediterranean wildfire regions (~500 m cells, MCD64A1 labels, spatially blocked
validation), six pre-fire thermal predictors added +0.06 to +0.15 ROC-AUC to a static
terrain-and-fuel baseline in every region, robust to coarser blocking and to earlier
predictor-window closure. The same block contributed +0.004 on average across the twenty ordered
transfer directions — improving ten with bootstrap support, degrading seven — and was the swing
factor at the chance line: local skill and portability are traded, not shared. The failure is
conditional rather than distributional, and not an artefact of comparing different places: within
one identical study area, two fires eleven months apart reverse the direction of elevation's
association with burning, their bootstrap intervals disjoint. Of twenty candidate pre-transfer
diagnostics — marginal predictor-space distances, learned domain separability, burned-niche overlap
and fire-regime distances — none ordered transfer performance; the highest-overlap pair failed in
both directions, the lowest-overlap pair transferred in both. Only conditional agreement in the
sign of each predictor's association tracked transfer (Spearman ρ = 0.84), and label-blind
adaptation (region-wise standardisation, CORAL) compressed every direction towards chance rather
than repairing it. Because signed associations require burned labels in both regions, this is a
labelled-probe instrument, not a label-free screen: transferability of dynamic-state fire models
must be measured, and measured conditionally.
