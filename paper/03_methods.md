# 3. Data and methods

> **Rewritten 2026-08-14 in the split.** This section was 15,407 words. It is now written to let a
> reader replicate the four contributions of Section 1.4 and to carry every number Section 4 cites, and
> nothing else. The observational layer beneath it, meaning predictor provenance, compositing,
> quality screening, index normalisation, label omission and the version and reproduction audits, is
> the subject of the companion paper and is summarised here only where a Paper 1 claim depends on it.
> The released repository remains the authoritative source for file and line references.
>
> **Updated 2026-09-23 for the corrected Manavgat label.** §3.13: the reproduction sentence now
> reports the check against the re-frozen outputs (1.3×10⁻⁸, formerly 1.6×10⁻⁷), names who carried it
> out, and states the one-line window-closure patch. The seed-stability sentence follows the new
> seed sweep.

## 3.1 Study regions and temporal windows

Five Mediterranean wildfire regions are analysed (Fig. 1): Manavgat 2021 and Muğla 2021 in Türkiye,
Bejís 2022 in Spain, North Evia 2021 in Greece and Montiferru 2021 in Sardinia. Each is a
place-based rectangle in EPSG:4326, defined from place coverage rather than from a fire perimeter and
deliberately not clipped to it, so that unburned cells around each fire form the negative class.
**The record does not show every box fixed before any outcome was seen**, so what it does show is
stated region by region. In the pipeline's version history each box has a single committed value,
never changed afterwards. Montiferru's is derived deterministically from the union of four municipal
boundaries. Manavgat's was drawn to exclude the coastal cropland belt; its final coordinates are in a dated
AOI preview record of 7 July 2026, the day before its first gate result, and never changed. Bejís's is still labelled the initial candidate in the registry but was committed after its first
gate and model results. Muğla's coordinates appear in a dated preflight record about four minutes
before its first gate result and were committed to the registry only afterwards. No box needed
adjusting to pass the gate, whose admitted margins are wide (Section 4.1). **One choice was label-informed and
is stated as such**: the North Evia box was extended after the legacy box proved atypically high in
burned prevalence, the extended geometry then defined from place anchors and the legacy variant kept
as a sensitivity arm. Section 4.4 shows this framing decision is consequential and Appendix C.5(ix)
treats it as the design lesson of the paper. A sixth region, Kozan 2023, is carried as a negative control and excluded by the gate of
Section 3.3.

Each region has two non-overlapping windows. The **predictor window** closes the day before the
**label window** opens, so no predictor observation can post-date the first labelled burning. Lengths
vary with the event: 57 to 61 days for predictors, 35 to 59 for labels, counted inclusively. A four-year baseline of window-symmetric composites precedes each
predictor window and supplies the climatological reference for the anomaly channels. Region
identifiers, bounding boxes, window dates and baseline years are registered in `core/regions.py` and
reproduced in Appendix C, Table C1. The processing chain and the evaluation
programme it feeds are drawn in Fig. 2.

## 3.2 Burned-area label and the ~500 m analysis grid

Labels come from MODIS MCD64A1 Collection 6.1 [@Giglio2018] retrieved through Google Earth Engine
[@Gorelick2017], whose omission and commission characteristics [@Boschetti2019] bound every model
here. The analysis grid is **reconstructed rather than native**: the pipeline's 30 m EPSG:4326
reference grid is partitioned into 17 x 17 blocks, giving a nominal 510 m cell that approximates
rather than reproduces the MODIS cell and is square in degrees but not on the ground. A cell's burn
date is the mode of its positive sub-pixel day-of-year values, tested against the label window; the
label never affects eligibility for modelling. Two safeguards are recorded rather than assumed:
cells burning before the label window opens are removed, which ran for three of five regions and
excluded 49 cells in Muğla, 16 in North Evia and 61 in Montiferru, with none arising in Manavgat or
Bejís, and burning in earlier years is screened for none. Appendix C.1 gives the
full specification, including what follows from the grid's shape.

## 3.3 Burned-landcover admissibility gate

Before any modelling each region passes a gate asking what fraction of its burned cells is dominated
by natural vegetation, using ESA WorldCover classes [@Zanaga2022] on the same cells. A region is admitted at 0.50
with at least 30 burned cells, and rejected as a cropland-dominated control at 0.50 cropland.
Verdicts and the purpose of the gate are in Section 4.1, the full rule in Appendix C.1.

## 3.4 Predictor variables

Two feature sets are used. The **baseline** is terrain, fuel and greenness: elevation, slope,
dominant land cover and a predictor-window median vegetation-index composite, all static or
near-static over the timescale at which fire danger varies. The **thermal** set adds six pre-fire
channels: current land surface temperature, its anomaly against a four-year window-symmetric
baseline at the same cell, the Temperature-Vegetation Dryness Index and its difference against that
baseline, and two coordinate-informed products, a downscaled and a fused surface temperature. The
two differenced channels are the ones constructed to isolate the dynamic anomaly. TVDI's wet and dry
edges are percentiles of the values a given area and window happen to contain, so **it is not
portable as a physical quantity independently of any concept shift** (Appendices C.4, C.5).

## 3.5 Cell aggregation, validity and analysis populations

Cell-level values are means over the ~510 m cell from valid 30 m pixels only, with the valid fraction
recorded. A cell is `valid_for_modeling` when it is analysis-eligible, meaning not excluded for
pre-label burning, and its predictors are valid: joint finite NDVI, elevation and slope support over
at least 30 % of the cell, finite means for those three channels, and at least one valid land-cover
pixel. **Thermal completeness is not part of the definition**: depending on the region, 6 % to 58 %
of valid cells carry at least one missing thermal channel, and missing values are imputed inside the
fitting pipeline (Section 3.6) rather than by excluding the cell. The **primary** population is natural vegetation, cells whose combined tree,
shrub and grass fraction reaches 0.50, which excludes cropland from every burnable mask. The
**secondary** population is all valid cells; the frozen export carries it for the within-region arm
in two regions, reported as a sensitivity in Appendix A(v), and the transfer matrix is defined on the
primary population only.

## 3.6 Classifier

The two feature sets of Section 3.4 are nested, the thermal set being the baseline plus the six
thermal channels. Land cover is one-hot encoded. Missing numeric values are median-imputed and the
categorical channel most-frequent-imputed, with the imputers fitted inside each training fold, and
on the source alone in transfer, so no held-out statistic enters a fit in the raw arms. Features are
not otherwise standardised. Standardisation appears only in the adapted arms of Section 3.9, where
target feature statistics, never target labels, enter the transform by design, and missing values
there are filled with the region's own mean. The classifier is a random forest [@Breiman2001] with 300 trees, unlimited depth,
`min_samples_leaf = 3`, balanced class weights and `random_state = 42`, identical for every region,
population, feature set and transfer direction, so that no comparison here is confounded by a model
choice.

## 3.7 Spatial-block cross-validation and bootstrap uncertainty

Cross-validation is spatially blocked. Cell $`i`$ at grid position $`(r_i, c_i)`$, from `row_500m` and
`col_500m`, is assigned to the block

```math {#eq:block}
b_k(i) = \left( \lfloor r_i / k \rfloor,\; \lfloor c_i / k \rfloor \right).
```

Five folds are drawn over whole blocks, stratified by label, so no block is split between training
and test. The block size $`k`$ is reported at 2, 10 and 20 cells, about 1, 5 and 10 km.

Every score is a ROC-AUC on a named set of cells $`F`$, its **evaluation frame**. With $`F^{+}`$ the
burned and $`F^{-}`$ the unburned cells of $`F`$, and $`s_i`$ the predicted score,

```math {#eq:auc}
\mathrm{AUC}(s; F) = \frac{1}{|F^{+}|\,|F^{-}|} \sum_{i \in F^{+}} \sum_{j \in F^{-}} \left[ \mathbf{1}(s_i > s_j) + \tfrac{1}{2}\,\mathbf{1}(s_i = s_j) \right].
```

This is the probability that a burned cell in $`F`$ outranks an unburned cell in $`F`$. Changing the frame
therefore changes the metric even when no score changes (Section 3.12).

Uncertainty is a spatial-block bootstrap. Let $`\beta_1, \dots, \beta_M`$ be the blocks of
[#eq:block] holding cells of $`F`$. Replicate $`b`$ draws $`M`$ indices $`u_{bm}`$ uniformly with replacement:

```math {#eq:boot}
F^{*b} = \biguplus_{m=1}^{M} \beta_{u_{bm}}, \qquad \mathrm{CI}_{95} = \left[ Q_{0.025}\{\theta(F^{*b})\}_{b},\; Q_{0.975}\{\theta(F^{*b})\}_{b} \right].
```

Here $`\theta`$ is the statistic and $`Q`$ the 2.5 and 97.5 percentiles over 1000 replicates, seed 42. A
single-class replicate is discarded. Differences are formed within each replicate, so they are
paired. The block size of each interval is stated with the result. Because it is blocks that are resampled,
what bounds an interval's reliability is the number of blocks carrying at least one burned cell, and
those counts are reported alongside the intervals. Where a verdict rests on too few such blocks it
is stated as indicative rather than as an interval.

The twenty transfer directions are not independent, since each region appears in eight. The
**pair-cluster bootstrap** therefore resamples the ten unordered region pairs, each carrying its set
$`\pi_p`$ of ordered directions, and averages the carried values $`\delta_{st}`$:

```math {#eq:pair}
\bar{\delta}^{*b} = \frac{\sum_{m=1}^{10} \sum_{(s,t) \in \pi_{u_{bm}}} \delta_{st}}{\sum_{m=1}^{10} |\pi_{u_{bm}}|}.
```

The interval is the same percentile form, over 20,000 replicates for Section 4.4. Clustering by
target region replaces $`\pi_p`$ by the four directions sharing a target. A quantity with one value
per held-out scar or target region gets a Student t interval over those $`n`$ units,

```math {#eq:tint}
\bar{x} \pm t_{0.975,\,n-1}\, s_x / \sqrt{n}.
```

**The effective sample is thus ten pairs or five regions for direction-level intervals, and at most
eight scars from four regions for scar-level ones.**

## 3.8 Cross-region transfer protocol

For each ordered pair the model is fitted on the source population and applied to the target with
**no target label used at any point**: no refitting, no threshold selection, no calibration. Both
feature sets are transferred, so the thermal block's contribution is a paired difference within a
direction rather than a comparison across directions. All twenty ordered directions are computed.

## 3.9 Label-blind domain adaptation

Two label-free remedies are tested on every direction, in both feature sets.

**Region-wise z-score.** Each region's numeric features are standardised using its own statistics,
source statistics from source data and target statistics from target data, never pooled. For
feature $`j`$ in region $`R`$,

```math {#eq:zscore}
z_{ij} = \frac{x_{ij} - \mu_j^{R}}{\sigma_j^{R}}, \qquad \mu_j^{R} = \frac{1}{n_j^{R}} \sum_{i \in O_j^{R}} x_{ij}, \qquad \sigma_j^{R} = \Big( \frac{1}{n_j^{R}} \sum_{i \in O_j^{R}} (x_{ij} - \mu_j^{R})^2 \Big)^{1/2},
```

where $`O_j^{R}`$ holds the $`n_j^{R}`$ cells with an observed value (ddof 0). A missing value is
first set to $`\mu_j^{R}`$, so it becomes zero, and $`\sigma_j^{R} < 10^{-12}`$ is replaced by 1.
Land cover is not transformed. Target feature statistics, never target labels, thus enter the
adapted arms by design. The
classifier is refitted on the z-scored source and applied to the z-scored target. This removes
first- and second-order marginal offsets.

**CORAL after region-wise z-score.** The source covariance is aligned to the target's by the standard
whitening-recolouring map [@Sun2016]. With $`Z_R`$ the $`n_R \times d`$ matrix of z-scored numeric
features, one row per cell,

```math {#eq:coral}
Z_s^{\mathrm{al}} = Z_s\,(C_s + \lambda I)^{-1/2}\,(C_t + \lambda I)^{1/2}, \qquad C_R = \frac{1}{n_R} \sum_{i=1}^{n_R} (z_i - \bar{z}_R)(z_i - \bar{z}_R)^{\top},
```

with $`\lambda = 10^{-5}`$ (ddof 0). Both means are zero after [#eq:zscore], so the general map's
mean terms vanish. Matrix powers use a symmetric eigendecomposition, eigenvalues floored at
$`10^{-12}`$. Critically **the transform is applied to the source
only**; the target stays at $`Z_t`$, and the classifier is refitted on $`Z_s^{\mathrm{al}}`$. Neither
variant sees a target label, and both are verified label-blind at run time. λ sensitivity was assessed over nine
values on four of the twenty directions, moving transfer AUC by at most 0.014, and no value of λ was
selected on performance; the λ = 1 of the original CORAL formulation lies outside that sweep, while
the value used throughout remains λ = 10⁻⁵ (Appendix A(b)).

## 3.10 Transfer-gap decomposition and the concept-shift criterion

For a direction into a target, let $`A_{\mathrm{w}}`$ be the target's within-region thermal AUC
under blocked cross-validation, $`A_{\mathrm{raw}}`$ the raw transfer AUC and $`A_{\mathrm{ad}}`$
the transfer AUC after adaptation method $`m`$, all on the same target cells. The gap is decomposed as

```math {#eq:decomp}
G = A_{\mathrm{w}} - A_{\mathrm{raw}}, \qquad R_m = A_{\mathrm{ad}} - A_{\mathrm{raw}}, \qquad U_m = A_{\mathrm{w}} - A_{\mathrm{ad}}, \qquad \rho_m = R_m / G,
```

so $`R_m + U_m = G`$. The recovered fraction $`\rho_m`$ is signed and unclipped. **When adaptation
lowers AUC, $`R_m`$ and $`\rho_m`$ are negative and reported as negative recovery, never set to
zero.** No fraction is reported when $`G \le 0`$. Intervals come from the paired bootstrap of
[#eq:boot] on 2-cell target blocks, resampling within-region out-of-fold and transfer scores
together and evaluating [#eq:decomp] per replicate; replicates with $`|G| < 10^{-6}`$ are dropped.
Where one method is shown per direction it is the one with the higher $`A_{\mathrm{ad}}`$, a choice
that uses target labels. Section 4.3 shows the remainder should not be read as a
conditional residual, because much of it is incurred inside a single region (Appendices A(j), C.7).

The mechanism is diagnosed by **signed univariate association**: the raw ROC-AUC of each numeric
predictor against `burned` is computed per region and never folded to max(AUC, 1 − AUC), so a value
below 0.5 is a direction rather than weakness. A reversal is called bootstrap-supported only when the
two regions' point estimates fall on opposite sides of 0.5 **and each region's own interval excludes
0.5**. That is stricter than requiring the intervals to be disjoint, and a feature failing the second
condition is recorded as a point reversal only.

## 3.11 Interventions

**Pooled multi-region training.** Leave-one-region-out: the model is trained on the pooled primary
populations of the other four regions and evaluated on the held-out region, with folds blocked as
before. This asks whether pooling recovers what single-source transfer loses.

**Removal of direction-reversing features.** The two predictors reversing with bootstrap support
**on the frames as drawn** are **`elevation_mean`** and **`lst_anomaly_mean`**. Section 4.4 withdraws
that support under an equalised frame, so the selection rule is frame-dependent and this arm is
reported as a measurement under the original protocol, not as a consequence of an established
reversal. Both are dropped and everything refitted, within-region and across every direction, and
each is dropped singly so the cost can be attributed. The two features are selected by the same
reversal analysis the result is then read against, so **both quantities are post-selection estimates**
with no correction applied.

## 3.12 Evaluation frames and controls on the transfer path

Let $`V_R`$ be the primary population of region $`R`$ and $`P_R \subset V_R`$ its burned cells. By
[#eq:auc], a frame fixes which burned and unburned cells are compared. The **region-wide frame** is
$`V_R`$, the rectangle as drawn, used in Sections 4.2 and 4.5.

**Scar frames.** A scar is an 8-connected component $`K`$ of $`P_R`$ with at least 50 cells. Its
**scar + 2 km collar** is

```math {#eq:scar}
H_K = \Big\{ i \in V_R : \min_{j \in K} \big( |r_i - r_j| + |c_i - c_j| \big) \le m \Big\},
```

with $`m = \mathrm{round}(2 / 0.45) = 4`$ grid steps, computed as $`m`$ steps of 4-connected dilation. Its negatives are all fire-adjacent. Four evaluations
use it (Table 2). A scores out-of-fold predictions from 5-fold blocked cross-validation ($`k = 10`$) on
$`V_R`$, and B scores the same predictions on $`H_K`$. B is thus the **same blocked model
restricted** to the scar area, which isolates the evaluation region from the training regime. C is
**leave-one-scar-out**: a model fitted on $`V_R \setminus H_K`$ is scored on $`H_K`$, skipped if
either set has one class. D, the **foreign-region evaluation**, averages over the four other regions
a model fitted on that region's population and scored on $`H_K`$. Buffers of 2, 5 and 10 km were
run, 2 km primary. Three controls reuse A's predictions, each averaged over 20 draws without
replacement. The **prevalence-matched** control draws $`|H_K^{+}|`$ cells from $`P_R`$ and
$`|H_K^{-}|`$ from $`V_R \setminus P_R`$. The **negative-pool** control keeps the drawn burned cells
but uses the scar's own negatives $`H_K^{-}`$, and the positive-pool control does the converse. A
**within-region half-split** (modelled cells cut at the median of a grid axis, both axes and
directions, a split discarded when either half is single-class) completes the set, under the
transfer protocol of Section 3.8 unchanged. The per-split and per-scar positive counts are unequal
and bear on the interpretation (Appendix A(i)).

**Distance collars.** With 0.45 km per grid step on both axes, the distance to the nearest burned
cell and the collar of radius $`r`$, for $`r`$ of 5 and 10 km, are

```math {#eq:collar}
d_i = 0.45 \min_{j \in P_R} \big\lVert (r_i, c_i) - (r_j, c_j) \big\rVert_2, \qquad F_R(r) = \{ i \in V_R : d_i \le r \}.
```

Every burned cell has $`d_i = 0`$ and is kept, so only far-field negatives leave. In transfer the
model is fitted on $`F_s(r_s)`$ and scored on $`F_t(r_t)`$, with the pairs of Table 3 and
$`r = \infty`$ for the region-wide frame.

**Every collar frame, $`H_K`$ and $`F_R(r)`$ alike, is defined from burned cells, so it is
label-conditioned.** It is a diagnostic of how the scoring extent shapes the metric. It cannot be
drawn before a fire.

## 3.13 Leakage control and reproducibility

An explicit forbidden-column set is enforced at every model fit as an assertion rather than a
convention: coordinates and their normalised forms, every burn-date and label-provenance column, and
the agreement fraction are excluded from all feature sets. The natural-vegetation mask defines the
population and is never a predictor. All randomness uses seed 42 and the bootstrap 1000
replicates, with one qualification: the diagnostic bootstraps of the released appendices use
per-measure offsets from that seed rather than the seed itself, so that independent measures do not
share a resampling draw. Across five seeds every transfer verdict at 1 km blocking is stable; at
5 km one level verdict and two paired-delta verdicts are not, and Section 4.5 identifies them.
The transfer analysis runs in an environment separate from the upstream pipeline's. The
repository's own reproduction check therefore refitted every within-region model and all twenty
directed CORAL transfers against the frozen upstream output. For Manavgat that output is the one
re-frozen on the corrected label (Section 3.2), produced with the upstream pipeline at commit
6381f4c, run unchanged apart from a one-line patch. That patch lets the window-closure module accept
a population column the corrected label adds, and its diff is released with the re-freeze. The
within-region comparisons agree exactly, and the transfer directions to within 1.3×10⁻⁸, under the
repository's pre-existing tolerance of 10⁻⁶. The tolerance that applies if the library version is
not pinned is given in Appendix C.5(vi). The re-freeze and this check were carried out by the
manuscript authors rather than independently by the pipeline's original author. Headline results are repeated across two
populations, three block sizes, the CORAL sweep, both feature sets and four classifier capacities,
and where a conclusion depends on one of those choices **the dependence is reported rather than
resolved by choosing the favourable setting** (Appendices A, C.6).

## 3.14 Same-geography event-to-event comparison (Muğla 2021 versus 2022)

Muğla admits a comparison in which place is held fixed and the event varies: a second fire burned
inside the identical AOI, on the identical grid, eleven months after the first. Signed univariate
AUCs are computed for both arms under the same 10-cell bootstrap used elsewhere. **Season, year and
population all differ**, since the 2022 arm is defined by removing the 2021 scar (Appendices A(m),
C.3).
