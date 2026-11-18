**Go with changes — as an empirical evaluation paper. No-go for the absolute “one scar tells us nothing” diagnosis or a new method claimed to succeed with 90% probability.**

1. **Numerical verification: mostly correct, with an important weighting error and incompatible populations.**

   I reproduced the calculations using the three CSVs and inspected the branch’s `claim14_future.py`, `claim16_replication.py`, and future-label exporter. I did not independently reconstruct the raster labels or frozen scores.

   **c14, 18 fires:**

   | Quantity | Verified mean |
   |---|---:|
   | Focal thermal AUC | 0.83555 |
   | Focal coordinate RF AUC | 0.96383 |
   | Thermal cAUC | 0.64075 |
   | Thermal sAUC_c | 0.60707 |
   | Primary later-burning thermal AUC | 0.60888 |
   | Primary later-burning coordinate AUC | 0.49261 |

   The later target runs **after each focal label’s end through December 2023**, rather than a common 2017–2023 interval. It uses mapped cells from the original population, excludes the focal scar, and requires at least 30 later positives and negatives.

   **c16, 18 eligible sites:** all quoted means and paired SEs reproduce.

   | Comparator | AUC | Thermal minus comparator | SE | Difference/SE |
   |---|---:|---:|---:|---:|
   | Thermal | 0.59394 | — | — | — |
   | Baseline | 0.59683 | −0.00288 | 0.01573 | −0.18 |
   | Thermal + coordinates | 0.58126 | 0.01268 | 0.02534 | 0.50 |
   | Thermal + distance | 0.56253 | 0.03141 | 0.01754 | 1.79 |
   | Coordinate RF | 0.52485 | 0.06909 | 0.03472 | 1.99 |
   | Coordinate kNN | 0.52260 | 0.07134 | 0.02904 | 2.46 |

   This target is **January 2024–September 2026**, outside the focal scar, with its own observation-coverage restriction. Burning during 2017–2023 is counted diagnostically; those cells are **not excluded**.

   **Only 13 sites overlap between c14 and eligible c16.** Equal counts do not mean matched populations.

   **Transitions:** the complete-case “all” subset contains 219 site-years, 29 sites, target years 2007–2025. The quoted means reproduce: TMA-cell 0.66419, f-only 0.65504, density 0.65903.

   The important correction is:

   - **Site-year-weighted** TMA-cell minus density: **+0.00516**.
   - **Equal-site-weighted**, first averaging within each site: **+0.00935**.
   - SD of those 29 site means: **0.13073**; SE: **0.02428**.

   Thus +0.005 and SE 0.024 currently describe **different estimators**. Choose one weighting scheme and calculate its uncertainty accordingly.

   The SD summaries are approximately right for the main models, but not every candidate: across-unit SD reaches 0.187; average within-site SD ranges from 0.125 to 0.168. Sites contribute **1–17 years**. On the separate 238-unit TMA-cell/density stopping set, the mean difference is indeed **−0.00318**.

2. **The revised diagnosis identifies a real problem but overcorrects.**

   **Argument 1: partly right.** Environmental models also show a substantial focal-to-later performance gap. However, 0.836 versus 0.594 combines different site sets, target periods, case definitions and supports.

   On the **13 overlapping sites**, the comparison is:

   | Thermal measure | Mean |
   |---|---:|
   | Focal AUC | 0.81748 |
   | Focal cAUC | 0.64040 |
   | Focal sAUC_c | 0.60479 |
   | c16 later AUC | 0.60250 |

   AUC is not mechanically prevalence-dependent, but changed prevalence can accompany changed case composition, horizon and spatial support. Removing focal positives also changes the population being ranked. Consequently, this establishes **poor transport of raw focal AUC to a different prediction task**, not a clean estimate of bias for the same estimand.

   **Argument 2: correct qualification.** Evidence against coordinate-only RF is borderline under ordinary two-sided site-level inference; kNN is stronger. The practical thermal-plus-coordinate difference is imprecise and small. Do not generalize coordinate-only failure to every use of location.

   **Argument 3: correct about location, excessive about “best.”** History density demonstrates that location information can be useful. It does not establish that spatial information becomes useful *because* events are replicated, or that density is universally best. It is the strongest reference in the inspected development comparisons.

   **Argument 4: substantially correct.** These small mean differences do not establish absence of useful gains. But failure to meet a prespecified search threshold remains a legitimate stopping outcome. Statistical uncertainty changes the interpretation, not the recorded outcome.

   The statement **“nothing can be selected or measured inside one event” is wrong**. A single event supports conditional measurements of spatial discrimination. It cannot, without assumptions or external replication, establish expected performance across future events. Cells contain information; they are not independent replications of an event.

   Distance correction deserves a fair hearing. On c14’s own 18 sites:

   | Focal estimate versus later thermal AUC | Mean signed error | Mean absolute error |
   |---|---:|---:|
   | Raw AUC | +0.22667 | 0.25291 |
   | cAUC | +0.03188 | 0.15783 |
   | sAUC_c | −0.00831 | 0.11159 |

   Those are meaningful improvements in agreement. They do **not** prove calibrated site-level forecasts: small aggregate bias can conceal large individual errors, and cAUC is not inherently an estimator of future AUC. Nevertheless, your data contradict a blanket claim that within-event corrections cannot help environmental models.

   My diagnosis would be: **evaluation must match the intended transfer task, and uncertainty must reflect replication across landscapes and periods. Raw within-event discrimination is insufficient evidence of future-burning performance.**

3. **The MDD calculation is sound as a scenario, not as a universal noise floor.**

   With independent, equally weighted sites and paired SD 0.13073:

   \[
   \mathrm{MDD}_{80\%}\approx(1.96+0.84)\frac{0.13073}{\sqrt{29}}
   =0.0680.
   \]

   Required sites for a 0.01 effect are approximately **1,340**, using this normal approximation. Small-sample corrections increase the current MDD somewhat.

   Qualifications:

   - **Use the paired contrast’s SD.** Marginal AUC variability is insufficient. Closely related maps can have highly correlated errors and a much smaller difference SD.
   - At 29 independent sites, detecting 0.01 with 80% power requires paired SD approximately **0.0192 or less**. That is possible; it must be measured for the proposed offset comparison.
   - A prespecified one-sided 5% test gives MDD approximately **0.0604**, rather than 0.0680. A two-sided 95% interval with its lower bound above zero retains the approximately 1.96 critical value.
   - Unequal years per site require an explicit estimand. Equal-site averaging targets a typical selected landscape; equal-site-year averaging gives greater weight to sites with more eligible years.
   - Spatial dependence and shared regional years can reduce effective replication. Nonoverlapping rectangles do not establish independence.
   - Bounded AUC does not invalidate the approximation, but skewness and influential sites matter with 29 observations.
   - The observed site-mean SD mixes persistent heterogeneity with uncertainty from finite, unequal follow-up.

   **Do not call differences below the MDD “ties.”** MDD describes design power. It is neither an equivalence margin nor the threshold below which effects do not exist. Report “unresolved”; reserve equivalence for intervals contained within an independently justified practical margin.

   Also, comparing an SE of a **mean** with the observed SD across years is not an uncertainty validation. Validate mean intervals against repeated mean estimates, and prediction intervals against individual outcomes. Those are different targets.

4. **The 90% claim is not supported by these files.**

   Your assumed calculation is arithmetically correct:

   - Forecast-error contrast: \(0.20/(0.15/\sqrt{20})=5.96\).
   - Selection contrast: \(0.15/(0.15/\sqrt{20})=4.47\).

   But the files do not supply the actual paired contrast vectors needed to justify either calculation.

   **Forecast comparison.** The raw thermal overstatement on 13 matched sites is 0.215, but this is **not** the reduction in absolute error from cross-site forecasting. The latter subtracts the cross-site forecast’s own error.

   As a diagnostic only, forecasting a constant 0.60 gives an absolute-error reduction of **0.115**, SD **0.112**, on these 13 sites. Extrapolated to 20 independent sites, that gives z≈**4.60**. This suggests raw AUC is a beatable comparator; it does not validate the proposed forecast.

   A cross-site forecast can fail through shorter history, earlier calendar periods, horizon mismatch, geographic shifts, or broad intervals that achieve coverage without useful precision. Against cAUC or sAUC_c, the expected advantage is much less secure.

   **Selection comparison.** R1’s quoted 0.675 comes from a different task/support. It cannot be paired with c16’s 0.525 to estimate the selector’s variance.

   If one provisionally treats 0.675 as a constant at every c16 site—an **unsupported illustration**, not a result—the implied z at 20 sites is:

   | Comparator | Illustrative z |
   |---|---:|
   | Coordinate RF | 4.81 |
   | Thermal + coordinates | 2.96 |
   | Always thermal | 2.57 |
   | Baseline | 2.41 |

   Real R1 variation and its covariance with competitors can move these substantially in either direction.

   Main failure modes are fewer eligible independent clusters; weaker R1 with shorter pre-2005–2016 history; changed two-year targets; density and label corrections; and a fair within-event candidate set choosing something stronger than coordinate-only RF.

   **My subjective probabilities of a positive paired contrast with a two-sided 95% interval excluding zero**, conditional on roughly 20 eligible independent clusters and a properly frozen analysis:

   - Cross-site forecast versus **raw focal thermal AUC**: **75%**.
   - Selector versus a **fair practical within-event selector**: **55%**.
   - Both: approximately **40–45%**, with dependence unknown.

   Against an explicitly coordinate-only comparator I would assign a higher probability, around 75%, but less scientific value. These are judgement estimates, not calculated power or posterior probabilities. Actual blind eligibility remains unverified.

5. **Contrast 3 risks being a straw man.**

   Coordinate-only models are useful diagnostics. They should not carry the primary deployment claim.

   A fair comparator set includes:

   - Always R1.
   - Always the prespecified environmental model, including the nonthermal baseline.
   - Always the development-selected strongest practical model.
   - Raw-AUC and cAUC selection over the **same implementable focal-model candidate set**.
   - An earlier-transition selector without the proposed abstention threshold.

   Include thermal-plus-coordinate and thermal-plus-distance models. Keep coordinate-only models as diagnostic candidates or a separate analysis.

   Pairwise c16 results show why candidate composition matters. Raw AUC selected thermal-plus-coordinates in **18/18** comparisons with thermal; cAUC selected it in **16/18**. Their selected later AUCs were **0.58126** and **0.57999**. For the distance-feature pair, cAUC improved selected performance from **0.56253 to 0.58018**.

   These are pairwise choices, **not a verified multiway selector**. The CSVs do not contain everything needed to reconstruct a common multiway focal ranking.

   Whether your rule beats “always environmental” is currently **unverified on matched G-B units**. Moreover, if it always returns R1, its performance adds nothing beyond “always R1.” A rule that almost never switches cannot establish that its switching criterion is useful.

   Replace “beats by more than MDD” with a clear decision criterion, such as a prespecified lower confidence bound exceeding a practical benefit margin. MDD is a planning quantity, not an optimal deployment rule.

6. **Novelty: 2/5 for the method; potentially 3/5 for a convincing empirical EMS paper.**

   I verified these precedents during this review:

   | Precedent | Verified relevance |
   |---|---|
   | [Obuchowski, 1997](https://pubmed.ncbi.nlm.nih.gov/9192452/) | Clustered AUC inference, effective sample size and sample-size planning. Event-aware ROC uncertainty is not new. |
   | [Meyer et al., 2018](https://cris.uni-muenster.de/portal/en/publication/61024062) | Target-oriented validation and feature selection, including leave-location-out evaluation; already an EMS contribution. Verified through the authors’ institutional record and abstract, not a full-text audit. |
   | [Roberts et al., 2017](https://www.biom.uni-freiburg.de/mitarbeiter/dormann/roberts-et-al-2017-ecography.pdf/at_download/file) | Validation strategies for spatial, temporal and hierarchical dependence, chosen around prediction goals. |
   | [Dietterich, 1998](https://web.engr.oregonstate.edu/~tgd/publications/dietterich-approximate-statistical-tests-nc1998.pdf) | Dependence, error rates and power in algorithm comparison. |
   | [Demšar, 2006](https://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf) | Paired comparison of algorithms across datasets rather than treating individual predictions as independent evidence. |
   | [Bates, Hastie and Tibshirani](https://arxiv.org/abs/2104.00673) | What cross-validation estimates and how accurately its intervals cover prediction error. Relevant to “validation of validation,” though not an exact precedent for your geographic performance forecasts. |

   None is an exact duplicate of the whole application. Together they substantially anticipate its methodological ingredients. Adding MDD and prediction intervals is good practice, not strong standalone novelty.

   I did **not** establish an exhaustive priority claim for performance forecasting, nor independently reverify every fire-history precedent listed in the earlier review. Do not claim this is the first such protocol.

7. **It is primarily amendment 14 with better inference and revised interpretation.**

   Amendment 14 already contains clustered uncertainty, future-burning evaluation, a density reference, an honesty comparison and a blind test. Prediction intervals make the honesty analysis more explicit; abstention formalizes defaulting to the reference.

   A substantive new contribution would require showing that:

   - The performance forecasts have useful, externally validated calibration and sharpness.
   - The uncertainty-aware selector improves decisions over fixed choices and simpler selectors.
   - These benefits persist against corrected within-event estimates.

   If the empirical outcome is “the rule always chooses R1 and raw AUC is optimistic,” the new contribution remains modest. I would not present this revision as a new evaluation theory.

8. **Record this as an explicitly development-informed amendment.**

   Preserve the old diagnosis, the results that challenged it, the revised wording, every changed endpoint and comparator, and the dates of those changes. State that this hypothesis was formed after inspecting all development results. The earlier frozen-score replication remains evidence for its original claims; it does not become confirmation of the newly formulated method.

   I would freeze:

   **Primary performance claim:** one development-selected practical candidate versus R1 on corrected, complete two-year G-B, with an equal-site paired estimand and clustered interval. Treat superiority and exclusion of a practical gain as distinct questions.

   **Primary evaluation claim:** for one fixed environmental procedure,

   \[
   D_i=|\widehat A_{\text{focal},i}-A_{\text{later},i}|
       -|\widehat A_{\text{cross-site},i}-A_{\text{later},i}|.
   \]

   Test its mean on matched sites. Compare cross-site forecasts with **cAUC and sAUC_c as declared secondary contrasts**, rather than omitting the strongest corrected estimates.

   **Secondary decision claim:** the frozen selector versus always R1, always environmental, and raw-AUC/cAUC selectors on a common candidate set and common scoring support.

   Freeze eligibility, weighting, geography clusters, horizon, targets, forecast construction, prediction-interval scoring, missing-data rules, fallback, multiplicity and failure wording. Use horizon-matched historical validation where possible; otherwise label the one-year estimate a proxy.

   Bootstrap uncertainty for already frozen scores can describe evaluation-sample variability. Claims about the full training-and-selection procedure require resampling or independently repeating that procedure as well.

   Keep both successful and failed outcomes publishable. Do not redefine the paper’s success after blind opening.

9. **The paper I would write has this headline claim:**

   **“High within-event discrimination does not establish skill on later burning; susceptibility models require temporal evaluation against a fire-history reference.”**

   This is narrower than “events are the only evidence,” and better supported.

   The smallest convincing analysis set is:

   1. **Matched focal-to-later evaluation:** raw AUC, cAUC and sAUC_c for the same environmental and practical location-using models; report signed error, absolute error and selection consequences.
   2. **Corrected temporal benchmark:** R1, a credible environmental model and the single R1-offset comparator, on common support and complete two-year follow-up. Report paired effects and intervals.
   3. **One untouched replication:** freeze those analyses and forecasts before opening blind outcomes; retain all eligible sites and disclose exclusions.
   4. **Essential robustness:** per-site effects, geographic dependence, observation support, fixed-cover sensitivity and an independently documented large-fire target where feasible.

   Event-count relationships and interval calibration would be useful secondary analyses. I would omit another method search and avoid making successful abstention a prerequisite for the paper.

**Ranked minimum changes**

1. **Replace the absolute event-unit diagnosis** with a task-matching and replication argument; acknowledge the corrected metrics’ demonstrated improvement.
2. **Finish the agreed label, horizon and kernel fixes**, then recompute matched development comparisons before making power claims.
3. **Resolve weighting:** +0.00516 and SE 0.02428 currently refer to different estimators.
4. **Remove the 90% claim and “below MDD means tied.”** Calculate contrast-specific uncertainty and design power.
5. **Use practical comparators**, especially always environmental, always R1 and cAUC selection; keep coordinate-only models diagnostic.
6. **Freeze a small, development-informed blind analysis**, with forecast accuracy and model-selection utility treated separately.
7. **Pitch an empirical EMS evaluation contribution**, not a new statistical method; retain a publishable conclusion if the blind effects are small or uncertain.