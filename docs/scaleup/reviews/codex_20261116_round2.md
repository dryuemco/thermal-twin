1. **Modify — several concrete problems; the calendar inequalities themselves are correct.**

   - **Calibration chronology:** `history()` excludes the evaluated geographic group. G-A’s `u <= T-1`, G-B’s `u+h-1 <= T0-1`, and G-C’s `u <= T-2` correctly ensure completed labels by 1 May T, assuming the panel’s May–April definition. G-C’s calendar summers **T and T+1** also match that cut-off. However, the upstream forest, BLUP and gate implementations are not supplied, so their chronology cannot be certified here.
   - **G-B scar mismatch:** `build_units()` defines `scar = window(Y, site, fy, fy, ...)`. That removes **all burns in the focal May–April target year**, not the focal-event scar required by 14.1. The supplied `later()` helper does the same. Use the actual focal label, aligned to this grid.
   - **Incomplete horizon:** G-B labels include incomplete 2026, but calibration labels contain complete May–April years. Thus nominally matched `h` does **not** match observation duration. The resulting probability scores have an additional calibration mismatch.
   - **Changing population becomes zero:** `label_grids()` initializes absent cells to false; `window()` then unions these grids. A cell present at the prediction cut-off but absent from later population masks contributes no later burns. This conflates exclusion/missing observation with unburned status. Construct future labels and observation coverage independently of future vegetation masks.
   - **Wildfire target:** `Yb` uses each future year’s `wildfire_keep()`, including its updated `burns_10y`. Consequently, G-B removes some burns according to recurrence accumulated **after prediction**, beyond its explicit cut-off recurrence exclusion. That can define a retrospective target, but it differs from “frequent at cut-off plus small patches removed.” Separate these operations. Patch sizes are also measured within population masks and rectangle boundaries, which can fragment larger events.
   - **TMA-cell:** the displayed recomputation uses complete earlier years correctly. Numerical reproduction is checked only in the final summary, without an assertion; neither the original implementation nor gate log is supplied. Require agreement on **cell scores**, plus configuration coverage, before relying on the reconstruction.
   - **R0/RM:** the ratio-of-sums BSS/LSS aggregation correctly gives equal weight to unit-mean losses. But `th["R0"] = platt(...)` means the evaluated R0 is **recalibrated site climatology**, not raw climatology. RM is an unconstrained fitted logistic combination, not guaranteed to outperform either component out of sample. Name both accurately.
   - **Honesty:** G-B uses historical **one-year G-A AUC** to estimate multi-year G-B AUC. That is a task mismatch, not purely evaluation optimism. Moreover, `cross = known[known.grp != r.grp]` does not establish that those historical models/gates were trained excluding `r.grp`; that requires upstream verification. Honesty summaries have no bootstrap intervals, so this script does not implement H2’s paired uncertainty test.
   - **Other implementation issues:** raw-score AUC/AP can disagree with calibrated-probability rankings when Platt slopes are negative—the script explicitly counts such slopes. Declare which ranking is operational. `CELL` uses degrees ×111.32 without longitude correction, so the displayed smoothing is not an isotropic physical 2 km kernel on these geographic grids.

   **Action:** fix scar and observation support first; resolve target definitions, calibration/ranking consistency and honesty estimands before freezing.

2. **Modify — add the comparator, but disclose a narrow exception to the stopping rule.**

   Receiving density does not mathematically guarantee that a fitted forest preserves its ranking. The 0.604 versus 0.659 result demonstrates a weak fitted competitor; it does not identify negative sampling or site weighting as the cause. Nevertheless, it weakens any broad claim about environmental information.

   Your offset model is reasonable. Calling it a comparator does **not** erase the fact that it is another attempt to beat R1 after 14.8 ended that search.

   **Action:** publish one explicit amendment allowing this single comparator; fix features, scaling, penalty grid, minimum local support, fallback and selection criterion before running it. Use chronological local fits and genuinely out-of-group penalty selection. Include the zero-correction case, retain every existing result, prohibit follow-up tuning, and choose the blind “best model” by a fixed development rule. It may receive blind validation, but it cannot retroactively satisfy 14.2’s completed candidate search.

3. **Modify — useful external validation, not automatically an independent gold standard.**

   The supplied files contain neither EFFIS provenance nor coverage documentation. They therefore cannot substantiate the proposed geographic completeness, threshold or independence from satellite inputs. Separate products can still share detection errors.

   Given your stated mapping threshold, EFFIS is better aligned with **G-C’s ≥100 ha events** than G-B’s all-burn target. At 500 m, perimeter rasterization and boundary errors matter substantially.

   **Action:** freeze an external-target analysis before opening blind outcomes: documented country/year coverage; consistent area-overlap rasterization; coverage-based exclusions; ≥100 ha common-support comparison; boundary sensitivity; paired model–R1 effects. For G-C, reconcile event-start dates and event aggregation. Specify now; execute blind evaluation afterward. A development feasibility audit should precede the freeze. Do not silently replace the primary target.

4. **Modify — a limitation plus T−2 sensitivity is insufficient for an operational cut-off claim.**

   Amendment 13.10 explicitly acknowledges that T−1 was unavailable on 1 May, and specifies **fixed 2001 cover** as the sensitivity. T−2 availability is not established by these files either.

   **Action:** use the latest map demonstrably released before each cut-off for the operational analysis, or explicitly describe the primary analysis as retrospective. Retain the declared fixed-2001 sensitivity and add T−2 only with release-date evidence. Apply the same availability rule to blind-site selection.

5. **Agree — make complete two-year follow-up primary, with transparent disclosure.**

   The strongest reason is comparability: equal exposure duration and horizon-matched calibration. The “all” horizon mixes different follow-up lengths and calibrates a partially observed final year against complete years. Unobserved future months are not observed negatives for a full-year estimand.

   The argument against changing now is real: two-year results have already been seen, and they favour R1 even more—approximately **0.699 versus TMA-cell 0.620**, compared with **0.675 versus 0.632** for “all.” This is an informed endpoint change.

   **Action:** amend before blind opening, disclose those development results and the reason, retain both horizons, and require complete two-year observation. For the sensitivity, define the endpoint as the exact last observed date and match calibration duration. A pre-blind correction remains legitimate; it is not an unseen development decision.

6. **Modify — distinguish absence of demonstrated superiority from exclusion of a meaningful gain.**

   The stopping result is precise: no candidate met the declared **+0.01 G-A development threshold**; TMA-cell was −0.003 on its 238-unit stopping set. That does not establish that no model can improve on R1.

   An upper confidence bound below +0.01 supports a stronger statement than failed superiority, but “no improvement larger than 0.01 was found” understates—and ambiguously describes—that inference.

   **Action:** predeclare: “For the development-selected model, the upper 95% confidence limit for mean AUC gain was below 0.01.” Explain that this excludes gains of that size **for this comparison and population**, without claiming equivalence. Select the model before blind evaluation; a claim covering every candidate requires simultaneous bounds. Avoid “non-inferiority” terminology unless its direction is carefully defined.

7. **Modify — the supplied evidence suggests more intersection clusters than you propose, but fewer effective independent regions.**

   Amendment 13.11 says **no two development rectangles overlap**, implying 31 intersection clusters if that remains true for these grids. The supplied claim16 summary reports **18 clusters for 18 eligible sites**. Thus 20–25 cannot be inferred from the supplied files. The blind scan’s cluster count is entirely unknown.

   Rectangle nonintersection establishes geometric separation, not independence: nearby sites may share weather, ignition regimes and model-training data. The five geographic groups address a different, broader dependence scale.

   **Action:** report actual counts after the scan, cluster sizes and spatial separation. With 20–25 plausibly independent clusters, a cluster bootstrap is usable but approximate. Keep the prespecified interval primary, accompanied by per-cluster effects and leave-one-cluster-out influence checks; add broader geographic clustering as sensitivity. Those diagnostics expose fragility but do not replace an uncertainty estimate. State whether the estimand weights sites or clusters equally—the current bootstrap preserves the unit-weighted mean.

8. **Modify — promising for an EMS methodological evaluation; not yet ready to freeze.**

   The negative method search is informative, and the register’s disclosure is a strength. The central weakness is currently whether the comparison measures incremental predictive value under a coherent, reproducible target—not algorithmic novelty.

   **Minimum changes, ranked:**

   1. Fix focal-scar removal, future observation support and complete primary follow-up.
   2. Freeze exact wildfire labels, physically defined density bandwidth and prediction-date availability.
   3. Add the single strong offset comparator through the disclosed exception.
   4. Correct and implement the honesty comparison, including paired cluster uncertainty and training exclusion checks.
   5. Freeze external-target validation, model selection, confidence-bound wording and cluster sensitivities; then push the score manifest before opening blind labels.

   Also describe the supplied “standard spatial” comparator accurately: amendment 13.13 replaced the promised persistent–transient model with an approximate **persistent-only** fit. It cannot support a claim that TMA was tested against a full standard spatiotemporal model.