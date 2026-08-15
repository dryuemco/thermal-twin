# Abstract



Pre-fire thermal dryness separates a fire year from a normal year, but models built on it are rarely
tested outside the region where they were fitted. Five Mediterranean wildfire regions were analysed
on about 500 m cells, with MCD64A1 labels and spatially blocked validation, adding six thermal
predictors to a terrain, fuel and greenness baseline.

**Local skill does not travel, and most of it is lost before the region changes.** Within-region
ROC-AUC rose by +0.056 to +0.153 under blocked cross-validation, but by +0.022 [−0.032, +0.077] when
a whole burn scar is withheld, and by +0.004 [−0.028, +0.036] across twenty transfer directions,
with a sign that changes from pair to pair. The static baseline transferred no better, 0.537 against
0.541, so this is not a property of the dynamic block. On **identical cells**, a model holding the held-out scar scores 0.634, one without it 0.552 and one
fitted 306 to 2,802 km away 0.555, so neither withholding the fire nor crossing the region is shown
to cost anything. What is measurable is the evaluation area itself, worth **0.143 [+0.077, +0.208]**
of the fall from a region-wide 0.776, because its negatives are all fire-adjacent and therefore the
hardest in the region.

**The failure is invisible before deployment.** Of twenty candidate diagnostics only two had
intervals excluding zero; both measure sign agreement over a selected feature subset (rho = 0.84,
post-selection) and both need target labels. No marginal measure ordered the matrix, so the family
that works is the one a practitioner does not have.

**Most of the apparent mechanism is an artefact of the evaluation frame.** Five predictors reverse
direction between regions on the frames as drawn, but those frames enclose very different far
fields, from 2 % to 63 % of cells beyond 10 km of any fire, on higher ground. A 10 km collar, which
drops no burned cells, makes all five agree in sign on elevation, LST and TVDI, lifts transfer from
0.540 to 0.617, drops the directions below chance from six to one, and leaves no reversal
bootstrap-supported under our own criterion. The agreed sign is not the one the dryness framing
predicts: hotter surfaces burned less everywhere, surviving stratification within elevation and
greenness.

Label-free alignment pushed fourteen of twenty directions towards chance rather than repairing them.
Transfer skill has to be measured, not inferred from similarity.
