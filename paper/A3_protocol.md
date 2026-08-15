# Appendix C. Protocol detail

These protocols are given here in full rather than in Methods, because each is a specification a
reader needs only when checking the corresponding result, and none is needed to follow the
argument. Sections 3.2, 3.3, 3.11 and 3.15 state in summary what each does.

## C.1 Burned-area label, the reconstructed analysis grid, and the admissibility gate

Labels come from MODIS MCD64A1 Collection 6.1 (`MODIS/061/MCD64A1`) retrieved through Google Earth
Engine [@Gorelick2017], whose omission and commission characteristics [@Boschetti2019] bound every
model here. The product is exported onto the 30 m EPSG:4326 reference grid used by the rest of the
pipeline, which duplicates each native ~500 m observation across the 30 m pixels beneath it.

The analysis grid is therefore **reconstructed rather than native**: the 30 m grid is partitioned
into non-overlapping blocks of `round(500 / 30) = 17 × 17` pixels, giving a nominal cell edge of
510 m, and each cell is identified by its integer block indices `row_500m` and `col_500m`. This
approximates the MODIS sinusoidal cell rather than reproducing it, being anchored to the
Landsat/EPSG:4326 reference grid, and marginal blocks are truncated. The cell is square in degrees
but not on the ground, about 510 m north to south and 390 to 407 m east to west, so its area is
0.199 to 0.208 km² against a MODIS cell's 0.250 km²; every block-size label in this paper is
therefore the north-south dimension. The companion paper develops what follows from that.

A cell's representative burn date is the **mode** of the positive sub-pixel day-of-year values in
the block, tested against the region's label window. Because the exported raster carries no
out-of-window positives, in this dataset a single in-window positive sub-pixel makes the cell burned.
The fraction of positive sub-pixels agreeing with the modal date is recorded as
`burn_date_pixel_agreement_fraction` but no agreement threshold is imposed. The label never affects a
cell's eligibility for modelling: unburned, all-no-data and out-of-window cells all remain as the
negative class.

Two safeguards are recorded rather than assumed. Cells that burned inside a region's own predictor
window are removed from its analysis universe rather than counted as unburned, which ran for Muğla,
Evia and Montiferru, is recorded as not run for Manavgat and has no recorded status for Bejís.
Burning in earlier years is screened for no region in the five-region cohort; the only historical
exclusion in the study removes the 2021 Muğla scar from the 2022 event-relative experiment of
Section 3.15.

Before any modelling each region passes a gate that answers one question: of the cells labelled
burned, what fraction is dominated by natural vegetation? A region is admitted as a wildfire
candidate when that fraction reaches 0.50 and at least 30 burned cells are present, and is rejected
as a cropland-dominated control when the cropland fraction reaches 0.50 instead. The gate uses ESA
WorldCover classes aggregated to the same reconstructed cells. Its purpose is to separate burned area
produced by natural-fuel combustion from burned area produced by post-harvest stubble burning, which
MCD64A1 does not distinguish. Verdicts are reported in Section 4.1.

## C.2 Transferability diagnostics versus transfer

Twenty candidate diagnostics from five families are each rank-correlated against the same target
quantity, the raw thermal transfer AUC over the twenty ordered directions, under one common
pair-based bootstrap. The families are marginal predictor-distribution measures P(x), burned-niche
overlap P(x|y=1), fire-regime label-pattern structure P(y), and conditional feature-response
direction P(y|x).

The **marginal** family includes area-of-applicability-style dissimilarity in scaled,
importance-weighted predictor space [@Meyer2021; @Meyer2022; @Ludwig2023], climatic and geographic
distance, and a learned domain classifier trained to separate source from target cells. The
**niche-overlap** family includes Schoener's D [@Schoener1968] and Warren's I [@Warren2008] over the burned cells of each region.
The **regime** family includes burned-patch component counts and effective component counts. The
**conditional** family is the sign-agreement index: the fraction of predictors whose signed
univariate association points the same way in both regions, computed over all predictors and over
the subset whose associations are individually interval-supported.

Two properties of this design are stated in advance because they bound what it can show. The
candidate set was fixed in a project analysis log before the correlations were computed; that log is
not a formal pre-registration and no independent timestamped registration exists. And with five
regions the effective sample is ten unordered pairs, so nineteen computed variants are evaluated at
that power with no family-wise error control claimed; where a diagnostic clears an interval test but
not a Bonferroni threshold, both are reported.

## C.3 Same-geography event-to-event comparison (Muğla 2021 versus 2022)

Muğla is the one region for which a second fire event is analysed on the identical AOI and analysis
grid, which allows the direction of feature-label associations to be compared with geography held
fixed. The 2022 experiment is registered with windows anchored to its own event: a 58-day predictor
window closing the day before ignition and a 49-day label window opening on it, matching the 2021
durations exactly.

**This is not a clean temporal-transfer design and is not presented as one.** The 2022 event ignites
about six weeks earlier in the season than the 2021 event, so calendar year and seasonal phase are
confounded and no difference can be attributed to the year alone. The registered claim is
same-geography event-to-event. The pair is deliberately kept out of the twenty-direction matrix, and
that exclusion is enforced in released code rather than merely asserted here.

Two further properties bound the comparison. A historical-burn exclusion applies to the 2022 arm
alone, masking every cell that burned in 2021 so the previous year's scar does not enter the
following year's analysis: it removes 3,073 cells, of which 2,941 belong to the primary population,
taking it from 41,730 rows to 38,790, a drop of 7.0 %. The two arms therefore share 38,789 of 38,790
cells and three byte-identical static predictors, and in the 2022-to-2021 direction every target
positive lies outside the source training population. Appendix A(m) states what follows for how these
two numbers may be read.

**Table C1. Study regions, areas of interest and temporal windows.** Bounding boxes are in EPSG:4326,
as registered. Window lengths in brackets are inclusive day counts. The baseline years are the four
window-symmetric years preceding each predictor window.

| Region | Bounding box (lon min, lat min, lon max, lat max) | Predictor window | Label window | Baseline years |
|---|---|---|---|---|
| Manavgat 2021 (Türkiye) | 31.05, 36.72, 31.85, 37.35 | 2021-06-01 to 2021-07-27 (57 d) | 2021-07-28 to 2021-08-31 (35 d) | 2017, 2018, 2019, 2020 |
| Bejís 2022 (Spain) | -1.05, 39.68, -0.35, 40.15 | 2022-06-15 to 2022-08-14 (61 d) | 2022-08-15 to 2022-09-30 (47 d) | 2018, 2019, 2020, 2021 |
| Muğla 2021 (Türkiye) | 27.1, 36.6, 28.9, 37.45 | 2021-06-01 to 2021-07-28 (58 d) | 2021-07-29 to 2021-09-15 (49 d) | 2017, 2018, 2019, 2020 |
| North Evia 2021 (Greece) | 23.05, 38.55, 23.85, 39.15 | 2021-06-05 to 2021-08-02 (59 d) | 2021-08-03 to 2021-09-30 (59 d) | 2017, 2018, 2019, 2020 |
| Montiferru 2021 (Italy) | 8.45, 40.05, 8.75, 40.27 | 2021-05-25 to 2021-07-23 (60 d) | 2021-07-24 to 2021-08-31 (39 d) | 2017, 2018, 2019, 2020 |

## C.4 Predictor provenance, compositing and the downscaler

Ten predictors are used, four baseline and six thermal, all summarised per cell over the predictor
window, through the chain shown in Fig. 2. All optical and thermal predictors come from Landsat 8 Collection 2 Level-2
(`LANDSAT/LC08/C02/T1_L2`), quality-screened per pixel from the `QA_PIXEL` band with the water bit
deliberately preserved; the coarse-resolution thermal input is `MODIS/061/MOD11A1`.

- **NDVI**, the predictor-window median of Landsat surface reflectance, is the baseline's one
  time-varying member.
- **Elevation** and **slope** come from the Copernicus DEM GLO-30.
- **Land cover** is ESA WorldCover v200 [@Zanaga2022], entering as the dominant class code.
- **Current LST**, the predictor-window median of Landsat surface temperature in °C.
- **LST anomaly**, a z-score of the current-window LST median against the four baseline years,
  set to no-data where the baseline standard deviation is below 1.0 °C or observations are too few.
- **TVDI** and **TVDI difference**. The Temperature-Vegetation Dryness Index [@Sandholt2002] is
  computed in the LST-NDVI feature space, with wet and dry edges taken as the 2nd and 98th LST
  percentiles within each of twenty NDVI bins and the index clamped to [0, 1]. The edges are
  percentiles of the LST values a given scene contains, so they are fitted per AOI and per window,
  and a TVDI of 0.5 denotes a different physical moisture state in each region. The companion paper
  reports what that scene dependence does and does not explain. **TVDI difference** is the raw
  anomaly of that index against the same four window-symmetric baseline years used for the LST
  anomaly: `tvdi_difference = current_tvdi − mean(baseline_tvdi)`, in index units rather than
  standard deviations, which is why it is reported alongside the z-scored channel rather than in
  place of it.
- **Downscaled LST** and **fused LST**. A MODIS-to-Landsat downscaling model is trained on the
  predictor window and applied to the full 30 m grid. The fused product equals observed Landsat LST
  wherever that is valid, and the downscaled surface only where it is not. Gap-filling therefore
  never replaces or blends a valid observation. The gap-filled share is 0.11 % to 9.70 % by region. The
  downscaler's own inputs include coordinates, which is the one route by which a coordinate-derived
  surface re-enters a feature set from which Section 3.14 excludes coordinates. Appendix A(g)
  reports the increment without these two channels.

## C.5 Limitations, in full

Section 5.8 states the four that bind the conclusions; all eleven are here.

(i) **No meteorological covariates** enter the models, so we cannot say how local skill and
portability behave for a mixed thermal-plus-weather predictor set.

(ii) **The same-geography comparison covers one region only**, and even there year and seasonal phase
are confounded. That confound cannot be resolved in this study area, and the reason is specific: the
two events sit 42 days apart in median burn day-of-year, neither year contains a second event at the
other's phase, and a calendar-matched arm would carry nine burned cells against this design's gate
minimum of thirty. The positive-block count for the 2022 arm is separately below the floor this
design sets itself, at eleven against sixteen (Appendix A(m)). Its 331 burned cells also leave the thermal reversals unresolved at interval level, and
the pair holds place fixed but not population. Those two arms are additionally the only transfer
directions here computed by us rather than read from the pipeline author's frozen export, with his
unmodified code and the same pinned environment.

(iii) **All labels derive from a single burned-area product**, MCD64A1 [@Giglio2018], whose omission
and commission characteristics [@Boschetti2019] bound every model evaluated here. No second
burned-area product covers 2021 and 2022 at this resolution; the companion paper reports what an
independent active-fire observation says about the omission concern.

(iv) **Evia remains the most imbalance-atypical population** even after the AOI extension, at a TSG
prevalence of 0.287 against 0.038 to 0.072 in three of the others.

(v) **Each region contributes one fire season**, so regional concept shift is confounded with event
meteorology, and distinguishing them requires multi-year labels.

(vi) **Cross-region point estimates carry an implementation tolerance** of roughly ±0.02 to 0.03
across scikit-learn versions. All reported numbers are fixed to one verified version, but exact
reproduction elsewhere requires the archived environment.

(vii) **The diagnostic correlations rest on an effective sample of ten region pairs.** Both the
successes and the failures of Section 4.6 should be read at that power.

(viii) **Manavgat's atypical transfer behaviour remains unexplained.** It is where the conditional
diagnosis bites hardest and where feature removal recovers most. Three candidates have now been tested and none survives: its meteorology, which was not extreme;
the quality screening of its coarse thermal input, which propagates widely but moves no signed
association by more than +0.0003 (Appendix A(v), Appendix A(e)); and the evaluation frame, which
explains its elevation figure but not its transfer behaviour (Section 4.4). With one fire season per
region the remaining candidates are not separable in this design.

(ix) **The interval-support counts are less stable than the point estimates behind them.** Several
verdicts sit within a thousandth of their reference value, and at 1 km blocking the published split
of ten positive, seven negative and three uncertain turns on a lower bound of −0.00045. The point
estimates and the sign pattern are stable; the counts are not. Every sentence in this paper that
leans on an exact count of supported directions should be read at that precision.
(x) **The five areas of interest are not comparable frames, and this cohort cannot fully repair it**
(Section 4.4). We report the equalised arm alongside the frame-as-drawn arm rather than replacing one
with the other, because the collar radius is itself a choice and 5 km and 10 km do not agree exactly
(0.608 against 0.617). The deeper limitation is that the frames were fixed upstream of this work, in
`repo/`, so we can restrict them but not extend them; a region whose rectangle is already fire-scale,
Montiferru, cannot be given a far field for symmetry. Any future cohort should fix the frame by an
explicit accessible-area rule [@Barve2011] before any predictor is computed, and we treat that as the
main design lesson of this paper.

(xi) **One classifier family.** The headline numbers use a random forest with unlimited depth, the
configuration most able to encode local structure and least able to extrapolate. Appendix A(h) shows the transfer result is not an artefact of that
choice: three further estimators, including a penalised linear one, all land between 0.510 and 0.556
and all place fourteen of twenty directions above chance. Those are point estimates without
intervals, so the ordering among them is not claimed as a result. Other model families were not
tried, and a different inductive bias might behave differently, but within this family the negative
result is a property of the predictors rather than of an unregularised estimator.

## C.6 Leakage control and reproducibility, in full

An explicit forbidden-column set is enforced at every model fit. Coordinates (`lon`, `lat`, `row`,
`col` and their normalised forms), every burn-date and label-provenance column, and the agreement
fraction are excluded from all feature sets, and the enforcement runs as an assertion rather than a
convention. The natural-vegetation mask is used only to define the population, never as a predictor.
Spatial blocking prevents a cell from sharing a fold with its own neighbours.

**Reproducibility.** All randomness uses seed 42 and the bootstrap uses 1000 replicates throughout.
The transfer and adaptation analysis runs in an environment separate from the upstream pipeline's.
Every within-region model was therefore refitted there and compared against the frozen upstream
output, and the independently implemented adaptation was compared against the pipeline's own. The
within-region comparisons agree exactly and the twenty transfer directions to within
1.6×10⁻⁷. All numbers here were produced under scikit-learn 1.9.0 or verified against it; the
implementation tolerance that applies if the version is not fixed is stated in Appendix C.5(vi), and
the companion paper reports the version sensitivity and the reproduction check in full.

**Sensitivity analyses.** Every headline result is repeated across two analysis populations, three
spatial-block sizes, the CORAL sweep, both feature sets and four classifier capacities; where a
conclusion depends on one of those choices the dependence is reported rather than resolved by
choosing the favourable setting (Appendix A).

## C.7 Transfer-gap decomposition and the concept-shift diagnostic, in full

For each direction the gap between the target's own within-region skill and the raw transfer result
is split in two. One part is what the best label-free adaptation recovers, and the other is what it
does not. The recovered fraction is (adapted − raw) / (within − raw), signed and unclipped, with its interval
from the same paired bootstrap; it bounds what covariate-level correction can achieve. Section 4.3
shows the remainder should not be read as a conditional residual, because much of it is incurred
inside a single region (Appendix A(j)).

The mechanism is diagnosed by **signed univariate association**. For each numeric predictor the raw
ROC-AUC of that predictor against `burned` is computed in each region and never folded to
max(AUC, 1 − AUC), so a value below 0.5 is read as a direction rather than as weakness. A reversal is
called bootstrap-supported only when the two regions' point estimates fall on opposite sides of 0.5
**and each region's own interval excludes 0.5**, under the same 10-cell spatial-block bootstrap.
That is stricter than requiring the two regions' intervals to be disjoint: a feature whose intervals
are disjoint but one of which straddles 0.5 has not been shown to point anywhere in that region, so
it is recorded as a point reversal only. Appendix B states the rule again beside the counts, and
`conditional_similarity_transfer.json` carries it as machine-readable metadata.
