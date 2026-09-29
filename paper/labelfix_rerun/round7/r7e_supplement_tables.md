| Feature set | Mean transfer AUC | Directions > 0.5 | Mean within-region AUC |
|---|---:|---:|---:|
| baseline_only | 0.5194 | 13 | 0.7973 |
| anomaly_only | 0.5245 | 14 | 0.8621 |
| absolute_only | 0.5308 | 13 | 0.8641 |
| no_coord_channels | 0.5277 | 13 | 0.8885 |
| full | 0.5267 | 13 | 0.8959 |

| Region | Increment, full | Without the two channels | Retained |
|---|---:|---:|---:|
| manavgat_2021 | +0.067 | +0.064 | 95 % |
| bejis_2022 | +0.056 | +0.046 | 82 % |
| mugla_2021 | +0.116 | +0.097 | 84 % |
| evia_2021_extended | +0.153 | +0.145 | 94 % |
| montiferru_2021 | +0.101 | +0.105 | 103 % |

| Estimator | Within thermal | Within increment | Transfer thermal | Transfer increment | Above chance |
|---|---:|---:|---:|---:|---:|
| rf_canonical | 0.896 | +0.099 | 0.527 | +0.007 | 13 of 20 |
| rf_shallow | 0.838 | +0.053 | 0.527 | -0.011 | 13 of 20 |
| rf_leaf200 | 0.814 | +0.046 | 0.522 | -0.019 | 13 of 20 |
| logistic | 0.759 | +0.046 | 0.481 | -0.021 | 11 of 20 |
