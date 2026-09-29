# Observational-layer sensitivities, run on this machine

Four analyses the manuscript recorded as not run, plus one query it wrongly described as cheap.
All were executed with the rebuilt environment of `ENVIRONMENT.md` (Python 3.12.10, NumPy 2.4.4,
pandas 3.0.2, scikit-learn 1.9.0), driving the pipeline's own code at `48b56e7`. Every arm that
has a frozen counterpart reproduces it first, and those reproductions are reported before any new
number.

## 1. Label agreement: are the reversals fringe artefacts?

`burn_date_pixel_agreement_fraction` is the share of a burned cell's positive sub-pixels agreeing
with its modal burn date. It is defined for burned cells only. Restricting to high agreement drops
burned cells labelled on thin evidence, which are disproportionately scar-fringe cells, and leaves
the negative class whole. Bootstrap: 10-cell blocks, 1000 replicates, seed 42, at step9g's
registered specification. The unrestricted arm reproduces the archived step9g AUCs to 1.1e-16.

### elevation_mean, the paper's sharpest reversal

| Region | All burned cells | Agreement >= 0.75 | Agreement >= 0.90 |
|---|---|---|---|
| Manavgat 2021 | **0.374** [0.289, 0.471] | **0.368** [0.284, 0.462] | **0.362** [0.279, 0.460] |
| Bejis 2022 | **0.643** [0.558, 0.729] | **0.642** [0.560, 0.728] | **0.635** [0.550, 0.722] |
| Mugla 2021 | **0.611** [0.531, 0.695] | **0.606** [0.527, 0.690] | **0.602** [0.520, 0.686] |
| North Evia 2021 (ext.) | 0.541 [0.458, 0.632] | 0.544 [0.461, 0.636] | 0.550 [0.463, 0.636] |
| Montiferru 2021 | 0.584 [0.395, 0.762] | 0.567 [0.390, 0.748] | 0.546 [0.380, 0.729] |

Bold marks an interval excluding 0.5. Manavgat stays entirely below, Bejis and Mugla entirely
above, at every threshold. The disjoint-interval contrast survives, and Manavgat moves further
from chance as thin-evidence cells are removed. **The elevation reversal is not a fringe artefact.**

The thermal channels behave the same way. Mugla and Evia keep `current_lst_mean`,
`downscaled_lst_mean`, `fused_lst_mean` and `current_tvdi_mean` entirely below 0.5 at both
thresholds. Two verdicts change, both Montiferru's and both by about 0.005 of an interval bound:
`current_tvdi_mean` from an upper bound of 0.499 to 0.505, `tvdi_difference_mean` from 0.497 to
0.503. Montiferru has the fewest positive-carrying blocks of the five.

## 2. Gap-filled thermal cells

`fused_lst` equals observed Landsat LST outside its gap-filled share. Restricted to cells with a
gap-filled fraction of at most 0.10, re-run through the pipeline's own Step 8B and Step 8C.

| Region | Cells retained | dAUC, full | dAUC, low gap-fill [95 % CI] | Verdict |
|---|---:|---|---|---|
| Manavgat 2021 | 95.4 % | +0.0669 | +0.0721 [+0.061, +0.083] | positive support |
| Bejis 2022 | 85.1 % | +0.0561 | +0.0428 [+0.033, +0.053] | positive support |
| Mugla 2021 | 99.2 % | +0.1157 | +0.1139 [+0.104, +0.123] | positive support |
| North Evia 2021 (ext.) | 98.3 % | +0.1533 | +0.1588 [+0.146, +0.171] | positive support |
| Montiferru 2021 | 99.7 % | +0.1014 | +0.1094 [+0.087, +0.134] | positive support |

The increment keeps bootstrap support everywhere. Bejis moves the most and in the direction the
concern predicts, from +0.0561 to +0.0428; the other four move by at most 0.008. The restriction
changes the population, so these are not paired comparisons.

## 3. The increment without the two coordinate-bearing channels

`downscaled_lst` is a fitted surface whose own inputs include lon, lat, row and col; `fused_lst`
inherits that on its gap-filled share. Both were dropped and the within-region comparison re-run
with the pipeline's Step 8B, its thermal feature list rebound in memory exactly as Step 8D does
for its ablation groups. **The six-channel arm reproduces the frozen metrics with a maximum
absolute difference of exactly 0 in all five regions**, so the harness contributes nothing.

| Region | dAUC, full block | dAUC without the two [95 % CI] | Retained |
|---|---|---|---:|
| Manavgat 2021 | +0.0669 | +0.0629 [+0.051, +0.074] | 94 % |
| Bejis 2022 | +0.0561 | +0.0460 [+0.038, +0.055] | 82 % |
| Mugla 2021 | +0.1157 | +0.0971 [+0.088, +0.107] | 84 % |
| North Evia 2021 (ext.) | +0.1533 | +0.1446 [+0.133, +0.157] | 94 % |
| Montiferru 2021 | +0.1014 | +0.1048 [+0.082, +0.128] | 103 % |

The increment retains 82 % to 103 % of its full-block value without the two channels, so the
coordinate-derived component is not what produces the within-region skill.

## 4. MODIS zero-fill, measured rather than inferred

Exact-zero share of each region's MODIS mean layer. The pipeline's own guard threshold is
`STEP7B_MODIS_SUSPICIOUS_ZERO_FRACTION = 0.05`.

| Region | Finite pixels | Exact zeros | Share | Guard | Water-dominant cell share |
|---|---:|---:|---:|---|---:|
| Manavgat 2021 | 6,390 | 518 | 8.11 % | would reject | 8.3 % |
| Bejis 2022 | 4,187 | 0 | 0.00 % | ok | 0.1 % |
| Mugla 2021 | 19,190 | 7,347 | 38.29 % | would reject | 38.9 % |
| North Evia 2021 (ext.) | 2,614 | 0 | 0.00 % | ok | 57.6 % |
| Montiferru 2021 | 797 | 0 | 0.00 % | ok | 7.4 % |

Manavgat's 8.11 % matches the attestation exactly. **Mugla's 38.29 % is more than four times it
and was previously unmeasured; Bejis has no zeros at all.** Each share tracks that AOI's water
share, so the zero-fill is sea rather than missing observation, and it is absent from the one
inland AOI. The two QC-screened regions carry an explicit -9999 sentinel and no zeros.

## 5. The pre-label exposure query, which is not cheap

Section 5.11(xv) described quantifying the exposure left by the pre-label burn exclusion not
running for Manavgat and Bejis as a cheap query. It is not answerable from the archive at all.
Both the working and the raw MCD64A1 rasters are clipped to each region's label window:

| Region | Positive sub-pixels | DOY range | In label window | In predictor window |
|---|---:|---|---:|---:|
| Manavgat 2021 | 179,667 | 213 to 241 | 179,667 (100 %) | 0 |
| Bejis 2022 | 285,751 | 227 to 237 | 285,751 (100 %) | 0 |
| Mugla 2021 | 759,212 | 210 to 235 | 759,212 (100 %) | 0 |
| North Evia 2021 (ext.) | 751,622 | 215 to 226 | 751,622 (100 %) | 0 |
| Montiferru 2021 | 181,738 | 205 to 219 | 181,738 (100 %) | 0 |

Zero positive sub-pixels lie in any predictor window in any region, so a pre-label detection
leaves no trace to count. Measuring the exposure requires MCD64A1 re-exported unclipped, which is
an upstream re-run rather than a query.


## 6. The CORAL lambda = 1 arm the released sweep cannot run

The released `coral_lambda_sensitivity` tool fixes its lambda grid as a token sequence ending at
1e-1 and asserts its own fit count at import, so the canonical lambda = 1 cannot be added without
editing it. The arm was therefore produced by driving the pipeline's own primitives
(`fit_coral_alignment`, `apply_coral`, `compute_regionwise_zscore_stats`, `apply_regionwise_zscore`
and Step 8B's `build_pipeline`) in the order `step10b` calls them, over the same four directions and
both model families.

**Control.** lambda = 1e-1 recomputed the same way reproduces the frozen sweep with a maximum
absolute ROC-AUC difference of 4.4e-09 over all eight rows, seven of them exactly zero.

| Direction | Family | lambda = 1e-1 | lambda = 1 | Change |
|---|---|---|---|---|
| bejis to mugla | baseline | 0.563636 | 0.574033 | +0.0104 |
| bejis to mugla | thermal | 0.507907 | 0.510365 | +0.0025 |
| mugla to bejis | baseline | 0.596282 | 0.596809 | +0.0005 |
| mugla to bejis | thermal | 0.564220 | 0.559360 | -0.0049 |
| manavgat to mugla | baseline | 0.479255 | 0.471337 | -0.0079 |
| manavgat to mugla | thermal | 0.444946 | 0.444042 | -0.0009 |
| mugla to manavgat | baseline | 0.601110 | 0.597097 | -0.0040 |
| mugla to manavgat | thermal | 0.558554 | 0.574475 | +0.0159 |

No direction changes side of the chance line at lambda = 1, and the largest movement is an
improvement rather than a collapse. Adding lambda = 1 to the grid widens the spread to at most
0.0190 in any direction and 0.0159 within the thermal family, against 0.0139 and 0.0075 over the
released grid alone.

This is the opposite of what the superseded two-region run showed and of what the scale argument in
Section 3.11 predicted. The two are not in direct contradiction: that run used a different region
set, and the sweep's four directions do not include Bejis to Manavgat, where its result sat.
Machine-readable: `paper/coral_lambda1.csv`.
## Provenance

Machine-readable: `paper/observational_sensitivities.json`. Inputs are the frozen
`step8a_500m_modeling_dataset` tables, `data/modis/modis_lst_mean_celsius.tif`,
`validation/labels/mcd64a1_raw.tif`, and for the reproduction checks
`step8b/step8b_model_comparison_metrics.json` and
`diagnostics/step9g_univariate_feature_auc_direction_reversal/*/step9g_univariate_auc_by_region.csv`.
