# Abstract



Pre-fire thermal dryness separates a fire year from a normal year, but models built on it are rarely
tested outside the region where they were fitted. Five Mediterranean wildfire regions were analysed
on about 500 m cells, with MCD64A1 labels and spatially blocked validation, adding six thermal
predictors to a terrain, fuel and greenness baseline.

**Local skill does not travel, and most of it is lost before the region changes.** Within-region
ROC-AUC rose by +0.056 to +0.153 under blocked cross-validation, but by +0.022 [−0.032, +0.077] when
a whole burn scar is withheld, and by +0.004 [−0.028, +0.036] across twenty transfer directions,
with a sign that changes from pair to pair. The static baseline transferred no better, 0.537 against
0.541, so this is not a property of the dynamic block. On **identical cells**, a model holding the held-out scar scores 0.634, one without it 0.552, and
one fitted 306 to 2,802 km away 0.555; the fire-specific residual is bounded at about +0.18 and the
region-crossing effect at about ±0.07, neither being shown to cost anything. Most of the apparent
collapse from a region-wide 0.776 is the evaluation area itself, worth **0.143 [+0.077, +0.208]**,
because its negatives are all fire-adjacent and therefore the hardest in the region.

**The failure is invisible to the diagnostics that can be run before deployment.** Of twenty
candidates rank-correlated against observed transfer, only two had intervals excluding zero, and
both need target labels; the stronger measures sign agreement over selected features (rho = 0.84
over sixteen directions, post-selection). No marginal measure ordered the matrix, so the family that
works is the one a practitioner does not have.

**Most of the apparent mechanism is an artefact of the evaluation frame.** Five predictors reverse
direction between regions on the frames as drawn, but those frames enclose very different far
fields, from 2 % to 63 % of cells beyond 10 km of any fire, on higher ground. Restricting every
region to a 10 km collar, which drops no burned cells, makes all five agree in sign on elevation,
LST and TVDI, and lifts transfer from 0.540 to 0.617 with directions below chance falling from six
to one. One reversal survives, the LST anomaly, the only channel carrying no lapse-rate signal.

Label-free alignment pushed fourteen of twenty directions towards chance rather than repairing them.
Transfer skill has to be measured, not inferred from similarity.
