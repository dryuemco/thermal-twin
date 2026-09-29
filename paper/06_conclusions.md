# 6. Conclusions

This study tested whether the skill of pre-fire thermal predictors transfers between five large
Mediterranean fires. Three conclusions are supported.

First, the evaluation area changes the score. When one fixed model was scored on the burn scar and
its 2 km collar instead of the whole region, 0.133 ROC-AUC was lost over seven scars and 0.160 with
the region as the unit. The loss came from the unburned cells near the fire, not from class balance.
A region-wide score should be reported as an upper bound.

Second, local skill transferred at most weakly. The thermal predictors improved within-region skill
in all five regions, but at the burn scar the gain was not established. Across twenty transfer
directions, the gain was +0.007 on the original study areas and +0.024 on comparable areas. Both
intervals included zero, and gains above about 0.05 were excluded. On matched areas, transfer stayed
0.197 below the within-region reference. The static baseline did not transfer better, and
label-blind domain adaptation did not help.

Third, no similarity measure was shown to predict transfer. The most similar pair failed in both
directions, and the least similar pair transferred above chance.

Transfer skill should therefore be measured in the target region, and the study area should be
fixed by a stated rule before the predictors are computed. Several fire seasons per region are
needed to separate region effects from event effects.
