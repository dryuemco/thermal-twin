# 1. Introduction


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
