# 3. Data and methods

> **Rewritten 2026-08-14 in the split.** This section was 15,407 words. It is now written to let a
> reader replicate the four contributions of Section 1.4 and to carry every number Section 4 cites, and
> nothing else. The observational layer beneath it, meaning predictor provenance, compositing,
> quality screening, index normalisation, label omission and the version and reproduction audits, is
> the subject of the companion paper and is summarised here only where a Paper 1 claim depends on it.
> The released repository remains the authoritative source for file and line references.

## 3.1 Study regions and temporal windows

Five Mediterranean wildfire regions are analysed (Fig. 1): Manavgat 2021 and Muğla 2021 in Türkiye,
Bejís 2022 in Spain, North Evia 2021 in Greece and Montiferru 2021 in Sardinia. Each is a
place-based rectangle in EPSG:4326, defined from place coverage rather than from a fire perimeter and
deliberately not clipped to it, so that unburned cells around each fire form the negative class.
**The record does not show every box fixed before any outcome was seen**, so what it does show is
stated region by region. In the pipeline's version history each box has a single committed value,
never changed afterwards. Montiferru's is derived deterministically from the union of four municipal
boundaries. Manavgat's was drawn to exclude the coastal cropland belt and committed together with the
gate-only workflow that first evaluated it, the commit that first gave the pipeline any Manavgat
geometry; its registry comments disagree on whether the drawing preceded or followed that first gate
run. Bejís's is still labelled the initial candidate in the registry but was committed after its first
gate and model results. Muğla's coordinates appear in a dated preflight record about four minutes
before its first gate result and were committed to the registry only afterwards. No box needed
adjusting to pass the gate, whose admitted margins are wide (Section 4.1). **One choice was label-informed and
is stated as such**: the North Evia box was extended after the legacy box proved atypically high in
burned prevalence, the extended geometry then defined from place anchors and the legacy variant kept
as a sensitivity arm. Section 4.4 shows this framing decision is consequential and Appendix C.5(ix)
treats it as the design lesson of the paper. A sixth region, Kozan 2023, is carried as a negative control and excluded by the gate of
Section 3.3.

Each region has two non-overlapping windows. The **predictor window** closes the day before the
**label window** opens, so no predictor observation can post-date the first labelled burning. Lengths
vary with the event: 57 to 61 days for predictors, 35 to 59 for labels, counted inclusively. A four-year baseline of window-symmetric composites precedes each
predictor window and supplies the climatological reference for the anomaly channels. Region
identifiers, bounding boxes, window dates and baseline years are registered in `core/regions.py` and
reproduced in Appendix C, Table C1. The processing chain and the evaluation
programme it feeds are drawn in Fig. 2.

## 3.2 Burned-area label and the ~500 m analysis grid

Labels come from MODIS MCD64A1 Collection 6.1 [@Giglio2018] retrieved through Google Earth Engine
[@Gorelick2017], whose omission and commission characteristics [@Boschetti2019] bound every model
here. The analysis grid is **reconstructed rather than native**: the pipeline's 30 m EPSG:4326
reference grid is partitioned into 17 x 17 blocks, giving a nominal 510 m cell that approximates
rather than reproduces the MODIS cell and is square in degrees but not on the ground. A cell's burn
date is the mode of its positive sub-pixel day-of-year values, tested against the label window; the
label never affects eligibility for modelling. Two safeguards are recorded rather than assumed:
cells burning before the label window opens are removed, which ran for three of five regions and
excluded 49 cells in Muğla, 16 in North Evia and 61 in Montiferru, with none arising in Manavgat or
Bejís, and burning in earlier years is screened for none. Appendix C.1 gives the
full specification, including what follows from the grid's shape.

## 3.3 Burned-landcover admissibility gate

Before any modelling each region passes a gate asking what fraction of its burned cells is dominated
by natural vegetation, using ESA WorldCover classes [@Zanaga2022] on the same cells. A region is admitted at 0.50
with at least 30 burned cells, and rejected as a cropland-dominated control at 0.50 cropland.
Verdicts and the purpose of the gate are in Section 4.1, the full rule in Appendix C.1.

## 3.4 Predictor variables

Two feature sets are used. The **baseline** is terrain, fuel and greenness: elevation, slope,
dominant land cover and a predictor-window median vegetation-index composite, all static or
near-static over the timescale at which fire danger varies. The **thermal** set adds six pre-fire
channels: current land surface temperature, its anomaly against a four-year window-symmetric
baseline at the same cell, the Temperature-Vegetation Dryness Index and its difference against that
baseline, and two coordinate-informed products, a downscaled and a fused surface temperature. The
two differenced channels are the ones constructed to isolate the dynamic anomaly. TVDI's wet and dry
edges are percentiles of the values a given area and window happen to contain, so **it is not
portable as a physical quantity independently of any concept shift** (Appendices C.4, C.5).

## 3.5 Cell aggregation, validity and analysis populations

Cell-level values are means over the ~510 m cell from valid 30 m pixels only, with the valid fraction
recorded. A cell is `valid_for_modeling` when it is analysis-eligible, meaning not excluded for
pre-label burning, and its predictors are valid: joint finite NDVI, elevation and slope support over
at least 30 % of the cell, finite means for those three channels, and at least one valid land-cover
pixel. **Thermal completeness is not part of the definition**: depending on the region, 6 % to 58 %
of valid cells carry at least one missing thermal channel, and missing values are imputed inside the
fitting pipeline (Section 3.6) rather than by excluding the cell. The **primary** population is natural vegetation, cells whose combined tree,
shrub and grass fraction reaches 0.50, which excludes cropland from every burnable mask. The
**secondary** population is all valid cells; the frozen export carries it for the within-region arm
in two regions, reported as a sensitivity in Appendix A(v), and the transfer matrix is defined on the
primary population only.

## 3.6 Classifier

The two feature sets of Section 3.4 are nested, the thermal set being the baseline plus the six
thermal channels. Land cover is one-hot encoded. Missing numeric values are median-imputed and the
categorical channel most-frequent-imputed, with the imputers fitted inside each training fold, and
on the source alone in transfer, so no held-out or target statistic enters a fit. Features are not
otherwise standardised; standardisation appears only as the adaptation intervention of Section 3.9. The classifier is a random forest [@Breiman2001] with 300 trees, unlimited depth,
`min_samples_leaf = 3`, balanced class weights and `random_state = 42`, identical for every region,
population, feature set and transfer direction, so that no comparison here is confounded by a model
choice.

## 3.7 Spatial-block cross-validation and bootstrap uncertainty

Cross-validation is spatially blocked. Blocks are squares of the analysis grid formed as
`row_500m // B` by `col_500m // B`, and five folds are drawn over whole blocks, so no block is split
between training and test. B is reported at 2, 10 and 20 cells, about 1, 5 and 10 km.

Uncertainty is a spatial-block bootstrap: blocks are resampled with replacement, 1000 replicates,
seed 42, with 2.5 and 97.5 percentiles as the interval. Because it is blocks that are resampled,
what bounds an interval's reliability is the number of blocks carrying at least one burned cell, and
those counts are reported alongside the intervals. Where a verdict rests on too few such blocks it
is stated as indicative rather than as an interval.

## 3.8 Cross-region transfer protocol

For each ordered pair the model is fitted on the source population and applied to the target with
**no target label used at any point**: no refitting, no threshold selection, no calibration. Both
feature sets are transferred, so the thermal block's contribution is a paired difference within a
direction rather than a comparison across directions. All twenty ordered directions are computed.

## 3.9 Label-blind domain adaptation

Two label-free remedies are tested on every direction, in both feature sets.

**Region-wise z-score.** Each region's numeric features are standardised using its own statistics,
source statistics from source data and target statistics from target data, never pooled. The
classifier is refitted on the z-scored source and applied to the z-scored target. This removes
first- and second-order marginal offsets.

**CORAL after region-wise z-score.** The source covariance is aligned to the target's by the standard
whitening-recolouring map [@Sun2016], λ = 10⁻⁵. Critically **the transform is applied to the source
only**; the target is left as it is, and the classifier is refitted on the aligned source. Neither
variant sees a target label, and both are verified label-blind at run time. λ sensitivity was assessed over nine
values on four of the twenty directions, moving transfer AUC by at most 0.014, and no value of λ was
selected on performance; the λ = 1 of the original CORAL formulation lies outside that sweep, while
the value used throughout remains λ = 10⁻⁵ (Appendix A(b)).

## 3.10 Transfer-gap decomposition and the concept-shift criterion

The transfer gap is decomposed as (adapted − raw) / (within − raw), signed and unclipped, with its
interval from the same paired bootstrap; Section 4.3 shows the remainder should not be read as a
conditional residual, because much of it is incurred inside a single region (Appendices A(j), C.7).

The mechanism is diagnosed by **signed univariate association**: the raw ROC-AUC of each numeric
predictor against `burned` is computed per region and never folded to max(AUC, 1 − AUC), so a value
below 0.5 is a direction rather than weakness. A reversal is called bootstrap-supported only when the
two regions' point estimates fall on opposite sides of 0.5 **and each region's own interval excludes
0.5**. That is stricter than requiring the intervals to be disjoint, and a feature failing the second
condition is recorded as a point reversal only.

## 3.11 Interventions

**Pooled multi-region training.** Leave-one-region-out: the model is trained on the pooled primary
populations of the other four regions and evaluated on the held-out region, with folds blocked as
before. This asks whether pooling recovers what single-source transfer loses.

**Removal of direction-reversing features.** The two predictors reversing with bootstrap support
**on the frames as drawn** are **`elevation_mean`** and **`lst_anomaly_mean`**. Section 4.4 withdraws
that support under an equalised frame, so the selection rule is frame-dependent and this arm is
reported as a measurement under the original protocol, not as a consequence of an established
reversal. Both are dropped and everything refitted, within-region and across every direction, and
each is dropped singly so the cost can be attributed. The two features are selected by the same
reversal analysis the result is then read against, so **both quantities are post-selection estimates**
with no correction applied.

## 3.12 Controls on the transfer path

Four evaluations establish what the transfer arms are measuring, all using the transfer protocol of
Section 3.8 unchanged: a **within-region half-split** (modelled cells cut at the median of a grid
axis, both axes and directions, a split discarded when either half is single-class);
**leave-one-scar-out** (each burned component of at least 50 cells, dilated by a 2 km buffer,
withheld from training and used as the target); a **foreign-region evaluation** of the same held-out
scar areas; and the **same blocked model restricted** to those areas, which isolates the evaluation
region from the training regime. Buffers of 2, 5 and 10 km were run, 2 km primary. The per-split and
per-scar positive counts are unequal and bear on the interpretation (Appendix A(i)).

## 3.13 Leakage control and reproducibility

An explicit forbidden-column set is enforced at every model fit as an assertion rather than a
convention: coordinates and their normalised forms, every burn-date and label-provenance column, and
the agreement fraction are excluded from all feature sets. The natural-vegetation mask defines the
population and is never a predictor. All randomness uses seed 42 and the bootstrap 1000
replicates, with one qualification: the diagnostic bootstraps of the released appendices use
per-measure offsets from that seed rather than the seed itself, so that independent measures do not
share a resampling draw. Two of the twenty transfer verdicts are not stable across seeds and are
identified in Section 4.5.
Because the transfer analysis runs in an environment separate from the upstream pipeline's, every
within-region model was refitted against the frozen upstream output: the within-region comparisons
agree exactly and the twenty transfer directions to within 1.6×10⁻⁷, with the tolerance that applies
if the library version is not pinned in Appendix C.5(vi). Headline results are repeated across two
populations, three block sizes, the CORAL sweep, both feature sets and four classifier capacities,
and where a conclusion depends on one of those choices **the dependence is reported rather than
resolved by choosing the favourable setting** (Appendices A, C.6).

## 3.14 Same-geography event-to-event comparison (Muğla 2021 versus 2022)

Muğla admits a comparison in which place is held fixed and the event varies: a second fire burned
inside the identical AOI, on the identical grid, eleven months after the first. Signed univariate
AUCs are computed for both arms under the same 10-cell bootstrap used elsewhere. **Season, year and
population all differ**, since the 2022 arm is defined by removing the 2021 scar (Appendices A(m),
C.3).
