# A positive control for the transfer path, and what it costs the interpretation

**Why this was run.** An external referee reduced their review to one demand: show a configuration
where this pipeline registers transfer it ought to register. Every transfer number in the manuscript
is a failure, so two explanations fit the evidence equally well. Either the relationship does not
travel, or the evaluation cannot detect travel. Nothing in the paper separates them.

Run 2026-08-14. Script `positive_control.py`, result `positive_control.json`.

## Design

Within each region the modelled cells are cut in half by a straight line, a model is fitted on one
half and applied to the other with **no refit, no recalibration and no threshold selection**, which
is the same label-free protocol the cross-region arms use. The relationship is shared by
construction: same region, same season, same fire, same processing chain, same units. Both split
axes are run, east-west and north-south, and both directions of each, giving eighteen usable splits
across five regions.

**The code path is the published one.** Fitted through the same pipeline, it reproduces the frozen
cross-region AUCs exactly: Manavgat to Bejís 0.3258, Muğla to Manavgat 0.4010, Evia to Manavgat
0.6858, each to 0.000000. The numbers below are therefore on the same footing as Table 4's.

## Result

| Arm | Mean AUC | Range |
|---|---:|---|
| Within-region, spatially blocked CV, 1 km blocks (Table 3) | 0.859 to 0.918 | per region |
| **Within-region, contiguous half-split, no refit** | **0.574** | **0.294 to 0.750** |
| Cross-region transfer, thermal (Table 4) | 0.541 | 0.326 to 0.686 |
| Cross-region transfer, baseline (Section 4.3) | 0.537 | |

Two of the eighteen splits exceed 0.7. Fifteen exceed 0.5. One, Muğla split north-south and applied
southward, returns **0.294**, further below chance than any cross-region direction in the paper. The
baseline feature set behaves the same way, at a mean of 0.547.

## Reading, stated against our own interest

**The harness is not broken.** It reproduces the frozen numbers exactly, and it returns 0.75 on the
easiest split. So "the evaluation cannot detect travel" is not the explanation.

**But the collapse does not wait for a region boundary.** Skill falls from 0.86 to 0.57 without
leaving the region, as soon as the held-out area is contiguous instead of interleaved. The further
fall on crossing a region boundary, 0.574 to 0.541, is small beside it. Most of what the manuscript
attributes to moving between regions is already present in moving across one region.

This does not overturn the transfer result, and it does not touch the sign-reversal evidence, which
is univariate and does not involve a fitted model at all. What it does is remove an interpretation.
The paper cannot claim that the failure is a property of *regional* difference until it has
separated regional difference from spatial extrapolation, and this control shows the two are
confounded in the present design.

**The honest reframing.** A model of this kind, fitted on one contiguous area and applied to another
with no target labels, returns about 0.57 whether the second area is 10 km away or 1,000 km away.
That is a stronger and more useful statement than the one the paper currently makes, and it is
better supported.

## What this does not settle

The half-split is not a matched comparison. A single fire cut in two means the model trains on part
of one scar and predicts the rest of it, so the target half's burned cells are spatially contiguous
with, and adjacent to, the training half's. Blocked CV interleaves instead, which is why it scores
higher. The right next step is a **distance-stratified curve**: within-region skill as a function of
the separation between training and evaluation cells, with the twenty cross-region points overlaid
at their true separations. If the cross-region points sit on the continuation of that curve, the
transfer failure needs no regional mechanism. If they fall below it, the paper has its evidence.

That curve has not been run. Until it is, this note records a confound, not a conclusion.
