**Go with changes — for a bounded calibration study; no-go as a 4/5-novelty method with the claimed guarantees. Relocated-fire nulls already exist, and the proposed transferable-AUC estimator is not yet justified.**

1. **Evidence A, B and C: mostly reproduced, with several material corrections.**

   I recalculated the CSV summaries and inspected the branch’s synthetic generator, focal/later scoring scripts and future-label exporter. I did not reconstruct the underlying rasters or refit models. No files were modified.

   **A reproduces:**

   | No environmental signal, \(a=0,b>0\) | All 186 runs | \(b=4,L=10\), 31 runs |
   |---|---:|---:|
   | Environmental forest focal AUC | 0.60317 | 0.69257 |
   | Coordinate forest focal AUC | 0.79942 | 0.91913 |
   | Geographic-null AUC | 0.75891 | 0.88973 |

   Mean independent-redraw AUC is **0.50138** for the environmental forest and **0.49649** for the coordinate forest, consistent with expected chance performance.

   Two qualifications matter:

   - The real **0.96383** in c14 is the **coordinate forest’s focal AUC**, not a verified mean of the distance-based geographic null. Those are different models.
   - Neither that number nor A establishes that relocated real scars will produce a higher environmental-model placebo AUC. Shape, folds, mask, position and predictor smoothness all matter. That expectation needs measurement.

   **B reproduces on the same 18 fires**, with exact agreement between c14 and c15 thermal later AUC:

   | Model | Raw bias / MAE | cAUC bias / MAE | sAUC_c bias / MAE |
   |---|---:|---:|---:|
   | Thermal | +0.227 / 0.253 | +0.032 / 0.158 | −0.008 / 0.112 |
   | Thermal + distance | +0.384 / 0.384 | +0.068 / 0.137 | +0.050 / 0.112 |
   | Thermal + coordinates | +0.380 / 0.380 | +0.165 / 0.199 | +0.125 / 0.149 |
   | Coordinate forest | +0.471 / 0.471 | +0.272 / 0.299 | +0.259 / 0.259 |
   | Coordinate kNN | +0.455 / 0.455 | +0.256 / 0.258 | +0.221 / 0.221 |

   “Overstate every model” is correct **on average within each class**, not necessarily at every site.

   The later target is **after each focal label’s end through December 2023**, excluding focal-burned cells and restricting observation coverage. It is not a common 2017–2023 horizon.

   **C’s numerical results reproduce, but its sample size is wrong: 558, not 744.** There are \(31\times3\times3\times2=558\) runs with \(a>0,b>0\). The 744 count includes the 186 \(a=0,b>0\) runs.

   | Model / estimator | Bias | MAE | Correlation with truth |
   |---|---:|---:|---:|
   | Environmental cAUC | −0.0015 | 0.0558 | 0.831 |
   | Environmental sAUC_c | −0.0153 | 0.0603 | 0.812 |
   | Environmental ratio | −0.0096 | 0.0588 | 0.802 |
   | Coordinate cAUC | +0.0595 | 0.1010 | −0.043 |
   | Coordinate sAUC_c | +0.1000 | 0.1239 | −0.084 |
   | Coordinate additive | −0.0595 | 0.0868 | 0.440 |
   | **Coordinate ratio** | **−0.0658** | **0.1169** | **0.331** |

   The omitted coordinate-ratio result matters: the proposed primary estimator is worse than cAUC by MAE there.

   Selection losses reproduce: raw **0.0579**, sAUC_c **0.0433**, cAUC **0.0223**, placebo difference **0.0094**, always environmental **0.0056**. Balanced accuracies also reproduce. Environmental truth wins **87.8%** of these runs. Placebo selection reduces loss but does not beat the simple default.

   Crucially, C tests **independent generator draws**, not rigid relocation of observed scars. It supports investigating a pipeline-specific null; it does not validate the proposed relocation algorithm.

2. **The diagnosis is useful, but “the defect is the missing geometry-matched null” is too exclusive.**

   B demonstrates a practical gap: corrected focal scores remain poor forecasts of later discrimination for several location-using models. That is worth documenting.

   It does not establish a newly discovered defect in cAUC. Hijmans targets **spatial sorting bias**, using distance-based null calibration and pairwise distance sampling; it does not promise recovery of future-event AUC for arbitrary spatial learners. Your result is a consequential limitation of using those corrections as transferable-performance estimates. [Hijmans, 2012](https://pubmed.ncbi.nlm.nih.gov/22624221/)

   Also, cAUC is not merely restriction of test cells: your implementation combines matching and null calibration. Describe the existing procedures accurately.

   A geometry-matched reference can expose how easily a pipeline learns arbitrary spatial patches. But focal-to-later disagreement also reflects changed case composition, exclusion of the focal scar, follow-up horizon, fire weather and persistent versus transient spatial drivers. Relocation cannot automatically separate those mechanisms.

3. **Property (i) is false as stated. A restricted null version is correct.**

   Let \(T(Y)\) be the entire pipeline’s focal AUC, including fold construction, training and scoring. An exact population statement requires:

   \[
   Y_{\mathrm{obs}},Y_1,\ldots,Y_K
   \quad\text{to be exchangeable under the specified placement null.}
   \]

   One sufficient design is an observed placement and placebo placements drawn independently from the **same prespecified distribution of admissible positions and orientations**, conditional on shape and other declared constraints.

   Then, for the population placebo mean \(\mu\),

   \[
   E[T(Y_{\mathrm{obs}})]=\mu.
   \]

   Both proposed transformations have expected value 0.5 when \(\mu\) is known. This applies to **every model under that null**, not uniquely to coordinate-only models.

   It does **not** imply that a coordinate-only model scores equally on an actual environmentally selected scar and random placements. Coordinates can proxy persistent environmental risk. Nor does it imply that adding coordinates cannot improve calibrated performance under an alternative: feature interactions and learning behavior invalidate that monotonicity claim.

   Specific problems:

   - **Centred rectangle:** selection of the window using the actual scar makes its position special. Random placements in that fixed window do not reproduce that selection process.
   - **Overlap ≤20%:** excludes the observed scar’s own placement and its neighborhood. This is not an ordinary exchangeable reference sample.
   - **Burn-count tolerance:** changes the placement distribution through the population mask and permits changes in the statistic’s sampling properties.
   - **Rotations/reflections:** require corresponding symmetry assumptions. Wind direction, terrain and fuel configuration can make them implausible.
   - **Block CV:** does not inherently invalidate randomization. Fixed blocks are acceptable under a valid placement design; label-dependent fold rules must be rerun identically. Central and peripheral scars can nevertheless interact very differently with folds.
   - **Finite \(K\):** additive calibration remains unbiased under the ideal exchangeable null; the ratio generally does not, because its estimated denominator introduces nonlinear bias.

   With exchangeability, use \((1+\#\{T_k\ge T_{\mathrm{obs}}\})/(K+1)\). Without it, call the result a **reference-tail probability**, not an exact randomization p value. At \(K=30\), p-value resolution is only \(1/31\).

   Property (ii) should therefore become: **the procedure can be applied to arbitrary pipelines; its validity still depends on the null and target assumptions.**

4. **The calibrated number is meaningful as an index; it is not yet identified as transferable AUC.**

   Write observed focal AUC as \(o\), placebo mean as \(p\).

   | Transformation | Assumption needed to interpret it as target AUC \(A\) |
   |---|---|
   | Additive: \(0.5+o-p\) | \(o=A+p-0.5\) |
   | Ratio: \(0.5+0.5(o-p)/(1-p)\) | \(o=p+2(A-0.5)(1-p)\) |
   | Null quantile \(F_0(o)\) | Measures extremeness under the null; supplies no target-AUC mapping |
   | Spike-in calibration | Requires a specified, sufficiently realistic family of alternatives and transfer processes |

   Neither additive nor ratio assumptions follow from preserving geometry. Null calibration identifies behavior at the null; it does not identify the response curve away from it.

   The ratio is particularly unstable near \(p=1\). Its sensitivity to observed AUC is \(0.5/(1-p)\): **5 at \(p=0.90\), 12.5 at \(p=0.96\)**. Small errors become large forecast changes. Both transformations can produce negative values; clipping changes bias and must be frozen.

   Your simulation already argues against one universal formula: ratio is competitive for environmental models, additive is better for coordinate models, and neither establishes performance for practical mixed models.

   **Prefer a prespecified spike-in response curve**, tested on held-out landscapes and generator families. Include persistent spatial risk, transient fire-specific spatial fields, environmental effects, irregular masks and plausible scar-generation mechanisms. Merely adding more draws from the existing generator mainly improves precision within its assumptions.

   Tilting rigid placements by an environmental index creates an alternative, but does not itself provide known transferable AUC. You must define future placement draws and evaluate the fitted score under that process.

   When environmental association operates through **shape and position together**, conditioning on shape removes part of the phenomenon you want to measure. The resulting statistic measures excess fit for the observed placement relative to alternative placements of that shape. It is not a decomposition of transferable versus geometric skill.

   Accordingly, rename “geometry share” **relative placebo excess**. It is not a causal share and can exceed one or become unstable near observed AUC 0.5.

5. **The Beale criticism does not sink the diagnostic; it does undermine the automatic interpretation.**

   Random spatial patterns can align with smooth environmental fields. That is precisely why a spatial null can be more informative than shuffled independent labels.

   The harder criticism is that the pattern’s spatial structure may itself encode environmental constraints. Preserving it can condition away real signal; changing the study extent can also change the conclusion. These concerns were explicitly discussed in the climate-envelope debate. [Beale et al., 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2567466/), [Thomas, 2010](https://onlinelibrary.wiley.com/doi/10.1111/j.1472-4642.2010.00642.x)

   Blind later-burning validation can establish that a frozen calibration **predicts that operational target usefully**. It cannot retroactively prove exchangeability, causal attribution or universal validity.

   Step 5 also overclaims:

   - Relocated later events do not necessarily have mean AUC 0.5 on a bounded, masked landscape. Equal inclusion probabilities and suitable symmetry are additional requirements.
   - Null spread depends on the score map, mask and event arrangement, not only event count and size.
   - A relocation reference interval is not automatically a confidence interval for actual future skill or a prediction interval under environmental selection.
   - Agreement with year-to-year SD would be informative, but would not establish coverage.

   The stated MAE floor near 0.10 is likewise unsupported. It follows approximately from Gaussian **irreducible error** with SD 0.13, whereas observed annual variation includes predictable heterogeneity and differs from pooled later-outcome uncertainty.

6. **My probability of primary blind success as written: 30%.**

   This is a subjective assessment, conditional on roughly 20 eligible, reasonably independent blind sites and a genuinely frozen analysis—not calculated power.

   The most likely failure is **poor transport of the null-to-transfer mapping**: relocation captures how readily patches are learned but cannot determine how much of a mixed model’s spatial fit persists into later fires. Ratio instability and the centred-window design compound that problem.

   The environmental candidates already give cAUC a strong position. Improving the mixed coordinate model must outweigh any harm to thermal, baseline and distance models.

   There is also a revealing benchmark: constant **0.5** has development MAE **0.148, 0.107 and 0.132** for thermal, thermal+distance and thermal+coordinates, respectively. Corresponding cAUC MAEs are **0.158, 0.137 and 0.199**. Thus beating cAUC alone could reflect useful shrinkage toward chance rather than information supplied by relocated scars.

   Define the primary site contrast explicitly:

   \[
   D_i=\frac14\sum_{m\in\mathcal M}
   \left(
   |\widehat A_{im}-A^{later}_{im}|
   -|cAUC_{im}-A^{later}_{im}|
   \right).
   \]

   Success means the 95% interval for mean \(D_i\) lies below zero. Models within a site are not independent replicates. Freeze horizon, support, model weights and geographic clustering. Include constant and development-only forecasts as benchmarks.

7. **Novelty: 2/5 for the proposed method; potentially 3/5 for a convincing complete study. Not 4/5 on present evidence.**

   The targeted search found stronger precedents than the proposal acknowledges:

   | Verified precedent | What it establishes |
   |---|---|
   | [**Wildfire Selectivity for Land Cover Type: Does Size Matter?**, 2014](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0084760) | Direct fire precedent: 1,670 real fire perimeters translated and rotated into 500 null maps, retaining shape and size distribution. This defeats novelty of relocated-scar null generation. |
   | [**Beale et al., 2008**](https://pmc.ncbi.nlm.nih.gov/articles/PMC2567466/) | Spatially structured response nulls compared using model fit/AUC; explicitly discusses cutting and pasting distributions at new locations and orientations. |
   | [**Hijmans, 2012**](https://pubmed.ncbi.nlm.nih.gov/22624221/) | Geographic-null calibration of cross-validated AUC and distance matching. |
   | [**Ridder et al., 2024**](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.14443) | Shift-and-rotate environmental surrogates; evaluates AUC under random, spatial and environmental CV, including models with spatial effects. Randomizes predictors rather than scars, but closely anticipates the diagnostic logic. |
   | [**Bohl, Kass and Anderson, 2019**](https://onlinelibrary.wiley.com/doi/10.1111/jbi.13573) | Null-model performance/effect-size evaluation using independent transfer data. Therefore “null calibration plus independent outcomes” is not itself new. |
   | [**Warren et al., 2021**](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13591) | Monte Carlo estimation of study-design biases in transferred distribution-model outputs. |
   | [**Kelly, 2019**](https://www.ucd.ie/economics/t4media/WP19_13.pdf) | Verified the working paper: replaces explanatory or response variables with spatial noise to diagnose misleading regression evidence. Not an AUC-calibration precedent. |

   I checked the relevant fire and Ridder methods passages, the Beale text, publisher abstracts for Bohl and Warren, and Kelly’s working-paper abstract. These are specific verified precedents, not an exhaustive priority review.

   Targeted landslide searches did **not** verify an exact relocated-scar susceptibility-calibration precedent. That does not establish absence.

   The potentially distinctive contribution is narrower: **using a pipeline-specific spatial-null distribution to forecast numerical later-event discrimination, then testing those forecasts blindly against corrected and simple forecasting baselines**. That contribution remains to be demonstrated.

8. **The single most valuable change: make the null-to-transfer response curve the method.**

   Replace the universal ratio with a calibration framework whose assumptions and limits are explicit, trained on diverse simulated event processes and tested on held-out generator families and landscapes before blind real evaluation.

   Keep additive and ratio corrections as simple comparators. Require the response curve to improve on chance shrinkage and development-only forecasts.

   This change targets the genuinely unresolved problem: **whether spatial-null behavior contains information about future discrimination beyond ordinary shrinkage**. More elaborate relocation alone will not supply 4/5 novelty.

9. **Compared with reply 2: currently an add-on, not a better replacement paper.**

   The empirical headline remains well supported: high within-event discrimination does not establish later-burning skill. Placebo fires could strengthen its explanation and provide a useful diagnostic.

   Making the paper depend on a universal transferable-AUC correction would currently weaken it. If a frozen, assumption-aware calibration improves blind forecasts over cAUC, sAUC_c and simple defaults, it could become the stronger methodological contribution. Until then, retain the empirical paper as the backbone.

**Ranked minimum changes**

1. **Withdraw properties (i)–(ii) as universal guarantees.** State the exchangeable null precisely and distinguish diagnostic calibration from transferable-AUC estimation.
2. **Fix placement validity before large-scale fitting.** Use a focal-independent window where possible; address centring, boundary/mask effects and the asymmetric overlap exclusion.
3. **Replace the universal ratio claim with a tested response curve**, using diverse persistent/transient spatial processes and held-out generators.
4. **Add chance-shrinkage and development-only forecast benchmarks**, with equal-site inference and a matched, frozen target horizon/support.
5. **Remove step 5’s automatic confidence-interval claim and the asserted MAE floor.**
6. **Correct C to 558 runs and acknowledge the 2014 relocated-fire precedent.** Keep novelty claims centred on validated performance forecasting, not random scar placement.