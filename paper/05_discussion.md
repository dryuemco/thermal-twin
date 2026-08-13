# 5. Discussion

> **Drafting note.** Every number in this section is taken from `04_results.md`; no value is
> re-derived from any other source. Citations resolve against `paper/REFERENCES.bib` and were
> restricted to keys already used in Sections 1–2. Interpretive claims that go beyond the literal
> statements of Section 4 are listed in the closing draft-notes block for coordinator review.

## 5.1 Principal findings

Across five Mediterranean fire regions, six pre-fire thermal predictors were added to a static
terrain-and-fuel baseline. Spatially blocked within-region ROC-AUC was raised by +0.056 to +0.153,
with bootstrap support at every block size up to ~10 km (Section 4.2). The same models were then
applied across regions without target labels. Transfer AUCs ran from 0.326 to 0.686. Six of twenty
ordered directions were *below* chance with interval support, and even the best direction fell 0.184
short of its target's within-region reference (Section 4.3).

Label-blind adaptation did not repair this. It compressed the whole matrix towards chance, to a
range of 0.431 to 0.630. Every direction that had transferred was degraded, and at most a third of
the deficit was recovered where transfer had failed.

Of twenty candidate transferability diagnostics, only two had bootstrap intervals that excluded
zero, and both were conditional. They are computed from the *direction* of each predictor's
association with burning in both regions. Every marginal, niche-overlap and fire-regime measure
failed to order the matrix (Section 4.4). The pair with the highest burned-niche overlap failed in
both directions, while the pair with the lowest overlap transferred in both (Section 4.5).

The trade-off is direct rather than inferred. Paired per direction, the thermal block that adds
+0.056 to +0.153 AUC inside every region contributes +0.004 on average to transfer. It is
CI-supported positive in ten directions and CI-supported negative in seven. It is also the swing
factor at the chance line, dragging three directions below chance and lifting one above it (Table
R6). Dynamic state predictors buy local skill at the cost of portability, and that cost is invisible
to the diagnostics the field currently uses to anticipate it.

## 5.2 Why the thermal increment is real but local

The within-region increment is not an artefact to be explained away. It replicates in five
independent regions. It survives coarsening of the spatial blocks to ~10 km. It persists in the
secondary all-valid population. It also strengthens rather than weakens when the predictor window is
closed earlier (Section 4.7c). The transfer failure is therefore not evidence that the thermal
signal is spurious. It is evidence that the fitted relationship is *local*.

The mechanism is visible at the level of single predictors. In the taxonomy of Moreno-Torres et al.
[@MorenoTorres2012] this is concept shift. P(y|x) is locally reparameterised, so the same predictor
carries a different relationship to burning in different regions, and in the sharpest case an
opposite one. Between Manavgat and Muğla, elevation discriminates burned cells in opposite
directions with disjoint intervals (signed AUC 0.374 vs 0.611). All four channels describing the
absolute pre-fire thermal state reverse as well, for example `current_lst_mean` at 0.538 vs 0.325. A
classifier trained on one side of such a reversal does not merely lose skill on the other side. It
inverts it. That is why raw transfer lands *below* chance with interval support in six directions.
Below-chance transfer is the signature that distinguishes concept shift from ordinary
covariate-shift degradation, which can only dilute skill towards 0.5.

Two refinements follow, and both are honest. First, in the Manavgat-Muğla pair the reversals
concentrate in the absolute channels. The two channels referenced to a local baseline,
`lst_anomaly_mean` and `tvdi_difference_mean`, keep a common direction. That is consistent with
anomaly-referencing absorbing part of the between-region offset. The protection is not general,
however. `lst_anomaly_mean` itself reverses with interval support between Bejís and Evia (Section
4.6b). TVDI reverses alongside the raw LST channels, even though it is internally normalised by
construction against scene-fitted wet and dry edges [@Sandholt2002]. That was the theoretical
portability advantage flagged in Section 2.2. Statistical self-normalisation does not guarantee a
stable direction of association, whether it is done within a scene (TVDI) or against a climatology
(LST anomaly).

Second, the reversal mechanism is not exclusive to the thermal block. The single sharpest supported
reversal belongs to elevation, a static predictor. The trade-off claim is about where the
within-region gain and the between-region loss co-locate, which is the thermal block. It is not a
claim that static predictors are immune to local reparameterisation.

There is an obvious objection to all of this, and it has to be met rather than deflected. Every
reversal cited so far is measured between *different places*. A sceptic can reasonably reply that
the relationship was never one relationship. Manavgat and Muğla are distinct landscapes with
distinct fuels, terrain and fire histories. On that reading, a predictor that means one thing in one
region and another thing in the other is not evidence of instability. It is evidence that two
different systems were compared.

The two Muğla events answer this directly (Section 4.8). Region, AOI, analysis grid, feature
registry and processing chain are identical, and only the fire differs. Elevation's association with
burning nevertheless reverses with bootstrap support. It is 0.611 [0.532, 0.690] in 2021, where
higher ground burned preferentially, against 0.296 [0.230, 0.355] in 2022, where lower ground did.
The intervals are disjoint and the difference is −0.317 [−0.414, −0.220]. Holding geography fixed
does not stabilise the direction of the relationship.

The mechanism is unusually visible here, and it is physical rather than statistical. The 2021 season
burned as a dispersed complex of ten components across the region's full relief, from near sea level
to 1,975 m. The 2022 event was a single compact scar confined below 777 m, with a median burned
elevation of 187 m against 563 m the year before. The effective component count falls from 4.05 to
1.34, and the observed land-cover classes from seven to two. The two fires simply occupied different
parts of the same elevation gradient. A model that learned "high ground burns" from the first would
be actively wrong about the second. This is what concept shift looks like when it can be seen. It is
not a subtle distributional drift. It is two events sampling opposite ends of a topographic range
that the region contains in full.

Two constraints limit how far this carries. First, the design is same-geography event-to-event and
not clean temporal transfer. The 2022 fire ignites about five weeks earlier in the season, so year
and seasonal phase are confounded and the difference cannot be attributed to elapsed time (Section
3.16.4). What the design does isolate is geography, which is precisely the variable the objection
rests on. Second, only elevation reverses with interval support. The four absolute thermal channels
move from bootstrap-supported *lower*-values-burn to *higher*-values-burn point estimates, and each
shift is itself interval-supported. With 331 burned cells in 2022, however, every one of those
intervals straddles 0.5. The 2022 direction is therefore not established, and the thermal reversals
are not claimed as supported (Section 4.8).

Transfer between the two events completes the picture and sharpens the trade-off rather than
softening it. With geography fixed, transfer no longer collapses. Both directions stay above chance,
where six of twenty between-region directions fell below it. The thermal block's contribution
nevertheless *changes sign*. It is −0.082 [−0.127, −0.040] carrying 2021 forward to 2022, and +0.089
[+0.072, +0.104] carrying 2022 back to 2021. Both signs are interval-supported, even though the same
block is locally informative within each event separately (+0.116 in 2021, +0.078 in 2022). This is
the trade-off at its most explicit. The six predictors that buy local skill in both events are not
merely unhelpful across them; in one direction they subtract from a static baseline that would
otherwise have transferred at 0.642. Whether a dynamic-state block helps or harms on transfer is a
property of the source-target pair, not of the block.

That elevation is the one supported reversal is itself worth noting, because it is the second time
the same predictor has played this role: elevation also carries the sharpest bootstrap-supported
reversal in the Manavgat-Muğla pair (signed AUC 0.374 against 0.611). Across a between-region
contrast and a within-region between-event contrast, the predictor that most reliably fails to keep
its direction is a static, perfectly measured, physically unambiguous one. Elevation does not drift
between regions and carries no sensor or compositing artefact; what changes is which part of the
gradient a given fire occupies. This sharpens the diagnosis in a way that runs against the paper's
own emphasis: the portability problem is not a property of thermal predictors specifically, nor of
noisy remote-sensing channels, but of the mapping from any landscape variable to burning. The
thermal block is where the trade-off is *costly*, because that is where the within-region gain sits;
it is not where instability is *worst*.

## 5.3 Why every similarity-based diagnostic fails

Every diagnostic family that failed measures either where things burn or what the landscape looks
like. None measures which way the response points. Marginal predictor-space measures describe P(x).
These are the area-of-applicability family [@Meyer2021; @Meyer2022; @Ludwig2023] together with
climatic and geographic distance. Burned-niche overlap describes P(x|y=1), through Schoener's D
[@Schoener1968], Warren's I [@Warren2008] and burned-centroid Mahalanobis distance. Fire-regime
structure describes the spatial pattern of P(y). All are computable without target labels, and all
are blind to the quantity that failed here, which is the sign of the conditional association.

The domain classifier makes the blind spot concrete. Source and target cells are separable at AUC
0.962 to 0.9999 for every pair, so marginal shift is essentially total everywhere. A marginal
instrument is therefore at ceiling and cannot discriminate transfer outcomes that range from 0.33 to
0.69. The contrast pair makes this vivid. Manavgat and Muğla have the most similar burned envelopes
of any pair in the matrix (mean Schoener's D 0.826, closest burned centroids), and they fail in both
directions with interval support. Bejís and Montiferru have the least similar envelopes (D 0.479,
farthest centroids), and they transfer in both directions. Where the envelope agrees but the
direction reverses, transfer fails. Where the envelope disagrees but the direction agrees, transfer
works. At pair level the two quantities are empirically distinct, and in partial rank correlations
the conditional index retains its association with transfer when niche overlap is held fixed (+0.82)
while niche overlap retains none in the reverse conditioning (−0.07).

This offers a measurable operationalisation of a concept the species-distribution-modelling
transferability literature has discussed as "ecological stationarity" [@Yates2018]: on this
evidence, the stationarity that transfer requires is *direction agreement in P(y|x)*, not overlap of
environmental envelopes. It is also consistent with the SDM findings that environmental and
geographic similarity do not predict transfer success [@Vesk2021; @Rousseau2022], now reproduced in
a fire application with interval support on both halves of a counterexample pair. None of this is a
criticism of the area-of-applicability construction, which does what it claims for the extrapolation
failure mode it was designed for. It is a demonstration that a reassuring marginal diagnostic is not
evidence of portability when the predictors are dynamic state variables.

## 5.4 What the conditional diagnostic is, and what it is not

The constructive result must be stated with its limits attached. The conditional index is the
fraction of CI-supported features whose signed univariate association points the same way in source
and target. It is the only diagnostic in the programme whose bootstrap interval excludes zero (ρ =
+0.84 [+0.58, +0.88]; cosine variant +0.81 [+0.33, +0.88]).

It is **not label-free**. Signed associations require burned labels in *both* regions. As a
pre-transfer instrument it therefore requires either an existing burned-area record or a labelled
probe in the target. The marginal diagnostics it outperforms are all label-free, so the comparison
is not like-for-like as an operational tool. The defensible claim is mechanistic: *the failure that
is invisible to marginal diagnostics is visible in the conditional structure*. The claim is not that
a deployable label-free predictor of transfer has been found.

It is also coarse. The supported-feature restriction that gives the index its discrimination leaves
six of eight pairs with denominators of one or two features, and the two Montiferru pairs drop out
entirely. That is not because Montiferru lacks supported features, since it has three. It is because
its supported set does not intersect its partner's. The exclusion arises from set-disjointness
between the two regions' supported features, which is the more precise and more defensible statement
of the coverage limit. The index is close to a binary flag for "any supported sign disagreement".
The power caveat of Section 4.4 also applies to *every* correlation in the diagnostic table,
including the two successes: the effective sample is ten unordered pairs, the two directions of a
pair are not independent, and intervals of width ±0.5 to 0.8 on the null rows cannot rule out
moderate true correlations. The null diagnostics are "not shown to order transfer", not "shown not
to". The conditional result is a strong ordering on a small pair set, not an established general
law.

## 5.5 Interventions, and the conservation pattern that runs through them

Every intervention tested obeys the same accounting: what transfer gains, something else pays for.

Label-blind adaptation compresses rather than repairs. Region-wise standardisation and CORAL
[@Sun2016] raise the failing directions part-way towards chance and pull the working directions down
towards it; seven of twelve decomposed directions show *negative* recovery, the worst
(Evia→Manavgat) recovering −0.86 of the gap. This is what Section 2.4 predicted as a property of the
methods: transformations defined on marginal statistics cannot restore a conditional relationship,
and where the relationship has reversed they deliver better-aligned inputs to a decision rule fitted
under the opposite one.

Pooled multi-region training does not escape the problem by averaging over it. The
leave-one-region-out pooled thermal model never beats the best single-source pairwise transfer, with
shortfalls of 0.02 to 0.22. It sits 0.22 to 0.50 below the within-region ceiling. For three of five
targets it is matched or beaten raw by the pooled *static* baseline. In effect, the pooled model
resolves conflicting thermal directions by discounting the block that carries them.

Feature removal is zero-sum, but its geometry confirms the diagnosis. Dropping the two supported
reversal features buys +0.014 mean transfer AUC for −0.081 mean within-region AUC. The gains land
exactly where the reversal analysis points. All three interval-supported gains involve the reversal
partners. The mean delta over Manavgat-involved directions is +0.025 against −0.009 elsewhere.
Removal of `lst_anomaly` contributes only in the one pair where it reverses with support. Knowing
*which* features to drop for *which* pair, however, requires the target's signed directions, that is
to say target labels. Applied label-free, the same removal degrades the five aligned directions. The
consistent lesson is the one the adaptation literature reached once the conditional component was
recognised as binding [@Tuia2016; @Persello2012]: a small number of target labels is the resource
that label-free machinery cannot substitute for. A supervised few-shot recalibration analysis exists
in the project diagnostics and is reported in the supplementary material (Supplementary S1). It is
not drawn on here.

## 5.6 The pre-registered regime hypothesis, reported as it happened

Section 2.5 offered fire-regime typology [@Archibald2013] as a candidate explanation for the concept
shift. The idea was that regions in different limiting regimes should map dryness to burning
differently. Before the Evia-extended results were computed, we pre-registered the expectation that
fire-regime distance would *not* predict transfer. The data confirmed the null. They did so in a way
that exposes the intuition behind the hypothesis as wrong, and that is reported plainly rather than
as vindication. The regime-distance point estimate has the wrong sign (ρ = +0.29). The most
regime-similar pair in the set is Bejís and Evia-extended, with effective burned-component counts of
1.0000 and 1.0083, which is as close to identical regime structure as the data allow. That pair
fails in both directions with interval support. The most regime-different pair, Bejís-Muğla,
transfers above chance. The error was in the hypothesised grouping, not in the data. It was the
assumption that Bejís's single-compact-burn structure placed it in a regime class whose members
would behave alike. With ten pairs this cannot refute regime typology as an explanation of concept
shift in general, but our data offer it no support in its distance-based form, and the candidate
explanation floated in Section 2.5 should be read accordingly.

## 5.7 The meteorological-extremity explanation, tested and not supported

Manavgat is the region whose behaviour most resists the account given above. It supplies the
reversal partner in the sharpest contrast pair (Section 5.2), it is where feature removal buys
almost all of its transfer gain (+0.025 mean delta over Manavgat-involved directions against −0.009
elsewhere, Section 5.5), and it is the target of the worst negative recovery under adaptation
(Evia→Manavgat, −0.86 of the gap). The most natural post hoc explanation is meteorological: that
Manavgat 2021 was an exceptionally extreme fire season, so that its thermal predictors were driven
by a regional weather anomaly the other regions did not share, and the resulting mapping from
dryness to burning was correspondingly idiosyncratic.

We tested that explanation and it was not supported. The ERA5-Land regional diagnostic (Sections
3.17, 4.9) characterises each region's predictor window against its own 2017 to 2020 climatology,
and Manavgat is not the meteorologically extreme member of the set. Its predictor-window temperature
sits 0.06 °C *below* its climatological mean, while the other four regions run 0.31 to 1.11 °C warm.
It is the only region at or below its own baseline, and the departure is small enough that the
honest reading is simply that Manavgat burned under climatologically ordinary temperatures. Its
humidity deficit of 3.24 % is mid-range among the five, its wind departure of +0.07 m s⁻¹ is the
second smallest, and its precipitation total is within 1.4 mm of climatology, the smallest
precipitation departure in the set. On none of the four variables is Manavgat the extreme member; on
two it is the least anomalous. Whatever makes its transfer behaviour atypical, regional
meteorological extremity in the predictor window is not it.

We report this as a failed prediction rather than as a result, and it carries the same status as the
pre-registered regime null of Section 5.6: a stated expectation, tested, and not borne out. The two
failures are informative in the same limited way. They remove candidate explanations without
supplying one.

The reader may reasonably ask why meteorology, once measured, is not simply added to the diagnostic
set of Section 4.4 as a ninth measure of region similarity. It is not added because the candidate
set was fixed before any diagnostic-versus-transfer correlation was computed. Eight measures were
specified and eight failed to order the transfer matrix; appending a ninth after seeing those eight
fail would be a search over the diagnostic space, and any correlation it returned on ten pairs would
be uninterpretable. The measurement is reported for what it is, namely a descriptive
characterisation of the regions and a test of one specific explanation. It is kept out of the
ordering analysis by construction.

Two cautions attach to the reading of Section 4.9, and they are the reason it reports physical units
rather than standardised ones. The first concerns the climatology. It spans four years, and the
standard deviations it yields differ between regions by factors of 2.7 to 6.0 in the predictor
windows, so a standardised anomaly measures a different physical departure in each region and
invites a cross-region comparison that the quantity cannot support (Section 3.17). The failure mode
is concrete rather than theoretical. Bejís's label-window temperature reaches 5.7 standardised units
on a physical anomaly of +0.83 °C. Its four reference years, 19.64, 19.95, 19.94 and 19.91 °C, agree
to within a third of a degree and yield a climatological SD of 0.147 °C. Muğla's predictor-window
wind speed reaches 5.3 units on +0.34 m s⁻¹ over an SD of 0.065 m s⁻¹. That these are artefacts of a
near-degenerate denominator rather than genuine extremes is settled by comparison: Evia's label
window closes on the same calendar day as Bejís's and is twelve days longer, so any
seasonal-composition explanation would apply to it at least as strongly, yet its comparable +0.67 °C
anomaly yields 1.9 standardised units against an SD of 0.351 °C. The physical anomalies of the two
regions are similar; only their denominators differ.

The second caution is that the label window is not fire weather: it opens on the ignition date and
runs 35 to 59 days into the autumn rains, so it describes conditions during and after the fire
rather than those that preceded it. Only predictor-window values are used anywhere in this paper,
and the label-window figures quoted immediately above serve solely to demonstrate the instability of
the standardised scale.

## 5.8 The pre-fire signal is not an early-fire artefact

The most direct threat to everything above is the possibility that the "pre-fire" thermal composite
is contaminated by early fire signal, since each region's predictor window closes one day before its
label window opens. The window-closure sensitivity (Section 4.7c) addresses this head-on. Both ends
of the predictor window are shifted 7 and 14 days earlier, so that the composite ends one and two
weeks before any labelled burning. The thermal increment stays bootstrap-supported in every region
and every variant. Nowhere does the increment shrink towards zero. The within-region signal is
therefore a genuine pre-fire dryness signal, not a leakage of the fire itself into the predictors.

One observation from this analysis must be reported even though we cannot explain it: in Manavgat
and Bejís the increment *increases* with earlier closure (0.074 → 0.101 and 0.094; 0.058 → 0.077 and
0.079). This is unexpected in direction: contamination by early fire signal would predict the
opposite. We do not know why the increment increases and we do not speculate. We note only that the
direction of the effect is the safe one for the validity of the pre-fire claim.

## 5.9 The empirical contrast with Dimarco et al. (2026)

Dimarco et al. [@Dimarco2026] and this study form a near-controlled contrast conducted by two
independent groups: Mediterranean regions, ~500 m cells, MCD64A1-derived targets, tree ensembles,
spatially aware validation, an explicit ordered-pair transfer matrix. Their predictors are spatially
stationary attributes of place: terrain, human modification, night-time lights, population density
and ERA5-Land long-term climatologies. Every transfer they report exceeds AUC 0.80. Our predictors
describe the dynamic state of a particular pre-fire window, and transfer collapses to chance or
below. Read together, the two studies bracket the predictor-class explanation: stationary-attribute
models learn a spatial ordering of susceptibility that a neighbouring region can inherit.
Dynamic-state models additionally encode how a given degree of anomalous dryness translates into
burning *there, then*, and that mapping is what fails to travel. WildfireGenome's county-level
matrix [@Liu2025], with its mixture of strong and collapsed transfers, sits between the two poles.

The contrast must not be overdrawn, and the bounding differences are stated in Section 2.5: their
target is an ignition proxy evaluated against a 1:1 balanced background, ours is burned-area
classification at the true, heavily imbalanced base rate. These are different problems with
different achievable ceilings. Their temperature variable is a static reanalysis climatology, ours
are event-specific satellite observations referenced to their own baselines. They apply no
adaptation, whereas adaptation is central to our diagnosis. The comparison is between two coherent
experimental programmes, not an ablation. What it supports is precisely the thesis-level reading:
portability tracks predictor class, and the class that carries the within-region gain is the class
that fails to port.

## 5.10 Implications

For practice, the immediate implication concerns regional and "global" fire-susceptibility products.
A within-region AUC prices only half of a predictor block's contribution, even when it is spatially
blocked and honestly computed. The portability it consumes appears on no ledger unless transfer is
measured. Our results say that for dynamic thermal predictors this cost can be total, and that
neither predictor-space applicability screening [@Meyer2021; @Ludwig2023] nor label-free alignment
will reveal or repair it. Transferability must be measured, not assumed from regional, climatic or
regime similarity. The measurement itself is sensitive to evaluation design [@Xu2026], down to the
library version (Section 4.7e).

For method development, the results point to two resources. The first is labels: the conditional
diagnostic requires a labelled probe in the target, and the interventions of Section 4.6 show that
knowing where the reversals are is what converts the diagnosis into an action. Only target labels
provide that knowledge. The second is predictors normalised physically rather than statistically:
TVDI's scene-internal normalisation and the climatological anomaly referencing both failed to
guarantee stable direction, suggesting that portability requires variables whose mapping to
fire-relevant state (for example, actual fuel moisture rather than its thermal proxy [@Yebra2013;
@Marino2024]) is invariant by construction rather than by rescaling. The self-calibrating satellite
thermal digital twin that motivated this project remains future work, and on this evidence its
calibration loop will need labelled feedback, not unsupervised alignment.

## 5.11 Limitations

The transfer failure is a finding, not a limitation. The limitations are the boundaries on how far
it generalises. (i) No meteorological covariates (wind, humidity, precipitation) enter the models,
so we cannot say how the trade-off behaves for a mixed thermal-plus-weather predictor set. The
ERA5-Land diagnostic of Sections 3.17 and 4.9 characterises the regions but is not a predictor and
does not close this gap, and its own four-year climatology limits how firmly its anomalies can be
read. (ii) Temporal transfer is measured for one region only, Muğla, and even there year and
seasonal phase are confounded by the 2022 event's roughly five-week-earlier ignition, so the design
is same-geography event-to-event rather than clean temporal transfer (Section 3.16.4). Its 331
burned cells also leave the thermal direction reversals unresolved at interval level. Those two arms
are additionally the only transfer directions in this paper computed by us rather than read from the
pipeline author's frozen export, albeit with his unmodified code and the same pinned environment
(Section 3.16.4). No other region has a second event. (iii) All labels derive from a single
burned-area product, MCD64A1 [@Giglio2018], whose omission and commission characteristics
[@Boschetti2019] bound every model evaluated here. (iv) The ~510 m analysis cells approximate, but
are not co-registered with, the native MODIS sinusoidal grid (Section 3.2). (v) Even after the AOI
extension, Evia's TSG prevalence (0.287) remains the highest of the five regions. It is four to
seven times that of Manavgat, Bejís and Muğla (0.038 to 0.072), though only marginally above
Montiferru (0.225). Prevalence sensitivity was checked for transfer (Section 4.7a), but Evia remains
the most imbalance-atypical population. (vi) Each region contributes one fire season, so regional
concept shift is confounded with event meteorology; distinguishing them requires multi-year labels.
(vii) Cross-region point estimates carry an implementation tolerance of roughly ±0.02 to 0.03 across
scikit-learn versions (Section 4.7e). All reported numbers are fixed to one verified version, but
exact reproduction elsewhere requires the archived environment. (viii) The diagnostic correlations
rest on an effective sample of ten region pairs. Both the successes and the failures of Section 4.4
should be read at that power. (ix) Manavgat's atypical transfer behaviour remains unexplained. It is
the region where the conditional diagnosis bites hardest and where feature removal recovers most.
The one explanation we were able to test, that its predictor window was meteorologically extreme, is
not supported (Section 5.7). We can say what does not account for it, but we cannot say what does.
With one fire season per region, the candidates that remain are not separable in this design: fuel
structure, ignition and suppression history, and terrain-driven fire behaviour.

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
    3. §5.11(ii) — "Muğla 2022 analysis is in progress" is a placeholder carried from the task
       brief; verify status before submission.
    4. §5.11(iv) — "~510 m cells approximate but are not co-registered with the MODIS sinusoidal
       grid" traces to 03_methods.md lines 55-64, not to 04; wording should be checked against
       the final §3.2.
    4b. 03 §3.1 Table 1 caption — [TO VERIFY] CLOSED 2026-08-11. repo/ was pulled (already at
       48b56e7, no new commits) and core.regions was IMPORTED and queried via get_experiment()
       rather than parsed. All five regions' bboxes, predictor/label windows, baseline years and
       roles match Table 1 exactly; the legacy Evia box and its cited line 67 also match. Only
       the caption's line numbers were stale and are now corrected (AOIs at :222 Manavgat, :252
       Bejís, :59 Muğla, :106 Evia-ext, :142 Montiferru; EXPERIMENTS at :332-790). The old
       caption's "lines 59, 142, 173" mapped to Muğla, Montiferru and a Kozan comment block
       respectively — i.e. it was wrong, not merely outdated. Muğla and Montiferru no longer
       need grid-transform reconstruction; both are declared constants agreeing with the
       previously derived corners.
    5. §5.7 / 04 §4.9 / 03 §3.17 — ERA5-Land block added 2026-08-11, RESOLVED FROM SOURCE
       2026-08-11. Raw files received as a zip, extracted to paper/era5_raw/<analysis_id>/ with
       hashes in paper/era5_raw/SHA256SUMS.txt. All numbers now read directly from
       era5_land_regional_summary.json; the derived-spreadsheet transcription is superseded (it
       was checked against source afterwards and was in fact accurate in all 80 values, but it
       is no longer the basis for anything). Status of the three former open items:
       (a) CLOSED — 04 §4.9 carries Table R9, predictor window only, physical units only.
       (b) CLOSED — Manavgat's predictor temperature anomaly is -0.06 °C, i.e. genuinely at or
           below its climatological mean, and the sign is confirmed from source. The sign-robust
           fallback wording is no longer needed and the claim is asserted directly.
       (c) CLOSED 2026-08-11 — the validator was RUN, not merely described.
           `scripts/validate_era5_land_regional_diagnostic.py --mode actual` against this
           namespace: 27/27 checks passed, 0 failed, 0 skipped, OVERALL PASS, exit code 0.
           Independently reproduced the pipeline author's own reported result. Environment:
           Python 3.12.3, earthengine-api 1.7.39 (import-chain only; no GEE session, no
           credentials), repo at 48b56e7, outputs staged OUTSIDE the repository via
           --output-root so that repo/ stayed untouched (read-only rule). §3.17 now asserts
           the result and names the environment. The 27 checks are identifiers A01-A27 with
           none missing; A24 is simply reported last, after A27, rather than in numeric order.
       (d) NEW, OPEN — provenance discrepancy, recorded in §3.17 and SHA256SUMS.txt rather than
           resolved: manifest.git_commit is a07ea33, but the diagnostic source does not exist at
           a07ea33 (first committed in 48b56e7). The run used an uncommitted working tree. All
           contract semantics strings match 48b56e7 verbatim, so the output is consistent with
           the described code but bit-identity is not established. Worth one question to the
           pipeline author before submission.
       (e) DECISION 2026-08-11 — standardised anomalies are excluded from the paper entirely.
           Climatological SDs are heterogeneous between regions (2.7x-6.0x in the predictor
           windows, up to 11.5x in the label windows), so z-scores are not comparable across
           regions. Rationale is stated in §3.17; §4.9 and §5.7 report physical units only.
           Do not reintroduce z-scores at assembly.
    6. §3.17 — [CITATION NEEDED] CLOSED 2026-08-11. @MunozSabater2021 verified via the Crossref
       REST API (DOI 10.5194/essd-13-4349-2021: Earth System Science Data 13(9):4349-4383, 2021,
       Copernicus, 17 authors, all fields taken from the API response) and added to
       REFERENCES.bib Block F, between Zanaga2022 and Malakar2018, in the file's ASCII-only
       convention with braced LaTeX accents. Cited inline at §3.17's first substantive use.
       First-mention citation also added at 02_related_work.md:294 (Dimarco's predictor list),
       so @MunozSabater2021 now appears twice: at first mention in Related Work, describing
       another study's use of the product, and at §3.17 where we use it ourselves. Both are
       intended; the §3.17 occurrence is the substantive data citation and should survive any
       de-duplication pass. The [^dimarco-lst] footnote's later "static ERA5-Land seasonal
       climatology" is a back-reference and deliberately carries no citation.
    7. §5.2 / 04 §4.8 / 03 §3.16.4 — Muğla two-event block added 2026-08-11 from raw files
       (paper/mugla_temporal_raw/, paper/step9g_raw/, hashes in each SHA256SUMS.txt). Every
       number was read from source and independently matched the values supplied in the task
       brief. Open items:
       (a) CLOSED 2026-08-11 — the transfer arms did not exist, so WE RAN THEM. Emrehan's
           unmodified step9b/step9c at 48b56e7, shadow PROJECT_ROOT so neither repo/ nor
           drive_new/ was written, env Python 3.12.3 / sklearn 1.9.0 / pandas 3.0.5 / numpy
           2.5.2 (matches the pinned version), seed 42. Outputs + hashes in
           paper/mugla_transfer_raw/. Result: both directions ABOVE chance (0.559 [0.513,0.604]
           and 0.670 [0.654,0.685]) but the thermal delta FLIPS SIGN with interval support
           (-0.082 [-0.127,-0.040] vs +0.089 [+0.072,+0.104]). Written into §4.8 Table R9 and
           the §5.2 addition. PROVENANCE: these are the only transfer directions in the paper
           not produced by the pipeline author; §3.16.4 says so explicitly and records
           git_commit: null. Do not let this drop out at assembly.
       (b) FRAMING — the registry itself (core/regions.py, mugla_2022_event_relative) records
           transfer_framing = "same_geography_event_to_event" and warns explicitly that year and
           seasonal phase are CONFOUNDED (2022 ignites ~5 weeks earlier). The section is
           therefore NOT titled or described as temporal transfer. Do not relabel it at assembly.
       (c) HONESTY — only elevation is a bootstrap-supported reversal. The four thermal channels
           are point-level: their AUC *differences* are interval-supported, but the 2022 AUCs
           themselves all straddle 0.5 at n = 331 burned. §4.8 and §5.2 both state this
           explicitly. Do not upgrade the thermal reversals.
       (d) INTERPRETIVE, for coordinator review — the closing paragraph of the §5.2 addition
           argues that elevation being the repeat offender means instability is a property of
           the predictor→burning mapping generally, not of thermal predictors specifically. This
           partly cuts against the paper's framing and is stated deliberately; it rests on two
           contrasts (Manavgat-Muğla, Muğla 2021-2022), so it is an observation at n = 2, not a
           general claim. Check the wording still reads as calibrated.
       (e) Four pair directories in the step9g export carry "_superseded_pre_manavgat_repair";
           they are recorded as superseded in §3.16.4 and were not read.

(b) Interpretation beyond the literal statements of 04 (flag for coordinator review):
    0. §5.7 — 04 §4.9 is now filled from source, so the section no longer runs ahead of its
       numbers (see (a)5). Two interpretive moves still to review: (i) characterising Manavgat
       as "the region whose behaviour most resists the account given above" aggregates three
       separate 04/§5 facts
       (contrast-pair reversal partner, largest feature-removal gain, worst negative recovery)
       into a single "atypicality" that 04 nowhere asserts as such; (ii) the referee-pre-emption
       paragraph ("candidate set fixed before computation, a ninth measure would be search
       behaviour") is a methodological argument, not a result — it states the project's actual
       sequence and should be checked against the lab record the same way §5.6's
       pre-registration narrative is (item b5).
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
    6. §5.8 — "the direction of the effect is the safe one for the validity of the pre-fire
       claim" is a mild interpretive addition to the observation-only rule; delete if it reads
       as speculation.
    7. §5.9 — "near-controlled contrast conducted by two independent groups" and the
       "bracket the predictor-class explanation" reading extend 02 §2.5's vetted framing; no new
       numbers.
    8. §5.10 — "its calibration loop will need labelled feedback, not unsupervised alignment" is
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
    - 02 §2.5 / OUTLINE §1.5: the Dimarco contrast → §5.9 with all three bounding differences.
    STILL OPEN (not closable in Discussion):
    - 01 §1.5 contribution-claim placeholders still read "pending results" — must be filled at
      assembly from 04.
    - RESOLVED 2026-08-08: the 11 METHODS GAPS are closed (03_methods §3.14–§3.16 + §3.1
      Table 1 update); §5.8 now rests on §3.16.3 and §5.11(iv) on §3.2's existing text.
    - Few-shot supplementary (item a2) — decision pending.

  Style: British English (-ise/-our), matching 01-04. Prose word count excluding this comment
  and the drafting note: ~2,450.

COORDINATOR REVIEW (2026-08-08), changes applied after drafting:
    1. §5.8 — recency-of-information clause removed (borderline mechanism speculation); the
       contamination-direction logic and the "safe direction" validity remark retained.
    2. §5.5 — few-shot supplementary pointer carried an inline [TO VERIFY] (inclusion decision
       pending); no numbers introduced. CLOSED 2026-08-13: the pipeline author decided it IN.
       The pointer now names Supplementary S1 (paper/S1_few_shot_recovery.md, written this round
       from the frozen few_shot_recovery export: 3 regions, 6 directions, Table S1, seven stated
       limits). §5.5 still introduces no numbers. 05_discussion now has no open body marker.
    3. §5.11(v) — "two to four times (0.038–0.225)" was numerically wrong (0.287/0.038 ≈ 7.6);
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
       04 §4.5/Table R2 and conditional_similarity_transfer.md all corrected; Fig. 8 shows it
       via filled-vs-open arrowheads.
-->
