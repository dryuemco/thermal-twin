# Skill against separation distance: is the transfer failure regional, or is it just distance?

**Why this was run.** The positive control (`positive_control.md`) showed that skill falls from about
0.86 to about 0.57 without leaving a region, as soon as the held-out area is contiguous rather than
interleaved. That left the paper's central attribution confounded: the failure was being called
*regional* when spatial extrapolation alone might explain it. This separates the two as far as the
design allows.

Run 2026-08-14. Script `distance_curve.py`, result `distance_curve.json`.

## Design

**Within region.** Each region is cut in half by a straight line, a model is fitted on one half and
applied to the other with no refit. Because the cut is a straight line, a target cell's distance to
the nearest training cell is exactly its distance to that line. Target cells are binned by that
distance and an AUC is computed per bin. One fitted model per split serves every bin, so the curve is
not confounded by refitting. Both axes, both directions, five regions, 55 usable bins.

**Across regions.** The twenty frozen transfer AUCs are placed at the geodesic distance between AOI
centroids, computed from the bounding boxes in `core/regions.py`.

## Result

**Within-region skill decays with separation and then flattens.**

| Separation | Bins | Mean AUC | Min | Max |
|---|---:|---:|---:|---:|
| 0 to 5 km | 18 | **0.692** | 0.345 | 0.893 |
| 5 to 10 km | 16 | 0.519 | 0.295 | 0.775 |
| 10 to 20 km | 11 | 0.499 | 0.250 | 0.851 |
| 20 to 40 km | 6 | 0.445 | 0.187 | 0.611 |
| 40 to 80 km | 3 | 0.541 | 0.454 | 0.592 |
| 80 to 160 km | 1 | 0.421 | — | — |

**Cross-region transfer, at 306 to 2,802 km, has a mean of 0.541 and a range of 0.326 to 0.686.**

## Reading

**The cross-region points sit on the continuation of the within-region curve, not below it.** By
10 to 20 km inside a single region the model is already at 0.499. At 20 to 40 km it is at 0.445.
Crossing a national border and going a hundred times further does not make it worse: the twenty
cross-region directions average 0.541, which is at or slightly above the within-region plateau.

That has a sharp consequence for how this paper's central result should be stated. **The failure is
not a property of moving between regions.** It is a property of moving away from the training cells
at all, and it saturates by about 10 to 20 km. After that, distance stops mattering, because there is
almost nothing left to lose.

**This makes the finding stronger, not weaker.** "A model of this kind does not generalise beyond
about ten kilometres, and a region boundary adds nothing to that" is a more general claim than "it
does not transfer between regions", it is better supported, and it is more useful to a practitioner,
who now has a length scale rather than a taxonomy.

**What is untouched.** The sign-reversal evidence is univariate and involves no fitted model, so
nothing here bears on it. Nor does it bear on the diagnostics result, which correlates diagnostics
against observed transfer whatever produces that transfer.

## Limits, stated plainly

1. **The two distance ranges do not overlap.** Within-region separations span 2 to 86 km; the
   cross-region separations start at 306 km. The comparison is therefore an extrapolation of the
   within-region curve rather than an interpolation between measured points. It is a safer
   extrapolation than it would otherwise be, because the curve has already flattened before the gap
   begins, but it is still an extrapolation.
2. **The far bins are thin.** Six bins at 20 to 40 km, three at 40 to 80, one beyond. Their means
   should not be read to three decimals, and the apparent rise at 40 to 80 km is not evidence of
   anything.
3. **The near bins are inflated by autocorrelation.** Cells within 5 km of the training half are
   spatially adjacent to training data, which is exactly the inflation that spatially blocked
   validation exists to remove. The 0.692 is an upper bound on honest near-field skill, not an
   estimate of it.
4. **Distance is not the only thing that changes with distance.** Moving across a region also moves
   across land cover, terrain and fire history. This design does not separate distance from what
   covaries with it; it separates distance from *crossing an AOI boundary*, which is the specific
   confound the positive control exposed.
5. **Centroid distance is a crude summary for large AOIs.** Muğla spans about 160 km, so the
   centroid-to-centroid figure understates the separation for some cell pairs and overstates it for
   others.

## What should follow in the manuscript

Contribution 1 currently attributes the failure to region change. On this evidence it should
attribute it to spatial extrapolation, with region change as the limiting case rather than the
cause, and the paper should report the length scale at which skill is lost. That is a change of
claim, not of numbers: every transfer figure in the paper stands exactly as reported.
