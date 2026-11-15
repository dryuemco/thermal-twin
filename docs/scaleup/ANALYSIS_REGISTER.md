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
| Base-rate re-reporting (8.1) | claim9_rereport.py | amendment 8 | after claim9 and claim10 | server (8, 14 Nov 21:25) | exploratory | no |
| Oracle truth, rho grid (8.2) | claim11_oracle.py | amendment 8 | before it ran | server | exploratory | no |
| Monte Carlo replicates, 20 km (8.3, 8.4) | claim12_replicates.py | amendment 8 | before they ran | server | exploratory | yes (one clause) |
| Calibrated scenarios (8.5) | claim13_calibrated.py | amendment 8 | before it ran | server | exploratory | yes (one clause) |
| Field checks (8.6) | field_checks.py | amendment 8 | before it ran | server | descriptive | no |
| G1: focal choice against later burning, rule 9.5 | claim14_future.py | amendment 9, 21:53 UTC; 9.9 before any comparison | before its own results; all earlier results known | server | confirmatory (rule 9.5: equivalence) | no |
| G1 future AUC difference thermal vs coordinate RF | claim14_future.py | amendment 9 (losses), 10.1 rule for G2 | before (losses), rule 10.1 after G1 | server | exploratory | yes |
| G2: location-using models, rule 10.1 | claim15_location.py | amendment 10, 07:37:14 UTC; run 07:38:17-07:40:20 | before its own results, after G1 | server | confirmatory for 10.1 only for the pairs whose results were unseen: met for coord-kNN, not met for thermal+coord and thermal+distance; the coordinate RF pair was known from G1 when 10.1 was written | yes |
| D of the distance-feature pair | claim15_followup.py | 10.5 | after | server | descriptive | no |
| G5: leave-one-fire/year/country out, largest event removed | claim15_location.py, claim15_followup.py | 10.2; countries 10.5 | before (10.2), countries after | server | sensitivity | no |
| G1d repeat pairs | claim15_location.py, claim15_followup.py | 10.3; shared cells 10.5 | before (10.3), tolerance after | server | descriptive | no |

The comparisons of cAUC with the pooled AUC and every result involving rho are exploratory. The paper does not
use "pre-registration"; it says that each rule was fixed before its own results but with the earlier results
known, and points to this register. The independent record of the semi-synthetic rule (Software Heritage,
19:05:38) is later than the first fire's output of that run (19:02:59); this is stated in the paper.
