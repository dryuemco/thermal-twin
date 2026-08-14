# Appendix A. Sensitivity analyses

Each arm below varies one design choice and leaves everything else fixed. None changes a conclusion
in the main text. They are reported so that a reader can see which choices were tested, and what
each was worth. Arm (f) is the exception in one respect: it is not a robustness check but a test of
a claim the introduction makes, and the claim is not upheld.

**(a) Evia AOI and prevalence.** The raw transfer arms were repeated with the legacy,
high-prevalence Evia box. Every qualitative conclusion is unchanged. Thermal raw transfer AUCs move
by up to 0.07, the largest being Evia to Bejís at 0.378 to 0.448, and no direction changes side of
the chance line.

**(b) CORAL regularisation, including the canonical λ = 1.** Over nine λ values from 0 to 10⁻¹ on
four directions, CORAL transfer AUC moves by at most 0.014 within any direction and 0.008 within the
thermal family. The canonical λ = 1 of the cited method lies outside that sweep and was computed
separately on the same four directions. It changes the thermal mean from 0.519 to 0.522, a shift of
+0.003 with a per-direction range of −0.005 to +0.016, and **no direction crosses the chance line**.
The λ = 1 values are 0.510, 0.444, 0.559 and 0.575 against 0.508, 0.445, 0.564 and 0.559 at λ = 0.1.
No CORAL-dependent conclusion in this paper is sensitive to λ over the full range from 0 to 1.

**(c) Blocking scale.** Recomputing the transfer quantities at 10-cell (≈ 5 km) blocking from the
frozen per-cell predictions widens the intervals and moves the verdict counts, from ten positive,
seven negative and three uncertain at 1 km to six, four and ten at 5 km. Coarser blocking therefore
removes support from seven verdicts and adds none. Across five seeds the counts run 5 to 6 positive,
3 to 4 negative and 10 to 11 uncertain, so they are not exact.

The point estimates are unchanged. That is an identity rather than a result, and it should not be
offered as robustness. The blocking scale is the bootstrap *resampling unit*, and each point
estimate is computed once over all target cells, so no choice of block size could have moved one.
The comparison does establish two things. Every verdict that changes, changes towards "no verdict".
And no direction crosses the chance line under the widened intervals. The counts are the fragile
part of this paper. The sign pattern is not thereby shown to be robust. It is simply not tested by
this variation.

**(d) Predictor-window closure.** The predictor window was closed 7 and 14 days earlier in all five
regions. The thermal contribution stays positive and bootstrap-supported everywhere. The direction
of the change is region-specific. It strengthens in Bejís, from 0.058 to 0.079 at 14 days, and in
Muğla, from 0.115 to 0.128. It is flat in Montiferru. It weakens monotonically in Evia, from 0.156
to 0.149 to 0.135. What holds in every region is survival, not improvement. That is the claim made
in Section 5.2.

**(e) Quality screening of the coarse thermal input.** Two of the five regions' MODIS inputs are
quality-screened and three are not. The split follows export date rather than design, and it induces
an elevation-correlated change at the input, at r = +0.615 in Manavgat. Manavgat's entire downstream
chain was rebuilt from a quality-screened input. That changes the downscaled surface on 22,304 of
24,150 cells, by up to 10.9 °C. No signed univariate association moves by more than +0.0003.
Elevation is identical in both arms, at 0.374, the population is unchanged, and the
within-region increment moves from [+0.055, +0.079] to [+0.054, +0.077]. The reason is structural.
Elevation is a DEM variable the screening cannot touch, and fusion falls back on the MODIS-derived
surface across only 2.14 percentage points of coverage. Details are in
`paper/modis_qc_downstream_propagation.md`.

**(f) Normalised against absolute dryness channels.** Section 1.2 argues that an internally
normalised index should be less exposed to absolute-temperature offsets between regions than raw
land surface temperature. The thermal block contains both kinds, so the argument can be tested
directly as a feature-set contrast.

One thing should be said before the result, because it makes the outcome less surprising than it
might otherwise appear. The normalised channels are the two that hold their direction in the
same-geography two-event comparison of Section 4.8, where the absolute channels move. That is a
statement about one region across two fires. **Across regions it does not hold**: `lst_anomaly_mean`
is itself one of the two bootstrap-supported reversing predictors, reversing between Bejís and Evia,
which is why Section 4.6b drops it alongside elevation. Being internally normalised protects a
channel against the offset between two seasons in one place. It does not, on this evidence, protect
it against a change of place.

Three feature sets were run over all twenty directions and all five within-region folds, with the
classifier, population, folds and bootstrap held fixed. The harness aborts unless its reference
configuration lands on the frozen exports. It did exactly: the maximum absolute difference between
the reference arm and the frozen transfer AUCs is 0.000000 across all twenty directions.

| Feature set | Mean transfer AUC | Directions > 0.5 | Mean within-region AUC |
|---|---:|---:|---:|
| baseline only | 0.5371 | 16 | 0.7896 |
| baseline + normalised anomalies | 0.5442 | 15 | 0.8551 |
| baseline + absolute surface state | 0.5479 | 13 | 0.8564 |
| all ten features (reference) | 0.5414 | 14 | 0.8883 |

**The advantage is not found.** Per direction, the normalised set minus the absolute set has a mean
of −0.0037. It is positive in 12 of 20 directions and runs from −0.099 to +0.094, so the spread is an
order of magnitude larger than the difference. The normalised channels transfer very slightly worse
at the mean, and nothing here supports a design rule favouring anomaly-referenced dryness for
portability.

Within region the two sub-blocks are indistinguishable, at 0.8551 and 0.8564, and each recovers most
of the gap between the baseline's 0.7896 and the full model's 0.8883. What separates them in sign
stability does not become transferable skill.

This arm strengthens the negative finding rather than softening it. Four differently constituted
feature sets were tried. None clears a mean of 0.548 across regions, and all differ sharply within
them. The baseline arm also gives an independent confirmation of the control reported in
Section 4.3: its mean transfer of 0.5371 was recomputed here from the modelling datasets and matches
the 0.537 read from the frozen per-direction export. Details are in
`paper/anomaly_only_transfer.md`.

The comparison is between two sub-blocks of one thermal set on one cohort. It does not test
normalised dryness indices in general, and it does not test a normalisation fitted against a pooled
multi-region reference rather than each region's own baseline years.

**(g) The coordinate-informed channels.** `downscaled_lst_mean` and `fused_lst_mean` come from a
per-region downscaling model whose own inputs include coordinates, which Section 3.14 names as the
one route by which a coordinate-derived surface re-enters a feature set that excludes coordinates. A
coordinate-smoothed surface is by construction locally informative and non-portable, so if the
within-region increment depended on it, that increment would be this paper's own result in
miniature rather than a finding about thermal dryness. The arm was therefore run here rather than
deferred.

Both channels were dropped and everything refitted, over all twenty directions and all five
within-region folds. The reference configuration reproduces the frozen exports exactly, at
0.000000 against both the transfer and the within-region references.

| Region | Increment, full set | Increment without the two channels | Retained |
|---|---:|---:|---:|
| Manavgat 2021 | +0.067 | +0.063 | 94 % |
| Bejís 2022 | +0.056 | +0.046 | 82 % |
| Muğla 2021 | +0.116 | +0.097 | 84 % |
| North Evia 2021 | +0.153 | +0.145 | 94 % |
| Montiferru 2021 | +0.101 | +0.105 | 103 % |
| **Mean** | **+0.099** | **+0.091** | **92 %** |

**The increment does not depend on them.** It stays positive in every region and retains 82 % to
103 % of its size, rising slightly in one region. Mean transfer is likewise unchanged, at 0.545
without the two channels against 0.541 with them and 0.537 for the baseline alone. The local skill
this paper reports is therefore not an artefact of a coordinate-smoothed surface.

This arm was computed independently here and reproduces the companion paper's figure for the same
quantity, 82 % to 103 %, from a separately written harness.

## A(h). The four evaluations of Section 4.3, in full

Section 4.3 reports four evaluations of the same models as a ladder. The per-split and per-scar
detail is here, so that the ladder can be checked without leaving the manuscript.

**Table A1. Within-region half-split, every split.** Source and target positive counts are given
because they are unequal, which is the principal limit on this arm: a straight cut does not produce
two exchangeable halves. Two splits are unusable because one half of Manavgat contains no burned
cells.

| Region | Axis | Direction | Source positives | Target positives | Thermal AUC | Baseline AUC |
|---|---|---|---:|---:|---:|---:|
| manavgat 2021 | east-west | low to high | 700 | 84 | 0.695 | 0.661 |
| manavgat 2021 | east-west | high to low | 84 | 700 | 0.557 | 0.580 |
| manavgat 2021 | north-south | low to high | 0 | 784 | — | — |
| manavgat 2021 | north-south | high to low | 784 | 0 | — | — |
| bejis 2022 | east-west | low to high | 640 | 460 | 0.750 | 0.784 |
| bejis 2022 | east-west | high to low | 460 | 640 | 0.578 | 0.560 |
| bejis 2022 | north-south | low to high | 357 | 743 | 0.713 | 0.662 |
| bejis 2022 | north-south | high to low | 743 | 357 | 0.603 | 0.613 |
| mugla 2021 | east-west | low to high | 1,449 | 1,462 | 0.448 | 0.378 |
| mugla 2021 | east-west | high to low | 1,462 | 1,449 | 0.636 | 0.628 |
| mugla 2021 | north-south | low to high | 774 | 2,137 | 0.533 | 0.503 |
| mugla 2021 | north-south | high to low | 2,137 | 774 | 0.294 | 0.549 |
| evia 2021 extended | east-west | low to high | 2,052 | 612 | 0.589 | 0.506 |
| evia 2021 extended | east-west | high to low | 612 | 2,052 | 0.645 | 0.482 |
| evia 2021 extended | north-south | low to high | 2,564 | 100 | 0.649 | 0.513 |
| evia 2021 extended | north-south | high to low | 100 | 2,564 | 0.533 | 0.495 |
| montiferru 2021 | east-west | low to high | 410 | 129 | 0.475 | 0.461 |
| montiferru 2021 | east-west | high to low | 129 | 410 | 0.507 | 0.513 |
| montiferru 2021 | north-south | low to high | 438 | 101 | 0.583 | 0.511 |
| montiferru 2021 | north-south | high to low | 101 | 438 | 0.536 | 0.447 |

**Table A2. Leave-one-scar-out at a 2 km buffer, every scar.** Only Muğla contains more than one
burned component of at least 50 cells, so it is the only region where holding one out leaves the
source model properly trained. Its four arms mean 0.579; the four arms in the other regions mean
0.525, and the pooled figure of 0.552 averages the two.

| Region | Component | Source positives left | Target positives | Target cells | AUC |
|---|---:|---:|---:|---:|---:|
| evia 2021 extended | 1 | 11 | 2,653 | 3,059 | 0.465 |
| manavgat 2021 | 1 | 88 | 696 | 1,135 | 0.592 |
| montiferru 2021 | 1 | 97 | 442 | 758 | 0.584 |
| montiferru 2021 | 5 | 472 | 67 | 195 | 0.458 |
| mugla 2021 | 6 | 1,997 | 914 | 1,266 | 0.595 |
| mugla 2021 | 1 | 2,173 | 738 | 1,244 | 0.561 |
| mugla 2021 | 10 | 2,272 | 639 | 940 | 0.617 |
| mugla 2021 | 8 | 2,363 | 548 | 954 | 0.542 |

The evaluation populations of the two arms are not comparable with each other or with the transfer
targets. A held-out scar with its 2 km collar contains only fire-adjacent negatives, against a whole target
region's inclusion of its easy far field; the burned fractions, 34 to 87 % against 3.8 to 28.7 %,
are a symptom of that rather than the cause, since ROC-AUC is invariant to class balance at fixed
class-conditional distributions. The scar arm therefore asks for discrimination against the nearest and
most similar negatives only, while a transfer arm includes the whole easy far field. Section 4.3
states the consequence: the last three rows of the ladder are not distinguishable by this design.

**Table A3. The foreign-region arm, decomposed by source.** Each held-out scar area is scored with a
model fitted on each of the other four regions. Row D of Table 5 is the mean of these.

| Target region | Scar | Mean over sources | Min | Max | Spread |
|---|---:|---:|---:|---:|---:|
| Bejís 2022 | 1 | 0.589 | 0.521 | 0.631 | 0.110 |
| North Evia 2021 | 1 | 0.590 | 0.374 | 0.704 | 0.329 |
| Manavgat 2021 | 1 | 0.468 | 0.407 | 0.563 | 0.156 |
| Montiferru 2021 | 1 | 0.504 | 0.457 | 0.546 | 0.089 |
| Montiferru 2021 | 5 | 0.490 | 0.399 | 0.656 | 0.257 |
| Muğla 2021 | 1 | 0.518 | 0.425 | 0.608 | 0.183 |
| Muğla 2021 | 6 | 0.568 | 0.533 | 0.597 | 0.064 |
| Muğla 2021 | 8 | 0.632 | 0.570 | 0.724 | 0.155 |
| Muğla 2021 | 10 | 0.671 | 0.579 | 0.716 | 0.137 |

Over all 36 combinations the mean is 0.559, the range 0.374 to 0.724, and ten fall below chance. The
mean spread across the four sources for a single scar is 0.164. Averaging over sources is what makes
row D comparable with row C, which is fitted on one region; it is not a claim that the choice of
foreign source is immaterial, and Section 4.3 states the distinction.

**Table A4. Prevalence is not the cause of the evaluation-area effect.** The same fitted model and
the same out-of-fold predictions are scored three ways: on the whole region, on a random sample of
region cells drawn at the scar area's own burned fraction, and on the scar area. Twenty draws per
scar, seed 42. Nine scars, since this control needs no leave-one-scar-out arm and Bejís therefore
qualifies.

| Target region | Scar | Burned fraction | A whole region | A′ prevalence-matched | B scar area |
|---|---:|---:|---:|---:|---:|
| Manavgat 2021 | 1 | 0.61 | 0.797 | 0.796 | 0.589 |
| Bejís 2022 | 1 | 0.66 | 0.824 | 0.825 | 0.575 |
| Muğla 2021 | 6 | 0.72 | 0.777 | 0.772 | 0.564 |
| Muğla 2021 | 1 | 0.59 | 0.777 | 0.779 | 0.654 |
| Muğla 2021 | 10 | 0.68 | 0.777 | 0.779 | 0.673 |
| Muğla 2021 | 8 | 0.57 | 0.777 | 0.782 | 0.761 |
| North Evia 2021 | 1 | 0.87 | 0.864 | 0.866 | 0.745 |
| Montiferru 2021 | 1 | 0.58 | 0.720 | 0.717 | 0.622 |
| Montiferru 2021 | 5 | 0.34 | 0.720 | 0.723 | 0.461 |
| **Mean** | | | **0.782** | **0.782** | **0.627** |

A minus A′, the effect of prevalence alone, is **−0.000 [−0.003, +0.002]**. A′ minus B, the effect of
replacing the region's negatives with fire-adjacent ones, is **+0.155 [+0.093, +0.217]**. The
evaluation-area effect is entirely the negative pool.
