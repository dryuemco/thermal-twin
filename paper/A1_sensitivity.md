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
+0.003 with a per-direction range of −0.005 to +0.016, and none of those four directions crosses the
chance line. The λ = 1 values are 0.510, 0.444, 0.559 and 0.575 against 0.508, 0.445, 0.564 and
0.559 at λ = 0.1.

**Those four directions are Bejís–Muğla and Manavgat–Muğla, and they exclude the pair that moves.**
An earlier version of this appendix generalised from them to the whole matrix, which was an error:
the Manavgat–Bejís pair is not in the sweep and it is the pair whose CORAL result is λ-dependent. A
separate frozen artefact, `experiments/cross_region/step10/coral_lambda_sensitivity.csv`, carries it.
Bejís to Manavgat gives 0.5571 [0.5292, 0.5857] at λ = 10⁻⁵, 0.5644 at λ = 10⁻³ and 0.5473 at
λ = 0.1, all with intervals entirely above 0.5, but **0.4850 [0.4496, 0.5197] at λ = 1**, which
crosses the chance line and loses its interval support. Manavgat to Bejís falls likewise, from
0.5108 to 0.4776 [0.4501, 0.5013].

The correct statement is therefore narrower. CORAL-dependent conclusions are insensitive to λ over
three orders of magnitude below 0.1; at the cited method's canonical λ = 1 the one direction whose
adapted interval sits entirely above chance loses that status. λ = 10⁻⁵ is the minimally regularised
choice and matches the reference implementation, but the dependence is real and is reported rather
than absorbed.

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
same-geography two-event comparison of Appendix A(m2), where the absolute channels move. That is a
statement about one region across two fires. **Across regions it does not hold**: `lst_anomaly_mean`
is itself one of the two predictors whose reversal is bootstrap-supported on the frames as drawn,
reversing between Bejís and Evia (Section 4.4 withdraws that support under an equalised frame),
which is why Appendix A(n2) drops it alongside elevation. Being internally normalised protects a
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
Section 4.5: its mean transfer of 0.5371 was recomputed here from the modelling datasets and matches
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

**(h) Model capacity.** Every number in this paper comes from one random forest with unlimited
depth and `min_samples_leaf = 3`. That is the configuration most able to encode local structure and
least able to extrapolate, so a reader may reasonably ask whether the transfer failure is a property
of the predictors or of the estimator. Holding the model fixed is right for the internal comparisons
and does not license the external claim, so three further estimators were run over the same twenty
directions and the same five within-region folds.

| Estimator | Within-region AUC | Within increment | Transfer AUC | Transfer increment | Above chance |
|---|---:|---:|---:|---:|---:|
| Random forest, depth unlimited, leaf 3 | 0.888 | +0.099 | 0.541 | +0.004 | 14 of 20 |
| Random forest, depth 6, leaf 50 | 0.829 | +0.055 | **0.556** | −0.007 | 14 of 20 |
| Random forest, leaf 200 | 0.805 | +0.047 | **0.550** | −0.021 | 14 of 20 |
| Penalised logistic regression | 0.741 | +0.045 | **0.510** | −0.024 | 14 of 20 |

**Regularisation does not rescue transfer.** All four estimators land between 0.510 and 0.556, all
four put exactly fourteen of twenty directions above chance, and the linear model, the one built to
extrapolate, transfers worst. Within-region skill falls as capacity is reduced, from 0.888 to 0.741,
which is what regularisation is expected to cost; transfer does not rise to meet it. The thermal
block's contribution to transfer is +0.004 under the canonical forest and **negative** under all
three regularised alternatives, so the block does not become portable when the model is made simpler.

The transfer failure is therefore a property of the predictors on this cohort, not of an
unregularised forest. Detail in `paper/model_capacity.json`.

## A(i). The four evaluations of Section 4.3, in full

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

**Table A2. Leave-one-scar-out at a 2 km buffer, every scar.** Muğla and Montiferru are the only
regions containing more than one burned component of at least 50 cells. Muğla is the only region
where holding one out still leaves the source model properly trained across every arm; Montiferru's
two components are very unequal, so one of its arms retains 472 source positives and the other 97.
Muğla's four arms mean 0.579; the four arms in the other regions mean 0.525, and the pooled figure of 0.552 averages the two.

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
model fitted on each of the other four regions. Table 2's row D is the mean over the **eight** scars that carry a row C, that is 32 of the 36
combinations below; the nine-scar mean quoted in this appendix is 0.559 against row D's 0.555.

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

Over all 36 combinations here the mean is 0.559, the range 0.374 to 0.724, and ten fall below
chance. Restricted to the 32 combinations behind row D the mean is 0.555 and the same ten fall below
chance. The mean spread across the four sources for a single scar is 0.164 over the nine scars and
0.171 over the eight. Averaging over sources is what makes
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

## A(j). The transfer-gap decomposition, in full

Section 4.5 states the two figures this table carries — at most 34 % of the gap recovered in the
directions that started below chance, and seven directions with negative recovery. The table is
kept here rather than in the body because Section 4.3 shows the within-region reference in its
denominator is not matched to a transfer evaluation, and Section 4.4 shows its raw column is
frame-dependent, so the fractions should be read as within-protocol quantities.

**Table A5. Transfer-gap decomposition (four-AOI set, 12 directions).** Within = target's
within-region thermal AUC; best adapted = the better of z-score/CORAL; recovered fraction = (adapted
− raw)/(within − raw), signed and unclipped, with paired bootstrap CI (1000 replicates). Montiferru
directions are not part of this decomposition (per-pair absolute decompositions exist without
fraction CIs). The status column asks whether the *adapted* value clears chance and uses the 2-cell
adapted intervals of Table B9. The adapted arms were not recomputed at the coarser blocking of
Appendix A(c), which covers the raw arm and the paired delta only.

| Direction | Within | Raw | Best adapted (method) | Recovered fraction [CI] | Status |
|---|---|---|---|---|---|
| Manavgat→Bejís | 0.918 | 0.326 | 0.511 (CORAL) | +0.31 [+0.28, +0.34] | recovery, chance not excluded |
| Bejís→Manavgat | 0.870 | 0.444 | 0.555 (CORAL) | +0.26 [+0.18, +0.34] | recovery above chance |
| Muğla→Manavgat | 0.870 | 0.401 | 0.560 (CORAL) | +0.34 [+0.28, +0.40] | recovery above chance |
| Bejís→Evia | 0.912 | 0.383 | 0.532 (z-score) | +0.28 [+0.23, +0.32] | recovery above chance |
| Evia→Bejís | 0.918 | 0.448 | 0.549 (z-score) | +0.22 [+0.16, +0.27] | recovery above chance |
| Manavgat→Muğla | 0.859 | 0.470 | 0.443 (CORAL) | −0.07 [−0.12, −0.03] | **negative recovery** |
| Muğla→Bejís | 0.918 | 0.583 | 0.560 (CORAL) | −0.07 [−0.16, +0.01] | **negative recovery** |
| Manavgat→Evia | 0.912 | 0.613 | 0.542 (z-score) | −0.23 [−0.32, −0.14] | **negative recovery** |
| Evia→Manavgat | 0.870 | 0.686 | 0.527 (CORAL) | −0.86 [−1.18, −0.60] | **negative recovery** |
| Evia→Muğla | 0.859 | 0.577 | 0.530 (CORAL) | −0.17 [−0.22, −0.11] | **negative recovery** |
| Muğla→Evia | 0.912 | 0.653 | 0.563 (CORAL) | −0.35 [−0.43, −0.27] | **negative recovery** |
| Bejís→Muğla | 0.859 | 0.618 | 0.518 (z-score) | −0.42 [−0.51, −0.34] | **negative recovery** |

## A(k). The thermal sign, stratified

Section 4.4 reports that all five regions agree on a negative association between pre-fire surface
temperature and burning, and that neither of the two obvious confounders explains it. The
per-region values are here. Signed AUC against `burned` within the 10 km collar; stratified columns
pool within-stratum concordance over deciles of the named variable, weighting each stratum by its
positive-negative pair count. Source `matched_frame_gap.csv`, recomputable by
`paper/code/verify_matched_gap.py`.

| Region | LST raw | LST within elevation | LST within NDVI | LST within distance | NDVI raw | NDVI within LST |
|---|---:|---:|---:|---:|---:|---:|
| Manavgat | 0.386 | 0.402 | 0.440 | **0.505** | 0.621 | 0.542 |
| Bejís | 0.405 | 0.509 | 0.486 | 0.350 | 0.618 | 0.574 |
| Muğla | 0.332 | 0.363 | 0.404 | 0.367 | 0.652 | 0.547 |
| Evia | 0.286 | 0.327 | 0.279 | 0.319 | 0.663 | **0.380** |
| Montiferru | 0.376 | 0.392 | 0.368 | **0.485** | 0.582 | **0.405** |

Three readings follow. The LST sign survives stratification within elevation in four of five regions
and within greenness in all five, despite r(LST, NDVI) reaching −0.92, so it is neither a lapse-rate
proxy nor an inverse-greenness proxy. It does *not* survive stratification within distance to the
nearest burned cell in Manavgat or Montiferru, which are the two regions where the collar leaves the
least residual gradient, so in those two the agreed sign is a weaker version of the same spatial
effect the collar was introduced to remove. And the reciprocal adjustment runs one way only: NDVI
reverses in two regions once temperature is held, while LST reverses in none once greenness is held.

## A(l). The LST anomaly under the difference instrument

Section 4.4 reports that no reversal meets this paper's strict criterion once evaluation frames are
equalised, and that the LST anomaly nonetheless differs between regions on the weaker instrument
Table B3's note commits the paper to. These are the four pairs that have opposite-sided point
estimates and a difference interval excluding zero, all on `lst_anomaly_mean`. Signed AUC within the
10 km collar; the two regions are bootstrapped independently under the 10-cell spatial-block scheme
and differenced, 1000 replicates, seed 42. Source `matched_frame_gap.csv`, recomputable by
`paper/code/verify_matched_gap.py`.

**Table A6. Between-region differences in the signed LST-anomaly association, 10 km collar.**

| Pair | AUC A | AUC B | Difference | 95 % CI |
|---|---:|---:|---:|---|
| Bejís vs Evia | 0.392 | 0.584 | −0.191 | [−0.295, −0.083] |
| Evia vs Montiferru | 0.584 | 0.400 | +0.184 | [+0.012, +0.321] |
| Manavgat vs Evia | 0.462 | 0.584 | −0.122 | [−0.225, −0.020] |
| Bejís vs Muğla | 0.392 | 0.507 | −0.115 | [−0.219, −0.002] |

Nine of the ninety feature-by-pair differences clear zero, against about 4.5 expected at nominal 5 %
under the null, and no multiplicity correction is applied; four of the nine are this feature and
three of those involve Evia. The nine features are effectively two to three dimensions (Section 4.4), so the ninety comparisons are not independent either. This is reported as a weaker result
than a reversal, not as a restored one.

## A(m). The same-geography event pair

Appendix A(m2) states the result and its withdrawal; the design, the two structural asymmetries that
have no analogue in the twenty-direction matrix, and the direction of the bias they impose are here.


This arm was designed to hold place fixed and vary only the fire, which would have separated
regional concept shift from everything that differs between study areas. Muğla burned twice, in 2021
and again eleven months later, on the same grid and through the same processing chain, and the 2022
arm is the 2021 population with the 2021 scar removed: 41,730 rows / 2,911 burned for 2021 against
38,790 rows / 331 burned for 2022. **Positive-carrying 5 km blocks: 70 for the 2021 arm and 11 for
the 2022 arm**, and eleven is below the sixteen this design sets as its own floor, so the 2022
intervals are read as indicative exactly as the 20-cell row of Table 1 is. Full per-feature values are in Appendix B, Table B5.

**On the frame as drawn, elevation reverses with bootstrap support.** In 2021 higher ground burned
preferentially, at 0.611 [0.532, 0.690]; in 2022 lower ground did, at 0.296 [0.230, 0.355]. The
intervals are disjoint and the difference is −0.317 [−0.414, −0.220]: the same predictor, region and
grid, and an association pointing the opposite way in two fires eleven months apart. The four
absolute thermal channels change side as well.

**Section 4.4 has already withdrawn it.** The 2022 arm is one compact scar inside the whole Muğla box, so
93.2 % of its cells lie beyond 10 km of any burned cell against 55.3 % for the 2021 arm — the most
extreme far field in the cohort. Under the same 10 km collar the 2021 figure barely moves, 0.611 to
0.606 and still supported, while the 2022 figure moves from 0.297 to 0.565, onto the same side of
0.5 as 2021 with an interval covering chance. The arm shows the same artefact as the cross-region
reversals rather than confirming them. We keep the section because the structural properties below
have no analogue elsewhere in the paper, and because this arm is what motivated the frame test.

The two arms are not disjoint samples: they share 38,789 of the 2022 arm's 38,790 cells, and
elevation, slope and land cover are identical to the digit across all 73,098 grid cells, so only
NDVI and the six thermal channels carry new information between them. And the removal is the
target's own positive class, so in the 2022-to-2021 direction not one target positive is in the
source training population while 38,789 of 38,819 target negatives are, and membership of the source
training set alone separates the 2021 target's classes at ROC-AUC 0.9996. **We therefore cannot
bound what that asymmetry does to a transfer estimate between the two arms.** The known part of the
bias runs the safe way: the removed cells are high, with a median of 563 m against the population's
lower centre, so removing them strips high negatives from the 2022 arm and makes the observed
reversal smaller rather than larger.

## A(n). The two interventions, in full

Appendix A(n2) states both results; the four feature-set configurations, the per-region deltas and the
pooled per-target shortfalls are here.


**(a) Pooled multi-region training** (Fig. 6). At the point estimate, training on the pooled primary
populations of the other four regions never beats the best single-source transfer for any target,
with shortfalls of 0.02 to 0.22, and it stays 0.28 to 0.50 AUC below the within-region ceiling; for two targets it falls below the pairwise mean and below chance, though
only Bejís is below chance with interval support, at 0.417 [0.369, 0.467]. Aggregation does not recover what single-source
transfer loses.

**(b) Removing the direction-reversing features.** The two predictors whose signed association
reverses between regions **with bootstrap support on the frames as drawn** are **`elevation_mean` and
`lst_anomaly_mean`**. Section 4.4 withdraws that support under an equalised frame, so this selection
rule is frame-dependent and the arm below measures what the removal costs under the original
protocol, not a consequence of an established reversal.
The per-region signed associations and the three pair-level reversals that meet that criterion are in
Appendix B, Tables B2 and B3. Retraining without them
costs **−0.081** of mean within-region AUC, supported in every region (per-region deltas −0.060,
−0.130, −0.074, −0.063, −0.079, every interval entirely below zero), and changes mean transfer by
**+0.014 [−0.017, +0.045]**, which spans zero.

Two qualifications belong with those numbers rather than after them. First, the debit is not the
thermal block's. Dropping elevation alone accounts for −0.061 of it, from 0.888 to 0.827. Dropping
the LST anomaly alone accounts for −0.013, from 0.888 to 0.875. Roughly three quarters of the cost
is therefore the removal of a **baseline** terrain variable, not of a thermal channel. Second, both
figures are post-selection. The two predictors were chosen because they reverse, using the same data
on which the −0.081 and the +0.014 are then estimated. No correction for that selection is applied.

| Configuration | Mean within-region AUC | Mean transfer AUC |
|---|---|---|
| full | 0.888 | 0.541 |
| drop `elevation_mean` | 0.827 | 0.546 |
| drop `lst_anomaly_mean` | 0.875 | 0.544 |
| drop both | 0.807 | 0.556 |

Figure 7 shows the four configurations together. What this measures is a local cost with no
compensating transfer gain. It does not measure an
exchange, because the transfer side is a null on both arms. The thermal block's own contribution to
transfer is +0.004, with an interval spanning zero (Section 4.5). Removing the reversing predictors
returns +0.014, with an interval spanning zero. Two nulls on the portability axis are not a price
paid.

## A(o). The thermal sign and the anomaly difference, in full

Section 4.4 states both results; the per-region values, the reciprocal stratification and the
difference-instrument argument are here.

**A weaker instrument does support the anomaly result.** Table B3's note commits this paper to a
difference interval on the pair as the sharper test, and it is applied here. Bootstrapping the two regions independently under the collar and differencing,
four pairs have opposite-sided point estimates **and** a difference interval excluding zero, all on
`lst_anomaly_mean` and three of the four involving Evia — the largest being Bejís against Evia at
−0.191 [−0.295, −0.083] (Appendix A(l), Table A6). The anomaly is the one channel the
frame-and-terrain mechanism of this section cannot explain, being decorrelated from elevation.
Three caveats keep it weak and all three are stated rather than buried: nine of ninety
feature-by-pair differences clear zero against about 4.5 expected under the null with no
multiplicity correction; the nine features are effectively two to three dimensions, as the
collinearity paragraph below shows; and Evia's own interval-support status turns on 0.003. **The
honest statement is that no reversal meets this paper's strict criterion under the collar, and that
the LST anomaly differs between regions on the weaker difference instrument.** We state it that way
because the alternative would be to apply a looser standard to the arm that supersedes Table B3 than
to Table B3 itself. Elevation under the collar is above 0.5 in all five regions but individually
supported in only two, Muğla at 0.606 [0.525, 0.685] and Evia at 0.648 [0.550, 0.740].

**The sign the five regions agree on is not the one the dryness framing predicts.** For LST the
common direction is *below* 0.5 in every region, at 0.386, 0.405, 0.332, 0.286 and 0.376: a hotter
pre-fire surface is associated with **less** burning, and the same holds for TVDI. It is not a
lapse-rate artefact and it is not greenness acting through fuel load. On mutual adjustment the
surviving channel is LST, not NDVI: holding NDVI, LST never reverses in any region, while holding
LST, NDVI's own association reverses in Evia and Montiferru. Greenness is therefore not the mechanism. Two caveats bound what the sign is: in Manavgat and
Montiferru it is a residual spatial gradient that disappears when distance to the nearest burned cell
is stratified within the collar, and interval support is not uniform, LST being supported in four of
five regions and TVDI in three, so "all five agree" is a statement about point estimates. What we can
defend is that the absolute thermal channels behave here as **static land-surface descriptors**
rather than as a dryness index, and that the two internally differenced channels carry no consistent
cross-region direction at all. Compositing depth was not tested and remains an open alternative.
Per-region stratifications are in Appendix A(k), and Section 5.2 states the consequence for the
moisture-stress motivation of Section 1.2.

**The same-geography arm of Appendix A(m2) is the most extreme case in the cohort, and it does not
survive either.** A fixed study area does not mean a fixed evaluation frame: its 2022 arm has
**93.2 % of cells beyond 10 km of any burned cell, median 43.6 km**, a larger far field than any
cross-region arm. Applying the same
collar (`mugla_two_event_collar.csv`; the full-frame values reproduce Table B5):

| Muğla arm | share beyond 10 km | full frame | 10 km collar |
|---|---:|---|---|
| 2021 | 55.3 % | 0.611 [0.529, 0.692], supported | 0.606 [0.525, 0.685], supported |
| 2022 | **93.2 %** | 0.297 [0.229, 0.363], supported | **0.565 [0.450, 0.677], not supported** |

The 2022 arm moves to the **same side of 0.5** as the 2021 arm and its interval covers chance, while
the 2021 arm is nearly frame-invariant, which isolates the effect to the 2022 arm's far field rather
than to the collar. **No bootstrap-supported sign reversal survives anywhere in this paper once
evaluation frames are equalised**, between regions or between two fires in one region.

Two points bound how many independent reversals could have been counted in the first place. The
channels whose reversal vanishes are the ones partly measuring terrain: current LST correlates with
elevation at −0.695 to −0.125 across the regions and TVDI at −0.722 to −0.298, so their proxy
strength varies fivefold and a frame that shifts the elevation distribution shifts them with it. And
within the collar `fused_lst_mean` correlates with `current_lst_mean` at 0.99 to 1.00,
`downscaled_lst_mean` at 0.97 to 0.99 and `current_tvdi_mean` at 0.87 to 0.98, so the four absolute
channels are close to one axis and the two differenced channels correlate at 0.64 to 0.94: the "five
of nine directions reverse" count of Appendix A(s) counts features, not independent quantities, and
**in effective dimensions it is closer to two**.

Two scope statements belong with the table. The full-frame values here are not numerically the
published ones — ρ = +0.86 over fourteen directions against the +0.84 over sixteen in Section 4.6 —
because the support test is itself bootstrap-dependent and at this setting three region pairs carry
no jointly supported feature rather than two; the argument rests on before-and-after under identical
settings, not on the published figure. And **only these diagnostics were recomputed on the collar**:
the other eighteen failed on the frames as drawn and were not rerun, so their correlations against
the equalised transfer vector are unknown rather than shown to be null.

**The thermal block's paired contribution to transfer, with its interval.** The two matrices were
differenced direction by direction. The mean is **+0.004**, but the mean is not the informative
statistic here. The individual paired contributions span **−0.148 to +0.133**, with **twelve
positive and eight negative** (`baseline_vs_thermal_transfer.csv`). The spread is thirty times the
mean, and the sign is not a property of the block but of the pair it is asked to cross: the same six
predictors that add +0.133 in one direction subtract 0.148 in another. A mean near zero here records
cancellation, not consistent absence of effect. The directions are not independent,
because each region appears in eight of the twenty. The interval therefore depends on what is
treated as the resampling unit. All four units the design permits give the same answer:

| Resampling unit | n | 95 % interval on the mean paired contribution |
|---|---:|---|
| Directions, naive | 20 | [−0.027, +0.034] |
| Unordered pairs, cluster bootstrap | 10 | [−0.028, +0.036] |
| Unordered pairs, t on pair means | 10 | [−0.034, +0.042] |
| Regions, leave-one-out jackknife | 5 | [−0.037, +0.046] |

Every interval spans zero, and the point estimate is a small fraction of each width. The per-region
jackknife shows how little the mean is anchored. Holding out Manavgat, Bejís, Muğla, Evia and
Montiferru in turn gives +0.0148, +0.0021, +0.0065, **−0.0081** and +0.0060. **Dropping Evia alone
reverses the sign of the headline.** None of these four units propagates within-direction sampling
variability. They resample between directions only.

**In precision terms the transfer is worse than the ROC figures suggest.** ROC-AUC is the metric
used throughout this paper, for comparability with the literature, but a susceptibility surface is
used as a ranked area budget, so precision-recall is the operational quantity. Across the twenty
directions the thermal model's PR-AUC averages **0.156 against a no-skill baseline of 0.136**. The
mean of the twenty per-direction lifts is 1.16; the ratio of the two means just quoted is 1.146.
**Six of the twenty fall below their own no-skill baseline at the point estimate, and five of those
six have intervals entirely below it.** The exception is Bejís to Manavgat, at 0.034 [0.029, 0.042]
against a baseline of 0.038, whose interval covers the baseline and which is therefore a
point-estimate case only. Only one direction, Evia to Manavgat, exceeds twice its baseline, at 0.094
against 0.038. A transferred model therefore ranks burned cells about a sixth better than random on
average, and worse than random in five directions with interval support and a sixth at the point. This is a
sharper statement than the ROC means support and it should be the one a practitioner reads.

**The within-region increment survives the same correction, and is reported here because Section 4.2
establishes it on the frames this section calls incomparable.** Running the baseline arm on the
collar as well (`collar_increment_and_cosine.csv`, `paper/code/verify_collar_increment.py`), the
thermal increment at 5 km blocking is +0.041, +0.030, +0.091, +0.134 and +0.090 across the five
regions, **positive in all five**, with a mean of +0.077 against +0.086 on the frame as drawn. It
does erode as the frame tightens further: at a 5 km collar the mean halves to +0.041, still positive
in all five. These are point estimates; the intervals in Table 1 are computed on the frame as drawn.
The paper's one surviving predictor-level positive claim therefore holds on the frame it argues is
the correct one.

**The five areas of interest are not comparable frames.** Each region is a rectangle drawn around a
fire, and the rectangles differ by an order of magnitude in how much unburnt far field they enclose.

The share of modelled cells lying beyond 10 km of any burned cell is 60.1 % in Manavgat, 63.1 % in
Bejís, 55.3 % in Muğla, 43.7 % in Evia and **2.1 %** in Montiferru, with median distances of 13.4,
13.5, 11.3, 8.0 and 2.7 km (Appendix B, Table B6). Montiferru's frame is fire-scale; Manavgat's and Bejís's are roughly three-fifths far field. The
far field is not a neutral addition. In Manavgat the median elevation of modelled cells rises from
472 m within 5 km of the fire to 955 m at 10 to 20 km and 1,273 m at 20 to 50 km, against 512 m for
the burned cells themselves, in Taurus terrain that no plausible spread model would place at risk.

## A(s). The contrast pair, in full

The clearest single view needs no ranking at all (Fig. 8). Manavgat and Muğla lie in the same
country and fire year, 306 km apart by centroid, and their burned cells occupy the most similar
environmental envelope of any pair in the matrix; Bejís and Montiferru occupy the least similar.

Per-quantity values for both pairs, on both frames, are in Appendix B, Table B10.

Two readings of this pair do not survive Section 4.4 and are not offered. On the frames as drawn
five of nine feature-response directions point opposite ways, elevation among them; under the collar
that figure moves to 0.561 against 0.606, on the same side of 0.5. And transfer is below chance in
both directions as drawn but above chance under the collar. **What survives is the ordinal
contrast**: the most similar pair is among the weakest in the matrix and the least similar among the
stronger, while neither is the extreme — the weakest direction is Manavgat to Bejís at 0.417 and the
strongest Muğla to Evia at 0.727. The claim this supports is that high envelope overlap does not buy
transfer, not that it produces anti-prediction. The AoA shares are full-frame quantities.

Bejís and Montiferru sit at the opposite extreme. Their burned envelopes barely overlap, and they
carry the most dissimilar values on every overlap measure. They transfer above chance in both
directions. That half of the contrast rests on point estimates: neither direction carries a verdict
at 5 km blocking, and the marginal applicability audit was never produced for Montiferru. The claim
is one of *sufficiency*. Similarity does not guarantee transfer, and dissimilarity does not preclude
it. The claim rests on two coexisting counterexamples, so it does not depend on the number of pairs
available.

## A(n2). Interventions, in full

Two interventions were pre-registered. **Pooling** four regions into one training set does not
recover what single-source transfer loses: every pooled target still falls short of its own
within-region reference, and only Bejís is below chance with interval support. **Removing the two
predictors whose signed association reverses** costs −0.081 of mean within-region AUC, supported in
every region and roughly three quarters of it attributable to elevation, a *baseline* terrain
variable, and returns +0.014 [−0.017, +0.045] on transfer, whose interval spans zero. A local cost
is measured; no compensating transfer gain is, so no exchange between the two is demonstrated. Both
predictors were chosen because they reverse, using the same data on which the two figures are then
estimated, and no correction for that selection is applied; Section 4.4 additionally withdraws the
support for the selection rule itself. Per-configuration values are in Appendix A(n).

## A(v). The sensitivity arms, summarised

Eight design choices were varied with everything else held fixed. They are the Evia AOI and its
prevalence, the CORAL regularisation constant, the blocking scale, the closure date of the predictor
window, the quality screening of the coarse thermal input, the contrast between the normalised and
the absolute dryness channels, the removal of the coordinate-informed channels, and the capacity of
the classifier. None changes a conclusion above. Two
bound how the results should be read, so they are carried into the main text here.

Coarsening the blocks from 1 km to 5 km moves the **paired thermal-minus-baseline delta** verdicts
from ten positive, seven negative and three uncertain to six, four and ten. The above-chance
verdicts on the thermal arm itself, a different quantity, move from twelve, six and two to nine,
four and seven. Support is removed from seven verdicts and added to none.
The point estimates are unchanged, but that is an identity rather than a result. The blocking scale
is the resampling unit, and it cannot move an estimate computed once over all target cells.

Manavgat's whole downstream chain was then rebuilt from a quality-screened MODIS input. That changes
the downscaled surface on 22,304 of 24,150 cells, by up to 10.9 °C. No signed univariate association
moves by more than +0.0003. This closes the one processing-artefact candidate for that region's
behaviour. Appendix A reports all eight arms, including one that tests a claim of Section 1.2 and does not uphold it.

## A(m2). The same geography, a second fire

Muğla burned twice, eleven months apart, on the same grid and through the same processing chain.
The arm was designed to hold place fixed and vary only the fire, which would have separated regional
concept shift from everything else that differs between study areas. On the frame as drawn it shows
a bootstrap-supported elevation reversal between the two fires; Section 4.4 withdraws that, because
the 2022 arm carries the largest far field in the cohort and under a 10 km collar the two arms fall
on the same side of 0.5. The arm, its structural asymmetries and the direction of the bias they
impose are in Appendix A(m).

## A(t). Distance within a region

One further arm measures how skill decays with distance inside a single region. A model is fitted on
one half of a region and applied to the other, and target cells are binned by their distance from the
training cells (`distance_curve.md`, `paper/code/distance_curve.py`). Means are unweighted over bins,
whose positive counts range from 1 to 2,564, and the bins carry no intervals.

| Separation from training cells | Bins | Mean target AUC |
|---|---:|---:|
| 0 to 5 km | 18 | 0.692 |
| 5 to 10 km | 16 | 0.519 |
| 10 to 20 km | 11 | 0.499 |
| 20 to 40 km | 6 | 0.445 |
| 40 to 80 km | 3 | 0.541 |
| 80 to 160 km | 1 | 0.421 |
| cross-region, 306 to 2,802 km | 20 | 0.541 |

**By 10 to 20 km inside a single region the model is already at chance.** That bounds how far a
susceptibility surface of this kind can be carried from the cells it was fitted on, and it is
consistent with Section 4.3, where withholding a scar and replacing the model with a foreign one cost
nothing distinguishable.

**It does not reframe the paper's negative result, and a reading that it does was considered and
rejected.** That reading argued that because the twenty cross-region directions average 0.541, at or
above the within-region plateau, they sit on the continuation of the curve and the failure needs no
regional mechanism — a rule fixed in advance in `positive_control.md`. Two objections defeat it, and
`scar_control.md` records the reframing as withdrawn in full. **The rule cannot fail**: once the
curve reaches the chance floor, any cross-region mean near 0.5 lies on its continuation by
construction, so the comparison could not have come out otherwise, and a test that cannot fail is not
evidence. And **extrapolating an uninformative model does not produce a reliably reversed ranking**:
Manavgat to Bejís is below chance with interval support on the frame as drawn and at the 10 km
collar, which is not what a model that has merely run out of skill returns.

Four limits bound even the descriptive reading. The two distance ranges do not overlap — within-region
separations span 2 to 86 km, cross-region separations start at 306 km — so any comparison across the
gap extrapolates the curve. The far bins are thin, six at 20 to 40 km and one beyond 80 km, so their
means should not be read closely and the apparent rise at 40 to 80 km is not evidence of anything.
The near bins carry exactly the autocorrelation blocked validation exists to remove, so **0.692 is an
upper bound on near-field skill rather than an estimate of it**. And this design separates distance
from crossing a study-area boundary, but not from the land cover, terrain and fire history that
covary with it.

The arm therefore contributes a length scale for the within-region decay, not an attribution. The
unit that fails to transfer is not established by this design, and Section 4.3 says so directly.

## A(u). What target labels cost

Everything above measures a failure; this prices it. Label-free alignment does not close the residual
gap, so the missing resource is information about the target that alignment cannot synthesise, and
the direct way to supply it is target labels. A frozen labelled-budget diagnostic answers how many, for
three regions across all six ordered directions, using one 10-cell (~5 km) spatial block as the unit
of labelling effort and reading recovery against a matched target-only ceiling of 0.777 to 0.824.

Thirty-two labelled blocks recover **85 to 89 % of that ceiling in three of the six directions**, two
of which started below chance; 51 to 57 % in two more, the directions where the conditional gap is
widest; and 30 % in the sixth. That budget is 7 to 20 % of the target's natural-vegetation
population, which at the 2,700 to 3,000 labelled cells those blocks carry (S1.3) and this grid's
effective cell area of 0.199 to 0.208 km² (Appendix C) is roughly **540 to 620 km²**, so it is a real
answer and not a cheap one. Two properties of the
measurement bound it and are stated in the supplement rather than buried: at the top budget the
selection pool is nearly exhausted, so the narrow upper-budget intervals reflect saturation rather
than precision, and the labelled blocks are drawn from the event being predicted, which is not a
resource available before that event burns. The protocol, the full curve and the limits are in
Supplement S1.

Two limits belong with the number. At small budgets the same intervention damages the direction that
already transfers best without any labels. And six directions in three regions cannot support a
general label budget, so none is offered.
