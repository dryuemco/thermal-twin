# The AOI frame artefact

**Status: verified, and it changes the paper's conclusions. Written 2026-08-15 after an internal
referee raised it; every number below was re-derived independently of the referee's script, from the
frozen `repo/outputs/experiments/*/step8a/*.parquet` files, by `paper/code/verify_aoi_frame.py` and
`paper/code/verify_aoi_transfer.py`.**

## The claim

The five "regions" are rectangles of very different generosity relative to their fires. A signed
univariate AUC, and a transfer AUC, computed over a whole rectangle is partly a statement about
where the rectangle was drawn. Because the far fields sit at systematically different elevations
from the burned area, this manufactures apparent sign reversals and apparent anti-prediction.

## Evidence 1: the frames are grossly unequal

Distance from every modelled cell to the nearest burned cell in the same region:

| Region | n | burned | median distance | share > 10 km | max |
|---|---:|---:|---:|---:|---:|
| Manavgat | 20,511 | 784 | 13.4 km | **60.1 %** | 45.7 km |
| Bejís | 15,190 | 1,100 | 13.5 km | **63.1 %** | 34.1 km |
| Muğla | 41,730 | 2,911 | 11.3 km | 55.3 % | 45.7 km |
| Evia | 9,298 | 2,664 | 8.0 km | 43.7 % | 45.7 km |
| Montiferru | 2,544 | 539 | 2.7 km | **2.1 %** | 12.0 km |

Montiferru's frame is fire-scale; Manavgat's and Bejís's are about 60 % far field. "Region" is
confounded with "how wide the box was drawn". This also explains a pattern §4.3 flags but cannot
account for: five of the six directions that improve under adaptation involve Montiferru.

## Evidence 2: Manavgat's far field is 800 m uphill of its fire

| Band from burned area | n | median elevation |
|---|---:|---:|
| 0–5 km | 4,718 | 472 m |
| 5–10 km | 3,475 | 501 m |
| 10–20 km | 5,617 | **955 m** |
| 20–50 km | 6,701 | **1,273 m** |
| burned cells | 784 | 512 m |

AOI maximum 2,355 m. Manavgat's signed elevation AUC of 0.374 is produced by ~12,300 cells 10–46 km
away, in Taurus terrain no plausible spread model would place at risk.

## Evidence 3: the reversals do not survive an equalised frame

Restricting to cells within 10 km of any burned cell. **No positives are dropped**; only far-field
negatives.

| elevation_mean | Manavgat | Bejís | Muğla | Evia | Montiferru | straddles 0.5? |
|---|---:|---:|---:|---:|---:|---|
| full AOI (Table B2) | **0.374** | 0.643 | 0.611 | 0.541 | 0.584 | **yes** |
| ≤ 10 km collar | 0.561 | 0.614 | 0.606 | 0.648 | 0.581 | **no** |

| current_lst_mean | Manavgat | Bejís | Muğla | Evia | Montiferru | straddles 0.5? |
|---|---:|---:|---:|---:|---:|---|
| full AOI | **0.538** | 0.477 | 0.325 | 0.377 | 0.370 | **yes** |
| ≤ 10 km collar | 0.386 | 0.405 | 0.332 | 0.286 | 0.376 | **no** |

`current_tvdi_mean` behaves the same way (full 0.336–0.552 straddling; collar 0.250–0.454, all one
side). Under an equalised frame **all five regions agree in sign** on elevation, on LST and on TVDI,
and both bootstrap-supported elevation reversals of Table B3 vanish.

**One reversal survives.** `lst_anomaly_mean` still straddles 0.5 under the collar (0.392 to 0.584,
Bejís 0.392 against Evia 0.584). This is coherent rather than lucky: the anomaly is the only
cell-relative, lapse-rate-free thermal channel, and it is the only one whose correlation with
elevation is negligible.

| r(feature, elevation) | Manavgat | Bejís | Muğla | Evia | Montiferru |
|---|---:|---:|---:|---:|---:|
| current_lst | **−0.695** | −0.125 | −0.404 | −0.511 | −0.507 |
| current_tvdi | **−0.722** | −0.298 | −0.472 | −0.583 | −0.488 |
| **lst_anomaly** | **+0.036** | +0.142 | +0.235 | −0.195 | +0.256 |

The absolute thermal channels are substantially lapse-rate proxies whose proxy strength varies
fivefold between regions. That, not a change in the dryness–burning relationship, is what the
"reversal" of those channels records.

## Evidence 4: the transfer matrix moves too

Both source and target restricted to the same collar. The reference arm reproduces the frozen
matrix, so this is measuring the same quantity.

| source frame | target frame | mean target AUC | above chance | below chance | paired thermal delta |
|---|---|---:|---:|---:|---:|
| full | full (**= Table 4**) | 0.5400 | 14/20 | **6** | +0.0029 |
| full | 10 km | 0.5753 | 17/20 | 3 | +0.0021 |
| 10 km | full | 0.5707 | 17/20 | 3 | +0.0143 |
| **10 km** | **10 km** | **0.6166** | **19/20** | **1** | **+0.0234** |
| 5 km | 5 km | 0.6077 | 18/20 | 2 | +0.0141 |

Reference check: full/full reproduces mean 0.5400 against the frozen 0.541 and 14/20 exactly.

Largest movers: Bejís→Evia 0.383 → 0.602, Bejís→Manavgat 0.440 → 0.601, Manavgat→Evia 0.604 → 0.726,
Muğla→Manavgat 0.393 → 0.510.

## What this does and does not overturn

**Does not survive:**
- "Six directions are anti-predictive with interval support" — one direction under the equalised
  frame.
- Elevation and LST/TVDI sign reversal as the mechanism of the residual (current Contribution 4).
  Under an equalised frame all five regions agree in sign on all three.
- "The thermal block contributes +0.004, indistinguishable from zero, across regions" — the paired
  delta rises to +0.0234 once frames are equalised.

**Survives:**
- The central negative claim. Equalised transfer is 0.617 against within-region ≈ 0.87. Local skill
  still does not travel.
- Contribution 1, the evaluation-geometry measurement — **strengthened**, because this is the same
  effect acting on the paper's own transfer matrix.
- One reversal, `lst_anomaly_mean` between Bejís and Evia, on the one channel where a lapse-rate
  explanation is unavailable.
- The within-region increment (checked separately by the referee, +0.031 to +0.118 under the collar
  against +0.064 to +0.151 on the full frame).

## The reading

The paper measured, in `prevalence_control.json`, that swapping a region's negatives for
fire-adjacent ones moves AUC by **+0.155 [+0.093, +0.217]**, and then computed its entire transfer
matrix and its whole reversal mechanism on frames whose fire-adjacent share ranges from 2 % to 98 %.
The artefact and its explanation are both already in the manuscript; they had not been connected.

This makes the paper more coherent, not less. Contribution 1 stops being a control that happens to
be interesting and becomes the organising result: **where you evaluate decides what you report**,
demonstrated first on one model in one region, and then on the paper's own five-region transfer
matrix and its own claimed mechanism.
