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
> 7. **Consistency pass 2026-08-13.** Four changes, no numbers added or altered. (i) The
>    sharpest-form thesis sentence claimed the block that gains the most within a region loses the
>    most between regions. That comparative is untested, since no other block's portability is
>    measured on the same footing. It now says the block contributes nothing on average between
>    regions and that its contribution is sign-unstable, being a property of the source-target pair.
>    The same echo in §1.4 Q1 was rewritten. (ii) "Static baseline" became "static and near-static
>    terrain, fuel and greenness baseline" at first mention in §1.4, with the vegetation-index
>    composite named as its one time-varying member (§3.4); later mentions read "the baseline".
>    §1.2 was softened for the same reason, from "by construction they cannot explain" to "explains
>    poorly". (iii) A short paragraph was added at the end of §1.3 stating in advance what §5.2
>    concedes at its close: the sharpest supported reversal belongs to elevation, so instability is
>    a property of the predictor-to-burning mapping generally, and the thermal block is where the
>    trade-off is costly rather than where instability is worst. (iv) Contribution 4 already
>    excepted the conditional family and was left alone.
> 8. **Blocking-scale pass 2026-08-13** (`paper/transfer_ci_blocksize.md`, Results §4.8g and Table
>    R13). Two support claims here were 2-cell (~1 km) counts quoted as exact. (i) Contribution 1's
>    "improving ten with bootstrap support and degrading seven" now leads with what is invariant, the
>    sign instability and the −0.148 to +0.133 span at twelve positive and eight negative, then gives
>    both blockings and names the fragility of the 1 km split. (ii) Contribution 3's "bootstrap
>    intervals entirely below chance" for Manavgat and Muğla held only at 1 km; at 5 km only
>    Muğla→Manavgat is supported. Bejís and Montiferru, the low-overlap pair, carries no verdict at
>    5 km at all, so that half of the contrast is now stated at the point estimate. Bejís and Muğla
>    is supported at both scales and is now said to be. The sufficiency argument is unaffected, since
>    it rests on Bejís-Muğla against Manavgat-Muğla. The swing-factor sentence is unchanged, because
>    it rests on point estimates. No number was introduced that is not in `transfer_ci_blocksize.md`,
>    §4.8g or §5.1.

---

Wildfire is a defining disturbance of Mediterranean-basin landscapes, and a changing climate is
reshaping where and how it burns [@Pausas2021]. The pressure to anticipate *where* fire will occur
has produced a large and still-growing literature on fire susceptibility mapping. It has recently
been synthesised from both a methodological and an application perspective [@Vibhandik2026;
@Jodhani2026]. The dominant pattern is well established. Geospatial predictors are assembled over a
study region and paired with a historical record of burned area. A supervised classifier is then
fitted, most often a random forest [@Breiman2001]. The resulting susceptibility surface is published
with a cross-validated AUC in the 0.85 to 0.95 range.

This paper is about a property that the pattern does not report. Predictors that describe the
*state* of a surface in a particular season are more informative about that season than predictors
that describe a place. They are also, as we show, not portable, and a large part of this paper is
about how much harder that is to establish than it looks: the reading we first reached, that the
relationship is reparameterised locally and points in different directions in different places, does
not survive a correction to how the study regions were evaluated (Section 4.10). The dynamic block is worth +0.056 to +0.153 ROC-AUC inside every region under blocked
cross-validation, +0.022 when a whole burn scar is withheld, and contributes
+0.004 between them, an estimate whose interval spans zero, with a sign that is a property of the
source-target pair rather than of the block.

The obvious reading of that pair of numbers is a trade-off, and our own earlier framing took it. The
data do not support it. The static baseline transfers at a mean of 0.537 against the thermal model's
0.541, so the predictor class that ought to travel does not travel either, and removing the
reversing predictors returns +0.014 of transfer on an interval that also spans zero. Two nulls on
the portability axis are not an exchange. What is measured is a local gain that does not export, and
a local cost when the reversing predictors are removed, with no compensating transfer gain on either
arm.

## 1.1 Portability goes unmeasured

A susceptibility model's reported skill is almost always an estimate of *within-region* performance.
Held-out folds come from the same study area and season, often from the same fire event, and where
folds are drawn at random over cells, spatial autocorrelation inflates the estimate further. The
problem is documented across ecological modelling [@Roberts2017; @Ploton2020] and is addressed by
spatially blocked cross-validation [@Valavi2019; @Meyer2018]. Blocking removes the inflation that
random folds produce, and it is the right correction for what it corrects. It does not make the
estimate honest about a fire the model has not seen. Section 4.3 measures that on identical cells: a
model with the held-out burn scar in its training data scores 0.634 on that scar's area, and
withholding the scar gives 0.552. Part of the apparent gap between a region-level figure and either
of those is the evaluation area rather than the model.

Because only that side of the ledger is reported, portability is never entered at all. A predictor
block is adopted on the strength of the increment it delivers inside its training footprint, and
whether that increment survives a change of region is not asked, even though any regional
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
space into an internally normalised measure. In principle it should be less exposed to
absolute-temperature offsets between regions than raw land surface temperature. That theoretical
portability advantage is tested here, and it is not found: the two internally normalised channels
transfer no better than the four absolute ones, at means of 0.544 and 0.548 over the twenty
directions (Appendix A(f)).

That pre-fire thermal state carries genuine information about subsequent fire is established
[@Maffei2018; @MaffeiMenenti2019; @Maffei2021; @Gelabert2025]. What has not been established is
whether the predictive *skill* of a classifier trained on it in one fire region survives strict,
label-free application to another. The physics linking moisture stress to combustion is universal, so
portability should be most expected for this class, which is what makes it diagnostic: a loss here
cannot be dismissed as a peculiarity of a locally defined covariate. That expectation is the
motivation for the design, not a finding of it. Section 4.10 reports that the signed associations run
the other way, a hotter pre-fire surface being associated with less burning in all five regions and
surviving stratification within elevation and greenness, so on this cohort the block behaves as a
proxy for fuel availability rather than as a moisture-stress index. We keep the framing because it
is why these predictors were chosen and why their failure to travel is informative, and we state the
contradiction where the evidence appears rather than adjusting the motivation after the fact.

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
nearest prior work is named inside the claim.

**Contribution 1. Where a model is scored decides what it appears to know, and the effect is large
enough to dissolve one of our own findings.** That evaluation extent inflates AUC is established in
species distribution modelling, by Lobo et al. [@Lobo2008], VanDerWal et al. [@VanDerWal2009] and
Barve et al. [@Barve2011] (Section 2.5); what is new here is a magnitude, under a controlled design
that earlier work did not run, and its consequences for a live wildfire result. Holding the model,
the predictors and the fitting fixed and changing only which cells are scored, moving from the whole
region to the burn scar and its 2 km collar costs **0.143 ROC-AUC [+0.077, +0.208]**, from 0.776 to
0.634. That exceeds the predictor-block increments this literature publishes as findings, so it is
not a second-order correction. A control isolates the cause: matching a region sample to the scar
area's prevalence changes nothing, at −0.000 [−0.003, +0.002], while scoring the same predictions on
the scar area costs +0.155 [+0.093, +0.217]. It is the composition of the negative pool, whose cells
are all fire-adjacent and therefore the hardest in the region, not class balance.

Applied between regions, the same effect withdraws three of our own claims (Section 4.10). The five
study areas enclose very different far fields, from 2 % of Montiferru's cells lying beyond 10 km of
any fire to 63 % of Bejís's, and that far field is higher ground. Restricting every region to a
10 km collar, **which drops no burned cells**, makes all five agree in sign on elevation, on LST and
on TVDI; both bootstrap-supported elevation reversals disappear; mean transfer rises from 0.540 to
0.617; and the directions below chance fall from six to one. The sign reversal we had offered as the
mechanism of the residual is therefore mostly a property of how five rectangles were drawn. Under
this paper's own criterion **no reversal remains bootstrap-supported** in the equalised frame; the
closest is the LST anomaly between Bejís and Evia, a point reversal whose Evia interval includes 0.5
by 0.003. The sign the five regions now agree on is also not the one the dryness framing predicts:
hotter pre-fire surfaces burned less in every region, and that survives stratification within
elevation and greenness deciles, so on this cohort the block behaves as a proxy for fuel
availability rather than as a moisture-stress index (Section 4.10). A reversal also appears
between two fires eleven months apart inside one study area, where the frame is fixed by
construction (Section 4.9), but on elevation alone, on eleven positive-carrying blocks, and with one
fire per arm it is as consistent with event-to-event variation as with any regional property. The
practical consequence is a reporting standard, stated in Section 5.8.

**Contribution 2. Local skill does not travel, and correcting the frame does not rescue it.** The
thermal block is worth +0.056 to +0.153 ROC-AUC inside every one of five regions under blocked
cross-validation, with every bootstrap interval above zero and the result holding in both analysis
populations. Much of that is a property of interleaved holdout: withholding a whole burn scar leaves
+0.022 [−0.032, +0.077]. Across twenty ordered transfer directions it contributes +0.004 [−0.028,
+0.036], an interval spanning zero under all four between-direction resampling units we computed,
with a sign that varies by pair — paired deltas run from −0.148 to +0.133, twelve positive and eight
negative, and dropping Evia alone reverses their mean. Two controls bound the reading. The static
baseline transfers at 0.537 against the thermal model's 0.541, so the portability failure is not the
dynamic block's peculiarity. And equalised transfer of 0.617 against within-region skill of about
0.87 leaves most of the gap intact, so the frame correction of Contribution 1 narrows the mechanism
without rescuing the result. The within-region half is not novel, comparable results existing for
these landscapes [@AlkanAkinci2023; @Iban2022]; the paired contrast against portability is. Dimarco
et al. [@Dimarco2026] transfer a predominantly stationary predictor set successfully across a
comparable Mediterranean design, though their response variable is ignition rather than burned area
(Section 5.7).

**Contribution 3. The shortfall is invisible to every diagnostic that could be run before
deployment.** Twenty candidate diagnostics from five families are evaluated against observed
transfer under one bootstrap framework. Area-of-applicability-style predictor-space dissimilarity
[@Meyer2021; @Meyer2022; @Ludwig2023], climatic and geographic distance, learned domain
separability, niche-overlap statistics and burn-pattern regime distances were none of them shown to
order the matrix; the domain classifier is at ceiling, with AUC ≥ 0.96 for every pair. Only two
diagnostics have intervals excluding zero, and both measure conditional direction agreement, that
is, whether each predictor's signed association points the same way in both regions (Spearman
ρ = +0.84 and +0.81 over sixteen directions from eight pairs). Both are computed on a data-selected
subset of predictors, and their all-nine-feature counterparts span zero. **Contribution 1 then
removes even that exception.** The sign-agreement statistic is built from the signed associations
that the frame test shows to be artefacts, and recomputed on an equalised frame it is unanimous —
1.0 in every direction, with no variance left to correlate — while the continuous alternative falls
from ρ = +0.50 to +0.12 (Section 4.10). The honest finding is therefore stronger and worse for the
practitioner than it first appeared: **no diagnostic tested here, marginal or conditional, was shown
to order transfer once the frames are comparable**, and the one that appeared to was reading how the
study rectangles were drawn. The same point survives without any ranking, at the point estimates: the pair with the
highest burned-niche overlap fails in both directions while the lowest transfers in both. That
contradicts an expectation the fire literature carries [@Dimarco2026; @Liu2025] and agrees with
species distribution modelling [@Vesk2021; @Rousseau2022].

Two consequences follow, reported as supporting results rather than leading ones. Label-free
alignment by standardisation and covariance alignment [@Sun2016] does not repair transfer; it
compresses fourteen of twenty directions towards chance, and we believe this is the first
application of covariance alignment to fire susceptibility. And because the residual is conditional,
the resource that closes it is target labels: thirty-two labelled 5 km blocks recover 85 to 89 % of
the target's matched ceiling in three of six directions, 51 to 57 % in two more, and 30 % in the
sixth.

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
