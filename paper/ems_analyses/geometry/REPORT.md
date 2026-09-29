# Evaluation-geometry analyses requested in referee round 5 — report (2026-09-19)

Specification written before any analysis ran: `SPEC.md` (one post-result deviation, D1, logged there).
Code: `paper/code/ems_geometry_common.py`, `ems_geometry_0_reproduce.py` … `ems_geometry_5_metrics.py`.
Inputs via `paper/code/_canonical.py` (SHA-256 verified); leakage assertion before every fit; seed 42.
Model, folds, scar, 2 km dilation and 10 km collar copied from the existing arms. These analyses are
**post hoc**, added in response to review.

## Reproduction gates (`reproduction_gates.json`)
Eight of nine scars reproduce `pool_decomposition.json` to four decimals. Manavgat row B is 0.589
against 0.597: the old script read the overwritten Manavgat file. Eight-scar A − B = 0.1427 (Table 2:
0.143). Transfer full/full 0.5414, 14/20; 10 km/10 km 0.6155, 19/20; paired delta +0.0223 (paper +0.0231,
same cause).

## 1. Distance bands and edge exclusion (`a1_*`) — supports the paper
Row-A AUC of burned cells against negatives in distance bands, mean over five regions: 0.615 (0–0.5 km),
0.668 (1–2 km), 0.748 (2–5 km), 0.803 (5–10 km), 0.830 (> 10 km), falling towards the fire in every
region. Excluding two cells either side of the scar edge still leaves 0.715 [0.623, 0.807] at 1–2 km
against 0.865 [0.838, 0.893] beyond 10 km. The frame cost A − B on the eight Table 2 scars:
0.143 [0.077, 0.208] with no exclusion, 0.133 [0.059, 0.208] at one cell, **0.122 [0.042, 0.202]** at
two cells (region-clustered [0.065, 0.203]). Edge label noise does not explain the cost; 85 % survives.

## 2. Placebo collars (`a2_*`) — supports the paper
Real scar shapes (8 orientations) placed in burned-free natural vegetation, 50 placements per scar.
Placebo mean 0.783 against A 0.784 and B 0.635: A − placebo +0.001 [−0.070, +0.072], placebo − B
+0.148 [+0.116, +0.180]. The placebo reproduces 0.7 % of the cost; the collar-only variant (D1) ≈ 0 %.
In 7 of 8 scars no placement scores as low as the real B. Limits: no valid placement for Montiferru's
largest scar; 33 candidates in Evia; placebos sit a median 15–20 km from the fire, so the test cannot
separate "fire-adjacent" from "near-field terrain".

## 3. Frame cost against far-field share (`a3_*`) — not established; qualifies the paper
Region-level slope +0.046 [−0.373, +0.464] (n = 5, df = 3). Scar-level slope −0.025 [−0.327, +0.278]
(pseudo-replicated). Montiferru, 2.1 % far field, still has A − B = 0.179. The 0.143 is a **near-field**
effect, full size in a fire-scale frame. The within-region cost of the 10 km collar does track the share
(+0.117 [−0.100, +0.334]). Section 4.4's "the same effect between regions" joins two different
mechanisms and must be reworded.

## 4. Label-free equalisation of transfer (`a4_*`) — supports the null, weakens the practical reading

| Frame | Mean thermal AUC | Above 0.5 | Paired delta [pair-cluster 95 %] |
|---|---:|---:|---|
| as drawn (full/full) | 0.541 | 14/20 | +0.004 [−0.027, +0.035] |
| 10 km collar (uses target labels) | 0.616 | 19/20 | +0.022 [−0.003, +0.047] |
| range trim, source full | 0.529 | 13/20 | −0.001 [−0.036, +0.033] |
| range trim, source 10 km | 0.553 | 14/20 | +0.005 [−0.028, +0.038] |
| area of applicability, source full | 0.562 | 13/20 | −0.001 [−0.045, +0.043] |
| area of applicability, source 10 km | **0.589** | 14/20 | +0.013 [−0.018, +0.040] |
| 20 km window at AOI centre | 0.485 | 8/20 | +0.012 [−0.028, +0.047] |

Every delta interval spans zero on every label-free frame, under pair-cluster and target-cluster
resampling. The best label-free frame recovers about 64 % of the mean-AUC lift and none of the gain in
directions above chance. **0.616 and 19/20 require target labels and must be presented only as a
diagnostic of unequal frames**; a deployer could expect about 0.53–0.59 and 13–14 of 20.

## 5. Prevalence-robust metrics (`a5_*`) — partial support
Region-wide → scar + 2 km, standardised partial AUC (FPR ≤ 0.1) drops 0.078 [0.037, 0.120]
(region-clustered [0.017, 0.157]) to about 0.53, so the cost is not a ROC-AUC artefact. Normalised
top-10 %/20 % capture shows no established drop (ill-conditioned at scar prevalences 0.34–0.87). In
transfer, partial AUC is 0.505 as drawn, 0.519 on the collar, 0.50–0.52 on label-free frames:
early-retrieval skill is near chance on every frame.
