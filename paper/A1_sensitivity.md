# Appendix A. Sensitivity analyses

Each arm below varies one design choice and leaves everything else fixed. None changes a conclusion
in the main text; they are reported here so that a reader can see which choices were tested and what
each was worth. The lettering is continuous, unlike the earlier draft's, where three of the original
subsections had moved to the companion paper and left gaps behind.

**(a) Evia AOI and prevalence.** Repeating the raw transfer arms with the legacy, high-prevalence
Evia box leaves every qualitative conclusion unchanged: thermal raw transfer AUCs move by up to 0.07
— the largest is Evia→Bejís, 0.378 to 0.448 — and no direction changes side of the chance line.

**(b) CORAL regularisation.** Over nine λ values from 0 to 10⁻¹ on four directions, CORAL transfer
AUC moves by at most 0.014 within any direction and 0.008 within the thermal family, so no
CORAL-dependent conclusion here is sensitive to λ in that range. The companion paper reports the
canonical λ = 1, which the released sweep omits.

**(c) Blocking scale.** Recomputing the transfer quantities at 10-cell (≈ 5 km) blocking from the
frozen per-cell predictions widens the intervals and moves the verdict counts, from ten positive,
seven negative and three uncertain at 1 km to six, four and ten at 5 km. Coarser blocking therefore
removes support from six verdicts and adds none.

The point estimates are unchanged, but that is an identity rather than a result and should not be
offered as robustness: the blocking scale is the bootstrap *resampling unit*, and each point
estimate is computed once over all target cells, so no choice of block size could have moved one.
What the comparison does establish is the direction of the fragility — every verdict that changes,
changes towards "no verdict" — and that no direction crosses the chance line under the widened
intervals. The counts are the fragile part of this paper. The sign pattern is not thereby shown to
be robust; it is simply not tested by this particular variation.

**(d) Predictor-window closure.** Closing the predictor window 7 and 14 days earlier, in all five
regions, leaves the thermal contribution positive and bootstrap-supported everywhere. The direction
of the change is region-specific: the contribution strengthens in Bejís (0.058 → 0.079 at 14 days)
and Muğla (0.115 → 0.128), is flat in Montiferru, and weakens monotonically in Evia (0.156 → 0.149 →
0.135). What holds in every region is survival, not improvement, which is the claim made in
Section 5.2.

**(e) Quality screening of the coarse thermal input.** Two of the five regions' MODIS inputs are
quality-screened and three are not, a split that follows export date rather than design and that
induces an elevation-correlated change at the input (r = +0.615 in Manavgat). Rebuilding Manavgat's
entire downstream chain from a quality-screened input changes the downscaled surface on 22,304 of
24,150 cells by up to 10.9 °C, and moves no signed univariate association by more than +0.0003:
elevation stays at 0.374 [0.290, 0.472] in both arms, the population is unchanged, and the
within-region increment moves from [+0.055, +0.079] to [+0.054, +0.077]. The reason is structural.
Elevation is a DEM variable the screening cannot touch, and fusion falls back on the MODIS-derived
surface across only 2.14 points of coverage. Details in `paper/modis_qc_downstream_propagation.md`.
