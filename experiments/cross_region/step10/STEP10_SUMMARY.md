# Step10 — Cross-Region Transfer and Concept-Shift Analysis of Pre-Fire Thermal Dryness

*Self-calibrating satellite thermal digital twin: transferability study.
Regions: Manavgat 2021 (Türkiye), Bejís 2022 (Spain). Label: MCD64A1 500 m
burned/unburned. All randomness seed=42; spatial-block CV and spatial-block
bootstrap throughout; leakage columns hard-excluded.*

> **Primary population = natural vegetation.** Following the project's own
> confound rule, the **primary** analysis is restricted to natural-vegetation
> cells (`valid_for_modeling == True AND burnable_tree_shrub_grass == True`) to
> exclude the cropland / bare-surface confound. The former mixed `all_valid`
> population is retained as a **secondary / sensitivity** analysis in each section.
> Primary transfer RF matches Step8B / Emrehan exactly:
> `n_estimators=300, max_depth=None, min_samples_leaf=3, class_weight="balanced",
> random_state=42`. The old `min_samples_leaf=2` (no class weight) RF is kept as a
> sensitivity profile.

---

## Headline finding

Pre-fire thermal/dryness features carry a **within-region** signal that
genuinely improves burned-area discrimination beyond a non-thermal baseline, and
this improvement is **robust to progressively coarser spatial cross-validation**
(the thermal ΔAUC 95% bootstrap interval stays above zero at 1 km, 5 km and 10 km
blocks in both regions, in the natural-vegetation population and in the mixed
population alike).

**Transfer across regions, however, fails and is not reliably rescued.** In the
natural-vegetation population a model trained in one region and applied naively to
the other scores at or **below** chance (ROC-AUC 0.32 Man→Bej, 0.44 Bej→Man).
Unsupervised, label-blind adaptation — per-region z-score, or CORAL after
region-wise z-score, using only each region's own feature statistics and never the
target labels — **improves the numbers but cannot push transfer reliably above
chance**: the best variant (CORAL) reaches only ≈ 0.51–0.56, and **only one of the
two directions (Bej→Man CORAL, 0.557 `[0.529, 0.586]`) has a 95% CI entirely above
0.5**; the other adapted scores straddle or sit below chance. Against a
within-region thermal ceiling of 0.87–0.92, the remaining gap is overwhelming.

Decomposition shows why: on natural vegetation, the **best** unsupervised
alignment (CORAL) recovers only about a quarter to a third of the transfer deficit
(31% Man→Bej, 27% Bej→Man), leaving **~69–73% as concept shift** — features reverse
the *direction* of their association with burning between the two regions. At a
spatial-block (~5 km) bootstrap scale, **only `elevation_mean`'s reversal is
bootstrap-supported** (disjoint 95% CIs); the four LST/TVDI reversals are
point-reversals whose CIs overlap. Concept shift is the dominant, irreducible
barrier, and label-free alignment provably cannot close a sign flip.

**A note on the single above-chance result.** The one adapted score with a CI
fully above 0.5 (Bej→Man CORAL) is **conditional on the CORAL regularization λ**: it
holds for λ ∈ {1e-5, 1e-3, 1e-1} but **collapses to chance at λ = 1** (0.485, CI
straddles 0.5). λ=1e-5 is Emrehan's/our defensible choice (minimal regularization =
strongest covariance alignment), and the result is stable across three orders of
magnitude of small λ — but it is not λ-independent, and heavy regularization erases
it. See §6.

**Critical caveat on the earlier "recovery" result.** In the *mixed* `all_valid`
population, z-score adaptation *does* lift thermal transfer above 0.5 (≈ 0.54–0.59
at the same RF). That above-chance "recovery" **does not survive** restriction to
natural vegetation (≈ 0.45–0.48). The contrast (see §2) indicates the apparent
self-calibration benefit in the mixed population is **largely a land-cover
composition artefact**, not portable thermal-dryness skill. The previous
"self-calibration recovers ~1/3 of the gap" framing is therefore withdrawn as the
headline; it holds only for the confounded mixed population.

---

## 1. Cross-region transfer (three variants) — PRIMARY (natural vegetation)

Trained on source region, evaluated on the target region's **natural-vegetation**
population. Feature set = thermal (baseline + 6 thermal channels). RF as above.
ROC-AUC with spatial-block bootstrap 95% CI (n=1000, block = 2 cells ≈ 1 km).
CORAL = `coral_after_regionwise_zscore` (region-wise z-score, then CORAL aligns the
source covariance to the target with λ=1e-5; the target stays z-scored, unchanged).

| Direction | Raw (naive) | Per-region z-score | CORAL |
|-----------|-------------|--------------------|-------|
| Manavgat → Bejís | 0.3245 `[0.304, 0.348]` | 0.4834 `[0.455, 0.509]` | **0.5108** `[0.486, 0.534]` |
| Bejís → Manavgat | 0.4444 `[0.411, 0.477]` | 0.4520 `[0.413, 0.489]` | **0.5571** `[0.529, 0.586]` |

- Naive transfer is at/below chance in both directions (Man→Bej CI entirely below
  0.5; Bej→Man point 0.44).
- z-score does **not** restore above-chance transfer here: 0.4834 (CI straddles 0.5)
  and 0.4520 (CI **entirely below** 0.5).
- CORAL is the best variant and slightly beats z-score, but reaches only ~0.51–0.56;
  **only Bej→Man CORAL has a CI fully above 0.5.** Man→Bej CORAL (0.5108) straddles it.
- Even the best-adapted transfer (~0.56) is far below the within-region thermal
  ceiling (0.870 Manavgat, 0.918 Bejís, natural vegetation).

**Reproduction against Emrehan's pipeline (primary population).** raw and z-score
match Yunus's independent replication within tolerance (raw ±0.03, z-score ±0.01;
observed deviations 0.005–0.028 and 0.000–0.003). CORAL matches Emrehan's pipeline
to ±0.002 (0.511 / 0.555) after aligning our CORAL to his exact definition
(λ=1e-5, `np.cov` ddof=0). *Full check: `reproduction_check.json`.*

### 1b. Sensitivity: same table, other configurations (thermal set)

| Config (population, RF) | Man→Bej z | Man→Bej CORAL | Bej→Man z | Bej→Man CORAL |
|-------------------------|-----------|---------------|-----------|---------------|
| **PRIMARY** burnable, msl3+bal | 0.4834 | 0.5108 | 0.4520 | 0.5571 |
| all_valid, msl3+bal | 0.5423 | 0.5101 | 0.5907 | 0.6066 |
| all_valid, msl2 (old Step10) | 0.5575 | 0.5507 | 0.5684 | 0.5516 |
| burnable, msl2 | 0.5264 | 0.5735 | 0.4324 | 0.4905 |

The old Step10 headline numbers reproduce in the `all_valid, msl2` row
(z-score 0.558 / 0.568, matching the previously reported 0.557 / 0.568).
*Full metrics: `transfer_metrics.json`, `transfer_metrics.csv`; per-cell
predictions: `<config>/<src>__<tgt>/predictions.parquet`.*

---

## 2. Population contrast: the z-score "recovery" is a land-cover artefact

Holding the RF **fixed** (msl3+balanced) and varying only the population isolates
the effect of land-cover composition on the apparent adaptation benefit.

| Population (fixed RF) | Man→Bej z-score | Bej→Man z-score |
|-----------------------|-----------------|-----------------|
| `all_valid` (mixed: incl. cropland/bare) | **0.5423** (above 0.5) | **0.5907** (above 0.5) |
| `burnable_tree_shrub_grass` (natural veg, PRIMARY) | 0.4834 (below 0.5) | 0.4520 (below 0.5) |

Same classifier, same features, same adaptation — **only the population differs.**
z-score lifts thermal transfer above chance in the mixed population but **not** in
natural vegetation. This is direct evidence that the above-chance "self-calibrated
recovery" reported previously is driven largely by **land-cover composition
differences between regions**, not by portable pre-fire thermal-dryness skill. The
honest reading: on the scientifically defensible natural-vegetation population,
unsupervised adaptation does **not** reliably recover cross-region skill.

Baseline-only feature set (natural vegetation) confirms there is no covariate-only
rescue either: Man→Bej z-score 0.407, Bej→Man z-score 0.442 — both below chance.
*Source: `transfer_metrics.csv`.*

---

## 3. Concept-shift evidence (signed univariate AUC + bootstrap CI)

For every numeric feature we compute its **signed** univariate ROC-AUC against
`burned` in each region's natural-vegetation population (no `max(auc, 1-auc)`
folding, so direction is preserved), with a **spatial-block bootstrap** 95% CI
(n=1000, **block = 10 cells ≈ 5 km**, matching Emrehan's `step9g`). A feature
"reverses" when its point AUC falls on opposite sides of 0.5 in the two regions; a
reversal is **bootstrap-supported** only when the two regions' spatial-block CIs are
**disjoint** (otherwise "point reversal").

> **Correction.** An earlier version used a 1 km (2-cell) bootstrap, which ignores
> short-range spatial autocorrelation and produced CIs ~4× too narrow (e.g.
> elevation Manavgat `[0.352, 0.398]` vs the correct `[0.290, 0.472]`). That
> artefact wrongly marked all 5 reversals "bootstrap-supported". At the proper
> ~5 km block scale, **only elevation survives** — the same conservative conclusion
> as Emrehan's independent implementation.

**5 of 9 features reverse by point estimate; only 1 (elevation) is
bootstrap-supported, 4 are point-only:**

| Feature | AUC Manavgat (CI) | AUC Bejís (CI) | Relation Man → Bej | Support |
|---------|-------------------|----------------|--------------------|---------|
| **elevation_mean** | 0.374 `[0.290, 0.472]` | 0.643 `[0.559, 0.727]` | negative → positive | **bootstrap-supported** |
| current_lst_mean | 0.538 `[0.450, 0.619]` | 0.477 `[0.405, 0.540]` | positive → negative | point reversal |
| downscaled_lst_mean | 0.552 `[0.460, 0.635]` | 0.484 `[0.405, 0.553]` | positive → negative | point reversal |
| fused_lst_mean | 0.540 `[0.452, 0.621]` | 0.481 `[0.407, 0.544]` | positive → negative | point reversal |
| tvdi_difference_mean | 0.449 `[0.385, 0.507]` | 0.512 `[0.446, 0.581]` | negative → positive | point reversal |

Elevation shows by far the largest, most significant reversal (gap 0.27, CIs
disjoint even at ~5 km). The absolute-LST channels all flip in point estimate and
in the same direction, but their spatial-block CIs overlap, so they are suggestive,
not statistically established, on n=2 regions. This is still the mechanistic reason
per-region *scaling* cannot close the gap — aligning means/variances cannot fix a
**sign flip** — but the honest strength of evidence is: elevation established,
LST/TVDI suggestive. *Source: `concept_shift.json`,
`concept_shift_univariate_auc.csv`, `concept_shift_reversals.csv`.*

---

## 4. Within-region robustness (spatial-block size 2 / 10 / 20)

Independent re-implementation of the Step8B baseline-vs-thermal spatial-block CV
(`StratifiedGroupKFold` n_splits=5; RandomForest `min_samples_leaf=3,
class_weight="balanced"`), re-run at three block sizes on the **natural-vegetation**
population. Thermal ΔAUC = AUC(thermal) − AUC(baseline) from out-of-fold
predictions; 95% CI via spatial-block bootstrap (n=1000) at the matching block size.

| Region | Block | n_blocks | Baseline AUC | Thermal AUC | ΔAUC | ΔAUC 95% CI | Verdict |
|--------|-------|----------|--------------|-------------|------|-------------|---------|
| Manavgat | 2 (~1 km) | 5439 | 0.803 | 0.870 | +0.067 | `[+0.055, +0.078]` | positive support |
| Manavgat | 10 (~5 km) | 237 | 0.747 | 0.798 | +0.050 | `[+0.023, +0.078]` | positive support |
| Manavgat | 20 (~10 km) | 60 | 0.682 | 0.731 | +0.049 | `[+0.015, +0.086]` | positive support |
| Bejís | 2 (~1 km) | 3967 | 0.862 | 0.918 | +0.056 | `[+0.048, +0.065]` | positive support |
| Bejís | 10 (~5 km) | 176 | 0.779 | 0.825 | +0.046 | `[+0.019, +0.069]` | positive support |
| Bejís | 20 (~10 km) | 48 | 0.738 | 0.795 | +0.057 | `[+0.031, +0.090]` | positive support |

- **The thermal ΔAUC 95% CI stays above zero at every block size in both
  regions** — it never crosses zero. Narrowest lower bound: Manavgat ~10 km, +0.015.
- **Absolute AUCs decline as blocks grow** (Manavgat thermal 0.870 → 0.731; Bejís
  0.918 → 0.795): coarser spatial CV removes short-range spatial-autocorrelation
  optimism, so the 1 km numbers are somewhat optimistic estimates of true spatial
  generalisation.
- The ΔAUC point trend is weak and region-dependent; **no evidence the thermal
  benefit dissolves** at coarse scale.
- **Reproduction check (block = 2):** the re-implementation reproduces the Step8E
  natural-vegetation point estimates to within 0.0001 (baseline 0.803/0.862,
  thermal 0.870/0.918), despite a scikit-learn version change (1.9 here vs 1.4.2 in
  Step8E).

**Sensitivity (`all_valid`):** the thermal ΔAUC CI is likewise above zero at all
three block sizes in both regions (Manavgat +0.059 → +0.044, Bejís +0.048 →
+0.061; all CIs > 0). So the within-region thermal benefit is robust in both
populations. *Source: `experiments/<region>/step10/within_robustness.json`
(`by_population`), `within_robustness_summary.csv`.*

---

## 5. Decomposition of the transfer gap — PRIMARY (natural vegetation)

For each target region (natural vegetation): `within` = that region's own
within-region thermal ROC-AUC (Step8E, `burnable_tree_shrub_grass`); `raw` and
`adapted` = the transfer scores from §1. `total_gap = within − raw`,
`recovered = adapted − raw`, `concept_remaining = within − adapted`. **All three
components are on the same population and same RF**, which is what makes the
decomposition valid.

**The recoverable fraction is defined by the *best* unsupervised method** — the
question is "how much of the gap can label-free alignment close?", whose answer is
"as much as the best label-free method achieves", i.e. CORAL (which beats z-score
in both directions). Primary table uses CORAL; z-score kept as a secondary row.

| Target (direction) | within | raw | adapted | total gap | recovered | remaining (concept) |
|--------------------|--------|-----|---------|-----------|-----------|---------------------|
| **Bejís (Man → Bej), CORAL (best)** | 0.918 | 0.324 | 0.511 | 0.593 | +0.186 — **31%** | +0.407 — **69%** |
| **Manavgat (Bej → Man), CORAL (best)** | 0.870 | 0.444 | 0.557 | 0.425 | +0.113 — **27%** | +0.313 — **73%** |
| Bejís (Man → Bej), z-score (secondary) | 0.918 | 0.324 | 0.483 | 0.593 | +0.159 — 27% | +0.434 — 73% |
| Manavgat (Bej → Man), z-score (secondary) | 0.870 | 0.444 | 0.452 | 0.425 | +0.008 — 2% | +0.418 — 98% |

Using the best unsupervised method (CORAL), **~27–31% of the transfer gap is
recoverable covariate shift and ~69–73% is unrecoverable concept shift**,
consistent across both directions — more concept-dominated than the earlier
mixed-population estimate (~2/3). (The z-score-based 2% figure understates the
recoverable part and is not the right denominator; it is retained only for
completeness.) *Source: `decomposition.json`, `decomposition.csv`
(`best_unsupervised_variant`, `is_best_unsupervised`).*

---

## 6. CORAL λ-sensitivity — is the one above-chance result robust?

The **only** adapted transfer score with a 95% CI entirely above 0.5 is Bej→Man
CORAL. Because CORAL's alignment strength is governed by the regularization λ
(smaller λ = stronger whitening/recoloring), we sweep λ ∈ {1e-5, 1e-3, 1e-1, 1.0}
(thermal set, natural vegetation, primary RF, spatial-block bootstrap CI).

| λ | Man→Bej CORAL | Bej→Man CORAL | Bej→Man CI above 0.5? |
|---|---------------|---------------|------------------------|
| **1e-5 (primary)** | 0.511 `[0.486, 0.534]` | **0.557** `[0.529, 0.586]` | **yes** |
| 1e-3 | 0.505 `[0.481, 0.528]` | 0.564 `[0.535, 0.592]` | yes |
| 1e-1 | 0.483 `[0.458, 0.506]` | 0.547 `[0.520, 0.578]` | yes |
| 1.0 | 0.478 `[0.450, 0.501]` | **0.485** `[0.450, 0.520]` | **no (straddles)** |

(z-score reference, λ-independent: Man→Bej 0.483, Bej→Man 0.452.)

**Reading:** the single above-chance result is **stable across three orders of
magnitude of small λ** (1e-5 → 1e-1) but **collapses to chance at the canonical
λ=1**. So it is not a knife-edge at λ=1e-5, but it is not λ-independent either:
heavy regularization erases it. λ=1e-5 (minimal regularization, strongest
alignment) is the defensible and pre-specified choice, matching Emrehan's pipeline;
we report the dependence openly rather than resting the claim silently on it. The
Man→Bej direction never reaches an above-chance CI at any λ.

**Why λ=1 is not the right default here.** λ=1 is *exactly* the canonical CORAL
regularization of Sun et al. (2016) (`Cs = cov + I`). But that canonical `+I` is
designed for **unstandardized** features; here CORAL is applied **after region-wise
z-score**, so each feature already has variance ≈ 1 — adding `+I` then **doubles the
diagonal** and imposes disproportionately heavy shrinkage, washing out the very
covariance structure the alignment is meant to use. With only d=9 features and
thousands of samples the covariance is well estimated, so minimal regularization
(λ=1e-5) is the appropriate choice and λ=1 is inappropriately strong *in this
post-standardization setting*. The λ dependence is not hidden — it is reported here
together with this justification. *Source: `coral_lambda_sensitivity.csv`, `.json`.*

---

## Threats to validity / limitations

Reported honestly; these bound the strength of the claims.

- **(a) Two regions = two directions only.** With just Manavgat and Bejís the
  "transfer matrix" has a single off-diagonal pair per direction. The
  covariate/concept split and the specific reversing features are estimated from
  n=2 regions; a third (and fourth) region is required before the decomposition can
  be treated as a general property rather than a region-pair-specific observation.
- **(b) One fire event per region, one meteorological realisation.** Each region
  contributes a single fire season / single weather draw. What we label "concept
  shift between regions" is confounded with between-*event* and between-*year*
  meteorological differences; we cannot separate a stable regional concept from a
  one-off seasonal one with the current data.
- **(c) Label granularity.** The target is MCD64A1 at its native ~500 m grid cell;
  there is no 30 m burned label. All skill numbers are cell-level and inherit
  MCD64A1's omission/commission characteristics. FIRMS is never used as a target.
- **(d) Absolute AUCs are mildly optimistic at 1 km.** As §4 shows, AUC drops when
  spatial blocks coarsen, so the headline within-region numbers (0.870 / 0.918)
  overstate true spatial generalisation somewhat. The *delta* (thermal benefit)
  nonetheless survives to ~10 km, so the qualitative claim is robust.
- **(e) scikit-learn version differs from Step8 (1.9 vs 1.4.2).** RandomForest is
  not bit-identical across versions. We treated ±0.02 as an acceptable reproduction
  band; the block=2 re-run matched Step8E to ±0.0001, so version drift is not a
  material confound.

---

## Reproducibility

- **Environment:** dedicated `/.venv-step10/` at the project root (scikit-learn
  1.9, pandas 3.0, numpy 2.5, pyarrow, scipy). The read-only `repo/` did not ship
  scikit-learn; no existing file under `repo/` or `experiments/*/step8*|step9*` was
  modified.
- **Determinism:** `seed = 42` everywhere (model `random_state`, CV shuffle,
  bootstrap RNG). Bootstrap = 1000 iterations, resampling unit = `spatial_block_id`.
- **Leakage control:** `lon/lat`, all `burn_*` columns, and row/col indices are
  hard-excluded from every feature set (`data_io.assert_no_leakage`, fail-fast).
  `burnable_tree_shrub_grass` is used only as a population **mask**, never a feature.
- **CORAL alignment:** cross-checked against Emrehan's `core/step10_shared.py`
  (`fit_coral_alignment`) — region-wise z-score (ddof=0), then
  `Cs=cov+λI, Ct=cov+λI, A=Cs^{-1/2}Ct^{1/2}, Xs*=Xs_z·A`, λ=`STEP10_CORAL_LAMBDA`
  =1e-5, applied to source only; target unchanged.

| Script | Produces | Output location |
|--------|----------|-----------------|
| `step10/run_a_cross_region.py` | §1 transfer, 3 variants × 2 directions × 4 configs + bootstrap CI; reproduction check | `cross_region/step10/transfer_metrics.{json,csv}`, `reproduction_check.json` (+ `sanity_gate.json`), `<config>/<src>__<tgt>/predictions.{parquet,csv}` |
| `step10/run_c_concept_shift.py` | §3 signed univariate AUC + **~5 km spatial-block** bootstrap CI + reversal support | `cross_region/step10/concept_shift.json`, `concept_shift_univariate_auc.csv`, `concept_shift_reversals.csv` |
| `step10/run_b_decomposition.py` | §5 within / raw / adapted decomposition, **best-unsupervised (CORAL)** primary | `cross_region/step10/decomposition.{json,csv}` |
| `step10/run_d_within_robustness.py` | §4 block-size 2/10/20 robustness, both populations + block=2 reproduction | `experiments/<region>/step10/within_robustness.json`, `cross_region/step10/within_robustness_summary.csv` |
| `step10/run_e_coral_lambda_sensitivity.py` | §6 CORAL λ ∈ {1e-5,1e-3,1e-1,1} sweep + bootstrap CI | `cross_region/step10/coral_lambda_sensitivity.{csv,json}` |

Shared modules: `config10.py` (single source of truth: paths, feature sets, seeds,
populations, RF profiles, CORAL λ), `data_io.py` (population filtering),
`metrics.py`, `adaptation.py` (raw / z-score / coral_after_regionwise_zscore),
`transfer.py`, `spatial_bootstrap.py`, `within_cv.py`. Run order:
`run_a` → reproduction check → `run_b`, `run_c`, `run_d`.

---

## Open questions / next steps

- **Third and fourth region → a real transfer matrix.** The single most valuable
  addition. With ≥3 regions, every region serves as both source and target, and the
  covariate/concept split can be estimated with a spread rather than a point. The
  third region **must be a new Mediterranean *forest-fire* region that passes the
  natural-vegetation gate** — **not Kozan**, which is our negative control. It has
  to be produced end-to-end through the GEE Step1–Step8a pipeline before it can
  enter the transfer study.
- **Negative control (Kozan 2023) — a validity check, *not* a transfer partner.**
  In Kozan the burned area is ~98% cropland / stubble-burning rather than genuine
  wildfire, so it fails the natural-vegetation gate. Its correct role is a
  within-region-only negative control. As of this run Kozan has only Step0 outputs
  locally.
- **Closing concept shift needs labels.** Since the residual gap is concept
  (sign-flipping), unsupervised alignment is provably insufficient — as this run now
  shows directly on natural vegetation. The obvious experiment is **few-shot /
  active learning**: recalibrate the transferred model with a small,
  spatially-blocked sample of target-region labels and measure how many labelled
  cells recover a target fraction of the within-region ceiling.
- **Disentangling regional concept from event/meteorology.** Multiple fire seasons
  per region would let us test whether the reversing features (elevation, absolute
  LST) flip because of stable regional physiography or the particular year's
  weather — the confound in (b).
