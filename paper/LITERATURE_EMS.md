# Referee-suggested literature, verified (EMS rewrite)

Compiled 2026-09-19 by the bibliography agent. Every work below was resolved via the Crossref
REST API (`https://api.crossref.org/works/<DOI>`); author list, title, journal, volume, issue,
pages/article number and year are Crossref's. Summaries are written **from the abstract only**,
never from memory of the paper body. The abstract source is named for each entry (Crossref where
it carries one; otherwise the stated open repository or publisher page).

"Bears on" lines say how the work could be used in the rewrite; they are proposals, not claims
the paper already makes.

Status key: **VERIFIED** (exists, metadata confirmed, abstract read) · **IN BIB** (already an
entry in `REFERENCES.bib`; no new BibTeX needed) · **NOT VERIFIED** (reason given).

None of the new BibTeX blocks below is in `REFERENCES.bib`: uncited entries are not allowed there.
Paste a block only when the manuscript cites the key. Titles follow the bib's sentence-case
convention; wording is Crossref's.

---

## A. Spatial validation, extent effects on AUC, transferability

### Hijmans 2012 — VERIFIED
Hijmans, R. J. (2012). Cross-validation of species distribution models: removing spatial sorting
bias and calibration with a null model. *Ecology* 93(3), 679–688. DOI 10.1890/11-0826.1
(abstract: Crossref)

**Summary.** Using 226 species, six regions and two algorithms (Bioclim, MaxEnt), shows that
cross-validated AUC is highly sensitive to "spatial sorting bias": the difference between the
distances from test-presence and from test-absence (or background) sites to training-presence
sites. A null model that uses only geographic distance to training sites beat MaxEnt for 45% and
Bioclim for 67% of species. Pairwise distance sampling removes the bias (null AUC near 0.5), and
the adjustment strongly lowered AUC and changed species rankings.

**Bears on:** spatial validation / extent effects on AUC — a distance-only null model is a direct
check on whether within-region AUC reflects geography rather than the predictors.

```bibtex
@article{Hijmans2012,
  author  = {Hijmans, Robert J.},
  title   = {Cross-validation of species distribution models: removing spatial
             sorting bias and calibration with a null model},
  journal = {Ecology},
  volume  = {93},
  number  = {3},
  pages   = {679--688},
  year    = {2012},
  doi     = {10.1890/11-0826.1},
}
```

### Wenger & Olden 2012 — VERIFIED
Wenger, S. J., Olden, J. D. (2012). Assessing transferability of ecological models: an
underappreciated aspect of statistical validation. *Methods in Ecology and Evolution* 3(2),
260–267. DOI 10.1111/j.2041-210X.2011.00170.x (abstract: Crossref; online 2012-01-23, issue
April 2012)

**Summary.** Argues that conventional in- or out-of-sample validation does not assess model
generality and can overestimate performance in other places, times or data sets. Proposes
cross-validation with data assigned non-randomly to spatially, temporally or otherwise distinct
groups. In a trout distribution example, random forests and neural networks had excellent
in-sample performance but poor transferability unless complexity was constrained, whereas linear
models transferred better.

**Bears on:** model transferability — early statement that flexible learners (including RF) can
fit well locally and transfer poorly; parallels the local-skill / portability trade-off.

```bibtex
@article{WengerOlden2012,
  author  = {Wenger, Seth J. and Olden, Julian D.},
  title   = {Assessing transferability of ecological models: an
             underappreciated aspect of statistical validation},
  journal = {Methods in Ecology and Evolution},
  volume  = {3},
  number  = {2},
  pages   = {260--267},
  year    = {2012},
  doi     = {10.1111/j.2041-210X.2011.00170.x},
}
```

### Yates et al. 2018 — VERIFIED; now IN BIB as `Yates2018` (added in Task 1)
Yates, K. L., Bouchet, P. J., Caley, M. J., et al. (50 authors) (2018). Outstanding challenges in
the transferability of ecological models. *Trends in Ecology & Evolution* 33(10), 790–802.
DOI 10.1016/j.tree.2018.08.001 (abstract: OpenAlex, Crossref carries none)

**Summary.** Notes that limited understanding of how accurate and precise models are when
transferred to novel conditions undermines confidence in their predictions. Fifty experts
identified priority knowledge gaps, summarised as six technical and six fundamental challenges.
It gives high priority to a widely applicable set of transferability metrics and tools for
quantifying sources of prediction uncertainty under novel conditions.

**Bears on:** model transferability — framing reference; already cited in the appendices.

### Meyer & Pebesma 2021 — VERIFIED; now IN BIB as `Meyer2021` (added in Task 1)
Meyer, H., Pebesma, E. (2021). Predicting into unknown space? Estimating the area of
applicability of spatial prediction models. *Methods in Ecology and Evolution* 12(9), 1620–1633.
DOI 10.1111/2041-210X.13650 (abstract: Crossref)

**Summary.** Proposes a dissimilarity index (DI): the minimum distance to training data in
importance-weighted predictor space. The area of applicability (AOA) is the region where DI is
below a threshold set from the cross-validated DI of the training data. In simulations,
prediction error inside the AOA matched cross-validation error, while cross-validation error did
not hold outside it. The authors recommend reporting predictions only within the AOA, with
DI-dependent performance maps.

**Bears on:** model transferability — the marginal predictor-space diagnostic that the paper's
diagnostics comparison tests. The AOA is defined on predictors, not labels.

### Milà et al. 2022 — VERIFIED; now IN BIB as `Mila2022` (added in Task 1)
Milà, C., Mateu, J., Pebesma, E., Meyer, H. (2022). Nearest neighbour distance matching
Leave-One-Out Cross-Validation for map validation. *Methods in Ecology and Evolution* 13(6),
1304–1316. DOI 10.1111/2041-210X.13851 (abstract: Crossref)

**Summary.** Proposes NNDM LOO CV, which matches the nearest-neighbour distance distribution
between test and training points during CV to the one between prediction and training
locations. In simulations with random forest, standard LOO worked for short autocorrelation
ranges or interpolation from random samples. Buffered LOO was realistic for new prediction areas
but overestimated interpolation error. NNDM LOO was reliable in all scenarios considered.

**Bears on:** spatial validation — the right CV design depends on the prediction task
(interpolation vs. extrapolation). This supports keeping within-region blocked CV separate from
cross-region transfer.

### Wadoux et al. 2021 — VERIFIED; now IN BIB as `Wadoux2021` (added in Task 1)
Wadoux, A. M. J.-C., Heuvelink, G. B. M., de Bruin, S., Brus, D. J. (2021). Spatial
cross-validation is not the right way to evaluate map accuracy. *Ecological Modelling* 457,
109692. DOI 10.1016/j.ecolmodel.2021.109692 (abstract: WUR research portal,
research.wur.nl; Crossref carries none)

**Summary.** Argues that claims that standard CV is invalid for spatial data rest on a
misconception. Unbiased map-accuracy estimates come from probability sampling and design-based
inference. In an above-ground-biomass experiment, standard CV had smaller bias than spatial CV.
Standard CV was deficient for strongly clustered data, though less so than spatial CV. The
authors conclude that spatial CV has no theoretical underpinning for map-accuracy assessment.

**Bears on:** spatial validation — the counter-position to blocked CV. It is needed so the paper
does not present blocking as settled, and it supports reporting results at several block sizes.

### Roberts et al. 2017 — IN BIB as `Roberts2017`
Roberts, D. R., et al. (2017). Cross-validation strategies for data with temporal, spatial,
hierarchical, or phylogenetic structure. *Ecography* 40(8), 913–929. DOI 10.1111/ecog.02881.
Existing entry re-checked against Crossref: all fields match (14 authors, 40(8), 913–929).

**Summary (abstract, Crossref).** Ignoring dependence structure in cross-validation seriously
underestimates predictive error and allows overfitting with non-causal predictors. Blocking can
also induce extrapolation and overestimate interpolation error. Across the simulations and case
studies, block CV was nearly always more appropriate than random CV when predicting to new data
or new predictor space.

**Bears on:** spatial validation — already cited; its "blocking can overestimate interpolation
error" point pairs with Wadoux2021.

### Bennett et al. 2013 — VERIFIED
Bennett, N. D., Croke, B. F. W., Guariso, G., Guillaume, J. H. A., Hamilton, S. H.,
Jakeman, A. J., Marsili-Libelli, S., Newham, L. T. H., Norton, J. P., Perrin, C., Pierce, S. A.,
Robson, B., Seppelt, R., Voinov, A. A., Fath, B. D., Andreassian, V. (2013). Characterising
performance of environmental models. *Environmental Modelling & Software* 40, 1–20.
DOI 10.1016/j.envsoft.2012.09.011 (abstract: ORBilu, orbilu.uni.lu/handle/10993/64935; Crossref
carries none)

**Summary.** Reviews numerical, graphical and qualitative methods for characterising the
performance of environmental models. It covers direct value comparison, coupling of real and
modelled values, preservation of data patterns, parameter-based indirect metrics and data
transformations. It proposes a five-step procedure: reassess the model's aim, scale and scope;
characterise the calibration and testing data; use visual and other analysis to find
under-modelled behaviour; choose basic performance criteria; then consider advanced methods for
systematic divergence.

**Bears on:** spatial validation / reporting — the EMS house reference for performance
evaluation. It supports using several metrics (ROC-AUC, PR-AUC, CIs) rather than one.

Note: Crossref spells the last author "Andreassian" without an accent; the block follows Crossref.

```bibtex
@article{Bennett2013,
  author  = {Bennett, Neil D. and Croke, Barry F. W. and Guariso, Giorgio and
             Guillaume, Joseph H. A. and Hamilton, Serena H. and
             Jakeman, Anthony J. and Marsili-Libelli, Stefano and
             Newham, Lachlan T. H. and Norton, John P. and Perrin, Charles and
             Pierce, Suzanne A. and Robson, Barbara and Seppelt, Ralf and
             Voinov, Alexey A. and Fath, Brian D. and Andreassian, Vazken},
  title   = {Characterising performance of environmental models},
  journal = {Environmental Modelling \& Software},
  volume  = {40},
  pages   = {1--20},
  year    = {2013},
  doi     = {10.1016/j.envsoft.2012.09.011},
}
```

### Lobo, Jiménez-Valverde & Real 2008 — IN BIB as `Lobo2008`
*Global Ecology and Biogeography* 17(2), 145–151. DOI 10.1111/j.1466-8238.2007.00358.x.
Existing entry re-checked against Crossref: matches (online 2007, issue 2008).

**Summary (abstract, Crossref).** Questions AUC as a comparative accuracy measure and gives five
reasons against it. The most important is that the total extent over which models are built
strongly influences the rate of well-predicted absences and hence AUC. The others are that AUC
ignores predicted probabilities and goodness-of-fit, covers rarely used ROC regions, weights
omission and commission equally, and says nothing about the spatial distribution of errors.

**Bears on:** extent effects on AUC — already cited. It is the reason AUCs from differently
framed AOIs are not directly comparable.

### Phillips et al. 2009 — VERIFIED
Phillips, S. J., Dudík, M., Elith, J., Graham, C. H., Lehmann, A., Leathwick, J., Ferrier, S.
(2009). Sample selection bias and presence-only distribution models: implications for
background and pseudo-absence data. *Ecological Applications* 19(1), 181–197.
DOI 10.1890/07-2153.1 (abstract: Crossref)

**Summary.** Occurrence records are often spatially biased while background data are drawn at
random, and the mismatch can bias models. The authors propose background data with the same bias
as the occurrences, and in practice use "target-group" background (all occurrences of a group
surveyed similarly). Across 226 species, target-group background improved average performance
for every method tested, with an effect as large as the choice of method.

**Bears on:** extent effects on AUC / label framing — the choice of background (here, which
unburned cells enter the frame) changes measured performance as much as the model does. This
matters for AOI and burnable-population framing.

```bibtex
@article{Phillips2009,
  author  = {Phillips, Steven J. and Dud{\'i}k, Miroslav and Elith, Jane and
             Graham, Catherine H. and Lehmann, Anthony and Leathwick, John and
             Ferrier, Simon},
  title   = {Sample selection bias and presence-only distribution models:
             implications for background and pseudo-absence data},
  journal = {Ecological Applications},
  volume  = {19},
  number  = {1},
  pages   = {181--197},
  year    = {2009},
  doi     = {10.1890/07-2153.1},
}
```

### Aronow, Samii & Assenova 2015 — VERIFIED
Aronow, P. M., Samii, C., Assenova, V. A. (2015). Cluster–robust variance estimation for dyadic
data. *Political Analysis* 23(4), 564–577. DOI 10.1093/pan/mpv018 (abstract: Crossref)

**Summary.** In dyadic data, multiple dyads share a member, so their errors are likely
correlated. Many analyses ignore this. The paper proposes a non-parametric sandwich-type robust
variance estimator for linear regression under dyadic clustering, gives consistency conditions,
and extends it to directed, repeated, weighted and longitudinal dyads and to GLMs such as
logistic regression.

**Bears on:** model transferability (inference) — region-pair statistics (e.g., diagnostics vs.
transfer AUC over ordered directions) are dyadic, since each region appears in many pairs. This
is the formal basis for pair-aware uncertainty.

```bibtex
@article{Aronow2015,
  author  = {Aronow, Peter M. and Samii, Cyrus and Assenova, Valentina A.},
  title   = {Cluster--robust variance estimation for dyadic data},
  journal = {Political Analysis},
  volume  = {23},
  number  = {4},
  pages   = {564--577},
  year    = {2015},
  doi     = {10.1093/pan/mpv018},
}
```

---

## B. Fire-regime drivers and fire–environment modelling

### Parisien & Moritz 2009 — VERIFIED
Parisien, M.-A., Moritz, M. A. (2009). Environmental controls on the distribution of wildfire
at multiple spatial scales. *Ecological Monographs* 79(1), 127–154. DOI 10.1890/07-1289.1
(abstract: Crossref)

**Summary.** Uses Maxent and boosted regression trees to model the environmental space of
wildfire in the conterminous USA, California and five Californian ecoregions. The models were
projected to other regions to test generality and spatial transferability. Predictions of the
potential range of wildfire had high classification accuracy. Models transferred to other areas
were useful only when they overlapped appreciably with the target's environmental space.

**Bears on:** model transferability — direct fire-domain precedent for testing transfer across
regions; its conclusion is framed in predictor-space overlap.

```bibtex
@article{ParisienMoritz2009,
  author  = {Parisien, Marc-Andr{\'e} and Moritz, Max A.},
  title   = {Environmental controls on the distribution of wildfire at multiple
             spatial scales},
  journal = {Ecological Monographs},
  volume  = {79},
  number  = {1},
  pages   = {127--154},
  year    = {2009},
  doi     = {10.1890/07-1289.1},
}
```

### Krawchuk & Moritz 2011 — VERIFIED
Krawchuk, M. A., Moritz, M. A. (2011). Constraints on global fire activity vary across a resource
gradient. *Ecology* 92(1), 121–132. DOI 10.1890/09-1843.1 (abstract: OpenAlex; Crossref carries
none)

**Summary.** A global empirical test of the varying-constraints hypothesis, using monthly fire
activity, soil moisture and mid-tropospheric circulation for 2001–2007 across gradients of net
primary productivity, temperature and biome. Where fuel is always available (mid-to-high NPP),
fuel moisture is the strongest constraint on fire. Where resources are limiting or variable
(deserts, xeric shrublands, grasslands/savannas), fuel moisture matters less and antecedent fuel
production matters more.

**Bears on:** Mediterranean fire regimes — a mechanism for why a dryness predictor's effect can
change between regions. This is a concept-shift explanation, not a covariate-shift one.

```bibtex
@article{KrawchukMoritz2011,
  author  = {Krawchuk, Meg A. and Moritz, Max A.},
  title   = {Constraints on global fire activity vary across a resource
             gradient},
  journal = {Ecology},
  volume  = {92},
  number  = {1},
  pages   = {121--132},
  year    = {2011},
  doi     = {10.1890/09-1843.1},
}
```

### Pausas & Fernández-Muñoz 2012 — VERIFIED
Pausas, J. G., Fernández-Muñoz, S. (2012). Fire regime changes in the Western Mediterranean
Basin: from fuel-limited to drought-driven fire regime. *Climatic Change* 110(1–2), 215–226.
DOI 10.1007/s10584-011-0060-6 (abstract: SpringerLink article page; Crossref carries none.
Crossref "issued" is the 2011 online date; print issue January 2012, hence year 2012.)

**Summary.** Compiles a 130-year fire history for Valencia province (eastern Spain) with rural
population and climate records. It finds a major fire-regime shift around the early 1970s, when
fire frequency doubled and area burned rose by about an order of magnitude. The main driver was
fuel build-up after rural depopulation. Climate was weakly related to pre-1970s fires and
strongly related to post-1970s fires, so fire became less fuel-limited and more drought-driven.

**Bears on:** Mediterranean fire regimes — the Bejís region lies in this province. It shows that
the fire–climate relationship itself changes with fuel history.

```bibtex
@article{PausasFernandezMunoz2012,
  author  = {Pausas, Juli G. and Fern{\'a}ndez-Mu{\~n}oz, Santiago},
  title   = {Fire regime changes in the {Western Mediterranean Basin}: from
             fuel-limited to drought-driven fire regime},
  journal = {Climatic Change},
  volume  = {110},
  number  = {1--2},
  pages   = {215--226},
  year    = {2012},
  doi     = {10.1007/s10584-011-0060-6},
}
```

### Pausas & Paula 2012 — VERIFIED
Pausas, J. G., Paula, S. (2012). Fuel shapes the fire–climate relationship: evidence from
Mediterranean ecosystems. *Global Ecology and Biogeography* 21(11), 1074–1082.
DOI 10.1111/j.1466-8238.2012.00769.x (abstract: Crossref)

**Summary.** Across 13 Iberian regions along an aridity/productivity gradient, the aridity level
at which conditions switch to flammable rose along the gradient. Differences in fire activity
between regions were explained by the sensitivity of fire to flammable conditions, not by how
often those conditions occurred; sensitivity was higher in wetter, more productive regions. The
authors conclude that fuel structure matters more than climate frequency and that fuel sets the
aridity threshold.

**Bears on:** Mediterranean fire regimes / transferability — region-specific dryness thresholds
and sensitivities are a published mechanism for why the dryness–burn relationship is not portable.

```bibtex
@article{PausasPaula2012,
  author  = {Pausas, Juli G. and Paula, Susana},
  title   = {Fuel shapes the fire--climate relationship: evidence from
             {Mediterranean} ecosystems},
  journal = {Global Ecology and Biogeography},
  volume  = {21},
  number  = {11},
  pages   = {1074--1082},
  year    = {2012},
  doi     = {10.1111/j.1466-8238.2012.00769.x},
}
```

### Turco et al. 2017 — VERIFIED
Turco, M., von Hardenberg, J., AghaKouchak, A., Llasat, M. C., Provenzale, A., Trigo, R. M.
(2017). On the key role of droughts in the dynamics of summer fires in Mediterranean Europe.
*Scientific Reports* 7(1), 81. DOI 10.1038/s41598-017-00116-9 (abstract: Crossref)

**Summary.** Models summer burned area across all Mediterranean European eco-regions from
same-summer drought and antecedent wet conditions (a proxy for fuel amount and structure). It
finds a statistically significant fire–drought relationship in most regions. Antecedent
conditions play a relatively minor role except in a few eco-regions. The per-eco-region models
are presented as promising for seasonal forecasting.

**Bears on:** Mediterranean fire weather — the fire–climate link varies by eco-region. This is
context for regional differences among the study events.

```bibtex
@article{Turco2017,
  author  = {Turco, Marco and von Hardenberg, Jost and AghaKouchak, Amir and
             Llasat, Maria Carmen and Provenzale, Antonello and
             Trigo, Ricardo M.},
  title   = {On the key role of droughts in the dynamics of summer fires in
             {Mediterranean Europe}},
  journal = {Scientific Reports},
  volume  = {7},
  number  = {1},
  pages   = {81},
  year    = {2017},
  doi     = {10.1038/s41598-017-00116-9},
}
```

### Oliveira et al. 2012 — VERIFIED
Oliveira, S., Oehler, F., San-Miguel-Ayanz, J., Camia, A., Pereira, J. M. C. (2012). Modeling
spatial patterns of fire occurrence in Mediterranean Europe using Multiple Regression and Random
Forest. *Forest Ecology and Management* 275, 117–129. DOI 10.1016/j.foreco.2012.03.003
(abstract: OpenAIRE record; Crossref carries none)

**Summary.** Models June–September fire density across European Mediterranean countries (EFFIS
European Fire Database) from physical, socio-economic and demographic predictors. It compares
multiple linear regression with random forest; RF had higher predictive ability and better
residual behaviour. Precipitation and soil moisture were influential in both models, as were
unemployment, livestock density and local-road density. Fire-likelihood maps at 10 km show high
variability across the region.

**Bears on:** Mediterranean fire regimes / method — random forest precedent for Mediterranean
fire occurrence at broad scale. Its predictors are occurrence drivers, not pre-fire thermal
state.

```bibtex
@article{Oliveira2012,
  author  = {Oliveira, Sandra and Oehler, Friderike and
             San-Miguel-Ayanz, Jes{\'u}s and Camia, Andrea and
             Pereira, Jos{\'e} M. C.},
  title   = {Modeling spatial patterns of fire occurrence in {Mediterranean
             Europe} using {Multiple Regression} and {Random Forest}},
  journal = {Forest Ecology and Management},
  volume  = {275},
  pages   = {117--129},
  year    = {2012},
  doi     = {10.1016/j.foreco.2012.03.003},
}
```

### Bar Massada et al. 2013 — VERIFIED
Bar Massada, A., Syphard, A. D., Stewart, S. I., Radeloff, V. C. (2013). Wildfire
ignition-distribution modelling: a comparative study in the Huron–Manistee National Forest,
Michigan, USA. *International Journal of Wildland Fire* 22(2), 174–183. DOI 10.1071/WF11178
(abstract: Crossref. Crossref "issued" is the 2012 online date; print issue 2013.)

**Summary.** Compares GLM, random forests and Maxent for ignition-distribution modelling using
16 years of ignitions. RF and Maxent had slightly better prediction accuracy than GLM, with
similar fit. Human population/development variables and elevation were the top predictors in all
models. Despite similar performance and predictors, Maxent's probability map was markedly
different, so the authors recommend comparing or ensembling model types.

**Bears on:** model transferability / method — similar AUCs can hide very different spatial
predictions. This is a caution when AUC is the only yardstick.

```bibtex
@article{BarMassada2013,
  author  = {Bar Massada, Avi and Syphard, Alexandra D. and Stewart, Susan I. and
             Radeloff, Volker C.},
  title   = {Wildfire ignition-distribution modelling: a comparative study in
             the {Huron--Manistee National Forest}, {Michigan}, {USA}},
  journal = {International Journal of Wildland Fire},
  volume  = {22},
  number  = {2},
  pages   = {174--183},
  year    = {2013},
  doi     = {10.1071/WF11178},
}
```

---

## C. Lower-confidence items

### Ruffault et al. 2018 (NHESS) — VERIFIED
Ruffault, J., Curt, T., Martin-StPaul, N. K., Moron, V., Trigo, R. M. (2018). Extreme wildfire
events are linked to global-change-type droughts in the northern Mediterranean. *Natural Hazards
and Earth System Sciences* 18(3), 847–856. DOI 10.5194/nhess-18-847-2018 (abstract: Crossref)

**Summary.** Analyses the weather of extreme wildfires in Mediterranean France in the dry summers
of 2003 and 2016. In both years, fire weather shifted into conditions not seen before, through
interactions between drought types and fire-weather types. In 2016, a long "press drought"
intensified wind-driven fires. In 2003, a "hot drought" (heat wave plus press drought)
intensified heat-induced fires.

**Bears on:** Mediterranean fire weather — distinct fire-weather types (wind-driven vs.
heat-induced) could make a thermal-dryness signal informative in some events and not others.

```bibtex
@article{Ruffault2018,
  author  = {Ruffault, Julien and Curt, Thomas and Martin-StPaul, Nicolas K. and
             Moron, Vincent and Trigo, Ricardo M.},
  title   = {Extreme wildfire events are linked to global-change-type droughts
             in the northern {Mediterranean}},
  journal = {Natural Hazards and Earth System Sciences},
  volume  = {18},
  number  = {3},
  pages   = {847--856},
  year    = {2018},
  doi     = {10.5194/nhess-18-847-2018},
}
```

### Ruffault et al. 2020 (Scientific Reports) — VERIFIED
Ruffault, J., Curt, T., Moron, V., Trigo, R. M., Mouillot, F., Koutsias, N., Pimont, F.,
Martin-StPaul, N., Barbero, R., Dupuy, J.-L., Russo, A., Belhadj-Khedher, C. (2020). Increased
likelihood of heat-induced large wildfires in the Mediterranean Basin. *Scientific Reports*
10(1), 13790. DOI 10.1038/s41598-020-70069-z (abstract: Crossref)

**Summary.** Uses a fire-weather classification of wildfires to show that future scenarios
increase the frequency of two heat-induced fire-weather types (heatwave; hot drought), which are
linked to recent largest fires. Their frequency is projected to rise by 14% (RCP4.5) and 30%
(RCP8.5) by 2071–2100. The authors infer that large-wildfire frequency and extent will increase
across the Mediterranean Basin.

**Bears on:** Mediterranean fire weather — basin-wide typology of fire weather; supports treating
events as drawn from different fire-weather regimes.

```bibtex
@article{Ruffault2020,
  author  = {Ruffault, Julien and Curt, Thomas and Moron, Vincent and
             Trigo, Ricardo M. and Mouillot, Florent and Koutsias, Nikos and
             Pimont, Fran{\c{c}}ois and Martin-StPaul, Nicolas and
             Barbero, Renaud and Dupuy, Jean-Luc and Russo, Ana and
             Belhadj-Khedher, Chiraz},
  title   = {Increased likelihood of heat-induced large wildfires in the
             {Mediterranean Basin}},
  journal = {Scientific Reports},
  volume  = {10},
  number  = {1},
  pages   = {13790},
  year    = {2020},
  doi     = {10.1038/s41598-020-70069-z},
}
```

### Nolan et al. 2016, *Global Change Biology* (fuel-moisture thresholds) — NOT VERIFIED as stated
Crossref searches (author "Nolan Boer", 2016; bibliographic queries on fuel moisture thresholds
in *Global Change Biology*) returned no 2016 Nolan fuel-moisture paper in *Global Change
Biology*. The work that matches the description ("clear thresholds of fuel moisture content")
is in **Geophysical Research Letters**, not GCB. The referee probably misremembered the journal;
confirm with the referee before citing. The GRL paper is verified:

Nolan, R. H., Boer, M. M., Resco de Dios, V., Caccamo, G., Bradstock, R. A. (2016). Large-scale,
dynamic transformations in fuel moisture drive wildfire activity across southeastern Australia.
*Geophysical Research Letters* 43(9), 4229–4238. DOI 10.1002/2016GL068614 (abstract: Crossref)

**Summary.** Uses macroscale monitoring of dead and live fuel moisture, combining remote sensing
and climate modelling, to ask what counts as "sufficiently dry" to burn. It finds clear
fuel-moisture thresholds associated with wildfire occurrence in forests and woodlands. It also
finds that fuel moisture can move across these thresholds rapidly, within a month.

**Bears on:** Mediterranean fire weather / dryness — threshold behaviour and rapid transitions
bear on how informative a single pre-fire thermal-dryness snapshot can be. The study region is
southeastern Australia, not the Mediterranean.

Crossref gives only initials for the authors; the block follows Crossref.

```bibtex
@article{Nolan2016,
  author  = {Nolan, R. H. and Boer, M. M. and Resco de Dios, V. and
             Caccamo, G. and Bradstock, R. A.},
  title   = {Large-scale, dynamic transformations in fuel moisture drive
             wildfire activity across southeastern {Australia}},
  journal = {Geophysical Research Letters},
  volume  = {43},
  number  = {9},
  pages   = {4229--4238},
  year    = {2016},
  doi     = {10.1002/2016GL068614},
}
```

### MCD64A1 accuracy (Boschetti et al.; Giglio et al.) — IN BIB
- `Giglio2018`: Giglio, L., Boschetti, L., Roy, D. P., Humber, M. L., Justice, C. O. (2018). The
  Collection 6 MODIS burned area mapping algorithm and product. *Remote Sensing of Environment*
  217, 72–85. DOI 10.1016/j.rse.2018.08.005.
- `Boschetti2019`: Boschetti, L., Roy, D. P., Giglio, L., Huang, H., Zubkova, M., Humber, M. L.
  (2019). Global validation of the Collection 6 MODIS burned area product. *Remote Sensing of
  Environment* 235, 111490. DOI 10.1016/j.rse.2019.111490.

Both are already cited. They carry the burned-area label-error argument, so no further MCD64A1
paper is needed unless a referee names a specific one.
