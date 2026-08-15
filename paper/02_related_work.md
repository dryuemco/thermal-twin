# 2. Related work

> **Cut 2026-08-14 in the split.** This section was 5,246 words across five subsections. It is now
> written to serve the four contributions of Section 1.4 and nothing else. No citation was dropped that
> a surviving claim depends on, and the Dimarco contrast, which Contribution 1 rests on, is kept
> whole. The removed material, chiefly the wider fire-susceptibility and thermal-dryness surveys,
> supports the companion paper.

## 2.1 Fire susceptibility mapping, and what it reports

The dominant pattern is described in Section 1; the figure it publishes, a cross-validated AUC of
0.85 to 0.95, is a within-region estimate. Comparable within-region results already exist for the
landscapes studied here [@AlkanAkinci2023; @Iban2022].

## 2.2 Pre-fire thermal dryness

Satellite thermal observation gives repeated access to surface state through fuel moisture content
[@Yebra2013]. Chuvieco et al. [@Chuvieco2004] established the pairing of land surface temperature
with a vegetation index as a live-fuel-moisture estimator for fire-danger rating, and the
Temperature-Vegetation Dryness Index [@Sandholt2002] formalises that feature space into an
internally normalised measure, which is why it is often expected to travel between regions better
than raw temperature. That pre-fire thermal state carries information about subsequent fire is
established [@Maffei2018; @MaffeiMenenti2019; @Maffei2021]. Gelabert et al. [@Gelabert2025] found
dead fine fuel moisture and its anomalies the most influential predictor of human-caused ignition
likelihood across Europe, testing generalisation by pooled fitting with per-site evaluation. What has
not been tested is whether a classifier built on this class survives strict, label-free application
to a region it never saw.

## 2.3 Spatial validation and transferability

Random cross-validation over spatially autocorrelated cells inflates skill estimates [@Roberts2017;
@Ploton2020], and spatially blocked designs are the standard remedy [@Valavi2019; @Meyer2018],
though blocked schemes have themselves been argued to introduce pessimistic bias [@Wadoux2021;
@Mila2022; @deBruin2022]. This paper blocks throughout and reports every result at three block
sizes, so a reader can see which verdicts depend on the choice.

Blocking corrects the inflation random folds produce within a region. It does not speak to
performance on a fire the model has not seen, which Section 4.3 measures on identical cells. For
that, the field's instrument is the area of applicability and related predictor-space dissimilarity
measures [@Meyer2021; @Meyer2022; @Ludwig2023], which ask whether a target's predictor values fall inside the
training data's envelope. Species distribution modelling has examined transferability far more
systematically than fire has [@Yates2018], and two studies there report that geographic and
environmental similarity do not reliably predict transfer success [@Vesk2021; @Rousseau2022];
transferability of satellite-derived empirical models is an active question in fire remote sensing
itself [@Marino2024].

The canonical taxonomy separates covariate shift, where the predictor distribution moves but the
predictor-response relationship holds, from concept shift, where the relationship itself changes
[@MorenoTorres2012]. Covariate shift is in principle correctable without target labels, by
per-region standardisation or by covariance alignment such as CORAL [@Sun2016], and domain
adaptation has an established remote-sensing literature [@Tuia2016; @Persello2012]. Concept shift is not: no
realignment of input distributions can repair a reversal in the sign of an association, because
detecting it requires the labels being withheld. Shift decomposition in applied remote sensing is
not itself new [@Huang2026]. We are not aware of a prior application of covariance alignment to fire
susceptibility, fire occurrence or burned-area prediction.

## 2.5 Cross-region generalisation of fire models

Few studies test fire-model transfer directly. Podschwit et al. [@Podschwit2022] report, in a
Peruvian case study, that meteorologically derived danger indices do not port cleanly between fire
environments. WildfireGenome [@Liu2025] runs a leave-one-county-out matrix across seven US counties
and reports strong within-county performance with highly variable off-diagonal transfer, similar
pairs transferring well and dissimilar pairs collapsing; its label is a principal-component composite
of hazard *indicators* rather than observed burned area, and it applies no adaptation. Xu et al.
[@Xu2026] argue that wildfire transfer conclusions depend strongly on evaluation design, a caution we
address by fixing the protocol in a project log before the diagnostics were computed and by reporting
every sensitivity axis; that log is not a formal pre-registration, and Section 3.11 states what was
fixed and when. Kondylatos et al. [@Kondylatos2023] provide Mesogeos, a 1 km Mediterranean datacube.

**Evaluation extent and AUC.** Species distribution modelling settled long ago that the area a model
is evaluated over is not a neutral choice. Lobo et al. [@Lobo2008] make it the fifth and, by their
own ranking, most important reason to distrust AUC as a comparative measure: the extent of the
modelled area governs how many easy absences enter the calculation, and therefore the score.
VanDerWal et al. [@VanDerWal2009] show the same lever on the calibration side, and Barve et al.
[@Barve2011] give the argument its general form as the accessible area. That literature is
qualitative about magnitude, because magnitude is problem-specific. Two things follow here. Our
Contribution 1 is a measurement inside that framework rather than a new phenomenon, and Section 1
states it that way. And the wildfire literature has largely not imported the lesson: region-wide
figures are reported as though they described performance at the fire, and we know of no wildfire
study that holds the model fixed and varies only the evaluation cells. The 0.143 we obtain is the
size of the predictor-block increments this literature reports, which is why Section 5.8 treats it
as a reporting problem rather than a caveat.

**The nearest neighbour, and the contrast the present paper draws.** Dimarco et al. [@Dimarco2026]
is the closest Mediterranean analogue: 500 m predictors harmonised across four countries, tree
ensembles under spatial cross-validation, transfer tested both leave-one-country-out and as a full
4 x 4 matrix, with every transfer exceeding AUC 0.80 and bioclimatically similar countries scoring
higher. They apply no domain adaptation.[^dimarco-lst]

Much of the design is shared — Mediterranean regions, 500 m cells, MCD64A1-derived targets, tree
ensembles, spatially aware validation, an explicit transfer matrix — and two things differ. **The
predictor class**: their model rests on attributes of a place, all spatially stationary, ours on the
state of a surface in one season. **The response variable**: theirs is human-driven ignition, ours is
burned area, and those are different quantities with different dominant controls. Read together the
two results suggest that the relationship between domain similarity and transfer success may be
predictor-class dependent, with Vesk et al. [@Vesk2021] and Rousseau and Betts [@Rousseau2022]
aligning from species distribution modelling while Dimarco et al. and WildfireGenome run against it.
We present that as a live disagreement, and Section 5.7 states why our own data do not settle it.

[^dimarco-lst]: Their Results text refers to "LST anomalies", which is inconsistent with their own
Methods, where no land surface temperature or TVDI variable appears and the only temperature
predictor is a static ERA5-Land seasonal climatology [@MunozSabater2021]. We follow their Methods,
which we take to be authoritative, and note the discrepancy so that the comparison is transparent.
Every statement about their work was checked against the full text, read 2026-08-08.
