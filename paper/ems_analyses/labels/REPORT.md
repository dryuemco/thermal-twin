# Label-quality and predictor analyses requested in referee round 5 — report (2026-09-19)

Specification: `SPEC.md` (base spec before any run; Addendum A before analysis 5; Addendum B marked
post hoc). Code: `paper/code/ems_labels_common.py`, `ems_labels_{1_prelabel,2_history,3_fraction,
4_dimensionality,5_manavgat_labelwindow,5b_manavgat_collar_sign,6_calibration}.py`. Earth Engine
queries used the pipeline's own `build_raw_burndate_image`, read-only (`computePixels`, no exports).

## Validation of the rebuild
The Earth Engine rebuild reproduces the frozen pre-label rasters of Muğla, Evia and Montiferru with 0
pixel mismatches and exactly the recorded 49/16/61 excluded cells, and Bejís's label raster exactly.
The label rule recomputed from local rasters matches the parquet `burned` in all five regions (0
disagreements). Reference arms reproduce Table 1 to ≤ 0.001 and the 20 transfer directions to ≤ 5e-5.
Fold-draw noise alone (splitter seeds 1–10, post hoc) moves ΔAUC by about ±0.01–0.02 at B = 10.

## 1. Pre-label burns (Manavgat, Bejís)
Manavgat: none. **Bejís: 49 cells** (48 in the natural-vegetation population, 10 of them also labelled
burned; burn dates 19–20 June, 25–29 July, 2 and 13 August 2022). Excluding them: B = 2 +0.056 → +0.050
[0.042, 0.059]; B = 10 +0.045 → +0.062 [0.037, 0.088]; indistinguishable from removing 48 random cells
(+0.047..+0.055 and +0.037..+0.067). The current §3.2 sentence ("none arising in Manavgat or Bejís") is
false for Bejís.

## 2. Burns in the five preceding years
Natural-vegetation cells: Manavgat 0; Bejís 163 (0 also labelled burned); Muğla 194 (25); Evia 366,
3.9 % (88); Montiferru 58 (32). With them excluded, B = 10 increments: Bejís +0.055 [0.025, 0.082],
Muğla +0.088 [0.063, 0.111], Evia +0.162 [0.129, 0.200], Montiferru +0.111 [0.032, 0.192]; all within
fold-draw noise of the reference. Transfer means 0.537 / 0.541 / +0.004 become 0.537 / 0.537 / +0.000.
On the frozen labels the collar "hotter surfaces burned less" signs survive.

## 3. Burned-fraction threshold
The 30 m label is a nearest-neighbour copy of ~463 m MODIS pixels, so the fraction is the share of the
cell covered by burned MODIS footprints, not a true sub-pixel burned fraction. At ≥ 50 %, 4 % (Evia) to
20 % (Manavgat) of burned cells drop. Every increment interval still excludes zero (Montiferru at
B = 10 only barely, on 14 positive blocks: indicative).

## 4. Thermal-block dimensionality
PC1 explains 0.71–0.75 of variance, PC2 0.19–0.26; two components reach 90 % in every region. The four
absolute channels correlate at r = 0.83–1.00 (current vs fused ≥ 0.995); the two differenced channels at
0.71–0.94. `fused_lst_mean` equals `current_lst_mean` exactly in 84.2–99.4 % of rows. **The six channels
are effectively two dimensions.**

## 5. Manavgat label defect (found in the course of this work; verified independently)
The frozen Manavgat label raster (`drive_new/.../manavgat_2021/validation/labels/mcd64a1_raw.tif`)
contains burn days 213–241 only; the label window opens on 2021-07-28 (day 209). Cause: the month-aligned
MCD64A1 query bug documented in `repo/src/step6_validate_fire_relation.py`
(`_mcd64a1_collection_query_bounds`), fixed in repo commit `183be42` on 2026-07-11; the Manavgat raster
was exported on 2026-07-08, before the fix. Earth Engine returns 624,130 further in-window 30 m
sub-pixels dated 28–31 July. **Burned natural-vegetation cells go from 784 to 2,935: the paper uses 27 %
of Manavgat's burned cells.** The other regions' windows open on their first label day and are unaffected.

With the full window: the within-region increment holds (B = 2 +0.067 → +0.067; B = 10 +0.050 → +0.062
[0.041, 0.082]); transfer means become 0.519 / 0.527 / +0.007. **Elevation reverses much more strongly**
(full frame 0.374 → 0.232 [0.177, 0.287]; collar 0.561 → 0.376 [0.300, 0.465]), contradicting "elevation
above 0.5 in all five under the collar". **Manavgat LST flips** (full frame 0.538 → 0.665; collar
0.386 → 0.522), so "hotter surfaces burned less in every region" fails for Manavgat. Adaptation,
decomposition, scar/half-split controls and diagnostics were not re-run on corrected labels.
