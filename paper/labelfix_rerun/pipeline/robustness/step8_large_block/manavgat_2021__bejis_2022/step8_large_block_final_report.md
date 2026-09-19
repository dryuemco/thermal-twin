# Step8 Large-Spatial-Block Robustness Report

- analysis_id: `bb909a2c9bff1b7b76c95fa6fd36144d54bfd532883d305238bebd8c97915d3a`
- protected original Step8 hash check: **passed**

## New predefined large-block conditions

| experiment | block cells | nominal scale | delta ROC-AUC | ROC CI | ROC support | delta PR-AUC | PR CI | PR support | joint status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| manavgat_2021 | 10 | approximately_5_km | 0.061904 | [0.039880, 0.082286] | bootstrap_supported_positive | 0.156864 | [0.086876, 0.211923] | bootstrap_supported_positive | supported_on_both_metrics |
| manavgat_2021 | 20 | approximately_10_km | 0.046940 | [0.015693, 0.080716] | bootstrap_supported_positive | 0.099436 | [0.028954, 0.176934] | bootstrap_supported_positive | supported_on_both_metrics |
| bejis_2022 | 10 | approximately_5_km | 0.045099 | [0.017780, 0.069003] | bootstrap_supported_positive | 0.107823 | [0.040781, 0.199715] | bootstrap_supported_positive | supported_on_both_metrics |
| bejis_2022 | 20 | approximately_10_km | 0.056610 | [0.031047, 0.089866] | bootstrap_supported_positive | 0.083513 | [0.022369, 0.160857] | bootstrap_supported_positive | supported_on_both_metrics |

## Block and fold feasibility

| experiment | block cells | total blocks | positive blocks | folds | min test positives | valid bootstrap |
| --- | --- | --- | --- | --- | --- | --- |
| manavgat_2021 | 10 | 237 | 47 | 5 | 575 | 1000 |
| manavgat_2021 | 20 | 60 | 17 | 5 | 553 | 1000 |
| bejis_2022 | 10 | 176 | 19 | 5 | 193 | 1000 |
| bejis_2022 | 20 | 48 | 6 | 5 | 73 | 995 |

## Frozen original 2-cell reference

| experiment | block cells | delta ROC-AUC | ROC CI | delta PR-AUC | PR CI | valid bootstrap | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| manavgat_2021 | 2 | 0.06689286691857155 | [0.060493, 0.073200] | 0.17571211849617985 | [0.154537, 0.194998] | 1000 | supported_on_both_metrics |
| bejis_2022 | 2 | 0.05613342796309451 | [0.047853, 0.065327] | 0.19503423145298132 | [0.155615, 0.231023] | 1000 | supported_on_both_metrics |

## Overall predefined-scale interpretation

thermal contribution remained bootstrap-supported across both predefined large-block scales in both wildfire regions

## Claim boundaries

- spatial autocorrelation was not claimed eliminated
- no causal thermal effects
- not operational wildfire prediction
- no statistical significance or p-values
- no proof that residual spatial dependence is absent
- not successful cross-region transfer
- no best block size was selected
