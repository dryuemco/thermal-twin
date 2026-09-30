# 2. Related work

## 2.1 Pre-fire thermal dryness

Satellite thermal data can be used to estimate fuel moisture [@Yebra2013]. Land surface
temperature (LST) combined with a vegetation index was used by Chuvieco et al. [@Chuvieco2004] to
estimate live fuel moisture for fire-danger rating. The Temperature-Vegetation Dryness Index (TVDI)
[@Sandholt2002] is an internally normalised form of this approach, so it is often expected to
transfer better than raw temperature. Pre-fire LST anomalies are related to the burned area and
duration of later fires [@Maffei2018; @Maffei2021], and pre-fire optical moisture indices carry
similar information [@MaffeiMenenti2019]. Dead fuel moisture was the strongest predictor of
human-caused ignition across Europe in a pooled model [@Gelabert2025]. Satellite fuel-moisture
models are, however, usually site-specific, and their transfer is rarely tested [@Marino2024].
Within-region susceptibility models already exist for Turkish Mediterranean landscapes
[@AlkanAkinci2023; @Iban2022]. To our knowledge, the transfer of a classifier that uses pre-fire
thermal state to an unseen region, without target labels, has not been tested. Large datacubes now
support deep-learning fire-danger models [@Kondylatos2023]. Here a simple fixed classifier was used,
so that only the evaluation changes.

## 2.2 Spatial validation, transferability and shift

Spatially blocked cross-validation reduces the optimism of random folds [@Roberts2017;
@Valavi2019], although its use for map accuracy is debated [@Wadoux2021; @deBruin2022; @Mila2022].
The area of applicability shows where predictor values are too far from the training data
[@Meyer2021; @Meyer2022; @Ludwig2023], and transferability, which must be tested on spatially or temporally separate data [@Wenger2012],
remains an open problem in ecological modelling [@Yates2018]. Under covariate shift only the predictor distribution changes, which can in
principle be corrected without target labels, for example by per-region standardisation or by
covariance alignment (CORAL) [@Sun2016], as is common in remote sensing [@Tuia2016; @Persello2012];
under concept shift the predictor-response relationship itself changes [@MorenoTorres2012], and a
reversed association can only be seen with target labels. Shift decomposition has been used in
remote sensing [@Huang2026], but we found no use of covariance alignment for fire susceptibility or
burned-area prediction.

## 2.3 Transfer of fire models and the evaluation area

Few studies test the transfer of fire models directly. Global fire-danger indices, which are dynamic and driven by weather, did not transfer well between
fire environments in Peru [@Podschwit2022]. In the Alps and the Mediterranean Basin,
regional fire-occurrence models transferred well only under similar conditions, and a pooled model
was more robust [@Bekar2020]. WildfireGenome [@Liu2025] trained models in one of seven US counties
and tested them in the others. Transfer was good between similar counties and poor between
dissimilar ones. Its label is a composite of hazard indicators, not observed burned area. Xu et al.
[@Xu2026] showed that conclusions about wildfire models depend on the evaluation design. The closest
Mediterranean study is Dimarco et al. [@Dimarco2026]. They used 500 m predictors in four countries
and a full transfer matrix. No transfer fell below AUC 0.80, and similar countries scored higher.
Their predictors are static attributes of a place, and their response is human-caused ignition.
Here the predictors describe the surface state in one season, and the response is burned area.
Susceptibility has also been mapped with one random forest for thirteen countries of the eastern
Mediterranean and southern Black Sea from a decade of fires [@Trucchia2023]; such a model is fitted
on all regions at once, so it does not measure transfer to a region without a fire record.

**Evaluation area and AUC.** In species distribution modelling, the evaluation area is known to
affect AUC. Lobo et al. [@Lobo2008] list it among the main reasons for caution when AUC
values are compared, because a larger area adds more easy absences and raises the score. Related
effects were shown for spatial sorting bias between training and test sites [@Hijmans2012] and in a
general analysis of AUC [@JimenezValverde2012]. The same effect
was shown for calibration [@VanDerWal2009] and was described in general terms as the accessible
area [@Barve2011]. The size of the effect depends on the problem, so it was not given in general.
We found no wildfire study that keeps the model fixed and changes only the evaluation cells.
Region-wide scores are often reported as if they described performance next to the fire.

**Similarity and transfer.** Species distribution studies disagree on the role of similarity.
Vesk et al. [@Vesk2021] found that trait-based models did not predict worse with increasing
geographic or environmental distance. Rousseau and Betts [@Rousseau2022] found that transferability
decreased with geographic distance and with extrapolation. The niche overlap measures used here are
Schoener's *D* and Warren's *I* [@Schoener1968; @Warren2008].
