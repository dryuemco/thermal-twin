# Appendix A. Sensitivity analyses

Each arm below varies one design choice and leaves everything else fixed. None changes a conclusion
in the main text. They are reported so that a reader can see which choices were tested, and what
each was worth. Arm (f) is the exception in one respect: it is not a robustness check but a test of
a claim the introduction makes, and the claim is not upheld.

**(a) Evia AOI and prevalence.** The raw transfer arms were repeated with the legacy,
high-prevalence Evia box. Every qualitative conclusion is unchanged. Thermal raw transfer AUCs move
by up to 0.07, the largest being Evia to Bejís at 0.378 to 0.448, and no direction changes side of
the chance line.

**(b) CORAL regularisation.** Over nine λ values from 0 to 10⁻¹ on four directions, CORAL transfer
AUC moves by at most 0.014 within any direction and 0.008 within the thermal family, so no
CORAL-dependent conclusion here is sensitive to λ in that range. The companion paper reports the
canonical λ = 1, which the released sweep omits.

**(c) Blocking scale.** Recomputing the transfer quantities at 10-cell (≈ 5 km) blocking from the
frozen per-cell predictions widens the intervals and moves the verdict counts, from ten positive,
seven negative and three uncertain at 1 km to six, four and ten at 5 km. Coarser blocking therefore
removes support from six verdicts and adds none.

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
Elevation stays at 0.374 [0.290, 0.472] in both arms, the population is unchanged, and the
within-region increment moves from [+0.055, +0.079] to [+0.054, +0.077]. The reason is structural.
Elevation is a DEM variable the screening cannot touch, and fusion falls back on the MODIS-derived
surface across only 2.14 points of coverage. Details are in
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
