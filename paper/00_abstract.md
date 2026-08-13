# Abstract


Pre-fire thermal dryness separates a fire year from a normal year. It is measured by land surface
temperature, its anomalies and dryness indices. Models built on it are rarely tested outside their
training region.

Five Mediterranean wildfire regions were analysed on about 500 m cells, with MCD64A1 labels and
spatially blocked validation. Six pre-fire thermal predictors were added to a static and near-static
terrain, fuel and greenness baseline. Within every region, ROC-AUC rose by +0.06 to +0.15. The gain
survived coarser blocks and an earlier predictor window.

The predictors were then transferred between regions. Their mean contribution over twenty ordered
directions was +0.004, with an interval spanning zero. Paired deltas ran from −0.148 to +0.132,
twelve positive and eight negative. Removing the two reversing predictors bought +0.014 of transfer
for −0.081 of within-region skill. Local skill and portability are therefore traded.

The failure is conditional. Inside one study area, two fires eleven months apart reversed the
elevation-burning link, with disjoint bootstrap intervals. Season and year are confounded there, so
place is what the design holds fixed.

Twenty candidate diagnostics were rank-correlated against observed transfer. Only two had bootstrap
intervals excluding zero. Both were conditional, the stronger being agreement in the sign of each
predictor's association (Spearman ρ = 0.84 over eight pairs). No marginal, niche-overlap or regime
measure ordered the matrix. At the point estimate, the highest-overlap pair failed in both
directions and the lowest-overlap pair transferred in both. Label-blind adaptation by standardisation
and CORAL only pushed transfer towards chance. Niche and regime measures need labels in both regions
too, so only the marginal family can be run before deployment, and it fails. Thirty-two labelled
target blocks recovered 85 to 89 % of the ceiling in four of six directions tested.

Transfer skill therefore has to be measured, not inferred from similarity. What carries the
information is conditional, so the price of this failure is target labels rather than better
unsupervised alignment.
