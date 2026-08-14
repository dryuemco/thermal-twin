# Paper 2 results, carried verbatim from Paper 1 section 4.7

These subsections were moved out of the transfer manuscript on 2026-08-14 when it
was split. They are the observational-layer sensitivities and they are the body of
Paper 2. The prose is exactly as it stood in Paper 1; it is rewritten in place once
Paper 2's own structure is settled, so that the move itself changes no number and no
claim.

Kept in Paper 1 instead, because each bears directly on one of its three findings:
  (a) Evia AOI
  (d) CORAL regularisation
  (g) Blocking scale

---

## From 4.7(b): Montiferru cropland fringe

**(b) Montiferru cropland fringe.** Within-region, excluding grassland (tree+shrub population)
leaves the thermal increment essentially unchanged: ΔAUC 0.104 [0.075, 0.131] versus 0.101 [0.080,
0.125] for TSG (Section 3.16.2). Cross-region, the thermal-minus-baseline delta on the target agrees
in sign and support between the two populations for six of eight Montiferru-involved directions. The
two disagreements (Bejís→Montiferru, Montiferru→Muğla) move from supported to uncertain, not to sign
reversal. Montiferru's transfer behaviour is not driven by its cropland/grassland fringe.

---

## From 4.7(c): Window closure

**(c) Window closure.** Shifting both ends of the predictor window earlier by 7 and 14 days (window
length preserved, fixed common cohort, shared folds; Section 3.16.3) leaves the within-region
thermal increment bootstrap-supported in every region and every variant (Table R5). Nowhere does the
increment shrink toward zero; in Manavgat and Bejís it increases with earlier closure. That increase
has a mechanism, and the window-closure report states it: the closure date is shifted against a
fixed production policy, so moving the window changes which acquisition dates enter the median
composite and how many clear observations back each pixel. With about seven usable dates in a
window, a 7 or 14 day shift is a change of one or two dates. The signature fits: across the same
comparison the baseline moves by +0.002 to +0.003 while the thermal family moves by +0.022 ROC-AUC,
so the shift acts almost entirely on the thermal channels, exactly as the compositing sensitivity of
(i) predicts. This does not weaken the pre-fire reading. Contamination by early fire signal would
push the increment the other way, and it does not appear. It does mean the increment is partly a
function of how the composite is built, which is the same conclusion (i) reaches from a different
direction.

**Table R5. Window-closure sensitivity: thermal ΔAUC (TSG common cohort; final numbering at
assembly).**

| Region | Canonical | Close 7 d | Close 14 d |
|---|---|---|---|
| Manavgat | 0.074 [0.062, 0.085] | 0.101 [0.088, 0.114] | 0.094 [0.078, 0.109] |
| Bejís | 0.058 [0.048, 0.068] | 0.077 [0.068, 0.088] | 0.079 [0.068, 0.090] |
| Muğla | 0.115 [0.105, 0.125] | 0.114 [0.104, 0.124] | 0.128 [0.118, 0.137] |
| Evia (ext.) | 0.156 [0.144, 0.170] | 0.149 [0.136, 0.162] | 0.135 [0.124, 0.147] |
| Montiferru | 0.096 [0.074, 0.118] | 0.091 [0.068, 0.113] | 0.100 [0.077, 0.122] |

---

## From 4.7(e): Library version

**(e) scikit-learn version.** With byte-identical data, pipeline and seed, changing only the library
version from 1.9.0 to 1.7.2 moves raw transfer AUC by +0.021 (Montiferru→Bejís) and +0.026
(Manavgat→Bejís) on the two probes tested, which is the same order as some reported effects.
Within-region AUCs, by contrast, reproduce to ~4 decimals across environments. All numbers in this
paper were produced under, or verified against, scikit-learn 1.9.0. The two probes reproduce to four
decimal places in the verification environment (difference 0.0000). Cross-region point estimates
therefore carry an implementation tolerance of roughly ±0.02 to 0.03 unless the exact library
version is fixed. The bootstrap intervals reported throughout are wider than this jitter.

---

## From 4.7(f): Analysis population and sea water

**(f) Analysis population.** In the secondary all-valid population the within-region thermal
increment is CI-supported in all five regions, with smaller deltas than in the primary
natural-vegetation population for the three high-increment regions: ΔAUC 0.059 [0.049, 0.068]
(Manavgat), 0.048 [0.040, 0.057] (Bejís), 0.072 [0.067, 0.078] (Muğla), 0.053 [0.049, 0.058] (Evia),
0.075 [0.057, 0.094] (Montiferru), against TSG values of 0.067, 0.056, 0.116, 0.153 and 0.101
respectively. Absolute AUCs are higher in the mixed population (baseline 0.827 to 0.910), consistent
with land-cover composition contributing separable but non-thermal discrimination; the within-region
conclusion does not depend on the population choice. The nature of that extra discrimination should
be stated plainly, because it is not a subtle land-cover effect in two of the five regions. The AOIs
are place-based rectangles and are not clipped to the coastline, and sea cells satisfy
`valid_for_modeling`, since elevation, slope and the vegetation index are all finite over water and
permanent water is a valid land-cover class. Counted over the frozen datasets, water-dominant cells
are 57.7 % of Evia's all-valid population and 38.9 % of Muğla's, against 8.3 % (Manavgat), 7.4 %
(Montiferru) and 0.1 % (Bejís). In those two regions most of the extra separability of the all-valid
population is therefore land against sea rather than any fire-relevant contrast. This is one of the
two reasons the natural-vegetation population is primary here, and it is why the all-valid arm is
reported only as a sensitivity.

---

## From 4.7(h): Which thermal channel carries the increment

**(h) Which thermal channel carries the increment.** The thermal block is six predictors, but they
are not six independent measurements. `fused_lst` equals the observed Landsat LST wherever that is
valid, and the gap-filled share is 2.15% (Manavgat), 9.70% (Bejís), 0.59% (Muğla), 0.90% (Evia) and
0.11% (Montiferru), so outside Bejís the two channels are near-copies of each other; Table R8 shows
the consequence directly, with signed univariate AUCs of 0.325 versus 0.325 in one arm and 0.515
versus 0.519 in the other. `downscaled_lst` is a fitted surface whose dominant input differs by
region: the MODIS context layer in Manavgat (importance 0.525) and Evia (0.593), NDVI in Bejís
(0.482) and Montiferru (0.666), and **slope in Muğla (0.777)**, where it is largely a re-expression
of a predictor the baseline already contains. The pipeline's Step 8D ablation, run on the primary
population with the same folds, quantifies the redundancy: a single subgroup recovers most of the
whole block's increment in every region.

**Table R14. Thermal-block ablation, primary population, ΔAUC against the baseline (final numbering
at assembly).** Source: `drive_new/experiments/<region>/step8d/step8d_ablation_delta_auc_by_population.csv`.

| Region | Full thermal block | Best subgroup | Its ΔAUC | Share of the full block |
|---|---|---|---|---|
| Manavgat | +0.067 | TVDI pair | +0.065 | 96% |
| Bejís | +0.056 | fused + downscaled | +0.040 | 71% |
| Muğla | +0.116 | TVDI pair | +0.089 | 77% |
| Evia (ext.) | +0.153 | LST anomaly | +0.125 | 81% |
| Montiferru | +0.101 | TVDI pair | +0.100 | 99% |

The dryness pair (`current_tvdi_mean`, `tvdi_difference_mean`) is the best subgroup in three of five
regions and recovers 96% and 99% of the full block in Manavgat and Montiferru. This matters twice.
It converts "the thermal block" from an opaque bundle into a statement about which physical quantity
carries the increment, and it means the six reversal tests of Section 4.4 are not six independent
probes of concept shift. Source: `paper/referee2_numbers.md`, blocks D, E and F.

That table reports what each subgroup adds. The complementary question is what the block is worth
**without** its two coordinate-bearing channels, since `downscaled_lst` is a fitted surface whose own
inputs include `lon`, `lat`, `row` and `col`, and `fused_lst` inherits that on its gap-filled share.
This is the one route by which a coordinate-derived surface re-enters a feature set from which
Section 3.13 excludes coordinates, so the increment ought not to depend on it. It does not. Dropping
both channels and re-running the comparison with the pipeline's own Step 8B and Step 8C leaves ΔAUC
at +0.063 [+0.051, +0.074] (Manavgat), +0.046 [+0.038, +0.055] (Bejís), +0.097 [+0.088, +0.107]
(Muğla), +0.145 [+0.133, +0.157] (Evia) and +0.105 [+0.082, +0.128] (Montiferru). That is 94 %,
82 %, 84 %, 94 % and 103 % of the full-block value, with every interval excluding zero. The
six-channel arm of the same harness reproduces the frozen metrics with a maximum absolute difference
of exactly zero in all five regions, so the comparison is not confounded by the re-run. Source:
`paper/observational_sensitivities.md`.

---

## From 4.7(i): Landsat compositing

**(i) Landsat compositing.** The current-period LST composite is a median over the clear
acquisitions inside the predictor window, and how those acquisitions are weighted is a choice. Three
controlled chains exist for Manavgat, on an identical cohort with identical folds and an identical
baseline, differing only in that raster: the production scene-weighted reference gives ΔAUC +0.064
[+0.052, +0.075], a date-balanced variant gives +0.084 [+0.072, +0.098], and an overlap-harmonised
date-balanced variant gives +0.045 [+0.033, +0.057]. The baseline AUC is identical to six decimal
places across all three (0.804362), so the entire spread sits in the thermal block, and both paired
comparisons have intervals excluding zero. The two are referenced differently, as their source
reports define them: date-balanced against the production chain is +0.021 [+0.012, +0.031], and
overlap-harmonised against the *date-balanced* chain is −0.040 [−0.050, −0.029]. Referenced to
production instead, the overlap-harmonised difference is −0.019. The mechanism is documented in the same export: at boundaries where the
number of contributing clear acquisitions changes, the residual seam analysis finds excess jumps of
0.850 °C [0.812, 0.890] in the current-minus-baseline field and 0.526 °C [0.503, 0.551] in the
anomaly z-score, with the final attribution `current_support_dominant`. Manavgat's window is backed
by seven acquisition dates from two alternating Landsat paths, so a cell inside the path overlap
rests on seven dates and a cell outside it on three or four.

Two limits on this axis are stated by the source reports themselves and are adopted here: the A/B
was run for one AOI only, the alternative chains are candidates rather than production, and no
non-inferiority claim is made for them. The conclusion drawn here is correspondingly narrow. **The
within-region increment carries a compositing tolerance of roughly ±0.02 AUC, which is the same
order as the scikit-learn tolerance of (e) and wider than the 2-cell interval of Table 3.** It does
not approach the increment itself, which stays bootstrap-supported and positive under all three
chains.

**The audit was then extended to a second region, and the intervention behind that tolerance does not
replicate.** Bejís was chosen because it carries the highest gap-filled share of the five and is
therefore the most exposed to how the composite is built. Its diagnostic reference chain reproduces
the frozen canonical products first: eight of nine semantic checks pass and six are exact, the two
derived ones differing by 2.7×10⁻⁵ and 2.2×10⁻⁵, which is float32 recomputation noise. On the seam
comparison itself, where a positive value means date-balanced compositing lowers the discontinuity,
Manavgat improves at all four boundary types (+0.125 scene-count, +0.095 unique-date-count, +0.597
same-day-multiplicity, +0.004 path/row, every one interval-supported). Bejís improves only at the
boundary the intervention directly targets, same-day multiplicity, at +0.378 [+0.278, +0.483]; its
unique-date-count edges get **worse** with interval support at −0.067 [−0.095, −0.041]; and its
scene-count and path/row boundaries are indistinguishable from no effect. The overall verdict for
Bejís is therefore *uncertain* against *supported reduction* for Manavgat, and the released A/B tool
declines to run the downstream comparison on that basis, since there is no established net seam
improvement to propagate. The difference is not the number of Landsat paths, which is two in both
(177 and 178 against 198 and 199), but their balance: Manavgat draws 3, 3, 4 and 4 scenes from its
four path/row tiles while Bejís draws 4, 4, 4 and 4. **The ±0.02 tolerance should therefore be read
as specific to Manavgat rather than as a cohort-wide figure**, and the remaining three regions stay
unaudited on this axis. Source: `paper/compositing_second_region.md`.

---

## From 4.7(j): Population size and positive count

**(j) Muğla's population size.** Muğla contributes the largest analysis population of the five
regions, 41,730 cells against Manavgat's 20,511, and it is also the region with the second largest
within-region increment and the one that takes part in the transfer directions that work. Whether
that is the region or simply its data volume is a question the design can answer, so it was
answered rather than argued. The Muğla modelling population was cut to exactly Manavgat's cell
count over 20 deterministic repeats, stratified by 10-cell block and label so that prevalence is
preserved (0.0698 full against 0.0701 subsampled) and every block of the full population is
retained, which isolates cell count from spatial extent. The full-Muğla block-to-fold mapping is
inherited unchanged, so the folds are not re-drawn.

Muğla's role in transfer does not depend on its size. With Muğla as the source, three of the four
direction-and-family combinations put the full-population value inside the subsampling range
(Muğla→Manavgat thermal 0.401 against a range of 0.378 to 0.404; Muğla→Bejís thermal 0.583 against
0.548 to 0.608). With Muğla as the target all four lie inside, and tightly (Bejís→Muğla thermal
0.618 against 0.613 to 0.625). The one value outside its range is the baseline family of
Muğla→Bejís, where the full-population 0.451 sits *below* the subsampled range of 0.465 to 0.556,
so shrinking Muğla would if anything improve that arm rather than explain its failure.

What size does affect is absolute within-region skill, modestly and in the expected direction. The
full-population reference lies above the subsampling range for both families, baseline 0.698
against 0.678 to 0.698 and thermal 0.777 against 0.747 to 0.772. **The increment survives the
matching**: it is +0.079 at full size and +0.071 at the median size-matched repeat. So Muğla's
larger population inflates its absolute AUC by roughly 0.01 to 0.02 and leaves both the increment
and the transfer behaviour substantially intact. Two limits belong with this. The repeats vary only
in which cells fill each stratum, so the range describes within-stratum selection variability and is
narrower than any sampling distribution; and that diagnostic equalises prevalence rather than the
positive count, which it states as its own limitation. No bootstrap was run there and no probability
statement is made. Source: `mugla_subsampling` in the frozen diagnostics export, recomputed here from
its 20 per-repeat records.

**The positive count was then equalised as well, since the variance of an AUC is dominated by the
minority class.** Muğla was cut to Manavgat's population on both axes at once, 20,511 cells of which
784 burned, over ten seeded stratified draws, and the pipeline's own Step 8B and feature lists were
used. The transfer behaviour again does not move: Muğla→Manavgat sits at 0.401 against a matched
range of 0.375 to 0.415, and Muğla→Bejís at 0.583 against 0.518 to 0.594, both inside. What does move
is the within-region increment, which falls from +0.116 to a matched median of +0.098, range +0.088
to +0.105, so the full-population value lies above the matched range. Part of Muğla's larger
increment is therefore a positive-count effect, and the part that is not still leaves it among the
larger increments in the cohort. This arm is our own design rather than the frozen diagnostic's and
is reported as such. Source: `paper/mugla_positive_matched.md`.

---

## From 4.7(k): Sea in the TVDI edges, and a common-edge index

**(k) Sea in the TVDI edges, and a common-edge index.** TVDI is normalised against wet and dry edges
fitted as the 2nd and 98th LST percentiles inside each NDVI bin, over whatever the scene contains
(Section 3.4). The AOIs are place-based rectangles that are not clipped to the coastline, so sea
takes part in that fit, and two of the five are largely marine. The index is also the one whose
internal normalisation was expected to make it portable, so if its reversal were an artefact of the
edges, the paper's mechanism would be weaker than it looks. Three arms were therefore compared: the
frozen scene fit; the same fit restricted to land cover classes 10, 20, 30, 40 and 60; and one set of
edges fitted once over the pooled land pixels of all five regions, 26.2 million of them, which puts
every region on a common dryness scale.

**Table R11. Signed univariate AUC of `current_tvdi_mean` against `burned` under three edge
definitions.** Primary population; raw AUC, never folded, so a value below 0.5 is a direction;
10-cell (≈ 5 km) spatial-block bootstrap, 1000 replicates, seed 42, at the registered specification
of Section 3.12. Bold marks an interval excluding 0.5. Source: `paper/tvdi_land_refit.md`.

| Region | Water share | Scene, all pixels | Scene, land only | Pooled, land only |
|---|---:|---|---|---|
| Bejís 2022 | 0.1 % | 0.517 [0.429, 0.595] | 0.519 [0.431, 0.597] | 0.503 [0.416, 0.578] |
| Montiferru 2021 | 7.4 % | **0.356** [0.233, 0.499] | 0.353 [0.229, 0.500] | 0.356 [0.232, 0.500] |
| Manavgat 2021 | 8.3 % | 0.552 [0.460, 0.641] | 0.558 [0.465, 0.646] | 0.565 [0.469, 0.656] |
| Muğla 2021 | 38.9 % | **0.336** [0.276, 0.401] | **0.351** [0.288, 0.424] | **0.341** [0.280, 0.408] |
| North Evia 2021 (ext.) | 57.6 % | **0.362** [0.280, 0.440] | **0.379** [0.298, 0.458] | **0.378** [0.297, 0.455] |

The effect of sea on the index is real and it is small. Removing water moves the signed AUC by
+0.017 in Evia and +0.016 in Muğla, the two marine AOIs, against +0.006 in Manavgat, −0.002 in
Montiferru and +0.002 in Bejís, so the shift scales with sea fraction as the mechanism predicts.
**It changes no region's direction.** The two regions in which higher TVDI ranks burned cells stay
above 0.5 and the three in which lower TVDI does stay below, with Muğla and Evia keeping intervals
entirely below 0.5. One verdict moves, on a knife edge: Montiferru's upper bound goes from 0.4991 to
0.5004, a shift of 0.0013, which is the count instability recorded as limitation (x) in Section 5.11
rather than a change of finding.

The common-edge arm is the stronger test, because it removes the scene dependence itself rather than
only the sea. With one set of edges for all five regions, Manavgat still ranks burned cells by higher
TVDI (0.565) while Muğla and Evia still rank them by lower TVDI with bootstrap support (0.341 and
0.378). Putting every region on the same dryness scale does not bring the directions into agreement.
The reversal is therefore a property of the relationship between dryness and burning in these
landscapes, not of how the index was normalised. Two limits: only `current_tvdi_mean` was
re-derived, since `tvdi_difference_mean` would need the four baseline-year surfaces refitted as
well; and pooling the current-window LST of five regions observed on different dates gives a common
statistical scale, not a radiometrically harmonised one.

---

## From 4.7(l): Label agreement

**(l) Label agreement, and whether the reversals are fringe artefacts.** MCD64A1 labels a 500 m cell
from its 30 m sub-pixels, and `burn_date_pixel_agreement_fraction` records the share of a cell's
positive sub-pixels that agree with its modal burn date. It is defined for burned cells only, and its
median is 1.000 in every region, but its lower tail is not empty: the 25th percentile runs from 0.765
(Muğla) to 0.985 (Montiferru). Cells with low agreement are disproportionately scar-fringe cells, and
fringe cells differ systematically in terrain from core cells, so differential fringe contamination
is a competing explanation for a reversal in a terrain variable. That is exactly what the paper's
sharpest reversal is. The signed univariate AUCs were therefore recomputed with burned cells below an
agreement threshold dropped and the negative class left whole, at thresholds of 0.75 and 0.90, which
retain 76 % to 88 % and 63 % to 79 % of each region's burned cells. The unrestricted arm reproduces
the archived step9g values exactly, to 1.1×10⁻¹⁶.

**Table R12. Signed univariate AUC of `elevation_mean` against `burned` by label-agreement
threshold.** Primary population; raw AUC; 10-cell spatial-block bootstrap, 1000 replicates, seed 42.
Bold marks an interval excluding 0.5.

| Region | All burned cells | Agreement ≥ 0.75 | Agreement ≥ 0.90 |
|---|---|---|---|
| Manavgat 2021 | **0.374** [0.289, 0.471] | **0.368** [0.284, 0.462] | **0.362** [0.279, 0.460] |
| Bejís 2022 | **0.643** [0.558, 0.729] | **0.642** [0.560, 0.728] | **0.635** [0.550, 0.722] |
| Muğla 2021 | **0.611** [0.531, 0.695] | **0.606** [0.527, 0.690] | **0.602** [0.520, 0.686] |
| North Evia 2021 (ext.) | 0.541 [0.458, 0.632] | 0.544 [0.461, 0.636] | 0.550 [0.463, 0.636] |
| Montiferru 2021 | 0.584 [0.395, 0.762] | 0.567 [0.390, 0.748] | 0.546 [0.380, 0.729] |

The elevation reversal is not a fringe artefact. Manavgat's interval stays entirely below 0.5 and
Bejís's and Muğla's stay entirely above it at every threshold, so the disjoint-interval contrast that
carries Section 4.4 survives the restriction; if anything Manavgat moves further from chance, from
0.374 to 0.362, as thin-evidence cells are removed. The thermal channels behave the same way: Muğla
and Evia keep `current_lst_mean`, `downscaled_lst_mean`, `fused_lst_mean` and `current_tvdi_mean`
entirely below 0.5 at both thresholds, while Manavgat's point estimates drift slightly upward and
its intervals continue to span chance. Two verdicts change, and both are Montiferru's, both by about
0.005 on an interval bound: `current_tvdi_mean` moves from an upper bound of 0.499 to 0.505 and
`tvdi_difference_mean` from 0.497 to 0.503. That is the count instability of limitation (x) in
Section 5.11, in the region with the fewest positive-carrying blocks, not a change of finding.
Source: `paper/observational_sensitivities.md`.

---

## From 4.7(m): Gap-filled thermal cells

**(m) Gap-filled thermal cells.** `fused_lst` equals the observed Landsat LST outside a gap-filled
share, and where that share is high the channel is the downscaled surface rather than an
observation. The gap-fill is concentrated rather than diffuse: its median is zero in every region,
but 18.8 % of Bejís's primary-population cells carry some, with a 90th percentile of 0.47, against
2.0 % to 9.1 % elsewhere. The within-region comparison was therefore re-run on cells whose gap-filled
fraction is at most 0.10, using the pipeline's own Step 8B and Step 8C on the restricted population.

| Region | Cells retained | ΔAUC, full | ΔAUC, low gap-fill [95 % CI] |
|---|---:|---|---|
| Manavgat 2021 | 95.4 % | +0.067 | +0.072 [+0.061, +0.083] |
| Bejís 2022 | 85.1 % | +0.056 | +0.043 [+0.033, +0.053] |
| Muğla 2021 | 99.2 % | +0.116 | +0.114 [+0.104, +0.123] |
| North Evia 2021 (ext.) | 98.3 % | +0.153 | +0.159 [+0.146, +0.171] |
| Montiferru 2021 | 99.7 % | +0.101 | +0.109 [+0.087, +0.134] |

The increment keeps bootstrap support in all five regions. Bejís moves the most and in the direction
the concern predicts, from +0.056 to +0.043, so part of its increment does rest on gap-filled cells;
the remaining four move by at most 0.008, in both directions. The restriction changes the population,
so these are not paired comparisons with the full-population row of Table 3. Source:
`paper/observational_sensitivities.md`.
