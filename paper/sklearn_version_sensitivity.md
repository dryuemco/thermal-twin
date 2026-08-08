# scikit-learn version sensitivity of transfer AUC — measured, must be reported

**What this is.** While setting up the LORO analysis (2026-08-08) we reproduced two of the frozen
step9b pairwise transfers with byte-identical data (parquet sha256s match the step9b manifests),
an identical pipeline (median imputer fit on source, one-hot `handle_unknown=ignore`,
RF 300 trees / min_samples_leaf 3 / class_weight balanced / random_state 42, identical feature
order per `repo/core`'s `SHARED_THERMAL_MODEL_FEATURES`), and only the library version varying.

## Measurement — two probes, same code, same data, same seed

| Direction (thermal, TSG, raw) | Emrehan step9b (sklearn 1.9.0) | Ours, sklearn **1.7.2** | Ours, sklearn **1.9.0** |
|---|---|---|---|
| Montiferru → Bejís | 0.5483 | 0.5691 (**+0.0208**) | 0.5483 (0.0000) |
| Manavgat → Bejís | 0.3258 | 0.3518 (**+0.0260**) | 0.3258 (0.0000) |

A secondary observation in the same session: the full 20-run LORO grid moved by up to ~0.03 per
cell between 1.7.2 and 1.9.0 (e.g. Bejís raw-thermal fold 0.384 → 0.417), with the qualitative
pattern unchanged.

## Why this matters for the manuscript

- **The version effect (~0.02–0.03 AUC) is the same order as our headline effects (~0.05).**
  Transfer evaluation amplifies implementation noise: identically-seeded forests differ across
  versions (RNG consumption and splitter changes between 1.7 and 1.9), and out-of-distribution
  prediction magnifies those tree-level differences far beyond their in-region effect (step8c
  within-region numbers reproduce to ~4 decimals across environments; the transfer numbers do
  not).
- **Consequence for practice:** every number that enters the paper was produced under, or
  verified against, **scikit-learn 1.9.0** (Emrehan's recorded version; see
  `step10_input_audit.json`: numpy 2.4.4, pandas 3.0.2, scikit_learn 1.9.0). Our verification
  environment: WSL Ubuntu-22.04, micromamba, python 3.12, sklearn 1.9.0, pandas 3.0.5,
  numpy 2.5.1 — the two probes reproduce to four decimal places despite the small numpy/pandas
  differences, so the sensitivity is specifically to the scikit-learn version.
- **Reporting obligation:** the Methods section must state the exact scikit-learn version, and
  the point that cross-region AUCs are reproducible only at fixed library version belongs in a
  footnote or the reproducibility statement. Bootstrap CIs (±0.02–0.04 wide) already cover
  version-level jitter of single point estimates, which is the honest frame: point estimates
  carry an implementation tolerance of roughly ±0.02–0.03 in transfer settings.

Probe script: `paper/pairwise_check.py`.
