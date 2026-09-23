# Final Cross-Region Transfer Report

- source: `manavgat_2021`
- target: `mugla_2021`
- primary population: `burnable_tree_shrub_grass`

**Overall conclusion: `transfer_not_supported`**

Neither transfer direction shows positive target-region spatial-block bootstrap support for the thermal predictor set over the baseline.

## Per-direction results (primary population)

### manavgat_2021_to_mugla_2021

- source cells: 20511 (positive: 2935)
- target cells: 41730 (positive: 2911)
- target burned prevalence: 0.0698
- baseline target ROC-AUC: 0.4656065622633644
- thermal target ROC-AUC: 0.4376617829318566
- baseline target PR-AUC: 0.06519776046968895
- thermal target PR-AUC: 0.05951686892404788
- baseline target Brier: 0.2320813380941932
- thermal target Brier: 0.23348500370330705
- delta_auc: -0.027944779331507796
- delta_pr_auc: -0.0056808915456410675
- delta_brier: 0.001403665609113841
- brier_improvement (baseline - thermal): -0.001403665609113841
- bootstrap interpretation: {'delta_auc': 'negative_bootstrap_support', 'delta_pr_auc': 'negative_bootstrap_support', 'delta_brier': 'uncertain'}

### mugla_2021_to_manavgat_2021

- source cells: 41730 (positive: 2911)
- target cells: 20511 (positive: 2935)
- target burned prevalence: 0.1431
- baseline target ROC-AUC: 0.4222591457764537
- thermal target ROC-AUC: 0.3449553227686198
- baseline target PR-AUC: 0.11374056637797869
- thermal target PR-AUC: 0.1007227330135432
- baseline target Brier: 0.2449638822344167
- thermal target Brier: 0.2457775976327831
- delta_auc: -0.0773038230078339
- delta_pr_auc: -0.013017833364435488
- delta_brier: 0.0008137153983663881
- brier_improvement (baseline - thermal): -0.0008137153983663881
- bootstrap interpretation: {'delta_auc': 'negative_bootstrap_support', 'delta_pr_auc': 'negative_bootstrap_support', 'delta_brier': 'uncertain'}

## Caution notes

- This is NOT a claim of operational wildfire prediction.
- This is NOT a claim of causal fire prediction.
- Labels are MCD64A1 ~500 m reconstructed cells, NOT 30 m fire labels.
- Bootstrap intervals are target-region spatial-block percentile intervals, NOT classical statistical significance.