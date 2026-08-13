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
> 6. **Style pass 2026-08-13** (`paper/STYLE.md`): no dashes, short sentences, passive where it
>    reads naturally, plain words. Every number, citation and hedge is unchanged. Note 4 above still
>    describes the old one-sentence construction; the framing is now two short sentences.

---

Wildfire is a defining disturbance of Mediterranean-basin landscapes, and a changing climate is
reshaping where and how it burns [@Pausas2021]. The pressure to anticipate *where* fire will occur
has produced a large and still-growing literature on fire susceptibility mapping. It has recently
been synthesised from both a methodological and an application perspective [@Vibhandik2026;
@Jodhani2026]. The dominant pattern is well established. Geospatial predictors are assembled over a
study region and paired with a historical record of burned area. A supervised classifier is then
fitted, most often a random forest [@Breiman2001]. The resulting susceptibility surface is published
with a cross-validated AUC in the 0.85 to 0.95 range.

This paper is about a cost that the pattern does not price. Predictors that describe the *state* of
a surface in a particular season are more informative about that season than predictors that
describe a place. They are also less portable, as we argue and then show. The relationship they
carry is reparameterised locally. It exists everywhere, but it points in different directions in
different places. The claim advanced here is a trade-off and not a dismissal: **dynamic state
predictors buy local skill at the cost of portability**. In its sharpest form, **the feature block
that gains the most within a region is the block that loses the most between regions.**

## 1.1 The trade-off goes unpriced because portability goes unmeasured

A susceptibility model's reported skill is almost always an estimate of *within-region* performance.
Held-out folds come from the same study area and season, and often from the same fire event. Where
folds are drawn at random over cells, spatial autocorrelation inflates the estimate further. The
problem is documented across ecological modelling [@Roberts2017; @Ploton2020] and is addressed by
spatially blocked cross-validation [@Valavi2019; @Meyer2018]. Controlling autocorrelation makes the
within-region estimate honest. It says nothing about whether the fitted relationship holds
elsewhere.

Because only that side of the ledger is routinely reported, the trade-off is structurally invisible.
A predictor block is adopted on the strength of the increment it delivers inside its training
footprint. The portability it consumes is never entered as a debit. Yet any regional product built
from locally trained models implicitly promises generalisation beyond that footprint.

For fire specifically, the transfer question is asked far less often than in adjacent fields.
Meteorologically derived fire-danger indices are known not to port cleanly between fire environments
[@Podschwit2022]. Two recent studies test model transfer systematically, across Mediterranean
countries [@Dimarco2026] and US counties [@Liu2025], and both report that it largely succeeds
between similar regions. Both, crucially, transfer models whose dominant predictors are *spatially
stationary*: terrain, human modification, night-time lights, population density and long-term
reanalysis climatologies. Each of these describes a place rather than a season, which is exactly the
class our thesis expects to travel well. In species distribution modelling, transferability has been
examined far more systematically [@Yates2018]. Two studies there report that geographic and
environmental similarity do *not* reliably predict transfer success [@Vesk2021; @Rousseau2022].

## 1.2 The pre-fire thermal block is the natural test case

The dynamic predictor class used here is pre-fire thermal dryness. It is under-exploited relative to
static terrain and fuel, and it is the class most plausibly *expected* to transfer. The standard
susceptibility predictors are terrain, land cover or fuel type, vegetation greenness, long-term
climatology, and proximity to roads and settlements. All of them are static or near-static over the
timescale at which fire danger varies. By construction they cannot explain why a particular summer
burned and the preceding one did not.

What changes between those summers is the state of the surface: fuel dryness, vegetation moisture
stress, and how anomalously hot the land surface has become relative to its own climatological
baseline. Satellite thermal observation gives direct and repeated access to part of that state
through fuel moisture content [@Yebra2013]. The pairing used here is surface temperature with a
vegetation index. It was established as a live-fuel-moisture estimator for fire-danger rating by
Chuvieco et al. [@Chuvieco2004]. The Temperature-Vegetation Dryness Index [@Sandholt2002] formalises
that feature space into an internally normalised measure. In principle it is less exposed to
absolute-temperature offsets between regions than raw land surface temperature. That theoretical
portability advantage is tested empirically here.

That pre-fire thermal state carries genuine information about subsequent fire is established
[@Maffei2018; @MaffeiMenenti2019; @Maffei2021]. Gelabert et al. [@Gelabert2025] found dead fine fuel
moisture and its yearly anomalies to be the most influential predictor of human-caused ignition
likelihood across Europe, testing generalisation by pooled fitting with per-site evaluation. What
has not been established is whether the *predictive skill* of a pre-fire thermal classifier trained
in one fire region survives strict, label-free application to another.

The physics linking moisture stress to combustion is universal. Portability should therefore be
*most* expected for this predictor class, which is what makes it diagnostic. A loss here cannot be
dismissed as a peculiarity of a locally defined covariate. It is also the class on which a
self-calibrating satellite thermal monitoring system would have to be built. That system is the
long-run motivation for this work rather than anything it demonstrates.

## 1.3 Why the loss is invisible: marginal distance versus conditional reversal

If a model trained in one region underperforms in another, the deficit can arise from two very
different mechanisms. Under **covariate shift** the marginal distribution of the predictors differs
while the predictor-response relationship is preserved. This is in principle correctable without
target labels, by per-region standardisation or by covariance alignment such as CORAL [@Sun2016].
Such adaptation has an established remote-sensing literature [@Tuia2016]. Under **concept shift**
the conditional relationship itself changes. A predictor positively associated with burning in one
region is negatively associated with it in another. No label-free realignment of input distributions
can repair a sign reversal, because the information needed to detect it is exactly the information
being withheld. The taxonomy is canonical [@MorenoTorres2012], and it has begun to be
operationalised in applied remote sensing. Huang et al. [@Huang2026] decompose domain shift for
hyperspectral foliar-trait retrieval and find concept shift dominant.

This distinction is what makes the trade-off hard to see. The field's principal transferability
diagnostic is the area of applicability of Meyer and Pebesma [@Meyer2021]. The assessment critique
[@Meyer2022] and the global-model audit of Ludwig et al. [@Ludwig2023] are built on the same
construction. Transferability is judged by *dissimilarity in predictor space* between the prediction
location and the training distribution. That is a **marginal** quantity, a statement about where the
predictors live, computed without reference to the response. It is a well-founded instrument for the
failure mode it was designed for, and it is used as such here. By construction, however, it cannot
register a failure in which the predictor distributions overlap acceptably while the conditional
predictor-response relationship has changed sign. Two regions can be mutually inside each other's
area of applicability and still be mutually unpredictable. This line of work is therefore extended
rather than contradicted. The marginal diagnostics are computed, what they do and do not order is
reported, and a **conditional** diagnostic is supplied for what they miss.

## 1.4 Objectives

This study evaluates the local-skill and portability trade-off for dynamic pre-fire thermal
predictors in Mediterranean wildfire regions, under a strict train-in-A, apply-to-B protocol. Four
questions follow.

**Q1. The trade-off.** Is the feature block that contributes the most within-region skill also the
block that costs the most between-region skill? The answer comes from a paired
static-versus-dynamic transfer contrast across all ordered region pairs. Two subordinate questions
supply the first half of the trade-off, and they are supporting evidence rather than findings in
their own right. The first is whether the thermal block improves burned-area discrimination beyond a
matched static baseline within a region. The second is whether that improvement survives
progressively coarser spatial blocking.

**Q2. Sufficiency of similarity.** Are geographic and bioclimatic similarity *sufficient* for
transfer? This is posed as a sufficiency question, which a single strong counterexample settles. It
is not posed as a claim about correlation across pairs, which our number of pairs would not support.

**Q3. Recoverability without labels.** Where transfer fails, how much of the deficit is
label-correctable covariate shift and how much is residual concept shift? The recoverable fraction
is defined operationally, as what the best available label-blind alignment actually recovers. The
residual is what that alignment demonstrably cannot recover. The resulting method dependence is
reported rather than concealed.

**Q4. Diagnosis.** Do marginal, predictor-space-distance diagnostics of the area-of-applicability
family order the observed transfer performance? And does a conditional diagnostic track it where the
marginal ones do not? The conditional diagnostic is the signed reversal, between source and target,
in the univariate association between a predictor and burning.

The evaluation standard throughout is deliberately conservative. The unit of analysis is the native
cell of the burned-area product. Cross-validation is spatially blocked and repeated at several block
sizes. Uncertainty comes from a spatial-block bootstrap. The primary population excludes cropland
and bare surfaces, so that stubble burning cannot masquerade as wildfire skill. Every column
carrying label information is hard-excluded from every feature set. These choices lower the headline
numbers, which is the point.

## 1.5 Contributions

The claims below are ordered by weight and stated at the strength the evidence supports. The nearest
prior work is named inside each claim rather than omitted.

**Contribution 1. The local-skill and portability trade-off, quantified per direction.** For every
ordered region pair, the change in transfer skill from adding the dynamic pre-fire thermal block to
a matched static baseline is quantified and set against the within-region increment the same block
delivers. The block is worth +0.056 to +0.153 ROC-AUC inside every region. Across the twenty ordered
transfer directions it contributes +0.004 on average, improving ten with bootstrap support and
degrading seven. It is also the swing factor at the chance line, dragging three directions below
chance and lifting one above it. This is the paper's thesis: the block that gains the most locally
is the block whose between-region contribution is sign-unstable. Dimarco et al. [@Dimarco2026]
transfer a predominantly spatially stationary predictor set successfully across a comparable
Mediterranean design. Our result is the complementary half of that picture rather than a
contradiction of it.

**Contribution 2. Label-free alignment does not recover transfer. It compresses it.** Region-wise
standardisation and covariance alignment [@Sun2016] are tested as label-blind remedies on all twenty
directions. Adaptation compresses the transfer matrix towards chance. It recovers at most 34 % of
the deficit where transfer fails, and it produces *negative* recovery in seven of twelve decomposed
directions. Every direction that already transferred is degraded, in the worst case by −0.86 of the
gap. We found no prior application of covariance alignment to fire susceptibility, fire occurrence
or burned-area prediction. This is a negative result reported with a mechanism, not an absence.

**Contribution 3. Similarity is not sufficient for transfer, whether geographic, climatic or
environmental.** Manavgat and Muğla lie in the same country and fire year, roughly 200 km apart, and
have the highest burned-niche overlap of any pair in the matrix. They fail in both directions, with
bootstrap intervals entirely below chance. Bejís and Muğla lie in different countries and years,
about 2500 km apart, and transfer above chance in both directions. So do Bejís and Montiferru, the
pair with the *lowest* niche overlap. The claim is one of *sufficiency*. It is established by
coexisting counterexamples and is independent of the number of pairs available. It is presented as a
contribution to a live disagreement rather than as a settled general law. The fire literature
expects similarity to predict transfer [@Dimarco2026; @Liu2025], while the species distribution
modelling literature has found that it does not [@Vesk2021; @Rousseau2022]. Dimarco et al. reach a
compatible conclusion from the opposite direction, attributing their weakest transfer to
non-climatic
factors rather than to bioclimatic distance.

**Contribution 4. The failure is conditional, and only a conditional diagnostic sees it.** Twenty
candidate transferability diagnostics from four families are evaluated against the observed transfer
outcomes under one bootstrap framework. Area-of-applicability-style predictor-space dissimilarity
[@Meyer2021; @Meyer2022; @Ludwig2023], climatic and geographic distance, learned domain
separability, canonical niche-overlap statistics and burn-pattern regime distances all fail to order
the matrix. The domain classifier is at ceiling, with AUC ≥ 0.96 for every pair. Only two
diagnostics have intervals that exclude zero, and both measure conditional direction agreement:
whether each predictor's signed association with burning points the same way in both regions
(Spearman ρ = +0.84 and +0.81). Signed associations require burned labels in both regions, so this
is a mechanism diagnosis and not a label-free screening tool. The failure that is invisible to
marginal diagnostics is visible in the conditional structure. Paired with label-blind adaptation
performance as an instrument for splitting recoverable from irreducible shift, it is the
constructive contribution that makes the paper more than a negative result. Shift decomposition in
applied remote sensing is not itself new [@Huang2026]. What we add is the fire application, the
adaptation-as-instrument formulation, and the explicit head-to-head of marginal, niche-overlap and
conditional diagnostics on the same pairs.

**Contribution 5. Within-region replication of the thermal increment.** The increment is replicated
across five independent Mediterranean regions under spatially blocked cross-validation. ΔAUC runs
from +0.056 to +0.153, every bootstrap interval lies above zero, and the result holds in both
analysis populations. It survives spatial blocks up to ~10 km and a predictor window closed up to 14
days earlier. The finding is not itself novel, since comparable within-region results exist for
these landscapes [@AlkanAkinci2023; @Iban2022]. It is included as the evidence for the first half of
Contribution 1.

Alongside these, a leakage-audited, spatially blocked evaluation and transfer protocol is released
with code, configuration and frozen outputs. A negative transfer result can then be checked rather
than taken on trust. This matters given evidence that wildfire transfer conclusions are sensitive to
evaluation design and task formulation [@Xu2026].

Section 2 reviews the relevant literature. Section 3 describes the study regions, the data, and the
full modelling, cross-validation, transfer and adaptation protocol. Section 4 reports results.
Section 5 discusses them, including limitations. Section 6 concludes.
