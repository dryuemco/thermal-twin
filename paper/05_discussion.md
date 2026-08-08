# 5. Discussion

> **Drafting note.** Every number in this section is taken from `04_results.md`; no value is
> re-derived from any other source. Citations resolve against `paper/REFERENCES.bib` and were
> restricted to keys already used in Sections 1–2. Interpretive claims that go beyond the literal
> statements of Section 4 are listed in the closing draft-notes block for coordinator review.

## 5.1 Principal findings

Across five Mediterranean fire regions, adding six pre-fire thermal predictors to a static
terrain-and-fuel baseline raised spatially blocked within-region ROC-AUC by +0.056 to +0.153, with
bootstrap support at every block size up to ~10 km (Section 4.2). The same models, applied across
regions without target labels, produced transfer AUCs of 0.326–0.686: six of twenty ordered
directions were *below* chance with interval support, and even the best direction fell 0.184 short
of its target's within-region reference (Section 4.3). Label-blind adaptation did not repair this;
it compressed the whole matrix towards chance (0.431–0.630), degrading every direction that had
transferred while recovering at most a third of the deficit where transfer had failed. Of twenty
candidate transferability diagnostics, the only two whose bootstrap intervals excluded zero were
conditional — computed from the *direction* of each predictor's association with burning in both
regions — while every marginal, niche-overlap and fire-regime measure failed to order the matrix
(Section 4.4). The pair with the highest burned-niche overlap failed in both directions; the pair
with the lowest transferred in both (Section 4.5). The trade-off is direct, not inferred: paired
per-direction, the thermal block that adds +0.056 to +0.153 AUC inside every region contributes
+0.004 on average to transfer — CI-supported positive in ten directions and CI-supported
negative in seven — and it is the swing factor at the chance line, dragging three directions
below chance and lifting one above it (Table R6). Dynamic state predictors buy local skill at
the cost of portability, and that cost is invisible to the diagnostics the field currently uses
to anticipate it.

## 5.2 Why the thermal increment is real but local

The within-region increment is not an artefact to be explained away. It replicates in five
independent regions, survives coarsening of the spatial blocks to ~10 km, persists in the
secondary all-valid population, and strengthens rather than weakens when the predictor window is
closed earlier (Section 4.7c). The transfer failure is therefore not evidence that the thermal
signal is spurious; it is evidence that the fitted relationship is *local*.

The mechanism is visible at the level of single predictors. In the taxonomy of Moreno-Torres et
al. [@MorenoTorres2012] this is concept shift: P(y|x) is locally reparameterised, so the same
predictor carries a different — in the sharpest case an opposite — relationship to burning in
different regions. Between Manavgat and Muğla, elevation discriminates burned cells in opposite
directions with disjoint intervals (signed AUC 0.374 vs 0.611), and all four channels describing
the absolute pre-fire thermal state reverse as well (e.g. `current_lst_mean` 0.538 vs 0.325). A
classifier trained on one side of such a reversal does not merely lose skill on the other side; it
inverts it, which is why raw transfer lands *below* chance with interval support in six
directions. Below-chance transfer is the signature that distinguishes concept shift from ordinary
covariate-shift degradation, which can only dilute skill towards 0.5.

Two refinements follow, both honest. First, in the Manavgat–Muğla pair the reversals concentrate
in the absolute channels, while the two channels referenced to a local baseline
(`lst_anomaly_mean`, `tvdi_difference_mean`) keep a common direction — consistent with
anomaly-referencing absorbing part of the between-region offset. But this protection is not
general: `lst_anomaly_mean` itself reverses with interval support between Bejís and Evia
(Section 4.6b), and TVDI — internally normalised by construction against scene-fitted wet and dry
edges [@Sandholt2002], the theoretical portability advantage flagged in Section 2.2 — reverses
alongside the raw LST channels. Statistical self-normalisation, whether within a scene (TVDI) or
against a climatology (LST anomaly), does not guarantee a stable direction of association. Second,
the reversal mechanism is not exclusive to the thermal block: the single sharpest supported
reversal belongs to elevation, a static predictor. The trade-off claim is about where the
within-region gain and the between-region loss co-locate — the thermal block — not a claim that
static predictors are immune to local reparameterisation.

## 5.3 Why every similarity-based diagnostic fails

Every diagnostic family that failed measures either where things burn or what the landscape looks
like; none measures which way the response points. Marginal predictor-space measures — the
area-of-applicability family [@Meyer2021; @Meyer2022; @Ludwig2023], climatic and geographic
distance — describe P(x). Burned-niche overlap (Schoener's D [@Schoener1968], Warren's I
[@Warren2008], burned-centroid Mahalanobis distance) describes P(x|y=1). Fire-regime structure describes the spatial pattern of P(y).
All are computable without target labels, and all are blind to the quantity that failed here: the
sign of the conditional association.

The domain classifier makes the blind spot concrete. Source and target cells are separable at AUC
0.962–0.9999 for every pair — marginal shift is essentially total everywhere — so a marginal
instrument is at ceiling and cannot discriminate transfer outcomes that range from 0.33 to 0.69.
The contrast pair makes it vivid: Manavgat and Muğla have the most similar burned envelopes of any
pair in the matrix (mean Schoener's D 0.826, closest burned centroids) and fail in both directions
with interval support, while Bejís and Montiferru have the least similar envelopes (D 0.479,
farthest centroids) and transfer in both directions. Where the envelope agrees but the direction
reverses, transfer fails; where the envelope disagrees but the direction agrees, transfer works.
At pair level the two quantities are empirically distinct, and in partial rank correlations the
conditional index retains its association with transfer when niche overlap is held fixed (+0.82)
while niche overlap retains none in the reverse conditioning (−0.07).

This offers a measurable operationalisation of a concept the species-distribution-modelling
transferability literature has discussed as "ecological stationarity" [@Yates2018]: on this
evidence, the stationarity that transfer requires is *direction agreement in P(y|x)*, not overlap
of environmental envelopes. It is also consistent with the SDM findings that environmental and
geographic similarity do not predict transfer success [@Vesk2021; @Rousseau2022], now reproduced
in a fire application with interval support on both halves of a counterexample pair. None of this
is a criticism of the area-of-applicability construction, which does what it claims for the
extrapolation failure mode it was designed for; it is a demonstration that a reassuring marginal
diagnostic is not evidence of portability when the predictors are dynamic state variables.

## 5.4 What the conditional diagnostic is — and is not

The constructive result must be stated with its limits attached. The conditional index — the
fraction of CI-supported features whose signed univariate association points the same way in
source and target — is the only diagnostic in the programme whose bootstrap interval excludes
zero (ρ = +0.84 [+0.58, +0.88]; cosine variant +0.81 [+0.33, +0.88]).

It is **not label-free**. Signed associations require burned labels in *both* regions; as a
pre-transfer instrument it therefore requires either an existing burned-area record or a labelled
probe in the target. The marginal diagnostics it outperforms are all label-free, so the comparison
is not like-for-like as an operational tool. The defensible claim is mechanistic: *the failure
that is invisible to marginal diagnostics is visible in the conditional structure* — not that we
possess a deployable label-free predictor of transfer.

It is also coarse. The supported-feature restriction that gives the index its discrimination
leaves six of eight pairs with denominators of one or two features, and the two Montiferru pairs
drop out entirely — not because Montiferru lacks supported features (it has three) but because
its supported set does not intersect its partner's; the exclusion arises from set-disjointness
between the two regions' supported features, which is the more precise and more defensible
statement of the coverage limit. The index is close to a binary flag for "any supported sign
disagreement". And the power caveat of Section 4.4 applies to *every* correlation
in the diagnostic table, including the two successes: the effective sample is ten unordered pairs,
the two directions of a pair are not independent, and intervals of width ±0.5–0.8 on the null
rows cannot rule out moderate true correlations. The null diagnostics are "not shown to order
transfer", not "shown not to"; the conditional result is a strong ordering on a small pair set,
not an established general law.

## 5.5 Interventions, and the conservation pattern that runs through them

Every intervention tested obeys the same accounting: what transfer gains, something else pays for.

Label-blind adaptation compresses rather than repairs. Region-wise standardisation and CORAL
[@Sun2016] raise the failing directions part-way towards chance and pull the working directions
down towards it; seven of twelve decomposed directions show *negative* recovery, the worst
(Evia→Manavgat) recovering −0.86 of the gap. This is what Section 2.4 predicted as a property of
the methods: transformations defined on marginal statistics cannot restore a conditional
relationship, and where the relationship has reversed they deliver better-aligned inputs to a
decision rule fitted under the opposite one.

Pooled multi-region training does not escape the problem by averaging over it. The
leave-one-region-out pooled thermal model never beats the best single-source pairwise transfer
(shortfalls 0.02–0.22), sits 0.22–0.50 below the within-region ceiling, and for three of five
targets is matched or beaten raw by the pooled *static* baseline — the pooled model resolves
conflicting thermal directions by, in effect, discounting the block that carries them.

Feature removal is zero-sum, but its geometry confirms the diagnosis. Dropping the two supported
reversal features buys +0.014 mean transfer AUC for −0.081 mean within-region AUC, and the gains
land exactly where the reversal analysis points: the three interval-supported gains all involve
the reversal partners, the mean delta over Manavgat-involved directions is +0.025 against −0.009
elsewhere, and `lst_anomaly` removal contributes only in the one pair where it reverses with
support. Knowing *which* features to drop for *which* pair, however, requires the target's signed
directions — that is, target labels; applied label-free, the same removal degrades the five
aligned directions. The consistent lesson is the one the adaptation literature reached once the
conditional component was recognised as binding [@Tuia2016; @Persello2012]: a small number of
target labels is the resource that label-free machinery cannot substitute for. A supervised
few-shot recalibration analysis exists in the project diagnostics and is intended for the
supplementary material [TO VERIFY: supplementary inclusion decision]; it is not drawn on here.

## 5.6 The pre-registered regime hypothesis, reported as it happened

Section 2.5 offered fire-regime typology [@Archibald2013] as a candidate explanation for the
concept shift — the idea that regions in different limiting regimes should map dryness to burning
differently. Before the Evia-extended results were computed we pre-registered the expectation that
fire-regime distance would *not* predict transfer. The data confirmed the null, and in a way that
exposes the intuition behind the hypothesis as wrong, which we report plainly rather than as
vindication. The regime-distance point estimate has the wrong sign (ρ = +0.29): the most
regime-similar pair in the set — Bejís and Evia-extended, with effective burned-component counts
of 1.0000 and 1.0083, as close to identical regime structure as the data allow — fails in both
directions with interval support, while the most regime-different pair (Bejís–Muğla) transfers
above chance. The error was in the hypothesised grouping — the assumption that Bejís's
single-compact-burn structure placed it in a regime class whose members would behave alike — not
in the data. With ten pairs this cannot refute regime typology as an explanation of concept
shift in general, but our data offer it no support in its distance-based form, and the candidate
explanation floated in Section 2.5 should be read accordingly.

## 5.7 The pre-fire signal is not an early-fire artefact

The most direct threat to everything above is the possibility that the "pre-fire" thermal
composite is contaminated by early fire signal, since each region's predictor window closes one
day before its label window opens. The window-closure sensitivity (Section 4.7c) addresses this
head-on: shifting both ends of the predictor window 7 and 14 days earlier — so that the composite
ends one and two weeks before any labelled burning — leaves the thermal increment
bootstrap-supported in every region and every variant. Nowhere does the increment shrink towards
zero. The within-region signal is therefore a genuine pre-fire dryness signal, not a leakage of
the fire itself into the predictors.

One observation from this analysis must be reported even though we cannot explain it: in Manavgat
and Bejís the increment *increases* with earlier closure (0.074 → 0.101 and 0.094; 0.058 → 0.077
and 0.079). This is unexpected in direction: contamination by early fire signal would predict the
opposite. We do not know why the increment increases and we do not speculate; we note only that
the direction of the effect is the safe one for the validity of the pre-fire claim.

## 5.8 The empirical contrast with Dimarco et al. (2026)

Dimarco et al. [@Dimarco2026] and this study form a near-controlled contrast conducted by two
independent groups: Mediterranean regions, ~500 m cells, MCD64A1-derived targets, tree ensembles,
spatially aware validation, an explicit ordered-pair transfer matrix. Their predictors are
spatially stationary attributes of place — terrain, human modification, night-time lights,
population density, ERA5-Land long-term climatologies — and every transfer they report exceeds
AUC 0.80. Our predictors describe the dynamic state of a particular pre-fire window, and transfer
collapses to chance or below. Read together, the two studies bracket the predictor-class
explanation: stationary-attribute models learn a spatial ordering of susceptibility that a
neighbouring region can inherit; dynamic-state models additionally encode how a given degree of
anomalous dryness translates into burning *there, then* — and that mapping is what fails to
travel. WildfireGenome's county-level matrix [@Liu2025], with its mixture of strong and collapsed
transfers, sits between the two poles.

The contrast must not be overdrawn, and the bounding differences are stated in Section 2.5:
their target is an ignition proxy evaluated against a 1:1 balanced background, ours is
burned-area classification at the true, heavily imbalanced base rate — different problems with
different achievable ceilings; their temperature variable is a static reanalysis climatology,
ours are event-specific satellite observations referenced to their own baselines; they apply no
adaptation, whereas adaptation is central to our diagnosis. The comparison is between two
coherent experimental programmes, not an ablation. What it supports is precisely the thesis-level
reading: portability tracks predictor class, and the class that carries the within-region gain is
the class that fails to port.

## 5.9 Implications

For practice, the immediate implication concerns regional and "global" fire-susceptibility
products. A within-region AUC — even a spatially blocked, honestly computed one — prices only
half of a predictor block's contribution; the portability it consumes appears on no ledger unless
transfer is measured. Our results say that for dynamic thermal predictors this cost can be total,
and that neither predictor-space applicability screening [@Meyer2021; @Ludwig2023] nor label-free
alignment will reveal or repair it. Transferability must be measured, not assumed from regional,
climatic or regime similarity — and the measurement itself is sensitive to evaluation design
[@Xu2026], down to the library version (Section 4.7e).

For method development, the results point to two resources. The first is labels: the conditional
diagnostic requires a labelled probe in the target, and the interventions of Section 4.6 show
that knowing where the reversals are — knowledge only target labels provide — is what converts
the diagnosis into an action. The second is predictors normalised physically rather than
statistically: TVDI's scene-internal normalisation and the climatological anomaly referencing
both failed to guarantee stable direction, suggesting that portability requires variables whose
mapping to fire-relevant state (for example, actual fuel moisture rather than its thermal proxy
[@Yebra2013; @Marino2024]) is invariant by construction rather than by rescaling. The
self-calibrating satellite thermal digital twin that motivated this project remains future work,
and on this evidence its calibration loop will need labelled feedback, not unsupervised
alignment.

## 5.10 Limitations

The transfer failure is a finding, not a limitation; the limitations are the boundaries on how
far it generalises. (i) No meteorological covariates (wind, humidity, precipitation) enter the
models, so we cannot say how the trade-off behaves for a mixed thermal-plus-weather predictor
set. (ii) Temporal transfer — the same region in a different fire year — is untested; a Muğla
2022 analysis is in progress and no results are available. (iii) All labels derive from a single
burned-area product, MCD64A1 [@Giglio2018], whose omission and commission characteristics
[@Boschetti2019] bound every model evaluated here. (iv) The ~510 m analysis cells approximate,
but are not co-registered with, the native MODIS sinusoidal grid (Section 3.2). (v) Even after
the AOI extension, Evia's TSG prevalence (0.287) remains the highest of the five regions — four
to seven times that of Manavgat, Bejís and Muğla (0.038–0.072), though only marginally above
Montiferru (0.225); prevalence sensitivity was checked for transfer (Section 4.7a) but Evia
remains the most imbalance-atypical population. (vi) Each region contributes one fire season, so regional concept
shift is confounded with event meteorology; distinguishing them requires multi-year labels.
(vii) Cross-region point estimates carry an implementation tolerance of roughly ±0.02–0.03 across
scikit-learn versions (Section 4.7e); all reported numbers are fixed to one verified version, but
exact reproduction elsewhere requires the archived environment. (viii) The diagnostic
correlations rest on an effective sample of ten region pairs; both the successes and the failures
of Section 4.4 should be read at that power.

<!-- DRAFT NOTES:

(a) [TO VERIFY] / [CITATION NEEDED] items:
    1. §5.3 — RESOLVED 2026-08-08: @Schoener1968 (Ecology 49(4):704-726, doi 10.2307/1935534)
       and @Warren2008 (Evolution 62(11):2868-2883, doi 10.1111/j.1558-5646.2008.00482.x) both
       verified via Crossref REST API and added to REFERENCES.bib (Block G); inline citation
       placed in §5.3.
    2. §5.5 — the sentence "A supervised few-shot recalibration analysis is reported in the
       supplementary material" is a POINTER ONLY: few-shot appears nowhere in 04_results.md.
       Coordinator must either (a) confirm the few-shot analysis (drive_new/diagnostics/
       few_shot_recovery, unread in detail per memory) will actually appear in supplementary, or
       (b) delete the sentence. No few-shot numbers were introduced.
    3. §5.10(ii) — "Muğla 2022 analysis is in progress" is a placeholder carried from the task
       brief; verify status before submission.
    4. §5.10(iv) — "~510 m cells approximate but are not co-registered with the MODIS sinusoidal
       grid" traces to 03_methods.md lines 55-64, not to 04; wording should be checked against
       the final §3.2.

(b) Interpretation beyond the literal statements of 04 (flag for coordinator review):
    1. §5.2 — "Below-chance transfer is the signature that distinguishes concept shift from
       ordinary covariate-shift degradation, which can only dilute skill towards 0.5." 04 shows
       below-chance transfers and reversals; the "signature/dilution" logic is an interpretive
       gloss (consistent with 02 §2.4's method-property argument).
    2. §5.2 — "anomaly-referenced channels keep a common direction in Manavgat-Muğla" is read
       from figure_contrast_pairs.csv (lst_anomaly 0.482/0.485; tvdi_difference 0.449/0.490,
       both sign-agreeing), which 04 §4.5 references but does not spell out per feature beyond
       "all four absolute thermal channels" reversing. The generalisation "consistent with
       anomaly-referencing absorbing part of the offset" is interpretation.
    3. §5.2 — grouping current_tvdi_mean among "channels describing the absolute pre-fire
       thermal state" follows 04 §4.5's phrase "all four absolute thermal channels"; the
       TVDI-normalisation-does-not-protect claim rests on current_tvdi reversing in that pair
       (figure_contrast_pairs.csv: 0.552 vs 0.336). Point reversal only, not CI-supported under
       the both-exclude-0.5 criterion — the text says "reverses alongside the raw LST channels"
       without claiming CI support; check this reads as intended.
    4. §5.5 — "the pooled model resolves conflicting thermal directions by, in effect,
       discounting the block that carries them" is a mechanism conjecture; 04 §4.6a reports only
       that the pooled baseline matches/beats pooled thermal for 3 of 5 targets.
    5. §5.6 — "the error was in the hypothesised grouping ... not in the data" follows the task
       brief's framing; the pre-registration record (regime_transfer_correlation.md) registered
       the null expectation citing the Bejís-Evia observation. Coordinator should confirm the
       narrative sequence (what was expected when) is stated accurately from the lab record.
    6. §5.7 — "the direction of the effect is the safe one for the validity of the pre-fire
       claim" is a mild interpretive addition to the observation-only rule; delete if it reads
       as speculation.
    7. §5.8 — "near-controlled contrast conducted by two independent groups" and the
       "bracket the predictor-class explanation" reading extend 02 §2.5's vetted framing; no new
       numbers.
    8. §5.9 — "its calibration loop will need labelled feedback, not unsupervised alignment" is
       an inference from C2/C4; kept to one sentence per POSITIONING (digital twin as future
       work only).

(c) Forward references from 01/02 closed here:
    CLOSED:
    - 01 §1.2 / 02 §2.2: TVDI's "theoretical portability advantage this study tests empirically"
      → closed negatively in §5.2 (internal normalisation does not protect direction).
    - 01 §1.3 / 02 §2.3: "a model may sit well inside its nominal area of applicability and
      still perform at or below chance" → closed in §5.3 via the domain-classifier ceiling and
      the Manavgat-Muğla contrast (highest envelope overlap, closest centroids, below-chance
      both directions). NOTE: 04 does not report a per-pair "fraction inside AoA" for
      Manavgat-Muğla specifically; the closure rests on overlap/Mahalanobis + the failed
      ordering of the AoA-fraction diagnostic. If a reviewer demands the literal AoA-inside
      number for that pair, it must come from Emrehan's AoA table [TO VERIFY].
    - 01 §1.4 Q1-Q4: Q1 answered in §5.1-5.2 (trade-off), Q2 in §5.3 (sufficiency
      counterexample), Q3 in §5.5 (compression, negative recovery), Q4 in §5.3-5.4 (marginal
      fail, conditional orders). NOTE on Q1 — RESOLVED 2026-08-08: the per-direction paired
      baseline-vs-thermal transfer contrast now exists (paper/baseline_vs_thermal_transfer.*,
      read-only extraction from frozen step9b/step9c; Table R6 in 04 §4.3) and §5.1 was
      sharpened to state the trade-off directly (+0.004 mean transfer contribution, 10 positive
      / 7 negative CI-supported directions, swing at the chance line).
    - 02 §2.4: "what remains genuinely empirical is how large the irreparable part is" → closed
      in §5.5 (compression, 7/12 negative recovery).
    - 02 §2.5: regime typology "offered as candidate explanation, not tested" → closed honestly
      in §5.6 (pre-registered null confirmed; grouping intuition wrong).
    - 02 §2.5 / OUTLINE §1.5: the Dimarco contrast → §5.8 with all three bounding differences.
    STILL OPEN (not closable in Discussion):
    - 01 §1.5 contribution-claim placeholders still read "pending results" — must be filled at
      assembly from 04.
    - RESOLVED 2026-08-08: the 11 METHODS GAPS are closed (03_methods §3.14–§3.16 + §3.1
      Table 1 update); §5.7 now rests on §3.16.3 and §5.10(iv) on §3.2's existing text.
    - Few-shot supplementary (item a2) — decision pending.

  Style: British English (-ise/-our), matching 01-04. Prose word count excluding this comment
  and the drafting note: ~2,450.

COORDINATOR REVIEW (2026-08-08), changes applied after drafting:
    1. §5.7 — recency-of-information clause removed (borderline mechanism speculation); the
       contamination-direction logic and the "safe direction" validity remark retained.
    2. §5.5 — few-shot supplementary pointer now carries an inline [TO VERIFY] (inclusion
       decision pending); no numbers introduced.
    3. §5.10(v) — "two to four times (0.038–0.225)" was numerically wrong (0.287/0.038 ≈ 7.6);
       corrected to 4–7× vs Manavgat/Bejís/Muğla, marginally above Montiferru.
    4. All 19 citation keys used here verified present in 01/02/03/LITERATURE/REFERENCES.bib;
       the single [CITATION NEEDED] (Schoener 1968; Warren et al. 2008) stands and must be
       Crossref-verified before entering REFERENCES.bib.
    5. Cross-checked every number against 04_results.md (post-fix version incl. the 0.630
       adapted maximum and the six-of-seven negative-recovery wording): consistent.
    6. Related: 03_methods §3.11 CORAL-λ sweep paragraph was amended this round to actual
       drive_new coverage (see 04's DRAFT NOTES conflict 3) — re-check in the Methods round.
    7. Correction (figure round, 2026-08-08): the Montiferru-pair exclusion from the
       supported index is SET-DISJOINTNESS of the two regions' supported features, not an
       empty Montiferru set (it has three: slope, current TVDI, TVDI difference). §5.4 here,
       04 §4.5/Table R2 and conditional_similarity_transfer.md all corrected; Fig. 7 shows it
       via filled-vs-open arrowheads.
-->
