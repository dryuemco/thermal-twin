# Study design rationale (v1.0, 2026-09-19)

**This document states no rules.** Every binding rule, threshold and parameter is in
`PREREGISTRATION.md` (v1.2), which is the single source. Keeping rules in one place is itself a design
decision: in draft v0.4 the same rules were written in several documents and an adversarial review
found eleven conflicts between them. This file records *why* each decision was taken, so a reader can
judge it; `PREREGISTRATION.md` records *what* will be done.

Revision history: v0.1–v0.4 (drafts, 2026-09-19); adversarial review of the registration (5 blockers,
11 major, 13 minor items, all addressed in `PREREGISTRATION.md` v1.1); second adversarial review (no blockers; 8 major and 15 minor items, all addressed in v1.2); v1.0 (this rationale).

## Why this study

The pilot (`paper/PILOT_FROZEN.md`, tag `pilot-v1-frozen`) found that wildfire susceptibility models
validated inside a region lose much of their skill elsewhere, and that how a region is framed changes the
measured skill as much as the predictors do. It could not separate a new region from a new fire season,
had no weather or human predictors, drew its regions by hand, and added most controls after seeing
results. This study is designed to answer the same questions without those weaknesses.

## Contribution (fixed before any result)

In one pre-registered design on rule-defined regions: (i) how much the evaluation frame alone changes
reported skill; (ii) separate estimates of the temporal (another season) and spatial (another region)
parts of the transfer gap, with their difference reported against a pre-registered detectability bound;
(iii) which predictor groups carry skill that travels; (iv) an open, tested research infrastructure.
The use case is a pre-season susceptibility map used to prioritise prevention.

## Decisions and their reasons

| Decision (rule in `PREREGISTRATION.md`) | Reason |
|---|---|
| Regions are tiles of a fixed 1° grid (§3) | Removes hand-drawn frames, the pilot's largest source of bias. 1° rather than 0.5°: with blocks no smaller than the 11 km weather resolution, a 0.5° tile holds about 20 blocks and a typical season touches 2–6, so almost no 0.5° tile could support spatial cross-validation. |
| 3–5 seasons per tile, 2015–2024 (§4.3) | Separates region from event weather, which one season per region cannot. |
| Deterministic cohort rule with an overlap constraint (§4.6) | Prevents selection by judgement; guarantees that tile pairs share seasons so the spatial transfer estimand exists. |
| Separation, pilot and trial exclusions (§4.4, §4.5) | Separation stops one fire or one autocorrelated neighbourhood spanning training and test; exclusions keep the cohort independent of everything the authors have already seen. |
| Two sealed hold-out tiles, one negative-control tile (§4.6, §15) | Tests whether conclusions hold out of sample; shows the gate separates agricultural burning from wildfire. |
| Native MCD64A1 grid, unit-tested label query (§3, §5.1) | The pilot's label defect came from an untested query; its grid was misaligned with the label. |
| Pre-season predictors only (§5.2) | A genuine forecast: no predictor can post-date a label. |
| Land cover of the year before (§4.1, §5.2) | The pilot defined its population with a map that may reflect post-fire state. The same reason excludes canopy height. |
| Weather, drought, FWI, human access, fire history (§5.2) | The pilot had none; transfer failure could not be attributed. |
| Redundancy rule (§5.3) | The pilot's six thermal channels were two dimensions, inflating one group. |
| V2 leakage rule (§5.5) | A model trained on later seasons would otherwise see the target season through fire-history predictors. |
| Fixed block size at the weather resolution (§6.1) | Removes a circularity in the draft and limits (the 0.1° weather lattice is not aligned with the analysis grid, so it cannot prevent) a weather pixel spanning training and test blocks. |
| Three model families with fixed settings (§6.3) | No tuning on evaluation data; robustness to model choice. |
| Crossed model with a pair effect (§11.1) | The pilot's transfer heterogeneity is reciprocal; without the pair term, simulated interval coverage is 0.90–0.92. |
| Equivalence margins and the P3 bound (§11.4) | At 10 tiles the temporal-versus-spatial difference is detectable only above about 0.12; a null must be read as a bound. |
| Planted-signal check (§9) | Shows the chain recovers a known gap before it is trusted on real labels. |
| Outcome lock, public registration, Software Heritage (§16, §19) | The registration cannot be edited after results; the timestamp is independent of the authors. |

## Threats to validity and their safeguards

| Threat | Safeguard (§ of `PREREGISTRATION.md`) |
|---|---|
| Frame drawn around the fire | Fixed-grid tiles; label-conditioned frames only as diagnostics (§3, §8) |
| Region confounded with event weather | 3–5 seasons; V2 vs V3 (§4.3, §6.2) |
| Spatial transfer undefined for some pairs | Overlap constraint in selection (§4.6) |
| Missing drivers | Weather, drought, human and fire-history groups (§5.2) |
| Label defects; small fires | Native grid, tested query, EFFIS and FireCCI sensitivities (§5.1, §12) |
| Post-fire information in predictors or population | Land cover and tree cover of *y* − 1; no canopy height; pre-season windows (§4.1, §5.2) |
| Temporal leakage in V2 | Target season treated as unobserved; past-only and block-disjoint variants (§5.5) |
| Spatial leakage between regions | Separation; spatial blocking (§4.4, §6.1) |
| Circular or unattainable eligibility | Fixed block size; full predictor list for eligibility (§4.2, §6.1) |
| Redundant predictors | Redundancy rule (§5.3) |
| Inconsistent quality screening | One rule per product for all tiles (§5.2, `PRODUCT_SPECS.md`) |
| Terra orbit drift | G4 contrasts repeated on 2015–2022 (§12) |
| Prevalence differences | Prevalence reported; prevalence-robust metrics (§7) |
| Oracle calibration presented as skill | Raw Brier first; recalibration labelled as target-oracle (§7) |
| Tuning on evaluation data | Fixed hyperparameters (§6.3) |
| Forking paths after results | Registration, outcome lock, deviations log (§16, §17) |
| Resampling unit chosen by result | Primary model fixed; all units reported; coverage-based switch decided before outcomes (§4.8, §11) |
| Nulls read as absence | Equivalence margins, P3 rule (§11.4) |
| Multiple comparisons | Holm within declared families; permutation p-values for pair diagnostics (§10.3, §11.5) |
| Training-size confound between designs | Size-matched sensitivity (§6.2, §12) |
| Conclusions specific to the cohort | Sealed hold-out; scope stated in advance (§15, §18) |
| Pipeline error | Tests, manifest hashes, planted-signal check (§9, §14) |
| Dataset changes during the study | Asset versions and file hashes frozen at export (§14) |
| Irreproducibility | Pinned environment, container digest, public code and data (§6.3) |
| Undisclosed prior knowledge | Disclosure of the pilot, the trial's candidate list and its AOI (§1) |
| Registration edited later | Public tag archived by Software Heritage; never moved (§19) |
| Study continued when invalid | Abandonment rule; planted-signal failure rule (§4.7, §9) |
