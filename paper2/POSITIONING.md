# Paper 2: positioning

**Working title.** *Decided before the model: a preprocessing uncertainty budget for satellite
fire-susceptibility modelling across five Mediterranean regions.*

**Created 2026-08-14** in the split of the 50,462-word manuscript. Paper 1 keeps the transfer science;
this paper takes the observational layer beneath it.

---

## The thesis

> A satellite fire-susceptibility result is decided in part before any model is fitted, and the size
> of that part can be measured. Across five regions holding data, model and validation fixed, eight
> preprocessing decisions are each varied in turn. Some move the answer by more than the effect the
> literature reports; some cannot move it at all, and which is which can be read off the inputs in
> advance.

The framing that makes this publishable rather than a self-audit is the last clause. A referee's
first objection to any such paper is "these are your own pipeline's bugs". The defence is that each
axis is turned into a **rule a reader can apply to their own data**, and in two cases the rule
predicts, from the scene inventory or the land-cover fractions alone, whether the decision can matter
at all.

## Why it is not a fragment of Paper 1

Paper 1 asks whether a fitted relationship travels between regions. This paper asks what the numbers
on both sides of that question are made of. They share the cohort and the pipeline, and nothing else:
Paper 1's findings are about the predictor-response relationship, this paper's are about the
observation and its handling. Neither depends on the other's conclusions.

## Contributions

**C1. A measured budget rather than a list of caveats.** Eight preprocessing axes, each varied on the
same five regions with the same data and model, so their effects are comparable with each other and
with the reported effect size. This is the paper's structure and its main claim to usefulness.

**C2. Two decisions whose relevance is predictable in advance, at no cost.** Whether the Landsat
compositing choice can move a result at all is decided by scenes per distinct acquisition date,
which is 2.0 in two of our regions and 1.0 in the other two; where it is 1.0 the two chains produce
identical rasters and every boundary estimate is exactly zero. Whether sea contaminates a
scene-fitted dryness index is decided by the AOI's water fraction and the NDVI range the modelled
population occupies. Both are readable before any model runs.

**C3. Provenance splits that are invisible in the outputs.** The cohort's coarse thermal input is
quality-screened in two regions and unscreened in three, split by **export date rather than by
design**, and the induced change is not a uniform offset: it correlates with elevation at +0.615 in
one region. The same three unscreened regions encode sea as exact 0.0 °C, at 8.1 % and 38.3 % of
pixels in two of them and not at all in the third.

**C4. The analysis cell is not the cell it is called.** A grid built by aggregating 17 reference
pixels is square in degrees and not on the ground: 510 m north-south against 390 to 407 m east-west,
17 to 20 % smaller in area than the MODIS cell it approximates. Blocking is therefore weaker in
longitude than every block-size label suggests, and the derivation reproduces all five frozen cell
counts exactly.

**C5. What does not move the answer.** Four axes were tested and found not to threaten the result:
label agreement, label omission against an independent fire observation, gap-filled thermal cells,
and the two coordinate-bearing derived channels. Reporting these is the point of a budget rather
than a caveat list, and one of them corrects in the direction opposite to the convenient one.

**C6. A reproducibility floor.** The within-region results rebuild bit for bit on a different
operating system from released code and archived data, while cross-region point estimates carry a
±0.02 to 0.03 tolerance across library versions. Both numbers belong in the budget.

## What this paper must not claim

- That these are the eight axes that matter in general. They are the eight this design could vary.
- That any axis is shown to be harmless. Four were shown not to move *this* result, on five regions.
- That the pipeline audited here is representative. It is one pipeline, and the generalisable content
  is the rules of C2 and the provenance failure modes of C3, not the specific magnitudes.

## Target

*Environmental Modelling & Software* or *ISPRS Journal of Photogrammetry and Remote Sensing*. Both
publish protocol and uncertainty-budget work; the fire-application journals would read this as a
methods appendix.
