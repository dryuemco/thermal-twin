# A label-omission control, and why it is not a second burned-area product

Section 5.11(xiv) names two things: that MCD64A1's omission at 500 m in fragmented Mediterranean
terrain is itself correlated with patch size, terrain and land-cover fragmentation, which are the
baseline predictors, and that no second label product was used as a control. The first is the
substantive worry, because differential omission in a terrain variable is a competing explanation for
the elevation reversal that carries the paper.

## A second burned-area product is not available for these years

ESA CCI FireCCI51, the usual comparator for MCD64A1, is in Earth Engine as 240 monthly images at
250 m covering **2001-01-01 to 2020-12-01**. Every fire in this study is 2021 or 2022, so it cannot
label anything here. That limitation therefore stands and cannot be closed with the products
available; it is stated rather than worked around.

## What can be done instead

FIRMS active-fire detections cover the period. They are a different quantity, a thermal anomaly at
satellite overpass rather than a mapped scar, so they cannot relabel the dataset. What they can do is
probe the exact mechanism the limitation names, because they are an observation of fire that is
independent of the burned-area algorithm.

For each region, within its own label window and AOI, every FIRMS detection at confidence 50 or above
was mapped to its 500 m analysis cell, and the primary population split three ways.

| Region | FIRMS cells | Burned cells with a FIRMS hit | MCD64A1 burned: median elev / slope | FIRMS-only: median elev / slope | Neither: median elev / slope |
|---|---:|---:|---|---|---|
| Manavgat 2021 | 1,161 | 26.1 % | 512 m / 18.9 | 258 m / 15.6 | 941 m / 18.8 |
| Bejís 2022 | 412 | 23.7 % | 935 m / 14.2 | 877 m / 12.9 | 785 m / 13.6 |
| Muğla 2021 | 1,512 | 25.9 % | 563 m / 19.0 | 524 m / 15.5 | 425 m / 15.4 |
| North Evia 2021 (ext.) | 897 | 24.0 % | 263 m / 15.1 | 136 m / 14.5 | 231 m / 15.7 |
| Montiferru 2021 | 331 | 23.4 % | 424 m / 9.2 | 419 m / 9.0 | 352 m / 5.7 |

That only about a quarter of burned cells carry a FIRMS detection is expected and is not an omission
estimate: FIRMS sees fire that is burning at an overpass moment, while a scar is mapped whenever it
burned. The consistency of that share across five regions, 23.4 % to 26.1 %, is a useful check that
the cell mapping is sound.

The cells FIRMS saw and MCD64A1 did not label do sit systematically lower than the labelled ones in
three regions, most sharply in Manavgat, 258 m against 512 m. If these were genuinely burned and
missed, the omission would be correlated with elevation, which is exactly the concern.

## The direct test: does the omission manufacture the reversal?

Rather than argue about it, every FIRMS-only cell was relabelled as burned and the signed univariate
AUCs recomputed. This deliberately over-corrects, since many FIRMS detections are small fires,
agricultural burning or other thermal anomalies that no burned-area product should map at 500 m. If
the reversal survives an over-correction, omission is not what produces it. Bootstrap as in Section
3.12: 10-cell blocks, 1000 replicates, seed 42.

| Region | Feature | As labelled | With FIRMS-only cells as burned |
|---|---|---|---|
| Manavgat | elevation | 0.374 [0.289, 0.471] | **0.308** [0.249, 0.366] |
| Bejís | elevation | 0.643 [0.558, 0.729] | 0.639 [0.554, 0.725] |
| Muğla | elevation | 0.611 [0.531, 0.695] | 0.602 [0.529, 0.676] |
| North Evia | elevation | 0.541 [0.458, 0.632] | 0.530 [0.448, 0.618] |
| Montiferru | elevation | 0.584 [0.395, 0.762] | 0.571 [0.409, 0.728] |
| Manavgat | current LST | 0.538 [0.452, 0.621] | 0.613 [0.561, 0.670] |
| Manavgat | current TVDI | 0.552 [0.460, 0.641] | 0.622 [0.567, 0.681] |
| Muğla | current LST | 0.325 [0.271, 0.381] | 0.355 [0.306, 0.407] |
| North Evia | current LST | 0.377 [0.300, 0.454] | 0.382 [0.307, 0.457] |

**No feature in any region changes its side of 0.5.** The Manavgat-against-Bejís and
Manavgat-against-Muğla elevation contrasts, which are the paper's sharpest, both survive. And the
correction runs *against* the conservative direction: Manavgat's elevation moves further from chance,
0.374 to 0.308, and its two thermal channels move up and away from chance as well, 0.538 to 0.613 and
0.552 to 0.622, which widens rather than narrows its disagreement with Muğla and Evia.

So differential label omission does not manufacture the reversals. If MCD64A1 is missing burned area
in a way correlated with terrain, correcting for it would sharpen the paper's finding, not dissolve
it.

## What this does and does not settle

It does not replace a second burned-area product, and the manuscript should keep saying so. FIRMS is
an active-fire observation with its own omission and commission behaviour, the relabelling is
deliberately crude, and no claim is made that the FIRMS-only cells actually burned. What it settles
is narrower and sufficient: the specific competing explanation named in 5.11(xiv), that
predictor-correlated label omission produces the elevation reversal, is not supported, and the bias
it would introduce runs in the opposite direction to the one that would threaten the result.

## Provenance

`paper/label_omission_control.json`. `FIRMS` and `ESA/CCI/FireCCI/5_1` queried 2026-08-14 through
Earth Engine project `thermaltwin`; cell assignment uses each region's own
`gate_inputs/reference_30m.tif` transform and the 17-pixel block of Section 3.2; populations and
predictors from the frozen `step8a_500m_modeling_dataset` tables.
