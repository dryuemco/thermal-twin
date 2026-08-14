# 1. Introduction


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
predictors buy local skill at the cost of portability**. Two measurements carry that claim. The
dynamic block is worth +0.056 to +0.153 ROC-AUC inside every region and contributes nothing
distinguishable from zero between them, with an unstable sign. Removing the reversing predictors
costs −0.081 of within-region skill with interval support in every region, while changing mean
transfer by +0.014, an estimate whose own interval spans zero. Whether the block helps or harms on
transfer is a property of the source-target pair, not of the block.

## 1.1 Portability goes unmeasured, so the trade-off goes unpriced

A susceptibility model's reported skill is almost always an estimate of *within-region* performance.
Held-out folds come from the same study area and season, often from the same fire event, and where
folds are drawn at random over cells, spatial autocorrelation inflates the estimate further. The
problem is documented across ecological modelling [@Roberts2017; @Ploton2020] and is addressed by
spatially blocked cross-validation [@Valavi2019; @Meyer2018]. Blocking makes the within-region
estimate honest. It says nothing about whether the fitted relationship holds elsewhere.

Because only that side of the ledger is reported, the trade-off is structurally invisible. A
predictor block is adopted on the strength of the increment it delivers inside its training
footprint, and the portability it consumes is never entered as a debit, even though any regional
product built from locally trained models implicitly promises generalisation beyond that footprint.
For fire specifically the transfer question is asked far less often than in adjacent fields.
Meteorological fire-danger indices are known not to port cleanly between fire environments
[@Podschwit2022], and the two recent studies that test model transfer systematically, across
Mediterranean countries [@Dimarco2026] and US counties [@Liu2025], both report that it largely
succeeds between similar regions. Both transfer models whose dominant predictors are *spatially
stationary*: terrain, human modification, night-time lights, population density, long-term
climatologies. Each describes a place rather than a season, which is the class our thesis expects to
travel well. Species distribution modelling has examined transferability far more systematically
[@Yates2018], and there geographic and environmental similarity do *not* reliably predict transfer
success [@Vesk2021; @Rousseau2022].

## 1.2 Pre-fire thermal dryness is the natural test case

The dynamic class used here is pre-fire thermal dryness, and it is the class most plausibly
*expected* to transfer. Standard susceptibility predictors are terrain, fuel type, greenness,
long-term climatology and proximity to roads and settlements, and most are static or near-static
over the timescale at which fire danger varies. Such a set explains poorly why a particular summer
burned and the preceding one did not. What changes between those summers is the state of the
surface: fuel dryness, moisture stress, and how anomalously hot the land surface has become relative
to its own baseline. Satellite thermal observation gives direct access to part of that state through
fuel moisture content [@Yebra2013], and pairing surface temperature with a vegetation index was
established as a live-fuel-moisture estimator for fire-danger rating by Chuvieco et al.
[@Chuvieco2004]. The Temperature-Vegetation Dryness Index [@Sandholt2002] formalises that feature
space into an internally normalised measure which should, in principle, be less exposed to
absolute-temperature offsets between regions than raw land surface temperature. That theoretical
portability advantage is tested here.

That pre-fire thermal state carries genuine information about subsequent fire is established
[@Maffei2018; @MaffeiMenenti2019; @Maffei2021; @Gelabert2025]. What has not been established is
whether the predictive *skill* of a classifier trained on it in one fire region survives strict,
label-free application to another. The physics linking moisture stress to combustion is universal,
so portability should be most expected for this class, which is what makes it diagnostic: a loss
here cannot be dismissed as a peculiarity of a locally defined covariate.

## 1.3 Why the loss is invisible to the diagnostics in use

A deficit on transfer can arise two ways. Under **covariate shift** the marginal distribution of the
predictors differs while the predictor-response relationship is preserved, which is in principle
correctable without target labels, by per-region standardisation or covariance alignment such as
CORAL [@Sun2016], an approach with an established remote-sensing literature [@Tuia2016]. Under
**concept shift** the conditional relationship itself changes: a predictor positively associated with
burning in one region is negatively associated with it in another. No label-free realignment of input
distributions can repair a sign reversal, because the information needed to detect it is exactly the
information being withheld. The taxonomy is canonical [@MorenoTorres2012].

This distinction is what makes the failure hard to anticipate. The diagnostics the field relies on to
decide whether a model may be applied to new ground, above all area-of-applicability measures built
on dissimilarity in predictor space [@Meyer2021; @Meyer2022; @Ludwig2023], are marginal by
construction. A target region can sit well inside the training data's predictor envelope while the
relationship between those predictors and burning points the other way. This paper measures both
sides on the same pairs.

## 1.4 Contributions

Three findings carry this paper. Each is stated at the strength its interval supports, and the
nearest prior work is named inside the claim rather than omitted.

**Contribution 1. Local skill and portability, measured separately and per direction.** For every
ordered region pair, the change in transfer skill from adding the dynamic pre-fire thermal block to
a matched baseline is set against the within-region increment the same block delivers. The block is
worth +0.056 to +0.153 ROC-AUC inside every one of five regions, with every bootstrap interval above
zero and the result holding in both analysis populations. Across the twenty ordered transfer
directions it contributes +0.004, an estimate whose interval spans zero under all four
between-direction resampling units we computed, and its sign is unstable: paired deltas run from
−0.148 to +0.132, twelve positive and eight negative. The control that bounds the interpretation is
the baseline arm: it transfers at a mean of 0.537 against the thermal model's 0.541, so the static
predictor class is not the portable one here either, and what the matrix shows is that **nothing in
this feature space travels** rather than that dynamic state is uniquely fragile. Feature removal
measures the local cost directly. Dropping the two reversing predictors, elevation and the LST
anomaly, costs −0.081 of mean within-region AUC, supported in every region and roughly three
quarters of it attributable to elevation, which is a *baseline* terrain variable; it changes mean
transfer by +0.014, whose interval spans zero. Both figures are post-selection, the two predictors
having been chosen on the same reversal analysis (Section 4.6b). A local cost is measured and no
compensating transfer gain is, which is weaker than an exchange and is stated as such. The within-region half is not itself novel, since comparable results exist for these
landscapes [@AlkanAkinci2023; @Iban2022]; the paired contrast against portability is. Dimarco et al.
[@Dimarco2026] transfer a predominantly spatially stationary predictor set successfully across a
comparable Mediterranean design, and this is the complementary half of that picture rather than a
contradiction of it.

**Contribution 2. The loss is invisible to the diagnostics that could be run before deployment, and
visible to one that cannot.** Twenty candidate transferability diagnostics from four families are
evaluated against the observed transfer outcomes under one bootstrap framework.
Area-of-applicability-style predictor-space dissimilarity [@Meyer2021; @Meyer2022; @Ludwig2023],
climatic and geographic distance, learned domain separability, niche-overlap statistics and
burn-pattern regime distances all fail to order the matrix; the domain classifier is at ceiling, with
AUC ≥ 0.96 for every pair. Only two diagnostics have intervals excluding zero, and both measure
conditional direction agreement, whether each predictor's signed association with burning points the
same way in both regions (Spearman ρ = +0.84 and +0.81 over sixteen directions from eight region
pairs). Both are computed on a data-selected subset of predictors, and their all-nine-feature
counterparts span zero, so the result rests on that selection and is reported with it. Equalising
the families onto a common twelve directions leaves the ordering unchanged, so it is not an artefact
of the marginal rows carrying the smaller sample. Signed associations need
burned labels on both sides, so this is a mechanism diagnosis rather than a pre-deployment screen,
and the marginal family, which is the only one that can be run before deployment, is the one that
fails. The same point survives without any ranking, at the point estimates: the pair with the highest
burned-niche overlap in the matrix fails in both directions while the pair with the lowest transfers
in both, so similarity is not sufficient for transfer. That contradicts an expectation the fire literature
carries [@Dimarco2026; @Liu2025] and agrees with what species distribution modelling has found
[@Vesk2021; @Rousseau2022]. Shift decomposition in applied remote sensing is not itself new
[@Huang2026]; what is added here is the fire application and the head-to-head of marginal,
niche-overlap and conditional diagnostics on the same pairs.

**Contribution 3. The mechanism is a sign reversal, and it survives holding geography fixed.**
Predictors do not merely weaken across regions, they reverse the direction of their association with
burning, which is why a distance in predictor space cannot see the failure. The sharpest reversal is
elevation, whose association points opposite ways in Manavgat and in Bejís and Muğla with disjoint
bootstrap intervals. The same reversal appears inside a single study area, between two fires eleven
months apart on an identical grid, where season and population also differ but place does not
(Section 4.8); that arm rests on one fire and eleven positive-carrying 5 km blocks, below the floor
this design sets for itself, so it corroborates the mechanism rather than establishing it. Two
consequences follow and are reported as supporting rather than leading results:
label-free alignment by standardisation and covariance alignment [@Sun2016] does not repair transfer
but compresses it towards chance in fourteen of twenty directions, which we believe is the first
application of covariance alignment to fire susceptibility; and because the residual gap is
conditional, the resource that closes it is target labels, whose price is measurable, thirty-two
labelled 5 km blocks recovering 85 to 89 % of the target's own ceiling in three of six directions
tested, 51 to 57 % in two more and 30 % in the sixth.

Alongside these, a leakage-audited, spatially blocked evaluation and transfer protocol is released
with code, configuration and frozen outputs, so that most of this result can be re-run rather than
taken on trust. One component is an exception and is named in the data-and-code availability
statement: the reproduction-check code is not in the released repository at the commit of record.
The few-shot export, previously also listed as an exception, was regenerated at commit `6d7a6a71`
and its validator now passes on every check. This matters given evidence that wildfire transfer
conclusions are sensitive to evaluation design and task formulation [@Xu2026].

A companion paper treats the observational layer beneath this one, where preprocessing decisions
taken before any model is fitted are shown to carry their own uncertainty budget.

Section 2 reviews the relevant literature. Section 3 describes the study regions, the data, and the
modelling, cross-validation, transfer and adaptation protocol. Section 4 reports results. Section 5
discusses them, including limitations. Section 6 concludes.
