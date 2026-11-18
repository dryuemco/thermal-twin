# Independent review request 2: a revised diagnosis and an "event-unit evaluation" method

You are an independent, sceptical reviewer. Read-only: do not modify any file. Give your own judgement,
including whether the new diagnosis is wrong or the method is not worth a paper. Do not defer to the proposal.

## Context

Same project as your review an hour ago (thermal-twin, Environmental Modelling & Software, 31 Mediterranean
fire landscapes, 500 m grids). Folder with copies of the branch documents and scripts:

<review folder>/

- docs/ANALYSIS_PLAN.md (amendments 1-14), docs/ANALYSIS_REGISTER.md, docs/SESSION_HANDOFF_20261116.md,
  docs/codex_20261116_round1.md, docs/codex_20261116_round2.md, docs/*.py
- brief.md and codex_reply.md: the reach-conditional proposal and your "no-go as proposed" reply. That proposal
  is withdrawn as the main plan. Your points on nesting, mass-conserving diffusion, event effects, distant
  negatives and the simpler interpolation explanation are accepted.

Result files copied from origin/scaleup-31fires, for checking the numbers below (python3 with pandas is available):

<scratch folder>/tr.csv
  = results/tma/dev/tma_cell_transitions.csv (per site-year out-of-group transition AUC, task G-A, columns
  tma_cell, tma, f_only, density, pooled_density_rank, standard_spatial, coord_dist_forest; target all/wildfire)
.../scratchpad/c16.csv = results/scaleup/claim16/claim16_per_fire.csv (frozen focal-event models scored on
  2024-2026 burning; eligible sites only are used)
.../scratchpad/c14.csv = results/scaleup/claim14/claim14_future_per_fire.csv (focal AUC, cAUC, sAUC_c and
  2017-2023 later-burning AUC per fire)

You can also read the branch with `git show origin/scaleup-31fires:<path>` from the repository root.

## Numbers computed today from those files (please verify the arithmetic and the reading)

- c14, 18 fires: focal within-event AUC of the thermal forest 0.836, of the coordinate forest 0.964; thermal cAUC
  0.641, sAUC_c 0.607.
- c16, 18 eligible sites, AUC on 2024-2026 burning: thermal 0.594, baseline (no thermal features) 0.597,
  thermal+coordinates 0.581, thermal+distance 0.563, coordinate forest 0.525, coordinate kNN 0.523.
  Paired differences, thermal minus other, mean (SE over sites): coordinate forest 0.069 (0.035), coordinate kNN
  0.071 (0.029), thermal+coordinates 0.013 (0.025), thermal+distance 0.031 (0.018), baseline -0.003 (0.016).
- tr.csv, target "all", 219 site-years with every candidate, 29 sites: mean AUC tma_cell 0.664, f_only 0.655,
  density (R1) 0.659. SD of AUC across site-years 0.14-0.18. Mean within-site SD across years (same procedure,
  same site) 0.13-0.15. tma_cell minus density: mean +0.005, SD of site means 0.131, SE over 29 sites 0.024.
  Minimum detectable paired difference at 80% power, two-sided 0.05: 2.8 * 0.131 / sqrt(29) = 0.068. Sites
  needed to detect 0.01 with that SD: about 1,300.

## Revised diagnosis

Old diagnosis (plan 13.8): within-event evaluation selects location-using models and this preference does not
carry over to later burning.

Why it may be incomplete or wrong:
1. Within-event evaluation also misleads for the correctly chosen environmental model (0.84 within the event,
   0.59 on later burning). The loss is not specific to location-using models.
2. The carry-over loss is established only for coordinate-only models (0.07, about 2 SE). For the practical
   location-using model (thermal+coordinates) it is 0.013 with SE 0.025.
3. The best predictor of later burning is itself a pure location model (R1, history density). Location
   information is not the culprit.
4. The method search used a 0.01 threshold, about one seventh of the detectable difference with about 30 sites.
   The four "failed" attempts (-0.003 to +0.008) are uninformative rather than negative.

New diagnosis: the unit of evidence is the event, not the cell. One scar is one observation, so nothing can be
selected or measured inside it, whatever the model or the distance correction. With events replicated in time,
location becomes the best predictor (R1). With events replicated across sites, the evaluation becomes accurate
(cross-site estimates within 0.02-0.05 of later performance against 0.23-0.47 for within-event estimates,
exploratory, plan 13.9 and 14.0). Model differences of the size the project chased are below the event-level
noise floor.

## Proposed method: event-unit evaluation (claimed to succeed with about 90% probability)

1. Event-level uncertainty. Every AUC and every paired difference gets an interval from resampling events and
   sites (never cells) and a minimum detectable difference (MDD). Differences below the MDD are reported as ties.
   Validation: the predicted standard error is compared with the observed spread across years and periods, and
   the spread of AUC is related to the number of separate events in the target year.
2. Performance forecast. Before the blind labels are opened, each procedure's later-burning AUC at each blind
   site is forecast, with a prediction interval, from transitions at other geographic groups. The within-event
   estimate is the comparator. This is H2 of plan 14.5 with an explicit forecast interval.
3. Abstaining decision rule. A procedure-level selector: the map is R1 unless a candidate beats R1 on earlier,
   out-of-group transitions by more than the MDD. The agreed R1-offset comparator (handoff item 6) is the first
   candidate. Compared on the blind sites, by selection loss on later burning, with within-event selection (pooled
   AUC, cAUC) among the focal-event models.

Why about 90%: the two blind contrasts are expected to be large relative to their standard errors. Forecast error
of within-event against cross-site estimates about 0.2; later-burning AUC of the rule's map (R1, about 0.675 in
development) against the map chosen within the event (coordinate models, about 0.52) about 0.15; paired SD about
0.15 and about 20 clusters give SE about 0.035, so both are about 4 SE.

Stated costs: no better map than R1; novelty guessed at 3 of 5; plan 14.5 H1 (gain at least 0.01 with the lower
bound above 0) cannot detect any realistic gain and should be restated in terms of the MDD before the freeze; the
G-B numbers carry the label problems you found (round 2) and the effect sizes must be rechecked after the 14.10
fixes.

## What I want from you

1. Verify the numbers above from the three csv files. Flag any that are wrong or misread (for example, which
   later-burning task and population each file uses, and whether "eligible" sites are comparable across files).
2. Is the revised diagnosis right? Check each of the four arguments. In particular: is 0.84 against 0.59 a fair
   comparison (different tasks, populations, prevalence, focal scar removed), and does the cAUC of 0.64 already
   predict the later 0.59, which would mean distance-corrected within-event evaluation works for environmental
   models and the "nothing can be measured inside one event" claim is too strong?
3. Is the MDD argument sound? Site means as the unit, heterogeneity across sites, AUC bounded, unequal years per
   site, clustered sites, one-sided against two-sided, and whether a paired difference between two specific
   procedures can have a much smaller SD than 0.13 (so that 0.01 could be detectable for closely related maps).
4. Is the 90% claim credible? Recompute the expected z for the two blind contrasts with what the files support.
   What is the main way each could fail on the blind sites (for example fewer eligible sites, R1 weaker on 2005-2016
   focal fires with a shorter history, the coordinate model not chosen within the event, the 14.10 label fixes)?
   Give your own probability for each of the two contrasts.
5. Is contrast 3 a straw man? Nobody deploys a coordinate-only forest. What is the fair comparator set, and does
   the rule still win against "always choose the environmental model" or against cAUC-based selection?
6. Novelty for EMS, 1 to 5, with the closest precedents you can verify (clustered ROC inference, for example
   Obuchowski 1997; leave-location-out and target-oriented validation, Meyer et al.; Roberts et al. 2017; power
   and minimum detectable effects in model comparison; performance forecasting or "validation of the validation").
   Say which you verified.
7. Does this differ enough from amendment 14 (which you rated 2-3 of 5) to be a new contribution, or is it the same
   protocol with intervals added?
8. Forking paths and the blind test: the diagnosis itself is now being revised after all development results.
   How should that be recorded, and which blind hypotheses would you freeze?
9. If you had to choose one paper to write from this project today, what would its single headline claim be, and
   what is the smallest set of analyses that supports it?

Output: verdict in the first line (go / go with changes / no-go), numbered answers 1-9, then a ranked list of
minimum changes. Be concrete. Mark anything you could not verify.
