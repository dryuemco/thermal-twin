| Measure | Family | n (frozen → corrected) | rho frozen [95% CI] | rho corrected [95% CI] | CI excludes 0 (frozen → corrected) |
|---|---|---|---|---|---|
| regime_dist_log_effn | P(y) spatial structure | 20 → 20 | +0.290 [-0.379, +0.739] | +0.109 [-0.670, +0.797] | False → False |
| regime_dist_largest_share | P(y) spatial structure | 20 → 20 | +0.290 [-0.390, +0.722] | +0.109 [-0.665, +0.766] | False → False |
| domain_classifier_auc | P(x) marginal | 20 → 20 | -0.317 [-0.775, +0.328] | -0.326 [-0.809, +0.359] | False → False |
| target_mean_dissimilarity | P(x) marginal | 12 → 12 | -0.105 [-0.587, +0.457] | -0.126 [-0.674, +0.370] | False → False |
| target_p95_dissimilarity | P(x) marginal | 12 → 12 | -0.084 [-0.580, +0.466] | -0.147 [-0.676, +0.245] | False → False |
| fraction_inside_weighted_aoa | P(x) marginal | 12 → 12 | +0.217 [-0.500, +0.600] | +0.210 [-0.478, +0.623] | False → False |
| climate_distance | P(x) marginal | 12 → 12 | +0.057 [-0.699, +0.793] | +0.028 [-0.837, +0.836] | False → False |
| geographic_distance_km | geographic | 12 → 12 | -0.240 [-0.839, +0.718] | -0.170 [-0.867, +0.839] | False → False |
| unweighted_fraction_inside_support | P(x) marginal | 12 → 12 | +0.077 [-0.925, +0.609] | +0.084 [-0.921, +0.761] | False → False |
| agree_count_9 | P(y|x) conditional | 20 → 20 | +0.178 [-0.400, +0.718] | +0.467 [-0.291, +0.796] | False → False |
| vector_spearman_9 | P(y|x) conditional | 20 → 20 | +0.269 [-0.363, +0.765] | +0.435 [-0.207, +0.800] | False → False |
| cosine_9 | P(y|x) conditional | 20 → 20 | +0.504 [-0.167, +0.825] | +0.444 [-0.290, +0.803] | False → False |
| agree_fraction_supported | P(y|x) conditional | 16 → 18 | +0.840 [+0.577, +0.876] | +0.517 [-0.274, +0.868] | True → False |
| vector_spearman_supported | P(y|x) conditional | 2 → 6 | not computable | +0.956 [+0.853, +0.956] | False → True | ‡
| cosine_supported | P(y|x) conditional | 16 → 18 | +0.805 [+0.330, +0.877] | +0.493 [-0.243, +0.871] | True → False |
| schoener_d_mean1d | P(x|y=1) niche overlap | 20 → 20 | +0.241 [-0.450, +0.742] | +0.097 [-0.534, +0.630] | False → False |
| warren_i_mean1d | P(x|y=1) niche overlap | 20 → 20 | +0.223 [-0.423, +0.729] | +0.190 [-0.426, +0.766] | False → False |
| schoener_d_pca2d | P(x|y=1) niche overlap | 20 → 20 | +0.097 [-0.511, +0.681] | +0.033 [-0.587, +0.630] | False → False |
| warren_i_pca2d | P(x|y=1) niche overlap | 20 → 20 | -0.069 [-0.661, +0.491] | -0.027 [-0.657, +0.560] | False → False |
| mahalanobis_burned | P(x|y=1) niche overlap | 20 → 20 | -0.226 [-0.750, +0.442] | -0.220 [-0.819, +0.424] | False → False |

‡ vector_spearman_supported: 6 directions, degenerate interval (upper bound = point estimate); not interpreted, not comparable with the other 19 measures. Frozen label: 2 directions, not computable. It is a member of the fixed candidate set and stays in the table.
