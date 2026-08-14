# Referee round 4 — four referees, consolidated, verified, and dispositioned

**Panel.** Four independent reviews of the post-split manuscript (12,404 words, 6 tables, 65 pages),
2026-08-14. R1 thermal remote sensing; R2 spatial statistics and model validation; R3 wildfire
science and fire ecology; R4 reproducibility and data integrity, with repository access.

**Verdicts.** R1, R2, R3: **major revision**. R4: **minor revision**. That split is not a
disagreement. R4 checked roughly 620 numeric values and found no fabricated number, none moved in
the paper's favour, and no misreported zero-crossing; the other three attacked the framing. The
consistent finding of the round is therefore: **the arithmetic is sound and the prose outruns it.**

## The rule applied

No referee claim was applied before it was re-derived from the frozen artefacts. This is the rule
carried from round 3, where two of that dossier's own claims failed re-derivation. This round it was
applied to every load-bearing item.

**Score: 13 claims re-derived, 13 confirmed, 0 refuted.** The panel was materially more accurate
than round 3's dossier.

## What was verified, first-hand

| # | Claim | Source | Verified against | Verdict |
|---|---|---|---|---|
| 1 | The two removed predictors are `elevation_mean` and `lst_anomaly_mean`, and −0.081 splits −0.061 / −0.013 | R1-M14, R2-M2 | `feature_drop_transfer.md` | **confirmed** |
| 2 | "Strengthens rather than weakens" is false; Evia weakens | R1-M2, R4-§3.1 | `repo/docs/final_archive_followup_2026-08-08.md` | **confirmed** |
| 3 | Mean baseline transfer 0.537 against thermal 0.541 | R2-M1 | `baseline_vs_thermal_transfer.md` | **confirmed** |
| 4 | The 2022 two-event arm rests on 11 positive-carrying 5 km blocks | R2-M4 | counted from `cross_region_transfer_predictions.parquet` | **confirmed** (11 at B=10; 103 at B=2; 6 at B=20; 2021 arm 70) |
| 5 | "+0.004" appears nowhere in Results | R2-M6 | `04_results.md` | **confirmed** (0 occurrences; 6 in abstract) |
| 6 | Table R13 is cited but never defined | R1, R2 | `04_results.md:129` | **confirmed** |
| 7 | `tvdi_difference` is never defined | R1-M12 | `03_methods.md:86-91` | **confirmed** |
| 8 | §4.3's opening paragraph appears twice | R1, R2, R3, R4 | `04_results.md:86-88` / `121-123` | **confirmed** |
| 9 | The common-subset diagnostics rerun exists and supports the authors | R2-M8 | `diagnostics_common_subset.md` | **confirmed** (conditional +0.87/+0.85 lead on the common 12; all-9 variants null) |
| 10 | Dropping Evia flips the headline's sign | R2-M3 | `referee2_numbers.md` | **confirmed** (−0.0081 against +0.0148/+0.0021/+0.0065/+0.0060) |
| 11 | Dimarco et al. model ignition, not burned area | R3-M6 | `REFERENCES.bib:419-420` | **confirmed** (title: "human-driven wildfire **ignition** models") |
| 12 | MOD11A1 is used with no quality screening | R1-M11 | `repo/src/step1_fetch_modis.py:57,76` | **confirmed** (`LST_Day_1km`, `.mean()`, `QC_Day` absent) |
| 13 | "No bootstrap replicate was invalid at any block size" is false | R4-§2.1 | `.../bejis_2022/block_20_cells/step8c_large_block_bootstrap_summary.json` | **confirmed** (995 valid, **5 invalid**) |
| 14 | "Five directions below chance" should be six | R4-§2.3 | `four_aoi_decomposition.csv` | **confirmed** (0.326, 0.383, 0.401, 0.444, 0.448, 0.470) |

## Bucket A — applied

Changes the manuscript makes because a verified claim showed the text said more, or less, than the
evidence.

1. **The baseline transfer control enters the paper.** Mean baseline transfer 0.537 against thermal
   0.541. This is the decisive control for the paper's own thesis and it was absent. It does not
   destroy the finding; it changes what the finding is, from "dynamic predictors are less portable
   than stationary ones" to "in this matrix nothing transfers, and adding dynamic state neither
   helps nor hurts on average while destabilising the sign per pair."
2. **The two removed predictors are named, and the debit is decomposed.** −0.061 elevation,
   −0.013 LST anomaly. Elevation is a baseline terrain variable, so the abstract's placement of
   −0.081 under the thermal block's cost was misleading. The post-selection nature of both figures
   is stated.
3. **The exchange metaphor is retired where the transfer side is a null.** "Buys" and "spends" are
   replaced by what was measured: a local cost, and no compensating transfer gain.
4. **"Strengthens" becomes "survives"**, with the per-region directions and Evia's weakening stated.
5. **The two-event arm is downgraded to corroborating**, with its positive-carrying block counts
   printed. Eleven is below the floor of sixteen the paper sets for itself in Table 3's own note.
6. **§4.7g's sign-invariance is restated as the identity it is.** Block size is the resampling unit;
   it cannot move a point estimate. The "sign pattern is robust" fallback is removed.
7. **The invalid-replicate sentence is corrected** (Bejís, 20 cells, 5 of 1000 single-class).
8. **Five below-chance directions becomes six.** The "at most 34 %" conclusion survives a fortiori.
9. **The duplicated §4.3 paragraph is deleted.**
10. **`tvdi_difference` is defined.**
11. **The common-subset diagnostics control enters §4.4.** It is the direct answer to "your marginal
    family fails only because it has half the sample", and it favours the authors.
12. **The headline interval enters Results**, with its four resampling units named, and the
    leave-one-region-out result that dropping Evia flips the sign.
13. **The niche-overlap point-estimate qualifier** is carried into the abstract, §1.4 and §5.3,
    where §4.5 and §6 already have it.
14. **The Dimarco comparison is qualified**: their response variable is ignition, ours is burned
    area, so the predictor-class reading is one of at least two explanations.
15. **The QC screening candidate for Manavgat is replaced by a measured negative**, from the
    propagation run of 2026-08-14 (`modis_qc_downstream_propagation.md`).
16. **Dangling and imprecise references fixed**: Table R13, "roughly 200 km" (307 km by the paper's
    own diagnostic), "no adapted direction exceeding 0.63" (0.630), "a few hundredths" (up to 0.07),
    the six Table 4 rounding slips, and the stale S1 provenance paragraph, which currently
    *understates* the released artefact.

## Bucket B — verified, deliberately not applied

1. **R3-M7, the fuel-limited / drought-limited framing.** The referee is almost certainly right that
   this is the mechanism, and the framing would strengthen the paper. It is not applied because it
   requires citing roughly ten works the referee supplied from memory and explicitly asked us to
   verify, and this project does not cite unread sources. **This is the highest-value writing change
   available and it should be done once the sources are read.**
2. **R3-M8, the anomaly-only feature set.** Genuinely promising: the two internally normalised
   channels are the ones that do not reverse, and a third feature set could convert a negative paper
   into a constructive one. It is a new twenty-direction run, not an edit.
3. **R3-M2, scar-anchored signed AUCs.** Cheap and decisive, but a new computation.
4. **R3-M3, multi-year labels.** The strongest available test of whether the reversal is regional or
   event-level. A substantial new build.
5. **R2-M9, the AOA inside-versus-outside paired test.** The referee is right that the paper tests an
   estimand the AOA was not built to supply. A new computation on frozen inputs.
6. **R2-M10, recomputing the adapted arms at 5 km.** A new run.
7. **R1-M4, screening the four baseline years for earlier fires.** A new run.

Items 2 to 7 are recorded as the work the next round should do, in that order.

## Bucket C — referee wrong, or not applicable

*Empty.* No claim from this panel failed re-derivation. Two were narrowed rather than rejected:
R3-M6 (the Dimarco design is not identical, but the shared MCD64A1 label source is real, so the
sentence is qualified rather than retracted) and R2-M5 (the sign-invariance is vacuous as
*justified*, but the underlying sign pattern is still a fact about the data, so it is restated
rather than deleted).

## What the panel praised, unprompted and in common

Recorded because it should not be lost in revision: Table 3's resampling-unit note, which counts
positive-carrying blocks at every scale and then demotes its own most favourable row; §4.8's
structural-asymmetry paragraph, which works out which way its own bias runs; §5.9(ix), which
volunteers that a published count turns on a bound of −0.00045; §4.4, which reports the Bonferroni
threshold that kills its own significant result; the pre-registered regime hypothesis reported as a
null; and the leakage protocol, which R4 found to be enforced by whitelist at import time and
therefore stronger than the manuscript claims for it.
