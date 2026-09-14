# 3. Cohort and protocol

## 3.1 The cohort and what is held fixed

Five Mediterranean wildfire regions are used: Manavgat 2021 and Muğla 2021 in Türkiye, Bejís 2022 in
Spain, North Evia 2021 in Greece and Montiferru 2021 in Sardinia. They were assembled for the
companion study and are described there in full: place-based rectangular areas of interest, burned
labels from MODIS MCD64A1 Collection 6.1, an analysis grid of ~510 m cells reconstructed from a 30 m
reference grid, predictors from Landsat 8 Collection 2 Level-2 and MODIS MOD11A1 over a predictor
window closing the day before the first labelled burning, and a natural-vegetation primary
population.

Everything downstream of the axis under test is held fixed: the same random forest with the same
hyperparameters and seed, the same nested baseline and thermal feature sets, the same five-fold
spatially blocked cross-validation, and the same spatial-block bootstrap with 1000 replicates. This
is what makes the axes comparable: any difference reported below is the axis, not a model choice.

## 3.2 How an axis is varied

Each axis is varied by re-running the pipeline's own code with one input or one setting changed, and
never by reimplementing it. Where a rule had to be applied that the released tooling does not expose,
the pipeline's own primitives were imported and driven directly, so that the binning, percentile,
alignment and metric functions are identical between arms and only the pixel selection or the
parameter differs.

Three practices are used throughout and are what make the comparisons trustworthy rather than merely
plausible.

**Reproduce before you vary.** Every arm that has a frozen counterpart reproduces it first, and the
reproduction is reported alongside the new number. Where an arm cannot reproduce its comparator, the
comparison is not made.

**Vary one thing.** Where an axis required staging inputs into a different location, the provenance
pointers were repointed to the staged copies and the change recorded, rather than allowing a path
mismatch to be read as a scientific difference.

**Report the axes that did nothing.** An axis found not to move the result is reported at the same
length as one that did, because a budget in which every entry is large is not a budget.

## 3.3 The eight axes

1. **Analysis-cell geometry.** Derived from the export scale and coordinate system and checked
   against the frozen cell counts. Not a variation but a description; reported because block-size
   labels depend on it. One provenance fact belongs here: no Earth Engine call in the pipeline sets
   an explicit resampling kernel, every export declaring only a scale and a coordinate system, so
   the platform's documented default of nearest-neighbour reprojection applies to every export,
   while the alignment kernels the pipeline does choose, bilinear for continuous rasters and
   nearest for categorical ones, are applied locally.
2. **Coarse-thermal quality screening.** The pipeline's own `QC_Day` bit rule and three-observation
   minimum, applied to the three regions exported before the rule existed, compared against their
   unscreened means at the input. That the cohort splits this way is established from provenance
   rather than assumed: the rule entered the export script on 2026-07-23, after those three regions
   had been exported, and nothing in the outputs marks the difference, so it was recovered by
   comparing export metadata across regions (Section 4.2).
3. **Nodata convention.** Exact-zero counts in each region's coarse thermal layer, against the
   pipeline's own suspicious-zero guard and each region's water-dominant cell share.
4. **Compositing chain.** The released counterfactual audit, which builds a date-balanced composite
   alongside the production scene-weighted one and compares them at support boundaries with a paired
   bootstrap, run for four regions. Each region's diagnostic chain is checked against the frozen
   canonical products before its comparison is read.
5. **Index normalisation.** The dryness index's wet and dry edges refitted on land pixels alone, and
   a third set fitted once over the pooled land pixels of all five regions, with the index
   recomputed and aggregated to cells each time and the signed association re-measured under the
   registered 10-cell spatial-block bootstrap.
6. **Label quality.** Three probes: restriction to burned cells above sub-pixel agreement thresholds;
   relabelling against an independent active-fire observation; and the exposure left where the
   pre-label safeguard did not run, measured against the unclipped burned-area product.
7. **Derived channels and design choices.** Restriction to low gap-fill cells; removal of the two
   coordinate-bearing channels; the water content of the secondary population; matching the largest
   region to the smallest on cell count and positive count; and the blocking scale of the transfer
   intervals.
8. **Software.** Library-version sensitivity from frozen probes, and an independent rebuild of the
   environment on a different operating system with a field-by-field comparison against the frozen
   metrics.

## 3.4 Reporting conventions

Signed univariate associations are reported as raw ROC-AUC against the burned label and are never
folded to max(AUC, 1 − AUC), so a value below 0.5 is a direction rather than weakness, and a
difference between regions is called supported only when the two bootstrap intervals are disjoint.
Where a verdict changes on a margin smaller than the precision of the counts behind it, that is
stated with the verdict.
