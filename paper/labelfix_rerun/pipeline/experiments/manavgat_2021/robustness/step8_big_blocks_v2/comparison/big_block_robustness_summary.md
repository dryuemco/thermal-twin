# Step8 Big-Spatial-Block Robustness Report -- manavgat_2021

- analysis_id: `f5f97cec4733da613e64f9e64a9b56fab774bb187417d8c9d54f60dcc139a24b`
- primary population: burnable_tree_shrub_grass
- support robustness status: **strongly_robust**
- effect magnitude stability status: **decreases_with_block_scale**
- delta ROC-AUC relative reduction (small→10-cell): 0.07458024531791266
- delta ROC-AUC relative reduction (small→20-cell): 0.2982821486385671
- delta ROC-AUC relative reduction (10→20-cell): 0.24173020101294848
- delta PR-AUC relative reduction (small→10-cell): 0.10726531103281381
- delta PR-AUC relative reduction (small→20-cell): 0.43409603618742815
- delta PR-AUC relative reduction (10→20-cell): 0.36610062227191836

Positive thermal contribution was retained at both larger block scales, while the magnitude of the contribution decreased as spatial separation increased.

| source | block cells | nominal scale | delta ROC-AUC | ROC CI | ROC support | delta PR-AUC | PR CI | PR support | brier_improvement | brier support | overall status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frozen_original_small_block | 2 | approximately_1_km | 0.066893 | [0.060493, 0.073200] | supported_positive | 0.175712 | [0.154537, 0.194998] | supported_positive | 0.037342 | supported_improvement | retained |
| new_big_block_robustness | 10 | approximately_5_km | 0.061904 | [0.039880, 0.082286] | supported_positive | 0.156864 | [0.086876, 0.211923] | supported_positive | 0.035105 | supported_improvement | retained |
| new_big_block_robustness | 20 | approximately_10_km | 0.046940 | [0.015693, 0.080716] | supported_positive | 0.099436 | [0.028954, 0.176934] | supported_positive | 0.024949 | supported_improvement | retained |

## Claim boundaries

- no causal thermal effects
- not operational wildfire prediction
- no statistical significance or p-values
- no proof that residual spatial dependence is absent
- not successful cross-region transfer
- no best block size was selected
- absolute AUC decline alone is not treated as failure; the primary estimand is the paired baseline-vs-thermal delta and its bootstrap interval
- support_robustness_status and effect_magnitude_stability_status answer different questions and must not be conflated
