# Scale-up analysis plan (frozen 14 November 2026)

This plan is fixed before any analysis of the official scale-up outputs was run. It was written
after the pilot of 12 November 2026 (scratch clone, same code, same fires and windows), whose
results the authors have seen, and after the literature review of 14 November 2026
(`reports/Yangın modeli değerlendirme boşlukları.md` in the project folder). The paper must say
both things: hypotheses fixed after the pilot, before the official analysis. Nothing in this file is
changed once the first official result exists; a needed change is added as a dated amendment at the
end, saying what was already seen.

## 1. Data

Fires (primary set, 31):
- the 26 scale-up fires px01_2023 ... px26_2021 including rhodes_2023 (branch `scaleup-31fires`,
  outputs `D:/ThermalTwin/scaleup/w*/outputs/experiments/<id>`);
- the five paper regions manavgat_2021, bejis_2022, mugla_2021, evia_2021_extended from the
  SHA-256 verified paper tables (`paper/code/_canonical.py`, corrected labels), and
  montiferru_2021_fullwindow in place of montiferru_2021, so that the MODIS predictor uses the whole
  predictor window in every fire (decision of 14 November). The other four paper windows lie inside
  June to September, where the month filter changes nothing.

Not in the primary set: the repeat fires rp01_2020, rp02_2023, rp03_2023 (same region as another
fire, overlapping rectangles), used only for the descriptive same-region comparison;
montiferru_2021 (paper version), used for the reproduction gates and as a sensitivity row.

Population: cells with `valid_for_modeling` and `burnable_tree_shrub_grass` (as in the paper).
Label: `burned` (MCD64A1). Missing predictor values are imputed with the training median, as in the
paper. No fire is dropped for missing predictors in the primary analysis.

Exclusion sensitivity (fixed now): repeat every headline number without the fires in which more than
20 % of population cells miss at least one thermal predictor. From the QC table of 14 November these
are px20_2021 (0.61), px12_2022 (0.40), px26_2021 (0.31) and px03_2022 (0.2006).

## 2. Models and validation

- Feature sets: BASELINE and THERMAL of `paper/code/_canonical.py`; leakage assertion before every fit.
- Primary classifier: the paper's random forest (300 trees, min_samples_leaf 3, class_weight balanced,
  seed 42, median and most-frequent imputation, one-hot land cover).
- Second classifier: sklearn HistGradientBoostingClassifier (max_iter 300, learning_rate 0.1,
  class_weight balanced, land cover as a categorical feature, native missing values, seed 42).
- Cross-validation: StratifiedGroupKFold, 5 folds, shuffle, seed 42, groups = square blocks of
  10 cells (about 5 km, primary), 20 cells (about 10 km) and 40 cells (about 20 km).
- Geographic null model (after Hijmans 2012): no predictor; a test cell is scored by minus its
  distance to the nearest burned cell of the training folds. Same folds as the classifiers.
- Metrics: ROC-AUC (primary) and average precision (PR-AUC) with the prevalence of the evaluated
  set reported beside it.
- Uncertainty: fires are the unit. Means over fires carry a percentile interval from 2000 bootstrap
  resamples of fires (seed 42). Counts of fires are reported as "k of n".

## 3. Claims, analyses and decision rules

Claim 1. Geographic null model against the classifiers.
- Per fire: ROC-AUC and PR-AUC of null, THERMAL RF, BASELINE RF and THERMAL HGB, at 5, 10 and 20 km
  blocks.
- Calibrated AUC after Hijmans (2012): pairwise distance sampling inside each test fold. For every
  test burned cell, the unused test unburned cell whose distance to the nearest training burned cell
  is closest is taken, and the pair is kept only if the two distances differ by at most 33 % of the
  burned cell's distance (floor one cell, 0.51 km). AUC on the kept pairs for the null and the
  classifiers; cAUC = AUC + 0.5 - max(0.5, AUC_null).
- Buffered validation (after Ploton et al. 2020): 5 km block folds, training cells within b km of
  any test cell removed, b = 0, 1, 2, 5, 10 km; null and THERMAL RF re-fitted per fold. A fold whose
  remaining training set has fewer than 30 burned cells is skipped and counted.
- Decision rule: if the null model beats the THERMAL RF in fewer than 28 of 31 fires at 5 km blocks,
  claim 1 is reduced to a descriptive finding and the paper falls back to the IJWF framing.

Claim 2. Fixed model re-scored on disjoint distance bands.
- Out-of-fold predictions of the 5 km block models are kept fixed. Unburned cells are split by their
  distance to the nearest burned cell of the same fire: 0-0.5, 0.5-1, 1-2, 2-5, 5-10, >10 km. Each
  band is scored with all burned cells as positives; a band needs at least 20 unburned cells.
- Per fire: band ROC-AUC and PR-AUC for THERMAL RF, BASELINE RF, THERMAL HGB and null; rise =
  AUC(farthest band) - AUC(0-0.5 km); count of fires with a positive rise and with a positive
  Spearman trend over bands.
- Environmental-distance version: the same, with unburned cells split into quintiles of their
  Mahalanobis distance (THERMAL numeric predictors, standardised within the fire) to the burned-cell
  centroid.
- Landscape heterogeneity beyond 10 km is reported per fire (standard deviation of elevation and
  NDVI by band).

Claim 3. Label error at the fire edge (Sentinel-2 check).
- Reference: Sentinel-2 L2A (COPERNICUS/S2_SR_HARMONIZED) in Earth Engine; pixels with SCL classes
  3, 8, 9, 10, 11 masked; pre-fire composite = median over the predictor window, post-fire composite
  = median over the 30 days after label_end (60 days if fewer than 3 valid observations);
  NBR = (B8 - B12) / (B8 + B12); dNBR = NBR_pre - NBR_post. A 20 m pixel is burned if dNBR >= 0.10
  (lower bound of low severity, Key and Benson 2006); sensitivity threshold 0.27. Burned fraction per
  500 m cell on the step8a grid.
- Report per distance band: share of MCD64A1-unburned cells with Sentinel-2 burned fraction above
  0.05, 0.25 and 0.5, and share of MCD64A1-burned cells with fraction below 0.1.
- Re-scoring the fixed predictions of claim 2 with three label variants: (a) Sentinel-2 label
  (fraction >= 0.5); (b) MCD64A1 label with ambiguous unburned cells (fraction > 0.05) dropped;
  (c) MCD64A1 label with unburned cells of fraction >= 0.5 relabelled burned. FireCCI51 agreement
  per band where the product covers the fire year.
- Decision rule: if, after re-labelling, the 0-0.5 km band AUC moves more than half of the way from
  its MCD64A1 value to the >10 km value (mean over fires), claim 2 is rewritten as a label-error
  finding.

Claim 4. Transfer and pooling.
- Raw and within-fire z-scored transfer over all 930 directions, THERMAL and BASELINE; per-region
  min-max scaling as in Dimarco et al. (2026); transfer scored on the whole target and on the
  distance bands of claim 2.
- Leave-one-fire-out pooling (4000 cells per source, seed 42) and the learning curve over 2, 5, 10,
  15, 20, 30 source fires, three random draws per size.
- Similarity measures as in the pilot (distance, same year, domain-classifier AUC, mean shift), with
  Spearman's rho and the fire-resampling interval.
- A mixed model separating source, target and pair effects is fitted when statsmodels is available;
  until then the source and target means are reported.
- No sentence "transfer does not work in the Mediterranean" unless the Dimarco reconciliation is
  done.

Claim 5. Sign of the pre-fire LST relation.
- Per fire: univariate AUC of current_lst_mean with block-bootstrap interval; residual AUC after
  elevation, then elevation + NDVI + tree cover, then + aspect (northness and eastness from the
  experiment DEM).
- Afternoon LST (MODIS Aqua MYD11A1, LST_Day, same QC rule as the pipeline, predictor window) as a
  second source.
- Reported as a secondary observation, never as a headline claim.

## 4. Reproduction gates

Before any new number is read, the five paper regions (montiferru_2021, paper version) must
reproduce: band AUC of `paper/labelfix_rerun/geometry/a1_band_auc.csv` (k = 0) within 0.0015 and
the raw transfer AUC of Supplementary Table S8 within 0.002. The script stops if a gate fails.

## 5. Order of work

1. Claims 1 and 2 (`scripts/scaleup/analysis_official.py`).
2. Claim 3 (Sentinel-2 export, then re-scoring).
3. Claim 4, then claim 5.

## Amendment 1 (14 November 2026, written after the results of claims 1 and 2 were seen)

Two facts of implementation, no change of rule.
- montiferru_2021_fullwindow has only 4 blocks of 40 cells, fewer than the 5 folds, so it has no
  20 km block result; the 20 km summary covers 30 fires and names the missing one.
- FireCCI51 in Earth Engine (ESA/CCI/FireCCI/5_1) ends in 2020, so the FireCCI51 agreement of claim 3
  covers only the fires of 2017 to 2020. The Sentinel-2 reference covers every fire.
- The Sentinel-2 shares are fetched in tiles of 24 x 24 cells because a single whole-grid request
  did not finish; the computation per pixel is the one fixed in claim 3.

## Amendment 2 (14 November 2026, after the results of claims 1 and 2 were seen)

Two analyses are added because the literature review found that most wildfire susceptibility studies
use multi-year inventories, not one fire's scar, and because the claim is about published results.
They do not change claims 1 to 5; they are written before any of their numbers exist.

Claim 6. Multi-year label.
- Label: a cell is burned if MCD64A1 (MODIS/061/MCD64A1, BurnDate > 0) marks at least half of the
  cell burned at least once in the period. Burned share per cell from the native 500 m product
  aggregated to the fire's step8a grid by area mean. Two periods: (i) 2001 to 2023 (all years, the
  common inventory design); (ii) 2001 to the year before the fire (history only, the fire itself
  excluded).
- Check of the aggregation: the same rule applied to the fire's own label window must agree with the
  step8a label; the agreement (share of cells and Cohen's kappa) is reported.
- Same population, predictors, models, folds, null model, cAUC and distance bands as claims 1 and 2.
  Predictors are those of the fire's predictor window, as in inventory studies that use one recent
  predictor date.
- Decision rule: if the null model beats the THERMAL RF in at least 28 of the 31 fires under label
  (i) at 5 km blocks, the claim is stated for multi-year inventories too; otherwise the paper limits
  claim 1 to single-event labels and reports claim 6 as the boundary.

Claim 7. Re-analysis of published open datasets.
- Datasets: every openly downloadable wildfire susceptibility dataset with coordinates and labels
  found by the search of 14 November (list in the project research notes), up to ten.
- For each: the authors' split if it can be recovered, otherwise their declared split rule
  (random or spatial) re-created with seed 42; the geographic null model scored on the same test
  points; its AUC compared with the AUC the paper reports and with a RF on the authors' predictors.
- Reported per dataset, no pooling across datasets; whatever it shows.

## Amendment 3 (14 November 2026, after all results were seen, prompted by an internal review)

Changes made after the results of claims 1 to 7 were known. Each is reported as post hoc in the paper.
- Claim 3: a cell enters the Sentinel-2 check only if at least half of its 20 m pixels have a valid dNBR,
  and shares are shares of the observed part of the cell. The MCD64A1 reference and the three variants are
  all scored on these cells. 111 of 436,721 cells are excluded; the decision is unchanged.
- Claim 3: the paper reports both thresholds. Reading the 0.27 threshold as the interpretable one (because
  the 0.10 threshold flags about a tenth of the cells beyond 10 km) is a post hoc judgement.
- Claim 4: intervals of transfer means are recomputed with fires as the resampling unit (a direction is
  counted once per copy of its source and of its target), as for the similarity correlations.
- Claim 1: the mean within-fire difference between the thermal and baseline cAUC gets a paired bootstrap
  interval over fires.
- Claim 7: the Alberta temporal comparison gets a 95% interval for the null model from 2000 bootstrap
  resamples of the test cells, beside the intervals the package reports for the published models.
- Claim 3 (second review round): the error share at 0.5 now uses "at least half" (>= 0.5), the same rule as
  the Sentinel-2 label; the shares changed in the fourth decimal.
- Implementation only: paths are read from THERMAL_TWIN_PAPER and THERMAL_TWIN_SCALEUP, and the transfer
  gate reads Table S8 from the committed paper/supplementary.md (identical 20 values); both gates pass as before.
- Implementation only (third review round): run_batch.sh reads the run folder, the Python interpreter and the
  Earth Engine project from THERMAL_TWIN_SCALEUP, THERMAL_TWIN_PYTHON and GEE_PROJECT, and the worker lists of
  the official run are committed as workers.txt. The >= 0.5 change of claim 3 affects only the error-share
  counter, not the labels of the rescoring variants, so no rescored AUC changed.

## Amendment 4 (14 November 2026, after all results were seen, prompted by a reviewer-style assessment)

Robustness analyses added post hoc; they are reported as such and change no decision rule.
- claim1_robustness.py: a model with the THERMAL predictors plus the distance to the nearest burned training
  cell, in the same folds, against the null model; AUC within folds (size-weighted mean); designs with the
  block grid shifted by half a block and fold seeds 7 and 2026; per-fold counts of the 20 km design; the
  calibrated AUC for matching tolerances 0.20, 0.33 and 0.50 and three orders of the burned cells.
- claim3_geometry.py: the Sentinel-2 variants that change the burned cells rescored with distance bands
  recomputed from their own burned cells, beside the fixed-geometry check, with paired differences from the
  MCD64A1 reference on the same fires.
- scripts/scaleup/selection/: the fire selection scripts and their outputs, copied from the pilot folder.
