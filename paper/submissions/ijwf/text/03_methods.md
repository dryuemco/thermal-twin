# Materials and methods

This section describes the data, the model and the evaluations, from the study regions, labels and predictors to the evaluation frames, the similarity measures and the two interventions.

We use the following terms throughout. A *study area* is the rectangle drawn around one fire. An *evaluation frame* is the set of cells on which a score is computed. We call a result *supported* when its 95 % interval excludes the null value (0.5 for an AUC, 0 for a difference).

The within-region comparison, the transfer matrix, the two adaptation methods, the gap decomposition and the reversal test follow the fixed protocols of the processing pipeline. We recorded the twenty similarity measures on 8 August 2026, before the label correction described below. We added the frame test, the distance collars, the equivalence tests, the additional resampling units and the checks of Supplementary Section S1 after the first results. They are exploratory, and we report them as such.

## Study regions and time windows

The five Mediterranean wildfire regions we analysed are Manavgat 2021 and Muğla 2021 in Türkiye, Bejís 2022 in Spain, North Evia 2021 in Greece and Montiferru 2021 in Sardinia (Fig. 1 and Table 1). Each region contributed one fire season, and each season was dominated by one large fire, although in Muğla several separate burned areas occurred in the same weeks. The largest fires burned 58,798 ha in Manavgat, 51,245 ha in North Evia, 18,058 ha in Bejís, 17,164 ha in Muğla and about 13,200 ha in Montiferru [@Eker2024; @Almeida2023; @FernandezGuisuraga2023]. They burned pine and oak forest and shrubland, except in Montiferru, where herbaceous vegetation and low shrubs made up most of the burned area (Supplementary Section S5.2). The events were not sampled from a defined population of fires, so the results describe large single-season events. Unlike susceptibility maps trained on multi-year fire inventories [@Tonini2020; @Trucchia2022], each model here was trained on the footprint of one fire season, so the task is closer to predicting which fuel burned during one large event. Each study area is a rectangle that was not clipped to the fire perimeter, so the unburned cells around each fire form the negative class.

**Table 1. Study regions, time windows and modelled cells.** Natural-vegetation (primary) population on the ~500 m grid. Both window ends are included, and the predictor window ends the day before the label window starts. Prevalence is the burned share of the modelled cells. Gate fraction is the share of burned cells dominated by natural vegetation. Beyond 10 km is the share of modelled cells more than 10 km from any burned cell. Bounding boxes and baseline years are given in Supplementary Table S13.

| Region | Predictor window | Label window | Cells | Burned | Prevalence | Gate fraction | Beyond 10 km |
|---|---|---|---:|---:|---:|---:|---:|
| Manavgat 2021 (Türkiye) | 1 Jun to 27 Jul 2021 | 28 Jul to 31 Aug 2021 | 20,511 | 2,935 | 0.143 | 0.955 | 58.5 % |
| Bejís 2022 (Spain) | 15 Jun to 14 Aug 2022 | 15 Aug to 30 Sep 2022 | 15,190 | 1,100 | 0.072 | 0.991 | 63.1 % |
| Muğla 2021 (Türkiye) | 1 Jun to 28 Jul 2021 | 29 Jul to 15 Sep 2021 | 41,730 | 2,911 | 0.070 | 0.958 | 55.3 % |
| North Evia 2021 (Greece) | 5 Jun to 2 Aug 2021 | 3 Aug to 30 Sep 2021 | 9,298 | 2,664 | 0.287 | 0.945 | 43.7 % |
| Montiferru 2021 (Italy) | 25 May to 23 Jul 2021 | 24 Jul to 31 Aug 2021 | 2,544 | 539 | 0.212 | 0.723 | 2.1 % |

We did not fix all rectangles before any outcome was seen. Only the Montiferru rectangle follows a stated rule, and we extended the North Evia rectangle after the first one showed a very high burned fraction. We kept the first Evia rectangle as a sensitivity analysis (Supplementary Section S1.2). In each region the predictor window ends the day before the label window starts, so no predictor observation is later than the first labelled burning. Fig. 2 shows the processing chain and the evaluation design.

## Burned-area labels and the analysis grid

We took labels from the Moderate Resolution Imaging Spectroradiometer (MODIS) MCD64A1 burned-area product, Collection 6.1 [@MCD64A1; @Giglio2018], through Google Earth Engine [@Gorelick2017]. As a check, we repeated the within-region and transfer analyses with the Visible Infrared Imaging Radiometer Suite (VIIRS) VNP64A1 product [@VNP64A1] (Supplementary Figs S1 and S2). We aggregated the product to an analysis grid with cells of about 500 m (Supplementary Section S5.1). A cell was labelled burned when any of its pixels had a burn date in the label window, so a scar can grow by up to one cell at its edge. We removed cells that burned in the predictor window in three regions, but in Bejís this removal was not applied and 48 such cells were kept (Supplementary Table S12).

The label first used for Manavgat missed the first four days of the fire, 28 to 31 July. The corrected label only adds burned cells and raises their number in the primary population from 784 to 2,935. In this paper, "original label" means the label before this correction (Supplementary Section S5.1).

Before modelling, each region had to pass a gate on the fraction of burned cells covered mainly by natural vegetation in the European Space Agency (ESA) WorldCover map [@Zanaga2022]. The five regions passed, and a cropland control, Kozan 2023, failed and was excluded (Supplementary Section S5.1).

## Predictors

We used ten predictors (Supplementary Table S14). The *baseline* set contains elevation and slope from the Copernicus DEM GLO-30 [@CopernicusDEM], dominant land cover from WorldCover v200 and the median normalised difference vegetation index (NDVI) of the predictor window from Landsat 8 Collection 2 Level-2 [@LandsatC2L2].  The *thermal* set adds six channels derived from Landsat 8 surface temperature and composited as the median of the predictor window. The six channels are current LST, its anomaly against the same calendar window in four earlier years, the TVDI [@Sandholt2002], its difference from those baseline years, a downscaled LST and a fused LST. The last two fill gaps in Landsat with MODIS daytime LST [@MOD11A1]. The median pixel had three to six clear morning Landsat observations in the predictor window (Supplementary Table S15). Because TVDI edges are fitted inside each study area and window, a TVDI value does not mean the same moisture state in two regions. The six thermal channels carry about two signals, because several of them are strongly correlated (Supplementary Section S5.3).

To test whether normalised channels transfer better, we also fitted the baseline with only the two anomaly channels, which are normalised against each region's own baseline years, and with only the four channels of absolute surface state. The current TVDI is normalised within each scene but not against the baseline years, so it belongs to the second set.

The *primary* population contains the valid cells in which tree, shrub and grass cover together reach 0.50, so cropland and water are excluded. Every result in the main text refers to it (Supplementary Section S5.8).

## Classifier and validation

The classifier is a random forest [@Breiman2001] with 300 trees, unlimited depth, at least three cells per leaf and balanced class weights. We fixed these settings in advance, did not tune them, and used the same settings in every analysis. Missing values were filled inside each training fold, and on the source region only in transfer, so no test data were used in fitting.

Cross-validation used five folds drawn over whole square blocks of cells, stratified by label, so a block is never split between training and test. We report block sizes of 2, 10 and 20 cells and write them as 1 km, 5 km and 10 km blocking. Every score is an AUC on a named evaluation frame. The AUC is the probability that a burned cell in the frame is ranked above an unburned one, so the metric can change when the frame changes, even when no prediction changes.

We estimated uncertainty with a spatial-block bootstrap of 1000 replicates and took the 2.5 and 97.5 percentiles as the interval. We resampled quantities with one value per transfer direction over the ten region pairs, and this pair-cluster bootstrap is the *primary resampling unit* for direction-level intervals. Quantities with one value per scar or per target region get a Student *t* interval. Because scars are nested in regions, the region-level estimates are the primary ones for the frame test (Supplementary Section S5.4).

## Cross-region transfer and label-free adaptation

For each ordered pair of regions, we fitted the model on the source region and applied it to the target region. We used no target label (no refitting, threshold selection or calibration on the target). We transferred both feature sets, so the gain from the thermal block is a paired difference within each direction, and we computed all twenty ordered directions.

We tested two label-free methods on every direction and in both feature sets. *Region-wise z-score* standardises the numeric features of each region with its own statistics. *CORAL after region-wise z-score* then aligns the source covariance with the target covariance [@Sun2016]. Both methods use target feature statistics, which are available before a fire, but never target labels (Supplementary Section S5.6).

## Evaluation frames

We scored models on three kinds of frame (Fig. 1b). The *region-wide frame* is the primary population of the study area as drawn. A scar is an 8-connected group of at least 50 burned cells, and its *scar frame* is the burned area together with a 2 km collar of unburned cells around it. A *distance collar* keeps all cells within 5 or 10 km of any burned cell, so only distant unburned cells are removed. In transfer, we fitted the model on the source collar and scored it on the target collar (Supplementary Section S5.9).

Within one region, we scored one region model on the whole region (A) and on the scar frame (B), so B is the same model scored on a different set of cells. We also scored on the scar frame a model fitted without that frame (C, *leave-one-scar-out*) and the models of the four other regions (D). The controls on this comparison, namely a prevalence-matched sample, swaps of the burned and of the unburned cells, a placebo collar and the exclusion of edge cells, are defined in Supplementary Sections S2.1 and S5.9. To see how skill falls with distance, a model fitted on one half of a region was scored on the cells of the other half by their distance from the training cells.

The two frames answer different questions. The region-wide frame asks where in a landscape a fire burned, which is the question behind prevention planning, and the scar frame asks which cells next to the fire burned. The second question is harder, because spread, wind and suppression matter more there and label errors are concentrated at scar edges. Every scar frame and distance collar is defined from burned cells, so these frames show how the evaluation area changes the metric but cannot be drawn before a fire.

## Signed associations, similarity measures and interventions

We measured the direction of each predictor with a *signed univariate association*, which is the AUC of each numeric predictor against the burned label, computed in each region and never folded to max(AUC, 1 − AUC). A value below 0.5 means that the predictor is lower on burned cells. We call a reversal between two regions supported only when the two values are on opposite sides of 0.5 and each region's own interval excludes 0.5. This is a per-comparison criterion, and we also report a Holm correction over each family of feature-by-pair comparisons.

To ask whether the similarity of two regions predicts transfer, we used twenty similarity measures in five families (Supplementary Table S11, where six measures are defined on twelve directions). They compare the predictor distributions of two regions, their geographic distance, the niche overlap of their burned cells (Schoener's *D* and Warren's *I* [@Schoener1968; @Warren2008]), their burned-patch regimes and the agreement of their signed associations. We rank-correlated each measure with the raw thermal transfer AUC (Spearman's ρ), with a pair-cluster bootstrap and a permutation test over the 120 orderings of the five regions. Only the predictor-distribution measures and geographic distance can be computed before a fire.

In pooled training, a model trained on four regions together was tested on the held-out region and compared with the mean of the four single-source models, because choosing the best single source would require target labels. In feature removal, we removed the two predictors whose reversal was supported under the original label, elevation and the LST anomaly, and refitted all models. Both results are post-selection estimates, because the two features were chosen from the same data.
