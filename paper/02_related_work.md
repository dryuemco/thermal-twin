# 2. Related work

> **Citation convention.** Citations are given as `[@BibKey]`, resolving against
> `paper/REFERENCES.bib`. **Every reference cited in this file was verified against
> publisher-deposited Crossref metadata on 2026-07-23**; the verification log, including corrections
> to the originally supplied metadata, is in `paper/LITERATURE.md`. Claims that could not be
> verified are marked `[UNVERIFIED: ...]` and are **not** attached to a citation. No reference,
> DOI, volume or page number in this file is invented.
>
> **Structure.** Each of the five blocks closes with a paragraph stating precisely where that
> literature stops short of the present study. Novelty is argued inside the review, not in a
> separate section, and each closing paragraph is written to survive an adversarial reading — the
> claims below have already been through one deliberate refutation attempt (see the novelty audit
> in `LITERATURE.md`), and several were narrowed as a result.
>
> **Orientation.** The review is organised around a single thesis: *adding dynamic state predictors
> buys local skill at the cost of portability, and that loss is invisible to the marginal,
> predictor-space-distance diagnostics the field currently relies on, because the failure is
> conditional rather than marginal.* Each closing paragraph is written to show what the literature
> in question contributes to that argument and where it stops short of it.

---

## 2.1 Fire susceptibility mapping with machine learning

Fire susceptibility mapping — estimating the spatial propensity of the land surface to burn, as
distinct from short-horizon fire-danger forecasting — has converged on supervised machine learning
applied to gridded geospatial predictors, most commonly tree ensembles such as random forests
[@Breiman2001]. Two recent syntheses document the state of the field and its methodological
conventions [@Vibhandik2026; @Jodhani2026]. Reported discrimination is consistently high, typically
in the 0.85 to 0.95 AUC range, and the predictor sets that produce those numbers are remarkably
uniform across studies: terrain from a digital elevation model, a land-cover or fuel-type
classification, a vegetation-greenness composite, climatological summaries, and anthropogenic
proximity variables.

The Mediterranean basin, and Türkiye within it, is one of the most intensively mapped fire
environments, which is fortunate for the present study because two of its regions have direct
precedents. Iban and Sekertekin [@Iban2022] mapped wildfire susceptibility across Adana and Mersin
provinces using remotely sensed fire data and machine learning — the same landscape as the Kozan
district that serves as our cropland-dominated negative control. Alkan Akıncı and Akıncı
[@AlkanAkinci2023] produced a machine-learning susceptibility assessment for the **Manavgat
district of Antalya**, which is our anchor study region, making it the closest published comparison
to our within-region analysis. Iban and Aksu [@Iban2024] extended this line to İzmir with an
explainability-driven framework, using SHAP to interpret the contribution of individual predictors —
though with MODIS active-fire pixels rather than a burned-area product as the target, a distinction
that matters when comparing reported skill. The broader ecological framing of why Mediterranean fire
regimes are changing is set out by Pausas and Keeley [@Pausas2021], and the comparative structure of
global fire regimes — the notion that fire behaves as a small number of distinguishable syndromes
rather than a continuum — by Archibald et al. [@Archibald2013].

**Where this literature stops.** These studies establish that fire susceptibility is learnable
within a region, and the Manavgat and Adana-Mersin precedents establish it for the specific
landscapes we analyse. What none of them establishes is whether a model fitted in one of these
landscapes retains any skill in another. Each is validated within its own study area, so the
reported AUC is an estimate of interpolation performance inside a fixed footprint, not of
generalisation beyond it. Two further gaps follow from the shared predictor design. First, the
predictor sets are dominated by static or near-static variables, which by construction cannot
explain why a particular summer burned and the preceding one did not; the dynamic pre-fire state of
the surface is largely absent. Second, evaluation rarely reports uncertainty at all, and where
cross-validation is used it is frequently random over cells, which — for spatially autocorrelated
data — is known to be optimistically biased (Section 2.3).

Read together, these two gaps are not independent, and their conjunction is what motivates the
present study. Because the field's predictor sets are near-static and its evaluations are
within-region, the natural remedy for the first gap — adding dynamic pre-fire state, so that the
model can distinguish one season from another — is proposed and assessed under precisely the
evaluation regime that cannot reveal its cost. A predictor block can raise within-region skill
while simultaneously binding the fitted model more tightly to the place and season in which it was
fitted, and a within-region AUC records only the first half of that exchange. The present study is
designed to record both halves: it adds a dynamic pre-fire block to a comparable static baseline,
evaluates both under spatially blocked cross-validation with bootstrap intervals, and then carries
the same paired contrast into cross-region transfer, so that the local gain and the portability
cost attributable to the same block are measured on the same footing.

## 2.2 Pre-fire thermal dryness from satellite observation

The physical rationale for thermal predictors runs through fuel moisture. Live fuel moisture content
governs ignition and spread, and its retrieval from satellite observation for fire-danger
assessment is a mature research area with a substantial operational literature [@Yebra2013].
Chuvieco et al. [@Chuvieco2004] established the specific combination used here — surface
temperature together with a vegetation index — as an estimator of live fuel moisture content for
fire-danger rating.

The index most directly relevant to our feature block is the Temperature-Vegetation Dryness Index,
introduced by Sandholt et al. [@Sandholt2002] as a simple interpretation of the LST-NDVI feature
space: a pixel's relative position between the moisture-unlimited "wet edge" and the
moisture-limited "dry edge" at its own vegetation-index level. TVDI is attractive for cross-region
work precisely because it is internally normalised — defined relative to edges fitted within the
scene — and therefore, in principle, less exposed to absolute-temperature offsets between regions
than raw land surface temperature. Whether that theoretical advantage survives contact with real
between-region differences is one of the questions this study answers empirically.

The most directly comparable body of work is the series by Maffei and colleagues. Maffei et al.
[@Maffei2018] related spatiotemporal patterns of burned area and fire duration to diurnal LST
anomalies computed against a climatological baseline — the same anomaly construction we use. Maffei
and Menenti [@MaffeiMenenti2019] predicted burned area and rate of spread from pre-fire
multispectral measurements, and Maffei et al. [@Maffei2021] extended this to a combined
multispectral-and-thermal prediction of fire characteristics, benchmarked against the Fire Weather
Index. Together these establish that pre-fire thermal state carries genuine information about
subsequent fire.

Underpinning all of it are the source products. The Landsat Level-2 surface temperature used here
derives from the operational retrieval of Malakar et al. [@Malakar2018], built on the calibration
methodology of Cook et al. [@Cook2014]. Burned-area labels come from the Collection 6 MODIS
burned-area algorithm [@Giglio2018], whose global validation [@Boschetti2019] documents the
omission and commission characteristics that bound any model trained against it. Land cover is ESA
WorldCover v200 [@Zanaga2022], and all satellite retrieval and compositing runs on Google Earth
Engine [@Gorelick2017].

**Where this literature stops.** The Maffei series demonstrates a relationship between pre-fire
thermal state and fire outcome, but always within a single region and within a probabilistic or
correlational frame — exceedance probabilities and decile-binned relationships rather than a
spatially validated classifier — and never with a transfer test. The question of whether the
relationship they identify is a *regionally stable* one is not posed. Two recent studies come
closer and must be acknowledged directly. Marino et al. [@Marino2024] explicitly test the
transferability of empirical satellite-derived live fuel moisture models to an uncalibrated region,
but what transfers there is a *moisture-retrieval* model, not a burned-versus-unburned classifier.
Gelabert et al. [@Gelabert2025] find dead fine fuel moisture content and its yearly anomalies — a
dynamic dryness-anomaly variable structurally analogous to our LST anomaly — to be the most
influential predictor of human-caused ignition likelihood across Europe, and do test spatial
generalisation by fitting a pooled model across five pilot sites and evaluating it per site, with
an AUC drop of roughly 0.10 at the weakest sites. That is a genuine cross-site generalisation test
of a dryness-dominated model, and it is why we do not claim that the transferability of pre-fire
dryness has "never been examined". What remains untested is narrower and, we argue, more decisive:
whether the *predictive skill* of a pre-fire thermal model trained in one fire region survives
strict train-in-A, apply-to-B transfer with no target labels, and whether label-free adaptation can
recover it if it does not. Gelabert et al.'s design pools regions during fitting and evaluates
locally, which measures something different — how well one shared model serves several places, not
whether the relationship learned in one place holds in another.

There is a further point this literature leaves implicit, and it is the one our thesis turns on.
The case for thermal dryness rests on a mechanism that is universal: moisture stress raises
flammability wherever vegetation burns, so a predictor built on that mechanism ought to be the
*most* portable kind of predictor available, not the least. But the quantity a satellite measures is
not fuel moisture; it is a surface state whose mapping onto flammability runs through fuel type,
canopy structure, terrain, seasonal phenology and the local relation between a thermal anomaly and
the dryness it stands for. Each of those mediating factors is regionally specific, so the
*relationship* between an observed thermal anomaly and burning may be locally reparameterised even
where the underlying physics is not. The work reviewed above cannot distinguish these two
possibilities, because a single-region study — or a pooled model evaluated locally — never places
the relationship learned in one region in contact with the data of another. Distinguishing them
requires strict train-in-A, apply-to-B transfer, and it is that test, rather than a further
demonstration of within-region skill, that the present study takes as its object.

## 2.3 Spatial validation and the transferability of ecological models

That randomly held-out spatial data give optimistically biased performance estimates when the data
are spatially autocorrelated is now a standard result. Roberts et al. [@Roberts2017] set out the
cross-validation strategies appropriate to temporally, spatially, hierarchically and
phylogenetically structured data; Ploton et al. [@Ploton2020] showed that spatial validation reveals
substantially poorer predictive performance in large-scale ecological mapping models than random
validation suggests. Blocked cross-validation, in which contiguous spatial units rather than
individual cells are assigned to folds, is the accepted correction, with an established
implementation [@Valavi2019] and a target-oriented variant for spatio-temporal data [@Meyer2018].

A parallel line asks not how well a model performs but *where* it can be trusted at all. Meyer and
Pebesma [@Meyer2021] formalised this as the area of applicability of a spatial prediction model,
defined in terms of dissimilarity in *predictor space* rather than geographic distance, and
subsequently argued that many published global maps of ecological variables are assessed in ways
that do not support their claimed coverage [@Meyer2022]. Ludwig et al. [@Ludwig2023] applied this
apparatus to existing global spatial prediction models and found their effective transferability
considerably narrower than advertised. This line of work is the field's principal answer to the
question "will this model travel?", and it is the standard we adopt: predictor-space dissimilarity
is a substantial advance on geographic distance, it is computable without target labels, and it
correctly flags the common case in which a model is asked to predict on inputs unlike anything it
was fitted to.

It is worth being precise, however, about what kind of quantity such an index is. The
area-of-applicability construction compares the *marginal* distribution of predictors in the target
domain against the marginal distribution in the source training sample; distance is measured in
scaled, importance-weighted predictor space, and the label plays no part in it beyond weighting the
axes. Predictor-space dissimilarity is therefore a statement about where the target data lie, not
about what the response does there.

In species distribution modelling, transferability has been examined far more systematically than
in fire science, and the conclusions are sobering. Yates et al. [@Yates2018] catalogue the
outstanding challenges. More pointedly for our purposes, two studies have already tested whether
proximity or similarity predicts transfer success and found that it does not: Vesk et al.
[@Vesk2021] report that predictive performance in target regions did not deteriorate with
increasing geographic, environmental or community-compositional distance from the reference region,
and Rousseau and Betts [@Rousseau2022] find environmental similarity to be a non-significant
predictor of transferability, with species and range traits mattering more.

**Where this literature stops.** This block supplies our evaluation standard and, in Vesk et al. and
Rousseau and Betts, an important precedent: the intuition that nearby or similar domains transfer
better has already been questioned outside fire science, so our corresponding claim is a
confirmation in a new domain rather than a discovery — a point we state explicitly rather than
letting a reviewer make it for us. It is also why we frame our version as a claim about
*sufficiency* (Section 2.5) rather than restating theirs. Two gaps remain. First, none of this work
has been applied to fire susceptibility, where the assumption of transferability is embedded in
every regional or pan-Mediterranean product but almost never tested.

Second, and more substantively, there is a structural blind spot in the diagnostic apparatus
itself, and it is the constructive opening this paper works from. Predictor-space dissimilarity is a
*marginal* quantity: it is computed from the distribution of the inputs alone. The failure mode we
document is *conditional*: the predictor distributions of two regions can overlap to an
unremarkable degree — target cells sitting comfortably inside the source's predictor envelope, so
that an applicability index raises no objection — while the association between a predictor and the
response differs, and in the sharpest case reverses sign, between them. In the taxonomy of Section
2.4 this is concept shift rather than covariate shift, and no index built from the marginal
predictor distribution can register it, because the two situations are indistinguishable in the
data the index consumes. This is a statement about what the construction can see, not a criticism of
how it has been applied: the area-of-applicability framework does exactly what it claims, and the
regime it was designed for — extrapolation beyond the training envelope — is real and widespread. We
therefore read our contribution as an extension rather than a correction. The blind spot has a
practical consequence worth stating plainly: for models built on dynamic state predictors, a
reassuring marginal diagnostic is not evidence of portability, and a model may be well inside its
nominal area of applicability and still perform at or below chance. Establishing this requires more
than an argument from construction, so we compute a predictor-space dissimilarity index alongside
climatic and geographic distances, test whether they order the observed transfer outcomes, and then
ask whether a conditional diagnostic — signed univariate association reversal between source and
target — tracks what the marginal ones miss.

## 2.4 Dataset shift and label-free domain adaptation

The machine-learning framing separates the ways a training and a deployment domain can differ.
Moreno-Torres et al. [@MorenoTorres2012] give the canonical taxonomy: covariate shift, in which the
input distribution changes while the conditional label distribution is preserved; prior or label
shift, in which class prevalence changes; and concept shift, in which the conditional relationship
between inputs and label changes. The distinction is the same marginal-versus-conditional
distinction that organises Section 2.3, and it has direct operational consequences, because only
the first is correctable without target labels: aligning input distributions cannot repair a
relationship that has itself changed.

That limitation is worth stating as a property of the methods rather than as an empirical finding
about any particular dataset. Both of the label-free alignment operations used here act on marginal
summary statistics of the predictors. Region-wise standardisation subtracts a per-region mean and
divides by a per-region standard deviation, so it equalises first and second marginal moments
coordinate by coordinate. Correlation alignment (CORAL) is the canonical simple, deterministic
extension of the same idea — a whitening-and-recolouring linear map that aligns the source feature
covariance to the target covariance [@Sun2016] — so it additionally equalises the second-order
cross-coordinate structure. Neither transformation consults a target label, and neither could: the
label is by construction unavailable. It follows that whatever either method achieves, it achieves
by making the source and target *input* distributions resemble one another more closely. If the
conditional relationship between inputs and label differs between the domains, then any
input-space map — including these two, and including any other method whose objective is defined on
the marginals alone — leaves that difference untouched. Where a predictor's association with the
response has opposite signs in the two regions, aligning the marginals can only bring the source
model's error into sharper focus, since it delivers target inputs to a decision rule fitted under
the opposite relationship. This is a logical consequence of what the methods optimise, not a result
we report; what remains genuinely empirical is how large the irreparable part is in a given
application, and that is what our experiments measure.

In remote sensing specifically, domain adaptation has an established literature surveyed by Tuia et
al. [@Tuia2016], and where unsupervised adaptation is insufficient, active learning has been used to
acquire a small number of maximally informative target labels [@Persello2012] — the standard
response once the conditional component is recognised as the binding constraint.

Very recently, shift decomposition has begun to appear in applied remote sensing. Huang et al.
[@Huang2026] compare transfer-learning strategies for hyperspectral foliar-trait retrieval and
quantitatively decompose domain shift into components across four transfer scenarios, reporting
concept shift as the dominant limitation on transferability. No effect coefficient or numerical
result of theirs is quoted here; the citation supports only the existence and direction of that
decomposition.

**Where this literature stops.** Huang et al. establish that decomposing transfer failure into shift
components is both possible and informative in an applied remote-sensing setting, and we do not
claim that idea as ours. Two differences remain, and they are the ones that matter. Theirs is a
hyperspectral regression problem, not a fire problem, and their instrument is a set of statistical
shift metrics regressed against the observed transferability gap. Ours is an *operational*
instrument: we use the performance of label-free adaptation itself as the measuring device, so that
the recoverable fraction of the gap is defined as what the best available label-free method actually
recovers, and the residual is what it demonstrably cannot. That definition has the advantage of
being decision-relevant — it answers "would unsupervised alignment fix this?" by trying it — and the
disadvantage of being method-dependent, which we report rather than conceal. Beyond that, we found
no application of CORAL or of region-wise feature alignment to fire susceptibility, fire occurrence
or burned-area prediction at all. Work labelled "domain adaptation" in the fire literature addresses
image-level post-fire tasks — burned-area segmentation, burn-severity mapping, smoke detection —
which share the vocabulary but not the problem.

What this block supplies to the present argument is the vocabulary in which the thesis can be stated
exactly. The portability cost of dynamic state predictors is not a covariate-shift problem that
better alignment would solve; it is a conditional change, and the marginal instruments the field
uses to anticipate transfer failure (Section 2.3) and the marginal operations it uses to repair it
are blind to it for the same reason. What the shift literature does not yet supply is a diagnostic
that operates on the conditional side and can be computed before deployment. Attempting the repair
and observing what it fails to recover is one such instrument, and pairing it with a feature-level
test for association reversal is the constructive part of our contribution.

## 2.5 Cross-region generalisation of fire models

A small number of studies test fire-model transfer directly, and they are the nearest neighbours of
the present work.

Podschwit et al. [@Podschwit2022] examined the reliability of applying global fire danger models
across regions in a Peruvian case study, and provide the long-standing reference point that
meteorologically derived danger indices do not port cleanly between fire environments.

Dimarco et al. [@Dimarco2026] is the closest Mediterranean analogue and the most important
comparison for this paper. They harmonise 500 m predictors across four Mediterranean countries, fit
random forest and gradient boosting models, select hyperparameters under five-fold spatial
cross-validation, evaluate on an 80/20 hold-out, and test transfer both leave-one-country-out and
as a full 4 × 4 transfer matrix. Their predictor set comprises NDVI; slope from ASTER GDEM; 2 m air
temperature, 10 m wind speed and relative humidity, all taken from ERA5-Land
[@MunozSabater2021] as **long-term seasonal means**; the global human modification index; VIIRS
night-time lights (and a log1p transform of the same); and population density.[^dimarco-lst] Their
target is burned-pixel centroids from MCD64A1 treated as an ignition proxy and matched against a
1:1 balanced background sample. They report that every transfer exceeds AUC 0.80, that transfers
between bioclimatically similar countries score higher, and that transfers to Morocco are
systematically lower — a drop they attribute not to climate alone but to differences in
anthropogenic drivers, fire management practice and data reporting. They apply no domain
adaptation.

[^dimarco-lst]: Their Results text refers to "LST anomalies", which is inconsistent with their own
Methods, where no land surface temperature or TVDI variable appears and the only temperature
predictor is a static ERA5-Land seasonal climatology. We follow their Methods, which we take to be
authoritative, and note the discrepancy here so that the comparison drawn below is transparent.
Every statement in this paragraph was checked against the full text (read 2026-08-08), not the
abstract alone.

Outside the Mediterranean, WildfireGenome [@Liu2025] performs the most systematic transfer
experiment we are aware of: a leave-one-county-out transfer matrix across seven ecologically diverse
US counties, with random forests and SHAP-based interpretation. It reports strong within-county
performance and highly variable off-diagonal transfer, with ecologically similar county pairs
transferring well and dissimilar pairs collapsing below chance. Its label, however, is a
principal-component composite of federal hazard *indicators* rather than observed burned area, and
it applies no domain adaptation and performs no shift decomposition. Finally, Xu et al. [@Xu2026]
argue that wildfire transfer conclusions depend strongly on evaluation design and task formulation —
a caution that applies to our results as much as to anyone's, and one we address by pre-specifying
the protocol and reporting every sensitivity axis.

For scaling this kind of work, Kondylatos et al. [@Kondylatos2023] provide Mesogeos, a
multi-purpose 1 km Mediterranean datacube built for data-driven wildfire modelling.

**Where this literature stops, and what this study adds.** These studies establish that fire-model
transfer is testable and that its outcome varies. What none of them asks is *what property of a
model* determines the outcome — transfer performance is reported per pair and explained, where it is
explained at all, by how similar the domains are. Read against ours, they set up an empirical
contrast that points to a different explanation, and that contrast is the most informative result
of the present work.

Dimarco et al. and this study share the essential experimental design — Mediterranean regions,
500 m cells, MCD64A1-derived targets, tree ensembles, spatially aware validation, an explicit
transfer matrix, and, as it happens, four regions and twelve ordered pairs each. What differs is the
**predictor class**. Their model is built on quantities that are attributes of a *place*: terrain
slope, night-time lights, human modification, population density, and temperature, wind and humidity
as long-term seasonal climatologies. Every one of these is spatially stationary — it describes a
region rather than a season — and their model transfers, everywhere above AUC 0.80. Our model is
built on the *state of a particular pre-fire window*: land surface temperature anomalies against a
multi-year baseline, thermal-optical dryness indices, and downscaled and fused thermal channels,
all composited over the weeks preceding a specific fire. Because the physics linking moisture stress
to combustion is universal, this predictor class is the one for which transfer should be *most*
expected. It is instead the one that fails.

The contrast, then, is not the one we initially expected to draw. It would be easy but wrong to
reduce it to target definition — their ignition proxy is human-driven, ours is burned area — and
easier still to reduce it to their finding that anthropogenic pressure dominates, which is a result
of their analysis rather than a feature of their design; their predictor set explicitly includes
vegetation condition, topography and climatic context. The sharper reading is about predictor class.
Every predictor in their model is an attribute of a *place*, stable across seasons and years, so a
model fitted on them is in effect learning a spatial ordering of susceptibility that a neighbouring
country can inherit. Every thermal predictor in ours describes the *state of a particular window*
preceding a particular fire, so the fitted model encodes not only which places are prone to burn
but how a given degree of anomalous dryness translates into burning in that region, in that season.
The first kind of knowledge travels; the second is exactly the kind that need not. The deeper point
this suggests — which our data support and cannot prove, and which we return to below — is that
predictor class, rather than domain similarity, is what governs portability: it is not that similar
regions transfer and dissimilar ones do not, but that stationary-attribute models track similarity
while dynamic-state models are reparameterised locally and therefore need not.

Three further differences must be stated precisely, because they bound how far the contrast can be
pushed. **Target:** they treat burned-pixel centroids as an ignition proxy against a 1:1 balanced
background, whereas we perform burned-area classification at the true, heavily imbalanced base rate
— a different problem with different achievable ceilings. **Thermal variable:** their temperature
predictor is a static reanalysis climatology, whereas ours are event-specific satellite thermal
observations referenced to their own baseline. **Adaptation:** they apply none, whereas the label-
blind adaptation step is central to our diagnosis. The contrast is therefore between two coherent
experimental programmes, not a controlled ablation, and we present it as such.

Why the predictor-response relationship should be reparameterised locally is a question this
literature can frame even if our design cannot settle it. Fire is conventionally described not as a
continuum but as a small number of distinguishable syndromes — pyromes, in the terminology of
Archibald et al. [@Archibald2013] — differing in the fuel, weather and ignition constraints that
limit burning in a given setting, and Pausas and Keeley [@Pausas2021] document how those constraints
are shifting under global change. Where burning is fuel-limited, additional dryness in an already
sparse system need not produce more of it; where it is drought-limited, the same anomaly is much
closer to a sufficient condition. If two regions sit in different limiting regimes, the mapping from
an observed thermal anomaly to burning probability differs between them by construction, even where
the predictor distributions overlap and the underlying combustion physics is identical — which is
precisely the conditional, marginally invisible difference described in Sections 2.3 and 2.4. We
offer regime typology as a candidate explanation consistent with what we observe, not as a
hypothesis this study tests: with the small number of regions available, a regime difference cannot
be distinguished from any other region-specific effect.

Five contributions follow, ordered by weight and stated at the strength the evidence supports.

**First — the trade-off itself, which is the paper's thesis.** We quantify, for every ordered region
pair, the change in transfer skill attributable to adding the dynamic pre-fire thermal block to a
matched static baseline, and set that against the within-region increment the same block delivers.
The claim is that the block gaining the most locally is the block losing the most between regions.
Dimarco et al. [@Dimarco2026] demonstrate the stationary-predictor half of this picture within the
same kind of Mediterranean design; our result is its complement, not its contradiction. Establishing
the portability half requires testing whether the predictive skill of pre-fire thermal state — not a
moisture-retrieval model [@Marino2024], and not a pooled multi-region model evaluated locally
[@Gelabert2025] — survives strict, label-free train-in-A, apply-to-B transfer. To our knowledge that
test has not been performed, but we state this as a gap in the transfer test specifically, not as an
absence of attention to the transferability of dryness predictors: Gelabert et al. come closer than
any other study, and the stronger wording would be indefensible.

**Second — label-free alignment does not recover transfer.** We test region-wise standardisation and
covariance alignment [@Sun2016] as label-blind remedies and characterise what each does to every
direction, including directions that already transfer. No application of CORAL or region-wise
feature alignment to fire susceptibility, fire occurrence or burned-area prediction was found in the
literature; work labelled "domain adaptation" in fire research addresses image-level post-fire
tasks. This is a negative result reported with a mechanism rather than an absence.

**Third — geographic and bioclimatic similarity are not sufficient for transfer.** This is
deliberately a sufficiency claim rather than a claim about correlation across pairs, and it is
therefore established by a single strong counterexample rather than by a sample of pairs: Manavgat
and Muğla lie in the same country, burned in the same fire year, sit roughly 200 km apart and share
a bioclimatic setting — about as similar as two independent fire regions can be — and transfer
between them collapses. Notably, Dimarco et al.'s own results point the same way from the other
side: they attribute the systematically weaker transfer to Morocco to anthropogenic drivers, fire
management and data reporting rather than to climate alone, which is itself an admission that
bioclimatic similarity does not account for transfer performance on its own.

**Fourth — a conditional transferability diagnostic.** We compute area-of-applicability-style
dissimilarity in predictor space [@Meyer2021; @Meyer2022; @Ludwig2023] alongside climatic and
geographic distance, report whether these marginal indices order the observed transfer outcomes, and
supply a conditional alternative: signed reversal in the univariate association between a predictor
and burning, paired with label-free adaptation performance as an operational instrument for
separating recoverable from irreducible shift. Shift decomposition in applied remote sensing is not
itself new [@Huang2026]; what is new here is the fire application, the adaptation-as-instrument
formulation, and the direct contrast between a marginal and a conditional diagnostic evaluated on
the same region pairs. This is the constructive contribution, and it is what distinguishes the paper
from a purely negative result.

**Fifth — within-region replication.** We replicate the thermal increment across independent
Mediterranean regions under spatially blocked cross-validation with spatial-block bootstrap
intervals, and characterise its behaviour as blocks coarsen. This finding is not itself novel —
comparable within-region results exist for these very landscapes [@AlkanAkinci2023; @Iban2022] — and
it is included because it supplies the first half of the trade-off in the first contribution.

Alongside these we release the protocol, code and frozen outputs, so that a negative transfer result
can be checked rather than taken on trust [@Xu2026].

We present the third of these as a **live disagreement**, not a settled result. Vesk et al.
[@Vesk2021] and Rousseau and Betts [@Rousseau2022] align with our direction, having already found
that geographic and environmental similarity fail to predict transfer success in species
distribution models; Dimarco et al. [@Dimarco2026] and WildfireGenome [@Liu2025] run against it,
both reporting that similar domains transfer better. The reading we favour — and which our data
support without proving — is that the relationship between domain similarity and transfer success is
**predictor-class dependent**: models built on spatially stationary attributes track similarity,
while models built on dynamic state need not.
