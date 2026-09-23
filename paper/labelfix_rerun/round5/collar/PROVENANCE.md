# round5/collar: the frame-transfer matrix on the corrected Manavgat label

**Re-run exception, 2026-09-23, on the corresponding author's decision.** The rule for this round
was "no re-runs". It is set aside here so that every number the paper prints in this round can be
traced to `round5`. Appendix D (Table B10) and Appendix A(s) had still carried frozen-label collar
values that contradicted Fig. 8. Two scripts were re-run, both **unchanged**. Each was byte-identical
to HEAD before running.

| File | Produced by | Invocation |
|---|---|---|
| `aoi_frame_transfer.csv` | `paper/code/regen_transfer_ci.py` | cwd repo root; `PAPER_ARTEFACTS=paper/labelfix_rerun/round5/collar THERMAL_TWIN_LABELS=corrected`; 4 min 20 s; log `regen_transfer_ci.log` |
| `aoi_frame_transfer_frozen_mugla.csv` / `.json` | `paper/code/frozen_mugla_verify_aoi_transfer.py` | cwd `paper/code`; `THERMAL_TWIN_LABELS=corrected`; argument = this path; 47 s; log `frozen_mugla_verify_aoi_transfer.log` |
| `aoa_directed_pair_summary.csv` | copy of the re-frozen pipeline output `diagnostics/marginal_aoa_completion/6d998eb5…/weighted_predictor_space/directed_pair_summary.csv` (step8a sha 5a5e876c) | copied, not computed |

Both scripts read Manavgat through `paper/code/_canonical.py`, i.e. the corrected table
`paper/data/manavgat_2021/step8a_500m_modeling_dataset_labelfix.parquet` (sha e4ab8b85). It equals
the re-frozen step8a (5a5e876c) in all 79 shared columns; the re-freeze adds only
`historical_burn_excluded`, all False.

## Which file is the paper's source

**`aoi_frame_transfer.csv` from `regen_transfer_ci.py` is the source of Table 3, Table B10 and
A(s).** It is the only one of the two that carries the 10-cell bootstrap bounds (`thermal_ci_lo`,
`thermal_ci_hi`, `ci_above_0.5`, `ci_below_0.5`).

**How the 2026-09-19 file came about.** The file cited until now,
`paper/labelfix_rerun/code/aoi_frame_transfer_frozen_mugla.csv`, carries those bound columns. It is
**not** the output of the script its name suggests, and it is not a two-step product either. It is a
byte copy of `regen_transfer_ci.py`'s output `aoi_frame_transfer.csv`, which `CHANGES.md` §0 lists
among the renames ("`aoi_frame_transfer.csv → aoi_frame_transfer_frozen_mugla.csv`"). The
2026-09-19 output of `frozen_mugla_verify_aoi_transfer.py` went to
`code/_staging/frozen_mugla_verify_aoi_transfer.csv`. It has no bound columns, and nothing in the
paper cites it.

So two scripts compute the same point matrix. One adds bounds, and its file was renamed to the
other's name.

## Reproduction against 2026-09-19

**Criterion** (set by the corresponding author): identical at the printed 3 dp, and |Δ| < 10⁻⁵ on
the computed values.

| Comparison | thermal | 10-cell bounds | baseline, delta | 3 dp | flags |
|---|---|---|---|---|---|
| `regen_transfer_ci.py`: this run vs `code/aoi_frame_transfer.csv` | 3.1×10⁻⁸ | 6.1×10⁻⁸ | 1.1×10⁻⁶ | all 100 rows identical | identical |
| `frozen_mugla_verify_aoi_transfer.py`: this run vs `code/_staging/frozen_mugla_verify_aoi_transfer.csv` | 9.7×10⁻⁹ | — | 1.9×10⁻⁶ | all 100 rows identical | — |

Both pass. The logs print identical means and counts. All five frame means and the
above/below/supported counts equal Table 3.

**Why not byte-identical.** Both scripts fit `RandomForestClassifier(n_jobs=4)`. The same script,
run twice in the same environment, differs from itself by the same magnitude (thermal 3.1×10⁻⁸,
baseline 1.4×10⁻⁶). The variation is therefore run-to-run thread nondeterminism, not a change of
input. It is the same class as the G1 legacy-pair exception of the re-freeze (1.3×10⁻⁵).

Methods §3.13 states that the 10⁻⁶ reproduction tolerance belongs to the CORAL and within-region
check, and that this script varies by up to 2×10⁻⁶.

## Assertions that bind the paper to these files

`paper/figures/fig8_contrast_pairs.py` asserts every cell of Table B10 and every number of the A(s)
paragraph at the printed 3 dp. The shared quantities (D̄, per-feature D, as-drawn transfer) are
checked against `round5/out_official/figure_contrast_pairs.json`, Fig. 8's own source. The collar
transfer, the ranks and the collar extremes are checked against `aoi_frame_transfer.csv` here, and
the AoA shares against `aoa_directed_pair_summary.csv`. A deliberately wrong B10 cell (0.494 for
0.493) makes the build fail. `paper/figures/check_all.py` runs the check.
