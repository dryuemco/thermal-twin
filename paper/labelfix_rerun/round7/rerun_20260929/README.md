# Rerun of 29 September 2026

A fresh rerun, from the corrected SHA-verified Manavgat parquet, of two sources the internal review
asked to see demonstrated rather than assumed.

- `aoi_frame_transfer.csv`, `regen_transfer_ci.log`: `paper/code/regen_transfer_ci.py`, unchanged,
  `THERMAL_TWIN_LABELS=corrected`. Against `round5/collar/aoi_frame_transfer.csv` all 100 rows agree;
  the largest difference is 1.4e-6 (baseline and delta), 6e-8 on the thermal AUC.
- `table1_manavgat.py`, `.json`, `.log`: Table 1's Manavgat rows recomputed with step10's own functions.
  Every point value agrees at 3 dp. The printed intervals are the pipeline's own bootstrap
  (`pipeline/experiments/manavgat_2021/step8c/`, `pipeline/robustness/step8_large_block/`), which they
  equal; step10's separate bootstrap moves two lower bounds by 0.001 (+0.061, +0.041).
