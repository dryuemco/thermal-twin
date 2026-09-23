# Multi-AOI Transfer Synthesis

Generated at: 2026-09-19T09:35:48.640890+00:00
Canonical AOI set id: `bejis_2022__evia_2021_extended__manavgat_2021__mugla_2021`
Primary population: `burnable_tree_shrub_grass`

This report is generated purely from already-frozen numeric outputs. No modeling, adaptation, prediction, or bootstrap computation was performed to produce this document.

## Selected AOIs

- Display order: bejis_2022, evia_2021_extended, manavgat_2021, mugla_2021
- Canonical order: bejis_2022, evia_2021_extended, manavgat_2021, mugla_2021

## Within-region performance

| experiment_id | model_family | roc_auc | pr_auc | thermal_minus_baseline_roc_auc | large_block_robustness_available | large_block_support_status | effect_magnitude_stability_status |
|---|---|---|---|---|---|---|---|
| bejis_2022 | baseline | 0.8617 | 0.3028 | 0.0561 | True | supported_on_both_metrics | n/a |
| bejis_2022 | thermal | 0.9178 | 0.4978 | 0.0561 | True | supported_on_both_metrics | n/a |
| evia_2021_extended | baseline | 0.7590 | 0.5160 | 0.1533 | True | strongly_robust | stable_across_block_scale |
| evia_2021_extended | thermal | 0.9122 | 0.8164 | 0.1533 | True | strongly_robust | stable_across_block_scale |
| manavgat_2021 | baseline | 0.8412 | 0.4699 | 0.0669 | True | strongly_robust | decreases_with_block_scale |
| manavgat_2021 | thermal | 0.9081 | 0.6456 | 0.0669 | True | strongly_robust | decreases_with_block_scale |
| mugla_2021 | baseline | 0.7433 | 0.2249 | 0.1157 | True | strongly_robust | decreases_with_block_scale |
| mugla_2021 | thermal | 0.8590 | 0.4467 | 0.1157 | True | strongly_robust | decreases_with_block_scale |

## Cross-region transfer matrix

| direction | model_family | adaptation_method | roc_auc | roc_auc_chance_status | pr_auc | raw_transfer_status | adapted_minus_raw | adapted_minus_raw_support_status | residual_gap_status | step9e_shift_categories | step9e_ranking_reversal_value | step9e_ranking_reversal_scope |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bejis_2022 -> evia_2021_extended | baseline | raw_source_only | 0.5305 | bootstrap_supported_above_chance | 0.2823 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> evia_2021_extended | baseline | regionwise_zscore | 0.5842 | bootstrap_supported_above_chance | 0.3280 | raw_roc_and_pr_supported | 0.0538 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> evia_2021_extended | baseline | coral_after_regionwise_zscore | 0.5985 | bootstrap_supported_above_chance | 0.3359 | raw_roc_and_pr_supported | 0.0681 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> evia_2021_extended | thermal | raw_source_only | 0.3828 | bootstrap_supported_below_chance | 0.2258 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> evia_2021_extended | thermal | regionwise_zscore | 0.5316 | bootstrap_supported_above_chance | 0.2909 | raw_discrimination_not_supported | 0.1488 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> evia_2021_extended | thermal | coral_after_regionwise_zscore | 0.4991 | chance_level_not_excluded | 0.2748 | raw_discrimination_not_supported | 0.1163 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| evia_2021_extended -> bejis_2022 | baseline | raw_source_only | 0.3917 | bootstrap_supported_below_chance | 0.0540 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| evia_2021_extended -> bejis_2022 | baseline | regionwise_zscore | 0.4810 | chance_level_not_excluded | 0.0692 | raw_discrimination_not_supported | 0.0893 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| evia_2021_extended -> bejis_2022 | baseline | coral_after_regionwise_zscore | 0.4863 | chance_level_not_excluded | 0.0705 | raw_discrimination_not_supported | 0.0945 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| evia_2021_extended -> bejis_2022 | thermal | raw_source_only | 0.4480 | bootstrap_supported_below_chance | 0.0592 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| evia_2021_extended -> bejis_2022 | thermal | regionwise_zscore | 0.5495 | bootstrap_supported_above_chance | 0.0766 | raw_discrimination_not_supported | 0.1015 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| evia_2021_extended -> bejis_2022 | thermal | coral_after_regionwise_zscore | 0.5489 | bootstrap_supported_above_chance | 0.0746 | raw_discrimination_not_supported | 0.1009 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> manavgat_2021 | baseline | raw_source_only | 0.2966 | bootstrap_supported_below_chance | 0.0964 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> manavgat_2021 | baseline | regionwise_zscore | 0.2939 | bootstrap_supported_below_chance | 0.0962 | raw_discrimination_not_supported | -0.0026 | adaptation_effect_uncertain | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> manavgat_2021 | baseline | coral_after_regionwise_zscore | 0.3088 | bootstrap_supported_below_chance | 0.0977 | raw_discrimination_not_supported | 0.0122 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> manavgat_2021 | thermal | raw_source_only | 0.3142 | bootstrap_supported_below_chance | 0.0978 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> manavgat_2021 | thermal | regionwise_zscore | 0.3021 | bootstrap_supported_below_chance | 0.1022 | raw_discrimination_not_supported | -0.0120 | adaptation_effect_uncertain | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> manavgat_2021 | thermal | coral_after_regionwise_zscore | 0.4057 | bootstrap_supported_below_chance | 0.1160 | raw_discrimination_not_supported | 0.0916 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> bejis_2022 | baseline | raw_source_only | 0.3707 | bootstrap_supported_below_chance | 0.0520 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> bejis_2022 | baseline | regionwise_zscore | 0.3850 | bootstrap_supported_below_chance | 0.0532 | raw_discrimination_not_supported | 0.0143 | adaptation_effect_uncertain | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> bejis_2022 | baseline | coral_after_regionwise_zscore | 0.3854 | bootstrap_supported_below_chance | 0.0533 | raw_discrimination_not_supported | 0.0147 | adaptation_effect_uncertain | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> bejis_2022 | thermal | raw_source_only | 0.3964 | bootstrap_supported_below_chance | 0.0542 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> bejis_2022 | thermal | regionwise_zscore | 0.4504 | bootstrap_supported_below_chance | 0.0596 | raw_discrimination_not_supported | 0.0540 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> bejis_2022 | thermal | coral_after_regionwise_zscore | 0.4668 | bootstrap_supported_below_chance | 0.0616 | raw_discrimination_not_supported | 0.0704 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| bejis_2022 -> mugla_2021 | baseline | raw_source_only | 0.5922 | bootstrap_supported_above_chance | 0.0936 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| bejis_2022 -> mugla_2021 | baseline | regionwise_zscore | 0.5650 | bootstrap_supported_above_chance | 0.0819 | raw_roc_and_pr_supported | -0.0273 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| bejis_2022 -> mugla_2021 | baseline | coral_after_regionwise_zscore | 0.5702 | bootstrap_supported_above_chance | 0.0836 | raw_roc_and_pr_supported | -0.0221 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| bejis_2022 -> mugla_2021 | thermal | raw_source_only | 0.6185 | bootstrap_supported_above_chance | 0.0925 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| bejis_2022 -> mugla_2021 | thermal | regionwise_zscore | 0.5177 | bootstrap_supported_above_chance | 0.0688 | raw_roc_and_pr_supported | -0.1007 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| bejis_2022 -> mugla_2021 | thermal | coral_after_regionwise_zscore | 0.5066 | chance_level_not_excluded | 0.0691 | raw_roc_and_pr_supported | -0.1118 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> bejis_2022 | baseline | raw_source_only | 0.4507 | bootstrap_supported_below_chance | 0.0642 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> bejis_2022 | baseline | regionwise_zscore | 0.5739 | bootstrap_supported_above_chance | 0.0852 | raw_discrimination_not_supported | 0.1231 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> bejis_2022 | baseline | coral_after_regionwise_zscore | 0.6087 | bootstrap_supported_above_chance | 0.0956 | raw_discrimination_not_supported | 0.1580 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> bejis_2022 | thermal | raw_source_only | 0.5832 | bootstrap_supported_above_chance | 0.0883 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> bejis_2022 | thermal | regionwise_zscore | 0.5353 | bootstrap_supported_above_chance | 0.0722 | raw_roc_and_pr_supported | -0.0479 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> bejis_2022 | thermal | coral_after_regionwise_zscore | 0.5603 | bootstrap_supported_above_chance | 0.0779 | raw_roc_and_pr_supported | -0.0229 | adaptation_effect_uncertain | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> manavgat_2021 | baseline | raw_source_only | 0.7274 | bootstrap_supported_above_chance | 0.2918 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> manavgat_2021 | baseline | regionwise_zscore | 0.5621 | bootstrap_supported_above_chance | 0.1495 | raw_roc_and_pr_supported | -0.1653 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> manavgat_2021 | baseline | coral_after_regionwise_zscore | 0.5356 | bootstrap_supported_above_chance | 0.1439 | raw_roc_and_pr_supported | -0.1918 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> manavgat_2021 | thermal | raw_source_only | 0.6769 | bootstrap_supported_above_chance | 0.3209 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> manavgat_2021 | thermal | regionwise_zscore | 0.4035 | bootstrap_supported_below_chance | 0.1109 | raw_roc_and_pr_supported | -0.2734 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> manavgat_2021 | thermal | coral_after_regionwise_zscore | 0.4165 | bootstrap_supported_below_chance | 0.1138 | raw_roc_and_pr_supported | -0.2604 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| manavgat_2021 -> evia_2021_extended | baseline | raw_source_only | 0.6226 | bootstrap_supported_above_chance | 0.3684 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| manavgat_2021 -> evia_2021_extended | baseline | regionwise_zscore | 0.5297 | bootstrap_supported_above_chance | 0.3066 | raw_roc_and_pr_supported | -0.0929 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| manavgat_2021 -> evia_2021_extended | baseline | coral_after_regionwise_zscore | 0.5520 | bootstrap_supported_above_chance | 0.3242 | raw_roc_and_pr_supported | -0.0706 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| manavgat_2021 -> evia_2021_extended | thermal | raw_source_only | 0.6540 | bootstrap_supported_above_chance | 0.4065 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| manavgat_2021 -> evia_2021_extended | thermal | regionwise_zscore | 0.5291 | bootstrap_supported_above_chance | 0.3200 | raw_roc_and_pr_supported | -0.1249 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| manavgat_2021 -> evia_2021_extended | thermal | coral_after_regionwise_zscore | 0.5043 | chance_level_not_excluded | 0.3031 | raw_roc_and_pr_supported | -0.1497 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> mugla_2021 | baseline | raw_source_only | 0.5125 | chance_level_not_excluded | 0.0816 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> mugla_2021 | baseline | regionwise_zscore | 0.4902 | chance_level_not_excluded | 0.0674 | raw_discrimination_not_supported | -0.0223 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> mugla_2021 | baseline | coral_after_regionwise_zscore | 0.4977 | chance_level_not_excluded | 0.0694 | raw_discrimination_not_supported | -0.0148 | adaptation_effect_uncertain | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> mugla_2021 | thermal | raw_source_only | 0.5768 | bootstrap_supported_above_chance | 0.0856 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> mugla_2021 | thermal | regionwise_zscore | 0.5013 | chance_level_not_excluded | 0.0664 | raw_roc_and_pr_supported | -0.0755 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| evia_2021_extended -> mugla_2021 | thermal | coral_after_regionwise_zscore | 0.5302 | bootstrap_supported_above_chance | 0.0717 | raw_roc_and_pr_supported | -0.0466 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> evia_2021_extended | baseline | raw_source_only | 0.5998 | bootstrap_supported_above_chance | 0.3437 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> evia_2021_extended | baseline | regionwise_zscore | 0.5444 | bootstrap_supported_above_chance | 0.2894 | raw_roc_and_pr_supported | -0.0554 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> evia_2021_extended | baseline | coral_after_regionwise_zscore | 0.5526 | bootstrap_supported_above_chance | 0.2971 | raw_roc_and_pr_supported | -0.0471 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> evia_2021_extended | thermal | raw_source_only | 0.6534 | bootstrap_supported_above_chance | 0.3788 | raw_roc_and_pr_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> evia_2021_extended | thermal | regionwise_zscore | 0.5613 | bootstrap_supported_above_chance | 0.2928 | raw_roc_and_pr_supported | -0.0921 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| mugla_2021 -> evia_2021_extended | thermal | coral_after_regionwise_zscore | 0.5633 | bootstrap_supported_above_chance | 0.2941 | raw_roc_and_pr_supported | -0.0901 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, moderate_shift, probability_scale_shift, relationship_direction_instability | False | direction_specific |
| manavgat_2021 -> mugla_2021 | baseline | raw_source_only | 0.4656 | bootstrap_supported_below_chance | 0.0652 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> mugla_2021 | baseline | regionwise_zscore | 0.4612 | bootstrap_supported_below_chance | 0.0610 | raw_discrimination_not_supported | -0.0044 | adaptation_effect_uncertain | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> mugla_2021 | baseline | coral_after_regionwise_zscore | 0.4753 | bootstrap_supported_below_chance | 0.0641 | raw_discrimination_not_supported | 0.0097 | adaptation_effect_uncertain | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> mugla_2021 | thermal | raw_source_only | 0.4377 | bootstrap_supported_below_chance | 0.0595 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> mugla_2021 | thermal | regionwise_zscore | 0.4267 | bootstrap_supported_below_chance | 0.0574 | raw_discrimination_not_supported | -0.0109 | adaptation_effect_uncertain | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| manavgat_2021 -> mugla_2021 | thermal | coral_after_regionwise_zscore | 0.4174 | bootstrap_supported_below_chance | 0.0571 | raw_discrimination_not_supported | -0.0202 | adaptation_degraded_transfer | residual_gap_remains | large_covariate_shift_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| mugla_2021 -> manavgat_2021 | baseline | raw_source_only | 0.4223 | bootstrap_supported_below_chance | 0.1137 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| mugla_2021 -> manavgat_2021 | baseline | regionwise_zscore | 0.5040 | chance_level_not_excluded | 0.1439 | raw_discrimination_not_supported | 0.0817 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| mugla_2021 -> manavgat_2021 | baseline | coral_after_regionwise_zscore | 0.5170 | bootstrap_supported_above_chance | 0.1439 | raw_discrimination_not_supported | 0.0947 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| mugla_2021 -> manavgat_2021 | thermal | raw_source_only | 0.3450 | bootstrap_supported_below_chance | 0.1007 | raw_discrimination_not_supported | n/a | n/a | n/a | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| mugla_2021 -> manavgat_2021 | thermal | regionwise_zscore | 0.4848 | chance_level_not_excluded | 0.1352 | raw_discrimination_not_supported | 0.1399 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |
| mugla_2021 -> manavgat_2021 | thermal | coral_after_regionwise_zscore | 0.4761 | bootstrap_supported_below_chance | 0.1338 | raw_discrimination_not_supported | 0.1312 | adaptation_supported | residual_gap_remains | large_covariate_shift_detected, distribution_support_mismatch_detected, high_shift, probability_scale_shift, ranking_reversal_suspected, relationship_direction_instability | True | direction_specific |

## Feature-level direction-reversal stability

| pair | feature | experiment_a_auc | experiment_b_auc | point_direction_reversal | reversal_status |
|---|---|---|---|---|---|
| bejis_2022 / evia_2021_extended | ndvi_mean | 0.5588 | 0.6391 | False | no_direction_reversal |
| bejis_2022 / evia_2021_extended | elevation_mean | 0.6433 | 0.5406 | False | no_direction_reversal |
| bejis_2022 / evia_2021_extended | slope_mean | 0.5208 | 0.4865 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / evia_2021_extended | lst_anomaly_mean | 0.4180 | 0.6401 | True | bootstrap_supported_direction_reversal |
| bejis_2022 / evia_2021_extended | current_lst_mean | 0.4767 | 0.3765 | False | no_direction_reversal |
| bejis_2022 / evia_2021_extended | current_tvdi_mean | 0.5173 | 0.3619 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / evia_2021_extended | tvdi_difference_mean | 0.5125 | 0.5191 | False | no_direction_reversal |
| bejis_2022 / evia_2021_extended | downscaled_lst_mean | 0.4836 | 0.3765 | False | no_direction_reversal |
| bejis_2022 / evia_2021_extended | fused_lst_mean | 0.4806 | 0.3757 | False | no_direction_reversal |
| bejis_2022 / manavgat_2021 | ndvi_mean | 0.5588 | 0.5640 | False | no_direction_reversal |
| bejis_2022 / manavgat_2021 | elevation_mean | 0.6433 | 0.2320 | True | bootstrap_supported_direction_reversal |
| bejis_2022 / manavgat_2021 | slope_mean | 0.5208 | 0.4002 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / manavgat_2021 | lst_anomaly_mean | 0.4180 | 0.5088 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / manavgat_2021 | current_lst_mean | 0.4767 | 0.6647 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / manavgat_2021 | current_tvdi_mean | 0.5173 | 0.6771 | False | no_direction_reversal |
| bejis_2022 / manavgat_2021 | tvdi_difference_mean | 0.5125 | 0.4604 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / manavgat_2021 | downscaled_lst_mean | 0.4836 | 0.6832 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / manavgat_2021 | fused_lst_mean | 0.4806 | 0.6662 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / mugla_2021 | ndvi_mean | 0.5588 | 0.6617 | False | no_direction_reversal |
| bejis_2022 / mugla_2021 | elevation_mean | 0.6433 | 0.6114 | False | no_direction_reversal |
| bejis_2022 / mugla_2021 | slope_mean | 0.5208 | 0.6368 | False | no_direction_reversal |
| bejis_2022 / mugla_2021 | lst_anomaly_mean | 0.4180 | 0.4846 | False | no_direction_reversal |
| bejis_2022 / mugla_2021 | current_lst_mean | 0.4767 | 0.3248 | False | no_direction_reversal |
| bejis_2022 / mugla_2021 | current_tvdi_mean | 0.5173 | 0.3358 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / mugla_2021 | tvdi_difference_mean | 0.5125 | 0.4900 | True | point_direction_reversal_interval_uncertain |
| bejis_2022 / mugla_2021 | downscaled_lst_mean | 0.4836 | 0.3070 | False | no_direction_reversal |
| bejis_2022 / mugla_2021 | fused_lst_mean | 0.4806 | 0.3252 | False | no_direction_reversal |
| evia_2021_extended / manavgat_2021 | ndvi_mean | 0.6391 | 0.5640 | False | no_direction_reversal |
| evia_2021_extended / manavgat_2021 | elevation_mean | 0.5406 | 0.2320 | True | point_direction_reversal_interval_uncertain |
| evia_2021_extended / manavgat_2021 | slope_mean | 0.4865 | 0.4002 | False | no_direction_reversal |
| evia_2021_extended / manavgat_2021 | lst_anomaly_mean | 0.6401 | 0.5088 | False | no_direction_reversal |
| evia_2021_extended / manavgat_2021 | current_lst_mean | 0.3765 | 0.6647 | True | bootstrap_supported_direction_reversal |
| evia_2021_extended / manavgat_2021 | current_tvdi_mean | 0.3619 | 0.6771 | True | bootstrap_supported_direction_reversal |
| evia_2021_extended / manavgat_2021 | tvdi_difference_mean | 0.5191 | 0.4604 | True | point_direction_reversal_interval_uncertain |
| evia_2021_extended / manavgat_2021 | downscaled_lst_mean | 0.3765 | 0.6832 | True | bootstrap_supported_direction_reversal |
| evia_2021_extended / manavgat_2021 | fused_lst_mean | 0.3757 | 0.6662 | True | bootstrap_supported_direction_reversal |
| evia_2021_extended / mugla_2021 | ndvi_mean | 0.6391 | 0.6617 | False | no_direction_reversal |
| evia_2021_extended / mugla_2021 | elevation_mean | 0.5406 | 0.6114 | False | no_direction_reversal |
| evia_2021_extended / mugla_2021 | slope_mean | 0.4865 | 0.6368 | True | point_direction_reversal_interval_uncertain |
| evia_2021_extended / mugla_2021 | lst_anomaly_mean | 0.6401 | 0.4846 | True | point_direction_reversal_interval_uncertain |
| evia_2021_extended / mugla_2021 | current_lst_mean | 0.3765 | 0.3248 | False | no_direction_reversal |
| evia_2021_extended / mugla_2021 | current_tvdi_mean | 0.3619 | 0.3358 | False | no_direction_reversal |
| evia_2021_extended / mugla_2021 | tvdi_difference_mean | 0.5191 | 0.4900 | True | point_direction_reversal_interval_uncertain |
| evia_2021_extended / mugla_2021 | downscaled_lst_mean | 0.3765 | 0.3070 | False | no_direction_reversal |
| evia_2021_extended / mugla_2021 | fused_lst_mean | 0.3757 | 0.3252 | False | no_direction_reversal |
| manavgat_2021 / mugla_2021 | ndvi_mean | 0.5640 | 0.6617 | False | no_direction_reversal |
| manavgat_2021 / mugla_2021 | elevation_mean | 0.2320 | 0.6114 | True | bootstrap_supported_direction_reversal |
| manavgat_2021 / mugla_2021 | slope_mean | 0.4002 | 0.6368 | True | bootstrap_supported_direction_reversal |
| manavgat_2021 / mugla_2021 | lst_anomaly_mean | 0.5088 | 0.4846 | True | point_direction_reversal_interval_uncertain |
| manavgat_2021 / mugla_2021 | current_lst_mean | 0.6647 | 0.3248 | True | bootstrap_supported_direction_reversal |
| manavgat_2021 / mugla_2021 | current_tvdi_mean | 0.6771 | 0.3358 | True | bootstrap_supported_direction_reversal |
| manavgat_2021 / mugla_2021 | tvdi_difference_mean | 0.4604 | 0.4900 | False | no_direction_reversal |
| manavgat_2021 / mugla_2021 | downscaled_lst_mean | 0.6832 | 0.3070 | True | bootstrap_supported_direction_reversal |
| manavgat_2021 / mugla_2021 | fused_lst_mean | 0.6662 | 0.3252 | True | bootstrap_supported_direction_reversal |

## Result-driven summary statements

- Strongest raw (unadapted) thermal ROC-AUC direction: evia_2021_extended -> manavgat_2021 (ROC-AUC = 0.6769).
- Weakest raw (unadapted) thermal ROC-AUC direction: bejis_2022 -> manavgat_2021 (ROC-AUC = 0.3142).
- Directions where raw thermal discrimination was not bootstrap-supported above chance: bejis_2022 -> evia_2021_extended, evia_2021_extended -> bejis_2022, bejis_2022 -> manavgat_2021, manavgat_2021 -> bejis_2022, manavgat_2021 -> mugla_2021, mugla_2021 -> manavgat_2021.
- Pairs with bidirectional raw thermal ROC-AUC support: bejis_2022/mugla_2021, evia_2021_extended/manavgat_2021, evia_2021_extended/mugla_2021.
- 18 row(s) have bootstrap-supported ROC-AUC improvement over raw transfer.
- 9 row(s) have an adapted-minus-raw ROC-AUC effect that is not bootstrap-resolved (CI crosses zero).
- 21 row(s) have bootstrap-supported ROC-AUC degradation relative to raw transfer.
- 23 adapted-transfer row(s) have ROC-AUC bootstrap-supported above chance (0.5).
- 10 adapted-transfer row(s) have ROC-AUC for which chance level (0.5) is not excluded.
- 15 adapted-transfer row(s) have ROC-AUC bootstrap-supported below chance (0.5).
- Recovery patterns describe the bootstrap-supported change relative to raw transfer, not whether the adapted ROC-AUC itself is above chance.
- bejis_2022/evia_2021_extended (baseline, coral_after_regionwise_zscore): bidirectional adapted-minus-raw recovery.
- bejis_2022/evia_2021_extended (baseline, regionwise_zscore): bidirectional adapted-minus-raw recovery.
- bejis_2022/evia_2021_extended (thermal, coral_after_regionwise_zscore): bidirectional adapted-minus-raw recovery.
- bejis_2022/evia_2021_extended (thermal, regionwise_zscore): bidirectional adapted-minus-raw recovery.
- bejis_2022/manavgat_2021 (baseline, coral_after_regionwise_zscore): direction-dependent adapted-minus-raw recovery.
- bejis_2022/manavgat_2021 (baseline, regionwise_zscore): no adapted-minus-raw recovery supported.
- bejis_2022/manavgat_2021 (thermal, coral_after_regionwise_zscore): bidirectional adapted-minus-raw recovery.
- bejis_2022/manavgat_2021 (thermal, regionwise_zscore): direction-dependent adapted-minus-raw recovery.
- bejis_2022/mugla_2021 (baseline, coral_after_regionwise_zscore): direction-dependent adapted-minus-raw recovery.
- bejis_2022/mugla_2021 (baseline, regionwise_zscore): direction-dependent adapted-minus-raw recovery.
- bejis_2022/mugla_2021 (thermal, coral_after_regionwise_zscore): no adapted-minus-raw recovery supported.
- bejis_2022/mugla_2021 (thermal, regionwise_zscore): no adapted-minus-raw recovery supported.
- evia_2021_extended/manavgat_2021 (baseline, coral_after_regionwise_zscore): no adapted-minus-raw recovery supported.
- evia_2021_extended/manavgat_2021 (baseline, regionwise_zscore): no adapted-minus-raw recovery supported.
- evia_2021_extended/manavgat_2021 (thermal, coral_after_regionwise_zscore): no adapted-minus-raw recovery supported.
- evia_2021_extended/manavgat_2021 (thermal, regionwise_zscore): no adapted-minus-raw recovery supported.
- evia_2021_extended/mugla_2021 (baseline, coral_after_regionwise_zscore): no adapted-minus-raw recovery supported.
- evia_2021_extended/mugla_2021 (baseline, regionwise_zscore): no adapted-minus-raw recovery supported.
- evia_2021_extended/mugla_2021 (thermal, coral_after_regionwise_zscore): no adapted-minus-raw recovery supported.
- evia_2021_extended/mugla_2021 (thermal, regionwise_zscore): no adapted-minus-raw recovery supported.
- manavgat_2021/mugla_2021 (baseline, coral_after_regionwise_zscore): direction-dependent adapted-minus-raw recovery.
- manavgat_2021/mugla_2021 (baseline, regionwise_zscore): direction-dependent adapted-minus-raw recovery.
- manavgat_2021/mugla_2021 (thermal, coral_after_regionwise_zscore): direction-dependent adapted-minus-raw recovery.
- manavgat_2021/mugla_2021 (thermal, regionwise_zscore): direction-dependent adapted-minus-raw recovery.
- Pairs with at least one bootstrap-supported feature-level direction reversal: bejis_2022/evia_2021_extended, bejis_2022/manavgat_2021, evia_2021_extended/manavgat_2021, manavgat_2021/mugla_2021.
- 48 transfer-matrix row(s) show a bootstrap-supported remaining residual gap after adaptation.
- Range of raw thermal ROC-AUC across all resolved directions: 0.3627.

## Scientific boundaries

- Within-region performance does not imply cross-region transportability.
- Transferability may be pair-specific and direction-dependent.
- Unsupervised covariate alignment may help some directions and harm others.
- Residual gaps after adaptation are consistent with relationship shift or other non-covariate differences between regions, not proof of a specific cause.
- Feature-level univariate direction reversals are diagnostic evidence of possible concept/relationship shift, not causal proof.
- One event per AOI does not allow region effects and event effects to be isolated.
- Target labels are used only for diagnostic evaluation; they are never used for adaptation, normalization, calibration, or model selection.
- No operational or universal cross-region transfer claim is supported by this report.
