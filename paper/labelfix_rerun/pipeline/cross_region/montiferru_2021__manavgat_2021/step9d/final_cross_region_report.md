# Final Cross-Region Transfer Report

- source: `montiferru_2021`
- target: `manavgat_2021`
- primary population: `burnable_tree_shrub_grass`

**Overall conclusion: `partial_transfer_supported`**

Only one direction (or only some metrics) show positive target-region spatial-block bootstrap support for the thermal predictor set; the cross-region transfer result is mixed.

## Per-direction results (primary population)

### manavgat_2021_to_montiferru_2021

- source cells: 20511 (positive: 2935)
- target cells: 2544 (positive: 539)
- target burned prevalence: 0.2119
- baseline target ROC-AUC: 0.5339859997501608
- thermal target ROC-AUC: 0.5178084473417569
- baseline target PR-AUC: 0.22516683861700296
- thermal target PR-AUC: 0.24319094268194025
- baseline target Brier: 0.26318920792770456
- thermal target Brier: 0.21616084349639064
- delta_auc: -0.016177552408403906
- delta_pr_auc: 0.01802410406493729
- delta_brier: -0.04702836443131392
- brier_improvement (baseline - thermal): 0.04702836443131392
- bootstrap interpretation: {'delta_auc': 'uncertain', 'delta_pr_auc': 'positive_bootstrap_support', 'delta_brier': 'positive_bootstrap_support'}

### montiferru_2021_to_manavgat_2021

- source cells: 2544 (positive: 539)
- target cells: 20511 (positive: 2935)
- target burned prevalence: 0.1431
- baseline target ROC-AUC: 0.3379486623776111
- thermal target ROC-AUC: 0.40410656586843297
- baseline target PR-AUC: 0.10149748008899191
- thermal target PR-AUC: 0.11309560200174143
- baseline target Brier: 0.4494142197956299
- thermal target Brier: 0.3099108239042197
- delta_auc: 0.06615790349082185
- delta_pr_auc: 0.011598121912749518
- delta_brier: -0.1395033958914102
- brier_improvement (baseline - thermal): 0.1395033958914102
- bootstrap interpretation: {'delta_auc': 'positive_bootstrap_support', 'delta_pr_auc': 'positive_bootstrap_support', 'delta_brier': 'positive_bootstrap_support'}

## Caution notes

- This is NOT a claim of operational wildfire prediction.
- This is NOT a claim of causal fire prediction.
- Labels are MCD64A1 ~500 m reconstructed cells, NOT 30 m fire labels.
- Bootstrap intervals are target-region spatial-block percentile intervals, NOT classical statistical significance.