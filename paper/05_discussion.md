# 5. Discussion


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

There is an obvious objection to all of this, and it has to be met rather than deflected. Every
reversal cited so far is measured between *different places*, so a sceptic can reasonably reply
that the relationship was never one relationship: Manavgat and Muğla are distinct landscapes with
distinct fuels, terrain and fire histories, and a predictor that means one thing in one and another
thing in the other is not evidence of instability so much as evidence that two different systems
were compared. The two Muğla events answer this directly (Section 4.8). Region, AOI, analysis grid,
feature registry and processing chain are identical; only the fire differs. Elevation's association
with burning nevertheless reverses with bootstrap support — 0.611 [0.532, 0.690] in 2021, higher
ground burning preferentially, against 0.296 [0.230, 0.355] in 2022, lower ground burning
preferentially, with disjoint intervals and a difference of −0.317 [−0.414, −0.220]. Holding
geography fixed does not stabilise the direction of the relationship.

The mechanism is unusually visible here, and it is physical rather than statistical. The 2021
season burned as a dispersed complex of ten components across the region's full relief, from near
sea level to 1,975 m; the 2022 event was a single compact scar confined below 777 m, with a median
burned elevation of 187 m against 563 m the year before. The effective component count falls from
4.05 to 1.34 and the observed land-cover classes from seven to two. The two fires simply occupied
different parts of the same elevation gradient, and a model that learned "high ground burns" from
the first would be actively wrong about the second. This is what concept shift looks like when it
can be seen: not a subtle distributional drift, but two events sampling opposite ends of a
topographic range that the region contains in full.

Two constraints on how far this carries. First, the design is same-geography event-to-event and not
clean temporal transfer: the 2022 fire ignites about five weeks earlier in the season, so year and
seasonal phase are confounded and the difference cannot be attributed to elapsed time
(Section 3.16.4). What it does isolate is geography, which is precisely the variable the objection
rests on. Second, only elevation reverses with interval support. The four absolute thermal channels
move from bootstrap-supported *lower*-values-burn to *higher*-values-burn point estimates, and each
shift is itself interval-supported, but with 331 burned cells in 2022 every one of those intervals
straddles 0.5, so the 2022 direction is not established and we do not claim the thermal reversals
as supported (Section 4.8).

Transfer between the two events completes the picture and sharpens the trade-off rather than
softening it. With geography fixed, transfer no longer collapses: both directions stay above
chance, where six of twenty between-region directions fell below it. But the thermal block's
contribution *changes sign* — −0.082 [−0.127, −0.040] carrying 2021 forward to 2022, +0.089
[+0.072, +0.104] carrying 2022 back to 2021 — with both signs interval-supported, even though the
same block is locally informative within each event separately (+0.116 in 2021, +0.078 in 2022).
This is the trade-off at its most explicit. The six predictors that buy local skill in both events
are not merely unhelpful across them; in one direction they subtract from a static baseline that
would otherwise have transferred at 0.642. Whether a dynamic-state block helps or harms on transfer
is a property of the source–target pair, not of the block.

That elevation is the one supported reversal is itself worth noting, because it is the second time
the same predictor has played this role: elevation also carries the sharpest bootstrap-supported
reversal in the Manavgat–Muğla pair (signed AUC 0.374 against 0.611). Across a between-region
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
few-shot recalibration analysis exists in the project diagnostics and is reported in the
supplementary material (Supplementary S1); it is not drawn on here.

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

## 5.7 The meteorological-extremity explanation, tested and not supported

Manavgat is the region whose behaviour most resists the account given above. It supplies the
reversal partner in the sharpest contrast pair (Section 5.2), it is where feature removal buys
almost all of its transfer gain (+0.025 mean delta over Manavgat-involved directions against
−0.009 elsewhere, Section 5.5), and it is the target of the worst negative recovery under
adaptation (Evia→Manavgat, −0.86 of the gap). The most natural post hoc explanation is
meteorological: that Manavgat 2021 was an exceptionally extreme fire season, so that its
thermal predictors were driven by a regional weather anomaly the other regions did not share,
and the resulting mapping from dryness to burning was correspondingly idiosyncratic.

We tested that explanation and it was not supported. The ERA5-Land regional diagnostic
(Sections 3.17, 4.9) characterises each region's predictor window against its own 2017–2020
climatology, and Manavgat is not the meteorologically extreme member of the set. Its
predictor-window temperature sits 0.06 °C *below* its climatological mean — the only region at or
below its own baseline, and a departure small enough that the honest reading is simply that
Manavgat burned under climatologically ordinary temperatures — while the other four regions run
0.31 to 1.11 °C warm. Its humidity deficit of 3.24 % is mid-range among the five, its wind
departure of +0.07 m s⁻¹ is the second smallest, and its precipitation total is within 1.4 mm of
climatology, the smallest precipitation departure in the set. On none of the four variables is
Manavgat the extreme member; on two it is the least anomalous. Whatever makes its transfer
behaviour atypical, regional meteorological extremity in the predictor window is not it.

We report this as a failed prediction rather than as a result, and it carries the same status as
the pre-registered regime null of Section 5.6: a stated expectation, tested, and not borne out.
The two failures are informative in the same limited way. They remove candidate explanations
without supplying one.

The reader may reasonably ask why meteorology, once measured, is not simply added to the
diagnostic set of Section 4.4 as a ninth measure of region similarity. It is not added because the
candidate set was fixed before any diagnostic-versus-transfer correlation was computed. Eight
measures were specified and eight failed to order the transfer matrix; appending a ninth after
seeing those eight fail would be a search over the diagnostic space, and any correlation it
returned on ten pairs would be uninterpretable. The measurement is reported for what it is — a
descriptive characterisation of the regions and a test of one specific explanation — and is kept
out of the ordering analysis by construction.

Two cautions attach to the reading of Section 4.9, and they are the reason it reports physical
units rather than standardised ones. The first concerns the climatology. It spans four years, and
the standard deviations it yields differ between regions by factors of 2.7 to 6.0 in the predictor
windows, so a standardised anomaly measures a different physical departure in each region and
invites a cross-region comparison that the quantity cannot support (Section 3.17). The failure
mode is concrete rather than theoretical. Bejís's label-window temperature reaches 5.7 standardised
units on a physical anomaly of +0.83 °C, because its four reference years — 19.64, 19.95, 19.94 and
19.91 °C — agree to within a third of a degree and yield a climatological SD of 0.147 °C; Muğla's
predictor-window wind speed reaches 5.3 units on +0.34 m s⁻¹ over an SD of 0.065 m s⁻¹. That these
are artefacts of a near-degenerate denominator rather than genuine extremes is settled by
comparison: Evia's label window closes on the same calendar day as Bejís's and is twelve days
longer, so any seasonal-composition explanation would apply to it at least as strongly, yet its
comparable +0.67 °C anomaly yields 1.9 standardised units against an SD of 0.351 °C. The physical
anomalies of the two regions are similar; only their denominators differ.

The second caution is that the label window is not fire weather: it opens on the ignition date and
runs 35–59 days into the autumn rains, so it describes conditions during and after the fire rather
than those that preceded it. Only predictor-window values are used anywhere in this paper, and the
label-window figures quoted immediately above serve solely to demonstrate the instability of the
standardised scale.

## 5.8 The pre-fire signal is not an early-fire artefact

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

## 5.9 The empirical contrast with Dimarco et al. (2026)

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

## 5.10 Implications

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

## 5.11 Limitations

The transfer failure is a finding, not a limitation; the limitations are the boundaries on how
far it generalises. (i) No meteorological covariates (wind, humidity, precipitation) enter the
models, so we cannot say how the trade-off behaves for a mixed thermal-plus-weather predictor
set; the ERA5-Land diagnostic of Sections 3.17 and 4.9 characterises the regions but is not a
predictor and does not close this gap, and its own four-year climatology limits how firmly its
anomalies can be read. (ii) Temporal transfer is measured for one region only, Muğla,
and even there year and seasonal phase are confounded by the 2022 event's roughly five-week-earlier
ignition, so the design is same-geography event-to-event rather than clean temporal transfer
(Section 3.16.4). Its 331 burned cells also leave the thermal direction reversals unresolved at
interval level. Those two arms are additionally the only transfer directions in this paper computed
by us rather than read from the pipeline author's frozen export, albeit with his unmodified code
and the same pinned environment (Section 3.16.4). No other region has a second event. (iii) All labels derive
from a single
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
of Section 4.4 should be read at that power. (ix) Manavgat's atypical transfer behaviour remains
unexplained. It is the region where the conditional diagnosis bites hardest and where feature
removal recovers most, and the one explanation we were able to test — that its predictor window
was meteorologically extreme — is not supported (Section 5.7). We can say what does not account
for it; we cannot say what does, and with one fire season per region the candidates that remain
(fuel structure, ignition and suppression history, terrain-driven fire behaviour) are not
separable in this design.

