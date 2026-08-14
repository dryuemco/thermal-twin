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

Twenty candidate diagnostics from four families are each rank-correlated against the same target
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
positive lies outside the source training population. Section 4.8 states what follows for how these
two numbers may be read.
