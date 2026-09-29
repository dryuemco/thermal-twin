# Cross-Region Input Compatibility Audit

- source: `mugla_2021`
- target: `manavgat_2021`
- **passed: `True`**

This audit checks whether two independently generated Step8A ~500 m MCD64A1-cell modeling datasets are compatible for cross-region association-model transfer. It does NOT train or evaluate any model.

## Per-experiment checks

| check | source | target |
|---|---|---|
| predictor_window_ends_before_label_window | True | True |
| gate_exists | True | True |
| gate_is_wildfire_candidate_pass | True | True |
| step8a_stats_exists | True | True |
| cell_level_correct | True | True |
| no_30m_label_claim_true | True | True |
| feature_semantics_resolved_from_manifest | True | True |
| dataset_exists | True | True |
| required_shared_columns_present | True | True |
| target_column_is_burned | True | True |
| primary_label_is_mcd64a1 | True | True |
| spatial_block_id_computable | True | True |
| no_forbidden_columns_in_feature_sets | True | True |
| primary_population_sufficient | True | True |
| tvdi_computed_for_region | True | True |

## Population counts (positive/negative cells)

| population | source pos/neg | target pos/neg |
|---|---|---|
| burnable_tree_shrub_grass | 2911/38819 | 2935/17576 |
| all_valid | 3026/70019 | 3046/21041 |
| burnable_tree_shrub | 2759/34658 | 2297/13241 |

## Scope note

This is a cross-region transfer of the Step8 ~500 m MCD64A1-cell burned-area **association** model. It is NOT a 30 m fire prediction model, NOT an operational fire detection system, and does NOT transfer the Step7 downscaling model itself.