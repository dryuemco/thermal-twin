# Referee round 2 — consolidated dossier

**Date:** 2026-08-14. **Panel:** four independent readers, each given the manuscript files and the
frozen evidence base, none shown the others' reports.

| | Lens | Verdict |
|---|---|---|
| R1 | Statistics and inference | major revision |
| R2 | Remote sensing, fire ecology, data provenance | major revision |
| R3 | Claim–evidence alignment | major revision |
| R4 | Handling editor: novelty, structure, reproducibility | major revision, **not submittable today** |

Unanimous. No referee proposed rejection; none proposed minor revision. Every one of them
volunteered a substantial "things done well" list, and the three that audited numbers against the
frozen files reported that the numeric traceability is, with the exceptions listed below,
exact.

**Verified by YEC before this dossier was written** (marked ✅ in place): the Table 4
counterexamples, the label-free taxonomy error, the per-region pre-label exclusion flags, the
Manavgat MODIS input semantics, and the Landsat compositing A/B numbers. Everything else is the
referee's claim as filed, with its source path given so it can be checked the same way.

---

## Tier 0 — statements in the manuscript that are wrong

These are not matters of emphasis. Each is a sentence the paper's own evidence contradicts.

**0.1 ✅ "Adaptation degrades every direction that already transferred" is false across the
20-direction matrix.** `04_results.md:227`, repeated at `01_introduction.md:228` and
`05_discussion.md:30`. Table 4 at `04_results.md:126-133` contains five above-chance directions that
adaptation *improves*: Montiferru→Manavgat 0.567→0.606 (CORAL), Manavgat→Montiferru 0.533→0.592,
Montiferru→Bejís 0.548→0.574, Muğla→Montiferru 0.531→0.587, Montiferru→Evia 0.586→0.630. All five
involve Montiferru, the region excluded from the Table 5 decomposition. The claim is true inside the
12-direction four-AOI set and false as a general statement. This is the headline characterisation of
Contribution 2, so it matters. The honest form is nearly as strong: *within the twelve decomposed
directions, all six that already transferred were degraded; across the full matrix the effect is
compression, with the Montiferru directions the exception.* Also re-scope `figure_captions.tex:133`.

**0.2 ✅ The label-free taxonomy is wrong, and correcting it strengthens the paper.**
`04_results.md:322` says the conditional indices are not label-free "unlike every P(x), P(x|y=1) and
P(y) row"; `05_discussion.md:161` says of the failing families "All are computable without target
labels". But `03_methods.md:682-684` defines burned-niche overlap on `burned = 1` cells of the
primary population in **both** regions, and `03_methods.md:712-713` defines regime structure on
connected components of burned cells. Both consume the target's burned map exactly as the conditional
index does. Only the marginal P(x) family is genuinely target-label-free. Restate as
target-label-free (marginal) versus target-label-requiring (P(x|y=1), P(y), P(y|x)). The
niche-versus-conditional contrast then becomes *cleaner*: two families consume the same information
and only one orders transfer. The cost is that the abstract's operational asymmetry at
`00_abstract.md:60-61` has to be softened, and that the only family a practitioner can run before
deployment is the one reduced to six rows on twelve directions. Say that.

**0.3 ✅ The pre-label burn exclusion ran in three of five regions, and §3.16.4 says otherwise.**
`03_methods.md:831-833` asserts "The same leakage-safe pre-label exclusion applies as in every other
region". From `drive_new/experiments/<region>/step8a/step8a_dataset_stats.json`: Manavgat
`exclude_pre_label_burns: false`, 0 cells excluded; **Bejís has no such field at all**; Muğla true /
49; Evia true / 16; Montiferru true / 61. §3.2:106 is correctly hedged ("Optionally"), so the false
statement is the parity claim in §3.16.4, not §3.2. Fix the parity claim, add a per-region line, and
either re-run the exclusion for Manavgat and Bejís or bound the exposure by counting MCD64A1
detections inside each predictor window. R2 adds that the exported label raster is pre-clipped to the
label window in all five regions, so `out_of_window_burndate_cells = 0` is a property of the export
rather than an empirical finding, and that prior-year burning is screened only for the Muğla pair
(`repo/src/historical_burn_exclusion.py` is opt-in, configured at `repo/core/regions.py:576-577`).

**0.4 The LORO ceiling gap is 0.28 to 0.50, not 0.22 to 0.50.** `04_results.md:468`,
`05_discussion.md:284`. From `loro_pooled_transfer.csv`: Evia 0.275, Montiferru 0.282, Muğla 0.307,
Manavgat 0.401, Bejís 0.501. The source file `loro_pooled_transfer.md:11,44` carries the same error
and needs the same fix.

**0.5 A figure caption names the wrong direction.** `figure_captions.tex:120` gives "CORAL
Bejís→Montiferru is 0.4991 (hatched, below chance)". Table 4 gives Bejís→Montiferru CORAL = 0.574;
the 0.499 cell is Bejís→**Evia**. The caption's worked example is its own explanation of the hatching
convention.

**0.6 The burned-area product is Collection 6.1, not Collection 6.** `03_methods.md:65`, `:591`,
`02_related_work.md:126`. `repo/core/config.py:207` sets `MODIS/061/MCD64A1`. Giglio et al. (2018)
and Boschetti et al. (2019) describe C6.

**0.7 §2.5 still claims pre-specification.** `02_related_work.md:340`: "we address it by
pre-specifying the protocol". §3.14.1:641-646 explicitly declines this ("not a formal
pre-registration... No independent timestamped public registration exists") and §5.6 was already
corrected to match. Related work was missed. A hostile referee will quote this phrase.

**0.8 §3.13 and §3.11 disagree on the λ sweep.** `03_methods.md:527` says "four CORAL regularisation
values"; `03_methods.md:432` says nine, listing them. The "four" is a survival from the superseded
two-region sweep.

**0.9 The retired comparative survives in half-form.** `01_introduction.md:67`, `:219`,
`02_related_work.md:413` all still open with "the block that gains/buys the most locally".
`POSITIONING.md:63-72` retired that comparative because no other block's portability was measured on
the same footing; the superlative's *first* half is untested for the same reason as its second. No
block-versus-block within-region comparison exists in §4. Suggested repair: "the dynamic thermal
block, which buys +0.056 to +0.153 within every region, contributes +0.004 on average between them,
and its contribution is sign-unstable."

**0.10 Four claim-bearing sentences lost their finite verb in the style pass.**
`02_related_work.md:287` (the method-dependence self-criticism), `02_related_work.md:404-405` (the
regime-typology hedge), `03_methods.md:742-743` (the justification for which two features were
dropped, including the "bootstrap-supported" qualifier that §4.6b leans on), `04_results.md:271-272`
(the opening sentence of §4.4). Separately `02_related_work.md:418-419` inverted an *exclusion* into
a three-item list when its em dashes were removed, and that sentence is the one guarding the novelty
claim against Marino and Gelabert. `check_splits.mjs` currently reads only `03_methods`; run a
verb-presence check across all eight body files before submission. R3 lists a further nine mechanical
split artefacts (run-ons at `02:386`, `03:511`; a literal "label- blind" at `02:390`; a duplicated
pronoun at `02:456`; an ASTER GDEM misattribution at `02:315`; a Dimarco predictor-composition change
at `02:318`; an added causal connective at `02:368`; a self-contradictory commit sentence at
`03:974`; a design statement swallowed into list item 4 at `03:225`).

**0.11 `figure_captions.tex` carries 17 em dashes** against `STYLE.md:3-4`, which names that file in
scope. `check_style.mjs` reads only `.md` and reported "0 dashes". Same class of failure as the
`paper/tex` checkers that pass on zero files.

---

## Tier 1 — statistical claims that must be restated (R1)

**1.1 The paper's headline quantity carries no interval anywhere.** "+0.004 over twenty ordered
directions" appears at `00_abstract.md:47`, `01_introduction.md:212`, `04_results.md:188`,
`05_discussion.md:40`, `06_conclusions.md:36`. Every other quantity in the manuscript has a bootstrap
interval; this one has none. R1 recomputed from `transfer_ci_blocksize.md:234-253`: mean +0.0042, SD
0.0713, giving [−0.027, +0.035] at a naive n = 20, [−0.034, +0.042] clustered to the ten unordered
pairs, and roughly [−0.084, +0.093] with regions as the unit. The conclusion is unharmed — "adds
nothing on average" is what an interval spanning zero says — but the reporting is not. Report a
cluster-aware interval and the effective sample size, and say in the abstract that it spans zero.

**1.2 ρ = 0.84 is over-sold on three counts.** `04_results.md:281`.
(a) The reported [+0.58, +0.88] is narrower than any interval consistent with the stated 8-pair
bootstrap. Fisher-z at n = 8 gives [+0.33, +0.97]; Bonett–Wright gives [+0.20, +0.98]. The reported
lower bound is almost exactly the bound one gets by treating all 16 directions as independent
(+0.590), which is what the pair bootstrap exists to avoid, and the upper bound sits below every
analytic bound, the signature of a statistic pinned near a combinatorial ceiling. R1 reproduced the
point estimate at 0.8404 against a tie-structure maximum of 0.8609. Your own working file says this
(`conditional_similarity_transfer.md:92`) and the manuscript does not.
(b) **At this design size the diagnostic could not have survived a correction whatever the data.**
The pair-level analogue gives ρ = 0.866 with an exact permutation p of 0.0060 one-sided, and 0.0060
is the *smallest attainable* p under this tie structure. Bonferroni over 19 computed variants needs
p ≤ 0.0026. That is a far stronger and more honest statement than "no family-wise control is
claimed": the design has no headroom, not merely no correction.
(c) The supported-feature selection is computed once, outside the bootstrap
(`conditional_similarity.mjs:104-109`, loop begins at 163). Since that restriction is exactly what
turns a null result (cosine over nine features, ρ = +0.50, interval spanning zero) into the paper's
one positive finding, the interval must either propagate the selection or be labelled as conditional
on a fixed one.

**1.3 The B = 20 robustness rows rest on single-digit resampling units.** R1 counted blocks from the
frozen per-cell prediction tables: at B = 20 the number of blocks carrying at least one burned cell
is 6 (Bejís), 6 (Montiferru), 12 (Manavgat), 15 (Evia), 33 (Muğla). Montiferru additionally feeds 12
groups into a 5-fold `StratifiedGroupKFold`. Equal-tailed percentile intervals have no meaningful
coverage there. The finding survives comfortably at B = 10 (19–70 positive-carrying blocks in all
five regions); it is the B = 20 row that should be labelled indicative. Add block counts and the
invalid-replicate fraction (§3.9 says these are recorded; none is reported) to Table 3, and raise the
replicate count above 1,000 given that your own seed sweep flips verdicts on noise of order 0.001.

**1.4 Direction counts are simultaneous interval decisions.** §3.14.1's multiplicity paragraph scopes
itself to the diagnostic table, but the 12/6/2 and 6/4/10 tallies apply the same rule 40 times and
then count outcomes. For the *level* the qualitative claim survives easily (9 above and 4 below out of
20 is far more than a global null predicts), so this is about precision, not retraction. One sentence
in §3.9 or §3.14.1, and stop quoting exact counts where §4.7g itself gives a range.

**1.5 Percentile intervals without BCa are used in two places they should not be:** the 8–10 unit pair
bootstrap (1.2a is the symptom) and Table 5's recovered fraction, a ratio whose denominator is
estimated and can be small (Evia→Manavgat: denominator 0.184, reported −0.86 [−1.18, −0.60]). The
pairing itself is correct; this is a distributional objection.

**1.6 A label-noise mechanism is untested and the column for it is in hand.** `03_methods.md:99-101`:
a single in-window positive sub-pixel labels a cell burned, and
`burn_date_pixel_agreement_fraction` is recorded and never used. Fringe-cell contamination scales
with perimeter-to-area ratio, which differs enormously across the five regions, and fringe cells
differ systematically in terrain — a plausible competing explanation for a *terrain* sign flip.
Restricting to cells above an agreement threshold and recomputing the signed univariate AUCs would
settle it in an afternoon of read-only work.

**1.7 Two promised sensitivities do not exist.** `03_methods.md:521` promises a fused-LST
gap-fill sensitivity; `03_methods.md:526` promises results from a second random-forest profile.
Neither appears in §4 or §5. Report or delete both promises.

**1.8 Evia's within-region increment is reported only on the extended AOI.** §4.7a runs the
legacy-versus-extended comparison on the transfer arms only. Evia carries the largest within-region
increment in the paper (+0.153, and near-flat as blocks coarsen, unlike every other region) and the
AOI change moved its TSG prevalence from 0.676 to 0.287. Give the legacy-AOI within-region ΔAUC.

---

## Tier 2 — the remote-sensing half is missing (R2)

**2.1 ✅ The within-region increment is compositing-dependent, by about as much as its own CI.**
Three controlled Landsat-compositing chains for Manavgat, identical cohort, folds and baseline,
differing only in the current-period LST raster
(`drive_new/diagnostics/landsat_composite_downstream_ab/manavgat_2021/downstream_ab_summary.md` and
`.../landsat_harmonization_downstream_ab/...`):

| chain | thermal ΔAUC [95% CI] |
|---|---|
| `scene_weighted_reference` (production) | +0.0636 [+0.0520, +0.0749] |
| `date_balanced_lst_only` | +0.0845 [+0.0723, +0.0979] |
| `overlap_harmonized_date_balanced` | +0.0450 [+0.0330, +0.0574] |

Baseline AUC is byte-identical at 0.804362 across all three, so the whole effect sits in the thermal
block. Both paired comparisons have intervals excluding zero. The mechanism is documented too:
`landsat_residual_seam_attribution/manavgat_2021/residual_seam_summary.md` §6 finds bootstrap-supported
excess jumps of 0.850 °C [0.812, 0.890] at boundaries where the number of contributing clear
acquisitions changes, final status `current_support_dominant`. Report this as a first-class
sensitivity axis with the source reports' own caveats (single AOI, candidate not production, no
non-inferiority claim), extend the A/B to Bejís as its own report requires, or state in §5.11 that
the increment carries a compositing tolerance of about ±0.02 audited in one region only.

**2.2 Nothing about the actual observations is in the Methods.** Greps over `00`–`06` and `S1` return
zero hits for QA, cloud, acquisition, path/row, overpass, Landsat 8, MOD11. From the code:
`LANDSAT/LC08/C02/T1_L2` only, no Landsat 9 even for Bejís 2022; `apply_qa_mask`
(`repo/src/step3_landsat_lst.py:67-98`) masks fill/dilated cloud/cirrus/cloud/shadow/snow and
preserves the water bit; `STEP5_MIN_CURRENT_VALID_COUNT = 2`, so a 57-day median composite may rest
on two clear observations; `ST_QA` is never selected. Manavgat's inventory gives 7 dates / 14 scenes
from two alternating paths, so a pixel's median rests on 3–4 dates outside the path overlap and 7
inside it — which is the mechanism behind 2.1 and is region-specific by construction. The MODIS LST
product (`MODIS/061/MOD11A1`, Terra only, daytime) is never named. Add a §3.4 subsection and a
supplementary table: sensor, collection, QA bits, per-region distinct acquisition dates and scenes,
path/row coverage, per-pixel valid-observation distribution. R2 also notes an upstream provenance
error worth fixing: the config text claims QA_RADSAT is applied and the mask does not apply it.

**2.3 ✅ Manavgat's downscaled and fused LST were built from a different MODIS input than the other
four regions.** `drive_new/experiments/manavgat_2021/step7c/downscaling_model_metadata.json`:
"`modis_lst_mean_celsius` is a 4-year summer-mean MODIS context layer, not a current daily MODIS
observation." Bejís records the opposite: "single-season MODIS predictor-window summary layers for
2022-06-15 -> 2022-08-14; they are not multi-year baselines". So two of the six thermal channels are
functions of a multi-year climatology in the anchor region and of an event-specific composite
everywhere else. Manavgat is the elevation dissenter, the contrast pair's reversal partner, and the
region §5.11(ix) concedes is unexplained. A first-order candidate explanation is sitting in the
pipeline's own metadata. The same run also carries `modis_nodata_issue_resolved: False`, encoding sea
cells as exact 0.0 in a coastal AOI.

**2.4 The six thermal predictors are close to one predictor, and Step 8D already measured it.**
`fused_lst` equals `current_lst` wherever Landsat is valid (gap-filled fractions 0.11 % to 9.70 %),
and Table R8 already shows the consequence (0.325 vs 0.325; 0.515 vs 0.519). `downscaled_lst` is an
RF surface whose dominant input is region-dependent — MODIS mean in Manavgat and Evia, NDVI in Bejís
and Montiferru, **slope 0.777 in Muğla**, where it is largely a re-expressed copy of a baseline
predictor. And `drive_new/experiments/<region>/step8d/step8d_ablation_delta_auc_by_population.csv`
gives the ablation directly on the primary population: `tvdi_group` alone recovers 96 % of the full
block in Manavgat, 99 % in Montiferru; `lst_anomaly_group` 81 % in Evia; `tvdi_group` 77 % in Muğla.
Step 8D exists, is frozen, is never cited in the manuscript, and converts "the thermal block" from an
opaque bundle into a statement about which physical quantity carries the increment. It also bears on
transfer: a block of near-duplicates is not six independent tests of concept shift.

**2.5 TVDI's construction is a competing mechanism for the reversals, and it is not addressed.**
Edges are the 2nd and 98th LST percentiles within 20 NDVI bins of the scene
(`03_methods.md:172-178`), so TVDI = 0.5 denotes a different physical state in every AOI and window.
Between AOIs of different size and relief (Montiferru 0.30° × 0.22° versus Muğla 1.80° × 0.85°) the
percentile edges sample different populations, and a sign reversal in `current_tvdi_mean` is what the
index does by construction. §5.2:76-79 currently generalises to "Statistical self-normalisation does
not guarantee a stable direction of association". Retire the general claim, name the specific
scene-dependent-edge mechanism, and either recompute TVDI on pooled edges or report the fitted edges
per region so a reader can see how far apart the normalisations are.

**2.6 Coordinates re-enter through `downscaled_lst_mean` and `fused_lst_mean`.** The Step 7C
downscaler is trained on `lon, lat, row, col, row_norm, col_norm` among others, with summed
coordinate importance 0.123 (Manavgat), 0.122 (Bejís), 0.101 (Evia), 0.066 (Montiferru), 0.035
(Muğla). The downscaler never sees a fire label, so this is not leakage in the strict sense — but
§3.13's leakage argument is emphatic that coordinates are excluded, and a coordinate-derived
component enters the feature set anyway. State it, quantify it, and show the increment without those
two channels (Step 8D has the pieces).

**2.7 The downscaling validation exists and is not in the paper.** Spatially blocked 64×64
train/validation/test splits, test RMSE 2.04 °C / R² 0.866 (Manavgat), 1.75 / 0.795 (Bejís), 1.65 /
0.956 (Muğla), 1.80 / 0.866 (Evia), 1.83 / 0.909 (Montiferru), each against a MODIS-baseline control.
A referee cannot assess an unvalidated downscaling step; here it is validated and the reader is not
told. Four sentences in §3.4 plus a supplementary table.

**2.8 The window-closure result has a mechanism the paper declines to give.** §5.8:392-395 says "We
do not know why the increment increases and we do not speculate". The window-closure report itself
says the closure date interacts with the fixed production policy, changing which dates enter the
median and how many observations back each pixel; in that same report the baseline moves by
+0.002–0.003 while the thermal family moves by +0.022 ROC-AUC. Naming this does not damage the
pre-fire claim (contamination would push the other way, and the authors are right about that). It
does mean part of the increment is a function of composite construction.

**2.9 Label provenance is under-specified for a burned-area paper.** §5.11(iii) disposes of it in one
sentence. MCD64A1 omission at 500 m in fragmented Mediterranean terrain is large and *spatially
structured*, correlating with patch size, terrain and fragmentation — which are the paper's baseline
predictors. Two regions with different patch-size distributions (Muğla effective component count
4.05 versus Bejís ~1.0) could therefore show different feature–label associations with no change in
fire ecology. `FIRECCI51_COLLECTION` is configured in the repo at 250 m and never used; one region as
a label-source sensitivity, or a stated reason for not doing it.

**2.10 Missing literature.** On the method side, the live dispute about blocked CV (Wadoux et al.
2021; Milà et al. 2022; de Bruin et al. 2022) is absent while `02_related_work.md:174` presents
blocked CV as "the accepted correction" — directly on point for a paper whose headline turns on how
blocking scale changes verdicts. On the remote-sensing side: burned-area validation beyond Boschetti
(Padilla et al. 2015; Roteta et al. 2019; Franquesa et al. 2020/2022), the Ts–VI feature-space
limitation literature for TVDI (Petropoulos et al. 2009; Long et al. 2012), LST validation (Wan 2014;
Ermida et al. 2020), and Jain et al. 2020 as the standard ML-in-wildfire review. R2 records that the
AoA implementation is faithful to Meyer and Pebesma (`repo/src/marginal_aoa_completion.py:34-46`) and
that the §2.3 critique is aimed at the real construction, but notes the module's own warning that the
weights come from a source-label-fitted RF and so "MUST NOT be described as label-blind" — which
§3.14.2 does not say.

---

## Tier 3 — editorial (R4)

**3.1 Length is a desk-return risk.** Main-text prose measures ~31,100 words (Abstract 252,
Introduction 2,584, Related work 5,085, Methods 10,294, Results 6,463, Discussion 5,965, Conclusions
462) against a journal norm of 9,000–11,000, plus 184 table rows and ~1,800 words of captions. R4's
cut plan: Related work → 1,800 (delete the contributions restatement at `02:408-460`, which
duplicates `01:203-276` almost verbatim); Methods → 2,600 with a Supplementary Methods S2 taking
§3.11, §3.13 detail, §3.14's framework, §3.16 and §3.17; Results → 2,600; Discussion → 3,000 *but
grow §5.10 from 230 to ~550 words*; Introduction → 1,400 by converting the five contributions from
~1,100 words of prose to five numbered sentences.

**3.2 Nineteen main-text tables → six.** Keep Tables 1, 3, 4, 5, 6 and one merged data summary; move
R1–R13 to supplementary. They are already annotated "final numbering at assembly", which reads as
though they were never meant to be main-text tables.

**3.3 Eight figures → six.** Keep 1, 3, 4, 5, 8 plus a new recovery curve. Caveat: if the C1 fix
below re-anchors the trade-off on feature removal, Fig. 7 stays and Fig. 6 goes instead.

**3.4 C1's thesis and its evidence are misaligned.** "Gains +0.056 to +0.153 within, contributes
+0.004 between, sign-unstable" describes a gain that *fails to travel*, not a gain that is *paid
for*. A trade-off needs a debit, and the only measured debit in the paper is Fig. 7 / Table R4:
removing the reversing features buys +0.014 mean transfer for −0.081 mean within-region, a 6:1
exchange. Either re-anchor the trade-off claim on that exchange explicitly, or restate the thesis as
non-portability rather than as a trade. Fixable in one paragraph, and it is the objection most likely
to cost a referee.

**3.5 Promote S1 to the main text.** `POSITIONING.md:161` already called the few-shot curve "what
turns C2 from a negative finding into an actionable one" and "a strong candidate for the paper's
final figure". Instead §5.5 currently ends "No number from it is used in this Discussion", §5.10
Implications is 230 words and the Conclusions explicitly decline to name a label budget — while S1
shows 32 labelled 5 km blocks recovering 85–89 % of the target ceiling in four of six directions from
starting points at or below chance. This is the single highest-leverage change available: it turns
the paper from "here is what does not work" into "here is what does not work, why, and what it costs
to fix". Keep the seven stated limits, especially limit 4.

**3.6 Recommended title** (R4, replacing the current `tex/manuscript.tex:38`, whose "miss conditional
failures" asserts more than §5.4 concedes): *Local skill, unstable portability: marginal diagnostics
do not order the cross-region transfer of pre-fire thermal dryness in Mediterranean wildfire
regions.* "Do not order" is exactly §4.4's finding and exactly what §5.4 defends. Candidate 1's "do
not transfer between them" is contradicted by the paper's own matrix; candidate 2's "transferability
cost" asserts the debit C1 does not measure.

**3.7 Recommended abstract closing:** *Transfer skill therefore has to be measured rather than
inferred from similarity, and what carries the information is conditional, so the cost of this
failure is labelled effort in the target region rather than better unsupervised alignment.* (+24
words; drop the two niche-overlap sentences, which duplicate highlight 3, if the limit is 250.)

**3.8 Submission blockers.**

| | Item | Status |
|---|---|---|
| 1 | Reproduction-check code absent from `48b56e7`. `git ls-tree -r --name-only HEAD \| grep -i reproduction` returns only `step5_preprocess_timeseries.py`, a substring false match | BLOCKING |
| 2 | Few-shot commit `19d825b` unreachable; `git cat-file -t` fails in a 92-commit clone. `src/few_shot_recovery.py` *is* at `48b56e7`, so a one-line equivalence statement closes it | BLOCKING |
| 3 | Length: ~31,100 words | BLOCKING |
| 4 | Nineteen main-text tables | BLOCKING |
| 5 | Table 2 does not exist; `manuscript.tex:355` emits its reference as literal prose | BLOCKING |
| 6 | Front matter: `[AFFILIATION]`, `[KEYWORDS]`, no corresponding author, no ORCIDs, no competing-interest / CRediT / funding / data-availability declarations | BLOCKING |
| 7 | Never compiled. 36 tabulars, 8 `\includegraphics`, elsarticle + longtable + lineno. Also a bare `---` after `\section{Introduction}` that LaTeX will set as an em dash, against the paper's own style rule | BLOCKING |
| 8 | C1 thesis/evidence misalignment (3.4) | BLOCKING |
| 9 | S1 promotion (3.5) | NEAR-BLOCKING |
| 10 | Abstract word limit unverified (Elsevier and ScienceDirect both 403 to automated fetching) | COSMETIC |
| 11 | Supplementary figure S1 not built — becomes BLOCKING if 3.5 is adopted | COSMETIC |
| 12 | WildfireGenome still preprint-only; recheck at proof | COSMETIC |

**3.9 Reproducibility verdict.** `01_introduction.md:273-276` claims the release exists "so that a
negative transfer result can then be checked rather than taken on trust", and §3.13 names the
repository authoritative. At the pinned commit that claim is false for two artefacts the paper leans
on hardest. A third is misattributed rather than missing: `a07ea33` *is* reachable — it is the parent
of `48b56e7` — and contains no ERA5-Land diagnostic at all, which confirms the paper's own reading
that the production run executed an uncommitted working tree. The repository additionally carries **no
tags**, so the "commit corresponding to the version of record" is a moving branch head; no DOI, no
Zenodo deposit. Either close items 1 and 2 and mint a DOI against a tagged commit (the mail is
already drafted at `paper/emrehan_mail_5.md`, unsent), or rewrite the availability statement to say
plainly what is missing and delete the "checked rather than taken on trust" sentence, because with
those disclosures standing it is not a claim the paper is entitled to make.

---

## Where the referees disagree

**The Muğla two-event control.** R1 calls it "the strongest single piece of evidence in the paper"
and R4 keeps it in the main text as the best answer to the different-places objection. R2 wants it
downgraded: the 2022 predictor window is 2022-04-24 → 2022-06-20 against 2021's 2021-06-01 →
2021-07-28, a late-spring composite against a high-summer one. In late spring, high ground in the
western Taurus is still cool, moist and effectively unburnable; by late July it is not. The elevation
reversal (0.611 [0.532, 0.690] versus 0.296 [0.230, 0.355]) and the sign change in all four absolute
LST channels are what a seasonal-phase contrast predicts, and the baseline climatology shifts with the
window too, so `lst_anomaly_mean` and `tvdi_difference_mean` are referenced to different seasons in
the two arms. The manuscript states the confound honestly in §3.16.4 and §5.2 and then uses the
result to license a strong general reading at `05_discussion.md:111-113`. **This is the panel's one
substantive disagreement and it needs a decision.** If the registry's superseded `mugla_2022`
calendar-shift record permits a calendar-matched arm, running it would settle the question and
convert the paper's boldest control into its safest. If it does not, the abstract's load-bearing
sentence at `00_abstract.md:51-53` has to be hedged where it stands.

**Hedging level.** R3 counts nine passages restating the interval-count fragility (§4.3 twice, §4.5,
§4.7g three times, §5.1, §5.2, §5.11(x), §1.5, §6) while the abstract's transfer paragraph has been
softened to "positive in some directions and negative in others", which conveys no magnitude. R3
would cut three of the nine and put the blocking-invariant result in the abstract: paired deltas span
−0.148 to +0.132, twelve positive and eight negative, at both blocking scales. R4 wants the abstract
*more* assertive in its closing sentence. Both point the same way: spend the words on the result, not
on the caveat, and keep the caveats in §4 and §5 where they belong.

---

## What all four told you to leave alone

- Signed AUCs are never folded to max(AUC, 1−AUC), and below-chance transfer is read as inversion
  rather than absence of signal. R1: the single most common error in the transfer literature, avoided
  deliberately and explained.
- The bootstrap is genuinely paired and genuinely blocked, with the difference formed inside each
  replicate on one shared resampled block set.
- §4.7g and `transfer_ci_blocksize.md`: recomputing both blockings from frozen predictions,
  validating to 1.1e-16, running a seed sweep, leading with the conservative count, and disclosing
  that the published split turns on a bound of −0.00045. Two referees called this exemplary; one
  called it "model referee-proofing".
- The self-reported corrections that weakened your own claims — cell to block resampling, 2-cell to
  10-cell for the reversal diagnostic.
- The Kozan negative control as a real gate calibration (0.017 versus 0.723–0.991).
- The natural-vegetation population choice, which removes the stubble-burning confound that would
  otherwise dominate a MODIS burned-area analysis in these provinces.
- The Methods-to-code correspondence: R2 spot-checked the RF configuration, the feature contract, the
  17×17 reconstruction and the label assignment against `repo/` and every one matched, including the
  tie-breaking rule and the conservative direction it implies.
- §5.4 conceding the diagnostic is undefined on Bejís–Montiferru, half of the paper's own headline
  counterexample, and calling it "a real gap rather than a technicality".
- §5.2 stating outright that the sharpest supported reversal belongs to a static predictor, against
  the paper's own emphasis.
- §5.9's fourth bounding difference, added voluntarily, which weakens the cleanest narrative.
- §3.14.1 refusing to call an internal analysis log a pre-registration.
- The reproduction record itself, and the independent execution of the Muğla pair.
- S1's honesty about its own limits, especially limit 4.
- Numeric traceability: three referees checked Tables 4, R6, R3, R8, 6, the partial correlations, the
  contrast-pair signed AUCs and the two-event gaps against the frozen files and found them exact,
  with the exceptions in Tier 0.

---

## Suggested order of work

1. **Tier 0** — all eleven items are text fixes against evidence already in hand. Nothing here needs
   Emrehan, a re-run, or a decision. Do these first; 0.1 and 0.2 change what three sections claim.
2. **Tier 1.1–1.4** — restate the four statistical claims. 1.1 and 1.2 need a small amount of
   computation on frozen numbers, not a model run.
3. **Tier 2.4 and 2.7** — Step 8D and the Step 7C validation metrics are already frozen and unused.
   These are the cheapest large gains in the whole list.
4. **Decide the Muğla question** (disagreement section), because the abstract depends on it.
5. **Tier 3.1–3.5** — the structural rebuild, which should happen after the claims are settled so it
   is done once.
6. **Emrehan round** — `emrehan_mail_5.md` is drafted and unsent; blockers 1 and 2 plus a tag and a
   DOI, and add the questions raised here: the Manavgat Step 7 MODIS contract (2.3), the acquisition
   inventory for the other four regions (2.2), the compositing A/B for Bejís (2.1), and whether a
   calendar-matched Muğla 2022 arm is runnable.
