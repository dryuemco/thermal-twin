# Few-Shot Recovery Curve

- schema: `few_shot_recovery.v1`
- analysis_id: `7348dfe74423acef7b5da3c0b64c45c73978738038797d490717d2c04e42b7c5`
- diagnostic class: `target_label_supervised_few_shot_adaptation_sensitivity`
- population: `burnable_tree_shrub_grass`
- blocks: 10 cells (approximately_5_km), 5 strict spatial folds
- budgets: [0, 1, 2, 4, 8, 16, 32]; 10 repeats for every k > 0

## Claim boundary

This is a supervised adaptation sensitivity analysis in which target labels
are deliberately used. It is **not** an operational deployment claim, **not**
active learning, **not** a causal decomposition and **not** target-label-free
adaptation.

## Forced decisions

1. Outer evaluation blocks are 10-cell (~5 km), not Step8B's canonical 2-cell
   blocks: a 2-cell block holds a median of 4 cells, so it is not a unit of
   labeling effort and would sit adjacent to the evaluation blocks.
2. No new bootstrap was designed. The frozen 10-cell ceiling artifacts are
   reused as a reproduction anchor; the 2-cell raw-transfer replicates are not
   comparable and are not reused.
3. k=0 and the ceiling carry one deterministic realisation, not ten duplicates,
   because neither has any block-selection randomness.

## Uncertainty wording

Every interval reported here is a **selection interval**: the 2.5th and 97.5th
percentiles across the 10 block-selection repeats. It describes which
blocks were selected and nothing else.
No hypothesis test was performed and no p-value is reported.

## Primary curve — roc_auc, thermal model

### bejis_2022_to_manavgat_2021

- raw (k=0): 0.314155
- ceiling (target-only): 0.882224
- ceiling gap: 0.568069

| budget | few-shot | selection interval | absolute recovery | recovery fraction | status |
|---:|---:|---|---:|---:|---|
| 0 | 0.314155 | [0.314155, 0.314155] | 0.000000 | 0.000000 | interpretable |
| 1 | 0.517572 | [0.352699, 0.581900] | 0.203417 | 0.358085 | interpretable |
| 2 | 0.564672 | [0.539593, 0.609824] | 0.250517 | 0.440997 | interpretable |
| 4 | 0.659122 | [0.606840, 0.707509] | 0.344967 | 0.607262 | interpretable |
| 8 | 0.697756 | [0.653943, 0.739730] | 0.383601 | 0.675273 | interpretable |
| 16 | 0.749946 | [0.726437, 0.777042] | 0.435791 | 0.767146 | interpretable |
| 32 | 0.819955 | [0.815060, 0.823635] | 0.505800 | 0.890386 | interpretable |

### bejis_2022_to_mugla_2021

- raw (k=0): 0.618475
- ceiling (target-only): 0.777327
- ceiling gap: 0.158852

| budget | few-shot | selection interval | absolute recovery | recovery fraction | status |
|---:|---:|---|---:|---:|---|
| 0 | 0.618475 | [0.618475, 0.618475] | 0.000000 | 0.000000 | interpretable |
| 1 | 0.575880 | [0.533043, 0.617314] | -0.042595 | -0.268143 | interpretable |
| 2 | 0.577376 | [0.545487, 0.609806] | -0.041099 | -0.258722 | interpretable |
| 4 | 0.578458 | [0.537798, 0.601029] | -0.040016 | -0.251910 | interpretable |
| 8 | 0.597705 | [0.550379, 0.639642] | -0.020770 | -0.130751 | interpretable |
| 16 | 0.637239 | [0.574346, 0.652211] | 0.018765 | 0.118127 | interpretable |
| 32 | 0.666136 | [0.629890, 0.694822] | 0.047661 | 0.300033 | interpretable |

### manavgat_2021_to_bejis_2022

- raw (k=0): 0.396403
- ceiling (target-only): 0.824469
- ceiling gap: 0.428066

| budget | few-shot | selection interval | absolute recovery | recovery fraction | status |
|---:|---:|---|---:|---:|---|
| 0 | 0.396403 | [0.396403, 0.396403] | 0.000000 | 0.000000 | interpretable |
| 1 | 0.446882 | [0.403189, 0.514094] | 0.050480 | 0.117925 | interpretable |
| 2 | 0.455851 | [0.408461, 0.511293] | 0.059448 | 0.138875 | interpretable |
| 4 | 0.540904 | [0.466311, 0.591753] | 0.144501 | 0.337567 | interpretable |
| 8 | 0.597718 | [0.565582, 0.616241] | 0.201315 | 0.470289 | interpretable |
| 16 | 0.689803 | [0.682873, 0.700242] | 0.293401 | 0.685410 | interpretable |
| 32 | 0.752284 | [0.735815, 0.761986] | 0.355882 | 0.831371 | interpretable |

### manavgat_2021_to_mugla_2021

- raw (k=0): 0.437662
- ceiling (target-only): 0.777327
- ceiling gap: 0.339665

| budget | few-shot | selection interval | absolute recovery | recovery fraction | status |
|---:|---:|---|---:|---:|---|
| 0 | 0.437662 | [0.437662, 0.437662] | 0.000000 | 0.000000 | interpretable |
| 1 | 0.446536 | [0.440409, 0.459407] | 0.008875 | 0.026128 | interpretable |
| 2 | 0.453104 | [0.442757, 0.468118] | 0.015442 | 0.045463 | interpretable |
| 4 | 0.467934 | [0.445113, 0.481336] | 0.030272 | 0.089125 | interpretable |
| 8 | 0.489876 | [0.466909, 0.504626] | 0.052214 | 0.153722 | interpretable |
| 16 | 0.532128 | [0.498389, 0.568219] | 0.094466 | 0.278114 | interpretable |
| 32 | 0.570647 | [0.556844, 0.590964] | 0.132985 | 0.391518 | interpretable |

### mugla_2021_to_bejis_2022

- raw (k=0): 0.583191
- ceiling (target-only): 0.824469
- ceiling gap: 0.241277

| budget | few-shot | selection interval | absolute recovery | recovery fraction | status |
|---:|---:|---|---:|---:|---|
| 0 | 0.583191 | [0.583191, 0.583191] | 0.000000 | 0.000000 | interpretable |
| 1 | 0.577605 | [0.553931, 0.606997] | -0.005586 | -0.023153 | interpretable |
| 2 | 0.602636 | [0.574560, 0.674372] | 0.019445 | 0.080591 | interpretable |
| 4 | 0.625034 | [0.604476, 0.688510] | 0.041843 | 0.173423 | interpretable |
| 8 | 0.666244 | [0.633484, 0.699484] | 0.083052 | 0.344220 | interpretable |
| 16 | 0.743105 | [0.735543, 0.748581] | 0.159914 | 0.662781 | interpretable |
| 32 | 0.788826 | [0.773326, 0.797340] | 0.205634 | 0.852274 | interpretable |

### mugla_2021_to_manavgat_2021

- raw (k=0): 0.344955
- ceiling (target-only): 0.882224
- ceiling gap: 0.537268

| budget | few-shot | selection interval | absolute recovery | recovery fraction | status |
|---:|---:|---|---:|---:|---|
| 0 | 0.344955 | [0.344955, 0.344955] | 0.000000 | 0.000000 | interpretable |
| 1 | 0.358062 | [0.350134, 0.384643] | 0.013107 | 0.024395 | interpretable |
| 2 | 0.380460 | [0.348848, 0.401804] | 0.035505 | 0.066084 | interpretable |
| 4 | 0.407233 | [0.376741, 0.438493] | 0.062278 | 0.115915 | interpretable |
| 8 | 0.436649 | [0.420079, 0.480270] | 0.091693 | 0.170666 | interpretable |
| 16 | 0.505018 | [0.486438, 0.532560] | 0.160063 | 0.297920 | interpretable |
| 32 | 0.624159 | [0.620411, 0.626120] | 0.279204 | 0.519673 | interpretable |

## Secondary metrics

`pr_auc` and `brier_score` are in `recovery_curve.csv` for every direction,
family and budget. Brier is lower-is-better, so recovery arithmetic uses
`oriented_value = -brier_score`; the natural-sign Brier is preserved in
`metric_value` and `raw_value`/`fewshot_value`/`ceiling_value`.

## Recovery-fraction rules

The fraction is signed and unclipped. Values below 0 (few-shot worse than raw)
and above 1 (few-shot above the ceiling) are preserved. A denominator within
1e-06 of zero yields an undefined fraction, and a
ceiling at or below raw is flagged rather than suppressed.

## Ceiling reproduction

- `bejis_2022` / baseline: expected 0.779370, observed 0.779370, match=True
- `bejis_2022` / thermal: expected 0.824469, observed 0.824469, match=True
- `manavgat_2021` / baseline: expected 0.820320, observed 0.820320, match=True
- `manavgat_2021` / thermal: expected 0.882224, observed 0.882224, match=True
- `mugla_2021` / baseline: expected 0.697986, observed 0.697986, match=True
- `mugla_2021` / thermal: expected 0.777327, observed 0.777327, match=True

## Limitations

- Outer evaluation blocks are 10-cell (~5 km), not Step8B's canonical 2-cell blocks. Values are not directly comparable to 2-cell Step8B/Step9B/Step10 numbers.
- No bootstrap interval exists for the raw endpoint at this block scale; existing Step9C/Step10 replicates resample 2-cell blocks and are not comparable. No new bootstrap was designed.
- The reported interval is a selection interval over 10 repeats. It describes block-selection variability only, is not a confidence interval, and supports no claim about statistical support.
- The frozen 10-cell ceiling anchors come from two separate robustness namespaces: the paired large-block run for manavgat_2021 and bejis_2022, and the per-experiment big-block run for mugla_2021. Both are read-only reproduction anchors under the same 10-cell contract; neither was produced or re-run by this analysis.
- At k=16 and k=32 some folds must include unburned-only adaptation blocks; the tier composition columns record where.
- evia_2021_extended is excluded by design; nothing here describes high-prevalence different-regime transfer.

## Fit accounting

- unique fits: 3642
- raw fits: 12 (reused across folds; mean references per fit 5.0)
- ceiling fits: 30 (shared across the directions of a target; mean references per fit 2.0)
- few-shot fits: 3600

