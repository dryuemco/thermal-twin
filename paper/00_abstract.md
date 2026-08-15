# Abstract



Pre-fire thermal dryness separates a fire year from a normal year, but models built on it are rarely
tested outside the region where they were fitted. Five Mediterranean wildfire regions were analysed
on about 500 m cells, with MCD64A1 labels and spatially blocked validation, adding six pre-fire
thermal predictors to a terrain, fuel and greenness baseline.

**Local skill does not travel, and most of it is lost before the region changes.** Within-region
ROC-AUC rose by +0.056 to +0.153 under blocked cross-validation, but by +0.022 [−0.032, +0.077] when
a whole burn scar is withheld, and by +0.004 [−0.028, +0.036] across twenty transfer directions,
with a sign that changes from pair to pair. The static baseline transferred no better, 0.537 against
0.541. On **identical cells**, a model holding the held-out scar scores 0.634, one without it 0.552, and
one fitted 306 to 2,802 km away 0.555, so withholding the fire and crossing the region are both
undetectable, at +0.082 [−0.011, +0.175] and −0.003 [−0.075, +0.069]. Most of the apparent collapse
from a region-wide 0.776 is the evaluation area itself, whose negatives are all fire-adjacent and
therefore the hardest in the region.

**The failure is invisible to the diagnostics that can be run before deployment.** Of twenty
candidates rank-correlated against observed transfer, only two had intervals excluding zero, and both
need target labels; the stronger measures agreement in the sign of each predictor's association
(Spearman rho = 0.84). No marginal measure ordered the matrix, so the family that works is the one a
practitioner does not have.

**The mechanism of the residual is a reversal of sign.** Elevation and the LST anomaly reverse the
direction of their association with burning between regions, with bootstrap support, and the same
reversal appears between two fires eleven months apart on one grid. Removing them cost −0.081 of
within-region skill and changed transfer by +0.014 [−0.017, +0.045].

Label-free alignment pushed fourteen of twenty directions towards chance rather than repairing them.
Transfer skill has to be measured, not inferred from similarity.
