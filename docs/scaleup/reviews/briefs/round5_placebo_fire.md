# Independent review request 3: placebo-fire calibration

You are an independent, sceptical reviewer. Read-only: do not modify any file. The author wants a method with
novelty of about 4 of 5 for Environmental Modelling & Software and has rejected the two earlier proposals as too
low. Judge this third one on its merits. Say plainly if it is not new, not sound or unlikely to work.

## Context

Same project and folder as your two reviews today:
<review folder>/
(docs/, brief.md + codex_reply.md, brief2.md + codex_reply2.md). Your corrections in reply 2 are accepted: no
"one scar tells us nothing", no 90% claim, MDD is not a tie rule, practical comparators.

Result files copied from origin/scaleup-31fires (python3 with pandas available), in
<scratch folder>/ :
- c9.csv  = results/scaleup/claim9/claim9_synthetic_runs.csv (plan 6.2: 31 real landscapes x 32 scenarios; label
  from eta = a*E + b*S + noise; M_env = forest on real predictors, M_geo = forest on coordinates; columns auc_*,
  cauc_*, saucc_*, truth_* where truth is the AUC on an independent redraw of the spatial field)
- c15.csv = results/scaleup/claim15/claim15_g2_per_fire.csv (18 real fires: focal AUC, cAUC, sAUC_c and 2017-2023
  later-burning AUC of the coordinate forest, coordinate kNN, thermal+coordinates, thermal+distance)
- c14.csv, c16.csv, tr.csv as before.
You can also read the branch with `git show origin/scaleup-31fires:<path>` from the repository root.

## Evidence computed today (please verify)

A. Synthetic runs with no environmental signal (a = 0, b > 0; 186 runs): the environmental forest scores a mean
   within-event AUC of 0.603 (0.693 at b = 4, L = 10 km, the most fire-like setting, where the geographic null
   reaches 0.89) while its true transferable AUC is 0.50. The coordinate forest scores 0.80 (0.92 at b = 4, L = 10).
   The real fires have a geographic-null AUC of 0.96, so the real placebo level is expected to be higher still.
B. Real fires (c15 and c14, 18 fires, later burning to 2023). Error of the focal estimate against later AUC,
   mean signed (mean absolute):
   thermal (environmental): raw +0.23 (0.25), cAUC +0.03 (0.16), sAUC_c -0.01 (0.11)
   thermal+distance:        raw +0.38 (0.38), cAUC +0.07 (0.14), sAUC_c +0.05 (0.11)
   thermal+coordinates:     raw +0.38 (0.38), cAUC +0.17 (0.20), sAUC_c +0.13 (0.15)
   coordinate forest:       raw +0.47 (0.47), cAUC +0.27 (0.30), sAUC_c +0.26 (0.26)
   coordinate kNN:          raw +0.46 (0.46), cAUC +0.26 (0.26), sAUC_c +0.22 (0.22)
   So the existing distance corrections are roughly right for the environmental model and overstate every model
   that uses location, including the practical thermal+coordinates model.
C. Post hoc check on c9 (744 runs with a > 0 and b > 0), using the same fire's a = 0 run with the same (b, L) as
   a single placebo draw. Estimators of the true AUC: for M_env, cAUC bias -0.002 (MAE 0.056), sAUC_c -0.015
   (0.060), ratio estimator 0.5 + 0.5*(AUC - placebo)/(1 - placebo) bias -0.010 (0.059). For M_geo, cAUC +0.059
   (0.101, correlation with truth -0.04), sAUC_c +0.100 (0.124, -0.08), additive estimator 0.5 + (AUC - placebo)
   -0.059 (0.087, correlation +0.44). Selection between M_env and M_geo: mean loss raw AUC 0.058, sAUC_c 0.043,
   cAUC 0.022, placebo difference 0.009, always-environmental 0.006; balanced accuracy raw 0.63, sAUC_c 0.69,
   cAUC 0.76, placebo 0.59. Caveats: one noisy placebo draw; the placebo comes from the true generator; exploratory.

## Third diagnosis

Within-event skill is inflated because the score has no reference with the same geometry. A scar is one contiguous
patch, and the same pipeline also "predicts" a patch that was placed without regard to the environment, from
coordinates trivially and from spatially smooth environmental predictors partly. The existing corrections (cAUC,
sAUC_c) restrict or stratify the test cells by distance; that repairs the estimate for an environmental model but
not for any model that uses location (evidence B). So the defect is the missing geometry-matched null, not the
use of location as such.

## Method: placebo-fire calibration

1. Placebo labels. For each fire, K placebo labels on its own grid: the real scar moved rigidly (translation,
   rotation by multiples of 90 degrees, reflection) to another place in the study rectangle, accepted when the
   burned count in the model population is within 10% of the real one and the overlap with the real scar is at
   most 20%. Sensitivity: scars of the other 30 fires transplanted in the same way. K about 30 to 100.
2. Placebo distribution. The identical pipeline (features, forest settings, block design, fold rule) is refitted
   and scored on every placebo label, for every candidate model. This gives the placebo distribution of the
   within-event metric for that model, landscape and geometry.
3. Outputs per model and fire: geometry share (mean placebo AUC - 0.5) / (observed AUC - 0.5); a Monte Carlo
   p value at event level; and a calibrated estimate of transferable AUC,
   A_hat = 0.5 + 0.5 * (AUC_obs - mean placebo) / (1 - mean placebo) (primary form to be fixed on simulations
   before any real later-burning comparison; the additive form is the alternative).
4. Spike-in check. Placebo labels with a known injected association (placements drawn with probability tilted by
   a chosen environmental index, and the existing generator of plan 6.2 with more draws) give the map from the
   observed metric to the true transferable AUC, so the estimator's bias is measured where the truth is known.
5. Same device for later burning. Relocating the later events gives, for one site, the null distribution of a
   later-burning AUC (mean 0.5, spread set by the number and size of events), hence an event-level p value and
   interval without relying on many sites. Its predicted spread is compared with the observed year-to-year SD
   (0.13 to 0.15).
6. Validation on real data. Development: the 18 sites with later burning; forecast error of A_hat against the
   later AUC for the practical candidate set (thermal, baseline, thermal+distance, thermal+coordinates), with the
   coordinate-only models as diagnostics, compared with raw AUC, cAUC and sAUC_c. Blind: the unopened 2005-2016
   sites, where focal labels are open and later labels closed. Forecasts are frozen with a manifest, then the
   later labels are opened once.
   Primary blind hypothesis: over the practical candidate set, the mean absolute forecast error of A_hat is lower
   than that of cAUC, paired over sites, two-sided 95% interval excluding zero. Secondary: against sAUC_c; signed
   bias per model class; selection loss against raw-AUC, cAUC, always-environmental and always-R1 rules.

Claimed properties: (i) a model that uses only location gets the same expected score on real and placebo labels,
so its calibrated estimate is 0.5 by construction, and adding a pure location feature cannot raise the calibrated
estimate in expectation; (ii) the calibration is applied to the whole pipeline, so it holds for any model class
and any cross-validation design; (iii) unlike the Beale et al. (2008) debate in species distribution modelling,
the estimate is checked against real later outcomes.

Known precedents the proposal admits: Hijmans (2012) null geographic model and cAUC; Beale, Lennon and Gimona
(2008, PNAS) null distributions preserving spatial autocorrelation, and the replies that such nulls carry climate
signal; Raes and ter Steege (2007); spin tests and BrainSMASH surrogates in neuroimaging; spatial-noise placebo
tests in econometrics (Kelly 2019, not verified today); fire selectivity studies with randomly placed fires (not
verified). A web search today found no placebo or relocated-scar null in wildfire or landslide susceptibility
evaluation; that search was short.

Stated risks: the study rectangles were built around the focal fire, so the real scar is central and placebo scars
are not; relocation may be too conservative (it removes real association carried by the scar's own shape); the
estimator form is chosen on simulations; later-burning AUC has a noise floor (year-to-year SD 0.13) that puts a
floor near 0.10 on any forecast's absolute error; the method evaluates maps and does not make a better map than
R1; cost of about 30 x 5 folds x 31 fires x 5 models forest fits.

## What I want from you

1. Verify evidence A, B and C from the csv files. Flag misreadings.
2. Is the third diagnosis sound, and does evidence B really show a gap that existing corrections leave open? Or is
   the overstatement for location-using models simply what cAUC and sAUC_c are known not to address?
3. Is claimed property (i) correct? Under which placement distribution is it exact, and how do the centred
   rectangle, the acceptance rules, block cross-validation and finite K break it?
4. Is the calibrated estimator meaningful? Additive against ratio against something better (for example mapping
   through the placebo distribution's quantiles, or a spike-in curve). What does A_hat estimate when the real
   association is carried by the scar's shape and position together?
5. Does the Beale et al. criticism (null patterns placed on an autocorrelated environment carry "signal") sink
   this, or does validation against later burning answer it?
6. Probability that the primary blind hypothesis succeeds, and what the most likely failure is. Give a number.
7. Novelty for EMS, 1 to 5, with verified precedents. Search specifically for relocated-scar, random-fire or
   pattern-preserving nulls in fire selectivity, susceptibility or landslide studies, and for permutation or
   surrogate-label calibration of cross-validated AUC under spatial autocorrelation. Say what you verified.
8. What single change would raise the novelty or the chance of success the most?
9. Compared with your recommended paper in reply 2 (empirical evaluation, headline "high within-event
   discrimination does not establish skill on later burning"), is this a better paper, an add-on, or a distraction?

Output: verdict first line (go / go with changes / no-go), numbered answers 1-9, ranked minimum changes.
