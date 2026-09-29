# 1. Introduction

Wildfire is a major disturbance in Mediterranean landscapes, and climate change is changing where
and how it burns [@Pausas2021]. Fire susceptibility maps are usually made in the same way
[@Vibhandik2026; @Jodhani2026]. Predictors are collected over a study region and matched with a
record of burned areas. A classifier, most often a random forest [@Breiman2001], is then trained.
The map is reported with a cross-validated score from the same region. **How well the model works
in another region is not reported.** This study measures it.

## 1.1 Transfer is rarely measured

The skill of a susceptibility model is almost always a *within-region* estimate. The test folds come
from the same area and season, and often from the same fire. Random folds also let spatial
autocorrelation raise the score [@Roberts2017; @Ploton2020]. Spatially blocked cross-validation
reduces this problem [@Valavi2019; @Meyer2018], but it does not show how the model works on a fire
it has not seen.

A regional product built from local models is expected to work outside its training area. This is
rarely tested. Fire-danger indices did not transfer well between fire environments in Peru
[@Podschwit2022]. Regional fire-occurrence models in the Alps and the Mediterranean Basin
transferred well only under similar conditions [@Bekar2020]. Two recent studies also found that
transfer mainly succeeds between similar regions [@Dimarco2026; @Liu2025]. All of these studies use
mainly static predictors, which describe a place. It is not known whether dynamic, season-specific
predictors behave in the same way.

## 1.2 Pre-fire thermal dryness as a test case

Pre-fire thermal dryness is the dynamic predictor class that is most expected to transfer. Static
predictors change little between years, so they cannot explain why one summer burned and another
did not. Surface state changes, and satellite thermal data give partial access to it (Section 2.1).
The link between moisture stress and burning is physical and general. Therefore, if thermal
predictors do not transfer, the failure cannot easily be blamed on a local variable. The normalised
channels were expected to transfer best, because they should be less affected by temperature
differences between regions. They did not transfer better than the absolute channels (Section
S1.6).

## 1.3 Contributions

**Contribution 1. The evaluation area changes what a model appears to know.** It is known from
species distribution modelling that the evaluation area affects AUC (Section 2.3). Here the size of
this effect was measured with a controlled design. The model, the predictors and the fitting were
kept fixed, and only the scored cells were changed. The score fell by **0.133 ROC-AUC** over seven
scars, and by 0.160 with the region as the unit. The loss came from the unburned cells near the
fire, not from class balance (Section 4.3). The same test shows that four of our own between-region
quantities depend on the study areas (Section 4.4).

**Contribution 2. Local skill transfers at most weakly.** The thermal predictors improved
within-region skill in all five regions. At the burn scar itself, the gain was small and not
established (Section 4.3). Across twenty transfer directions, the gain was +0.007 on the original
study areas and +0.024 on comparable study areas. Both intervals included zero, and gains above
about 0.05 were excluded (Section 4.4). The static baseline did not transfer better. On matched
areas, transfer stayed **0.197** below the within-region reference.

**Contribution 3. No similarity measure was shown to predict transfer.** Twenty similarity
measures were tested, from predictor distance to niche overlap and the agreement of
predictor-burning relationships. On the original study areas, no measure predicted transfer
(Section 4.6). With ten independent region pairs, this shows a failure to find an ordering, not
proof that none exists.

Label-free domain adaptation [@Sun2016] also did not improve transfer. The analysis code,
configuration and frozen outputs are public, so the results can be checked and re-run
(Declarations). This matters because conclusions about wildfire models depend on how they are
evaluated [@Xu2026].
