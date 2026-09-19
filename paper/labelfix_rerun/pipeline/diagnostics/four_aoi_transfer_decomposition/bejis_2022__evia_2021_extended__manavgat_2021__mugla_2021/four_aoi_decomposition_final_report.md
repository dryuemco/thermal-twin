# Multi-AOI transfer gap/recovery decomposition

- Generated: `2026-09-19T09:35:44.075657+00:00`
- Canonical set: `bejis_2022__evia_2021_extended__manavgat_2021__mugla_2021`
- Ordered directions: 12 / 12
- Rows: 96 (direction x model family x adaptation method x metric)

```
raw_gap           = within_target - raw_transfer
adaptation_effect = adapted       - raw_transfer
remaining_gap     = within_target - adapted
recovered_fraction = adaptation_effect / raw_gap
remaining_fraction = remaining_gap     / raw_gap
```

Negative recovery is reported as such and never clipped to zero. Fractions are suppressed only when `raw_gap <= 0`.

## Reproduction of frozen Step10

- Rows compared: 128
- Worst |Δ|: `4.867e-08` (tolerance `1e-06`)
- Reproduces frozen Step10: **True**

## Status distribution

- `negative_recovery`: 54
- `recovery_effect_uncertain`: 6
- `supported_recovery_above_chance`: 12
- `supported_relative_recovery_but_chance_not_excluded`: 24

- Rows with negative recovery: **54**
- Rows hitting the raw-gap guard (`raw_gap <= 0`): **0**
- Replicates excluded by the ratio guard, summed over rows: **0**

## Uncertainty scope

The frozen Step10 bootstrap stores the within-region reference per replicate, resampled jointly with the raw and adapted series on the same target spatial-block replicate. The fraction CIs therefore carry **full joint uncertainty** across the within, raw and adapted terms.

## Bejís <-> Muğla (ROC-AUC), all four combinations

| Direction | Family | Method | within | raw | adapted | raw_gap | effect | recovered | recovered CI | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| bejis_2022_to_mugla_2021 | baseline | zscore+coral | 0.7433 | 0.5922 | 0.5702 | +0.1511 | -0.0221 | -0.146 | [-0.28, -0.04] | negative_recovery |
| bejis_2022_to_mugla_2021 | baseline | zscore | 0.7433 | 0.5922 | 0.5650 | +0.1511 | -0.0273 | -0.180 | [-0.31, -0.06] | negative_recovery |
| bejis_2022_to_mugla_2021 | thermal | zscore+coral | 0.8590 | 0.6185 | 0.5066 | +0.2405 | -0.1118 | -0.465 | [-0.56, -0.37] | negative_recovery |
| bejis_2022_to_mugla_2021 | thermal | zscore | 0.8590 | 0.6185 | 0.5177 | +0.2405 | -0.1007 | -0.419 | [-0.51, -0.34] | negative_recovery |
| mugla_2021_to_bejis_2022 | baseline | zscore+coral | 0.8617 | 0.4507 | 0.6087 | +0.4109 | +0.1580 | +0.385 | [+0.31, +0.44] | supported_recovery_above_chance |
| mugla_2021_to_bejis_2022 | baseline | zscore | 0.8617 | 0.4507 | 0.5739 | +0.4109 | +0.1231 | +0.300 | [+0.22, +0.36] | supported_recovery_above_chance |
| mugla_2021_to_bejis_2022 | thermal | zscore+coral | 0.9178 | 0.5832 | 0.5603 | +0.3346 | -0.0229 | -0.068 | [-0.16, +0.01] | negative_recovery |
| mugla_2021_to_bejis_2022 | thermal | zscore | 0.9178 | 0.5832 | 0.5353 | +0.3346 | -0.0479 | -0.143 | [-0.24, -0.06] | negative_recovery |

> The earlier two-region 27-31% recovered / 69-73% remaining split is superseded and must not be carried forward.

## Negative-recovery rows (all directions, ROC-AUC)

| Direction | Family | Method | raw_gap | effect | recovered | Status |
|---|---|---|---|---|---|---|
| bejis_2022_to_manavgat_2021 | baseline | zscore | +0.5446 | -0.0026 | -0.005 | negative_recovery |
| bejis_2022_to_manavgat_2021 | thermal | zscore | +0.5939 | -0.0120 | -0.020 | negative_recovery |
| bejis_2022_to_mugla_2021 | baseline | zscore | +0.1511 | -0.0273 | -0.180 | negative_recovery |
| bejis_2022_to_mugla_2021 | baseline | zscore+coral | +0.1511 | -0.0221 | -0.146 | negative_recovery |
| bejis_2022_to_mugla_2021 | thermal | zscore | +0.2405 | -0.1007 | -0.419 | negative_recovery |
| bejis_2022_to_mugla_2021 | thermal | zscore+coral | +0.2405 | -0.1118 | -0.465 | negative_recovery |
| evia_2021_extended_to_manavgat_2021 | baseline | zscore | +0.1138 | -0.1653 | -1.452 | negative_recovery |
| evia_2021_extended_to_manavgat_2021 | baseline | zscore+coral | +0.1138 | -0.1918 | -1.685 | negative_recovery |
| evia_2021_extended_to_manavgat_2021 | thermal | zscore | +0.2312 | -0.2734 | -1.182 | negative_recovery |
| evia_2021_extended_to_manavgat_2021 | thermal | zscore+coral | +0.2312 | -0.2604 | -1.126 | negative_recovery |
| evia_2021_extended_to_mugla_2021 | baseline | zscore | +0.2308 | -0.0223 | -0.097 | negative_recovery |
| evia_2021_extended_to_mugla_2021 | baseline | zscore+coral | +0.2308 | -0.0148 | -0.064 | negative_recovery |
| evia_2021_extended_to_mugla_2021 | thermal | zscore | +0.2821 | -0.0755 | -0.268 | negative_recovery |
| evia_2021_extended_to_mugla_2021 | thermal | zscore+coral | +0.2821 | -0.0466 | -0.165 | negative_recovery |
| manavgat_2021_to_evia_2021_extended | baseline | zscore | +0.1364 | -0.0929 | -0.681 | negative_recovery |
| manavgat_2021_to_evia_2021_extended | baseline | zscore+coral | +0.1364 | -0.0706 | -0.518 | negative_recovery |
| manavgat_2021_to_evia_2021_extended | thermal | zscore | +0.2582 | -0.1249 | -0.484 | negative_recovery |
| manavgat_2021_to_evia_2021_extended | thermal | zscore+coral | +0.2582 | -0.1497 | -0.580 | negative_recovery |
| manavgat_2021_to_mugla_2021 | baseline | zscore | +0.2777 | -0.0044 | -0.016 | negative_recovery |
| manavgat_2021_to_mugla_2021 | thermal | zscore | +0.4213 | -0.0109 | -0.026 | negative_recovery |
| manavgat_2021_to_mugla_2021 | thermal | zscore+coral | +0.4213 | -0.0202 | -0.048 | negative_recovery |
| mugla_2021_to_bejis_2022 | thermal | zscore | +0.3346 | -0.0479 | -0.143 | negative_recovery |
| mugla_2021_to_bejis_2022 | thermal | zscore+coral | +0.3346 | -0.0229 | -0.068 | negative_recovery |
| mugla_2021_to_evia_2021_extended | baseline | zscore | +0.1592 | -0.0554 | -0.348 | negative_recovery |
| mugla_2021_to_evia_2021_extended | baseline | zscore+coral | +0.1592 | -0.0471 | -0.296 | negative_recovery |
| mugla_2021_to_evia_2021_extended | thermal | zscore | +0.2588 | -0.0921 | -0.356 | negative_recovery |
| mugla_2021_to_evia_2021_extended | thermal | zscore+coral | +0.2588 | -0.0901 | -0.348 | negative_recovery |
