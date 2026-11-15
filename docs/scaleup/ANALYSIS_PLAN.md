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

### 7.4 Addition to 7.1 (14 November 2026, before claim10_persistent.py was run)

rho = 0 is added to the truth labels of 7.1 (same fits, a third truth label with S2 = S_new, no extra random
draws), so that the effect of rho is read on the same models as {0, 0.5, 0.8}. rho = 0 is included as a
within-run reference; it does not replace the decision of 6.2. The saved scores gain a y2_rho0 column.

## Amendment 8 (15 November 2026, after claim9 and claim10 were seen; everything here is exploratory)

### 8.0 Record

- While amendment 7 was written (19:35 UTC), claim9_synthetic.py was running and printing every run's
  measures to its console; the idea of a partly persistent field came from a critique of the truth
  definition of 6.2 (that a fully redrawn field penalises any spatial signal), not from those results, but the
  results were visible. GitHub recorded the pushes of 7 and 7.4 at 19:35:54 and 19:41:13 UTC.
- claim10_persistent.py ran from 20:06:46 (log creation) to 20:52:58 UTC (last write of its runs file).
- Base-rate finding (after the results): the measures are identical across rho because the models are; only
  the truth changes. The share of runs whose truth is the environmental model is 0.76, 0.38 and 0.24 at rho 0,
  0.5 and 0.8, and a constant rule "always choose the environmental model" agrees with the truth in 76-80% of
  runs at rho = 0. Agreement with the truth therefore mixes the measure's preference with the base rate. From
  here on, every comparison of measures reports separately (i) the preference, the share of runs in which the
  measure chooses the environmental model, and (ii) discrimination, balanced accuracy and Cohen's kappa of
  the choice against the truth. The interpretation of 7.1 ("which geometry is right depends on persistence")
  is withdrawn. The decision of 6.2 stands (not met).

### 8.1 Re-reporting of claim9 and claim10 (no new computation)

Per scenario (a, b, L, rho) and pooled: preference of each measure; balanced accuracy and kappa against the
truth; AUC loss on the truth label of the measure's choice (truth AUC of the better model minus truth AUC of the
chosen one); Spearman correlation over fires, within each scenario, between each measure's difference
(env - geo) and the truth difference. a = 0 scenarios are reported apart. Heat maps over a x b per L and rho.
The two rho = 0 arms (claim9 and claim10 rho 0) are reported as two replicates, not as a range.

### 8.2 Oracle truth on fixed scores (claim11_oracle.py)

On the saved claim10 scores (out-of-fold scores of M_env and M_geo, null scores, y1), with E and S1 regenerated
from the claim10 seeds: for rho in {-0.5, -0.25, 0, 0.25, 0.5, 0.7, 0.8, 0.9}, K = 50 second labels are drawn
(eta2 = a*E + b*(rho*S1 + sqrt(1 - rho^2)*S_new) + noise, same burned share; seed 20,000,000 + 1000 * fire
index + scenario index, draws in the order rho, k). Per run: expected truth AUC of each model over the K draws,
the oracle truth (the model with the higher expected AUC), the rank stability (share of draws in which M_env
wins) and the expected AUC loss of each measure's choice. Negative rho stands for reduced reburning of recently
burned ground (fuel depletion). No model is refitted.

### 8.3 Monte Carlo replicates (claim12_replicates.py)

The design of 6.2 (rho = 0 truth, 5 km blocks, refitted models) with five new draws per fire and scenario
(seed 30,000,000 + 100,000 * draw + 1000 * fire index + scenario index). Agreement, preference, balanced accuracy
and kappa of the three measures and all pairwise differences (cAUC - AUC, sAUC_c - AUC, sAUC_c - cAUC) with
95% intervals from 2000 bootstrap resamples of fires (draws kept within fires), seed 42.

### 8.4 Blocks of 20 km (claim12_replicates.py --blocks 40)

One draw per fire and scenario of the 6.2 design with blocks of 40 cells (about 20 km), seed 40,000,000 +
1000 * fire index + scenario index; fires with fewer than five blocks are skipped and listed.

### 8.5 Scenarios calibrated to the real fires (claim13_calibrated.py)

Targets, from the real fires at 5 km blocks: null-model AUC 0.958, share of burned cells kept by matching 0.57,
share of fires with sAUC support 19/31. Calibration (seed 50,000,000 + ...): for each fire, a in {0.5, 1, 2},
b in {2, 4, 8, 16}, L in {5, 10, 20, 40} km, one draw each; the (b, L) pair per fire and a that minimises
|null AUC - 0.958| / 0.05 + |kept share - 0.57| / 0.10 is retained. Main run with new seeds (60,000,000 + ...):
three draws per fire and a at the retained (b, L), measures and the 8.1 quantities, plus a table comparing the
simulated and the real fires on null AUC, kept share, sAUC support and burned share.

### 8.6 Field checks (G4, descriptive)

Realised correlation of the simulated field against distance (0.5 to 40 km) in five fires of different size,
compared with exp(-r/L), and the same with the padding doubled to 4x, to show the effect of the finite raster
and of centring within the fire.

### 8.7 Reporting additions (15 November 2026, before 8.2-8.5 results)

- Relative loss: the mean AUC loss of a measure's choice divided by the mean achievable difference, the
  absolute difference between the two models' truth AUCs (ratio of means over runs). Reported with the
  absolute loss in 8.1, 8.2 (expected AUCs), 8.3, 8.4 and 8.5.
- The constant rules ("always env", "always geo") are labelled as references that know the distribution of
  the truth, which only a simulation provides; they are not candidate measures.
- No statement about the size of the loss is written before the calibrated scenarios of 8.5 are known.

## Amendment 9 (15 November 2026): G1, transfer of the focal-event model choice to later real burning

Written after a design review by two independent reviewers; declared before any G1 score was compared with any
future label. Everything in amendment 9 is exploratory except the decision rule of 9.5, which is fixed here.

### 9.0 Seen before this design

All results up to amendment 8. Label counts only, from the existing multi-year rasters: 18 of 31 fires have at
least 30 cells burned after the focal label window (approximate count; prospective minus window band); future
burns overlap the focal scar in at most 21 cells per fire; burns before the focal year are abundant (21 to
8,182 cells). The population choice of 9.2 was made after this inspection of label counts. No comparison of a
G1 score with a future label has been seen. A precision estimate from the claim9 synthetic runs (9.6) was
computed for this amendment.

### 9.1 Question

How well does the choice between two models made on the focal event carry over to later real burning in the
same study rectangle? The future label is one realisation of later burning, which depends on weather and
ignitions; it is not the true underlying susceptibility. The out-of-fold map is assembled from five fold
models and is not a single operational model trained on all focal data.

### 9.2 Labels and populations

- Future label (future_label_export.py, MCD64A1 v061): a 500 m cell is future-burned if at least half of its
  area has a BurnDate after the focal label_end and on or before 2023-12-31. Monthly images are dated on the
  first of the month; the month of label_end uses BurnDate > day of year of label_end, later months any
  BurnDate > 0. Taken directly from BurnDate, not by subtracting masks, so reburned cells are kept.
- Unmapped observations: per pixel the share of months in the horizon with BurnDate < 0 or masked; cells whose
  mean unmapped share exceeds 0.10 are excluded from the future population, never counted as unburned.
- Two-year horizon (sensitivity): label_end < BurnDate date <= label_end + 730 days, same rules.
- Primary future population: the model population of the fire minus the focal-scar cells (focal y = 1) minus
  unmapped cells. Cells burned before the focal window stay. Full population (scar included) is a sensitivity.
- Measures on the focal event are computed on the full focal population, as in claims 1-8.
- Eligible fires: at least 30 future-burned and 30 future-unburned cells in the primary future population.
  The excluded fires are listed with the reason (too few future burns, horizon, unmapped).

### 9.3 Candidate models

Primary comparison: thermal RF (cached out-of-fold scores, 5 km blocks, claims 1-2) against a coordinate RF
whose two features are the cell centre coordinates in km on the fire's grid (f.xy, north-south and east-west
km from the grid origin), RandomForestClassifier(300 trees, min_samples_leaf 3, class_weight balanced,
random_state 42), the same five folds (StratifiedGroupKFold, blocks of 10 cells, seed 42). Secondary: thermal
RF against baseline RF. The null model is a descriptive reference, not a candidate. No combined model in G1.

### 9.4 Measures and losses

Each measure chooses on the focal event: pooled AUC, cAUC (primary pair), sAUC_c (secondary; when it is not
supported the choice counts as the model with the worse future AUC). For each fire, future AUC of both
candidates on the primary future population; loss L of a measure = best future AUC minus future AUC of its
choice. Primary quantity D = L(pooled AUC) - L(cAUC); secondary L(pooled AUC) - L(sAUC_c) and
L(cAUC) - L(sAUC_c). Relative loss (mean L / mean |future AUC difference|) is reported, not primary.

### 9.5 Decision rule (fixed now)

Fires weighted equally. Paired bootstrap over fires, 10,000 resamples, seed 42; fires whose study rectangles
intersect are resampled together as one geographic cluster.
- Advantage of cAUC over the pooled AUC for this target is claimed only if the lower end of the 95% interval
  of mean D is above 0. It is called practically important only if mean D >= 0.01 AUC as well (0.01 is about
  one eighth of the mean difference of 0.082 between the two models' truth AUCs in the claim9 runs).
- Equivalence is claimed only if the 90% interval of mean D lies within -0.01 to 0.01.
- Otherwise the result is inconclusive, which is not evidence of equivalence.

### 9.6 Expected precision

From the claim9 synthetic runs (b > 0), the run-level SD of D is 0.055 AUC, so with 18 fires and one
comparison per fire the smallest difference detectable with 80% power at alpha 0.05 is about
2.8 * 0.055 / sqrt(18) = 0.036 AUC. Differences near the 0.01 threshold are therefore not expected to be
detectable; an inconclusive result is the likely outcome unless the real difference is large.

### 9.7 Clustering of future burns and sensitivities

Per fire: number of future burning events (8-connected components of future-burned cells per year of first
future burn) and years, and the share of the largest event. Sensitivities, all reported, none changes 9.5:
equal weight per event (sample weights so that each event's positives sum to one), leave one event out (range
of mean D), two-year horizon, full population, secondary comparison.

### 9.8 G1b, G1c, G1d (descriptive, exploratory)

- G1b: future AUC of minus the distance to the nearest focal-scar cell (higher = closer), on the primary
  future population; the expected direction is not assumed; not called rho.
- G1c: burn history from 2001-01-01 to the day before the focal predictor window starts (share of the cell
  burned at least once); thermal RF against thermal RF plus this history share, same folds, pooled AUC, cAUC
  and sAUC_c on the focal event, and the history share alone as a score.
- G1d: the three repeat pairs; chronology and shared cells checked first; AUC on the later fire's label of the
  thermal and coordinate RF trained on the earlier fire; descriptive only.

### 9.9 Correction to 9.2 (15 November 2026, from a one-fire label test, before any G1 comparison)

In Earth Engine, MCD64A1 BurnDate is masked on unburned land, so "BurnDate < 0 or masked" flagged nearly every
cell as unmapped (33,345 cells in the test fire px25_2017). An unmapped month is now one whose QA bit 0 (valid
land data) is 0 or masked; the 0.10 exclusion rule is unchanged. The test also fixed a type error in the band of
first future-burn years; its label counts (no scores) were the only output seen.

## Amendment 10 (15 November 2026): G2, G5, G1d; written after the G1, Z3, Z4 and Z5 results were seen

All exploratory. Seen before this amendment: every result up to amendment 9, including G1 (the coordinate RF
was chosen on the focal event by the pooled AUC in 18 of 18 and by cAUC in 17 of 18 fires and did worse on
later burning; between the thermal and baseline RF the pooled AUC chose the thermal RF in 18 of 18), the
Monte Carlo, 20 km and calibrated runs.

### 10.1 G2: location-using models that are used in practice (claim15_location.py)

Same 18 fires, focal folds, future labels, populations and losses as 9.2-9.4. Pairs, each against the thermal RF:
- primary: thermal RF plus the two cell-centre coordinates (km, f.xy) as features (thermal+coord);
- secondary: thermal RF plus the distance to the nearest burned cell of the training folds, measured for
  training cells by the inner split of claim1_combined.py and for test cells to the burned training cells
  (thermal+distance);
- tertiary: k-nearest-neighbour classifier on the coordinates, k = 25, distance-weighted (coord-kNN), to check
  that the G1 coordinate result is not specific to random forests.
RF settings as in 9.3. For each pair and measure (pooled AUC, cAUC, sAUC_c): number of fires in which the
measure chooses the location-using model, loss and relative loss on later burning, and the mean future AUC
difference (thermal minus location-using) with a 95% fire-bootstrap interval (10,000, seed 42, clusters of 9.5).
Rule fixed here: a pair is called a transfer failure of within-event evaluation if the pooled AUC chooses the
location-using model in at least 12 of 18 fires and the 95% interval of the mean future AUC difference is above 0.

### 10.2 G5: dependence on single fires, countries, years and events (claim15_location.py)

For the G1 pair (thermal vs coordinate RF) and the 10.1 primary pair: the mean future AUC difference and the
mean loss of each measure recomputed leaving out one country at a time (regions.EXPERIMENTS country), one focal
year at a time and one fire at a time (min and max reported), and with the largest future event of each fire
removed from the positives (cells of other events kept).

### 10.3 G1d: repeat pairs (claim15_location.py)

Pairs (earlier -> later): rp01_2020 -> px17_2022, px16_2022 -> rp02_2023, evia_2021_extended -> rp03_2023.
Chronology and the number of cells shared on the 500 m grid (lon/lat match) are reported first. Thermal RF and
coordinate RF (lon/lat in km) trained on all cells of the earlier fire, scored on the later fire's cells with the
later fire's predictors; AUC on the later fire's label beside the measures' choice on the earlier fire. A pair
whose later fire has no analysis table is reported as missing. Descriptive only.

### 10.4 Limits written into the paper

The calibrated scenarios of 8.5 reached the real null AUC only in part (0.926 against 0.964) and kept far more
burned cells in matching (0.82 against 0.57). The 13 fires without enough later burning are mostly 2021-2023
fires, so G1 and G2 lean on 2017-2021 fires.

### 10.5 Follow-ups (15 November 2026, after the claim15 results)

- claim15_location.py ran from 07:38:17 (log creation) to 07:40:20 UTC (summary written), after the push of
  its script (7163c8b, 07:38:11 local commit time); amendment 10 reached the server at 07:37:14.
- Countries: the regions file has no country for the 26 added fires, so the leave-one-country-out check of
  10.2 had only three groups. Countries are assigned from the centroid of each fire's burned cells with the
  LSIB 2017 boundaries in Earth Engine (selection/fire_countries.json) and the check is rerun
  (claim15_followup.py); everything else of 10.2 is unchanged.
- G1d shared cells: the lon/lat match rounded to five decimals counted no shared cell because the rectangles
  of the two fires of a pair have different grid origins. Shared cells are recounted as cells of the later
  fire whose centre lies within half a cell (0.0023 degree) of a cell centre of the earlier fire.
- The D of the distance-feature pair (L pooled AUC - L cAUC = +0.018) has no declared rule; it is reported
  with its fire-bootstrap interval as a descriptive observation.

## Amendment 11 (15 November 2026): forward selection across past events, a sequence simulation, and a
## replication of G1/G2 on burning from 2024 to September 2026

Declared before any computation or export that scores a model against a label named here. Rules, settings and
seeds below are fixed now and are not changed afterwards.

### 11.0 Seen before this amendment

All results of amendments 1-10. Label counts only (label_counts_11.json, commit 39b35ff): for each primary fire,
the burned cells outside the focal scar in each year 2013-2026 (MCD64A1 v061, last published image
2026-09-01). From them: 6 sites have at least 3 past years with at least 100 such cells (px06_2017, px13_2021,
px03_2022, px10_2022, px17_2022, px23_2023); 18 sites have at least 30 such cells in 2024-2026. The
eligibility of 11.4 rests on these counts. No score has been compared with any 2024-2026 label. The support
threshold of 11.2 (3 years, 100 cells) is the one proposed before the counts and is not changed.

### 11.1 Question and candidates

For a model family trained on one focal fire, can the site's own burning history choose between an
environmental and a location-using model better than within-fire AUC? Primary candidates: thermal RF against
thermal RF plus the two cell-centre coordinates (as in 10.1). The coordinate-only RF is a secondary stress test.

### 11.2 Forward selection (the proposed selector)

- Past events: every calendar year from 2013 to the year before the focal predictor window with at least 100
  burned cells outside the focal scar on the focal grid. For each such year s, predictors are produced from its
  own pre-event window (58 days ending the day before the first burn date of the year's largest cluster, as in
  the fire selection rule), the label is the year's burned share >= 0.5, the population is the focal model
  population minus the focal scar, and the candidates are trained on year s (all cells) and scored on the burns
  of years s + 1 and s + 2 (cells burned in year s removed from that evaluation).
- Support: at least 3 distinct target years and in total at least 100 burned and 100 unburned evaluation cells.
  Replicates of the same target year are averaged within the year first. Years are weighted equally.
- Rule: the location-using model is selected only if the lower end of the 95% interval of the mean paired AUC
  difference (location minus environmental), from 10,000 bootstrap resamples of target years (seed 42), is above
  0.01; otherwise the environmental model is selected. Sites without support default to the environmental model,
  and the share of sites with support is reported. The focal-fire AUC is not used in this selection.
- After selection, every candidate is trained on all focal cells with the same settings; selections and final
  maps are frozen before any 2024-2026 label is exported.
- Comparators, fixed: within-fire pooled AUC, within-fire cAUC, "always environmental", "always location"; the
  last two are truth-informed references in the simulation and fixed rules in real data.
- Secondary competitor: today's focal map scored against burns at least 5 years old at the focal window
  (2013 to focal year - 5), cells burned in the 5 years before the focal window removed, focal scar removed,
  same thresholds. A 10-year limit and a symmetric 5 km buffer around the focal scar are sensitivities only.
- On real data, forward selection is run on the 6 supported sites and reported descriptively (11.0).

### 11.3 Sequence simulation (the evidence for the method)

On the 31 landscapes (population cells and real predictors), years 2013-2026 are simulated:
eta_t = a * E_t + c * P + b * S_t - f * D_t + noise_t,
- E_t: the environmental index of 6.2 computed from the observed predictors at t; NDVI and LST observed at t are
  shifted by -0.5 and +0.5 standard deviations times D_t (post-fire effect, only from burns before t);
- P: persistent field (L = 10 km, fixed per landscape and draw); S_t: event field (L calibrated, new each year);
- D_t = sum over earlier years u of B_u * exp(-(t - u) / 8) (fuel deficit recovering with an 8-year scale);
- burned share per year 0.03 for past and future years and the fire's real share in the focal year (2017-2023 as
  for the real fire); the focal label is drawn in the real focal year.
- Regimes (8): c in {0, 1} (persistent location signal), f in {0, 2} (fuel depletion), relation stable or
  drifting (the four weights of E rotate linearly so that by 2026 each has moved by 0.5 of its 2013 value
  toward the mean weight).
- a = 1; b and L of S_t calibrated once, before the main run, on the focal year with seeds 80,000,000 + ...,
  over b in {2, 4, 8, 16} and L in {5, 10, 20, 40} km, to the real null AUC 0.964, the median largest-event
  share 0.59 of later burning and the real matching support (kept share 0.57); the pair minimising the sum of
  |difference| / (0.05, 0.10, 0.10) is used for all regimes.
- Draws: 3 per landscape and regime, seed 70,000,000 + 1000 * landscape index + 100 * regime index + draw.
- Models: RF with 100 trees, min_samples_leaf 3, balanced (cost), candidates as in 11.1; within-fire measures
  under the 5 km block design; forward selection as in 11.2 on the simulated past years.
- Oracle: for each candidate trained on all focal cells, the expected AUC over 50 independent future
  trajectories of 2024-2026 (same regime and fields, new S_t and noise); loss = best expected AUC minus that of
  the selected candidate.
- Success rule (fixed now): the paired loss reduction of forward selection over the pooled AUC and over cAUC,
  each averaged over landscapes, regimes and draws, must both be positive by one-sided tests with Holm
  correction at 0.05 (bootstrap over landscapes, 10,000 resamples, seed 42; landscapes whose rectangles
  intersect resampled together), and both mean reductions must be at least 0.01 AUC. Reported in full: loss,
  preference, balanced accuracy, kappa, the fixed references, and per regime. If the rule is not met, or the
  real data are inconclusive, the paper does not say that model selection is solved.

### 11.4 Replication of G1/G2 on 2024-2026 burning

- Label: a cell is later-burned if at least half of its area has a BurnDate from 2024-01-01 to the last published
  month (2026-09); the QA rule of 9.9 over the same months; population = focal model population minus the focal
  scar minus unmapped cells. Cells burned in 2017-2023 stay in the population and are counted separately.
- Scores: the frozen focal out-of-fold scores of G1 and G2 (thermal, coordinate RF, coord-kNN, thermal+coord,
  thermal+distance), unchanged.
- Primary set: all sites with at least 30 later-burned and 30 later-unburned cells. Secondary set: the sites of
  the primary set that were excluded from G1 (no later-burning score of them was ever seen); listed by the script.
- Rules 9.5 (D between the losses of pooled AUC and cAUC) and 10.1 (transfer failure) unchanged; Holm correction
  across the two sets for each rule.

### 11.2a Correction to 11.2 and 11.3 (15 November 2026, before 11.2 or 11.3 is run, after label counts only)

- Leak: in 11.2 a past year s could be evaluated on years s + 1 and s + 2 that reach into the focal year or into
  2024-2026 (the labels of G1 and of 11.4). Now both the training year and every evaluation year must lie
  entirely before the focal year (calendar years up to focal year - 1); if s + 2 does not, only s + 1 is used; if
  neither does, the year is not used. The same rule applies to the simulated past years of 11.3.
- Definition made explicit: a target year counts toward the support of 11.2 only if it has at least 30 burned
  evaluation cells (an AUC can be estimated). This definition was written after the counts below were seen.
- Recount (label counts only, label_counts_11a.json): with the cut-off, the 6 sites of 11.0 keep at least 3
  target years, but with the 30-cell definition only 2 sites are supported (px03_2022: 2015-2019, px10_2022:
  2016, 2017, 2019). The threshold (3 years, 100 cells) is not changed. 11.2 on real data is therefore a
  descriptive demonstration on 2 sites; the evidence for the method rests on 11.3 and 11.4, and this is stated
  as a limitation.
- No regional pooling of past events across sites is added: the question of 11.1 is selection by the site's own
  history, the calendar cut-off limits pooled sites in the same way, and a pooled selector would be a different
  method that has not been declared.
