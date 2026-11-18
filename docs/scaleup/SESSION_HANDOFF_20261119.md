# Session handoff, 19 November 2026 (PC)

## What was done

The EMS draft of 14 November (thermal-twin-main, `paper/submissions/ems/manuscript.tex`) was judged not novel enough
by the authors. Three steps were taken to decide what the paper should be about:

1. Close reading of the work the method borrows from or competes with (SDM and spatial CV, 2020-2026 wildfire
   evaluation, decision-level and UAV evaluation, other fields). Notes outside the repository:
   `C:\Users\CORSAIR\projects\ThermalTwin\research_notes\Yöntem yeniliği ve hakem paneli\`.
2. Three independent simulated referees (spatial statistics/SDM, wildfire science, forecast verification/EMS
   editor), each writing a report before seeing the candidate methods. Synthesis (Turkish):
   `C:\Users\CORSAIR\projects\ThermalTwin\reports\Yöntem yeniliği ve hakem paneli.md`.
3. An independent Codex review (read-only, web search, without the referee notes):
   `docs/scaleup/reviews/codex_20261119_novelty_independent.md`. It opened the local result files.

## Decisions

- The paper is rewritten from scratch around the selection consequence: pooled within-event AUC (and cAUC) chose
  a coordinate-only random forest over the thermal random forest in 18 of 18 eligible fires, and that choice lost
  on later burning in the same landscapes. The 31/31 geographic-null result becomes a split-adequacy diagnostic,
  not the headline.
- The UAV patrol arm (ThermoSwarm A9 planner) is not part of this paper. All four reviews moved it to a separate
  paper: as written the planner takes the top-k cells without a flight budget, so its capture curve equals a
  prediction-rate (Molchan) curve, and WFDroneBench (arXiv 2609.11829) already evaluates risk maps by routed
  drones.
- The transfer and pre-fire LST sections leave this paper.

## Verified numbers (Codex, from results/scaleup/claim14-16 and claim12)

| Window | Pooled AUC / cAUC / stratified chose coordinate RF | Thermal RF minus coordinate RF, later AUC | Selection loss (pooled AUC) |
|---|---|---|---|
| through 2023 (claim15) | 18 / 17 / 11 of 18 | +0.116 [0.044, 0.204] | 0.127 |
| Jan 2024 - Sep 2026 (claim16, 11.4) | 18 / 17 / 14 of 18 | +0.069 [0.003, 0.135] | 0.094 |

- Claim 13 (scenarios tuned to the observed fires, 279 runs): balanced accuracy 0.500 / 0.496 / 0.492. Claim 12
  (nominal 5 km, 3,720 runs): 0.608 / 0.731 / 0.671, so cAUC helps in other settings. Report both.
- Manavgat label is the corrected one in the 31-fire artifacts (2,935 burned cells).

## Wording rules for the rewrite

- The result is about coordinate-only learners. Thermal RF + coordinates and thermal RF + training-burn distance
  did not meet the G2 rule in either window. Do not write "location-using models".
- 11.4 is a "frozen-score replication", not a blind test: the scores were frozen in November 2026, after the
  target period.
- Prior art that makes the selection question an application, not a new principle: Baker et al. 2024
  (Diversity and Distributions, 10.1111/ddi.13802), Finn et al. 2024 (J. Appl. Ecol., 10.1111/1365-2664.14616),
  Milà et al. 2024 (GMD, 10.5194/gmd-17-6007-2024). Fire-history references: Preisler et al. 2008
  (10.1071/WF06162), Moran et al. 2025 (10.1038/s41598-025-07968-6), Trucchia et al. 2022 (10.3390/fire5010030).
- No "first" claims (see section 3 of the Codex review for the list).
- No Diebold-Mariano test across sites; use paired cluster-level loss differences.

## Still open

- P2 (proper scores and matched-area capture against the fire-history reference, R1-offset) has no valid result:
  amendment 14.10 must be written and checkpoint 2 rerun (fixes listed in SESSION_HANDOFF_20261116.md).
- Codex's single most useful addition: one frozen, independently scored deployment test in new landscapes or
  seasons, including sites without later burns, declared before scoring.
- Hijmans (2012) full text was not obtained (paywalled); the 0.51 km floor in matching is our own change.
- thermal-twin-main has uncommitted changes in `paper/submissions/ems/` from before this session; left untouched.
