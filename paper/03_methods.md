# 3. Data and methods

This section first defines the terms used throughout. A **study area** is the rectangle drawn
around one fire. An **evaluation frame** is the set of cells on which a score is computed. The
**scar frame** is a burned area together with a 2 km collar of unburned cells around it, and a
**distance collar** keeps all cells within 5 or 10 km of any burned cell. A result is called
**supported** when its 95 % interval excludes the null value (0.5 for an AUC, 0 for a difference).
**Label-free** methods use target features but never target labels.

The analyses fall into two groups. The within-region comparison, the transfer matrix, the two
adaptation methods, the gap decomposition and the reversal test follow the fixed protocols of the
processing pipeline. The twenty similarity measures were recorded on 8 August 2026, before the label
correction of Section 3.2. By contrast, the frame test (Section 3.12), the distance collars, the equivalence tests, the additional resampling units and the analyses listed in Tables S21 and S35
(Sections S1.22 and S1.23) were added after the first results. These are exploratory, and they are reported as such.

## 3.1 Study regions and temporal windows

Five Mediterranean wildfire regions were analysed (Fig. 1): Manavgat 2021 and Muğla 2021 in Türkiye,
Bejís 2022 in Spain, North Evia 2021 in Greece and Montiferru 2021 in Sardinia. Each region
contributes one fire season, and each season was dominated by one large fire; in Muğla, however,
several separate burned areas occurred in the same weeks. The events were not sampled from a defined
population of fires, so the results describe large single-season events. Each study area is a
rectangle in EPSG:4326 around the fire. It was not clipped to the fire perimeter, so the unburned
cells around each fire form the negative class.

The rectangles were not all fixed before any outcome was seen. Only the Montiferru rectangle follows
a stated rule, and the North Evia rectangle was extended after the first one showed a very high
burned fraction (Section S3.3, Table S19). The first Evia rectangle is kept as a sensitivity analysis
(Section S1.1). A sixth region, Kozan 2023, served as a negative control and was excluded by the gate
of Section 3.3.

Each region has two windows that do not overlap. The **predictor window** ends the day before the
**label window** starts, so no predictor observation is later than the first labelled burning.
Predictor windows are 57 to 61 days long and label windows 35 to 59 days. Four earlier years of
composites from the same calendar window serve as the baseline for the anomaly channels. The
processing chain is shown in Fig. 2.

## 3.2 Burned-area label and the ~500 m analysis grid

Labels were taken from the MODIS MCD64A1 burned-area product, Collection 6.1 [@MCD64A1;
@Giglio2018], through Google Earth Engine [@Gorelick2017]. Its errors [@Boschetti2019] limit every model in this study. As a check, the within-region and transfer analyses
were repeated with the VIIRS VNP64A1 product [@VNP64A1] (Section S1.23). The MCD64A1 monthly burn-date
layer was sampled onto the 30 m reference grid of the processing pipeline by
nearest neighbour, so each ~500 m observation is repeated over the 30 m pixels below it. The
analysis grid is built from this grid in blocks of 17 × 17 pixels. A cell is therefore about 510 m from north to south and 390 to
407 m from east to west, with an area of 0.199 to 0.208 km² (a MODIS cell is 0.215 km²). A cell is
labelled burned when any of its pixels has a burn date in the label window. Because of this rule, a
scar can grow by up to one cell at its edge. Water cells are removed by the population filter of
Section 3.5.

**Earlier burning.** Cells that burned in the predictor window were removed in Muğla (49 cells),
North Evia (16) and Montiferru (61). Manavgat had no burning in that window. In Bejís this removal
was not applied, so 48 cells that burned before the label window were kept. Burning in the five
previous years was not screened in any region. When those cells were excluded, the mean transfer
gain fell from +0.007 to +0.003, while the within-region gain stayed positive in all regions
(Section S3.1.1).

**Corrected Manavgat label.** The label first used for Manavgat missed the first four days of the
fire, 28 to 31 July. The corrected label only adds burned cells, and it raises the number of burned
cells in the primary population from 784 to 2,935. In this paper, "original label" means the label
before this correction. The correction and its control run are described in Section S3.1.2.

## 3.3 Burned-landcover admissibility gate

Before modelling, each region had to pass a gate. The gate asks what fraction of the burned cells is
covered mainly by natural vegetation, using ESA WorldCover classes [@Zanaga2022]. A region is
admitted if this fraction is at least 0.50 and at least 30 cells burned. Conversely, it is rejected
as a cropland control if the cropland fraction is at least 0.50 (Section S3.1).

## 3.4 Predictor variables

Ten predictors were used (Table S20). The **baseline** set contains elevation and slope from the
Copernicus DEM GLO-30 [@CopernicusDEM], dominant land cover from ESA WorldCover v200 [@Zanaga2022],
and the median NDVI of the predictor window from Landsat 8 Collection 2 Level-2 [@LandsatC2L2].
These change little over one fire season. The **thermal** set adds six channels derived from Landsat
8 surface temperature, screened for quality and composited as the median of the predictor window.
The six channels are current LST, its anomaly against the four baseline years, the TVDI
[@Sandholt2002], its difference from the baseline years, a downscaled LST and a fused LST. The last two use MODIS MOD11A1 v061 daytime LST (Terra, about 10:30 local time) [@MOD11A1] and a
random-forest downscaling model to fill gaps in Landsat (0.11 % to 9.70 % of pixels,
depending on the region). Because TVDI edges are fitted inside each study area and window, a TVDI value does not mean the
same moisture state in two regions (Section S3.4). The median pixel had three to six clear Landsat
observations in the predictor window, and one to seven in each baseline year (Table S36). Landsat 9
was not used.

**The six thermal channels carry about two signals.** Current, fused and downscaled LST are
correlated at 0.97 to 1.00 in every region. Current LST and TVDI are correlated at 0.88 to 0.98, and
the two anomaly channels at 0.71 to 0.94. As a result, two principal components explain 92 % to 98 %
of their variance (Section S3.4), and counts over the nine numeric predictors are read with care.

**Land cover.** WorldCover v200 is built from 2021 images, which is after the fire for the four
2021 events. All analyses were therefore repeated with the 2020 map (WorldCover v100 [@Zanaga2021]), aggregated
to the same cells. The 2020 map changed the population by at most 43 burned cells in four regions. In
Montiferru, however, it added 142 burned cells that the 2021 map did not class as natural
vegetation. The within-region gains and the transfer results did not change in any conclusion
(Section S1.23).

## 3.5 Cell aggregation, validity and analysis populations

Cell values are means over the valid 30 m pixels of the cell. A cell is valid for modelling when
NDVI, elevation and slope are available for at least 30 % of the cell and at least one land-cover
pixel is valid. Thermal completeness is not required. The **primary** population contains the valid
cells in which tree, shrub and grass cover together reach 0.50, so cropland and water are excluded.
In this population, 0.1 % to 6.5 % of cells have at least one missing thermal value, depending on
the region. These values are filled inside the model pipeline (Section 3.6), and missingness is not related to burning (AUC 0.49 to 0.51 in every region; Table S35). A **secondary** population of all valid cells
is used only as a within-region sensitivity analysis in two regions (Section S1.17).

## 3.6 Classifier

The thermal set contains the baseline set (Section 3.4). Land cover is one-hot encoded. Missing
numeric values are replaced by the median and missing land cover by the most frequent class. These
values are fitted inside each training fold, and on the source region only in transfer, so no test
data are used in fitting. The adapted models of Section 3.9 are the only exception. The classifier is
a random forest [@Breiman2001] with 300 trees, unlimited depth, `min_samples_leaf = 3`, balanced class
weights and `random_state = 42`. These settings were fixed in advance, were not tuned, and are the
same in every analysis.

## 3.7 Spatial-block cross-validation and bootstrap uncertainty

Cross-validation is spatially blocked. Cell $`i`$ at grid position $`(r_i, c_i)`$ is assigned to the
block

```math {#eq:block}
b_k(i) = \left( \lfloor r_i / k \rfloor,\; \lfloor c_i / k \rfloor \right).
```

Five folds are drawn over whole blocks, stratified by label, so a block is never split between
training and test. Block sizes of $`k`$ = 2, 10 and 20 cells are reported; they are written as
1 km, 5 km and 10 km blocking in the text.

Every score is a ROC-AUC on a named set of cells $`F`$, its evaluation frame. With $`F^{+}`$ the
burned and $`F^{-}`$ the unburned cells of $`F`$, and $`s_i`$ the predicted score,

```math {#eq:auc}
\mathrm{AUC}(s; F) = \frac{1}{|F^{+}|\,|F^{-}|} \sum_{i \in F^{+}} \sum_{j \in F^{-}} \left[ \mathbf{1}(s_i > s_j) + \tfrac{1}{2}\,\mathbf{1}(s_i = s_j) \right].
```

This is the probability that a burned cell in $`F`$ is ranked above an unburned one. The metric can
therefore change when the frame changes, even when no score changes (Section 3.12). Precision-recall AUC is also reported, because it reflects how a susceptibility map is used when
burned cells are rare [@Sofaer2019]. The out-of-fold residuals stay spatially correlated beyond 5 km. Their correlation falls below 0.05
at 10 to 20 km in Manavgat, Bejís and Muğla, at 5 to 10 km in Montiferru, and only at 20 to 40 km in
North Evia (Section S1.23). Intervals at 5 km blocking may therefore be too narrow, especially in
North Evia, where even 10 km blocks do not remove the dependence; the 10 km results are given as a
check.

Uncertainty is estimated with a spatial-block bootstrap. Blocks are resampled with replacement, 1000
times, with seed 42, and the 2.5 and 97.5 percentiles give the interval. Differences are paired
within each replicate, and the block size is given with every result. Quantities with one value per
transfer direction are resampled over the ten region pairs; this pair-cluster bootstrap is the
**primary resampling unit** for direction-level intervals, and five further units are compared in
Section S1.22. Quantities with one value per scar or per target region get a Student *t* interval.
The effective sample is therefore ten pairs or five regions for direction-level intervals, and at
most seven scars from three regions for scar-level intervals. Because scars are nested in regions,
the region-level estimates are the primary ones for the frame test.

## 3.8 Cross-region transfer protocol

For each ordered pair of regions, the model was fitted on the source region and applied to the
target region. **No target label was used**: there was no refitting, threshold selection or
calibration on the target. Both feature sets were transferred, so the gain from the thermal block is
a paired difference within each direction. All twenty ordered directions were computed.

## 3.9 Label-free domain adaptation

Two label-free methods were tested on every direction and in both feature sets. **Region-wise
z-score** standardises the numeric features of each region with its own statistics. **CORAL after
region-wise z-score** then aligns the source covariance with the target covariance [@Sun2016], with
λ = 10⁻⁵. Both methods use target feature statistics, which are available before a fire, but never
target labels. The value of λ was not chosen by performance; its effect is reported in Sections S1.2 and S1.23.
Details are given in Section S3.8.

## 3.10 Transfer-gap decomposition and the reversal criterion

For a direction into a target, let $`A_{\mathrm{w}}`$ be the within-region thermal AUC of the target,
$`A_{\mathrm{raw}}`$ the raw transfer AUC and $`A_{\mathrm{ad}}`$ the transfer AUC after adaptation
method $`m`$, all on the same target cells. The gap is split as

```math {#eq:decomp}
G = A_{\mathrm{w}} - A_{\mathrm{raw}}, \qquad R_m = A_{\mathrm{ad}} - A_{\mathrm{raw}}, \qquad U_m = A_{\mathrm{w}} - A_{\mathrm{ad}}, \qquad f_m = R_m / G,
```

so that $`R_m + U_m = G`$. The recovered fraction $`f_m`$ is signed and is not clipped, so when
adaptation lowers AUC, the recovery is negative and is reported as negative. Intervals come from the
paired bootstrap of Section 3.7 (Section S3.7).

The direction of each predictor was measured with a **signed univariate association**: the ROC-AUC
of each numeric predictor against `burned`, computed in each region and never folded to
max(AUC, 1 − AUC). A value below 0.5 therefore shows a direction, not weakness. A reversal between
two regions is called supported only when the two values are on opposite sides of 0.5 **and** each
region's own interval excludes 0.5. This is a per-comparison criterion, and a Holm correction over
each family of feature-by-pair comparisons is also reported (Section S1.19). A marginal reversal can
also arise when the predictors are distributed differently in two regions, so it is not a direct
test of a change in the predictor-burning relationship.

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

**Scar frames.** A scar is an 8-connected group $`K`$ of at least 50 burned cells. Its **scar
frame** is

```math {#eq:scar}
H_K = \Big\{ i \in V_R : \min_{j \in K} \big( |r_i - r_j| + |c_i - c_j| \big) \le m \Big\},
```

with $`m = 4`$ grid steps. On this grid the collar is therefore about 1.6 to 2.0 km wide along the
axes and about 1.3 km along the diagonals, and all its unburned cells are next to the fire. Four
evaluations use it (Table 2). A scores the out-of-fold predictions of 5-fold blocked cross-validation
($`k = 10`$) on $`V_R`$, and B scores the same predictions on $`H_K`$, so B is the same model scored
on a different set of cells. C is **leave-one-scar-out**: a model fitted on $`V_R \setminus H_K`$ is
scored on $`H_K`$. D averages, over the four other regions, a model fitted on that region and scored
on $`H_K`$. Three controls reuse the predictions of A: a prevalence-matched sample, a negative-pool
swap and a positive-pool swap (Section S1.9.3).

**The two frames answer different questions.** The region-wide frame asks where in a landscape a
fire burned, which is the question behind prevention planning. The scar frame asks which cells next
to the fire burned. This second question is harder: spread, wind and suppression matter more there,
and label errors of the burned-area product are concentrated at scar edges. Two controls address the
edge errors: excluding up to two cells at the scar edge, and a placebo collar of the same shape
placed away from any burned cell (Table S21).

**Distance collars.** The distance to the nearest burned cell and the collar of radius $`r`$ (5 or
10 km) are

```math {#eq:collar}
d_i = 0.45 \min_{j \in P_R} \big\lVert (r_i, c_i) - (r_j, c_j) \big\rVert_2, \qquad F_R(r) = \{ i \in V_R : d_i \le r \}.
```

The 0.45 km step is a single value for both axes, so collar radii are nominal to within about 15 %.
Every burned cell has $`d_i = 0`$ and is kept; only distant unburned cells are removed. In transfer
the model is fitted on $`F_s(r_s)`$ and scored on $`F_t(r_t)`$.

The study areas, burned cells and collars are mapped in Fig. S1.

**Every scar frame and distance collar is defined from burned cells.** These frames therefore show
how the evaluation area changes the metric, but they cannot be drawn before a fire.

## 3.13 Leakage control and reproducibility

A list of forbidden columns is checked at every model fit: coordinates, all burn-date and
label-provenance columns, and the agreement fraction. The vegetation mask defines the population and
is never used as a predictor. All randomness uses seed 42. Because the random-forest seed is fixed,
direction-level intervals are conditional on one fitted source model. Refitting with ten seeds changed mean transfer by at most 0.003, but single directions by up to
0.049 (seed-to-seed standard deviation at most 0.015; Section S1.23). This variation is not part of
the direction-level intervals. Across five bootstrap seeds,
every transfer verdict at 1 km blocking is stable, whereas at 5 km three verdicts change (Section
S1.20).

The reproduction check refitted every within-region model and all twenty CORAL transfers against
the frozen pipeline outputs. The within-region results agree exactly and the transfers to within
1.3×10⁻⁸ (Section S3.6.2). Point estimates depend on the scikit-learn version: under version 1.5.2
instead of 1.9.0, single-direction AUCs moved by up to 0.047 and one support count changed (Section
S3.5(vi)). Exact reproduction therefore needs the archived environment. The label correction and the
re-run were done by the corresponding author and were not repeated independently by the author of
the pipeline. The source file of every reported number is named in the Supplementary Material.

**Use of AI tools.** Claude (Anthropic; Opus-family models, July to September 2026) was used to
write and run analysis, verification and figure code, including the label correction and re-run. It
was also used to check reported numbers, to draft and edit text, and to produce simulated referee
reports on drafts, which the authors used as an internal check. Every input is identified by
SHA-256, and reported numbers are checked automatically against tracked outputs. The corresponding
author reviewed the code, outputs and text.

## 3.14 Same-geography event-to-event comparison (Muğla 2021 versus 2022)

A second fire burned inside the same Muğla study area eleven months after the first. The signed
associations of both fires were computed with the same bootstrap. However, season, year and
population all differ between the two fires, because the 2022 population is defined by removing the
2021 scar (Sections S1.13 and S3.3).
