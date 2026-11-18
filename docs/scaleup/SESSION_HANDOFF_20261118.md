# Session handoff, 18 November 2026 (Mac, 16 to 18 November)

Nothing was run on the analysis machine and no plan text was changed in this session. It was a design
discussion: three method proposals, each reviewed by Codex, and a set of exploratory checks on result files
already committed. The author has not approved a direction yet.

## Where things stand

- Unchanged from SESSION_HANDOFF_20261116.md: amendment 14.10 (eleven agreed fixes) is still to be written, and
  checkpoint 2 must be rerun after it. The table of the first checkpoint 2 run must not be used.
- The blind sites (focal fires 2005-2016) are still unopened.
- The author asked for a method with novelty of about 4 of 5 for Environmental Modelling & Software. None of the
  three proposals reached that in review. Codex scored each at 2 of 5 as an idea and at most 3 of 5 with
  convincing evidence.

## The three proposals and their reviews

Briefs are in reviews/briefs/, replies in reviews/. Local paths in the briefs were replaced by placeholders.

| Round | Proposal | Brief | Reply | Verdict |
|---|---|---|---|---|
| 3 | Reach-conditional susceptibility (percolation likelihood, burned against outer-boundary cells, diffusion of fire history with learned conductance) | round3_reach_conditional.md | codex_20261116_round3.md | No-go as proposed |
| 4 | Event-unit evaluation (event-level intervals, performance forecast, abstaining rule) with a revised diagnosis | round4_event_unit.md | codex_20261116_round4.md | Go with changes, as an empirical evaluation paper |
| 5 | Placebo-fire calibration (the real scar relocated, pipeline refitted, calibrated transferable AUC) | round5_placebo_fire.md | codex_20261117_round5.md | Go with changes, as a bounded calibration study |

Errors in the proposals that the reviews found and that are accepted:

- Round 3. "beta = gamma = 0 gives exactly R1" is false on a finite degree grid. A mass-conserving diffusion mixes
  faster where conductance is high and does not attract mass to burnable ground. Event weights do not cancel
  weather. Distant unburned cells are legitimate negatives for a burn-occurrence target. The panel has no
  predictors for all cells of the buffered grid.
- Round 4. "Nothing can be measured inside one event" is wrong: cAUC and sAUC_c estimate the later AUC of the
  environmental model with a small mean error. The 90% claim had no support in the files (the R1 and coordinate
  numbers come from different tasks and site sets; only 13 sites are common to claim14 and claim16). A difference
  below the minimum detectable difference is unresolved, not a tie. The +0.005 and the SE of 0.024 for TMA-cell
  minus density belonged to different estimators (site-year mean against equal-site SE).
- Round 5. Relocated fire perimeters as a null exist already (Barros and Pereira 2014, PLoS ONE, 1,670 perimeters
  translated and rotated into 500 null maps). The calibrated-AUC formula is not identified away from the null and
  is unstable when the placebo AUC is near 1. The claim that a location-only model gets 0.5 by construction needs
  exchangeable placements, which the rectangles centred on the focal fire do not give. The synthetic comparison
  has 558 runs, not 744, and the ratio estimator is worse than cAUC for the coordinate model. A constant forecast
  of 0.5 already beats cAUC on the development fires.

## Exploratory checks made in this session

All from committed result files, no model fitted. `python scripts/explore/session_20261118_checks.py` prints
them. Codex reproduced items 1 to 3 and 5. Item 4 was computed after the last review and has not been checked
by anyone else.

1. Task G-A, 219 site-years, 29 sites: within-site SD of AUC across years 0.13 to 0.15 for the same procedure.
   TMA-cell minus density: +0.0052 (site-year mean), +0.0093 (equal-site mean, SE 0.024). Minimum detectable
   paired difference at 80% power about 0.068. About 1,340 sites would be needed to detect 0.01 with this SD. The
   SD of a difference between two closely related maps can be much smaller and has to be measured per contrast.
2. Focal-event models on 2024-2026 burning (claim16, 18 sites): thermal 0.594, baseline 0.597, thermal+coordinates
   0.581, thermal+distance 0.563, coordinate forest 0.525, coordinate kNN 0.523. Thermal minus coordinate forest
   0.069 (SE 0.035), thermal minus thermal+coordinates 0.013 (SE 0.025).
3. Mean signed error of the focal estimate against later AUC to 2023 (18 fires; sAUC_c on the 11 where it is
   supported):

   | Model | Raw AUC | cAUC | sAUC_c |
   |---|---|---|---|
   | Thermal | +0.23 | +0.03 | -0.01 |
   | Thermal + distance | +0.38 | +0.07 | +0.05 |
   | Thermal + coordinates | +0.38 | +0.17 | +0.13 |
   | Coordinate forest | +0.47 | +0.27 | +0.26 |
   | Coordinate kNN | +0.46 | +0.26 | +0.22 |

4. Site-level information in the focal measures (11 fires, wide uncertainty). Spearman correlation of sAUC_c
   with later AUC: thermal -0.22, thermal+distance +0.06, thermal+coordinates -0.62, coordinate forest -0.05. Mean
   absolute error of three forecasts of later AUC, in the order sAUC_c, constant 0.5, mean of the other sites:
   thermal 0.112, 0.119, 0.086; thermal+distance 0.112, 0.092, 0.086; thermal+coordinates 0.149, 0.099, 0.069;
   coordinate forest 0.259, 0.070, 0.078. Within a site, the order of the five models by focal measure is
   negatively related to their order on later burning (-0.29 to -0.41). The later AUC of the thermal model to 2023
   and in 2024-2026 correlate at +0.51 over 13 sites.
5. Synthetic runs of plan 6.2 with no environmental signal (a = 0, b > 0, 186 runs): the environmental forest
   scores 0.603 within the event (0.693 at b = 4, L = 10 km) against a true 0.501, the coordinate forest 0.799
   (0.919). Using the same fire's a = 0 run as one placebo draw on the 558 runs with a > 0 and b > 0: selection
   loss 0.058 raw AUC, 0.043 sAUC_c, 0.022 cAUC, 0.009 placebo difference, 0.006 always environmental.

## What the checks suggest about the diagnosis

- The focal-to-later gap is not specific to location-using models. The environmental model drops from 0.82 to
  0.60 on the 13 matched sites.
- The carry-over loss is shown for coordinate-only models. For thermal+coordinates the later difference is 0.013
  with an SE of 0.025.
- The distance corrections are close on average for the environmental model and overstate every model class that
  uses location.
- On these few fires no focal measure, corrected or not, ranks sites or models by later performance, and the
  mean of the other sites forecasts later AUC better than any of them (item 4).
- The 0.01 threshold of the method search is far below what about 30 sites can resolve for the contrasts
  measured so far. The four earlier attempts are unresolved by that standard. The stopping-rule outcome stays as
  recorded.

## Last recommendation given to the author (not approved)

Stop the method search and write the empirical evaluation paper Codex outlined in round 4, without the
response-curve calibration Codex suggested in round 5. Reasons for leaving the response curve out: plan 8.0
already showed that one event cannot tell a persistent spatial pattern from a transient one, and item 4 sets a
benchmark (mean of the other sites) that focal statistics do not approach. Steps:

1. Amendment 14.10 fixes (labels, complete two-year horizon, isotropic kernel).
2. Matched focal-to-later error table: raw AUC, cAUC, sAUC_c, constant 0.5 and the mean of the other sites, for
   the same environmental and location-using models, with equal-site paired intervals.
3. Corrected temporal benchmark: R1, one environmental model and the single R1-offset comparator (handoff item 6
   of 16 November).
4. Freeze, then one replication on the blind sites. Candidate blind hypothesis from item 4: the forecast from
   other sites has a lower absolute error than cAUC and sAUC_c, paired over sites.

An amendment 15 would have to record that the diagnosis was revised after all development results were seen,
keep the old wording, and state the plan 14.5 H1 problem (a gain of 0.01 with the lower bound above zero cannot be
detected with the available sites).

## Open decisions for the next session

- Which direction the author takes: the empirical paper above, one of the three proposals in reduced form
  (Codex allowed a boundary-trained correction as one extra check, and a placebo diagnostic as an add-on), or a
  further search for a method.
- Whether item 4 is worth a place in the plan. It rests on 11 to 18 fires and should be recomputed after the
  14.10 fixes before anything is built on it.

## Files added with this handoff

- docs/scaleup/SESSION_HANDOFF_20261118.md
- docs/scaleup/reviews/codex_20261116_round3.md, codex_20261116_round4.md, codex_20261117_round5.md
- docs/scaleup/reviews/briefs/round3_reach_conditional.md, round4_event_unit.md, round5_placebo_fire.md
- scripts/explore/session_20261118_checks.py
