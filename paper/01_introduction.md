# 1. Introduction

Wildfire is a major disturbance in Mediterranean landscapes, and climate change is changing where
and how it burns [@Pausas2021]. Most fire susceptibility maps follow a common workflow
[@Jain2020; @Vibhandik2026; @Jodhani2026]. Predictors are collected over a study region and matched
with a record of burned areas, and a classifier, most often a random forest [@Breiman2001;
@Oliveira2012], is then trained. Finally, the map is reported with a cross-validated score from the
same region. **How well the model works in another region is not reported.** This study measures it.

## 1.1 Transfer is rarely measured

The skill of a susceptibility model is almost always a *within-region* estimate. The test folds come
from the same area and season, and often from the same fire. In addition, random folds let spatial
autocorrelation raise the score [@Roberts2017; @Ploton2020]. Spatially blocked cross-validation
reduces this problem [@Valavi2019; @Meyer2018], but it still does not show how the model works on a
fire it has not seen.

A regional product built from local models is expected to work outside its training area, yet this
is rarely tested. Fire-danger indices, which are driven by weather, did not transfer well between
fire environments in Peru [@Podschwit2022]. Regional fire-occurrence models in the Alps and the
Mediterranean Basin transferred well only under similar conditions [@Bekar2020], and two recent
studies also found that transfer mainly succeeds between similar regions [@Dimarco2026; @Liu2025].
Satellite measurements of the land surface before a fire are a third kind of predictor. They change
from season to season like weather, but they describe each location like a map. Whether models built
on them transfer between regions has not been tested.

## 1.2 Pre-fire thermal state as a test case

Pre-fire thermal state is a natural test case. Static predictors change little between years, so
they cannot explain why one summer burned and another did not. Surface state does change, and
satellite thermal data give partial access to it, because land surface temperature rises as
vegetation dries (Section 2.1). If the link between moisture stress and burning is general, thermal
predictors should keep at least part of their value in a new region. Normalised channels, such as
the Temperature-Vegetation Dryness Index, were expected to transfer best, because they should be less
affected by temperature differences between regions. A failure of these predictors to transfer is
therefore informative.

## 1.3 Contributions

**Contribution 1. The evaluation area changes what a model appears to know.** It is known from
species distribution modelling (Section 2.3) that the evaluation area affects the area under the
receiver operating characteristic curve (ROC-AUC). Here the size of
this effect was measured for burned-area models with a controlled design. The model, the predictors
and the fitting were kept fixed, and only the scored cells were changed. With the region as the unit,
the score fell by **0.160 ROC-AUC** across five regions. The loss came from the unburned cells next to
the fire, not from class balance (Section 4.3). The same test showed that four between-region
results of this study depend on the study areas: mean transfer, the supported elevation reversals,
the reversal between the two Muğla fires, and the correlation of one similarity measure with
transfer (Section 4.4).

**Contribution 2. Local skill transfers at most weakly.** The thermal predictors improved
within-region skill in all five regions. On the scar frame, however, the gain was small and not
established (Section 4.3). Across twenty transfer directions the gain was +0.007 on the original
study areas and +0.024 on comparable study areas. Both intervals included zero (Section 4.4). The
static baseline did not transfer better. On matched areas, transfer stayed **0.197** below the
within-region reference.

**Contribution 3. No similarity measure was shown to predict transfer.** Twenty similarity
measures were tested, ranging from predictor distance to niche overlap and the agreement of
predictor-burning relationships. On the original study areas, none predicted transfer (Section
4.6). With ten independent region pairs, this is a failure to find an ordering, not proof that none
exists.

The two label-free adaptation methods tested [@Sun2016] did not improve transfer either. The analysis
code, configuration and frozen outputs are public, so all results can be checked and re-run
(Declarations). This matters because conclusions about wildfire models depend on how they are
evaluated [@Xu2026].
