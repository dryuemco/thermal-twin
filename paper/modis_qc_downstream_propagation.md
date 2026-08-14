# Propagating the MOD11A1 quality screening through the downstream chain

**What this is.** The companion paper reports that the coarse thermal input is quality-screened in
two of five regions and unscreened in three, that the split follows export date rather than design,
and that the induced change at the input is not a uniform offset but correlates with elevation at
**+0.615 in Manavgat**. That measurement stops at the input. Its own limitations section says so:
the axis was "measured at the input and not propagated through the downstream chain, which would
require rebuilding three regions' derived products."

This note propagates it, for Manavgat and then for Muğla, and converts the bounded axis into a
measured one for two of the three unscreened regions.

It matters beyond bookkeeping. An elevation-correlated preprocessing artefact, in the one region
whose elevation-burning association anchors the transfer paper's reversal mechanism, is a live
competing explanation for that mechanism. Two independent reviews raised it as potentially fatal.
Either it propagates and the mechanism is in question, or it does not and the candidate is closed.

Run 2026-08-14. Driver `run_qc_propagation.ps1`; comparison `qc_compare.py`; machine-readable
output `modis_qc_downstream_propagation.json`.

## Design: two arms, both rebuilt here

The frozen outputs were produced on another machine by another operator. Comparing a screened arm
directly against them would mix the screening effect with every difference the rerun itself
introduces. So **both** arms were rebuilt from the same staged inputs, with the same code and the
same pinned environment, and only the MODIS input differs between them:

- **Arm A** — unscreened MODIS, exactly as exported for this region, then `step7` (downscaling and
  fusion) then `step8` (500 m modelling dataset and metrics).
- **Arm B** — MODIS regenerated with the `QC_Day` mandatory-QA and data-quality bit rule and the
  three-observation minimum, carrying the explicit `-9999` nodata sentinel, then the identical
  `step7` and `step8` chain.

The driver refuses to continue if the regenerated raster does not carry the `-9999` tag, since
without it arm B would not be the screened chain. It carried it.

**Arm A reproduces the frozen result.** Its within-region thermal increment is
ΔAUC 95 % CI `[0.0546, 0.0786]` against the published `+0.067 [+0.055, +0.078]`. The rerun is
therefore a valid comparator and the contrast below is not confounded with rebuild drift.

## The screening propagates, and it propagates substantially

This is not a null intervention that failed to reach the model. Comparing the two arms' 500 m
modelling datasets cell by cell, over all 24,150 cells:

| Channel | Cells changed | Mean abs. change | Max abs. change |
|---|---:|---:|---:|
| `downscaled_lst_mean` | **22,304** of 24,150 | 0.365 °C | **10.877 °C** |
| `fused_lst_mean` | 1,804 | 0.017 °C | 4.602 °C |
| `current_lst_mean` | 0 | 0 | 0 |
| `elevation_mean` | 0 | 0 | 0 |
| `lst_anomaly_mean` | 0 | 0 | 0 |

Ninety-two per cent of cells have a different downscaled surface, by up to 10.9 °C. The Landsat-derived
channels are byte-identical, as they must be, since the screening touches only the MODIS input.
`fused_lst` changes on 1,804 cells because fusion takes the observed Landsat value wherever it is
valid and the downscaled surface only where it is not: observed coverage is 97.24 % and fused
coverage 99.37 %, so the modelled surface reaches only the 2.14-point gap.

## The modelled associations are nonetheless insensitive to it

Signed univariate AUC against `burned`, never folded to max(AUC, 1−AUC), primary
natural-vegetation population, 10-cell (~5 km) spatial-block bootstrap, 1000 replicates, seed 42.

| Feature | Arm A (unscreened) | Arm B (screened) | Shift |
|---|---|---|---:|
| `elevation_mean` | 0.374 `[0.290, 0.472]` | 0.374 `[0.290, 0.472]` | **+0.0000** |
| `slope_mean` | 0.531 `[0.426, 0.648]` | 0.531 `[0.426, 0.648]` | +0.0000 |
| `ndvi_mean` | 0.636 `[0.587, 0.678]` | 0.636 `[0.587, 0.678]` | +0.0000 |
| `lst_anomaly_mean` | 0.482 `[0.424, 0.533]` | 0.482 `[0.424, 0.533]` | +0.0000 |
| `current_lst_mean` | 0.538 `[0.450, 0.619]` | 0.538 `[0.450, 0.619]` | +0.0000 |
| `current_tvdi_mean` | 0.552 `[0.456, 0.636]` | 0.552 `[0.456, 0.636]` | +0.0000 |
| `tvdi_difference_mean` | 0.449 `[0.385, 0.507]` | 0.449 `[0.385, 0.507]` | +0.0000 |
| `downscaled_lst_mean` | 0.552 `[0.460, 0.635]` | 0.552 `[0.462, 0.636]` | **+0.0003** |
| `fused_lst_mean` | 0.540 `[0.452, 0.621]` | 0.540 `[0.452, 0.621]` | −0.0000 |

The population is unchanged: 20,511 cells, 784 burned, 28 positive-carrying 5 km blocks in both
arms. The within-region thermal increment is unchanged: `[0.0546, 0.0786]` against
`[0.0543, 0.0774]`.

Not one feature changes side of the chance line, and the largest movement in any signed association
is **+0.0003**, in the one channel that is by construction most exposed.

## What this closes, and what it does not

**Closed.** The quality-screening split is not the explanation for Manavgat's elevation reversal.
Two things make that conclusion structural rather than lucky. Elevation is a DEM variable: screening
a thermal product cannot change its values, and here it did not change the population either, so
there is no route by which the screening could move the elevation-burning association. And the
thermal channels that carry the signal are Landsat-derived, with fusion falling back on the
MODIS-derived surface across only 2.14 points of coverage, so even a 10.9 °C change in the
downscaled surface is diluted to +0.0003 in the association.

The elevation correlation of +0.615 at the input is real and worth reporting. It does not survive
into the modelled associations.

**Not closed.** Three things.

1. ~~**One region.**~~ **Muğla has now been run and agrees.** Its population is unchanged at 41,730
   cells and 2,911 burned, with 70 positive-carrying 5 km blocks in both arms. The screening again
   propagates substantially, changing `downscaled_lst_mean` on **46,356 of 73,098 cells** by a mean
   of 0.428 °C and a maximum of **20.97 °C**, larger in every respect than in Manavgat. The modelled
   associations again do not follow: elevation stays at 0.611 [0.529, 0.692] in both arms, the
   largest movement in any signed association is **−0.0079** in `downscaled_lst_mean` itself, and no
   feature changes side of the chance line. Muğla was the more informative of the two remaining
   regions, having a zero-fill share of 38.3 % against Manavgat's 8.1 %, and it dilutes the effect
   even further, because its observed Landsat coverage is 99.39 % so fusion falls back on the
   modelled surface across only 0.57 points rather than Manavgat's 2.14. **Bejís remains unrun**,
   and it is the least informative of the three, its input-level correlation with elevation being
   −0.041.
2. **Transfer was not recomputed.** The claim above is about signed associations and the
   within-region increment. Since the two arms' feature matrices differ in one channel by a mean of
   0.365 °C, and that channel's association moves by +0.0003, a material change in transfer is
   implausible — but it is inferred, not measured.
3. **Manavgat's atypical transfer behaviour remains unexplained.** This note removes a candidate; it
   does not supply one. That limitation stands as written, minus this explanation.

## Where this belongs

- **Companion paper §4.2 and §5.5(iii).** The axis moves from bounded to measured for one region.
  The propagation table and the insensitivity table are the result; §5.5(iii)'s admission should be
  narrowed to Muğla and Bejís.
- **Transfer paper, limitation (viii).** The sentence naming a quality-screening difference as a
  second candidate for Manavgat's behaviour should be replaced by the measured negative: the
  candidate was tested by propagating the screening through the full chain and does not explain it.
