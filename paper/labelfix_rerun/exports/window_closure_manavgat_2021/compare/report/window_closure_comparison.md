# Window-closure comparison — `manavgat_2021`

- Schema: `window_closure_compare.v1`
- analysis_id: `ccd42192a789adedac69d97791ab3879143d9396945f05b74e8802d429774682`
- Primary population: `burnable_tree_shrub_grass`
- Display rounding: 3 decimals. The CSV and JSON artefacts carry full precision.

## 1. Analysis contract

- Only the predictor closure timing was changed; both window ends moved together so the window LENGTH is preserved.
- The label window was held fixed and is identical in every variant.
- One exact common cohort was held fixed across all six evaluations.
- One shared spatial-fold assignment was used by all six evaluations.
- The model family, feature registry, preprocessing, hyper-parameters and seeds were held fixed.
- The existing production MODIS seasonal policy was preserved.
- Reducer, QA and processing policy were held fixed; the closure date's interaction with the fixed production policy could change observation support and effective MODIS coverage.
- The analysis therefore measures the closure date together with its interaction with that fixed production policy, not the closure date in isolation.

## 2. Common cohort and shared folds

- Common cohort rows: **19406**
- Positives / negatives: **2725** / **16681**
- Prevalence: **0.140**
- Shared folds: **5**, spatial blocks: **5350**
- All six evaluations used these exact cells and this exact fold assignment.

## 3. Point metrics

| Variant | Metric | Baseline | Thermal | Thermal contribution (raw) |
|---|---|---:|---:|---:|
| canonical | roc_auc | 0.841 | 0.906 | 0.065 |
| canonical | pr_auc | 0.468 | 0.639 | 0.171 |
| canonical | brier | 0.131 | 0.095 | -0.036 |
| close_7d_earlier | roc_auc | 0.840 | 0.922 | 0.082 |
| close_7d_earlier | pr_auc | 0.465 | 0.692 | 0.227 |
| close_7d_earlier | brier | 0.132 | 0.086 | -0.046 |
| close_14d_earlier | roc_auc | 0.840 | 0.898 | 0.058 |
| close_14d_earlier | pr_auc | 0.467 | 0.619 | 0.152 |
| close_14d_earlier | brier | 0.131 | 0.099 | -0.033 |

## 4. Thermal contributions

Raw `thermal - baseline` per variant and metric. Negative raw deltas indicate lower Brier scores.

| Variant | Metric | Raw delta |
|---|---|---:|
| canonical | roc_auc | 0.065 |
| canonical | pr_auc | 0.171 |
| canonical | brier | -0.036 |
| close_7d_earlier | roc_auc | 0.082 |
| close_7d_earlier | pr_auc | 0.227 |
| close_7d_earlier | brier | -0.046 |
| close_14d_earlier | roc_auc | 0.058 |
| close_14d_earlier | pr_auc | 0.152 |
| close_14d_earlier | brier | -0.033 |

## 5. Predictor-closure changes

Raw `earlier_closure - canonical` per model family and metric. Negative raw deltas indicate lower Brier scores.

| Variant | Model family | Metric | Raw delta |
|---|---|---|---:|
| close_7d_earlier | baseline | roc_auc | -0.001 |
| close_7d_earlier | baseline | pr_auc | -0.003 |
| close_7d_earlier | baseline | brier | 0.001 |
| close_7d_earlier | thermal | roc_auc | 0.016 |
| close_7d_earlier | thermal | pr_auc | 0.053 |
| close_7d_earlier | thermal | brier | -0.009 |
| close_14d_earlier | baseline | roc_auc | -0.001 |
| close_14d_earlier | baseline | pr_auc | -0.001 |
| close_14d_earlier | baseline | brier | 0.000 |
| close_14d_earlier | thermal | roc_auc | -0.008 |
| close_14d_earlier | thermal | pr_auc | -0.020 |
| close_14d_earlier | thermal | brier | 0.003 |

## 6. Thermal-contribution changes

Raw `(thermal - baseline)_earlier - (thermal - baseline)_canonical`.

| Variant | Metric | Raw delta |
|---|---|---:|
| close_7d_earlier | roc_auc | 0.017 |
| close_7d_earlier | pr_auc | 0.056 |
| close_7d_earlier | brier | -0.010 |
| close_14d_earlier | roc_auc | -0.008 |
| close_14d_earlier | pr_auc | -0.019 |
| close_14d_earlier | brier | 0.003 |

## 7. Bootstrap evidence

Paired spatial-block bootstrap on the model stage's own replicate draws. The compare stage recomputes no replicate.

| Comparison | Variant | Model family | Metric | Delta | CI low | CI high | Valid | Status |
|---|---|---|---|---:|---:|---:|---:|---|
| thermal_contribution_within_variant | canonical | thermal_minus_baseline | roc_auc | 0.065 | 0.059 | 0.072 | 1000 | bootstrap_supported_increase |
| thermal_contribution_within_variant | canonical | thermal_minus_baseline | pr_auc | 0.171 | 0.149 | 0.191 | 1000 | bootstrap_supported_increase |
| thermal_contribution_within_variant | canonical | thermal_minus_baseline | brier | -0.036 | -0.039 | -0.033 | 1000 | bootstrap_supported_decrease |
| thermal_contribution_within_variant | close_7d_earlier | thermal_minus_baseline | roc_auc | 0.082 | 0.075 | 0.090 | 1000 | bootstrap_supported_increase |
| thermal_contribution_within_variant | close_7d_earlier | thermal_minus_baseline | pr_auc | 0.227 | 0.204 | 0.248 | 1000 | bootstrap_supported_increase |
| thermal_contribution_within_variant | close_7d_earlier | thermal_minus_baseline | brier | -0.046 | -0.049 | -0.042 | 1000 | bootstrap_supported_decrease |
| thermal_contribution_within_variant | close_14d_earlier | thermal_minus_baseline | roc_auc | 0.058 | 0.051 | 0.065 | 1000 | bootstrap_supported_increase |
| thermal_contribution_within_variant | close_14d_earlier | thermal_minus_baseline | pr_auc | 0.152 | 0.133 | 0.172 | 1000 | bootstrap_supported_increase |
| thermal_contribution_within_variant | close_14d_earlier | thermal_minus_baseline | brier | -0.033 | -0.036 | -0.030 | 1000 | bootstrap_supported_decrease |
| closure_change_within_model_family | close_7d_earlier | baseline | roc_auc | -0.001 | -0.002 | 0.000 | 1000 | interval_includes_zero |
| closure_change_within_model_family | close_7d_earlier | baseline | pr_auc | -0.003 | -0.008 | 0.002 | 1000 | interval_includes_zero |
| closure_change_within_model_family | close_7d_earlier | baseline | brier | 0.001 | 0.000 | 0.001 | 1000 | bootstrap_supported_increase |
| closure_change_within_model_family | close_7d_earlier | thermal | roc_auc | 0.016 | 0.011 | 0.021 | 1000 | bootstrap_supported_increase |
| closure_change_within_model_family | close_7d_earlier | thermal | pr_auc | 0.053 | 0.032 | 0.072 | 1000 | bootstrap_supported_increase |
| closure_change_within_model_family | close_7d_earlier | thermal | brier | -0.009 | -0.012 | -0.006 | 1000 | bootstrap_supported_decrease |
| closure_change_within_model_family | close_14d_earlier | baseline | roc_auc | -0.001 | -0.003 | 0.001 | 1000 | interval_includes_zero |
| closure_change_within_model_family | close_14d_earlier | baseline | pr_auc | -0.001 | -0.007 | 0.004 | 1000 | interval_includes_zero |
| closure_change_within_model_family | close_14d_earlier | baseline | brier | 0.000 | -0.001 | 0.001 | 1000 | interval_includes_zero |
| closure_change_within_model_family | close_14d_earlier | thermal | roc_auc | -0.008 | -0.014 | -0.003 | 1000 | bootstrap_supported_decrease |
| closure_change_within_model_family | close_14d_earlier | thermal | pr_auc | -0.020 | -0.039 | -0.002 | 1000 | bootstrap_supported_decrease |
| closure_change_within_model_family | close_14d_earlier | thermal | brier | 0.003 | 0.001 | 0.006 | 1000 | bootstrap_supported_increase |
| thermal_contribution_change | close_7d_earlier | thermal_minus_baseline | roc_auc | 0.017 | 0.011 | 0.022 | 1000 | bootstrap_supported_increase |
| thermal_contribution_change | close_7d_earlier | thermal_minus_baseline | pr_auc | 0.056 | 0.034 | 0.076 | 1000 | bootstrap_supported_increase |
| thermal_contribution_change | close_7d_earlier | thermal_minus_baseline | brier | -0.010 | -0.013 | -0.006 | 1000 | bootstrap_supported_decrease |
| thermal_contribution_change | close_14d_earlier | thermal_minus_baseline | roc_auc | -0.008 | -0.013 | -0.002 | 1000 | bootstrap_supported_decrease |
| thermal_contribution_change | close_14d_earlier | thermal_minus_baseline | pr_auc | -0.019 | -0.039 | -0.000 | 1000 | bootstrap_supported_decrease |
| thermal_contribution_change | close_14d_earlier | thermal_minus_baseline | brier | 0.003 | 0.000 | 0.006 | 1000 | bootstrap_supported_increase |

- bootstrap-supported increase: **13**
- bootstrap-supported decrease: **9**
- interval includes zero; uncertainty remains: **5**

### Evidence by metric

- `roc_auc` — ROC-AUC: a positive raw delta indicates a higher ROC-AUC value. increase: 5, decrease: 2, interval includes zero: 2.
- `pr_auc` — PR-AUC: a positive raw delta indicates a higher PR-AUC value. increase: 5, decrease: 2, interval includes zero: 2.
- `brier` — Brier score is a loss: a negative raw delta indicates a lower Brier score. The sign is reported raw and is never re-oriented. increase: 3, decrease: 5, interval includes zero: 1.

### Evidence by comparison family

- `thermal_contribution_within_variant` — increase: 6, decrease: 3, interval includes zero: 0.
- `closure_change_within_model_family` — increase: 4, decrease: 3, interval includes zero: 5.
- `thermal_contribution_change` — increase: 3, decrease: 3, interval includes zero: 0.

No single overall scientific verdict is produced and no majority vote is taken across metrics: each metric and each comparison family is reported on its own evidence.

## 8. Interpretation limits

- Results apply to the Manavgat-2021-style common cohort of this analysis only; they are not automatically transferable to another AOI or fire season.
- These results are descriptive and do not establish an underlying mechanism.
- It is not an operational forecasting validation and supports no deployment or alerting claim.
- Where a bootstrap interval includes zero, the direction of the change is not resolved by these data; uncertainty remains.
- The compare stage produces no new model and no new uncertainty estimate. It summarises verified model-stage outputs.
- No global comparison-evidence criterion is preregistered in this analysis, so no such overall claim is made.

## 9. Provenance and integrity

- Model stage metadata: `74385e364c96f2af800b3345a29abd65082943b3247fbe1c0cf22badd3b4f339`
- Bound model artefacts: **22**
- The compare stage fitted no model, generated no out-of-fold prediction and drew no bootstrap replicate.
- No canonical, predictor, pre-label, local-downstream or model artefact was written by this stage.
