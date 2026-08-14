# 5. Discussion

> **Drafting note.** Numbers in this section come from `04_results.md`, except for the referee-round
> values added on 2026-08-13, which come from the three verified reports named in the closing
> draft-notes block: `referee_round_numbers.md`, `transfer_ci_blocksize.md` and
> `diagnostics_common_subset.md`. No value is re-derived from any other source. Citations resolve
> against `paper/REFERENCES.bib` and were restricted to keys already used in Sections 1–2.
> Interpretive claims that go beyond the literal statements of Section 4 are listed in the closing
> draft-notes block for coordinator review.

## 5.1 Principal findings

Across five Mediterranean fire regions, six pre-fire thermal predictors were added to a static and
near-static baseline of terrain, fuel and greenness, whose only time-varying member is the
vegetation-index composite. Spatially blocked within-region ROC-AUC was raised by +0.056 to +0.153,
with bootstrap support at ~1 km and ~5 km blocking in all five regions (Section 4.2). The same models were then
applied across regions without target labels. Transfer AUCs ran from 0.326 to 0.686, and even the
best direction fell 0.184 short of its target's within-region reference (Section 4.3).

One feature of the transfer matrix is invariant to how the bootstrap is blocked, and the argument is
built on it. The point estimates do not depend on the blocking, and no direction changes side of the
chance line when the blocking is coarsened. Coarsening only weakens support. At the conservative
5 km blocking that Section 3.12 defends, nine of twenty directions are above chance with interval
support and three to four are below it, with the remaining seven or eight carrying no verdict. The
fourth below-chance direction, Evia to Bejís, sits on the chance line across bootstrap seeds and
should be read as borderline. The finer 1 km blocking used in Table 4 gives twelve above, six below
and two uncertain.

Label-blind adaptation did not repair this. It compressed the whole matrix towards chance, to a
range of 0.431 to 0.630. Of the twelve directions that had transferred above chance, nine were
degraded and three were raised, all three with Montiferru as their source; inside the four-AOI
subset that carries the decomposition there is no exception at all. At most a third of the deficit
was recovered where transfer had failed.

Of twenty candidate transferability diagnostics, only two had bootstrap intervals that excluded
zero, and both were conditional. They are computed from the *direction* of each predictor's
association with burning in both regions. Every marginal, niche-overlap and fire-regime measure
failed to order the matrix (Section 4.4). At the point estimate, the pair with the highest
burned-niche overlap failed in both directions while the pair with the lowest overlap transferred in
both (Section 4.5); half of that contrast carries interval support at 5 km blocking and half does
not.

The trade-off is direct rather than inferred. Paired per direction, the thermal block that adds
+0.056 to +0.153 AUC inside every region contributes +0.004 on average to transfer, and that mean
carries an interval that spans zero under any resampling unit the design permits (pair-clustered
[−0.028, +0.036]). What the design supports is not a small positive contribution but no contribution
distinguishable from zero. Its sign is unstable across directions, and this too is invariant to the
blocking. The paired deltas run from −0.148 to +0.132, twelve of twenty positive and eight negative,
at either blocking scale. At 5 km blocking the block is CI-supported positive in five to six
directions and CI-supported negative in three to four, with ten or eleven carrying no verdict, the
range reflecting two boundary directions; at 1 km blocking the split is ten, seven and three, itself
decided by one bound of −0.00045 (Section 4.7g). It is also the
swing factor at the chance line: at the point estimate it drags three directions below chance and
lifts one above it (Table R6). Dynamic state predictors buy local skill at the cost of portability,
and that cost is invisible to the diagnostics the field currently uses to anticipate it.

## 5.2 Why the thermal increment is real but local

The within-region increment is not an artefact to be explained away. It replicates in five
independent regions. It survives coarsening of the spatial blocks to ~5 km with its interval intact,
and its point estimate holds at ~10 km. It persists in the
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
inverts it. That is why raw transfer lands *below* chance rather than merely towards it. Six of
twenty directions are below chance at the point estimate. Three to four of them carry interval
support at the conservative 5 km blocking, and six do at 1 km, with Evia to Bejís the borderline
case at the coarser one. Below-chance transfer is the signature that distinguishes concept shift from
ordinary covariate-shift degradation, which can only dilute skill towards 0.5.

Two refinements follow, and both are honest. First, in the Manavgat-Muğla pair the reversals
concentrate in the absolute channels. The two channels referenced to a local baseline,
`lst_anomaly_mean` and `tvdi_difference_mean`, keep a common direction. That is consistent with
anomaly-referencing absorbing part of the between-region offset. The protection is not general,
however. `lst_anomaly_mean` itself reverses with interval support between Bejís and Evia (Section
4.6b). TVDI reverses alongside the raw LST channels, even though it is internally normalised by
construction against scene-fitted wet and dry edges [@Sandholt2002]. That was the theoretical
portability advantage flagged in Section 2.2, and it does not survive contact with the data.

TVDI's own construction is a competing explanation for that particular reversal, and it should be
stated rather than argued away. The wet and dry edges are percentiles of the LST values a given
scene contains (Section 3.4), so they are refitted for every AOI and every window. A TVDI of 0.5
denotes whatever the middle of that AOI's own dryness range happened to be, and the five AOIs differ
by an order of magnitude in area and widely in relief. Two regions can therefore disagree about the
sign of the TVDI-burning association without any difference in the underlying dryness-to-burning
relationship, purely because the index is anchored to different populations in the two places. We
therefore computed the analysis that separates the two explanations, and it does not support the
index-artefact reading (Section 4.7k). Two things were done. Sea water takes part in the edge fit and
dominates two of the AOIs, so the edges were refitted on land pixels alone; and because that still
leaves each region normalised against its own scene, one set of edges was then fitted once over the
pooled land pixels of all five regions, so that a TVDI of 0.5 denotes the same dryness everywhere.
The sea does move the index, by an amount that scales with each AOI's sea fraction, +0.017 in Evia
and +0.016 in Muğla against +0.002 in inland Bejís. Neither re-run changes any region's direction.
Under the common edge Manavgat still ranks burned cells by higher TVDI at 0.565, while Muğla and
Evia still rank them by lower TVDI with intervals entirely below 0.5, at 0.341 and 0.378. Since the
index's scene dependence was the competing explanation, and removing it leaves the disagreement
intact, the reversal belongs to the dryness-to-burning relationship rather than to the normalisation.
The honest reading is still narrower than the fully general one: statistical self-normalisation against locally fitted
reference values does not guarantee a stable direction of association, and the TVDI reversal is
consistent both with concept shift and with the index's own scene dependence. The reversals in the
absolute LST channels, which carry no such normalisation, and the elevation reversal, which involves
no thermal quantity at all, do not admit this explanation.

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

The two Muğla events speak directly to this (Section 4.8). Region, AOI, analysis grid, feature
registry and processing chain are identical, and the static predictors are identical cell by cell.
The design holds place fixed; it does not hold the population fixed, because the 2022 arm is defined
by removing the 2021 scar, and that qualification is developed in Section 4.8 and in Section
5.11(ii). Elevation's association with burning nevertheless reverses with bootstrap support. It is 0.611 [0.532, 0.690] in 2021, where
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

This changes how a within-region score should be read, and the implication is worth stating plainly.
If a relationship fitted on one event does not hold for another event in the same region, then a
within-region ROC-AUC estimates interpolation inside one fire season's footprint. It is not an
estimate of a stable susceptibility surface. The 2022 thermal model reaches a within-region AUC of
0.942, and it does so on 331 burned cells forming essentially one scar. That is the clearest
illustration in this paper of how local such a score can be. It also sharpens the practical point of
Section 5.10: a within-region AUC prices only half of a predictor block's contribution, and the half
it does price is tied to the footprint it was fitted on. This rests on one region with two events,
so it is an observation rather than an established general property.

Two constraints limit how far this carries, and the first is heavier than it first appears. The
design is same-geography event-to-event and not clean temporal transfer. The 2022 fire ignites about
five weeks earlier in the season, so year and seasonal phase are confounded and the difference
cannot be attributed to elapsed time (Section 3.16.4). What the design does isolate is geography,
which is precisely the variable the objection rests on. But seasonal phase is not a neutral nuisance
here. The 2022 predictor window closes on 20 June and the 2021 window on 28 July, so a late-spring
composite is being compared with a high-summer one, and in this landscape high ground in late spring
is still cool, moist and effectively unburnable while by late July it is not. A seasonal-phase
contrast therefore predicts the observed direction of the elevation reversal, and it predicts the
sign change in the absolute LST channels as well, since their baseline climatology is recomputed for
the shifted calendar window. The two explanations, a genuine reparameterisation of the
elevation-burning relationship and a seasonal-phase artefact, are not separated by this design. **Nor
can they be, in this study area.** An earlier version of this section called a calendar-matched 2022
arm the single most valuable follow-up the paper could name. That arm was then attempted and the
burned-area record rules it out. The two Muğla events sit 42 days apart in seasonal phase, with
median burn day-of-year 215 in 2021 and 173 in 2022, and holding the calendar fixed at the 2021
window leaves nine burned cells in 2022 against a gate minimum of thirty. The mirror pairing fails
for the same reason: 2022 contains no high-summer event and 2021 no late-spring one, the whole of
2022 in this area amounting to 358 burned cells against 3,206 in 2021. Separating year from seasonal
phase needs a region with two events at a matching phase in different years, and no region in this
cohort has one, since each contributes a single fire season (limitation (vi)). The details and the
validation of these counts are in `paper/mugla_calendar_arm.md`. The comparison therefore
establishes that *something* reverses the elevation-burning association with geography, grid and
pipeline held fixed, and it does not establish that the something is year rather than season. What
the confound does not weaken is the narrower reading that the sign of the thermal block's transfer
contribution is a property of the pair rather than of the block, since that holds under either
explanation. Second, only elevation reverses with interval support. The four absolute thermal channels
move from bootstrap-supported *lower*-values-burn to *higher*-values-burn point estimates, and each
shift is itself interval-supported. With 331 burned cells in 2022, however, every one of those
intervals straddles 0.5. The 2022 direction is therefore not established, and the thermal reversals
are not claimed as supported (Section 4.8).

Transfer between the two events completes the picture and sharpens the trade-off rather than
softening it. With geography fixed, transfer no longer collapses. Both directions stay above chance,
where six of twenty between-region directions fell below it at the point estimate. The thermal
block's contribution nevertheless *changes sign*. It is −0.082 [−0.127, −0.040] carrying 2021
forward to 2022, and +0.089
[+0.072, +0.104] carrying 2022 back to 2021. Both signs are interval-supported, even though the same
block is locally informative within each event separately (+0.116 in 2021, +0.078 in 2022). This is
the trade-off at its most explicit. The six predictors that buy local skill in both events are not
merely unhelpful across them; in one direction they subtract from a baseline that would
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
structure describes the spatial pattern of P(y). All are blind to the quantity that failed here,
which is the sign of the conditional association.

They are not, however, all label-free, and the contrast is often drawn too broadly. Only the
marginal P(x) family is computable before any target label exists. Burned-niche overlap is defined
on the burned cells of both regions and fire-regime structure on the target's burned map, so both
consume the target's labels exactly as the conditional index does (Section 3.14.4). This makes the
comparison sharper. Niche overlap and the conditional index are built from the same labelled
information about where fire happened, and only the one that reads the *direction* of each
predictor's association orders the transfer matrix. Describing burned cells is not the same as
describing the response. It also leaves the practitioner in a worse position than the tidy version
of this story would suggest: the single family that could be run before deployment is the marginal
one, and it is the family that fails.

The domain classifier makes the blind spot concrete. Source and target cells are separable at AUC
0.962 to 0.9999 for every pair, so marginal shift is essentially total everywhere. A marginal
instrument is therefore at ceiling and cannot discriminate transfer outcomes that range from 0.33 to
0.69.

The applicability numbers themselves say the same thing directly, and they settle a claim made in
Section 1.3. Manavgat to Muğla places 0.8752 of the target's cells inside the weighted area of
applicability and 0.9640 inside the unweighted support. That is the highest weighted value in the
matrix. It transfers at 0.4702, below chance. The reverse direction sits at 0.5305 weighted and
0.9702 unweighted, the highest unweighted value in the matrix, and transfers at 0.4010. Both
directions are below chance at the point estimate. Muğla to Manavgat is below chance with interval
support at both blocking scales, while Manavgat to Muğla is supported at 1 km blocking and carries
no verdict at 5 km. Muğla to Bejís runs the other way. It places 0.0050 of the target inside the
weighted area of applicability, the lowest value in the matrix, and transfers above chance at
0.5832 with interval support at both blockings. A model can therefore sit almost entirely inside its
nominal area of applicability and still perform below chance, and sit almost entirely outside it and
still perform above chance.

Two limits attach to that statement. The marginal audit covers only the four-region subset, so
Montiferru has no applicability value in any direction. The Bejís and Montiferru half of the contrast
pair described next therefore cannot be given one. The two applicability quantities also disagree
sharply with each other across the matrix, so any claim about applicability must say which of them
is meant.

The contrast pair makes the same point through burned-niche overlap. Manavgat and Muğla have the
most similar burned envelopes of any pair in the matrix (mean Schoener's D 0.826, closest burned
centroids), and both directions are below chance, as the applicability figures above record. Bejís
and Montiferru have the least similar envelopes (D 0.479, farthest centroids), and both directions
are above chance, with interval support at 1 km blocking and no verdict at 5 km. Where the envelope
agrees but the direction reverses, transfer fails. Where the envelope disagrees but the direction
agrees, transfer works. At pair level the two quantities are empirically distinct, and in partial
rank correlations
the conditional index retains its association with transfer when niche overlap is held fixed (+0.82)
while niche overlap retains none in the reverse conditioning (−0.07).

This offers a measurable operationalisation of a concept the species-distribution-modelling
transferability literature has discussed as "ecological stationarity" [@Yates2018]: on this
evidence, the stationarity that transfer requires is *direction agreement in P(y|x)*, not overlap of
environmental envelopes. It is also consistent with the SDM findings that environmental and
geographic similarity do not predict transfer success [@Vesk2021; @Rousseau2022], now reproduced in
a fire application in which the most similar pair falls below chance in both directions. None of
this is a criticism of the area-of-applicability construction, which does what it claims for the
extrapolation failure mode it was designed for. It is a demonstration that a reassuring marginal
diagnostic is not evidence of portability when the predictors are dynamic state variables.

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

It is also coarse, and it is undefined for one of the pairs the paper leans on hardest. The
supported-feature restriction that gives the index its discrimination leaves six of eight pairs with
denominators of one or two features, and the two Montiferru pairs drop out entirely. One of those
two is Bejís and Montiferru, which supplies half of the contrast pair of Section 5.3: the lowest
burned-niche overlap in the matrix, and transfer above chance in both directions. The diagnostic
this section advances is therefore silent on exactly the pair that carries half of the paper's
headline counterexample, and that should be read as a real gap rather than a technicality. The
exclusion is not because Montiferru lacks supported features, since it has three. It arises from
set-disjointness between the two regions' supported features, which is the more precise and more
defensible statement of the coverage limit. The index is close to a binary flag for "any supported
sign disagreement". The power caveat of Section 4.4 also applies to *every* correlation in the
diagnostic table, including the two successes: the effective sample is ten unordered pairs, the two
directions of a pair are not independent, and intervals of width ±0.5 to 0.8 on the null rows cannot
rule out moderate true correlations. The null diagnostics are "not shown to order transfer", not
"shown not to". The conditional result is a strong ordering on a small pair set, not an established
general law.

Multiplicity is not controlled, and no control is claimed. Twenty variants were correlated against
one target quantity, nineteen of them computable, on an effective sample of ten unordered pairs. Two
intervals excluded zero. No family-wise error correction is applied and none is offered (Section
3.14.1). Two mitigations are genuine, and neither substitutes for an error rate. The families and
their variants were listed in advance rather than searched over. The conditional-versus-marginal
contrast was a directional expectation stated before computation. The restriction to CI-supported
features was pre-specified in the same way, and that matters, because the unrestricted versions did
not clear the bar. The best of them, cosine over all nine features, reaches ρ = +0.50 with an
interval that spans zero. Stating this openly is the defence. Concealing that the unrestricted
variant failed would not be one.

A referee may object that the index is close to definitional, and the objection is fair. The model
is built from these same features. If a strongly supported feature's association is inverted in the
target, the model's ranking must invert with it, so a correlation between the index and transfer is
not a discovery. That is precisely the point being made here. The diagnosis is mechanistic rather
than predictive: it locates the failure in P(y|x) rather than in P(x). The non-trivial empirical
content is that the *marginal* instruments do not see what the conditional one sees, on the same
pairs. Nothing beyond that is claimed.

One competing explanation for that contrast has been excluded. The diagnostic rows were not all
computed on the same directions. The marginal, applicability, climatic and geographic rows sit on
twelve directions, the supported-conditional rows on sixteen, and the rest on twenty, so the
marginal family carried the smallest sample by construction and its failure could have been a power
artefact. Every diagnostic was therefore recomputed on a common subset of twelve directions from six
unordered pairs. The two supported-conditional rows remain the only ones whose intervals exclude
zero, and they are slightly stronger there, at +0.87 [+0.65, +0.88] and +0.85 [+0.43, +0.88]. All
eighteen other rows span zero. Unequal sample size was not what separated the families. Removing the
power confound does not remove the coarseness one: on that same subset the index still takes only
three distinct values, and it still requires target labels.

Two further bounds belong here, because they are the ones a sceptical reader would derive
independently. The index's tie structure caps the attainable 16-direction Spearman at +0.861, so the
observed +0.840 sits on its own ceiling and the narrow published interval reflects heavy ties under
pair resampling rather than precision. At the pair level the exact one-sided permutation p is 0.0060, which is the smallest value this tie structure can produce, against a Bonferroni threshold
of 0.0026 over the nineteen computed variants. No outcome of this diagnostic could have cleared a
family-wise correction on this pair set, whatever the data had been. That is a statement about the
design rather than about the result, and it is the reason this section describes a mechanism
diagnosis rather than a validated instrument (Section 4.4).

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
leave-one-region-out pooled thermal model never beats the best single-source pairwise transfer at the
point estimate, with shortfalls of 0.02 to 0.22. It sits 0.28 to 0.50 below the within-region
ceiling. For two of five targets it is beaten raw by the pooled baseline, and for a third the two are within 0.006. In effect, the pooled model
resolves conflicting thermal directions by discounting the block that carries them.

Feature removal is not a favourable trade, but its geometry confirms the diagnosis. Dropping the two
supported reversal features costs −0.081 mean within-region AUC, supported in every region, and
changes mean transfer AUC by +0.014, an estimate whose pair-clustered interval spans zero. The gains land
exactly where the reversal analysis points. All three interval-supported gains involve the reversal
partners. The mean delta over Manavgat-involved directions is +0.025 against −0.009 elsewhere.
Removal of `lst_anomaly` contributes only in the one pair where it reverses with support. Knowing
*which* features to drop for *which* pair, however, requires the target's signed directions, that is
to say target labels. Applied label-free, the same removal degrades the five aligned directions. The
consistent lesson is the one the adaptation literature reached once the conditional component was
recognised as binding [@Tuia2016; @Persello2012]: a small number of target labels is the resource
that label-free machinery cannot substitute for. A supervised few-shot recalibration analysis exists
in the project diagnostics. Its headline is now in the main text at Section 4.10, its design and
limits in Supplementary S1, and Section 5.10 uses it to say what the failure documented here costs
to repair.

## 5.6 The stated regime hypothesis, reported as it happened

Section 2.5 offered fire-regime typology [@Archibald2013] as a candidate explanation for the concept
shift. The idea was that regions in different limiting regimes should map dryness to burning
differently. The expectation that fire-regime distance would *not* predict transfer was written down
before the regime correlation was run and before the Evia-extended results were computed. It is an
entry in the project's analysis log rather than a formal pre-registration. No independent timestamped
public registration exists, and the record entered version control on the day the diagnostics were
computed (Section 3.14.1). The expectation was stated in advance, and that is the whole of the claim
made for it. The data confirmed the null. They did so in a way
that exposes the intuition behind the hypothesis as wrong, and that is reported plainly rather than
as vindication. The regime-distance point estimate has the wrong sign (ρ = +0.29). The most
regime-similar pair in the set is Bejís and Evia-extended, with effective burned-component counts of
1.0000 and 1.0083, which is as close to identical regime structure as the data allow. That pair
fails in both directions with interval support, though the Evia to Bejís interval reaches the chance
line at the conservative blocking. The most regime-different pair, Bejís-Muğla,
transfers above chance. One mundane explanation for Muğla's part in that result can be set aside:
Muğla has by far the largest analysis population, but cutting it to Manavgat's cell count over
twenty stratified repeats leaves its transfer behaviour where it was, in both roles and in seven of
the eight direction-and-family combinations (Section 4.7j). What the size matching does move is
Muğla's absolute within-region AUC, by roughly 0.01 to 0.02, and the thermal increment survives it.
The error was in the hypothesised grouping, not in the data. It was the
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
stated regime null of Section 5.6: an expectation on record, tested, and not borne out. The two
failures are informative in the same limited way. They remove candidate explanations without
supplying one.

The reader may reasonably ask why meteorology, once measured, is not simply added to the diagnostic
set of Section 4.4 as a further measure of region similarity. It is not added because the candidate
set was fixed before any diagnostic-versus-transfer correlation was computed. Twenty variants across
four families were specified, and only two of them, both conditional, ordered the transfer matrix.
Appending another measure after seeing the rest fail would be a search over the diagnostic space,
and any correlation it returned on ten pairs would be uninterpretable. The measurement is reported
for what it is, namely a descriptive
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

One observation from this analysis needs reporting: in Manavgat and Bejís the increment *increases*
with earlier closure (0.074 → 0.101 and 0.094; 0.058 → 0.077 and 0.079). This is unexpected in
direction, since contamination by early fire signal would predict the opposite. A mechanism is
available and the window-closure report states it. The closure date is shifted against a fixed
production policy, so moving the window changes which acquisition dates enter the median composite
and how many clear observations back each pixel. With about seven usable dates in a window, a 7 or
14 day shift adds or removes one or two of them. The evidence fits: over the same comparison the
baseline moves by +0.002 to +0.003 while the thermal family moves by +0.022 ROC-AUC, so the shift
acts almost entirely on the thermal channels. That is the same dependence the compositing A/B of
Section 4.7i finds by a different route, where three defensible weighting choices move Manavgat's
increment between +0.045 and +0.084 on an identical cohort. The pre-fire claim is unaffected, and
the direction of the effect remains the safe one for it. What this does say is that part of the
increment's magnitude is a function of how the composite was built rather than of dryness alone, and
Section 5.11 records the resulting tolerance.

## 5.9 The empirical contrast with Dimarco et al. (2026)

Dimarco et al. [@Dimarco2026] and this study form a near-controlled contrast conducted by two
independent groups: Mediterranean regions, ~500 m cells, MCD64A1-derived targets, tree ensembles,
spatially aware validation, an explicit ordered-pair transfer matrix. Their predictors are spatially
stationary attributes of place: terrain, human modification, night-time lights, population density
and ERA5-Land long-term climatologies. Every transfer they report exceeds AUC 0.80. Our predictors
describe the dynamic state of a particular pre-fire window, and transfer collapses to chance or
below. Read together, the two studies are consistent with a predictor-class explanation:
stationary-attribute models can learn a spatial ordering of susceptibility that a neighbouring
region inherits. Dynamic-state models additionally encode how a given degree of anomalous dryness
translates into burning *there, then*, and that mapping is what fails to travel. WildfireGenome's
county-level matrix [@Liu2025], with its mixture of strong and collapsed transfers, sits between the
two poles.

The contrast must not be overdrawn, and three of the bounding differences are stated in Section 2.5:
their target is an ignition proxy evaluated against a 1:1 balanced background, ours is burned-area
classification at the true, heavily imbalanced base rate. These are different problems with
different achievable ceilings. Their temperature variable is a static reanalysis climatology, ours
are event-specific satellite observations referenced to their own baselines. They apply no
adaptation, whereas adaptation is central to our diagnosis. The comparison is between two coherent
experimental programmes, not an ablation.

A fourth bounding difference is the sharpest, and it must be stated because it bears directly on the
reading above. Our own baseline is predominantly stationary, and it does not transfer well
either. Across the twenty directions it averages ROC-AUC 0.5371. Four directions are below chance at
the point estimate, and at 1 km blocking all four have intervals lying entirely below it. Set
against every Dimarco transfer exceeding 0.80, that is not a stationary-versus-dynamic contrast in
the abstract. Our baseline carries four predictors of terrain, fuel and greenness. Theirs adds human
modification, night-time lights, population density and long-term reanalysis climatologies. The
contrast is therefore a thin place-descriptor set plus a dynamic block against a rich
place-descriptor set. The predictor-class reading survives, but it survives as a reading of two
programmes that differ in predictor richness as well as in predictor class. What the pair of studies
supports is that portability may track predictor class, and that the class carrying our
within-region gain is the class that fails to port. A stationary predictor set is not on its own
sufficient for portability, as our own baseline shows.

## 5.10 Implications

For practice, the immediate implication concerns regional and "global" fire-susceptibility products.
A within-region AUC prices only half of a predictor block's contribution, even when it is spatially
blocked and honestly computed. The portability it consumes appears on no ledger unless transfer is
measured. Our results say that for dynamic thermal predictors this cost can be total, and that
neither predictor-space applicability screening [@Meyer2021; @Ludwig2023] nor label-free alignment
will reveal or repair it. Transferability must be measured, not assumed from regional, climatic or
regime similarity. The measurement itself is sensitive to evaluation design [@Xu2026], down to the
library version (Section 4.7e).

What should a practitioner do instead? The results support three concrete answers, and the third is
the one this paper adds. First, screen with the right instrument. A marginal applicability check
answers "is this target inside the training distribution?" and that question was not the binding one
here: Manavgat to Muğla sits at 0.875 weighted applicability and transfers at 0.470, below chance.
Where labels exist on both sides, the signed-association comparison of Section 3.14.4 tracked
transfer where twenty other candidates did not, so it is the screen to run, with the caveats of
Section 5.4 attached. Second, do not spend effort on label-free alignment. Two standard methods,
applied carefully, moved 14 of the 20 directions towards chance rather than towards skill, and every
direction they improved involves Montiferru, the smallest region in the set. Third, price the labels
instead. Section 4.10 gives the shape of that price for three regions: thirty-two labelled 5 km
blocks recovered 85 to 89 % of the target's own ceiling in three of six directions, two of them from
starting points below chance. That is a real answer to "what do we do", and it is not a cheap one.
The same budget is 7 to 20 % of the target's natural-vegetation population, it recovers only 51 to
57 % where the concept gap is widest and 30 % in the sixth direction, and at small budgets it
damages the direction that transfers best without any labels. No general label budget follows from six directions in three regions, and none is claimed
here. What follows is the form of the answer: transfer failure of this kind is bought back with
target labels, at a price that scales with the size of the conditional gap, and a campaign that
cannot afford the labels should not deploy the model.

For method development, the results point to two resources. The first is labels, as above: the
conditional diagnostic requires a labelled probe in the target, the interventions of Section 4.6
show that knowing where the reversals are is what converts the diagnosis into an action, and Section
4.10 shows what buying that knowledge costs. Only target labels provide it. The second is predictors normalised physically rather than statistically:
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
seasonal phase are confounded by the 2022 event's six-week-earlier ignition, so the design is
same-geography event-to-event rather than clean temporal transfer (Section 3.16.4). That confound
is not merely unaddressed: it cannot be addressed here. The two events differ by 42 days in median
burn day-of-year, and neither year contains a second event at the other's phase, so a
calendar-matched arm would carry nine burned cells against a gate minimum of thirty (Section 5.2 and
`paper/mugla_calendar_arm.md`). Its 331
burned cells also leave the thermal direction reversals unresolved at interval level. The pair holds
place fixed but not population: the 2022 arm is the 2021 arm with the 2021 scar removed, so the two
share 38,789 of 38,790 cells and three identical static predictors, and in the 2022 to 2021
direction every target positive lies outside the source training population while almost every
target negative lies inside it (Section 4.8). We cannot bound what that does to the two reported
numbers, so they are not comparable to the 20 between-region directions and the elevation reversal
has a structural competing explanation this design cannot exclude. Those two arms are additionally
the only transfer directions in this paper computed by us rather than read from the pipeline
author's frozen export, albeit with his unmodified code and the same pinned environment (Section
3.16.4). No other region has a second event. (iii) All labels derive from a single
burned-area product, MCD64A1 [@Giglio2018], whose omission and commission characteristics
[@Boschetti2019] bound every model evaluated here. (iv) The analysis cells approximate, but are not
co-registered with, the native MODIS sinusoidal grid (Section 3.2). They are also not square on the
ground: about 510 m north to south but 390 to 407 m east to west, giving 0.199 to 0.208 km² against
a MODIS cell's 0.250 km². Two things follow. The block sizes quoted throughout as about 1, 5 and
10 km are the north-south dimension, so blocking is weaker in longitude by roughly a fifth. And the
smaller, offset cell dilates the labelled burned footprint relative to MCD64A1, which compounds
(xiv). (v) Even after the AOI
extension, Evia's TSG prevalence (0.287) remains the highest of the five regions. It is four to
seven times that of Manavgat, Bejís and Muğla (0.038 to 0.072), though only modestly above
Montiferru, whose modelled-population prevalence is 0.212. Prevalence sensitivity was checked for
transfer (Section 4.7a), but Evia remains the most imbalance-atypical population. (vi) Each region
contributes one fire season, so regional
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
structure, ignition and suppression history, and terrain-driven fire behaviour. (x) The
interval-support counts are less stable than the point estimates behind them. Several verdicts sit
within a thousandth of their reference value. At 1 km blocking the published split of ten positive,
seven negative and three uncertain paired deltas turns on a lower bound of −0.00045 for Bejís to
Manavgat, and a different random stream gives eleven, seven and two. The point estimates and the
sign pattern are stable; the counts are not. Every sentence in this paper that leans on an exact
count of supported directions should be read at that precision.

Five further limitations concern the observational layer, and they were added after an internal
review found the paper strong on modelling and thin on provenance. (xi) **The within-region
increment carries a compositing tolerance.** Three defensible Landsat compositing chains, run on an
identical Manavgat cohort with an identical baseline, give increments of +0.045, +0.064 and +0.084
(Section 4.7i). The tolerance is about ±0.02 AUC, comparable to the cross-version tolerance of (vii)
and wider than the 1 km interval of Table 3. It never approaches the increment itself, which stays
supported under all three chains, and it was audited for one region only; the other four are
unaudited on this axis. The same dependence explains the window-closure behaviour of Section 5.8.
(xii) **The thermal block is six predictors but not six independent measurements.** `fused_lst`
equals observed LST outside a gap-filled share of 0.11 % to 9.70 %, `downscaled_lst` is a fitted
surface whose dominant input is the MODIS context layer in two regions, NDVI in two and slope in
Muğla, and a single subgroup recovers 71 % to 99 % of the whole block's increment in every region
(Section 4.7h). The six reversal tests of Section 4.4 are therefore not six independent probes of
concept shift. Two related concerns have since been tested and neither survives as a threat to the
increment. Restricting to cells with a gap-filled fraction of at most 0.10 leaves the increment
bootstrap-supported in all five regions; Bejís moves the most, from +0.056 to +0.043, and the other
four by at most 0.008 (Section 4.7m). And dropping the two derived channels, which carry a
coordinate-derived component from the downscaler's own inputs (summed importance 0.035 to 0.123) and
are the one route by which coordinates re-enter a feature set from which Section 3.13 excludes them,
retains 82 % to 103 % of the increment, with every interval still excluding zero (Section 4.7h). What remains true is the redundancy itself:
the block is six predictors but not six independent measurements. (xiii) **The MODIS input behind the two derived
channels is quality-screened in two regions and unscreened in three.** Evia and Montiferru apply a
`QC_Day` mask, a three-observation minimum and an explicit nodata sentinel. Manavgat, Bejís and
Muğla apply none of these, so cells with nothing to report enter as exact 0.0 °C. Those zeros were
measured for this paper: 8.11 % of pixels in Manavgat, **38.29 % in Muğla** and **none in Bejís**,
each tracking that AOI's water share almost exactly, so the zero-fill is sea rather than missing
observation (Section 3.4). Muğla's share is more than four times Manavgat's and both exceed the
pipeline's own 5 % guard. The split follows export
date, not design, so it is confounded with nothing in the study and with everything about when each
region was run. Three of the five regions are on the unscreened path, Manavgat among them, and
Manavgat is the subject of the unexplained behaviour in (ix). This is a candidate explanation that
we have not been able to test, since rebuilding Step 7 on one common contract is upstream of this
analysis. An earlier version of this paper attributed the anomaly instead to Manavgat using a
four-year summer-mean MODIS layer. That was read from a stale metadata string and is withdrawn;
all five regions used single-season predictor-window layers (Section 3.4). (xiv) **Label noise is spatially structured and its
interaction with the predictors is untested.** The cell's representative burn date is the mode of its
positive sub-pixel dates, and because the exported raster holds no out-of-window positives, a single
in-window positive sub-pixel labels a cell burned in this dataset (Section 3.2). No agreement
threshold is imposed, so the proportion of cells labelled on thin evidence
scales with each scar's perimeter-to-area ratio, which differs sharply across these regions
(effective component counts 1.0 to 4.05). Fringe cells also differ systematically in terrain from
core cells, which makes differential fringe contamination a competing explanation for a reversal in
a terrain variable. The `burn_date_pixel_agreement_fraction` column needed to test this is recorded
and hard-excluded from the features, and the sensitivity restricting to high-agreement cells was not
run. At the product level, MCD64A1's omission at 500 m in fragmented Mediterranean terrain is itself
correlated with patch size, terrain and land-cover fragmentation, which are the baseline predictors;
no second label product was used as a control. (xv) **Two safeguards did not run everywhere.** The
pre-label burn exclusion ran for Muğla, Evia and Montiferru, is recorded as not run for Manavgat, and
has no recorded status for Bejís (Section 3.2). Prior-year burning is screened for no region in the
five-region cohort; the only historical-burn exclusion in the study removes the 2021 Muğla scar from
the 2022 event-relative experiment of Section 3.16.4. The exposure this leaves cannot be quantified
from the archive, and an earlier version of this paper wrongly described doing so as a cheap query.
It is not: both the working and the raw MCD64A1 rasters in the export are clipped to each region's
label window, with zero positive sub-pixels anywhere in any predictor window, so a pre-label
detection leaves no trace to count. Measuring the exposure needs MCD64A1 re-exported unclipped,
which is an upstream re-run. In the same vein, the per-region acquisition inventory behind the composites exists for
Manavgat alone.

Four analyses were named in an earlier version of this section as the ones that would close most of
the above. **Two have since been run and are reported here rather than promised.** The common-edge
TVDI, fitted once across the pooled land pixels of all five regions, does not bring the directions
into agreement, so the index's scene dependence is not the explanation for its reversal (Section
4.7k). The signed univariate AUCs recomputed on high-agreement cells only leave the elevation
reversal intact at every threshold, so differential fringe contamination is not the explanation
either (Section 4.7l). A third, the calendar-matched Muğla 2022 arm, was attempted and **cannot be
run at all**: the two Muğla events are 42 days apart in seasonal phase and neither year holds a
second event at the other's phase, so the calendar-matched window carries nine burned cells against
a gate minimum of thirty (Section 5.2). That is a limit of the fire record rather than of effort,
and it is now stated as one. Only the compositing A/B extended to a second region remains genuinely
outstanding.

<!-- DRAFT NOTES:

(a) [TO VERIFY] / [CITATION NEEDED] items:
    1. §5.3 — RESOLVED 2026-08-08: @Schoener1968 (Ecology 49(4):704-726, doi 10.2307/1935534)
       and @Warren2008 (Evolution 62(11):2868-2883, doi 10.1111/j.1558-5646.2008.00482.x) both
       verified via Crossref REST API and added to REFERENCES.bib (Block G); inline citation
       placed in §5.3.
    2. §5.5 — CLOSED 2026-08-13 (see COORDINATOR REVIEW item 2 and REFEREE ROUND item 10 below).
       The pointer names Supplementary S1 and the wording now reads "No number from it is used in
       this Discussion", which does not contradict the Conclusions, where S1 is used
       substantively. No few-shot numbers were introduced here.
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
      both directions). [TO VERIFY] CLOSED 2026-08-13. The literal AoA-inside numbers now exist
      and are written into §5.3 from paper/referee_round_numbers.md §1 (Table A1), which reads
      drive_new/diagnostics/marginal_aoa_completion/4b2a1c86.../comparison/
      marginal_diagnostics_with_transfer.csv by header name with a quote-aware parser.
      Manavgat→Muğla: 0.8752 weighted AoA (highest in the matrix), 0.9640 unweighted support,
      transfers 0.4702. Muğla→Manavgat: 0.5305 / 0.9702 (highest unweighted), transfers 0.4010.
      Muğla→Bejís: 0.0050 weighted, transfers 0.5832 above chance. The §1.3 forward reference is
      now closed on literal numbers, not only on the domain-classifier ceiling. SCOPE: the AoA
      file covers 12 of 20 directions and has nothing for Montiferru, so §5.3 states that the
      Bejís/Montiferru half of the contrast pair has no applicability value.
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
      in §5.6 (stated null confirmed; grouping intuition wrong). Wording aligned 2026-08-13 to
      03 §3.14.1: analysis-log entry, not a formal pre-registration.
    - 02 §2.5 / OUTLINE §1.5: the Dimarco contrast → §5.9, now with four bounding differences
      (the fourth added 2026-08-13: our own baseline's transfer performance).
    STILL OPEN (not closable in Discussion):
    - 01 §1.5 contribution-claim placeholders still read "pending results" — must be filled at
      assembly from 04.
    - RESOLVED 2026-08-08: the 11 METHODS GAPS are closed (03_methods §3.14–§3.16 + §3.1
      Table 1 update); §5.8 now rests on §3.16.3 and §5.11(iv) on §3.2's existing text.
    - Few-shot supplementary — CLOSED 2026-08-13, see item (a)2.

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

REFEREE ROUND (2026-08-13). Eight tasks, all in 05_discussion only. Sources: three verified
reports read first, paper/referee_round_numbers.md, paper/transfer_ci_blocksize.md and
paper/diagnostics_common_subset.md. 04_results.md was NOT read this round (another agent held
it). No number entered that is not in those reports, with the two exceptions noted at item 9.
    1. §5.1 restated at the conservative blocking. It now leads with the blocking-invariant
       facts (point estimates unchanged, no direction changes side of the chance line, only
       support weakens), then gives 10-cell counts first and 2-cell second. Level: 9 above /
       3-4 below / 7-8 uncertain at 10-cell against 12 / 6 / 2 at 2-cell. Paired delta: 6 / 4 /
       10 at 10-cell against 10 / 7 / 3 at 2-cell, with the sign pattern (12 positive, 8
       negative point deltas, range -0.148 to +0.132) stated as invariant. The swing-factor
       claim was moved to the point estimate (drags 3 below, lifts 1 above), which is
       blocking-independent, rather than left resting on 2-cell CI verdicts.
       Source: transfer_ci_blocksize.md Parts 1-2 and its summary table; referee_round_numbers.md
       Table A6 for the point-estimate counts and the direction lists.
    2. §5.2 counts fixed. "below chance with interval support in six directions" became six at
       the point estimate, 3-4 CI-supported at 10-cell and 6 at 2-cell, with Evia→Bejís named as
       the borderline case (its 10-cell upper bound runs 0.497, 0.501, 0.504, 0.500, 0.500 over
       seeds 42-46). The same fix applied at the Muğla two-event paragraph and, as a support
       qualifier, at §5.6's Bejís/Evia regime-similar pair.
    3. §5.2 new paragraph (task 7): the two-Muğla-events result licenses the sharper reading
       that a within-region ROC-AUC estimates interpolation inside one fire season's footprint,
       illustrated by the 2022 thermal within-region AUC of 0.942 on 331 burned cells forming
       one scar, and connected to §5.10. Constraint stated: one region, two events, so an
       observation and not an established general property. INTERPRETIVE, for coordinator
       review. The 0.942 figure is not in the three referee reports; it was read from
       paper/mugla_transfer_raw/emrehan_run_20260809/step10/step10_bootstrap_summary.json
       (roc_auc__within_thermal, median 0.94244, mean 0.94168) and it matches 04 Table R9.
    4. §5.3 given its literal AoA evidence; see (c) above for the closed [TO VERIFY].
       CONFLICT WITH THE BRIEF, resolved in favour of the sources: the brief says Manavgat→Muğla
       transfers "with its interval entirely below chance". That is true at 2-cell blocking
       ([0.454, 0.486]) but NOT at the 10-cell blocking this round adopts, where it is
       [0.415, 0.524], i.e. no verdict (transfer_ci_blocksize.md Part 1). §5.3 therefore states
       both directions below chance at the point estimate, with Muğla→Manavgat CI-supported at
       both blockings and Manavgat→Muğla supported at 1 km only. For the same reason the
       Bejís/Montiferru half of the contrast pair is now stated as above chance in both
       directions with support at 1 km and no verdict at 5 km, and 02's SDM sentence no longer
       claims "interval support on both halves of a counterexample pair".
    5. §5.4 given the three defences: multiplicity (20 variants, 19 computable, 10 unordered
       pairs, 2 intervals exclude zero, no FWER control, the two pre-specification mitigations,
       and the open statement that the unrestricted cosine-over-nine reaches rho = +0.50 with an
       interval spanning zero); near-tautology (answered, not deflected: the diagnosis is
       mechanistic, the empirical content is that the marginal instruments miss what the
       conditional one sees on the same pairs); and the common-subset rerun (12 directions, 6
       pairs, the two supported-conditional rows still the only ones excluding zero at
       +0.87 [+0.65, +0.88] and +0.85 [+0.43, +0.88], all 18 others spanning zero), with the
       coarseness caveat the source insists on (three distinct values, still needs target
       labels). Sources: diagnostics_common_subset.md §2 and §4; 03 §3.14.1 for the multiplicity
       and provenance wording. The +0.50 value is the published cosine_9 row of
       paper/all_diagnostics_vs_transfer.csv (0.5042 [-0.1668, +0.8253], n = 20); it is not in
       the three referee reports and was verified against that file directly.
    6. §5.4 Bejís/Montiferru exclusion promoted from a clause to the paragraph's opening claim,
       and tied explicitly to §5.3's headline contrast.
    7. §5.6 title and wording aligned to 03 §3.14.1: "stated" rather than "pre-registered", an
       analysis-log entry, no independent timestamped registration, records entered version
       control on the computation date. Substance unchanged. §5.7's back-reference updated.
    8. §5.7 opening count corrected: "Eight measures were specified and eight failed" was a
       leftover count of the label-free marginal measures. It now reads 20 variants across four
       families of which two, both conditional, ordered the matrix. The argument for excluding
       meteorology from the candidate set is unchanged.
    9. §5.9 repaired. Our own baseline's transfer performance is now stated openly (mean
       ROC-AUC 0.5371 over 20 directions, 4 below chance at the point estimate with intervals
       entirely below it at 1 km blocking; referee_round_numbers.md Table A6) against Dimarco's
       every transfer exceeding 0.80, and the contrast is reframed as thin place-descriptor set
       plus dynamic block against rich place-descriptor set. The predictor-class claim is now
       stated as a reading. "Bracket the predictor-class explanation" softened to "consistent
       with" (supersedes item (b)7's description).
   10. §5.11: (v) Montiferru prevalence 0.225 → 0.212 modelled population (the published figure
       was counted before the valid_for_modeling filter; referee_round_numbers.md Table A5),
       "marginally" → "modestly"; the 4-7x comparison with Evia's 0.287 is unaffected. New item
       (x) on interval-support count fragility, including the -0.00045 lower bound for
       Bejís→Manavgat that decides the published 2-cell 10/7/3 split
       (transfer_ci_blocksize.md Part 2). §5.5's few-shot sentence reworded to "No number from
       it is used in this Discussion" so that it does not read as contradicting the Conclusions,
       which now use S1 substantively. No S1 number was imported.
   11. LEFT UNCHANGED, deliberately: the two mis-rounded Table 4 cells and the "four times too
       narrow" caveat (transfer_ci_blocksize.md, "Two things to record for the Results agent")
       belong to 04 and were not touched. §5.5's 7-of-12 negative-recovery count and §5.1's
       0.184 shortfall, 0.431-0.630 adapted range and +0.004 mean delta are unaffected by
       blocking and stand. The decomposition percentages and the CORAL-lambda material are
       untouched.
-->
