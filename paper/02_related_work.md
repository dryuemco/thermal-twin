# 2. Related work

> **Cut 2026-08-14 in the split.** This section was 5,246 words across five subsections. It is now
> written to serve the four contributions of Section 1.4 and nothing else. No citation was dropped that
> a surviving claim depends on, and the Dimarco contrast, which Contribution 1 rests on, is kept
> whole. The removed material, chiefly the wider fire-susceptibility and thermal-dryness surveys,
> supports the companion paper.
>
> **Style pass 2026-09-23.** Long sentences were split; no citation, number or claim changed, except
> one stale value. In §2.4, "the 0.143" is now 0.133, the frame cost on the corrected Manavgat label
> (Section 4.3).

## 2.1 Fire susceptibility mapping, and what it reports

The dominant pattern is described in Section 1; the figure it publishes, a cross-validated AUC of
0.85 to 0.95, is a within-region estimate. Comparable within-region results already exist for the
landscapes studied here [@AlkanAkinci2023; @Iban2022].

## 2.2 Pre-fire thermal dryness

Satellite thermal observation gives repeated access to surface state through fuel moisture content
[@Yebra2013]. Chuvieco et al. [@Chuvieco2004] established the pairing of land surface temperature
with a vegetation index as a live-fuel-moisture estimator for fire-danger rating. The
Temperature-Vegetation Dryness Index [@Sandholt2002] formalises that feature space into an
internally normalised measure, which is why it is often expected to travel better than raw
temperature. That pre-fire thermal state carries information about subsequent fire is established
[@Maffei2018; @MaffeiMenenti2019; @Maffei2021]. Gelabert et al. [@Gelabert2025] found dead fine
fuel moisture and its anomalies the most influential predictor of human-caused ignition likelihood
across Europe, testing generalisation by pooled fitting with per-site evaluation. What has not
been tested is whether such a classifier survives strict, label-free application to an unseen
region.

## 2.3 Spatial validation and transferability

The canonical taxonomy separates covariate shift from concept shift [@MorenoTorres2012]. Under
covariate shift the predictor distribution moves but the predictor-response relationship holds;
under concept shift the relationship itself changes. Covariate shift is in principle correctable
without target labels, by per-region standardisation or covariance alignment such as CORAL
[@Sun2016], and domain adaptation has an established remote-sensing literature [@Tuia2016;
@Persello2012]. Concept shift is not: no realignment of inputs can repair a
reversal in the sign of an association, because detecting one requires the labels being withheld.
Shift decomposition in applied remote sensing is not itself new [@Huang2026], but we are aware
of no prior application of covariance alignment to fire susceptibility, fire occurrence or
burned-area prediction.

## 2.4 Cross-region generalisation of fire models

Few studies test fire-model transfer directly. Podschwit et al. [@Podschwit2022] report, in a
Peruvian case study, that meteorologically derived danger indices do not port cleanly between fire
environments. WildfireGenome [@Liu2025] runs a leave-one-county-out matrix across seven US counties,
and reports strong within-county performance with highly variable off-diagonal transfer, similar pairs
transferring well and dissimilar pairs collapsing. Its label is a principal-component composite of
hazard *indicators* rather than observed burned area, and it applies no adaptation. Xu et al.
[@Xu2026] argue that wildfire transfer conclusions depend strongly on evaluation design. We address
that caution in two ways: the protocol was fixed in a project log before the diagnostics were
computed, and every sensitivity axis is reported. That log is not a formal pre-registration, and
Appendix D states what was fixed and when. Kondylatos et al. [@Kondylatos2023] provide Mesogeos, a
1 km Mediterranean datacube.

**Evaluation extent and AUC.** Species distribution modelling settled long ago that the area a model
is evaluated over is not a neutral choice. Lobo et al. [@Lobo2008] make it the fifth and, by their
own ranking, most important reason to distrust AUC comparatively. The extent of the modelled area
governs how many easy absences enter the calculation, and therefore the score. VanDerWal et al.
[@VanDerWal2009] show the same lever on the calibration side, and Barve et al. [@Barve2011] give the
argument its general form as the accessible area. That literature is qualitative about magnitude,
because magnitude is problem-specific, so our Contribution 1 is a measurement inside that
framework rather than a new phenomenon. The wildfire literature has largely not imported the lesson:
region-wide figures are reported as though they described performance at the fire. We know of no
wildfire study that holds the model fixed and varies only the evaluation cells. That is why Section
5.6 treats the 0.133 as a reporting problem rather than a caveat.

**The nearest neighbour, and the contrast this paper draws.** Dimarco et al. [@Dimarco2026] is the
closest Mediterranean analogue. They harmonise 500 m predictors across four countries and fit tree
ensembles under spatial cross-validation. Transfer is tested both leave-one-country-out and as a full
4 × 4 matrix. Every transfer exceeds AUC 0.80, bioclimatically similar countries score higher, and no
domain adaptation is used.[^dimarco-lst] Much of the design is shared: Mediterranean regions, 500 m
cells, MCD64A1-derived targets, tree ensembles, spatially aware validation and an explicit transfer
matrix; two things differ. **The predictor class**: their model rests on attributes of a place, all
spatially stationary, ours on the state of a surface in one season. **The response variable**:
theirs is human-driven ignition, ours burned area, which have different dominant controls. Read
together, the two results suggest the relationship between domain similarity and transfer success
may be predictor-class dependent. Vesk et al. [@Vesk2021] align with that reading from species
distribution modelling, while Dimarco et al. and WildfireGenome run against it. Rousseau and Betts
[@Rousseau2022] found environmental similarity not a significant predictor of transferability; our
result is consistent with theirs. We present that as a live disagreement; Section 5.5 states why our data do not
settle it.

[^dimarco-lst]: Their Results text refers to "LST anomalies", inconsistent with their own Methods,
where no land surface temperature or TVDI variable appears and the only temperature predictor is a
static ERA5-Land seasonal climatology [@MunozSabater2021]. We follow their Methods and note the
discrepancy so the comparison is transparent.
