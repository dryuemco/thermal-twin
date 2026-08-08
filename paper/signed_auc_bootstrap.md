# Signed univariate AUC with spatial-block bootstrap intervals — three regions

**What this is.** Signed univariate ROC-AUC of each predictor against `burned`, per region, in the
natural-vegetation population, with a **spatial-block bootstrap** 95% confidence interval. This is
the C4 concept-shift diagnostic (POSITIONING.md §4) that was previously available only as point
estimates; the intervals turn "point reversal" into either **bootstrap-supported reversal** or "not
established".

**Method.** Signed AUC = P(feature higher on a burned cell than on an unburned cell), rank-based,
**no** `max(auc, 1−auc)` folding, so >0.5 means higher predictor values go with burning and <0.5
means the opposite. Bootstrap resamples **spatial blocks** (block = 10 native cells ≈ 5 km, matching
`row_500m`/`col_500m` blocking used in the pipeline's `run_c` / `step9g`), 1000 replicates, seed 42,
equal-tailed 2.5/97.5 percentile CI. A block drawn *k* times contributes its cells *k* times.

**Provenance and honesty notes.**
- Computed directly from `experiments/<region>/step8a/step8a_500m_modeling_dataset.parquet`
  (extracted from archive part `-1-002`), read with the pure-JS `hyparquet` reader under Node, since
  no Python environment exists on this machine. Script: `paper/signed_auc_bootstrap.mjs`; raw
  output: `paper/signed_auc_bootstrap.json`.
- **The PRNG is `mulberry32`, not NumPy's Generator**, so replicate draws are not bit-identical to
  the pipeline's `run_c`. The *procedure* (block resampling, 1000×, ~5 km blocks, percentile CI) is
  identical.
- **Reproduction check against the frozen pipeline.** Point estimates reproduce `step9e` exactly.
  The CIs reproduce the values in `CLAUDE.md`'s §3 to ~0.01 despite the different RNG — e.g.
  elevation Manavgat here `0.374 [0.292, 0.469]` vs pipeline `0.374 [0.290, 0.472]`; elevation Bejís
  here `0.643 [0.560, 0.721]` vs pipeline `0.643 [0.559, 0.727]`; current_lst Manavgat here
  `0.538 [0.456, 0.615]` vs pipeline `0.538 [0.450, 0.619]`. This independent re-implementation
  therefore validates the pipeline's own bootstrap.
- **`[BLOCKED: Evia]`** North Evia's parquet is in a missing archive part (001/003/004/005), so Evia
  is absent here. This is a **three-region** table; it must be re-run with Evia and re-verified from
  the final complete export before the manuscript uses it. Even then, Evia's 67% prevalence
  (`RESULTS_INVENTORY.md` §1.1) may make its signed AUCs non-comparable.

---

## Table — signed AUC (95% spatial-block-bootstrap CI), natural vegetation

| Feature | Manavgat | Bejís | Muğla |
|---|---|---|---|
| `ndvi_mean` | 0.636 [0.586, 0.680] | 0.559 [0.491, 0.629] | 0.662 [0.620, 0.705] |
| `elevation_mean` | 0.374 [0.292, 0.469] | 0.643 [0.560, 0.721] | 0.611 [0.532, 0.691] |
| `slope_mean` | 0.531 [0.429, 0.639] | 0.521 [0.438, 0.616] | 0.637 [0.584, 0.688] |
| `current_lst_mean` | 0.538 [0.456, 0.615] | 0.477 [0.396, 0.543] | 0.325 [0.270, 0.383] |
| `current_tvdi_mean` | 0.552 [0.463, 0.632] | 0.517 [0.432, 0.594] | 0.336 [0.271, 0.405] |
| `tvdi_difference_mean` | 0.449 [0.388, 0.504] | 0.512 [0.442, 0.579] | 0.490 [0.400, 0.579] |
| `downscaled_lst_mean` | 0.552 [0.466, 0.629] | 0.484 [0.397, 0.555] | 0.307 [0.251, 0.366] |
| `fused_lst_mean` | 0.540 [0.457, 0.617] | 0.481 [0.400, 0.548] | 0.325 [0.270, 0.383] |
| `lst_anomaly_mean` | 0.482 [0.427, 0.532] | 0.418 [0.358, 0.470] | 0.485 [0.396, 0.568] |

Sample sizes: Manavgat n=20 511 (784 burned, 237 blocks); Bejís n=15 190 (1 100 burned, 176
blocks); Muğla n=41 730 (2 911 burned, 576 blocks).

---

## Bootstrap-supported reversals (two regions' CIs disjoint)

A reversal counts as **bootstrap-supported** only when the two regions' ~5 km-block 95% CIs do not
overlap. A **sign flip** additionally requires the two point estimates to fall on opposite sides of
0.5.

**Manavgat vs Muğla — five disjoint-CI features, four of them sign flips:**

| Feature | Manavgat | Muğla | Type |
|---|---|---|---|
| `elevation_mean` | 0.374 [0.292, 0.469] | 0.611 [0.532, 0.691] | **sign flip** |
| `current_lst_mean` | 0.538 [0.456, 0.615] | 0.325 [0.270, 0.383] | **sign flip** |
| `current_tvdi_mean` | 0.552 [0.463, 0.632] | 0.336 [0.271, 0.405] | **sign flip** |
| `downscaled_lst_mean` | 0.552 [0.466, 0.629] | 0.307 [0.251, 0.366] | **sign flip** |
| `fused_lst_mean` | 0.540 [0.457, 0.617] | 0.325 [0.270, 0.383] | **sign flip** |

**Bejís vs Muğla — four disjoint-CI features, one sign flip:**

| Feature | Bejís | Muğla | Type |
|---|---|---|---|
| `current_tvdi_mean` | 0.517 [0.432, 0.594] | 0.336 [0.271, 0.405] | **sign flip** |
| `current_lst_mean` | 0.477 [0.396, 0.543] | 0.325 [0.270, 0.383] | magnitude only (both ≤0.5) |
| `downscaled_lst_mean` | 0.484 [0.397, 0.555] | 0.307 [0.251, 0.366] | magnitude only |
| `fused_lst_mean` | 0.481 [0.400, 0.548] | 0.325 [0.270, 0.383] | magnitude only |

**Manavgat vs Bejís — one disjoint-CI feature (the original n=2 finding):**

| Feature | Manavgat | Bejís | Type |
|---|---|---|---|
| `elevation_mean` | 0.374 [0.292, 0.469] | 0.643 [0.560, 0.721] | **sign flip** |

---

## What changed relative to the two-region analysis

The frozen two-region summary (`CLAUDE.md` §3) concluded: *only `elevation_mean`'s reversal is
bootstrap-supported; the four LST/TVDI reversals are point reversals whose CIs overlap.* With Muğla
added, that conclusion is superseded:

1. **The four absolute thermal channels now reverse with bootstrap support** — all of
   `current_lst`, `current_tvdi`, `downscaled_lst`, `fused_lst` sign-flip between Manavgat and Muğla
   with disjoint 95% CIs. What was "suggestive but not statistically established at n=2" is
   established at n=3, because Muğla drives the absolute channels hard below chance
   (0.31–0.34, CIs entirely below 0.5) while Manavgat holds them above 0.5.

2. **Elevation is a Manavgat-specific dissent, not a general reversing feature.** Its sign flip is
   bootstrap-supported in *both* comparisons that involve Manavgat (vs Bejís and vs Muğla), but
   Bejís and Muğla agree with each other (0.643 and 0.611, CIs overlapping), so the reversal is
   between Manavgat and the-rest, not a pairwise-general phenomenon.

3. **The static baseline block never reverses; the thermal block does.** `ndvi_mean` and
   `slope_mean` stay ≥0.5 in all three regions with no bootstrap-supported reversal anywhere; the
   absolute thermal channels cross 0.5 with disjoint CIs. This is the paper's thesis (the block that
   gains the most locally is the block whose direction is least stable) established at the level of
   individual predictors, now with intervals rather than point estimates.

4. **Anomaly-referenced channels are the most stable thermal features.** `lst_anomaly_mean`
   (0.418–0.485) and `tvdi_difference_mean` (0.449–0.512) have overlapping CIs across regions and no
   bootstrap-supported reversal — weak signals, but stable ones — whereas the absolute channels
   swing hardest. Referencing a variable to its own local baseline buys direction stability at the
   cost of strength. Note also that TVDI's *internal* normalisation does **not** protect it:
   `current_tvdi_mean` sign-flips with bootstrap support in both Manavgat–Muğla and Bejís–Muğla.

**Consequence for the manuscript.** The C4 conditional diagnostic is now an interval-backed result
for three regions, not a point-estimate observation. `RESULTS_INVENTORY.md` §5b.1's caveat ("these
are point estimates with no intervals … before any reversal can be called bootstrap-supported") is
discharged for the three available regions. The forward references in `01_introduction.md` §1.3 and
`02_related_work.md` §2.3 to a conditional diagnostic that "tracks what the marginal ones miss" are
now supported by data on the conditional side; the marginal (area-of-applicability) side still has
to be computed before the full contrast in those passages can stand.
