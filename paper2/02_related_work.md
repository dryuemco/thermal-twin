# 2. Related work

Sensitivity of environmental model results to preprocessing is not a new concern, but it is usually
raised one decision at a time and inside a study whose purpose is something else. The closest
established practice is in spatial validation, where random cross-validation over autocorrelated
cells is known to inflate skill estimates [@Roberts2017; @Ploton2020] and blocked designs are the
standard remedy [@Valavi2019; @Meyer2018], itself contested as introducing a pessimistic bias
[@Wadoux2021; @Mila2022; @deBruin2022]. That literature is a budget for one axis, and it is the model
this paper follows for eight.

For the observations themselves, the relevant reference points are product validation rather than
pipeline sensitivity: the burned-area product's omission and commission characteristics
[@Boschetti2019; @Giglio2018] bound anything built on it, and land surface temperature products carry
their own documented calibration and quality behaviour [@Cook2014; @Malakar2018]. What is rarely
reported is what a given handling of those products costs in the units of the study's own result,
which is the gap this paper addresses.

The transferability question that motivates the cohort is treated in the companion paper and in the
studies it engages [@Dimarco2026; @Liu2025; @Meyer2021; @Ludwig2023]. Xu et al. [@Xu2026] argue that
wildfire modelling conclusions depend strongly on evaluation design and task formulation; the present
paper is the same argument carried one layer further down, into how the observations were made.
