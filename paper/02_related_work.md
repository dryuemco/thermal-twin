# 2. Related work

> **Cut 2026-08-14 in the split.** This section was 5,246 words across five subsections. It is now
> written to serve the three findings of Section 1.4 and nothing else. No citation was dropped that
> a surviving claim depends on, and the Dimarco contrast, which Contribution 1 rests on, is kept
> whole. The removed material, chiefly the wider fire-susceptibility and thermal-dryness surveys,
> supports the companion paper.

## 2.1 Fire susceptibility mapping, and what it reports

Fire susceptibility mapping has been synthesised recently from both methodological and application
perspectives [@Vibhandik2026; @Jodhani2026]. The dominant pattern is stable: geospatial predictors
are assembled over a study region, paired with a historical burned-area record, and fitted with a
supervised classifier, most often a random forest [@Breiman2001], and the resulting surface is
published with a cross-validated AUC in the 0.85 to 0.95 range. That figure is a within-region
estimate. Comparable within-region results already exist for the landscapes studied here
[@AlkanAkinci2023; @Iban2022].

## 2.2 Pre-fire thermal dryness

Satellite thermal observation gives repeated access to surface state through fuel moisture content
[@Yebra2013]. Pairing land surface temperature with a vegetation index was established as a
live-fuel-moisture estimator for fire-danger rating by Chuvieco et al. [@Chuvieco2004], and the
Temperature-Vegetation Dryness Index [@Sandholt2002] formalises that feature space into an
internally normalised measure, which is why it is often expected to travel between regions better
than raw temperature. That pre-fire thermal state carries information about subsequent fire is
established [@Maffei2018; @MaffeiMenenti2019; @Maffei2021]. Gelabert et al. [@Gelabert2025] found
dead fine fuel moisture and its anomalies to be the most influential predictor of human-caused
ignition likelihood across Europe, testing generalisation by pooled fitting with per-site
evaluation. What has not been tested is whether a classifier built on this class survives strict,
label-free application to a region it never saw.

## 2.3 Spatial validation and transferability

Random cross-validation over spatially autocorrelated cells inflates skill estimates
[@Roberts2017; @Ploton2020], and spatially blocked designs are the standard remedy
[@Valavi2019; @Meyer2018]. The remedy is not uncontested: blocked schemes have been argued to
introduce pessimistic bias of their own [@Wadoux2021; @Mila2022; @deBruin2022]. This paper uses
spatial blocking throughout and reports every result at three block sizes, so that a reader can see
which verdicts depend on the choice.

Blocking makes a within-region estimate honest but says nothing about another region. For that, the
field's instrument is the area of applicability and related predictor-space dissimilarity measures
[@Meyer2021; @Meyer2022; @Ludwig2023], which ask whether a target's predictor values fall inside the
training data's envelope. Species distribution modelling has examined transferability far more
systematically than fire has [@Yates2018], and two studies there report that geographic and
environmental similarity do not reliably predict transfer success [@Vesk2021; @Rousseau2022].

## 2.4 Dataset shift and label-free adaptation

The canonical taxonomy separates covariate shift, where the predictor distribution moves but the
predictor-response relationship holds, from concept shift, where the relationship itself changes
[@MorenoTorres2012]. Covariate shift is in principle correctable without target labels, by
per-region standardisation or by covariance alignment such as CORAL [@Sun2016], and domain
adaptation has an established remote-sensing literature [@Tuia2016]. Concept shift is not: no
realignment of input distributions can repair a reversal in the sign of an association, because
detecting it requires the labels being withheld. Shift decomposition in applied remote sensing is
not itself new [@Huang2026]. We are not aware of a prior application of covariance alignment to fire
susceptibility, fire occurrence or burned-area prediction.

## 2.5 Cross-region generalisation of fire models

Few studies test fire-model transfer directly. Podschwit et al. [@Podschwit2022] provide the
long-standing reference point that meteorologically derived danger indices do not port cleanly
between fire environments. WildfireGenome [@Liu2025] performs a leave-one-county-out transfer matrix
across seven ecologically diverse US counties and reports strong within-county performance with
highly variable off-diagonal transfer, ecologically similar pairs transferring well and dissimilar
pairs collapsing; its label, however, is a principal-component composite of federal hazard
*indicators* rather than observed burned area, and it applies no adaptation and no shift
decomposition. Xu et al. [@Xu2026] argue that wildfire transfer conclusions depend strongly on
evaluation design and task formulation, a caution that applies here as much as anywhere, and which
we address by fixing the analysis protocol in a project log before the diagnostics were computed and
by reporting every sensitivity axis. That log is not a formal pre-registration and no independent
timestamped registration exists; Section 3.14.1 states what was fixed and when. For infrastructure at
this scale, Kondylatos et al. [@Kondylatos2023] provide Mesogeos, a 1 km Mediterranean datacube built
for data-driven wildfire modelling.

**The nearest neighbour, and the contrast the present paper draws.** Dimarco et al. [@Dimarco2026]
is the closest Mediterranean analogue. They harmonise 500 m predictors across four Mediterranean
countries, fit tree ensembles under five-fold spatial cross-validation with an 80/20 hold-out, and
test transfer both leave-one-country-out and as a full 4 × 4 matrix. Every transfer exceeds AUC 0.80.
Transfers between bioclimatically similar countries score higher, and transfers to Morocco are
systematically lower, which they attribute to anthropogenic drivers, fire management practice and
data reporting rather than to climate alone. They apply no domain adaptation.[^dimarco-lst]

The two studies share their essential design: Mediterranean regions, 500 m cells, MCD64A1-derived
targets, tree ensembles, spatially aware validation and an explicit transfer matrix. Theirs covers
four countries and twelve ordered pairs, ours five regions and twenty ordered directions. **What
differs is the predictor class.** Their model rests on quantities that are attributes of a place:
terrain slope, night-time lights, human modification, population density, and temperature, wind and
humidity as long-term seasonal climatologies. Every one is spatially stationary. Ours rests on the
state of a surface in one season. Their result and ours are therefore not in conflict; read together
they suggest that the relationship between domain similarity and transfer success is
**predictor-class dependent**, so that models built on stationary attributes track similarity while
models built on dynamic state need not. We present that reading as a live disagreement rather than a
settled result: Vesk et al. [@Vesk2021] and Rousseau and Betts [@Rousseau2022] align with it from
species distribution modelling, while Dimarco et al. and WildfireGenome run against it.

[^dimarco-lst]: Their Results text refers to "LST anomalies", which is inconsistent with their own
Methods, where no land surface temperature or TVDI variable appears and the only temperature
predictor is a static ERA5-Land seasonal climatology [@MunozSabater2021]. We follow their Methods,
which we take to be authoritative, and note the discrepancy so that the comparison is transparent.
Every statement about their work was checked against the full text, read 2026-08-08, not the
abstract alone.
