# Leave-one-scar-out: the unit that fails to transfer is the fire event

**Why this was run.** The distance reframing this project applied on 2026-08-14 was wrong, and an
adversarial review broke it. The argument had been that within-region skill decays with separation
and flattens near 0.50 by 10 to 20 km, so the cross-region points lie on the continuation of that
curve. Two objections killed it. Once the curve reaches the chance floor any cross-region mean near
0.5 lies on its continuation, so the comparison could not have come out otherwise; and six transfer
directions are below chance with interval support, which extrapolating an uninformative model does
not produce.

The referee then proposed the control that locates the real unit, and it is reported here after
independent re-derivation rather than on the referee's word.

## Design

Every burned connected component of at least 50 cells was identified with 8-connectivity on the
analysis grid. Each was held out together with all cells within a buffer of it, a model was fitted on
the rest of **the same region**, and applied to the held-out area with no refit, no recalibration and
no threshold selection. Buffers of 2, 5 and 10 km were run. The classifier, population, feature set
and preprocessing are the manuscript's primary choices throughout.

This was implemented independently of the referee's script, with a separately written component
finder and buffer, precisely because the claim it tests is large.

## Result

| Buffer | Scars | Mean AUC | Median | Range |
|---|---:|---:|---:|---|
| 2 km | 8 | **0.552** | 0.573 | 0.458 to 0.617 |
| 5 km | 8 | 0.540 | 0.539 | 0.465 to 0.602 |
| 10 km | 7 | 0.553 | 0.528 | 0.468 to 0.693 |

For comparison: blocked cross-validation at the same 5 km blocking gives a mean of 0.797; the
within-region contiguous half-split gives 0.574; and the twenty cross-region directions, at 306 to
2,802 km, give 0.541.

**Per region, 2 km buffer:**

| Region | Scars ≥ 50 cells | Source positives left | Target positives | AUC |
|---|---:|---:|---:|---:|
| Manavgat 2021 | 1 | 88 | 696 | 0.592 |
| Bejís 2022 | 1 | — | — | no usable arm |
| Muğla 2021 | 4 | 1,997 to 2,363 | 548 to 914 | 0.542 to 0.617, mean **0.579** |
| North Evia 2021 | 1 | 11 | 2,653 | 0.465 |
| Montiferru 2021 | 2 | 97 and 472 | 67 and 442 | 0.458 and 0.584 |

## Reading

**A model of this kind retains the fire it was fitted to.** Asked about a scar it has not seen, it
returns about 0.55, and the answer does not depend on whether that scar is two kilometres from its
training cells or two thousand. There is no distance decay to measure, because the skill is already
gone at the first separation this design can resolve.

That reframes the paper's transfer result. The failure is not a property of crossing a region
boundary, and it is not a property of separation distance either. **The unit that fails to transfer
is the fire event.** This unifies findings that previously stood apart: a model whose effective
footprint is one scar is a model that does not extend to the next scar 20 km away, does not extend
across a border, and whose fitted associations can point differently for a different fire.

## Limits, and they are not small

1. **Only one region supports the control cleanly.** Manavgat, Bejís and Evia each contain a single
   burned component of any size. Holding it out leaves 88, no usable arm and 11 training positives.
   Muğla, with four separate scars, is the only region where the source model is still properly
   trained, and it gives 0.579 rather than the pooled 0.552. The pooled mean is therefore carried by
   arms that are partly degenerate, and the Muğla-only figure is the more trustworthy one.
2. **Eight scars, no per-scar interval.** The means above are unweighted over a small and uneven set.
3. **The fire event is not separated from its season or its meteorology.** Each region contributes
   one fire season, so "the fire event" here bundles the event with the conditions that produced it.
   What this control does separate is the fire event from distance and from region identity, which
   were the two explanations previously on the table.
4. **Buffer radius is approximate.** A single 0.45 km figure is used for the cell, against true
   dimensions of about 0.51 km north to south and 0.39 to 0.41 km east to west, so the buffers are
   nominal rather than exact. The result is flat across 2, 5 and 10 km, so this does not matter to
   the conclusion.

## Record of the correction

This is the third framing this result has carried. It was "the relationship does not transfer between
regions", then "the failure is distance and saturates at 10 to 20 km", now "the unit that fails to
transfer is the fire event". The first was under-specified, the second was wrong and was withdrawn in
full, and the third is reported with the control that would have falsified it had it been false: a
scar held out at 2 km inside its own region scores what a scar 2,802 km away scores.
