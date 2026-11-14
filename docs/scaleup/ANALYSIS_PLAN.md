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

## Amendment 5 (14 November 2026, after all results were seen, prompted by a second reviewer-style assessment)

Post hoc checks, reported as such; no decision rule changes.
- claim1_validity.py: the fixed 5 km predictions rescored inside the burned-cell bounding box plus 0.05 and
  0.10 degree; the thermal RF refitted without land cover; the 2022-2023 fires alone; distance bands with the
  unburned cells restricted to the middle three quintiles of their Mahalanobis distance to the burned cells.
- claim6_multiyear.py: a third label, burns from the first day of the label window to the end of 2023
  (no burn before the predictor window enters the label); export by multiyear_label_export.py --prospective.
- claim7_protocol.py: null AUC, cAUC and distance bands on the four open datasets that ship predictors, with a
  random forest on the authors' split; the distance from each Alberta negative to the same year's positives.
- planned_outputs.py: FireCCI51 agreement, per-fire Spearman trend over bands, landscape heterogeneity by
  band and the paired near-band difference, which the plan listed and the first draft did not report.
- s2_label_check_export.py --offset (dNBR offset, Key and Benson 2006): attempted; the first fire did not
  finish in 25 minutes and the run was stopped. Not reported unless it is completed.
- geonull/: the three numbers as a standalone module with unit tests; check_against_study.py compares it with
  this code on the 31 fires.

## Amendment 6 (14 November 2026, declared BEFORE any of the following is computed on the fires or simulated)

The paper is reframed around the question of when a model comparison carries over when the evaluation
geometry changes. Two analyses are added; their definitions, settings and decision rule are fixed here.

### 6.1 Distance-standardised AUC (sAUC)

- Covariate z of a test cell: its distance (km) to the nearest burned cell of its fold's training set (the
  null model's score, sign reversed); defined for burned and unburned cells alike.
- Strata of z: [0, 0.5), [0.5, 1), [1, 2), [2, 5), [5, 10), [10, inf) km. AUC_b is the AUC between the test
  burned and test unburned cells of stratum b, out-of-fold predictions pooled over folds. A stratum is
  supported when it holds at least 20 burned and 20 unburned test cells.
- sAUC_Q = sum_b q_b AUC_b / sum_{b supported} q_b over the supported strata, coverage = sum_{b supported} q_b.
  sAUC is reported only when coverage >= 0.80; otherwise "not supported" with the coverage.
- Primary Q: the distribution of z among the fire's burned test cells (AUC at equal distance from known
  burns, averaged over where burns occur; the target that the calibrated AUC approximates by matching).
  Secondary Q: uniform over the supported strata, and one common reference Q_ref, the distribution of z among
  all burned test cells of the 31 fires pooled, for comparison across fires and datasets.
- Reported for the null model, the thermal and baseline RF and HGB at 5, 10 and 20 km blocks, with the
  fire bootstrap (2000, seed 42) as elsewhere, and on the four open datasets of claim7_protocol.py.
- The pooled AUC is also written as sum_b w_b AUC_b over the distance-to-fire bands of the unburned cells
  (w_b = share of unburned cells in band b, exact when the burned cells are fixed); the AUC under the study
  rectangle margins 0.05, 0.10 and 0.15 degree is reported from this identity and from direct rescoring.

### 6.2 Semi-synthetic experiment with known truth

- Landscapes: the population cells (coordinates and real predictors) of the 31 primary fires.
- Latent risk: eta = a * E + b * S + noise (standard normal), where E is the standardised mean of four real
  predictors (NDVI, elevation, slope and the predictor-window LST, each standardised within the fire, signs
  +, -, +, + in that order) and S a Gaussian random field with exponential correlation of length L
  (independent of E, unit variance). Burned = the cells whose eta exceeds the quantile that gives the fire's
  real burned share.
- Grid: a in {0, 0.5, 1, 2}, b in {0, 1, 2, 4}, L in {2, 10} km (32 scenarios), one draw per fire and
  scenario, seed = 1000 * fire index + scenario index.
- Candidate models (RF, 300 trees, min_samples_leaf 3, balanced): M_env on the four signal predictors plus
  two independent standard-normal noise predictors; M_geo on the cell coordinates. Both are fitted and scored
  with the 5 km block design of the study.
- Truth: the model with the higher AUC on a second label of the same landscape drawn with the same E and a
  new, independent S field and noise (the comparison that carries over to a new geometry of burning).
- Measures compared: pooled AUC, calibrated AUC, sAUC (primary Q). For each scenario, the share of fires in
  which each measure ranks M_env and M_geo as the truth does (ties count as wrong).
- Decision rule (fixed now): the paper claims an advantage of sAUC only if, averaged over the 24 scenarios
  with b > 0, its agreement with the truth exceeds that of the pooled AUC by at least 10 percentage points and
  is not lower than that of the calibrated AUC by more than 2 points. Otherwise sAUC is reported as a
  descriptive re-expression of the cAUC idea and no advantage is claimed. Scenarios where sAUC is not
  supported count as wrong for sAUC.

### 6.3 Correction to 6.1 (14 November 2026, before any sAUC was computed on the fires)

The unit test of the module on a synthetic grid (one circular burned patch, 5 km blocks, geonull/test_geonull.py)
showed that within the strata of 6.1 the null model still separates the classes (sAUC of the null model 0.84),
because a stratum such as 2-5 km is wide relative to the spread of z inside it. The strata are therefore
replaced, before any fire was scored, by geometric strata matching the relative tolerance of the calibrated
AUC: [0, 0.51) km, then [0.51 * 1.33^k, 0.51 * 1.33^(k+1)) for k = 0, 1, ... (on the test grid the null model's
sAUC became 0.51-0.53). Everything else in 6.1 stands (support of 20 and 20, coverage >= 0.80, primary Q the
burned cells' z, fire bootstrap). In addition, as in the calibrated AUC, the corrected value
sAUC_c = sAUC_model + 0.5 - max(0.5, sAUC_null) is reported beside sAUC; the decision rule of 6.2 uses sAUC_c.

### 6.4 Status note (14 November 2026, before the push of this branch)

- The prospective multi-year label of amendment 5 has no decision rule; it was added after the results of
  the two other labels were known and is reported descriptively only.
- The sAUC of 6.1/6.3 was computed on the 31 fires (claim8_sauc.py) after 6.3 was committed and before this
  push; its commit order is the only record of that sequence. The semi-synthetic experiment of 6.2
  (claim9_synthetic.py) was started after 6.3 and is still running at the time of this push.
- Comparisons between sAUC and cAUC are made on the same fires (those where sAUC is supported).
- The frozen text above (sections written before amendment 4) is kept unchanged, including its references to
  internal notes and to the earlier manuscript.

### 6.5 Correction (14 November 2026)

The first export of the prospective label (amendment 5) filtered MCD64A1 from the first day of the label window,
which drops the fire's own monthly image (MCD64A1 images are dated on the first of the month): its mean burned
share was 4.1% against about 10% for the single-event label, and two fires had no burned cell. The export now
takes the label-start month with BurnDate >= the start day and all later months to 2023; the result of the
first export is discarded and the label is re-exported and re-analysed. The label stays descriptive.

### 6.6 Timeline and reporting addition (14 November 2026, while the semi-synthetic run was in progress)

Times in UTC. Commit times are the author's and are not independent evidence; the other times are.
- 18:56:51 commit 579ed1b (amendment 6), 18:57:47 commit 951b4dd (6.3; the unit test of the module that
  prompted it ran after amendment 6 was written).
- 19:00:18 claim9_synthetic.py started (creation time of its log file); 19:02:59 the results of the first
  fire (32 scenarios) were written to claim9_synthetic_runs.csv. They were not inspected before the push.
- 19:05:28 push of commit d29e04e (amendment 6, 6.3, 6.4 and the unchanged claim9_synthetic.py) to GitHub,
  recorded server-side in the repository's activity log.
- 19:05:38 Software Heritage archive of the repository, snapshot
  swh:1:snp:d76d390439762f05fe54abb877ef42841794daa4, branch scaleup-31fires at d29e04e.
So the independent records show the plan, the decision rule and the experiment code as they were about five
minutes after the run started, when one of 31 fires had been written. The finish time of the run is added to
its summary file.
- Reporting addition, decision rule unchanged: agreement is also given separately for the six scenarios with
  a = 0 and b > 0 (no environmental signal, so the truth is close to a coin toss) and for the 18 with a > 0.
- Note on 6.3: it changed the measure used by the decision rule from sAUC to the corrected sAUC_c, before any
  synthetic result; the max(0.5, .) correction is the one of the calibrated AUC (Hijmans 2012, plan claim 1).
- Sensitivity check, added while the run was in progress (decision rule unchanged): the rule is also computed
  without the first fire (manavgat_2021, written at 19:02:59, before the archived push), i.e. on the 30 fires
  whose results were written after 19:05:38. Both decisions are reported; if they differ, the paper says so.

## Amendment 7 (14 November 2026, while the claim9 run was in progress, before any of the following is run)

### 7.0 Corrections of wording in amendment 6 (no change to any computation)

- 6.1 called the calibrated AUC an approximation of the primary sAUC target. That is withdrawn. Matching
  equalises the distance distributions of the burned and unburned cells kept, but the AUC on the pairs still
  compares cells at different distances; sAUC compares cells within the same distance stratum. The two answer
  different questions and the paper says so, with a small analytic example.
- The null correction max(0.5, .) shifts both models of a fire by the same amount, so sAUC and sAUC_c rank
  two models identically, as cAUC and the AUC on the pairs do. The semi-synthetic experiment therefore compares
  three evaluation geometries: pooled AUC, AUC on distance-matched pairs, AUC within distance strata.
- Fires without support are described as "not supported under the declared strata and support rule", not as
  fires in which the comparison is undefined.

### 7.1 Partly persistent spatial field (claim10_persistent.py)

The truth of 6.2 redraws the spatial field independently, which penalises any spatial signal that would
persist in a new geometry of burning. A second experiment varies this: for the 24 scenarios of 6.2 with b > 0,
the truth label uses S2 = rho * S1 + sqrt(1 - rho^2) * S_new with rho in {0.5, 0.8} (S_new independent with
the same L, same E, new noise). Training label, folds, models and measures are as in 6.2 (one fit per fire
and scenario; seed 10,000,000 + 1000 * fire index + scenario index). The decision quantities of 6.2 are
computed separately for each rho, with and without the first fire. They are reported for each rho whatever
they show; they do not change the decision of 6.2. A smaller advantage of sAUC_c at larger rho is expected
if part of the geographic signal carries over, and is reported as such.

### 7.2 Fire-level paired intervals (claim9_intervals.py, reporting only)

For 6.2 and for each rho of 7.1: per fire, the agreement of each measure with the truth over the scenarios
with b > 0; paired differences sAUC_c - AUC and sAUC_c - cAUC with 95% intervals from 2000 bootstrap resamples
of fires (seed 42).

### 7.3 Support sensitivity (claim9_intervals.py, reporting only)

Coverage 0.70 / 0.80 / 0.90, minimum 10 / 20 / 40 burned and unburned cells per stratum and stratum ratio
1.20 / 1.33 / 1.50, each varied alone from the declared setting (0.80, 20, 1.33): on the 31 fires the number
of fires supported and the mean sAUC_c of the thermal RF (5 km); on the saved scores of 7.1 the agreement of
sAUC_c with the truth. On the 31 fires, the share of fires in which cAUC and sAUC_c (and the pooled AUC and
sAUC_c) rank the thermal and the baseline RF the same way.

Run order: claim10_persistent.py after claim9_synthetic.py has finished, then claim9_intervals.py.
