# Independent review request: a proposed fifth method for the thermal-twin paper

You are reviewing a method proposal as an independent, sceptical peer. Read-only: do not modify any file.
I want your own judgement, including whether the idea is wrong. Do not defer to the proposal.

## Context (read these first)

Project: wildfire susceptibility paper aimed at Environmental Modelling & Software, 31 Mediterranean fire
landscapes on 500 m grids. The analysis branch is `scaleup-31fires` (not checked out locally). Copies of its
documents are in this folder, and you can also read them with `git show origin/scaleup-31fires:<path>` from
the repository root:

- docs/ANALYSIS_PLAN.md (docs/scaleup/ANALYSIS_PLAN.md on the branch): frozen plan and amendments 1-14.
  Amendments 9-11 are the diagnosis (G1, G2, 11.4). Amendments 13-14 are the method search and its stopping rule.
- docs/SESSION_HANDOFF_20261116.md: current state and the open question "the method".
- docs/ANALYSIS_REGISTER.md, docs/codex_20261116_round1.md and round2.md: your two earlier reviews.
- docs/panel_build.py, event_export.py, rstar_precheck.py, tma_cell.py, protocol_dev.py: what data exist
  (cell-year panel 2001-2026 with ndvi, evi, lst_day, lst_night, elevation, slope, natural share, burn history;
  per-site buffered grids with the earliest MCD64A1 burn day per calendar year; event extraction by 8-connectivity
  and burn dates at most 7 days apart).

The copies are at:
<review folder>/docs/

Established facts (from the plan, not to be re-derived):
- Diagnosis: within one fire, a geographic null model (distance to the nearest burned training cell) beats the
  random forest (AUC about 0.96); within-event evaluation (pooled AUC, cAUC, sAUC_c) selects location-using models;
  that choice loses 0.07-0.12 AUC on later burning; replicated on unseen 2024-2026 labels.
- Four method attempts failed: sAUC (synthetic rule not met), forward selection (2 supported sites), TMA (BLUP
  spatial residual, equal to its baseline), TMA-cell (-0.003 against density), R* pre-check (+0.008).
- The reference R1 (Gaussian kernel density of past burns, h = 2 km, no decay) leads: 0.651-0.659 out-of-group
  transition AUC (task G-A), 0.675 on later burning (G-B). Environmental pooled forests reach 0.57-0.58.
- The stopping rule of 14.2 ended the method search. One exception was agreed (item 6 of the handoff: one R1-offset
  comparator). The blind sites (2005-2016 focal fires) have not been opened.

## The proposal: reach-conditional susceptibility

Claimed root cause. All four attempts assumed risk is a per-cell score plus a spatial correction. Fire spreads by
contagion and none of the models contains contagion.

Idea. Treat a scar as a site-percolation cluster. Let q_i be the probability that cell i burns given that fire
reaches a neighbour. Then P(scar C) = prod_{i in C} q_i * prod_{j in outer boundary of C} (1 - q_j). Cells beyond
the outer boundary do not appear in the likelihood: the fire never reached them, so they are censored, not
negatives. Conventional susceptibility models count them as negatives, which makes distance to the scar the
strongest discriminator. This is offered as the explanation of the diagnosis.

Method, two parts.
1. Learning. q is learned from the contrast "burned cell vs outer-boundary cell" over all events since 2001 at the
   31 sites (the buffered burn-date layers), events weighted equally, using only events before the prediction date
   and from other geographic groups. Predictors: panel variables (NDVI, EVI, LST day/night, elevation, slope,
   natural-cover share, time since last burn), taken at the 1 May cut-off before the event. Event-level effects
   (weather, wind) cancel in the within-event contrast.
2. Propagation. The Gaussian kernel of R1 is the solution of the heat equation with constant conductivity. Make
   the conductivity depend on q: past burns diffuse on the grid graph (all cells, including non-natural ones) with
   edge conductance exp(beta * z), z = logit q standardised within the site-year. Score S = log u + gamma * z,
   u = diffused density. beta = gamma = 0 gives exactly R1, so the reference is nested in the method. beta and
   gamma are chosen on out-of-group transitions of earlier years, as the TMA gate was.

Claimed tests that the diagnosis is solved:
- T1: on the reach-conditional contrast, the geographic null and coordinate models fall to AUC about 0.5, while
  the environmental model stays above 0.5 on unseen events.
- T2: a model trained with this objective transfers to other sites better than the same model class trained on
  cell labels.
- T3: the diffused map beats R1 on later burning (G-A, G-B, G-C).
- T4: a simulation with percolation fires on the real landscapes and known q reproduces the diagnosis and the
  method recovers q.

Plan.
0. Pre-checks (hours): literature scan for an exact precedent; counts of events of 100 ha or more and of boundary
   cells per site; out-of-group AUC of the contrast (stop if the mean is below 0.55 or the cluster-bootstrap lower
   bound does not exceed 0.5); beta = 0 must reproduce R1 within 0.002.
1. Write the already agreed 14.10 fixes and an amendment 15 that records this as a fifth attempt chosen after the
   development results.
2. G-A development with a fixed (beta, gamma) grid and ablations (beta only; gamma only; q trained on cell labels,
   which is the R1-offset comparator of item 6; q = natural share only). Threshold unchanged: at least 0.01 over R1.
3. Percolation simulation; reach-conditional rerun of G1/G2 on the 31 focal fires.
4. Freeze, then the blind test on the unopened 2005-2016 sites.

Stated risks: probability of beating R1 by 0.01 judged below one half; MCD64A1 edge labels at 500 m are noisy
(claim 3 of the plan); most fires stop because of weather change or suppression; known precedents for parts
(perimeter vs interior matched case-control: Holsinger et al. 2016, O'Connor et al. 2017, Macauley et al. 2022;
neighbourhood connectivity index, IJWF WF23055; lattice diffusion kernel density with barriers, Barry and
McIntyre 2011). The claimed new parts are the censoring explanation of the diagnosis, the reach-conditional
objective for scar-based susceptibility, and the diffusion that nests R1.

## What I want from you

1. Is the percolation/censoring argument correct? Check the likelihood (site vs bond percolation, multiple
   exposures, unburned islands, events cut by the rectangle, daily burn-date resolution against fast fires, events
   merged or split by the 7-day rule). Does it really explain a null AUC of 0.96 and the selection of
   location-using models, or is there a simpler explanation the proposal ignores?
2. Is T1 circular or trivially true by construction? If negatives are a one-cell ring around positives, what does
   a low null AUC prove? What would a non-trivial version of the test look like?
3. Does "beta = gamma = 0 gives exactly R1" hold on a degree grid with 8 neighbours, finite boundaries and the
   buffer? Is exp(beta * z) conductance with a symmetric Laplacian the right operator, or does it do something
   unintended (mass trapped at sources in low-q areas, edge effects, scale of z)? Suggest a better operator if
   there is one.
4. Leakage and chronology: any path by which the target year's burning, post-fire NDVI/LST, land-cover maps
   published after the cut-off, or the evaluated geographic group can enter q, z, u, beta or gamma.
5. Chance of success. Given the numbers in the plan (R1 0.65-0.70; pooled environmental forests 0.57-0.58;
   pooled forest + density rank 0.604; TMA-cell about equal to R1), is there any reason to expect this to gain
   0.01? Where would the gain come from, and which cheap check would tell us fastest?
6. Novelty for EMS, 1-5, with the closest precedents you can verify (search if you have web access; say which
   citations you verified and which you did not). Is there prior work that already does reach-conditional or
   boundary-negative training for susceptibility, or learned-conductance diffusion of fire history?
7. Forking paths: this is a fifth attempt after a declared stopping rule. Can it be made legitimate, and how
   should it be recorded? Does it invalidate the blind test?
8. Are the kill criteria of step 0 well chosen (0.55, lower bound above 0.5, 0.002)? Propose better ones.
9. Is there a clearly better direction than this one for "a novel method that resolves the diagnosis"? One
   paragraph, concrete.

Output: a verdict (go / go with changes / no-go) in the first line, then numbered answers to 1-9, then a ranked
list of the minimum changes to the plan. Be specific; cite file names and amendment numbers where you rely on
them. Mark anything you could not verify.
