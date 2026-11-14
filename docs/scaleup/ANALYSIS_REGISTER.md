# Analysis register

One row per reported result: when it was specified relative to its own results, the kind of time evidence, and
whether it is used in the abstract. "Author" evidence is a commit time, which the authors can change; "server"
is the GitHub push record of the repository's activity log; "archive" is a Software Heritage snapshot. Times UTC.
Status: confirmatory = a decision rule fixed before the result; exploratory = everything else.

| Result | Script | Specified | Relative to its results | Time evidence | Status | Abstract |
|---|---|---|---|---|---|---|
| Null model vs RF, 5/10/20 km (claim 1) | analysis_official.py | plan 067e676, 14 Nov 11:35 local | after a pilot on the same fires, before the official run | author | confirmatory (rule 28/31) | yes |
| Distance bands (claim 2) | analysis_official.py | plan 067e676 | after the pilot, before the official run | author | confirmatory | yes |
| Sentinel-2 label check (claim 3), 0.10 | claim3_label_check.py | plan 067e676 | before | author | confirmatory (gap rule) | no |
| Sentinel-2 threshold 0.27 read as the credible one | claim3_label_check.py | amendment 3 | after | author | exploratory | no |
| Transfer, pre-fire LST (claims 4, 5) | claim4/5 | plan 067e676 | before | author | descriptive | no |
| Multi-year label (claim 6), threshold 28 | claim6_multiyear.py | amendment 2, 14 Nov 12:11 | after claims 1-2 were seen, before its own numbers | author | confirmatory (rule 28/31) | yes |
| Open datasets (claim 7) | claim7_open_data.py | amendment 2 | after claims 1-2, before its own numbers | author | descriptive | yes |
| Robustness: combined model, folds, designs, matching (am. 4) | claim1_robustness.py, claim1_combined.py | amendment 4 | after | author | exploratory | no |
| Validity checks: margins, no land cover, 2022-23, env. bands (am. 5) | claim1_validity.py | amendment 5 | after | author | exploratory | no |
| Prospective multi-year label (am. 5, 6.5) | claim6_multiyear.py | amendment 5 | after the other labels | author | exploratory | no |
| Full protocol on open data (am. 5) | claim7_protocol.py | amendment 5 | after | author | exploratory | no |
| sAUC on the 31 fires (6.1, 6.3) | claim8_sauc.py | amendment 6, 18:56:51; 6.3, 18:57:47 | before (by commit order only) | author; server/archive at 19:05 only after | exploratory | no |
| Semi-synthetic decision rule (6.2) | claim9_synthetic.py | amendment 6 | run started 19:00:18, one fire written 19:02:59; archived 19:05:38 | archive, server | confirmatory (not met) | yes |
| 30-fire sensitivity of 6.2 (6.6) | claim9_synthetic.py | 6.6 | written while the run was in progress | server 19:13:01 | sensitivity | no |
| Persistent field rho 0.5, 0.8 (7.1) | claim10_persistent.py | amendment 7 | written while claim9 printed results; run 20:06-20:53 | server 19:35:54 | exploratory | no |
| rho = 0 within-run reference (7.4) | claim10_persistent.py | 7.4 | before claim10 ran | server 19:41:13 | exploratory | no |
| Paired intervals, support sensitivity (7.2, 7.3) | claim9_intervals.py | amendment 7 | before they ran, after claim9 | server 19:35:54 | exploratory | no |
| Base-rate re-reporting (8.1) | claim9_rereport.py | amendment 8 | after claim9 and claim10 | server (8, 15 Nov 21:25) | exploratory | to be decided |
| Oracle truth, rho grid (8.2) | claim11_oracle.py | amendment 8 | before it ran | server | exploratory | to be decided |
| Monte Carlo replicates, 20 km (8.3, 8.4) | claim12_replicates.py | amendment 8 | before they ran | server | exploratory | to be decided |
| Calibrated scenarios (8.5) | claim13_calibrated.py | amendment 8 | before it ran | server | exploratory | to be decided |

The comparisons of cAUC with the pooled AUC and every result involving rho are exploratory. The paper does not
use "pre-registration"; it says "analysis plan committed to the repository" and points to this register.
