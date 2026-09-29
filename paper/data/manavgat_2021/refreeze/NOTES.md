# Re-freeze notes (2026-09-23)

## Stage C: ERA5-Land validator
`scripts/validate_era5_land_regional_diagnostic.py` (repo 6381f4c, unchanged) was run in the official tree
against the frozen ERA5 namespace `4850c165…`. That namespace was copied from drive_new byte-identical: the
label does not enter ERA5 (`is_model_predictor` false; meteorology is label-independent).
- **actual mode: 27/27 PASS.** A02/A22: analysis_id `4850c165…` re-derived from the registry. A14: region
  keys and dates match the registry. A21: manifest hashes and sizes match.
- **dry-run mode: 15/15 PASS.** C06: observed windows match the registry. C10/C11: analysis_id is stable.
- The Manavgat windows are unchanged by the label correction, so the ERA5 diagnostic stands as frozen.
- Records: `era5_validator/`.

## Silent-failure audit: `scripts/main.py` exits 0 on failure
`scripts/main.py` catches command errors, prints `HATA: ...` and exits 0. A runner that trusts the exit code
therefore misses the failure. The repo code is not changed. Our runners detect it from `run_b2.sh` onward
(`grep "HATA:"`), committed in `847aa47`.

Scan of every earlier runner that calls `scripts/main.py`:

| Run | main.py steps | Evidence | Affected |
|---|---|---|---|
| 2026-09-19 `rerun_labelfix/_runners/post.sh`, control and pipeline trees | 11 each (step9g ×6, compare, decomposition, synthesis ×3) | No `HATA`/`ERROR` in `post_*.log` or in the 11 `logs/main_20260919_*.log` of each tree | **None** |
| 2026-09-23 `refreeze/_runners/run_b.sh`, first pass, both trees | 11 each | `HATA` in the three synthesis logs (missing non-Manavgat Step9G inputs) | **Synthesis 5/4/3-AOI.** Re-run successfully in `run_b2.sh` |
| round3 and round4 paper-side runners, canonical_rerun | none call `scripts/main.py` | — | — |

The two jobs that never ran in round 3 had different causes, not this one. `run_d` never started because
`_env.sh` overwrites `$R`, so `bash $R` executed a directory. The `feature_drop` merge was never queued.
Both are recorded in `paper/labelfix_rerun/round4/REPORT.md`.

## Pending text change (stage E, not applied)
Methods §3.13 replaces the 1.6×10⁻⁷ sentence with the following. User wording, 2026-09-23; keep "run
unchanged".

> The Manavgat 2021 outputs were re-frozen on the corrected label with the upstream pipeline at commit
> 6381f4c, run unchanged. The original label had been exported on 8 July 2026, before the month-alignment
> fix of the MCD64A1 query (commit 183be42, 11 July), and was never renewed, so the defect was a stale export
> rather than a code error. The repository's own reproduction check then refitted every within-region model
> and all twenty transfer directions against the re-frozen outputs: the within-region comparisons agree
> exactly and the transfer directions to within 1.3×10⁻⁸, under the repository's pre-existing tolerance of
> 10⁻⁶. The re-freeze and this check were carried out by the manuscript authors rather than independently
> by the pipeline's original author.
