# Abstract

**Background** Wildfire susceptibility maps are usually scored in the region where they were trained,
yet agencies without a long fire record may borrow a map from elsewhere. We tested whether pre-fire
satellite thermal predictors, expected to track fuel dryness, transfer between Mediterranean regions.
Six land surface temperature (LST) and dryness predictors extended a terrain, land-cover and greenness
baseline. We fitted random forests in five regions, each with one large fire season (2021 or 2022):
Manavgat and Muğla (Türkiye), Bejís (Spain), North Evia (Greece) and Montiferru (Italy). Skill was the
spatially blocked area under the receiver operating characteristic curve (ROC-AUC) against Moderate
Resolution Imaging Spectroradiometer (MODIS) burned areas, within each region and across all twenty
ordered pairs of regions without target labels.

**Results** Scored on the burn scar and a 2 km collar, not region-wide, the same models lost 0.160
[0.090, 0.230] ROC-AUC on average. At 5 km blocking, thermal predictors added +0.045 to +0.148 within
regions, but only +0.007 [−0.020, +0.038] across twenty directions and +0.024 [−0.004, +0.049] on
comparable areas. Two label-free adaptation methods moved transfer toward chance. None of twenty
similarity measures was shown to predict transfer. At point estimates, the most similar pair of
regions failed in both directions, and hotter surfaces burned less in four of five regions (two with
interval support), consistent with LST describing land surface rather than dryness.

**Conclusions** A score from the training region does not show how a susceptibility map will perform
in another region. Before a borrowed single-season model is used for prevention planning, fire
agencies should test it against burned areas in the target region and report on which cells its score
was computed. Region and event effects are confounded here, so several fire seasons per region are
needed to generalise.
