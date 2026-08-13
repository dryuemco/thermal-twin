# Final Cross-Region Transfer Report

- source: `mugla_2021`
- target: `mugla_2022_event_relative`
- primary population: `burnable_tree_shrub_grass`

**Overall conclusion: `partial_transfer_supported`**

Only one direction (or only some metrics) show positive target-region spatial-block bootstrap support for the thermal predictor set; the cross-region transfer result is mixed.

## Per-direction results (primary population)

### mugla_2021_to_mugla_2022_event_relative

- source cells: 41730 (positive: 2911)
- target cells: 38790 (positive: 331)
- target burned prevalence: 0.0085
- baseline target ROC-AUC: 0.6421276976485887
- thermal target ROC-AUC: 0.5588060231914883
- baseline target PR-AUC: 0.011667245004187716
- thermal target PR-AUC: 0.00990857877751113
- baseline target Brier: 0.0834372054903673
- thermal target Brier: 0.07326147828513525
- delta_auc: -0.08332167445710037
- delta_pr_auc: -0.0017586662266765862
- delta_brier: -0.010175727205232049
- brier_improvement (baseline - thermal): 0.010175727205232049
- bootstrap interpretation: {'delta_auc': 'negative_bootstrap_support', 'delta_pr_auc': 'uncertain', 'delta_brier': 'positive_bootstrap_support'}

### mugla_2022_event_relative_to_mugla_2021

- source cells: 38790 (positive: 331)
- target cells: 41730 (positive: 2911)
- target burned prevalence: 0.0698
- baseline target ROC-AUC: 0.5809242374405595
- thermal target ROC-AUC: 0.6692151604002363
- baseline target PR-AUC: 0.08330432150197827
- thermal target PR-AUC: 0.1408454118074078
- baseline target Brier: 0.07437613874604898
- thermal target Brier: 0.0674961414845562
- delta_auc: 0.08829092295967678
- delta_pr_auc: 0.057541090305429546
- delta_brier: -0.0068799972614927846
- brier_improvement (baseline - thermal): 0.0068799972614927846
- bootstrap interpretation: {'delta_auc': 'positive_bootstrap_support', 'delta_pr_auc': 'positive_bootstrap_support', 'delta_brier': 'positive_bootstrap_support'}

## Caution notes

- This is NOT a claim of operational wildfire prediction.
- This is NOT a claim of causal fire prediction.
- Labels are MCD64A1 ~500 m reconstructed cells, NOT 30 m fire labels.
- Bootstrap intervals are target-region spatial-block percentile intervals, NOT classical statistical significance.