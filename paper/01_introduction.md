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
> 8. **Blocking-scale pass 2026-08-13** (`paper/transfer_ci_blocksize.md`, Results §4.9g and Table
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
>    §4.9g or §5.1.

---

Wildfire is a defining disturbance of Mediterranean-basin landscapes, and a changing climate is
reshaping where and how it burns [@Pausas2021]. The dominant pattern in fire susceptibility mapping
[@Vibhandik2026; @Jodhani2026] is settled: geospatial predictors are assembled over a study region,
paired with a historical burned-area record and fitted with a supervised classifier, most often a
random forest [@Breiman2001], and the surface is published with a cross-validated AUC of 0.85 to 0.95. **That pattern does not report portability**, and this paper measures it.

## 1.1 Portability goes unmeasured

A susceptibility model's reported skill is almost always a *within-region* estimate: held-out folds
come from the same study area and season, often the same fire, and random folds over cells let
spatial autocorrelation inflate it further. The problem is documented across ecological modelling
[@Roberts2017; @Ploton2020] and addressed by spatially blocked cross-validation [@Valavi2019;
@Meyer2018], but blocking does not make the estimate honest about a fire the model has not seen.

Because only that side of the ledger is reported, portability is never entered: a predictor block is
adopted on the increment it delivers inside its training footprint, and whether that survives a
change of region is not asked, even though any regional product built from locally trained models
implicitly promises generalisation beyond it. Meteorological fire-danger indices are known not to
port cleanly in a Peruvian case study [@Podschwit2022], and the two studies that test transfer
systematically [@Dimarco2026; @Liu2025] both report that it largely succeeds between similar
regions — and both transfer models whose dominant predictors are *spatially stationary*. Whether a
dynamic, season-specific class behaves the same way is this paper's question.

## 1.2 Pre-fire thermal dryness is the natural test case

Pre-fire thermal dryness is the dynamic class most plausibly *expected* to transfer. Standard
predictors are static or near-static over the timescale at which fire danger varies, so they explain
poorly why one summer burned and the preceding one did not; what changes is the state of the
surface, to which satellite thermal observation gives partial access (Section 2.2). The physics
linking moisture stress to combustion is universal, so portability should be most expected here,
which makes the class diagnostic: a loss cannot be dismissed as a peculiarity of a locally defined
covariate. The expectation is sharpest for the internally normalised channels, which should
be least exposed to absolute-temperature offsets between regions; **they transfer no better than the
absolute ones** (Appendix A(f)). The expectation motivates the design and is not a finding of it —
Section 4.4 reports the associations running the other way.

## 1.4 Contributions

Two findings carry this paper, stated here as claims and established in Section 4, which carries
every interval.

**Contribution 1. Where a model is scored decides what it appears to know, and the effect is large
enough to dissolve findings of our own.** That evaluation extent inflates AUC is established in
species distribution modelling (Section 2.4); what is new is a magnitude under a controlled design.
Holding model, predictors and fitting fixed and changing only which cells are scored costs **0.143
ROC-AUC**, the size of the increments this design measures for a predictor block, with the cause
measured as the negative pool's composition rather than class balance (Section 4.3). Applied between
regions it withdraws five claims of our own, including the sign reversal we had offered as the
mechanism and the one arm that held place fixed (Section 4.4), and the practical consequence is a
reporting standard (Section 5.6).

**Contribution 2. Local skill does not travel, and correcting the frame does not rescue it.** The
thermal block is worth a substantial within-region increment in all five regions, every bootstrap
interval above zero, and stays positive when the frame is equalised — but much of it is a property of
interleaved holdout, and across twenty transfer directions the paired contribution spans zero on both
frames under the primary resampling unit, though much closer to the boundary once equalised and not
under every admissible unit (Section 4.4), with a sign belonging to the pair rather than the block.
Two controls bound this: the static baseline transfers no better on either frame, so the failure is
not the thermal block's peculiarity, and on matched frames and blocking equalised transfer still
falls **0.155** short of the within-region reference. The within-region half is not novel
[@AlkanAkinci2023; @Iban2022]; the paired contrast against portability is.

Two consequences follow, as supporting results: label-free alignment by standardisation and
covariance alignment [@Sun2016] does not repair transfer, in what we believe is its first application
to fire susceptibility; and because the residual is conditional, the resource that closes it is
target labels, priced in Appendix A(u).

The leakage-audited, spatially blocked protocol is released with code, configuration and frozen
outputs, so most of this can be re-run rather than taken on trust, the release being complete as
the declarations record — which matters given evidence that wildfire transfer conclusions are sensitive
to evaluation design [@Xu2026]. A companion paper treats the observational layer beneath this one.
