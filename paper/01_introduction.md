# 1. Background

Wildfire is a major disturbance in Mediterranean landscapes, and climate change is altering fire regimes [@Pausas2021]. Mediterranean fire policy needs to shift from suppression towards prevention and landscape management [@Moreira2020], with susceptibility maps supporting this planning. Most maps follow a common workflow [@Jain2020; @Vibhandik2026; @Jodhani2026], using predictors and burned-area records to train a classifier, most commonly a random forest [@Breiman2001; @Oliveira2012; @Tonini2020], whose performance is evaluated within the same region. However, agencies with limited local fire records may need to use a model trained elsewhere, but how well such models perform in another region is rarely reported.

## 1.1 Transfer is rarely measured

Susceptibility models are usually evaluated within the regions where they are trained, often using test folds from the same area, season or fire. Random folds can inflate performance through spatial autocorrelation [@Roberts2017; @Ploton2020], while spatial blocking reduces this optimism [@Valavi2019; @Meyer2018], although its suitability for map accuracy assessment remains debated [@Wadoux2021; @deBruin2022; @Mila2022]. The area of applicability identifies locations where predictor values are sufficiently dissimilar from the training data, based on their distance in predictor space [@Meyer2021; @Meyer2022; @Ludwig2023]. However, neither approach establishes performance on an unseen fire. Transferability requires testing on spatially or temporally independent data [@Wenger2012] and remains an open challenge in ecological modelling [@Yates2018].

Few studies directly assess the transferability of fire models. Weather-driven fire-danger indices transferred poorly between fire environments in Peru [@Podschwit2022]. European operational fire-danger systems, including the European Forest Fire Information System, also rely on weather-based indices such as the Canadian Fire Weather Index [@Vitolo2020], while major Mediterranean fires are driven by heat, wind and drought [@Ruffault2020; @Ghasemiazma2026]. Regional fire-occurrence models transferred well across the Alps and Mediterranean Basin only under similar conditions, with a pooled model proving more robust [@Bekar2020]. WildfireGenome [@Liu2025] likewise found better transfer between similar US counties than dissimilar ones, but used composite hazard indicators rather than observed burned areas as the response. The closest Mediterranean study [@Dimarco2026] evaluated a full transfer matrix across four countries using 500 m predictors; all transfers achieved an AUC of at least 0.80, with higher scores between similar countries. However, its predictors described static place characteristics, and its response was human-caused ignition. A random forest susceptibility model covering thirteen eastern Mediterranean and southern Black Sea countries was trained on a decade of fire records [@Trucchia2023], but fitting all regions jointly does not test transfer to a region without a fire record. More broadly, conclusions about wildfire models depend on how performance is evaluated [@Xu2026].

When a model is transferred to a new region, its predictor distribution may change (covariate shift). This can potentially be addressed without target labels using methods such as covariance alignment (CORAL) [@Sun2016]. Domain adaptation more broadly is well established in remote sensing [@Tuia2016; @Persello2012], including approaches that decompose different sources of shift [@Huang2026]. However, the predictor-response relationship may also change (concept shift) [@MorenoTorres2012], and detecting a reversal in association requires target labels. We found no previous application of covariance alignment to fire susceptibility or burned-area prediction.

## 1.2 Pre-fire thermal state as a test case

Satellite measurements of the land surface before a fire are a third kind of predictor. They change
from season to season like weather, but they describe each location like a map. Static predictors
change little between years, so they cannot explain why one summer burned and another did not.
Satellite thermal data can be used to estimate fuel moisture [@Yebra2013], because land surface
temperature (LST) rises as vegetation dries. LST combined with a vegetation index was used by
Chuvieco et al. [@Chuvieco2004] to estimate live fuel moisture for fire-danger rating, and the
Temperature-Vegetation Dryness Index (TVDI) [@Sandholt2002] is an internally normalised form of this
approach, so it is often expected to transfer better than raw temperature. Pre-fire LST anomalies are
related to the burned area and duration of later fires [@Maffei2018; @Maffei2021], pre-fire optical
moisture indices carry similar information [@MaffeiMenenti2019], and dead fuel moisture was the
strongest predictor of human-caused ignition across Europe in a pooled model [@Gelabert2025].
Pre-fire evaporative stress from spaceborne thermal data has been used to predict unseen fires
within one region [@PascoliniCampbell2025], and within-region susceptibility models exist for
Turkish Mediterranean landscapes [@AlkanAkinci2023; @Iban2022]. Satellite fuel-moisture models are,
however, usually site-specific, and their transfer is rarely tested [@Marino2024]. To our knowledge,
the transfer of a classifier that uses pre-fire thermal state to another region, without target
labels, has not been tested. Large datacubes now support deep-learning fire-danger models
[@Kondylatos2023]; we used a simple fixed classifier, so that only the evaluation changes. Surface
predictors of this kind are meant to complement weather-driven danger ratings, not to replace them.

## 1.3 Evaluation area and similarity

In species distribution modelling, the evaluation area is known to affect the area under the
receiver operating characteristic curve (ROC-AUC). Lobo et al. [@Lobo2008] list it among the main
reasons for caution when AUC values are compared, because a larger area adds more easy absences and
raises the score. Related effects were shown for spatial sorting bias between training and test
sites [@Hijmans2012], in a general analysis of AUC [@JimenezValverde2012] and for calibration
[@VanDerWal2009], and the effect was described in general terms as the accessible area [@Barve2011].
Its size depends on the problem. We found no wildfire study that keeps the model fixed and changes
only the evaluation cells, although region-wide scores are often read as if they described
performance next to the fire.

If transfer cannot be assumed, it might still be predicted from the similarity of two regions.
Species distribution studies disagree on this. Vesk et al. [@Vesk2021] found that trait-based models
did not predict worse with increasing geographic or environmental distance, whereas Rousseau and
Betts [@Rousseau2022] found that transferability decreased with geographic distance and with
extrapolation. Niche overlap can be measured with Schoener's *D* and Warren's *I*
[@Schoener1968; @Warren2008].

## 1.4 Objectives

We measured how far the skill of pre-fire thermal predictors transfers between five Mediterranean
regions, each with one large fire season, and asked three questions.

1. How much does the evaluation area change the score of one fixed model? We kept the model, the
   predictors and the fitting fixed and changed only the scored cells.
2. Does within-region thermal skill transfer to another region without target labels? If the link
   between moisture stress and burning is general, thermal predictors should keep at least part of
   their value in a new region, and normalised channels such as the TVDI should transfer best,
   because they should be less affected by temperature differences between regions.
3. Can the similarity of two regions predict transfer, so that a source region could be chosen
   before a fire?

We also tested two label-free adaptation methods [@Sun2016], pooled training and the removal of
predictors whose association reversed between regions. The analysis code, configuration and frozen
outputs are public, so all results can be checked and re-run (Data availability).
