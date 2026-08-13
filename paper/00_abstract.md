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
> technical terms that cannot be simplified without losing meaning. Current measurements: 251
> words, 0 dashes, mean sentence 12 words, longest 24.
>
> **Word limit not verified.** Both the Elsevier and ScienceDirect guide-for-authors pages return
> HTTP 403 to automated fetching. A web search reports 400 words for *Ecological Informatics*, but
> that was not corroborated by a second source and is not quoted from the guide itself. 250 is
> therefore used as a deliberately safe target: it satisfies a 400-word limit and a 250-word one
> alike. **Check the guide before submission**; if 400 is confirmed, there is room to restore the
> per-region robustness detail and the domain-classifier ceiling.

Pre-fire thermal dryness separates a fire year from a normal year. It is measured by land surface
temperature, its anomalies against a climatology, and thermal and optical dryness indices. Models
built on these predictors are rarely tested outside their training region.

Five Mediterranean wildfire regions were analysed on about 500 m cells, with MCD64A1 labels and
spatially blocked validation. Six pre-fire thermal predictors were added to a static
terrain and fuel baseline. Within every region, ROC-AUC was raised by +0.06 to +0.15. The gain
survived coarser blocks and an earlier predictor window.

The predictors were then transferred between regions. Their mean contribution over twenty ordered
directions was only +0.004. Ten directions were improved with bootstrap support and seven
were degraded. Local skill and portability are therefore traded.

The failure is conditional, not distributional, and not caused by comparing different places.
Inside one identical study area, two fires eleven months apart reversed the link between elevation
and burning, with no overlap in their bootstrap intervals.

Twenty candidate diagnostics were tested before transfer. None ordered transfer
performance. The pair with the highest burned-niche overlap failed in both directions. The pair
with the lowest overlap transferred in both. Only the agreement in the sign of each predictor's
association tracked transfer (Spearman ρ = 0.84). Label-blind adaptation, by region-wise
standardisation and CORAL, only pushed the directions towards chance. Signed associations need
burned labels in both regions, so the test is a labelled probe, not a label-free screen.
Transferability must therefore be measured, and measured conditionally.
