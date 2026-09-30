# 6. Conclusions

This study tested whether the skill of pre-fire thermal predictors transfers between five
Mediterranean regions, each with one large fire season. Three conclusions are supported.

First, the evaluation area changes the score. When one fixed model was scored on the burn scar and
its 2 km collar instead of the whole region, ROC-AUC fell by 0.160 with the region as the unit. The
loss came from the unburned cells next to the fire, not from class balance. The two areas answer
different questions, so a paper should report which area its score refers to.

Second, local skill transferred at most weakly. The thermal predictors improved within-region skill
in all five regions, but on the scar frame the gain was not established. Across twenty transfer
directions, the gain was +0.007 on the original study areas and +0.024 on comparable areas, and both
intervals included zero. On matched areas, transfer stayed 0.197 below the within-region reference.
The static baseline did not transfer better, and the two label-free adaptation methods tested did not
help.

Third, none of twenty similarity measures was shown to predict transfer. At the point estimates, the
most similar pair of regions failed in both directions, while the least similar pair transferred
above chance.

Transfer skill should therefore be measured in the target region before a borrowed model is used for
prevention planning, and the study area should be fixed
by a stated rule before the predictors are computed. Several fire seasons per region are needed to
separate region effects from event effects.
