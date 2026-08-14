# 4. The budget, axis by axis

Each axis below is varied with everything else held fixed: the same five regions, the same label
product, the same feature sets, the same classifier, the same spatially blocked folds and the same
bootstrap. Effects are therefore comparable across axes. For scale, the within-region effect these
models report is +0.056 to +0.153 ROC-AUC, and its bootstrap interval at 1 km blocking is about
±0.010 wide.

## 4.1 The analysis cell is not the cell it is called

The grid is built by aggregating 17 × 17 reference pixels, each exported at 30 m in EPSG:4326, into
a cell described throughout as ~500 m. Because the export is in a geographic coordinate system, the
reference pixel is a step in degrees, 30 / 111,319.49 = 0.00026949°, so the cell is 17 times that,
0.0045814°, **in both axes**. On the ground it is about 510 m north to south everywhere, but only
407 m east to west at 37° N and 390 m at 40° N. Cell area is 0.199 to 0.208 km² against the MODIS
cell's 0.250 km², so the analysis cell is 17 to 20 % smaller than the cell it approximates.

The derivation is checkable rather than nominal: dividing each AOI's span by 0.0045814° and rounding
outward reproduces every frozen cell count in the cohort exactly (Table 1).

**Table 1. The analysis cell's true ground dimensions, per region.** Columns and rows are derived by
dividing each AOI's span by the cell step of 0.0045814° and rounding outward; the frozen cell count
is the one recorded in the pipeline's own outputs, and the two agree exactly in every region. The
north-south edge is about 510 m everywhere; only the east-west edge varies, with latitude.

| Region | Derived columns × rows | Frozen cell count | East-west edge |
|---|---|---:|---:|
| Manavgat 2021 | 175 × 138 | 24,150 | 407 m |
| Bejís 2022 | 153 × 103 | 15,759 | 391 m |
| Muğla 2021 | 393 × 186 | 73,098 | 407 m |
| North Evia 2021 | 175 × 131 | 22,925 | 397 m |
| Montiferru 2021 | 66 × 49 | 3,234 | 390 m |

Two consequences follow and neither is cosmetic. Every block-size label in a study of this kind is
the north-south dimension: a 10-cell block described as ~5 km is 5.1 km by 3.9 to 4.1 km, so
**spatial blocking is systematically weaker in longitude by about a fifth**, in analyses whose
central robustness argument is blocking scale. And because the cell is smaller than a MODIS cell and
not aligned to it, a typical cell draws on more than one MODIS cell, which dilates the labelled
burned footprint relative to the source product.

## 4.2 Observation provenance: a quality rule applied to part of a cohort

The coarse thermal input is `MOD11A1`. Two of the five regions apply a `QC_Day` bit rule with a
three-observation minimum and write an explicit −9999 nodata sentinel; three apply no quality mask
and declare no nodata value. The split follows **export date**, not design: the rule was added to
the export script on 2026-07-23, after three regions had already been exported. Nothing in the
outputs marks the difference; it is visible only by comparing metadata across regions.

The size and shape of what that costs were measured by recomputing each unscreened region's
predictor-window mean with and without the rule (Table 2).

**Table 2. Cost of the quality-screening rule in the three regions that were exported without it.**
Each region's predictor-window mean was recomputed with the `QC_Day` bit rule and the
three-observation minimum applied, and differenced against the frozen unscreened mean. The final
column is what matters: a shift correlated with elevation is not an offset a downscaling model
would absorb.

| Region | Mean shift | SD of shift | Pixels below the 3-observation minimum | Correlation of the shift with elevation |
|---|---:|---:|---:|---:|
| Manavgat 2021 | +1.17 °C | 0.60 | 0.2 % | **+0.615** |
| Muğla 2021 | +0.67 °C | 0.50 | 0.1 % | +0.443 |
| Bejís 2022 | +0.47 °C | 0.89 | 3.6 % | −0.041 |

Coverage is barely affected. What matters is that **the change is not a uniform offset**, which a
downscaling model fitted to Landsat would largely absorb: in two of the three regions it correlates
with elevation, at +0.615 in the region whose elevation-burning association is the one that reverses
in the companion paper. This does not establish that the screening split explains that behaviour; it
establishes that the candidate has a mechanism and is strongest where the anomaly is.

**Zero-fill.** The same three unscreened regions declare no nodata value, so cells with nothing to
report are written as exact 0.0 °C. Counting them: 518 of 6,390 pixels in Manavgat (8.11 %),
**7,347 of 19,190 in Muğla (38.29 %)** and **none at all in Bejís**. Both non-zero fractions exceed
the pipeline's own 5 % suspicious-zero guard. What the zeros are is settled by the counts, which
track each AOI's water-dominant cell share almost exactly, 8.3 % and 38.9 % against 0.1 % for the
one inland AOI: **the zero-fill is sea encoded as a physical temperature**, not missing observation.

## 4.3 Compositing: a decision whose relevance is readable in advance

A current-period composite is a median over the clear acquisitions in the window, and how those
acquisitions are weighted is a choice. A scene-weighted median counts every scene; a date-balanced
median counts every calendar date once. The pipeline offers both, and an audit compares them at
support boundaries, where a positive value means the date-balanced chain lowers the discontinuity.

For Manavgat the intervention helps at every boundary type, which is what motivated it. Extending
the audit to three more regions turns that into a rule (Table 3).

**Table 3. Whether the compositing choice can act, read from the scene inventory alone.** Scenes per
distinct acquisition date is counted before anything is fitted. Where it is 1.0 the two compositing
chains produce identical rasters and there are no same-day boundaries to compare, so the verdict is
not "no evidence" but "no effect is possible". The verdict column reports the boundary-discontinuity
audit only for the two regions where the intervention can act.

| Region | WRS tiles in the window | Scenes | Distinct dates | Scenes per date | Same-day boundaries | Verdict |
|---|---|---:|---:|---:|---:|---|
| Manavgat 2021 | 177/34, 177/35, 178/34, 178/35 | 14 | 7 | **2.0** | 172 | **supported reduction** |
| Bejís 2022 | 198/32, 198/33, 199/32, 199/33 | 16 | 8 | **2.0** | 79 | uncertain |
| North Evia 2021 | 183/33, 184/33 | 8 | 8 | 1.0 | **0** | no effect |
| Montiferru 2021 | 193/32 | 4 | 4 | 1.0 | **0** | no effect |

Where scenes per date is 1.0 the two chains produce **identical rasters** and every boundary estimate
is exactly zero, with no same-day boundaries existing to compare. The dividing line is not the number
of Landsat paths an AOI spans: Evia spans two, as Manavgat and Bejís do, and shows nothing, because
its two paths image it on different days. What Manavgat and Bejís share is spanning two WRS **rows**,
so a single overpass delivers two scenes bearing the same date, which is exactly what a
scene-weighted median double-counts.

Among the two regions where the intervention can act, only Manavgat improves consistently; Bejís
improves at the boundary the intervention targets, +0.378 [+0.278, +0.483], and gets **worse** at
unique-date-count edges, −0.067 [−0.095, −0.041], for an overall verdict of uncertain. The downstream
ROC-AUC comparison is admissible only for Manavgat, where three defensible chains on an identical
cohort give increments of +0.045, +0.064 and +0.084, a tolerance of about ±0.02.

**The rule.** Scenes per distinct acquisition date, counted from the scene inventory before anything
is fitted, tells a reader whether this decision can move their result at all. In this cohort it can
in two regions of four, and does consistently in one.

## 4.4 Index normalisation: sea inside a scene-fitted dryness index

TVDI is normalised against wet and dry edges taken as percentiles of the land surface temperatures a
scene contains, within bins of a vegetation index. The AOIs are place-based rectangles that are not
clipped to the coastline, and the water bit is deliberately preserved, so sea takes part in that fit.
Water-dominant cells are 57.6 % of one AOI and 38.9 % of another, against 0.1 % for the one inland
region.

The contamination is real and visible: in the marine AOI the three lowest vegetation-index bins carry
dry edges of 28.8 to 29.9 °C, which is sea-surface temperature and not a land dry edge, where the
inland AOI's equivalent bins sit near 49 °C.

**It does not reach the modelled population.** Not one cell of the primary natural-vegetation
population in any region has a mean vegetation index below 0.15, and the fifth percentile is 0.376
in the marine AOI, so the population occupies bins where the dry edge is a genuine land edge, 44 to
47.5 °C. Refitting the edges on land pixels alone shifts the signed association of the index with
burning by an amount that scales with sea fraction, +0.017 and +0.016 in the two marine AOIs against
+0.002 inland, and **changes no region's direction**.

A stronger test removes the scene dependence itself. Fitting one set of edges over the pooled land
pixels of all five regions, 26.2 million of them, so that a given index value denotes the same
dryness everywhere, leaves the disagreement intact: one region still ranks burned cells by higher
dryness at 0.565 while two others rank them by lower dryness with bootstrap support, at 0.341 and
0.378. **The index's scene dependence is not the explanation for its reversal.**

## 4.5 Label quality

**A second burned-area product is not available for these years.** The usual comparator for MCD64A1
stops at December 2020 and every fire in this cohort is 2021 or 2022. That limitation cannot be
closed with the products available and is stated rather than worked around.

**Agreement.** The share of a burned cell's positive sub-pixels agreeing with its modal burn date has
a median of 1.000 in every region but a non-empty lower tail. Dropping burned cells below agreement
thresholds of 0.75 and 0.90 leaves every reversal in the cohort intact, and moves the sharpest one
*further* from chance as thin-evidence cells are removed.

**Omission.** An independent active-fire observation covers the period and is independent of the
burned-area algorithm. Cells it saw burning that the burned-area product did not label do sit
systematically lower than labelled ones, 258 m against 512 m in one region, which is the
predictor-correlated omission the literature worries about. Relabelling every such cell as burned,
which deliberately over-corrects, changes **no** feature's side of chance in any region, and moves
the sharpest reversal from 0.374 to 0.308, further from chance. The bias runs opposite to the
direction that would threaten the result.

**Pre-label exposure.** Where the safeguard that removes cells burning inside their own predictor
window did not run, the exposure is zero cells in one region and 28 in the other, under 0.2 % of its
population. It could not be measured from the archive, because both label rasters there are clipped
to the label window; it required the unclipped product.

## 4.6 Derived channels and design choices

**Gap-filled thermal cells.** Where the fused product falls back on a modelled surface, the channel
is not an observation. The gap-filled share is concentrated rather than diffuse, reaching 18.8 % of
cells in one region against 2.0 to 9.1 % elsewhere. Restricting to cells at most 10 % gap-filled
leaves the increment bootstrap-supported in all five regions; the most exposed region moves most and
in the predicted direction, +0.056 to +0.043, and the others by at most 0.008.

**Coordinate-bearing channels.** Two derived channels inherit a coordinate-derived component from
their own model's inputs, which is the one route by which coordinates re-enter a feature set that
excludes them. Dropping both retains 82 % to 103 % of the increment, every interval excluding zero,
so the coordinate component is not what produces the within-region skill.

**Population definition.** The secondary all-valid population is **57.7 % and 38.9 % seawater** in the
two marine AOIs, because sea cells satisfy every validity criterion. Most of the extra separability
that population shows is therefore land against sea rather than any fire-relevant contrast, which is
why the natural-vegetation population is primary.

**Population size and positive count.** Matching the largest region to the smallest on cell count and
positive count together, over ten stratified draws, leaves its transfer behaviour inside the matched
range in both roles while moving its within-region increment from +0.116 to a median +0.098. Part of
a within-region increment is a positive-count effect; the transfer behaviour is not.

**Blocking scale.** Recomputing the transfer verdicts at 5 km rather than 1 km blocking moves the
counts from ten positive, seven negative and three uncertain to six, four and ten, while **no
direction changes side of the chance line and no point estimate changes sign**. Counts are the
fragile quantity; signs are not.

## 4.7 Software

With byte-identical data, pipeline and seed, changing only the library version moves two frozen
cross-region probes by +0.021 and +0.026 AUC, so cross-region point estimates carry an implementation
tolerance of roughly ±0.02 to 0.03 unless the version is pinned. Within-region AUCs reproduce to
about four decimals across versions.

Against that, the within-region results rebuild **bit for bit**. Reconstructing the environment from
the released dependency pins on a different operating system and re-running the released modelling
step against the archived inputs reproduces every numeric field of the frozen metrics: 142 fields for
one region with a maximum absolute difference of 6.9×10⁻¹⁸, and 168 for another with a maximum
difference of **exactly 0**. A regularisation constant that the released sensitivity sweep omits was
also recomputed directly and leaves every direction on its side of chance, widening the sweep's
reported spread from 0.014 to 0.019.
