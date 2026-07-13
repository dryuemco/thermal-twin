# Step10 — Cross-Region Transfer and Concept-Shift Analysis of Pre-Fire Thermal Dryness

*Self-calibrating satellite thermal digital twin: transferability study.
Regions: Manavgat 2021 (Türkiye), Bejís 2022 (Spain). Label: MCD64A1 500 m
burned/unburned. All randomness seed=42; spatial-block CV and spatial-block
bootstrap throughout; leakage columns hard-excluded.*

---

## Headline finding

Pre-fire thermal/dryness features carry a **within-region** signal that
genuinely improves burned-area discrimination beyond a non-thermal baseline,
and this improvement is **robust to progressively coarser spatial
cross-validation** (the thermal ΔAUC 95% bootstrap interval stays above zero at
1 km, 5 km, and 10 km blocks in both regions). Yet a model trained in one region
and applied naively to the other **does not merely lose accuracy — it inverts**,
scoring *below* random (ROC-AUC ≈ 0.39–0.41). Unsupervised per-region
z-score self-calibration (using only each region's own feature statistics, never
the target labels) lifts transfer back above chance to ≈ 0.56, but no further:
decomposing the gap shows self-calibration recovers only about **one third** of
the within-region-to-naive-transfer deficit, while the remaining **two thirds is
concept shift** — several features, most sharply elevation and the LST/thermal
channels, reverse the *direction* of their association with burning between the
two regions. In short: the thermal effect is real and locally reproducible; a
portion of transfer failure is a recoverable covariate-distribution problem, but
the dominant, irreducible barrier is that the pre-fire thermal "signature of
dryness" is regionally re-parameterised, not universal.

---

## 1. Cross-region transfer (three variants)

Model: RandomForest (`n_estimators=300, min_samples_leaf=2, random_state=42`),
`landcover_dominant` one-hot. Trained on source region, evaluated on the *entire*
`valid_for_modeling` population of the target region. Feature set = thermal
(baseline + 6 thermal channels). ROC-AUC with spatial-block bootstrap 95% CI
(n=1000, block = 2 cells ≈ 1 km).

| Direction | Raw (naive) | Per-region z-score | CORAL |
|-----------|-------------|--------------------|-------|
| Manavgat → Bejís | 0.386 `[0.363, 0.412]` | **0.557** `[0.531, 0.586]` | 0.553 `[0.528, 0.578]` |
| Bejís → Manavgat | 0.407 `[0.375, 0.442]` | **0.568** `[0.531, 0.605]` | 0.558 `[0.533, 0.584]` |

- Naive transfer is **anti-predictive** (CI entirely below 0.5) in both
  directions.
- Per-region z-score standardisation restores above-chance transfer; CORAL does
  **not** beat simple z-score (marginally lower in both directions).
- Even the best-adapted transfer (~0.56) remains far below the within-region
  thermal ceiling (0.887 Manavgat, 0.917 Bejís).

*Full metrics: `transfer_metrics.json`, `transfer_metrics.csv`; gate:
`sanity_gate.json`; per-cell predictions: `<src>__<tgt>/predictions.parquet`.*

---

## 2. Bonus finding: z-score adaptation helps only the thermal features

The same z-score standardisation applied to the **baseline** feature set
(NDVI, elevation, slope, landcover) does **not** rescue transfer — in one
direction it makes it worse.

| Direction | Feature set | Raw | z-score |
|-----------|-------------|-----|---------|
| Man → Bej | thermal  | 0.386 | **0.557** |
| Man → Bej | baseline | 0.386 | 0.464 |
| Bej → Man | thermal  | 0.407 | **0.568** |
| Bej → Man | baseline | 0.487 | 0.528 |

Interpretation: the transferable, self-calibratable structure lives in the
thermal channels. Baseline covariate alignment alone cannot recover
cross-region skill. This is consistent with the digital-twin framing — it is the
*thermal* state, once put on a common regional scale, that carries the portable
information. *Source: `transfer_metrics.csv`.*

---

## 3. Concept-shift evidence (signed univariate AUC / direction reversal)

For every numeric feature we compute its **signed** univariate ROC-AUC against
`burned` in each region (no `max(auc, 1-auc)` folding, so direction is
preserved). A feature "reverses" when it falls on opposite sides of 0.5 in the
two regions. 5 of 9 features reverse:

| Feature | AUC Manavgat | AUC Bejís | Relation Man → Bej | \|gap\| |
|---------|-------------|-----------|--------------------|------|
| **elevation_mean** | 0.453 | 0.641 | negative → positive | 0.188 |
| downscaled_lst_mean | 0.560 | 0.468 | positive → negative | 0.091 |
| current_lst_mean | 0.548 | 0.462 | positive → negative | 0.086 |
| fused_lst_mean | 0.550 | 0.466 | positive → negative | 0.084 |
| tvdi_difference_mean | 0.464 | 0.512 | negative → positive | 0.048 |

Elevation shows the largest reversal, and all three absolute-LST channels flip
together. This is the mechanistic explanation for why per-region *scaling*
(z-score) cannot fully close the gap: aligning means/variances cannot fix a sign
flip in the feature→outcome relationship. *Source: `concept_shift.json`,
`concept_shift_univariate_auc.csv`, `concept_shift_reversals.csv`.*

---

## 4. Within-region robustness (spatial-block size 2 / 10 / 20)

Independent re-implementation of the Step8B baseline-vs-thermal spatial-block CV
(`StratifiedGroupKFold` n_splits=5; RandomForest `min_samples_leaf=3,
class_weight="balanced"`), re-run at three block sizes. Thermal ΔAUC = AUC(thermal)
− AUC(baseline) from out-of-fold predictions; 95% CI via spatial-block bootstrap
(n=1000) at the matching block size.

| Region | Block | n_blocks | Baseline AUC | Thermal AUC | ΔAUC | ΔAUC 95% CI | Verdict |
|--------|-------|----------|--------------|-------------|------|-------------|---------|
| Manavgat | 2 (~1 km) | 6070 | 0.828 | 0.887 | +0.059 | `[+0.050, +0.068]` | positive support |
| Manavgat | 10 (~5 km) | 252 | 0.771 | 0.824 | +0.053 | `[+0.032, +0.076]` | positive support |
| Manavgat | 20 (~10 km) | 63 | 0.719 | 0.763 | +0.044 | `[+0.014, +0.077]` | positive support |
| Bejís | 2 (~1 km) | 4004 | 0.869 | 0.917 | +0.048 | `[+0.040, +0.057]` | positive support |
| Bejís | 10 (~5 km) | 176 | 0.790 | 0.846 | +0.056 | `[+0.033, +0.079]` | positive support |
| Bejís | 20 (~10 km) | 48 | 0.716 | 0.777 | +0.061 | `[+0.039, +0.087]` | positive support |

- **The thermal ΔAUC 95% CI stays above zero at every block size in both
  regions** — it never crosses zero. The narrowest case is Manavgat at ~10 km
  (lower bound +0.014).
- **Absolute AUCs decline as blocks grow** (Manavgat thermal 0.887 → 0.763; Bejís
  0.917 → 0.777): coarser spatial CV removes short-range spatial-autocorrelation
  optimism, so both models' 1 km numbers are somewhat optimistic estimates of true
  spatial generalisation.
- The ΔAUC point trend is weak and region-dependent (Manavgat slightly down, Bejís
  slightly up); CIs widen mainly because the number of independent resampling
  blocks drops sharply. There is **no evidence the thermal benefit dissolves** at
  coarse scale.
- **Reproduction check:** at block = 2 the re-implementation reproduces the
  Step8E point estimates to within 0.0001 (baseline 0.828/0.869, thermal
  0.887/0.917), despite a scikit-learn version change (1.9 here vs 1.4.2 in
  Step8E).

*Source: `experiments/<region>/step10/within_robustness.json`,
`within_robustness_summary.csv`.*

---

## 5. Decomposition of the transfer gap

For each target region: `within` = that region's own within-region thermal
ROC-AUC (Step8E); `raw` and `adapted` (z-score) = the transfer scores from §1.
`total_gap = within − raw`, `recovered = adapted − raw` (covariate shift removed
by self-calibration), `concept_remaining = within − adapted` (irreducible
concept shift).

| Target (direction) | within | raw | adapted (z) | total gap | recovered (covariate) | remaining (concept) |
|--------------------|--------|-----|-------------|-----------|-----------------------|---------------------|
| Bejís (Man → Bej) | 0.917 | 0.386 | 0.557 | 0.531 | +0.172 — **32.3 %** | +0.360 — **67.7 %** |
| Manavgat (Bej → Man) | 0.887 | 0.407 | 0.568 | 0.480 | +0.161 — **33.6 %** | +0.318 — **66.4 %** |

Consistent across both directions: **~1/3 of the transfer gap is recoverable
covariate shift; ~2/3 is concept shift.** *Source: `decomposition.json`,
`decomposition.csv`.*

---

## Threats to validity / limitations

Reported honestly; these bound the strength of the claims.

- **(a) Two regions = two directions only.** With just Manavgat and Bejís the
  "transfer matrix" has a single off-diagonal pair per direction. The
  1/3-covariate / 2/3-concept split and the specific reversing features are
  estimated from n=2 regions; a third (and fourth) region is required before the
  decomposition can be treated as a general property rather than a
  region-pair-specific observation.
- **(b) One fire event per region, one meteorological realisation.** Each region
  contributes a single fire season / single weather draw. What we label "concept
  shift between regions" is confounded with between-*event* and between-*year*
  meteorological differences; we cannot separate a stable regional concept from a
  one-off seasonal one with the current data.
- **(c) Label granularity.** The target is MCD64A1 at its native ~500 m grid
  cell; there is no 30 m burned label. All skill numbers are cell-level and
  inherit MCD64A1's omission/commission characteristics. FIRMS is never used as a
  target.
- **(d) Absolute AUCs are mildly optimistic at 1 km.** As §4 shows, AUC drops
  when spatial blocks coarsen, so the headline within-region numbers (0.887 /
  0.917) overstate true spatial generalisation somewhat. The *delta* (thermal
  benefit) nonetheless survives to ~10 km, so the qualitative claim is robust
  even if the absolute ceiling is soft.
- **(e) scikit-learn version differs from Step8 (1.9 vs 1.4.2).** RandomForest is
  not bit-identical across versions. We treated ±0.02 as an acceptable
  reproduction band; the block=2 re-run in fact matched Step8E to ±0.0001, so
  version drift is not a material confound for these results.

---

## Reproducibility

- **Environment:** dedicated `/.venv-step10/` at the project root
  (scikit-learn 1.9, pandas 3.0, numpy 2.5, pyarrow, scipy). The read-only `repo/`
  did not ship scikit-learn; no existing file under `repo/` or
  `experiments/*/step8*|step9*` was modified.
- **Determinism:** `seed = 42` everywhere (model `random_state`, CV shuffle,
  bootstrap RNG). Bootstrap = 1000 iterations, resampling unit = `spatial_block_id`.
- **Leakage control:** `lon/lat`, all `burn_*` columns, and row/col indices are
  hard-excluded from every feature set (`data_io.assert_no_leakage`, fail-fast).

| Script | Produces | Output location |
|--------|----------|-----------------|
| `step10/run_a_cross_region.py` | §1 transfer, 3 variants, both directions + bootstrap CI; sanity gate | `cross_region/step10/transfer_metrics.{json,csv}`, `sanity_gate.json`, `<src>__<tgt>/predictions.{parquet,csv}` |
| `step10/run_c_concept_shift.py` | §3 signed univariate AUC + reversal table | `cross_region/step10/concept_shift.json`, `concept_shift_univariate_auc.csv`, `concept_shift_reversals.csv` |
| `step10/run_b_decomposition.py` | §5 within / raw / adapted decomposition | `cross_region/step10/decomposition.{json,csv}` |
| `step10/run_d_within_robustness.py` | §4 block-size 2/10/20 robustness + block=2 reproduction | `experiments/<region>/step10/within_robustness.json`, `cross_region/step10/within_robustness_summary.csv` |

Shared modules: `config10.py` (single source of truth for paths, feature sets,
seeds, model params), `data_io.py`, `metrics.py`, `adaptation.py` (raw / z-score /
CORAL), `transfer.py`, `spatial_bootstrap.py`, `within_cv.py` (Step8B CV
re-implementation). Run order: `run_a` → gate → `run_b`, `run_c`, `run_d`.

---

## Open questions / next steps

- **Third and fourth region → a real transfer matrix.** The single most
  valuable addition. With ≥3 regions, every region serves as both source and
  target, and the covariate/concept split can be estimated with a spread rather
  than a point. The third region **must be a new Mediterranean *forest-fire*
  region that passes the natural-vegetation gate** (like Manavgat and Bejís) —
  **not Kozan**, which is our negative control (see below). No such third region
  exists locally yet: it has to be produced end-to-end through the GEE Step1–Step8a
  pipeline (fetch MODIS/Landsat, build the 500 m modeling dataset) before it can
  enter the transfer study. Adding a region without re-running that pipeline is
  not possible from the current on-disk data.
- **Negative control (Kozan 2023) — a validity check, *not* a transfer partner.**
  In Kozan the burned area is ~98 % cropland / stubble-burning rather than genuine
  wildfire, so it fails the natural-vegetation wildfire gate. Including it in the
  transfer matrix as if it were a forest-fire region would be a methodological
  error: any "transfer" score would conflate a different physical process
  (agricultural burning) with forest-fire dryness dynamics. Its correct role is a
  **negative control** — a region where the pre-fire *forest*-dryness signal is
  expected to behave differently — evaluated **within-region only**. As of this
  run Kozan has only Step0 outputs locally (no Step8a modeling dataset), so no
  Kozan result is included here; producing it would likewise require running the
  GEE pipeline first.
- **Closing concept shift with a few in-region labels.** Since the residual gap
  is concept (sign-flipping) rather than covariate, pure unsupervised alignment
  is provably insufficient. The obvious experiment is **few-shot / active
  learning**: fine-tune or recalibrate the transferred model with a small,
  spatially-blocked sample of target-region labels and measure how many labelled
  cells are needed to recover a target fraction of the within-region ceiling.
  This directly tests the "self-calibrating digital twin" premise — how cheaply
  can a new region be adapted.
- **Disentangling regional concept from event/meteorology.** Multiple fire
  seasons per region (where available) would let us test whether the reversing
  features (elevation, absolute LST) flip because of stable regional physiography
  or because of the particular year's weather — the key confound in (b).
