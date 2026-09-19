# Step8 Large-Spatial-Block Robustness Report -- FORMAL PRIMARY (all_valid)

- analysis_id: `bad06061e02ea00942bf6c407bf1e0203adcf23531941b6aad17fa8c64dd267b`
- protected original Step8 hash check: **passed**
- protected existing (v1) robustness hash check: **passed**

## Formal Step8B primary-population (all_valid) robustness -- NEW

| experiment | block cells | nominal scale | delta ROC-AUC | ROC CI | ROC support | delta PR-AUC | PR CI | PR support | joint status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| manavgat_2021 | 10 | approximately_5_km | 0.051145 | [0.033522, 0.069936] | bootstrap_supported_positive | 0.124547 | [0.061720, 0.184087] | bootstrap_supported_positive | supported_on_both_metrics |
| manavgat_2021 | 20 | approximately_10_km | 0.049637 | [0.019723, 0.080583] | bootstrap_supported_positive | 0.145488 | [0.073668, 0.206318] | bootstrap_supported_positive | supported_on_both_metrics |
| bejis_2022 | 10 | approximately_5_km | 0.055725 | [0.030753, 0.078098] | bootstrap_supported_positive | 0.134358 | [0.059101, 0.226400] | bootstrap_supported_positive | supported_on_both_metrics |
| bejis_2022 | 20 | approximately_10_km | 0.061286 | [0.039680, 0.087105] | bootstrap_supported_positive | 0.076055 | [0.014015, 0.155429] | bootstrap_supported_positive | supported_on_both_metrics |

the formal Step8B primary-population (all_valid) thermal contribution remained bootstrap-supported across both predefined large-block scales in both wildfire regions

## Natural-vegetation (burnable_tree_shrub_grass) sensitivity robustness -- EXTERNAL FROZEN REFERENCE, NOT recomputed

- source analysis_id: `bb909a2c9bff1b7b76c95fa6fd36144d54bfd532883d305238bebd8c97915d3a`
- source output root: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\robustness\step8_large_block\manavgat_2021__bejis_2022`
- overall (as originally reported): {'all_four_conditions_supported_on_both_metrics': True, 'statement': 'thermal contribution remained bootstrap-supported across both predefined large-block scales in both wildfire regions', 'conditions_losing_support': []}

## Claim boundaries

- spatial autocorrelation was not claimed eliminated
- no causal thermal effects
- not operational wildfire prediction
- no statistical significance or p-values
- no proof that residual spatial dependence is absent
- not successful cross-region transfer
- no best block size was selected
- the natural-vegetation (burnable_tree_shrub_grass) figures above are an external frozen reference and must not be read as newly rerun or as evidence about the formal all_valid primary result
