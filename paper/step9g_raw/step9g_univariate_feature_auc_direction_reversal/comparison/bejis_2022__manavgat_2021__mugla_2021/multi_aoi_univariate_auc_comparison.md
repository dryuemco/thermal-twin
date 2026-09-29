# Multi-AOI Step9G univariate-AUC comparison

analysis_id: `6b4a639adb62ccbaee98a9914b7a8dca49dc06a826ae3bb070e601560812ee11` (order-invariant)  
created_at: 2026-07-23T08:40:01.558740+00:00  
requested_experiment_ids: ['manavgat_2021', 'bejis_2022', 'mugla_2021']  
resolved_experiment_ids: ['bejis_2022', 'manavgat_2021', 'mugla_2021']  
complete_pairwise_matrix: True

**Legend**: cell = `AUC [CI low, CI high] direction*` -- ↑ higher values rank burned; ↓ lower values rank burned; `*` 95% spatial-block bootstrap interval excludes 0.5.

| feature | bejis_2022 | manavgat_2021 | mugla_2021 |
| --- | --- | --- | --- |
| ndvi_mean | 0.559 [0.497, 0.619] ↑ | 0.636 [0.587, 0.676] ↑* | 0.662 [0.616, 0.704] ↑* |
| elevation_mean | 0.643 [0.558, 0.729] ↑* | 0.374 [0.289, 0.471] ↓* | 0.611 [0.532, 0.690] ↑* |
| slope_mean | 0.521 [0.439, 0.605] ↑ | 0.531 [0.423, 0.642] ↑ | 0.637 [0.582, 0.686] ↑* |
| lst_anomaly_mean | 0.418 [0.364, 0.480] ↓* | 0.482 [0.428, 0.530] ↓ | 0.485 [0.395, 0.566] ↓ |
| current_lst_mean | 0.477 [0.401, 0.547] ↓ | 0.538 [0.452, 0.621] ↑ | 0.325 [0.271, 0.382] ↓* |
| current_tvdi_mean | 0.517 [0.429, 0.595] ↑ | 0.552 [0.460, 0.641] ↑ | 0.336 [0.275, 0.398] ↓* |
| tvdi_difference_mean | 0.512 [0.443, 0.583] ↑ | 0.449 [0.391, 0.505] ↓ | 0.490 [0.396, 0.575] ↓ |
| downscaled_lst_mean | 0.484 [0.400, 0.560] ↓ | 0.552 [0.466, 0.637] ↑ | 0.307 [0.253, 0.366] ↓* |
| fused_lst_mean | 0.481 [0.404, 0.551] ↓ | 0.540 [0.454, 0.622] ↑ | 0.325 [0.272, 0.383] ↓* |

## Advisor-critical elevation result

- bejis_2022: AUC 0.6432824053164721, CI [0.5583150457861116, 0.7290055219147464], higher values rank burned, bootstrap_supported_higher_values_rank_burned
- manavgat_2021: AUC 0.37410755666893913, CI [0.2890796631009303, 0.4711534398242251], lower values rank burned, bootstrap_supported_lower_values_rank_burned
- mugla_2021: AUC 0.6114025048859928, CI [0.5319021930545539, 0.6904319830630276], higher values rank burned, bootstrap_supported_higher_values_rank_burned

bejis_2022 and mugla_2021 share a bootstrap-supported positive elevation_mean direction, whereas manavgat_2021 has a bootstrap-supported negative direction.
This descriptive cross-region contrast does not prove that this feature difference causally explains any cross-region transfer performance difference.

## Pairwise bootstrap-supported direction reversals

- bejis_2022–manavgat_2021: elevation_mean is a bootstrap-supported direction reversal.
- bejis_2022–mugla_2021: no feature has a bootstrap-supported direction reversal.
- manavgat_2021–mugla_2021: elevation_mean is a bootstrap-supported direction reversal.

## Limitations

- Connected/pairwise reversal findings are descriptive diagnostics; they do not establish causality and do not prove that concept/relationship shift is the only source of cross-region transfer failure.
- A point-estimate direction reversal whose 95% spatial-block bootstrap interval includes 0.5 is uncertain and must never be reported as bootstrap-supported.
- This synthesis recomputes no AUC, bootstrap replicate, or reversal classification; it only reads and cross-validates existing canonical Step9G pair reports.
- landcover_dominant is excluded from scalar AUC because its integer class codes have no scientifically meaningful ordering.
