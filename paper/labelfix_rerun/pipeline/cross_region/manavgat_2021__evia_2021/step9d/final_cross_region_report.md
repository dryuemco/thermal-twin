# Final Cross-Region Transfer Report

- source: `manavgat_2021`
- target: `evia_2021`
- primary population: `burnable_tree_shrub_grass`

**Overall conclusion: `partial_transfer_supported`**

Only one direction (or only some metrics) show positive target-region spatial-block bootstrap support for the thermal predictor set; the cross-region transfer result is mixed.

## Per-direction results (primary population)

### evia_2021_to_manavgat_2021

- source cells: 3946 (positive: 2663)
- target cells: 20511 (positive: 2935)
- target burned prevalence: 0.1431
- baseline target ROC-AUC: 0.7013431278055331
- thermal target ROC-AUC: 0.543205424153581
- baseline target PR-AUC: 0.26645420113682705
- thermal target PR-AUC: 0.22250511975527193
- baseline target Brier: 0.21305368604830194
- thermal target Brier: 0.2678563162538193
- delta_auc: -0.15813770365195212
- delta_pr_auc: -0.04394908138155512
- delta_brier: 0.054802630205517344
- brier_improvement (baseline - thermal): -0.054802630205517344
- bootstrap interpretation: {'delta_auc': 'negative_bootstrap_support', 'delta_pr_auc': 'negative_bootstrap_support', 'delta_brier': 'negative_bootstrap_support'}

### manavgat_2021_to_evia_2021

- source cells: 20511 (positive: 2935)
- target cells: 3946 (positive: 2663)
- target burned prevalence: 0.6749
- baseline target ROC-AUC: 0.6279142394447861
- thermal target ROC-AUC: 0.62206607741139
- baseline target PR-AUC: 0.7529795986226415
- thermal target PR-AUC: 0.7732794385058308
- baseline target Brier: 0.25195232184222205
- thermal target Brier: 0.24743336011559766
- delta_auc: -0.005848162033396109
- delta_pr_auc: 0.020299839883189286
- delta_brier: -0.0045189617266243876
- brier_improvement (baseline - thermal): 0.0045189617266243876
- bootstrap interpretation: {'delta_auc': 'uncertain', 'delta_pr_auc': 'positive_bootstrap_support', 'delta_brier': 'uncertain'}

## Caution notes

- This is NOT a claim of operational wildfire prediction.
- This is NOT a claim of causal fire prediction.
- Labels are MCD64A1 ~500 m reconstructed cells, NOT 30 m fire labels.
- Bootstrap intervals are target-region spatial-block percentile intervals, NOT classical statistical significance.