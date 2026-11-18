**No-go as proposed.** The boundary contrast merits a small exploratory test, but the claimed likelihood, causal explanation and exact nesting are not established. I would run the already agreed R1-offset comparator before reopening the method search.

I read the supplied document and code copies, including amendments 9–14. I did not run analyses, inspect the underlying rasters, or verify the copies against the remote branch. No files were modified.

1. **The percolation likelihood is correct only under restrictive assumptions that the proposal does not establish.**

   Let independently open sites have probabilities \(q_i\), and let \(C\) be the complete connected open cluster containing a specified seed \(s\). Conditional on the seed being open,

   \[
   P(C\mid s\text{ open})=
   \prod_{i\in C\setminus\{s\}}q_i
   \prod_{j\in\partial_V C}(1-q_j).
   \]

   Here \(\partial_V C\) means **every unburned vertex adjacent to \(C\)**, including adjacent cells in unburned islands. It does not mean only the exterior perimeter. Without conditioning on an open seed, its \(q_s\) factor remains.

   This assumes permanent site openness, complete propagation through the reachable open component, known adjacency, and no externally imposed stopping time. Under those assumptions, additional exposures do nothing: a site is either open or closed.

   That differs from bond percolation or repeated ignition attempts. With independent transmission probabilities \(p_{ji}\), failure after exposure from several neighbours involves \(\prod_j(1-p_{ji})\). The probability of a final scar generally requires integrating over possible transmission histories; the proposed site product does not supply that likelihood.

   Several practical failures follow:

   - **Weather and suppression:** an unburned boundary cell may be combustible but never receive an effective exposure before the fire stops. Final adjacency does not establish comparable exposure.
   - **Event effects:** weather does not automatically “cancel.” A conditional logistic model can eliminate an additive event intercept by conditioning on event totals; an ordinary classifier with event weights does not. Wind direction, changing weather and suppression are not common additive intercepts anyway.
   - **Islands:** include adjacent island cells as possible failures, with observation checks; do not label an entire island exposed merely because it lies within a perimeter.
   - **Truncation:** the 22-cell buffer in `event_export.py` reduces clipping but cannot guarantee complete events. Events touching the buffered edge require exclusion or explicit truncation treatment.
   - **Timing:** daily burn dates cannot order subdaily neighbour exposures reliably. Equal-day burns do not identify transmission direction.
   - **Event construction:** `rstar_precheck.py` joins adjacent cells through pairwise date gaps of at most seven days. Transitive chains can span much longer than seven days, merge separate ignitions, and split one event across disconnected patches or calendar years.
   - **Repeated burning and observation:** `event_export.py` retains only the earliest date per cell-year and uses `unmask(0)`. Its output alone cannot distinguish reliably observed unburned cells from missing observations, or reconstruct subsequent burns.

   Selecting only events exceeding 100 ha also conditions on a model-dependent outcome. The displayed unconditional cluster likelihood omits that selection.

   **The simpler explanation of the diagnosis is already sufficient:** held-out parts of one contiguous realised scar are predictable from other parts of that scar. A distance model reconstructs the event’s geometry; later ignitions and footprints move. This is an interpolation-versus-future-prediction mismatch, consistent with amendments 9–11.4, without needing a censoring explanation.

   For annual or multiyear **burn occurrence**, observed unburned distant cells are legitimate negatives. They are uninformative about *flammability conditional on exposure*, which is a different estimand. Calling them censored in conventional susceptibility modelling conflates those targets.

2. **T1 is strongly design-dependent and does not demonstrate resolution.**

   Restricting negatives to the ring removes distant, easy negatives. A drop in distance-null AUC therefore largely demonstrates that the evaluation population changed.

   Nor is AUC near 0.5 guaranteed. With all scar cells as positives, interior cells and exterior ring cells have different geometry. Distance to training positives, coordinates, fold placement and scar shape can still discriminate them. Distance to the complete target scar would directly encode the labels.

   A non-trivial test would:

   - Hold out complete events and geographic groups.
   - Compare the **same model class and fitting budget**, trained using boundary versus conventional labels.
   - Evaluate both on the **same future-burning population**, primarily paired improvement beyond R1.
   - Separately assess boundary discrimination using matched inner/outer samples, prespecified ring widths and geometry-preserving nulls.

   If credible progression observations exist, an exposed-front risk set would be stronger: predict which currently unburned neighbours subsequently burn. These exports do not establish that risk set.

   T2 is useful only with that common evaluation target. T4 is a software sanity check under its own generative assumptions; recovering \(q\) from fires generated by the assumed model does not validate the explanation of real fires. Include competing generators with external stopping and spatially clustered labels.

3. **The exact-R1 claim is false for the stated implementation.**

   A continuous, infinite-domain heat kernel is Gaussian, with variance \(2Dt\) per axis. A finite grid graph’s heat kernel is generally different from a sampled, truncated Gaussian convolution. Eight-neighbour weights, unequal physical axis lengths, diagonal lengths, boundary conditions and source support all matter.

   The handoff already identifies the square-degree-grid error requiring amendment 14.10: physical east–west spacing differs from north–south spacing. The corrected R1 must be defined first. A graph cannot inherit exact equivalence merely by choosing a nominal 2 km diffusion scale.

   Also, \(z\) is defined on vertices: the proposal has not specified how to construct an **edge** conductance from its two endpoint values.

   For a symmetric combinatorial Laplacian,

   \[
   \dot u_i=\sum_j c_{ij}(u_j-u_i),
   \]

   mass is conserved and the equilibrium on a connected equal-area graph is uniform. High conductance means faster mixing, **not attraction toward high susceptibility**. Low-conductance source neighbourhoods can retain high density; high-conductance neighbourhoods can lose peaks. Adding \(\gamma z\) may compensate numerically without making this a contagion model.

   Within-site standardisation adds another problem: almost constant, poorly estimated \(q\) can become a unit-variance conductance field. Specify probability clipping, a variance floor, conductance bounds and physical units.

   **Preferred immediate operator: retain R1 and test the additive environmental correction.** If later pursuing propagation, use a destination-dependent transmission model with explicit exposure, stopping and ignition assumptions. A killed transport process can represent failed propagation more naturally than mass-conserving heat flow, but it still needs validation.

   If exact nesting is essential for an exploratory smoother, define it explicitly, for example

   \[
   S=\log(R1+\epsilon)+
   \{\log(u_\beta+\epsilon)-\log(u_0+\epsilon)\}+\gamma z.
   \]

   This guarantees the baseline at zero parameters; it does not make the smoother mechanistic.

4. **There are multiple leakage paths, including ones already visible in the supplied code.**

   - **January–April events:** “1 May before the event” must mean the preceding May, not May of the event’s calendar year. Otherwise predictors are post-event.
   - **Same-year history:** exclude every burn on or after the issue date from \(u\), time-since-burn and other history variables. Complete calendar-year layers are unsafe for a May issue date.
   - **Annual minimum dates:** a cell burning before and after the cutoff can retain only the earlier burn in `event_export.py`; that is insufficient for reconstructing later labels or events.
   - **Composite windows and publication:** audit full observation intervals and release availability. Amendment 13.2 explicitly requires complete pre-cutoff MOD13 intervals.
   - **Land cover:** amendments 13.10–13.11 acknowledge that the previous-year MCD12Q1 map was published after the issue date. Retrospective reconstruction and operational forecasting must remain distinct. Fixed-2001 is itself unavailable for the earliest cutoffs before that product’s release.
   - **Future population masks:** `panel_build.py` uses target-period unmapped share to decide which predictor rows exist. That may define retrospective evaluation support, but it must not determine the operational \(z\) field or graph topology.
   - **Missing graph predictors:** the panel retains natural, predictor-complete population cells; it does not provide predictors throughout the buffered all-cell propagation domain. It also does not retain `natural` as a dataframe column. Additional extraction is required.
   - **Geographic exclusion:** group exclusion must cover q fitting, feature selection, calibration and gate tuning. A gate-training score can indirectly depend on the evaluated group if its underlying q model was trained on that group. Use nested exclusions.
   - **Gate chronology:** for each issue date, beta/gamma tuning may use only fully observed earlier outcomes, accounting for the complete evaluation horizon.
   - **Blind geography:** deduplicate shared events and overlapping buffers. Never use blind future events to train q, including indirectly through the enlarged event collection.

   Historical burns from the prediction site may legitimately seed \(u\). Excluding its group from q training does not require discarding locally available history.

5. **There is a plausible source of gain, but no persuasive evidence yet for +0.01.**

   Boundary training might isolate transferable fuel or terrain information obscured by distant negatives. A correction could then distinguish cells with similar historical density, particularly through fuel recovery or barriers.

   But that is an argument for **incremental conditional information**, not for diffusion. The weak environmental results, pooled forest plus density rank at 0.604, and failed TMA-cell attempt are adverse evidence. They do not prove impossibility, but they make a gain speculative. Exact nesting guarantees an available baseline, not that tuning will select safely.

   **Fastest informative check:** cross-fit one modest boundary-trained score on development data, then insert it into a strongly penalised R1-offset model. Compare against R1 and the identically fitted correction trained on conventional cell labels. Use the corrected common G-A population and paired geographic uncertainty.

   If boundary-trained q cannot improve this simple correction, I would stop before implementing diffusion. A boundary AUC of 0.60 alone would not change that decision.

6. **EMS novelty: 2/5 now; potentially 3/5 with convincing independent predictive evidence.**

   The verified precedents materially narrow the claim:

   | Precedent | What I verified | Implication |
   |---|---|---|
   | **Holsinger, Parks & Miller (2016)** | Full author-hosted paper: matched fire-edge/core analysis of weather, fuels and topography. | Boundary-conditioned environmental analysis is established. [Paper](https://www.fs.usda.gov/rm/pubs_journals/2016/rmrs_2016_holsinger_l001.pdf) |
   | **Macauley, McLoughlin & Beverly (2022)** | Publisher abstract: matched case-control conditional logistic regression for perimeter formation and mapped spread potential; matching distance affected results. | Particularly close precedent for the learning rationale, although not verified as the exact outer-unburned-ring objective. [Publisher](https://www.sciencedirect.com/science/article/pii/S0378112721010513) |
   | **O’Connor, Calkin & Thompson (2017)** | Full paper: boosted-tree prediction of perimeter locations using landscape, fire-behaviour and suppression-access variables. | A related perimeter-learning precedent, **not accurately described as the same matched case-control design**. [Paper](https://www.fs.usda.gov/rm/pubs_journals/2017/rmrs_2017_oconnor_c002.pdf) |
   | **Grieshop & Wikle (2024)** | Publisher methods description: learned stochastic cellular automata with dynamic neighbourhoods and latent spatiotemporal effects. | Learning contagion and neighbour-dependent transitions is already established. [Publisher](https://www.sciencedirect.com/science/article/pii/S2211675323000696) |

   **Partially verified:** Barry & McIntyre (2011), DOI `10.1016/j.ecolmodel.2011.02.016`: bibliographic records confirm lattice density estimation with irregular boundaries and holes; I could not retrieve the primary paper. WF23055’s title, *An efficient, multi-scale neighbourhood index to quantify wildfire likelihood*, was found in an institutional repository result, but I could not retrieve its methods.

   I did **not** verify an exact precedent combining outer-ring training with learned-conductance diffusion of historical burns. That is not evidence of priority. The potentially distinctive contribution is the tested combination and its incremental value—not contagion, boundary learning or diffusion individually.

7. **A fifth attempt can be legitimate, but it is a disclosed reversal of the stopping rule.**

   Amendments 13.14 and 14.2 ended the search; 14.8 records failure. Handoff item 6 authorises one offset comparator. The propagation proposal exceeds that exception.

   Amendment 15 should preserve the original stopping result and record: the decision to reopen, all development evidence available, the new candidate budget, exact settings, selection rule and unconditional termination after this attempt. Add separate rows to `ANALYSIS_REGISTER.md`; do not retrospectively relabel development results confirmatory.

   **The blind test is not automatically invalidated.** Amendment 13.0 explicitly permits exploratory development before the single freeze. Its credibility depends on keeping blind outcomes inaccessible to every component and freezing one final procedure and primary comparison under 13.6.

   There is an additional distinction for these earlier blind fires: amendment 13.5 already calls this new-geography validation, not forward-in-time validation. If the method promises only pre-issue-date learning, the entire q and gate pipeline must honour that historical cutoff. Otherwise describe the test as retrospectively trained geographic transfer.

8. **Step 0’s criteria test the wrong quantities.**

   - **AUC 0.55:** arbitrary and disconnected from value beyond density. A strong boundary classifier can add nothing to R1; a weaker one can add useful complementary information.
   - **Lower bound above 0.5:** a transferable-signal check at best, not a development significance gate. Millions of cells must not substitute for independent events or regions. Five broad geographic groups also limit precision.
   - **R1 agreement within 0.002 AUC:** inadequate for “exactly.” Different maps can have identical AUC, and 0.002 is a material fraction of the proposed gain.
   - **100 ha support:** on these grids this can be only roughly five or six cells, latitude-dependent. Such events provide little interior and a boundary highly sensitive to registration.

   Replace them with ordered gates:

   1. **Data validity:** quantify valid boundary observations, clipping, event ambiguity, predictor coverage and actual independent-event support. Stop if a usable exposed-boundary interpretation cannot be supported.
   2. **Numerical validity:** test baseline equality on score arrays to floating-point tolerance where nesting is claimed; separately test mass, positivity, physical bandwidth and boundary behaviour.
   3. **Predictive value:** run the single paired R1-offset check in answer 5. Keep +0.01 as the already declared practical development threshold, with uncertainty reported as exploratory.
   4. **Robustness:** require that the apparent gain survive a small prespecified boundary-definition sensitivity and not depend on one region.
   5. **No expansion:** failure ends this exception; no revised rings, operators or grids selected after inspecting their gains.

   Freeze one primary endpoint. G-A/G-B/G-C should not become three alternative routes to declaring success.

9. **A better direction is a density-referenced decision procedure with an explicit abstention rule.**

   Use the agreed R1-offset comparator: historical density supplies the baseline, and a heavily shrunk environmental correction—especially time-since-burn interacting with density—must demonstrate value on earlier, geographically excluded transitions before being activated. Otherwise return R1. Evaluate whether that deployment-matched selection procedure reduces later-burning selection loss relative to within-event selection, using the diagnosis’s own loss framework from amendments 9–11. This directly targets the observed failure with available data and fewer identification assumptions. Its novelty would be modest, but a demonstrated reduction in decision error is more defensible than claiming to recover reach-conditional susceptibility from final scars.

Minimum changes to the plan, ranked:

1. **Implement and document the agreed 14.10 corrections first**, especially labels, observation support, complete horizons and physical R1 bandwidth.
2. **Run the already authorised offset comparator.** If reopening the search, permit only one additional boundary-trained correction check initially.
3. **Remove the claims that distant negatives are wrongly labelled, weather cancels, and the diagnosis is explained.** State the narrower boundary-discrimination hypothesis.
4. **Resolve event validity and missing graph data** before treating ring cells as exposure failures or proposing all-cell propagation.
5. **Replace T1 with common-target, paired incremental-value testing.** Keep ring discrimination descriptive.
6. **Make nesting numerical and explicit; defer diffusion** unless the cheap correction demonstrates useful signal.
7. **Record amendment 15 as a reversal**, with a fixed budget, one primary endpoint and a final stopping rule; preserve the untouched blind test and single freeze.