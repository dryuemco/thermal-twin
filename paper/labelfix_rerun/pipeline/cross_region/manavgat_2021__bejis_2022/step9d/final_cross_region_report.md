# Final Cross-Region Transfer Report

- source: `manavgat_2021`
- target: `bejis_2022`
- primary population: `burnable_tree_shrub_grass`

**Overall conclusion: `partial_transfer_supported`**

Only one direction (or only some metrics) show positive target-region spatial-block bootstrap support for the thermal predictor set; the cross-region transfer result is mixed.

## Per-direction results (primary population)

### bejis_2022_to_manavgat_2021

- source cells: 15190 (positive: 1100)
- target cells: 20511 (positive: 2935)
- target burned prevalence: 0.1431
- baseline target ROC-AUC: 0.2965551309319895
- thermal target ROC-AUC: 0.3141548720223256
- baseline target PR-AUC: 0.09644753386308019
- thermal target PR-AUC: 0.09776772462629946
- baseline target Brier: 0.20027263356813213
- thermal target Brier: 0.17422225515795853
- delta_auc: 0.01759974109033613
- delta_pr_auc: 0.0013201907632192644
- delta_brier: -0.026050378410173602
- brier_improvement (baseline - thermal): 0.026050378410173602
- bootstrap interpretation: {'delta_auc': 'positive_bootstrap_support', 'delta_pr_auc': 'uncertain', 'delta_brier': 'positive_bootstrap_support'}

### manavgat_2021_to_bejis_2022

- source cells: 20511 (positive: 2935)
- target cells: 15190 (positive: 1100)
- target burned prevalence: 0.0724
- baseline target ROC-AUC: 0.37069117362410486
- thermal target ROC-AUC: 0.3964026711400735
- baseline target PR-AUC: 0.052010675967464864
- thermal target PR-AUC: 0.05417448341892161
- baseline target Brier: 0.15951819321725308
- thermal target Brier: 0.1381497524851594
- delta_auc: 0.02571149751596863
- delta_pr_auc: 0.0021638074514567437
- delta_brier: -0.02136844073209368
- brier_improvement (baseline - thermal): 0.02136844073209368
- bootstrap interpretation: {'delta_auc': 'positive_bootstrap_support', 'delta_pr_auc': 'positive_bootstrap_support', 'delta_brier': 'positive_bootstrap_support'}

## Caution notes

- This is NOT a claim of operational wildfire prediction.
- This is NOT a claim of causal fire prediction.
- Labels are MCD64A1 ~500 m reconstructed cells, NOT 30 m fire labels.
- Bootstrap intervals are target-region spatial-block percentile intervals, NOT classical statistical significance.