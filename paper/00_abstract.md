# Abstract


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
