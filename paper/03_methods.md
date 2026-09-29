# 3. Data and methods

## 3.1 Study regions and temporal windows

Five Mediterranean wildfire regions were analysed (Fig. 1): Manavgat 2021 and Muğla 2021 in Türkiye,
Bejís 2022 in Spain, North Evia 2021 in Greece and Montiferru 2021 in Sardinia. All five are large,
well-documented fires. They were not sampled from a defined population of fires, so the results
describe these events. Each region is a rectangle in EPSG:4326 around the fire. It was not clipped to
the fire perimeter, so unburned cells around each fire form the negative class. The rectangles were
not all fixed before any outcome was seen; the record for each region is given in Section S3.3 and
Table S19. The North Evia rectangle was extended after the first one showed a very high burned
fraction; the first rectangle is kept as a sensitivity arm (Section S1.1). A sixth region, Kozan
2023, was used as a negative control and was excluded by the gate of Section 3.3.

Each region has two windows that do not overlap. The **predictor window** ends the day before the
**label window** starts, so no predictor observation is later than the first labelled burning.
Predictor windows are 57 to 61 days long and label windows 35 to 59 days. Four earlier years of
composites from the same calendar window are used as the baseline for the anomaly channels. The
processing chain is shown in Fig. 2.

## 3.2 Burned-area label and the ~500 m analysis grid

Labels were taken from the MODIS MCD64A1 burned-area product, Collection 6.1 [@Giglio2018], through
Google Earth Engine [@Gorelick2017]. Its errors [@Boschetti2019] limit every model in this study.
The analysis grid is built from the 30 m reference grid of the processing pipeline in blocks of
17 × 17 pixels. A cell is about 510 m north to south and 390 to 407 m east to west, with an area of
0.199 to 0.208 km² (a MODIS cell is 0.215 km²). A cell is labelled burned when any of its pixels has
a burn date in the label window. This rule can widen a scar by up to one cell at its edge. Water
cells are removed by the population filter of Section 3.5.

**Earlier burning.** Cells that burned in the predictor window were removed in Muğla (49 cells),
North Evia (16) and Montiferru (61). Manavgat had no burning in that window. In Bejís this removal
was not applied, so 49 cells that burned before the label window were kept. Burning in the five
previous years was not screened in any region. When those cells were excluded, the mean transfer
gain fell from +0.007 to +0.003, and the within-region gain stayed positive in all regions (Section
S3.1.1).

**Corrected Manavgat label.** The label first used for Manavgat missed the first four days of the
fire, 28 to 31 July. The corrected label only adds burned cells. It raises the number of burned cells
in the primary population from 784 to 2,935. "Original label" in this paper means the label before
this correction. The correction and its control run are described in Section S3.1.2.

## 3.3 Burned-landcover admissibility gate

Before modelling, each region had to pass a gate. The gate asks what fraction of the burned cells is
covered mainly by natural vegetation, using ESA WorldCover classes [@Zanaga2022]. A region is
admitted if this fraction is at least 0.50 and at least 30 cells burned. It is rejected as a cropland
control if the cropland fraction is at least 0.50 (Section S3.1).

## 3.4 Predictor variables

Ten predictors were used (Table S20). The **baseline** set contains elevation and slope from the
Copernicus DEM GLO-30 [@CopernicusDEM], dominant land cover from ESA WorldCover v200 [@Zanaga2022],
and the median NDVI of the predictor window from Landsat 8 Collection 2 Level-2 [@LandsatC2L2].
These change little over one fire season. The **thermal** set adds six channels from Landsat 8
surface temperature. They are screened for quality and composited as the median of the predictor
window. The six channels are current LST, its anomaly against the four baseline years, the TVDI
[@Sandholt2002], its difference from the baseline years, a downscaled LST and a fused LST. The last two use MODIS MOD11A1
v061 daily LST [@MOD11A1] to fill gaps in Landsat (0.11 % to 9.70 % of pixels, depending on the
region). TVDI edges are fitted inside each area and window, so a TVDI value does not mean the same
moisture state in two regions (Section S3.4).

**The six thermal channels carry about two signals.** Current, fused and downscaled LST are
correlated at 0.97 to 1.00 in every region. Current LST and TVDI are correlated at 0.88 to 0.98, and
the two anomaly channels at 0.71 to 0.94. Two principal components explain 92 % to 98 % of their variance
(`paper/labelfix_rerun/labels/r4_dimensionality.json`). Counts over the nine numeric predictors are
therefore read with care.

**Land cover.** WorldCover v200 is built from 2021 images. This is after the fire for the four 2021
events. Burned land may therefore be under-represented in its pre-fire vegetation class. The wide
gate margins (Section 4.1) make it unlikely that this changes a gate decision.

## 3.5 Cell aggregation, validity and analysis populations

Cell values are means over the valid 30 m pixels of the cell. A cell is valid for modelling when
NDVI, elevation and slope are available for at least 30 % of the cell and at least one land-cover
pixel is valid. Thermal completeness is not required. Missing thermal values (6 % to 58 % of valid
cells, depending on the region) are filled inside the model pipeline (Section 3.6). The **primary**
population contains cells in which tree, shrub and grass cover together reach 0.50. Cropland and
water are therefore excluded. A **secondary** population of all valid cells is used only as a
within-region sensitivity arm in two regions (Section S1.17).

## 3.6 Classifier

The thermal set contains the baseline set (Section 3.4). Land cover is one-hot encoded. Missing
numeric values are replaced by the median and missing land cover by the most frequent class. These
values are fitted inside each training fold, and on the source region only in transfer, so no test
data are used in fitting. The adapted arms of Section 3.9 are the only exception. The classifier is a
random forest [@Breiman2001] with 300 trees, unlimited depth, `min_samples_leaf = 3`, balanced class
weights and `random_state = 42`. The same settings are used in every arm.

## 3.7 Spatial-block cross-validation and bootstrap uncertainty

Cross-validation is spatially blocked. Cell $`i`$ at grid position $`(r_i, c_i)`$ is assigned to the
block

```math {#eq:block}
b_k(i) = \left( \lfloor r_i / k \rfloor,\; \lfloor c_i / k \rfloor \right).
```

Five folds are drawn over whole blocks, stratified by label, so a block is never split between
training and test. Block sizes of $`k`$ = 2, 10 and 20 cells (about 1, 5 and 10 km) are reported.

Every score is a ROC-AUC on a named set of cells $`F`$, its **evaluation frame**. With $`F^{+}`$ the
burned and $`F^{-}`$ the unburned cells of $`F`$, and $`s_i`$ the predicted score,

```math {#eq:auc}
\mathrm{AUC}(s; F) = \frac{1}{|F^{+}|\,|F^{-}|} \sum_{i \in F^{+}} \sum_{j \in F^{-}} \left[ \mathbf{1}(s_i > s_j) + \tfrac{1}{2}\,\mathbf{1}(s_i = s_j) \right].
```

This is the probability that a burned cell in $`F`$ is ranked above an unburned one. The metric can
therefore change when the frame changes, even when no score changes (Section 3.12).

Uncertainty is estimated with a spatial-block bootstrap: blocks are resampled with replacement,
1000 times, with seed 42, and the 2.5 and 97.5 percentiles give the interval. Differences are paired
within each replicate. The block size is given with every result. Quantities with one value per
direction are resampled over the ten region pairs. This is the **primary resampling unit** for
direction-level intervals; other units are given in Section S1.23. Quantities with one value per
scar or target region get a Student *t* interval. The effective sample is therefore ten pairs or five
regions for direction-level intervals, and at most seven scars from three regions for scar-level
intervals.

## 3.8 Cross-region transfer protocol

For each ordered pair of regions, the model was fitted on the source region and applied to the
target region. **No target label was used**: there was no refitting, threshold selection or
calibration on the target. Both feature sets were transferred, so the gain from the thermal block is
a paired difference within each direction. All twenty ordered directions were computed.

## 3.9 Label-blind domain adaptation

Two label-free methods were tested on every direction and in both feature sets. **Region-wise
z-score** standardises the numeric features of each region with its own statistics. **CORAL after
region-wise z-score** then aligns the source covariance with the target covariance [@Sun2016], with
λ = 10⁻⁵. Only target feature statistics, never target labels, are used. The value of λ was not
chosen by performance; its effect is reported in Section S1.2. Details are in Section S3.8.

## 3.10 Transfer-gap decomposition and the concept-shift criterion

For a direction into a target, let $`A_{\mathrm{w}}`$ be the within-region thermal AUC of the target,
$`A_{\mathrm{raw}}`$ the raw transfer AUC and $`A_{\mathrm{ad}}`$ the transfer AUC after adaptation
method $`m`$, all on the same target cells. The gap is split as

```math {#eq:decomp}
G = A_{\mathrm{w}} - A_{\mathrm{raw}}, \qquad R_m = A_{\mathrm{ad}} - A_{\mathrm{raw}}, \qquad U_m = A_{\mathrm{w}} - A_{\mathrm{ad}}, \qquad f_m = R_m / G,
```

so that $`R_m + U_m = G`$. The recovered fraction $`f_m`$ is signed and is not clipped. When
adaptation lowers AUC, the recovery is negative and is reported as negative. Intervals come from the
paired bootstrap of Section 3.7 (Section S3.7).

The direction of each predictor was measured with a **signed univariate association**: the ROC-AUC
of each numeric predictor against `burned`, computed in each region and never folded to
max(AUC, 1 − AUC). A value below 0.5 shows a direction, not weakness. A reversal between two regions
is called supported only when the two values are on opposite sides of 0.5 **and** each region's own
interval excludes 0.5. This is a per-comparison criterion. A Holm correction over each family of
feature-by-pair comparisons is also reported (Section S1.20).

## 3.11 Interventions

**Pooled training.** In leave-one-region-out training, a model was trained on the other four regions
together and tested on the held-out region. It was compared with the mean of the four single-source
models, because choosing the best single source would require target labels.

**Removal of reversing features.** The two predictors whose reversal was supported under the
original label, `elevation_mean` and `lst_anomaly_mean`, were removed, and all models were refitted.
Each was also removed alone. The selection was not repeated under the corrected label (Table S10).
Because the two features were chosen from the same data, both results are post-selection estimates.

## 3.12 Evaluation frames and controls on the transfer path

Let $`V_R`$ be the primary population of region $`R`$ and $`P_R \subset V_R`$ its burned cells. The
**region-wide frame** is $`V_R`$, the rectangle as drawn.

**Scar frames.** A scar is an 8-connected group $`K`$ of at least 50 burned cells. Its **scar and
2 km collar** is

```math {#eq:scar}
H_K = \Big\{ i \in V_R : \min_{j \in K} \big( |r_i - r_j| + |c_i - c_j| \big) \le m \Big\},
```

with $`m = 4`$ grid steps. All its unburned cells are next to the fire. Four evaluations use it
(Table 2). A scores the out-of-fold predictions of 5-fold blocked cross-validation ($`k = 10`$) on
$`V_R`$, and B scores the same predictions on $`H_K`$. B is therefore the same model scored on a
different set of cells. C is **leave-one-scar-out**: a model fitted on $`V_R \setminus H_K`$ is
scored on $`H_K`$. D averages over the four other regions a model fitted on that region and scored on
$`H_K`$. Three controls reuse the predictions of A: a prevalence-matched sample, a negative-pool swap
and a positive-pool swap (Section S1.9.3).

**Distance collars.** The distance to the nearest burned cell and the collar of radius $`r`$ (5 or
10 km) are

```math {#eq:collar}
d_i = 0.45 \min_{j \in P_R} \big\lVert (r_i, c_i) - (r_j, c_j) \big\rVert_2, \qquad F_R(r) = \{ i \in V_R : d_i \le r \}.
```

The 0.45 km step is a single value for both axes, so collar radii are nominal to within about 15 %.
Every burned cell has $`d_i = 0`$ and is kept; only distant unburned cells are removed. In transfer
the model is fitted on $`F_s(r_s)`$ and scored on $`F_t(r_t)`$.

**Every collar frame is defined from burned cells.** It is used to show how the evaluation area
changes the metric. It cannot be drawn before a fire.

## 3.13 Leakage control and reproducibility

A list of forbidden columns is checked at every model fit: coordinates, all burn-date and
label-provenance columns, and the agreement fraction. The vegetation mask defines the population and
is never used as a predictor. All randomness uses seed 42. The random-forest seed is fixed, so
direction-level intervals are conditional on one fitted source model. Across five bootstrap seeds,
every transfer verdict at 1 km blocking is stable; at 5 km, three verdicts change (Section S1.21).

The reproduction check refitted every within-region model and all twenty CORAL transfers against
the frozen pipeline outputs. The within-region results agree exactly and the transfers to within
1.3×10⁻⁸ (Section S3.6.2). Point estimates depend on the scikit-learn version. Under version 1.5.2
instead of 1.9.0, single-direction AUCs moved by up to 0.047 and one support count changed
(`paper/labelfix_rerun/round7/sklearn152/`). Exact reproduction therefore needs the archived
environment. The label correction and the re-run were done by the corresponding author; they were
not repeated independently by the author of the pipeline. Where a result depends on a design choice,
the dependence is reported (Sections S1 and S3.6). Analyses added after the main results are
listed in Section S1.23.

**Use of AI tools.** Claude (Anthropic; Opus-family models, July to September 2026) was used to
write and run analysis, verification and figure code, including the label correction and re-run. It
was also used to check reported numbers, to run simulated reviews, and to draft and edit text. Every
input is identified by SHA-256, and reported numbers are checked against tracked outputs by
`paper/figures/check_all.py`. The corresponding author reviewed the code, outputs and text.

## 3.14 Same-geography event-to-event comparison (Muğla 2021 versus 2022)

A second fire burned inside the same Muğla study area eleven months after the first. The signed
associations of both fires were computed with the same bootstrap. Season, year and population all
differ between the two arms, because the 2022 arm is defined by removing the 2021 scar (Sections
S1.13 and S3.3).
