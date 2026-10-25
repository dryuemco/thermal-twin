# 5. Conclusions

Three conclusions are supported for these five Mediterranean regions, each with one large fire
season.

First, the evaluation area changes the score. Scoring one fixed model on the burn scar and its 2 km
collar instead of the whole region lowered ROC-AUC by 0.160 with the region as the unit, and the loss
came from the unburned cells next to the fire. A study should report which area its score refers to.

Second, local skill transferred at most weakly. The thermal gain held within all five regions but was
not established on the scar frame. Across twenty transfer directions it was +0.007 on the original
study areas and +0.024 on comparable areas, both intervals including zero, and on matched areas
transfer stayed 0.197 below the within-region reference. Neither the static baseline nor the two
label-free adaptation methods did better.

Third, none of twenty similarity measures was shown to predict transfer. At the point estimates the
most similar pair of regions failed in both directions, and the least similar pair transferred above
chance.

Before a borrowed model is used for prevention planning, its skill should be measured in the target
region, and the study area should be fixed by a stated rule before the predictors are computed.
Several fire seasons per region are needed to separate region effects from event effects.
