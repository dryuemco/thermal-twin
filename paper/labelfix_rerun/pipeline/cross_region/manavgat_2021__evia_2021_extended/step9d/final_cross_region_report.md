# Final Cross-Region Transfer Report

- source: `manavgat_2021`
- target: `evia_2021_extended`
- primary population: `burnable_tree_shrub_grass`

**Overall conclusion: `partial_transfer_supported`**

Only one direction (or only some metrics) show positive target-region spatial-block bootstrap support for the thermal predictor set; the cross-region transfer result is mixed.

## Per-direction results (primary population)

### evia_2021_extended_to_manavgat_2021

- source cells: 9298 (positive: 2664)
- target cells: 20511 (positive: 2935)
- target burned prevalence: 0.1431
- baseline target ROC-AUC: 0.7273654778585326
- thermal target ROC-AUC: 0.6768829881850658
- baseline target PR-AUC: 0.29184880895484727
- thermal target PR-AUC: 0.32088833865905136
- baseline target Brier: 0.1298894115987032
- thermal target Brier: 0.11784650562250447
- delta_auc: -0.0504824896734668
- delta_pr_auc: 0.029039529704204092
- delta_brier: -0.01204290597619874
- brier_improvement (baseline - thermal): 0.01204290597619874
- bootstrap interpretation: {'delta_auc': 'negative_bootstrap_support', 'delta_pr_auc': 'positive_bootstrap_support', 'delta_brier': 'positive_bootstrap_support'}

### manavgat_2021_to_evia_2021_extended

- source cells: 20511 (positive: 2935)
- target cells: 9298 (positive: 2664)
- target burned prevalence: 0.2865
- baseline target ROC-AUC: 0.6225921429418566
- thermal target ROC-AUC: 0.6540092625033838
- baseline target PR-AUC: 0.36835056989917536
- thermal target PR-AUC: 0.4065333593047762
- baseline target Brier: 0.27116895302561733
- thermal target Brier: 0.2628962479212862
- delta_auc: 0.03141711956152715
- delta_pr_auc: 0.038182789405600825
- delta_brier: -0.008272705104331146
- brier_improvement (baseline - thermal): 0.008272705104331146
- bootstrap interpretation: {'delta_auc': 'positive_bootstrap_support', 'delta_pr_auc': 'positive_bootstrap_support', 'delta_brier': 'positive_bootstrap_support'}

## Caution notes

- This is NOT a claim of operational wildfire prediction.
- This is NOT a claim of causal fire prediction.
- Labels are MCD64A1 ~500 m reconstructed cells, NOT 30 m fire labels.
- Bootstrap intervals are target-region spatial-block percentile intervals, NOT classical statistical significance.