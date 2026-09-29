# Cross-region transfer intervals at two blocking scales

Written 2026-08-13. Internal working note, not a manuscript section.

## Why this was done

Table 4 of `04_results.md` reports raw cross-region transfer ROC-AUC for 20 ordered directions with
spatial-block bootstrap 95% intervals built on 2-cell (about 1 km) blocks. Methods Section 3.12
rejects that blocking scale for the concept-shift diagnostic. It states that 2-cell blocks ignore
short-range spatial autocorrelation and give intervals roughly four times too narrow, and it moves
that diagnostic to 10-cell (about 5 km) blocks. The headline counts in Section 4.4, "twelve of 20
directions above chance with CI support, six below chance with CI support", therefore rest on a
blocking choice the paper argues against elsewhere. The caption of Table R4 already concedes that
only 9 of 20 survive as CI-supported above chance under a 5 km bootstrap, but that concession is
unsourced in the working files and the below-chance count at 5 km is reported nowhere.

This note recomputes both blockings from the frozen per-cell predictions and gives every number.

Two quantities are covered, and they must not be confused. Part 1 is the **level**, the raw thermal
transfer AUC of Table 4. Part 2 is the **paired thermal-minus-baseline delta** of Table R6 and the
abstract. They come from different pipeline stages, step10 and step9c respectively, and both were
published at 2-cell blocking. A short section at the end records two side findings for whoever
edits the Results.

## Step 1: what exists locally

Everything needed is present. No new model fitting was required.

The step9c bootstrap resamples stored predictions only. `repo/src/step9c_cross_region_block_bootstrap.py`
reads `step9b/cross_region_transfer_predictions.parquet`, groups by `transfer_direction` and
`population`, takes the unique values of `target_spatial_block_id` as the resampling units, draws
`n_blocks` blocks with replacement, and keeps every row of each drawn block. Nothing is refitted.

Table 4 itself was produced by the step10 bootstrap, not step9c. `repo/core/step10_shared.py`
(`run_n_way_paired_bootstrap`) applies the same block scheme to the step10 prediction table and
records the raw arm as the series `roc_auc__raw_source_only_thermal`. The two differ in one respect
only: step9c redraws a degenerate replicate and counts it as an attempt, while step10 counts it as
invalid and moves on. The published values were checked against
`step10/step10_bootstrap_summary.csv`. So step10 is the correct reference, and the "record and
exclude" rule is the correct one to copy.

Two small rounding slips in Table 4 came out of that check. Fifty-eight of the 60 printed values
(point, lower bound, upper bound over 20 directions) agree exactly at three decimals. The
exceptions are Bejis to Mugla, printed as 0.619 where the stored value is 0.61847, and the lower
bound of Manavgat to Mugla, printed as 0.452 where the stored value is 0.45145. Both are the
printed digit, not the data. They are noted here so that the tables in this file, which use the
stored values, do not look inconsistent with the manuscript.

Per-cell predictions and grid indices are available for all 20 directions:

- `drive_new/cross_region/<pair>/step9b/cross_region_transfer_predictions.csv` holds
  `transfer_direction`, `population`, `target_cell_id`, `target_spatial_block_id`, `burned`,
  `baseline_probability` and `thermal_probability`. A CSV twin of the parquet exists for every pair,
  which matters because this machine has no Python.
- `target_cell_id` has the form `r<row_500m>_c<col_500m>`, so the grid indices are recoverable
  directly. `target_spatial_block_id` was verified to equal `row//2 _ col//2` for every one of the
  357,092 rows read across the 20 directions. Blocks at any other size can therefore be derived
  without touching step8a.
- `drive_new/cross_region/<pair>/step10/step10_predictions.parquet` holds the same raw arm plus the
  two adapted arms, but carries no `burned` column. The labels live in the step8a datasets. The
  step9b CSVs are self-contained and were used instead.

Sixteen pair directories exist. Ten of them cover the five regions of the manuscript, giving the 20
ordered directions. "Evia" in Table 4 is `evia_2021_extended`, confirmed by matching every raw point
estimate. Two pairs are stored twice under reversed directory names
(`manavgat_2021__mugla_2021` and `mugla_2021__manavgat_2021`; `bejis_2022__mugla_2021` and
`mugla_2021__bejis_2022`). Their step10 interval bounds are identical to all printed digits, so the
alphabetically first directory was used and the duplicate ignored.

Only the raw thermal arm is covered here, which is what the task asked for. The z-score and CORAL
columns of Table 4 would need the step10 parquet joined to step8a labels and were not recomputed.

## Part 1: the level (raw thermal transfer AUC)

Implemented in `transfer_ci_blocksize.mjs` (Node, no Python). The procedure copies step10 exactly:

- resampling unit is the block, drawn with replacement from the unique blocks of the target region;
- the number of draws equals the number of unique blocks;
- a block drawn k times contributes all of its cells k times;
- 1,000 replicates, seed 42;
- a replicate whose resampled target labels are all one class is recorded as invalid and skipped,
  not redrawn;
- equal-tailed 2.5 and 97.5 percentile bounds, with the linear interpolation `np.percentile` uses.

ROC-AUC is the rank statistic with tied predictions scored at 0.5, computed from a pre-sorted
prediction order and per-cell multiplicities. No replicate was invalid in any direction at either
blocking.

The one thing that cannot be copied is the random number stream. NumPy's PCG64 is not reproducible
in Node, so a mulberry32 generator seeded with 42 was used, as in the other Node analyses in this
directory. Agreement is therefore expected at Monte Carlo precision, not exactly.

### Validation against the published 2-cell intervals

Point estimates first. The recomputed raw thermal ROC-AUC reproduces the frozen step9b value in all
20 directions to 1.1e-16, that is, to double-precision round-off. The point estimates are unchanged
by anything in this note, as they must be.

Interval bounds, recomputed 2-cell against the published step10 2-cell:

| Quantity | Value |
|---|---|
| Mean absolute difference, lower bound | 0.0016 |
| Mean absolute difference, upper bound | 0.0010 |
| Worst single bound, lower | 0.0055 (Bejis to Montiferru) |
| Worst single bound, upper | 0.0041 (Manavgat to Montiferru) |
| Directions where the verdict agrees | 20 of 20 |

The agreement is at the third decimal on average and the worst case is 0.0055, on the smallest
target (Montiferru, 743 blocks), where the bootstrap is noisiest. This is the expected scale of
Monte Carlo disagreement between two 1,000-replicate runs with different generators. The
implementation is treated as validated.

The recomputed 2-cell counts are 12 above chance, 6 below chance and 2 uncertain. That matches the
published counts, and it matches direction by direction, not just in total.

### Results at both blockings

Full table in `transfer_ci_blocksize.csv`, per-direction detail in `transfer_ci_blocksize.json`.
Point estimates are unchanged. The 2-cell interval quoted below is the published step10 one.

| Direction | Point | 2-cell CI | Verdict | 10-cell CI | Verdict |
|---|---|---|---|---|---|
| Manavgat to Bejis | 0.326 | [0.305, 0.349] | below | [0.266, 0.388] | below |
| Bejis to Manavgat | 0.444 | [0.408, 0.480] | below | [0.345, 0.562] | uncertain |
| Manavgat to Mugla | 0.470 | [0.451, 0.488] | below | [0.415, 0.524] | uncertain |
| Mugla to Manavgat | 0.401 | [0.378, 0.426] | below | [0.353, 0.455] | below |
| Manavgat to Evia | 0.613 | [0.593, 0.631] | above | [0.561, 0.665] | above |
| Evia to Manavgat | 0.686 | [0.653, 0.716] | above | [0.589, 0.764] | above |
| Bejis to Mugla | 0.618 | [0.601, 0.635] | above | [0.562, 0.675] | above |
| Mugla to Bejis | 0.583 | [0.561, 0.607] | above | [0.532, 0.636] | above |
| Bejis to Evia | 0.383 | [0.363, 0.402] | below | [0.330, 0.431] | below |
| Evia to Bejis | 0.448 | [0.426, 0.470] | below | [0.394, 0.497] | below |
| Mugla to Evia | 0.653 | [0.636, 0.671] | above | [0.590, 0.709] | above |
| Evia to Mugla | 0.577 | [0.560, 0.593] | above | [0.520, 0.634] | above |
| Montiferru to Manavgat | 0.567 | [0.539, 0.594] | above | [0.497, 0.644] | uncertain |
| Manavgat to Montiferru | 0.533 | [0.488, 0.580] | uncertain | [0.411, 0.669] | uncertain |
| Montiferru to Bejis | 0.548 | [0.521, 0.578] | above | [0.479, 0.636] | uncertain |
| Bejis to Montiferru | 0.594 | [0.560, 0.631] | above | [0.467, 0.687] | uncertain |
| Montiferru to Mugla | 0.619 | [0.604, 0.634] | above | [0.570, 0.668] | above |
| Mugla to Montiferru | 0.531 | [0.495, 0.568] | uncertain | [0.457, 0.604] | uncertain |
| Montiferru to Evia | 0.586 | [0.565, 0.606] | above | [0.520, 0.649] | above |
| Evia to Montiferru | 0.647 | [0.608, 0.682] | above | [0.552, 0.738] | above |

### Counts

| Blocking | Above chance with CI support | Below chance with CI support | Uncertain |
|---|---|---|---|
| 2-cell (about 1 km), published | 12 | 6 | 2 |
| 10-cell (about 5 km) | 9 | 4 | 7 |

Five directions change verdict, all of them from supported to uncertain. Two leave the below-chance
group (Bejis to Manavgat, Manavgat to Mugla) and three leave the above-chance group (Montiferru to
Manavgat, Montiferru to Bejis, Bejis to Montiferru). No direction changes side of the chance line,
and no direction moves from uncertain to supported.

The nine that stay above chance are Manavgat to Evia, Evia to Manavgat, Bejis to Mugla, Mugla to
Bejis, Mugla to Evia, Evia to Mugla, Montiferru to Mugla, Montiferru to Evia, Evia to Montiferru.
This matches the "9 of 20" already conceded in the caption of Table R4, which is now sourced.

The four that stay below chance are Manavgat to Bejis, Mugla to Manavgat, Bejis to Evia and Evia to
Bejis. This number was not reported anywhere before.

### How much the intervals widen

Widening is by a factor of 2.1 to 3.6, median 2.8. Mean interval width goes from 0.051 to 0.141. The
"roughly four times" figure in Section 3.12 refers to the univariate reversal diagnostic, not to
these transfer intervals, and it should not be quoted for them. The direction of the correction is
the same but the size is smaller.

### Seed sensitivity

The whole analysis was repeated with generator seeds 43, 44, 45 and 46. The above-chance count is 9
at every seed. The below-chance count is 4 at seeds 42, 45 and 46 and 3 at seeds 43 and 44. One
direction sits on the boundary: Evia to Bejis, whose 10-cell upper bound lands at 0.497, 0.501,
0.504, 0.500 and 0.500 across the five seeds. It should be described as at the chance line rather
than as supported below it. Every other direction keeps its verdict at every seed. The honest
statement is 9 above, 3 to 4 below, 7 to 8 uncertain, with Evia to Bejis flagged as borderline.

## Part 2: the paired thermal-minus-baseline delta

Everything above concerns a **level**, the transfer AUC of the thermal model. This part concerns a
**difference**, the paired thermal-minus-baseline delta on the target. It is a separate quantity
with a separate source and it carries the manuscript's most prominent transfer claim: "CI-supported
positive in 10 directions, CI-supported negative in 7, and uncertain in 3". That claim appears in
Section 4.3 and Table R6, in Contribution 1 of the introduction, in the abstract and in Section 5.1.
Its intervals come from `baseline_vs_thermal_transfer.csv`, which reads `delta_roc_auc` out of
step9c, and they are 2-cell. So the same blocking objection applies.

Note the source differs from Part 1. The level intervals of Table 4 come from step10; these delta
intervals come from step9c. Both were reproduced against their own source.

Both probability series sit in the same prediction file, so the delta needs no new input. The delta
is formed **inside each replicate** on identical resampled target blocks, as Section 3.9 specifies,
and the replicate loop is shared with the level, so no level number changes.

### Validation at 2-cell blocking, and what it uncovered

Point estimates reproduce step9b exactly: baseline to 1.1e-16 and the delta to 2.2e-16 in all 20
directions. That rules out a swapped series mapping, which would flip the sign of every delta.

Interval bounds against the published step9c `delta_roc_auc`:

| Quantity | Value |
|---|---|
| Mean absolute difference, lower bound | 0.0012 |
| Mean absolute difference, upper bound | 0.0009 |
| Worst single bound, lower | 0.0039 |
| Worst single bound, upper | 0.0028 |
| Directions where the verdict agrees, seed 42 | 19 of 20 |
| Directions where the verdict agrees, seed 46 | 20 of 20 |

The bound agreement is the same Monte Carlo scale as in Part 1. The counts, however, come out as 11
positive, 7 negative and 2 uncertain at seed 42, not the published 10, 7 and 3.

**This is not a harness fault. It is a genuine boundary case, and it is a finding about the
published number.** One direction disagrees, Bejis to Manavgat. Its published step9c lower bound is
-0.00045. The recomputed lower bound is +0.00014, +0.00103, +0.00009, +0.00022 and -0.00027 at
seeds 42 to 46. At seed 46 the whole table reproduces exactly, 20 of 20 verdicts and counts of 10,
7 and 3. So the published split is decided by a bound sitting within one thousandth of zero, and a
different random stream moves it. `baseline_vs_thermal_transfer.md` already prints this direction
as "+0.023 [-0.000, +0.044]", which is the same fact in the same table.

The manuscript should therefore not assert 10 positive as though it were exact even at 2-cell
blocking. The honest 2-cell statement is 10 or 11 positive, 7 negative, 2 or 3 uncertain, with
Bejis to Manavgat named as sitting on zero.

### Results at both blockings

Delta is thermal minus baseline. The 2-cell interval quoted is the published step9c one.

| Direction | Baseline | Thermal | Delta | 2-cell CI | Verdict | 10-cell CI | Verdict |
|---|---|---|---|---|---|---|---|
| Manavgat to Bejis | 0.332 | 0.326 | -0.006 | [-0.023, +0.010] | uncertain | [-0.044, +0.028] | uncertain |
| Bejis to Manavgat | 0.421 | 0.444 | +0.023 | [-0.000, +0.044] | uncertain | [-0.031, +0.078] | uncertain |
| Manavgat to Mugla | 0.508 | 0.470 | -0.038 | [-0.051, -0.024] | negative | [-0.078, -0.001] | negative |
| Mugla to Manavgat | 0.522 | 0.401 | -0.121 | [-0.146, -0.098] | negative | [-0.157, -0.086] | negative |
| Manavgat to Evia | 0.594 | 0.613 | +0.019 | [+0.003, +0.034] | positive | [-0.024, +0.065] | uncertain |
| Evia to Manavgat | 0.676 | 0.686 | +0.010 | [-0.012, +0.032] | uncertain | [-0.038, +0.058] | uncertain |
| Bejis to Mugla | 0.592 | 0.618 | +0.026 | [+0.014, +0.038] | positive | [-0.016, +0.068] | uncertain |
| Mugla to Bejis | 0.451 | 0.583 | +0.132 | [+0.105, +0.158] | positive | [+0.065, +0.192] | positive |
| Bejis to Evia | 0.530 | 0.383 | -0.148 | [-0.168, -0.126] | negative | [-0.202, -0.095] | negative |
| Evia to Bejis | 0.392 | 0.448 | +0.056 | [+0.037, +0.077] | positive | [+0.019, +0.101] | positive |
| Mugla to Evia | 0.600 | 0.653 | +0.054 | [+0.039, +0.067] | positive | [+0.023, +0.083] | positive |
| Evia to Mugla | 0.513 | 0.577 | +0.064 | [+0.044, +0.083] | positive | [+0.005, +0.129] | positive |
| Montiferru to Manavgat | 0.502 | 0.567 | +0.065 | [+0.041, +0.091] | positive | [+0.009, +0.122] | positive |
| Manavgat to Montiferru | 0.578 | 0.533 | -0.045 | [-0.077, -0.010] | negative | [-0.112, +0.031] | uncertain |
| Montiferru to Bejis | 0.613 | 0.548 | -0.064 | [-0.082, -0.044] | negative | [-0.099, -0.026] | negative |
| Bejis to Montiferru | 0.553 | 0.594 | +0.041 | [+0.005, +0.073] | positive | [-0.045, +0.121] | uncertain |
| Montiferru to Mugla | 0.651 | 0.619 | -0.032 | [-0.048, -0.017] | negative | [-0.087, +0.024] | uncertain |
| Mugla to Montiferru | 0.611 | 0.531 | -0.079 | [-0.117, -0.037] | negative | [-0.170, +0.022] | uncertain |
| Montiferru to Evia | 0.556 | 0.586 | +0.030 | [+0.013, +0.046] | positive | [-0.008, +0.068] | uncertain |
| Evia to Montiferru | 0.549 | 0.647 | +0.097 | [+0.054, +0.138] | positive | [+0.013, +0.187] | positive |

### Delta counts

| Blocking | CI-supported positive | CI-supported negative | Uncertain |
|---|---|---|---|
| 2-cell (about 1 km), published | 10 | 7 | 3 |
| 10-cell (about 5 km) | 6 | 4 | 10 |

Seven directions change verdict, all of them from supported to uncertain. Four leave the positive
group (Manavgat to Evia, Bejis to Mugla, Bejis to Montiferru, Montiferru to Evia) and three leave
the negative group (Manavgat to Montiferru, Montiferru to Mugla, Mugla to Montiferru). No direction
crosses from positive to negative or back.

The six that stay positive are Mugla to Bejis, Evia to Bejis, Mugla to Evia, Evia to Mugla,
Montiferru to Manavgat and Evia to Montiferru. The four that stay negative are Manavgat to Mugla,
Mugla to Manavgat, Bejis to Evia and Montiferru to Bejis.

No point estimate changes sign, and none can. The point delta depends only on the predictions and
the labels, not on the blocking. Eight of the 20 point deltas are negative and 12 positive at both
blockings, exactly as before. Blocking changes only how much of that pattern is claimable.

Delta intervals widen by a factor of 1.5 to 3.4, median 2.3.

### Seed sensitivity of the delta

Same sweep, seeds 42 to 46. Two directions sit on the boundary at 10-cell blocking:

- **Manavgat to Mugla**, negative at four of five seeds. Its upper bound runs -0.0005, -0.0011,
  +0.0002, -0.0007, -0.0027.
- **Evia to Montiferru**, positive at four of five seeds. Its lower bound runs +0.0130, -0.0009,
  +0.0082, +0.0029, +0.0109.

Every other direction keeps its verdict at every seed. The 10-cell counts across the five seeds are
6/4/10, 5/4/11, 6/3/11, 6/4/10 and 6/4/10. The honest statement is 5 to 6 positive, 3 to 4 negative
and 10 to 11 uncertain, with those two directions named as borderline.

Adding the 2-cell boundary case found above, three directions in total should never be quoted as
though their verdict were firm: Bejis to Manavgat at 2-cell, Manavgat to Mugla and Evia to
Montiferru at 10-cell.

### What this does and does not change

The qualitative claim survives and is arguably strengthened. The thermal block's transfer
contribution is still sign-unstable across directions: it is CI-supported positive in six
directions and CI-supported negative in four at the conservative blocking, and the point deltas
still run from -0.148 to +0.132. A block worth +0.056 to +0.153 inside every region is still worth
about nothing on average across regions.

What does not survive is the precision of "10 positive, 7 negative, 3 uncertain". At 5 km blocking
half the matrix carries no verdict, and even at 2-cell the split between 10 and 11 positive is a
coin flip. Any sentence in the abstract or introduction that leans on the exact counts should be
rewritten to lean on the sign instability instead, which is what the argument actually needs.

## Two things to record for the Results agent

Both were found while checking the tables above. Neither changes a conclusion. Both would be
embarrassing if a referee found them first.

**1. Two mis-rounded cells in Table 4.** Bejis to Mugla is printed as 0.619 where the stored value
is 0.61847, which rounds to 0.618. The lower bound of Manavgat to Mugla is printed as 0.452 where
the stored value is 0.45145, which rounds to 0.451. The other 58 of the 60 printed values are
exact. This is a typesetting slip, not a data problem.

**2. The "four times too narrow" figure must not be quoted for transfer intervals.** Methods
Section 3.12 says 2-cell blocking gives intervals roughly four times too narrow. That statement is
about the univariate reversal diagnostic and it is correct there. For the transfer intervals
measured here the widening factor is smaller: 2.1 to 3.6 with a median of 2.8 for the levels, and
1.5 to 3.4 with a median of 2.3 for the paired deltas. If a Results sentence needs a number for the
transfer intervals, it should use those, not the four.

## What this implies for the manuscript

Not a change of conclusion, but a change of emphasis, and the same shape in both parts.

**Levels.** The paper's argument is that raw transfer is heterogeneous and includes anti-predictive
directions. That survives: four directions are still below chance with support at 5 km, and
Manavgat to Bejis at [0.266, 0.388] is nowhere near 0.5. What weakens is the precision of the
count. At the blocking scale the paper itself defends, 7 of 20 directions carry no verdict at all.
The sentence "twelve of 20 directions are above chance with CI support, six are below chance with
CI support" is defensible only with the 2-cell qualifier attached, and the paper argues 2-cell is
too narrow. The safer form is the 5 km one: 9 above, 4 below with one of those borderline, 7
uncertain.

**Paired delta.** The sign instability of the thermal block survives, and it is the part of the
claim the argument actually rests on. Six directions are CI-supported positive and four
CI-supported negative at 5 km, and the point deltas still span -0.148 to +0.132. What does not
survive is "10 positive, 7 negative, 3 uncertain" as a precise count. At 5 km it becomes 6, 4 and
10, and even at 2-cell the boundary between 10 and 11 positive turns on a bound sitting within one
thousandth of zero.

**Summary of the four numbers.**

| Quantity | 2-cell, as published | 10-cell |
|---|---|---|
| Level: above chance | 12 | 9 |
| Level: below chance | 6 | 4, one borderline |
| Delta: CI-supported positive | 10, borderline between 10 and 11 | 6, one borderline |
| Delta: CI-supported negative | 7 | 4, one borderline |

No manuscript section file was edited for this note.

## Provenance

Computed 2026-08-13 on Node v24.15.0, single-threaded, seed 42. Hashes are of the working-tree bytes
as read. Files under `drive_new/` and `repo/` were read only.

Analysis script and outputs (in `paper/`):

```
95de013f86153e695ff628df78ea5a2679560eb8ecefd6117b58f9634fd22725  transfer_ci_blocksize.mjs
3dac37f16ad09d61e0be5aa842c2a2ed1e11534dd3f5c5e58b63a7eebdd72ef3  transfer_ci_blocksize.csv
2bf54067278b3d771f3e1c95fe91d970fb000402764f71d14fffb2c14341d88f  transfer_ci_blocksize.json
```

Published tables this note validates against (in `paper/`, read only):

```
1365fd775d1b28d589b86355ae85659bb4f3c105943ad0206a7c6bce8d1fffd1  baseline_vs_thermal_transfer.csv
```

Procedure reference, read not run (`repo/`, read-only):

```
f4afd3d5ea14cc5c2c50d2c3c479551d3e78d3c8b785bb995c76dc931dfcab8a  repo/src/step9c_cross_region_block_bootstrap.py
f1f230c52917481e0cdc50eb08f673690ff51b917a0869b0f1bf94c0a1f8577f  repo/src/step10c_paired_evaluation_bootstrap.py
b286fc8de7a5d2304a36e1a632e9e3e348d875210295f3ec94864d2dc68881c7  repo/core/step10_shared.py
```

Data inputs, all under `drive_new/cross_region/` (read-only). Per pair, four files: the step9b
prediction table (both probability series, labels and grid indices), the step9b metrics file
(point-estimate check), the step9c bootstrap metrics (published 2-cell paired-delta interval) and
the step10 bootstrap summary (published 2-cell level interval).

```
0fec7824e34ba997311d51b7684f3f4666920a4dad9551ca606e3a923fb76038  manavgat_2021__bejis_2022/step9b/cross_region_transfer_predictions.csv
f39ba69a4a9fc18a7e80e921a11ec621e3a10f5d01b01e007b788cb1084ef0c6  manavgat_2021__bejis_2022/step9b/cross_region_transfer_metrics.json
09a3ad8bb0d8e3eada821fbb211ab3cd8bc4114313c3ccf1fe4ac5f3b92243c2  manavgat_2021__bejis_2022/step9c/cross_region_bootstrap_metrics.json
ae505a00a01e8fb293eff5978ff88595e762211707591f402f47680d6a897c6e  manavgat_2021__bejis_2022/step10/step10_bootstrap_summary.csv
fdffde49a1ab4239a2aa0b9a61641973ec382ae90078ddd8ee4686eace7b043e  manavgat_2021__mugla_2021/step9b/cross_region_transfer_predictions.csv
3bd2a6ecbd8b815969295ce6fcaa87b840b7dc4e6901e7dba50d49e142927fd7  manavgat_2021__mugla_2021/step9b/cross_region_transfer_metrics.json
9312a067ba8e8dc1c2d22b06a42db9643ecdae6548e488df2a4752dc794587a1  manavgat_2021__mugla_2021/step9c/cross_region_bootstrap_metrics.json
cea13d07ddf096fd788a8013ae570d2486bfcf74c10f59dcb576090a046965ef  manavgat_2021__mugla_2021/step10/step10_bootstrap_summary.csv
ad1eac88cf36311d4264531932b3ef669ac5ea4fe34dc653a0f0a118d328e5a6  manavgat_2021__evia_2021_extended/step9b/cross_region_transfer_predictions.csv
eb51989e28b0107f48f339c8232683b76056a874f5caeb47a4c64fe0cddea270  manavgat_2021__evia_2021_extended/step9b/cross_region_transfer_metrics.json
ec0c1cec3887c104d5f137f77e4fd7e5099168fbea3167fbeef52aecfaf832ba  manavgat_2021__evia_2021_extended/step9c/cross_region_bootstrap_metrics.json
43114092d3ccca81ddf8ae7901efd1be1825d47670ee260bc2d23129a0d9d88f  manavgat_2021__evia_2021_extended/step10/step10_bootstrap_summary.csv
297bc611c803dde42fabcd3b6f4035dee70e152cfab2fe27f707fa9c2e720155  montiferru_2021__manavgat_2021/step9b/cross_region_transfer_predictions.csv
ba8e09b1ac96ba6156fe23e9bcbfb8b5b0550245d9dd61d72bd101604af54552  montiferru_2021__manavgat_2021/step9b/cross_region_transfer_metrics.json
d9f23870b1343751f12acb96062546c1aab47c535e9e77285c193b64d148ffb5  montiferru_2021__manavgat_2021/step9c/cross_region_bootstrap_metrics.json
e6f93f7e8f861fd6a25ebb4ca07a62caa5758685f234826245e3e2200d89e841  montiferru_2021__manavgat_2021/step10/step10_bootstrap_summary.csv
552217e2337d8541bd64a757cc5795351215cda6d77482a50f801191b300054d  bejis_2022__mugla_2021/step9b/cross_region_transfer_predictions.csv
a635143d4e80f3ca863a243f174a958d27cd87837a889c6d01a5981885a50f6c  bejis_2022__mugla_2021/step9b/cross_region_transfer_metrics.json
377b592451d98f771e6f7783d45d6e7a5e7220b3ecab84809b4d0e0696f812c3  bejis_2022__mugla_2021/step9c/cross_region_bootstrap_metrics.json
8b92799201e362c1429fb67a16354dfd9213cfaa3ec06ca26ff65416ce49119f  bejis_2022__mugla_2021/step10/step10_bootstrap_summary.csv
54ba38fedc59aa69073755860614c398ed98336363daf00987b6dcebd8173320  bejis_2022__evia_2021_extended/step9b/cross_region_transfer_predictions.csv
346dd9a6fea611a907a9ba7c2cbc3af117f4add3c84905e829c41efafcf61194  bejis_2022__evia_2021_extended/step9b/cross_region_transfer_metrics.json
9a47878d79e3e5c88857192e6eb9b892556c03bcfa60889788b7ff8422e23e55  bejis_2022__evia_2021_extended/step9c/cross_region_bootstrap_metrics.json
2f9cdd63a91c5742f568b36e8f66dd1de1d794e49a6f3f270d1a2486897a0789  bejis_2022__evia_2021_extended/step10/step10_bootstrap_summary.csv
d3f541e7acc3af7e4d7058e2164220686488f5ee6747fa4c05ec5f7937b34b13  montiferru_2021__bejis_2022/step9b/cross_region_transfer_predictions.csv
014f74424f3417f16b2fad9764de515ada41e1b40bb5ab0ca45acc7067cd76a2  montiferru_2021__bejis_2022/step9b/cross_region_transfer_metrics.json
d49bb302702537ac34c5ddc6985dda770da1204225d4cbe299b877cf6904ab37  montiferru_2021__bejis_2022/step9c/cross_region_bootstrap_metrics.json
3cdb12d2f8e0ba9fb1b942181b136510a331e526036f632661eb574a5f945d4d  montiferru_2021__bejis_2022/step10/step10_bootstrap_summary.csv
98969f4508957262707126c9b7ff8fc3a34dc25db8122ddf9b30fe7288bfc404  mugla_2021__evia_2021_extended/step9b/cross_region_transfer_predictions.csv
48ae27122fa41282e55fb138cd394ad3adb613b360f8bb3c70b24dd4c0729e4e  mugla_2021__evia_2021_extended/step9b/cross_region_transfer_metrics.json
e18cf614047a0f255497534d0bf3235ec555f17870e9bea1b11eb7f2819f5562  mugla_2021__evia_2021_extended/step9c/cross_region_bootstrap_metrics.json
b775b0e0703806a955ee42833bff44726e54d4259918ae3f8c931e1b2c133ecf  mugla_2021__evia_2021_extended/step10/step10_bootstrap_summary.csv
7916628c232f167ead0ebd553c98981470e813d29ae856bf5656417cd244afb2  montiferru_2021__mugla_2021/step9b/cross_region_transfer_predictions.csv
39b2fb0cc60d71363ce2b033f52547c57fd7ebdb761975e5dc97b61609f0103c  montiferru_2021__mugla_2021/step9b/cross_region_transfer_metrics.json
0e91bb350f75c2f02123b83ea4115729a5bcd6bb25361efcfdd1dfa31896bf61  montiferru_2021__mugla_2021/step9c/cross_region_bootstrap_metrics.json
ba2773a62181686c172a60abe434cddccb27565b35df66e6c4dd5ab098259f91  montiferru_2021__mugla_2021/step10/step10_bootstrap_summary.csv
06f8db1c12f4b5ab26b1b707e24eb52f1a9a72f783da26a64217c7d3b98c98db  montiferru_2021__evia_2021_extended/step9b/cross_region_transfer_predictions.csv
9d60da0313bb93e392a9089c68220c1ca7b2d695b866b3f201bebfa45c01a8ed  montiferru_2021__evia_2021_extended/step9b/cross_region_transfer_metrics.json
c553560bd6262f72c04226e106649c1d06a99c5a32cdd4c76a72ba53bf217192  montiferru_2021__evia_2021_extended/step9c/cross_region_bootstrap_metrics.json
44ab1f4b8d6f4f90e2b682e9bad59bb6814aaf5f6f27e80b085f6a7ec61145cd  montiferru_2021__evia_2021_extended/step10/step10_bootstrap_summary.csv
```

Line endings: the hashes above are of the files as they sit in the working tree today. The
`drive_new/` tree is not under the `-text` attribute that protects `paper/mugla_transfer_raw/`, so
if a hash ever fails, strip carriage returns and compare again before suspecting the data.

## Reproducing

```
cd paper
node transfer_ci_blocksize.mjs
```

The script reads the step9b CSV twins, so it has no package dependency at all. It computes both the
level and the paired delta in one pass and rewrites `transfer_ci_blocksize.csv` and
`transfer_ci_blocksize.json` in place. Runtime is about two minutes. Setting `BSEED` to any other
value writes `transfer_ci_blocksize_seed<N>.csv` and `.json` instead, which is how both seed
sensitivity checks above were run.

The two `*_seed_stable` columns in the CSV are filled from hard-coded sets near the bottom of the
script. They record the outcome of that sweep, not of the single run, and the comment there says
so. If the sweep is ever repeated with different seeds, those sets need updating by hand.
