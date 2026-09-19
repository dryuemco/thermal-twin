# Precision analysis for the pre-registration (PREREGISTRATION §11)

**Status:** computed 2026-09-19 from pilot artefacts on the corrected Manavgat labels (inputs in §1). No
outcome of the new study is used. Code: `precision_analysis.py` (seed 42, `.venv-step10`, numpy/scipy/pandas; runtime
about 9 min). Outputs: `pilot_variance_components.{json,csv}`, `precision_table.{csv,json}`,
`precision_results.json` (assumptions, per-scenario components, REML check), `run.log`.

Reproduce: `<thermal-twin>/.venv-step10/Scripts/python.exe design/precision/precision_analysis.py`

## 1. Pilot inputs

| Input | File |
|---|---|
| 20-direction transfer matrix, within-region AUC (1 km blocks) | `paper/labelfix_rerun/pipeline/_derived/matrix_corrected.csv` |
| Per-direction 10-cell (~5 km) spatial-block CIs, AUC and thermal−baseline delta | `design/precision/inputs/transfer_ci_blocksize.csv` (points asserted equal to the matrix, < 6e-5) |
| Within-region at 5 and 10 km blocks (Manavgat, Bejís only) | `paper/labelfix_rerun/pipeline/robustness/step8_large_block/manavgat_2021__bejis_2022/` |
| Within-region increment at 5 km blocks, all 5 regions; scar-frame ladder | `paper/labelfix_rerun/inference/ladder_summary.json` |
| Pooled leave-one-region-out transfer | `paper/labelfix_rerun/code/loro_all.json` |

**Provenance.** The within-direction spatial-block sampling SEs come from
`design/precision/inputs/transfer_ci_blocksize.csv`. That file was produced on the corrected Manavgat labels
by the paper's `transfer_ci_blocksize` computation during the stopped round-3 re-run, where it is
git-ignored (`paper/labelfix_rerun/round3/`); it was copied here unchanged, SHA-256
`33233d2abc2dcf29f7750fb4391daee4f275ecdb7adfc31bdf7d3089fafb4f82`. The other four inputs are committed
pilot artefacts: `paper/labelfix_rerun/pipeline/_derived/matrix_corrected.csv`,
`paper/labelfix_rerun/pipeline/robustness/step8_large_block/manavgat_2021__bejis_2022/`,
`paper/labelfix_rerun/inference/ladder_summary.json` and `paper/labelfix_rerun/code/loro_all.json`.

Sampling SEs are taken from the 10-cell CIs. The 2-cell CIs in the matrix ignore spatial autocorrelation
and are narrower by a median factor of 3.1, so they are not used.

## 2. Pilot variance components (Task 1)

**Within region (V1 analogue), 5 regions.** These have n = 5; the intervals are χ² intervals and assume
normality.
- Between-region SD of within thermal AUC (1 km blocks) is **0.025**, 95 % CI [0.015, 0.071]. After
  removing sampling error it is 0.024.
- Between-region SD of the within thermal increment is **0.039** at 1 km blocks, CI [0.023, 0.112], and
  **0.040** at 5 km blocks, CI [0.024, 0.114]. After removing sampling error it is 0.038.
- Sampling SE of a within AUC at 10 km blocks is 0.038, and of a within increment 0.016. Both are means
  over Manavgat and Bejís. Going from 5 km to 10 km blocks multiplies the SE by 1.57 for AUC and 1.32 for
  the increment.

**Transfer (20 directions).**
- Raw thermal AUC: mean 0.527, observed SD **0.114**.
- z-score: SD 0.080. CORAL: SD 0.064. Baseline: SD 0.113.
- Within-direction sampling SE (10-cell): median **0.032**, IQR 0.028–0.038. For the paired delta the
  median SE is 0.022.

**Crossed REML decomposition.** This is implemented directly, because statsmodels is absent. Each fit uses
the known per-direction sampling variance. The 95 % intervals come from a parametric bootstrap with 1000
refits. The ranges come from leave-one-region-out (LORO) refits.

| Outcome | Model | source | target | pair | dyad (residual) | total |
|---|---|---|---|---|---|---|
| Raw thermal AUC | crossed | 0 [0, .083] | .022 [0, .085] | – | .108 [.057, .141] | .111 |
| Raw thermal AUC | **crossed + pair** | 0 [0, .047] | .016 [0, .054] | **.106 [.042, .161]**; LORO .070–.133 | .038 [0, .062] | .114 |
| V1 − V3 gap | crossed + pair | 0 [0, .063] | .044 [0, .078] | **.104 [.038, .153]** | .039 [0, .067] | .119 |
| Thermal − baseline delta | crossed + pair | 0 [0, .046] | 0 [0, .045] | .016 [0, .056] | **.059 [.014, .075]** | .061 |
| z-score thermal | crossed + pair | .038 [0, .075] | .068 [0, .115] | 0 | .031 | .083 |
| CORAL thermal | crossed + pair | .041 | .052 | 0 | 0 | .066 |

**The key finding: the heterogeneity of raw transfer is reciprocal and pair-level, not source or target.**
If region A transfers poorly to region B, then B also transfers poorly to A. The dyadic residuals of the
plain crossed model correlate at +0.82 across the 10 pairs. Adding an unordered-pair term improves the
REML fit a great deal: LRT 9.9, boundary p ≈ 0.001 for AUC; 8.5, p ≈ 0.002 for the gap.

With 5 regions, the individual components are poorly identified. Every source and target interval
includes 0. The pair SD is the only one whose interval excludes 0, and it stays in 0.070–0.133 in every
LORO refit.

The paired thermal-minus-baseline delta behaves differently. It is asymmetric and dyad-level, with SD
0.06 and little pair structure.

## 3. Expected precision (Task 2)

The central scenario is 10 tiles and 4 seasons, with the assumption values in §5. "Model" means:
- for contrasts involving V3: the crossed source × target + pair RE model, GLS SE at the true components,
  t with T − 1 df;
- for per-tile contrasts: the tile random-effect model.

"Boot" is the tile-cluster bootstrap. For V3 it resamples tiles in both roles (the pigeonhole bootstrap)
and uses percentile limits. Each bootstrap cell is 2000 simulated studies × 1000 resamples.

Power is P(95 % CI excludes 0). Equivalence is TOST, i.e. the 90 % CI lies inside ±M. For mean V3 the
effect is AUC − 0.5.

| Contrast | Method | Half-width | Coverage | Power δ=.02 | δ=.05 | δ=.10 | P(equiv ±.05) δ=0 / .02 | P(equiv ±.02) δ=0 | MDE80 |
|---|---|---|---|---|---|---|---|---|---|
| V1 − V3 | model | 0.050 | 0.95* | .13 | .52 | .98 | .32 / .22 | 0 | **0.070** |
| V1 − V3 | boot | 0.057 | 0.98 | .07 | .40 | .97 | .16 / .12 | 0 | 0.078 |
| V1 − V2 (k=1) | model | 0.071 | – | .09 | .30 | .81 | 0 / 0 | 0 | **0.099** |
| V1 − V2 (k=1) | boot | 0.056 | **0.89** | .16 | .43 | .89 | .14 / .12 | 0 | 0.087 |
| V2 − V3 (k=1) | model | 0.085 | – | .08 | .22 | .66 | 0 / 0 | 0 | **0.118** |
| V2 − V3 (k=1) | boot | 0.076 | 0.95 | .08 | .26 | .73 | .02 / .01 | 0 | 0.108 |
| Group contribution to V3 | model | 0.015 | 0.99* | .75 | 1 | 1 | 1 / .99 | .71 | **0.021** |
| Group contribution to V3 | boot | 0.022 | 0.995 | .42 | 1 | 1 | 1 / .94 | .27 | 0.028 |
| Group contribution to V1 | model | 0.028 | – | .31 | .95 | 1 | .95 / .72 | 0 | **0.039** |
| Group contribution to V1 | boot | 0.022 | 0.91 | .45 | .98 | 1 | .99 / .81 | .16 | 0.033 |
| Mean V3 (vs 0.5) | model | 0.039 | 0.997* | .18 | .73 | 1 | .68 / .43 | 0 | **0.055** |
| Mean V3 (vs 0.5) | boot | 0.054 | 0.995 | .04 | .45 | .99 | .29 / .18 | 0 | 0.069 |

\* Realised coverage when the components are re-estimated by REML in each of 300 simulated studies,
using the model with the pair term. The same check for **the crossed model without the pair term of
PREREGISTRATION §11.1** gives coverage **0.92 for mean V3 and 0.90 for V1 − V3**, with half-widths 0.032 and 0.044.

**Half-width by number of tiles (central, S = 4; model / boot):**

| T | 8 | 10 | 12 | 15 |
|---|---|---|---|---|
| V1 − V3 | .063 / .070 | .050 / .057 | .042 / .049 | .035 / .041 |
| V1 − V2 (k = 0.5 / 1 / 1.5, model) | .047 / .083 / .121 | .040 / .071 / .104 | .036 / .063 / .092 | .031 / .055 / .080 |
| V2 − V3 (k = 0.5 / 1 / 1.5, model) | .075 / .102 / .134 | .061 / .085 / .113 | .053 / .074 / .100 | .044 / .063 / .086 |
| Group contribution to V3 | .020 / .027 | .015 / .022 | .012 / .018 | .010 / .014 |
| Mean V3 | .051 / .067 | .039 / .054 | .032 / .044 | .025 / .036 |

**Seasons barely matter.** Going from 3 to 5 seasons changes each half-width by ≤ 0.005, because the
persistent tile and pair components dominate and seasons only average the sampling error.

**Sensitivity at T = 10, S = 4 (model half-width):**
- The sampling-SE multiplier g from 0.7 to 2 moves every contrast by ≤ 0.01.
- Treating half of the spatial variance as season-specific (persist = 0.5) shrinks V3 contrasts by about
  0.01.
- π = 1 (all temporal variance persistent per tile) raises V1 − V2 to 0.088.
- Using the 80th-percentile pilot components raises:
  - V1 − V3 to 0.063;
  - group contribution to V3 to 0.034;
  - group contribution to V1 to 0.082 (this row uses the χ² 97.5 % upper bound of the increment SD, so it
    is harsher than p80).
- The combined pessimistic case (p80 components, k = 1.5, g = 1.5) gives V1 − V2 0.126 and V2 − V3 0.138.

## 4. Minimum detectable effects at 80 % power (Task 3), T = 10, S = 4

Values are for the model / boot. The range in brackets runs from the p80-component case to T = 15.

| Contrast | MDE80 |
|---|---|
| V1 − V3 | **0.070** / 0.078 (p80: 0.087; T = 15: 0.049) |
| V1 − V2 | **0.099** / 0.087 at k = 1; 0.056 at k = 0.5; 0.144 at k = 1.5 |
| V2 − V3 | **0.118** / 0.108 at k = 1; 0.086 at k = 0.5; 0.158 at k = 1.5 |
| Group contribution to V3 | **0.021** / 0.028 (p80: 0.047) |
| Group contribution to V1 | **0.039** / 0.033 (upper-bound SD: 0.114) |
| Mean V3 − 0.5 | **0.055** / 0.069 |

**What this means.** At 10 tiles the design can:
- estimate group contributions to about ±0.02;
- detect a V1 − V3 gap of 0.07. The pilot gap was about 0.37, so the gap itself is not in doubt; only
  its size is.

It **cannot** detect a V1 − V2 or V2 − V3 difference smaller than about 0.10–0.12. It **cannot** establish
equivalence within ±0.02 for any AUC-level contrast, and within ±0.05 only for group contributions. A null
on V2 − V3 therefore has to be reported as a bound of roughly ±0.08, not as "no difference".

## 5. Assumptions, in order of influence

1. **Temporal heterogeneity k is not estimated.** The pilot has one season per region. The temporal-gap
   SD is set to k × the spatial-gap SD (0.119), with k = 0.5 / **1** / 1.5.
   - This one assumption moves V1 − V2 half-widths from 0.040 to 0.104, and V2 − V3 from 0.061 to 0.113.
   - The only pilot-internal proxy points to k ≈ 1: leave-one-scar-out AUCs (same region, another fire)
     are exactly as dispersed as foreign-region AUCs (SD 0.063 vs 0.063; 7 scars, 3 regions). But that is
     a same-season, label-conditioned frame, not temporal transfer.
   - No external anchor was adopted. No verified published inter-annual AUC variance for this model class
     and grid was available to me, and I did not invent one.
   - Recommendation (adopted: PREREGISTRATION §4.8(c)): re-run this analysis after the label-free stage using the observed number of
     eligible seasons, and pre-register k = 1.5 as the planning value if a conservative choice is wanted.
2. **Pilot components come from 5 regions.** Source and target SDs cannot be told apart from 0. The
   pair SD's 95 % interval is [0.04, 0.16]. The p80 scenario shows the cost: +0.013 on V1 − V3, doubled
   group-contribution half-widths.
3. **The pair (reciprocal) structure is real in the pilot, and it decides which inference is valid.**
   - The crossed model without the pair term of PREREGISTRATION §11.1 under-covers: 0.90–0.92.
   - The target-only cluster bootstrap under-covers: 0.79–0.90.
   - The two-way (pigeonhole) tile bootstrap is conservative, 0.98–0.995. It over-counts pair variance,
     which costs about 0.01–0.015 in half-width.
   - The percentile one-way tile bootstrap under-covers at 10 tiles (0.89–0.91) for per-tile contrasts.
   - **Recommendation for the registration (adopted: PREREGISTRATION §11.1):** add an unordered-pair random effect to the crossed model and
     make that model primary; keep the two-way tile bootstrap as the conservative check; do not use a
     target-only bootstrap; use t(T − 1) or a bias-corrected interval for per-tile contrasts.
4. **Group-ablation heterogeneity uses one proxy:** the pilot's thermal-plus-baseline increment. Removing
   one of seven groups may give smaller and less variable deltas.
5. **Seasonal persistence of spatial components** (central: fully persistent, which is conservative),
   **ρ(temporal, spatial) = 0** (conservative; 0.5 reduces V2 − V3 to 0.073), and the **sampling-SE
   scaling** to ≥ 10 km blocks (×1.57 from Manavgat and Bejís; smaller fires handled by g ≤ 2) all have
   small effects.
6. **Other modelling choices:**
   - V3 is modelled as pairwise. Pooled leave-one-tile-out should be at least as precise.
   - Effects are treated as additive location shifts.
   - Levels were measured at 1 km (V1) and 5 km (V3) blocks. Only variances are carried over, not levels.
