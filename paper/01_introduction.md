# 1. Introduction

> **Drafting notes.**
> 1. **The thesis of this section changed.** It no longer leads with "does pre-fire thermal state add
>    skill within a region". It leads with the **local-skill / portability trade-off**: adding
>    dynamic state predictors buys within-region skill at the cost of between-region portability,
>    and that cost is invisible to the marginal, predictor-space-distance diagnostics the field
>    currently relies on. The within-region increment is retained as the *first half of the
>    trade-off*, i.e. supporting evidence, not the headline.
> 2. **No result numbers appear in this section.** Contribution claims are placeholders whose
>    *framing* is fixed but whose *magnitudes* stay open until Results are final.
> 3. **Claim strength has been narrowed** to match the adversarial novelty audit in
>    `LITERATURE.md`. This section does not say the transferability of pre-fire dryness has "never
>    been tested" (Gelabert et al. come close), does not treat shift decomposition as unprecedented
>    in remote sensing (Huang et al. do it), and states the similarity result as one of
>    **sufficiency**, never as a correlation across pairs.
> 4. The "self-calibrating satellite thermal digital twin" framing is motivation only — one
>    sentence — and is never presented as an achievement.
> 5. Citations use `[@BibKey]` against `paper/REFERENCES.bib`; all were verified against Crossref
>    on 2026-07-23. Remaining gaps are marked `[UNVERIFIED: ...]` and carry no citation.

---

Wildfire is a defining disturbance of Mediterranean-basin landscapes, and a changing climate is
reshaping where and how it burns [@Pausas2021]. The pressure to anticipate *where* fire will occur
has produced a large and still-growing literature on fire susceptibility mapping, recently
synthesised from both a methodological and an application perspective [@Vibhandik2026;
@Jodhani2026]. The dominant pattern is well established: assemble geospatial predictors over a study
region, pair them with a historical record of burned area, fit a supervised classifier — most often
a random forest [@Breiman2001] — and publish the resulting susceptibility surface with a
cross-validated AUC in the 0.85 to 0.95 range.

This paper is about a cost that pattern does not price. Predictors describing the *state* of a
surface in a particular season are more informative about that season than predictors describing a
place; they are also, we argue and then show, less portable, because the relationship they carry is
locally reparameterised — it exists everywhere and points in different directions in different
places. The claim we advance is a trade-off rather than a dismissal: **dynamic state predictors buy
local skill at the cost of portability**, and in its sharpest form, **the feature block that gains
the most within a region is the block that loses the most between regions.**

## 1.1 The trade-off goes unpriced because portability goes unmeasured

A susceptibility model's reported skill is almost always an estimate of *within-region* performance:
held-out folds come from the same study area, season and often the same fire event, and where they
are drawn at random over cells, spatial autocorrelation inflates the estimate further — a problem
documented across ecological modelling [@Roberts2017; @Ploton2020] and addressed by spatially
blocked cross-validation [@Valavi2019; @Meyer2018]. Controlling autocorrelation makes the
within-region estimate honest; it says nothing about whether the fitted relationship holds elsewhere.
Because only that side of the ledger is routinely reported, the trade-off is structurally invisible:
a predictor block is adopted on the strength of the increment it delivers inside its training
footprint, and the portability it consumes is never entered as a debit — even though any regional
product built from locally trained models implicitly promises generalisation beyond that footprint.

For fire specifically, the transfer question is asked far less often than in adjacent fields.
Meteorologically derived fire-danger indices are known not to port cleanly between fire environments
[@Podschwit2022], while two recent studies test model transfer systematically — across Mediterranean
countries [@Dimarco2026] and US counties [@Liu2025] — and both report that it largely succeeds
between similar regions. Crucially, both
transfer models whose dominant predictors are *spatially stationary*: terrain, human modification,
night-time lights, population density, long-term reanalysis climatologies. Each describes a place
rather than a season, which is exactly the class our thesis expects to travel well. In species
distribution modelling, where transferability has been examined far more systematically [@Yates2018],
two studies report that geographic and environmental similarity do *not* reliably predict transfer
success [@Vesk2021; @Rousseau2022].

## 1.2 The pre-fire thermal block is the natural test case

The dynamic predictor class we use is pre-fire thermal dryness: under-exploited relative to static
terrain and fuel, and the class most plausibly *expected* to transfer. The standard susceptibility
predictors — terrain, land cover or fuel type, vegetation greenness,
long-term climatology, proximity to roads and settlements — are static or near-static over the
timescale at which fire danger varies, and cannot by construction explain why a particular summer
burned and the preceding one did not. What changes between those summers is the state of the
surface: fuel dryness, vegetation moisture stress, and how anomalously hot the land surface has
become relative to its own climatological baseline. Satellite thermal observation gives direct,
repeated access to part of that state through fuel moisture content [@Yebra2013]; the pairing used
here — surface temperature with a vegetation index — was established as a live-fuel-moisture
estimator for fire-danger rating by Chuvieco et al. [@Chuvieco2004], and the Temperature-Vegetation
Dryness Index [@Sandholt2002] formalises that feature space into an internally normalised measure,
in principle less exposed to absolute-temperature offsets between regions than raw land surface
temperature — a theoretical portability advantage this study tests empirically.

That pre-fire thermal state carries genuine information about subsequent fire is established
[@Maffei2018; @MaffeiMenenti2019; @Maffei2021], and Gelabert et al. [@Gelabert2025] found dead fine
fuel moisture and its yearly anomalies to be the most influential predictor of human-caused ignition
likelihood across Europe, testing generalisation by pooled fitting with per-site evaluation. What
has not been established is whether the *predictive skill* of a pre-fire thermal classifier trained
in one fire region survives strict, label-free application to another.

Because the physics linking moisture stress to combustion is universal, this is the predictor class
for which portability should be *most* expected, which is what makes it diagnostic: a loss here
cannot be dismissed as a peculiarity of a locally defined covariate. It is also the class on which a
self-calibrating satellite thermal monitoring system would have to be built — the long-run
motivation for this work rather than anything it demonstrates.

## 1.3 Why the loss is invisible: marginal distance versus conditional reversal

If a model trained in one region underperforms in another, the deficit can arise from two very
different mechanisms. Under **covariate shift** the marginal distribution of the predictors differs
while the predictor-response relationship is preserved; this is in principle correctable without
target labels, by per-region standardisation or covariance alignment such as CORAL [@Sun2016], and
such adaptation has an established remote-sensing literature [@Tuia2016]. Under **concept shift** the
conditional relationship itself changes: a predictor positively associated with burning in one
region is negatively associated with it in another. No label-free realignment of input distributions
can repair a sign reversal, because the information needed to detect it is exactly the information
being withheld. The taxonomy is canonical [@MorenoTorres2012] and has begun to be operationalised in
applied remote sensing: Huang et al. [@Huang2026] decompose domain shift for hyperspectral
foliar-trait retrieval and find concept shift dominant.

This distinction is what makes the trade-off hard to see. The field's principal transferability
diagnostic is the area of applicability of Meyer and Pebesma [@Meyer2021], with the assessment
critique [@Meyer2022] and the global-model audit of Ludwig et al. [@Ludwig2023] built on the same
construction: transferability is judged by *dissimilarity in predictor space* between the prediction
location and the training distribution. That is a **marginal** quantity — a statement about where
the predictors live, computed without reference to the response. It is a well-founded instrument for
the failure mode it was designed for, and we use it as such. But by construction it cannot register
a failure in which the predictor distributions overlap acceptably while the conditional
predictor-response relationship has changed sign: two regions can be mutually inside each other's
area of applicability and still be mutually unpredictable. We therefore extend this line of work
rather than contradict it — computing the marginal diagnostics, reporting what they do and do not
order, then supplying a **conditional** diagnostic for what they miss.

## 1.4 Objectives

This study evaluates the local-skill / portability trade-off for dynamic pre-fire thermal predictors
in Mediterranean wildfire regions, under a strict train-in-A, apply-to-B protocol. Four questions
follow.

**Q1 — The trade-off.** Is the feature block that contributes the most within-region skill also the
block that costs the most between-region skill? We answer with a paired static-versus-dynamic
transfer contrast across all ordered region pairs. Two subordinate questions supply the first half
of the trade-off and are supporting evidence rather than findings in their own right: whether the
thermal block improves burned-area discrimination beyond a matched static baseline within a region,
and whether that improvement survives progressively coarser spatial blocking.

**Q2 — Sufficiency of similarity.** Are geographic and bioclimatic similarity *sufficient* for
transfer? We pose this as a sufficiency question, which a single strong counterexample settles, not
as a claim about correlation across pairs, which our number of pairs would not support.

**Q3 — Recoverability without labels.** Where transfer fails, how much of the deficit is
label-correctable covariate shift and how much is residual concept shift? We define the recoverable
fraction operationally — what the best available label-blind alignment actually recovers — and the
residual as what it demonstrably cannot, reporting the resulting method dependence rather than
concealing it.

**Q4 — Diagnosis.** Do marginal, predictor-space-distance diagnostics of the area-of-applicability
family order the observed transfer performance? And does a conditional diagnostic — signed reversal
in the univariate association between a predictor and burning, between source and target — track it
where the marginal ones do not?

The evaluation standard throughout is deliberately conservative: the unit of analysis is the native
cell of the burned-area product; cross-validation is spatially blocked and repeated at several block
sizes; uncertainty comes from a spatial-block bootstrap; the primary population excludes cropland
and bare surfaces so that stubble burning cannot masquerade as wildfire skill; and every column
carrying label information is hard-excluded from every feature set. These choices lower the headline
numbers, which is the point.

## 1.5 Contributions

The claims below are ordered by weight and stated at the strength the evidence supports, with the
nearest prior work named inside each claim rather than omitted.

**Contribution 1. The local-skill / portability trade-off, quantified per direction.** We
quantify, for every ordered region pair, the change in transfer skill attributable to adding the
dynamic pre-fire thermal block to a matched static baseline, and set it against the
within-region increment the same block delivers. The block worth +0.056 to +0.153 ROC-AUC inside
every region contributes +0.004 on average across the twenty ordered transfer directions —
improving ten with bootstrap support and degrading seven — and is the swing factor at the chance
line, dragging three directions below chance and lifting one above it. This is the paper's
thesis: the block that gains the most locally is the block whose between-region contribution is
sign-unstable. Dimarco et al. [@Dimarco2026] transfer a predominantly spatially stationary
predictor set successfully across a comparable Mediterranean design; our result is the
complementary half of that picture rather than a contradiction of it.

**Contribution 2. Label-free alignment does not recover transfer — it compresses it.** We test
region-wise standardisation and covariance alignment [@Sun2016] as label-blind remedies on all
twenty directions. Adaptation compresses the transfer matrix towards chance: it recovers at most
34 % of the deficit where transfer fails, and produces *negative* recovery in seven of twelve
decomposed directions — degrading every direction that already transferred, in the worst case by
−0.86 of the gap. We found no prior application of covariance alignment to fire susceptibility,
fire occurrence or burned-area prediction. This is a negative result reported with a mechanism,
not an absence.

**Contribution 3. Similarity — geographic, climatic or environmental — is not sufficient for
transfer.** Manavgat and Muğla, in the same country and fire year, roughly 200 km apart and with
the highest burned-niche overlap of any pair in the matrix, fail in both directions with
bootstrap intervals entirely below chance; Bejís and Muğla, in different countries and years and
~2500 km apart, transfer above chance in both directions, as do Bejís and Montiferru, the pair
with the *lowest* niche overlap. The claim is one of *sufficiency*, established by coexisting
counterexamples and independent of the number of pairs available. We present it as a
contribution to a live disagreement — the fire literature expects similarity to predict transfer
[@Dimarco2026; @Liu2025], the species distribution modelling literature has found it does not
[@Vesk2021; @Rousseau2022] — not as a settled general law. Dimarco et al. reach a compatible
conclusion from the opposite direction, attributing their weakest transfer to non-climatic
factors rather than bioclimatic distance.

**Contribution 4. The failure is conditional, and only a conditional diagnostic sees it.** We
evaluate twenty candidate transferability diagnostics from four families against the observed
transfer outcomes under one bootstrap framework: area-of-applicability-style predictor-space
dissimilarity [@Meyer2021; @Meyer2022; @Ludwig2023], climatic and geographic distance, learned
domain separability, canonical niche-overlap statistics and burn-pattern regime distances all
fail to order the matrix — the domain classifier is at ceiling (AUC ≥ 0.96) for every pair. The
only two diagnostics whose intervals exclude zero measure conditional direction agreement:
whether each predictor's signed association with burning points the same way in both regions
(Spearman ρ = +0.84 and +0.81). Because signed associations require burned labels in both
regions, this is a mechanism diagnosis — the failure invisible to marginal diagnostics is
visible in the conditional structure — not a label-free screening tool; paired with label-blind
adaptation performance as an instrument for splitting recoverable from irreducible shift, it is
the constructive contribution that makes the paper more than a negative result. Shift
decomposition in applied remote sensing is not itself new [@Huang2026]; what we add is the fire
application, the adaptation-as-instrument formulation, and the explicit head-to-head of marginal,
niche-overlap and conditional diagnostics on the same pairs.

**Contribution 5. Within-region replication of the thermal increment.** We replicate the
increment across five independent Mediterranean regions under spatially blocked
cross-validation: ΔAUC +0.056 to +0.153, every bootstrap interval above zero, in both analysis
populations, surviving spatial blocks up to ~10 km and a predictor window closed up to 14 days
earlier. The finding is not itself novel — comparable within-region results exist for these
landscapes [@AlkanAkinci2023; @Iban2022] — and it is included as the evidence for the first half
of Contribution 1.

Alongside these we release a leakage-audited, spatially blocked evaluation and transfer protocol
with code, configuration and frozen outputs, so that a negative transfer result can be checked
rather than taken on trust — which matters given evidence that wildfire transfer conclusions are
sensitive to evaluation design and task formulation [@Xu2026].

Section 2 reviews the relevant literature. Section 3 describes the study regions, the data and the
full modelling, cross-validation, transfer and adaptation protocol. Section 4 reports results;
Section 5 discusses them, including limitations; Section 6 concludes.
