# Literature metadata — supplied by the author (Yunus Emre Coğurcu), 2026-07-23

This file records the literature search results **as supplied**, before independent verification.
Verification status is tracked in the right-hand column and updated in `REFERENCES.bib`; the
rewritten `02_related_work.md` cites only entries that reached `VERIFIED` or are explicitly marked
`[UNVERIFIED: ...]` in the text.

Legend: `VERIFIED` = author–title–venue–year–DOI cross-checked against an independent source ·
`PARTIAL` = work exists, some field (volume, pages, author list) unconfirmed ·
`UNVERIFIED` = could not be confirmed; must not be cited as fact.

---

## Block A — Fire susceptibility mapping with machine learning

| # | Citation as supplied | Status |
|---|---|---|
| A1 | Iban MC, Sekertekin A (2022). Machine learning based wildfire susceptibility mapping using remotely sensed fire data and GIS: A case study of Adana and Mersin provinces, Turkey. *Ecological Informatics* 69:101647. doi:10.1016/j.ecoinf.2022.101647 — **target journal; same provinces as the Kozan negative control** | see verification log |
| A2 | Manavgat forest fire susceptibility (2023). *Earth Science Informatics*. doi:10.1007/s12145-023-00953-5 — **our anchor AOI; author names to confirm** | see verification log |
| A3 | İzmir SHAP wildfire susceptibility (2024). *Remote Sensing* 16(15):2842. doi:10.3390/rs16152842 | see verification log |
| A4 | Systematic literature review, forest fire susceptibility (2026). *Discover Artificial Intelligence*. doi:10.1007/s44163-026-00921-0 | see verification log |
| A5 | AI and remote sensing wildfire review (2026). *AIMS Environmental Science*. doi:10.3934/environsci.2026004 | see verification log |

## Block B — Thermal dryness indicators

| # | Citation as supplied | Status |
|---|---|---|
| B1 | Sandholt I, Rasmussen K, Andersen J (2002). A simple interpretation of the surface temperature/vegetation index space for assessment of surface moisture status. *Remote Sensing of Environment* 79(2–3):213–224. doi:10.1016/S0034-4257(01)00274-7 | see verification log |
| B2 | Maffei C et al. (2018). Relating Spatiotemporal Patterns of Forest Fires Burned Area and Duration to Diurnal Land Surface Temperature Anomalies. *Remote Sensing* 10(11):1777. doi:10.3390/rs10111777 | see verification log |
| B3 | Maffei C, Lindenbergh R, Menenti M (2021). Combining multi-spectral and thermal remote sensing to predict forest fire characteristics. *ISPRS Journal of Photogrammetry and Remote Sensing*. Volume/pages to confirm | see verification log |
| B4 | Chuvieco E et al. (2004). Combining NDVI and surface temperature for the estimation of live fuel moisture content in forest fire danger rating. *Remote Sensing of Environment* 92:322–331. doi:10.1016/j.rse.2004.01.019 | see verification log |

## Block C — Spatial validation and transferability

| # | Citation as supplied | Status |
|---|---|---|
| C1 | Roberts DR et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40:913–929. | see verification log |
| C2 | Ploton P et al. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. *Nature Communications*. doi:10.1038/s41467-020-18321-y | see verification log |
| C3 | Meyer H, Pebesma E (2021). Predicting into unknown space? Estimating the area of applicability of spatial prediction models. *Methods in Ecology and Evolution* 12(9):1620–1633. doi:10.1111/2041-210X.13650 | see verification log |
| C4 | Meyer H, Pebesma E (2022). Machine learning-based global maps of ecological variables and the challenge of assessing them. *Nature Communications* 13:2208. doi:10.1038/s41467-022-29838-9 | see verification log |
| C5 | Meyer H et al. (2018). Improving performance of spatio-temporal machine learning models using forward feature selection and target-oriented validation. *Environmental Modelling & Software* 101:1–9. doi:10.1016/j.envsoft.2017.12.001 | see verification log |
| C6 | Ludwig M et al. (2023). Assessing and improving the transferability of current global spatial prediction models. *Global Ecology and Biogeography* 32:356–368. doi:10.1111/geb.13635 | see verification log |
| C7 | Yates KL et al. (2018). Outstanding challenges in the transferability of ecological models. *Trends in Ecology & Evolution* 33(10):790–802. doi:10.1016/j.tree.2018.08.001 | see verification log |
| C8 | Valavi R et al. (2018). blockCV: an R package for generating spatially or environmentally separated folds. *Methods in Ecology and Evolution* 10:225–232. | see verification log |

## Block D — Dataset shift and domain adaptation

| # | Citation as supplied | Status |
|---|---|---|
| D1 | Moreno-Torres JG, Raeder T, Alaiz-Rodríguez R, Chawla NV, Herrera F (2012). A unifying view on dataset shift in classification. *Pattern Recognition* 45(2):521–530. doi:10.1016/j.patcog.2011.06.019 — **canonical covariate/concept shift definition** | see verification log |
| D2 | Sun B, Feng J, Saenko K (2016). Return of Frustratingly Easy Domain Adaptation. AAAI. — supplied as **NOT VERIFIED**, confirm | see verification log |

## Block E — Direct competitors / scooping risk

| # | Citation as supplied | Status |
|---|---|---|
| E1 | Generalizing Human-Driven Wildfire Ignition Models Across Mediterranean Regions (2026). *Geomatics* 6(1):13. doi:10.3390/geomatics6010013 — finds transfer AUC ≈ 0.85, **but predicts human-caused ignition; anthropogenic pressure dominates** | see verification log |
| E2 | WildfireGenome (2025). arXiv:2511.11589 — cross-county transfer heatmap for the United States | see verification log |

---

## Novelty argument as supplied (four claims)

**N1 — The transferability of pre-fire thermal state has never been tested.** Maffei et al. show a
relationship between LST anomalies and burned area, but state themselves that the effect is
"preconditioning in nature, does not predict actual fire occurrence". Their analysis is
decile-binned; there is no spatially validated predictive model and no transfer test.

**N2 — The one Mediterranean transfer study measures a different target.** Geomatics (2026)
predicts *human-caused ignition*, with night-time lights and human modification as dominant
predictors. Human infrastructure is spatially stationary, which is *why* it transfers. We measure
dynamic biophysical dryness, where physics is universal and transfer is therefore the *expected*
outcome — and it does not happen. That is the surprise.

**N3 — Nobody decomposes transfer failure into covariate versus concept shift.** Reviews flag it as
a gap but leave it a black box. We operationalise the Moreno-Torres taxonomy: the fraction recovered
by label-blind alignment is covariate, the residual is concept (≈1/3 and ≈2/3).

**N4 — Nobody has shown that geographic/climatic proximity fails to predict transfer.** Manavgat–Muğla
(same country, same year, 200 km) collapses; Bejís–Muğla (different country, different year, 2500 km)
works. This challenges both the implicit "similar bioclimate ⇒ transfer works" assumption of
Geomatics (2026) and the predictor-space-distance basis of the Meyer–Pebesma area-of-applicability
approach.

---

## Verification log

Independent verification performed 2026-07-23 against the **Crossref REST API**
(`api.crossref.org/works/{DOI}`), which returns publisher-deposited metadata, supplemented by dblp
and arXiv where no DOI exists. Every field below (authors, journal, volume, issue, pages, year)
was read from that response, not from memory.

### Result summary

**16 of 16 supplied entries confirmed to exist. No supplied DOI was invalid. Two entries needed
correction or completion; one has a year ambiguity.**

### Per-entry results

| # | Verdict | Notes |
|---|---|---|
| A1 | **VERIFIED** | Iban MC, Sekertekin A. *Ecological Informatics* **69**, 101647 (2022). All fields exact as supplied. Title confirms Adana and Mersin provinces — Kozan district lies in Adana, so this is indeed the same landscape as our negative control. |
| A2 | **VERIFIED + COMPLETED** | Authors were missing; they are **Hazan Alkan Akıncı and Halil Akıncı**. Full title: *"Machine learning based forest fire susceptibility assessment of Manavgat district (Antalya), Turkey"*. *Earth Science Informatics* **16**(1):397–414 (2023). This is the same district as our anchor AOI and is therefore the closest direct comparison in the literature. |
| A3 | **VERIFIED + COMPLETED** | Authors: **Muzaffer Can Iban and Oktay Aksu**. Full title: *"SHAP-Driven Explainable Artificial Intelligence Framework for Wildfire Susceptibility Mapping Using MODIS Active Fire Pixels: An In-Depth Interpretation of Contributing Factors in Izmir, Türkiye"*. *Remote Sensing* **16**(15):2842 (2024). Note: the target is **MODIS active-fire pixels**, not burned area — a relevant methodological difference from our MCD64A1 label. |
| A4 | **VERIFIED + COMPLETED (article number resolved 2026-08-08)** | Vibhandik P, Sawant S, Joshi A, Bidwe R. *"A systematic literature review on forest fire susceptibility mapping using geo-spatial technology and future research directions"*. *Discover Artificial Intelligence* **6**(1) (2026). Crossref reports article-number 00921; DOI 10.1007/s44163-026-00921-0 is unambiguous — cite by DOI. |
| A5 | **VERIFIED + COMPLETED** | Jodhani K, Bhatiya L, Sirvi L, Chanda A, Thakkar S, Rathnayake U. *"Artificial intelligence and remote sensing frameworks for wildfire monitoring and risk analysis across multiple ecosystems: a review"*. *AIMS Environmental Science* **13**(1):56–98 (2026). Volume and pages were not supplied; now complete. |
| B1 | **VERIFIED** | Sandholt I, Rasmussen K, Andersen J. *RSE* **79**(2–3):213–224 (2002). Exact as supplied. |
| B2 | **VERIFIED + CORRECTED** | Author list is **Maffei C, Alfieri SM, Menenti M** (the "et al." resolves to Silvia Maria Alfieri and Massimo Menenti — note *not* Lindenbergh, who is on the 2021 paper). *Remote Sensing* **10**(11):1777 (2018). |
| B3 | **VERIFIED + COMPLETED** | Maffei C, Lindenbergh R, Menenti M. *ISPRS Journal of Photogrammetry and Remote Sensing* **181**:400–412 (2021). doi:10.1016/j.isprsjprs.2021.09.016. Volume and pages now supplied. |
| B4 | **VERIFIED + COMPLETED** | Full author list: Chuvieco E, Cocero D, Riaño D, Martin P, Martínez-Vega J, de la Riva J, Pérez F. *RSE* **92**(3):322–331 (2004). Issue number added. |
| C1 | **VERIFIED + COMPLETED** | DOI was missing: **10.1111/ecog.02881**. *Ecography* **40**(8):913–929 (2017). Issue number added. |
| C2 | **VERIFIED + COMPLETED** | *Nature Communications* **11**(1), article **4540** (2020). Volume and article number were missing. |
| C3 | **VERIFIED** | Meyer H, Pebesma E. *MEE* **12**(9):1620–1633 (2021). Exact as supplied. |
| C4 | **VERIFIED** | Meyer H, Pebesma E. *Nature Communications* **13**(1), article 2208 (2022). Exact as supplied. |
| C5 | **VERIFIED** | Meyer H, Reudenbach C, Hengl T, Katurji M, Nauss T. *EMS* **101**:1–9 (2018). Exact as supplied. |
| C6 | **VERIFIED + COMPLETED** | Ludwig M, Moreno-Martinez A, Hölzel N, Pebesma E, Meyer H. *GEB* **32**(3):356–368 (2023). Issue added. |
| C7 | **VERIFIED** | Yates KL et al. *TREE* **33**(10):790–802 (2018). Exact as supplied. Author list is 40+ names; use "et al." after the first six per Elsevier style. |
| C8 | **VERIFIED, YEAR AMBIGUOUS** | Valavi R, Elith J, Lahoz-Monfort JJ, Guillera-Arroita G. *MEE* **10**(2):225–232, doi:10.1111/2041-210X.13107. Crossref's `published` date is **2018** (online-first); the print issue is **2019**. The community cites it as 2019. **Recommendation: cite as 2019** and keep the DOI, which is unambiguous. A 2018 bioRxiv preprint (doi:10.1101/357798) also exists — do not cite that one. |
| D1 | **VERIFIED + CORRECTED** | Moreno-Torres JG, Raeder T, Alaiz-Rodríguez R, Chawla NV, Herrera F. *Pattern Recognition* **45**(1):521–530 (2012). **The supplied issue number (2) is wrong; it is issue 1.** Pages and volume as supplied. |
| D2 | **VERIFIED + COMPLETED (2026-08-08)** | Sun B, Feng J, Saenko K. *"Return of Frustratingly Easy Domain Adaptation"*. Proceedings of the AAAI Conference on Artificial Intelligence **30**(1) (2016). **DOI 10.1609/aaai.v30i1.10306 now confirmed via the Crossref REST API** (the earlier note said it must not be guessed; it has now been verified, not guessed). Pages 2058–2065 per dblp (`conf/aaai/SunFS16`); Crossref carries the article number rather than pages — cite with the DOI, which is unambiguous. Added to `REFERENCES.bib`. |
| E1 | **VERIFIED + COMPLETED; FULL TEXT READ (YEC, 2026-08-08)** | Full title: *"Generalizing Human-Driven Wildfire Ignition Models Across Mediterranean Regions Using Harmonized Remote-Sensing and Machine-Learning Data"*. Authors: Dimarco NA, Faraji I, Wahbi M, Maatouk M, Boulaassal H, Yazidi Aalaoui O, El Kharki O. *Geomatics* **6**(1):13 (2026). Full-text details (per YEC's reading, now reflected in 02 §2.5): predictors = NDVI; slope (ASTER GDEM); ERA5-Land long-term seasonal means of T2M, WS10M, RH; global human modification; VIIRS night-time lights (+ log1p transform); population density — **no LST, no TVDI**. Target = MCD64A1 burn-pixel centroids as ignition proxy vs 1:1 balanced background. Validation = 80/20 hold-out; 5-fold spatial CV for hyperparameters. Transfer = LOCO + full 4×4 matrix; no domain adaptation. All transfers AUC > 0.80; bioclimatically similar country pairs higher; Morocco systematically lower, attributed to anthropogenic drivers, fire management and data reporting. **Caution: their Results text says "LST anomalies", contradicting their own Methods — Methods taken as authoritative (footnote in 02 §2.5).** |
| E2 | **VERIFIED + COMPLETED** | Liu C, Mostafavi A. *"WildfireGenome: Interpretable Machine Learning Reveals Local Drivers of Wildfire Risk and Their Cross-County Variation"*. arXiv:2511.11589 (2025), Texas A&M University. Preprint; no journal version confirmed. **Important**: the label is a PCA composite of seven federal wildfire *hazard indicators* at H3 level-8, **not observed burned area**, and the paper reports that transfer works between ecologically similar counties and collapses across dissimilar ones. See the novelty audit for why this matters to claim N4. |

### Additional references identified during verification (not in the supplied list)

All verified via Crossref unless noted.

| Ref | Why it is needed |
|---|---|
| Giglio L, Boschetti L, Roy DP, Humber ML, Justice CO (2018). The Collection 6 MODIS burned area mapping algorithm and product. *RSE* **217**:72–85. doi:10.1016/j.rse.2018.08.005 | **Mandatory** — this is our label product and it was uncited. |
| Boschetti L, Roy DP, Giglio L, Huang H, Zubkova M, Humber ML (2019). Global validation of the Collection 6 MODIS burned area product. *RSE* **235**:111490. doi:10.1016/j.rse.2019.111490 | Bounds achievable performance; supports the label-granularity limitation. |
| Zanaga D, Van De Kerchove R, Daems D, De Keersmaecker W, Brockmann C, Kirches G, Wevers J, Cartus O, Santoro M, Fritz S, Lesiv M, Herold M, Tsendbazar N-E, Xu P, Ramoino F, Arino O (2022). ESA WorldCover 10 m 2021 v200. Zenodo. doi:10.5281/zenodo.7254221 | **Mandatory** — land cover source and the basis of the natural-vegetation population. Verified via the ESA WorldCover documentation and the IIASA/WUR dataset records; it is a Zenodo dataset, not a journal article. |
| Malakar NK, Hulley GC, Hook SJ, Laraby K, Cook M, Schott JR (2018). An operational land surface temperature product for Landsat thermal data: methodology and validation. *IEEE TGRS* **56**(10):5717–5735. doi:10.1109/TGRS.2018.2824828 | **Mandatory** — the retrieval behind the Landsat Level-2 surface temperature band we composite. |
| Cook M, Schott JR, Mandel J, Raqueno N (2014). Development of an operational calibration methodology for the Landsat thermal data archive… *Remote Sensing* **6**(11):11244–11266. doi:10.3390/rs6111244 | Supporting reference for the same product lineage. |
| Breiman L (2001). Random forests. *Machine Learning* **45**(1):5–32. doi:10.1023/A:1010933404324 | Classifier reference. |
| Yebra M, Dennison PE, Chuvieco E, Riaño D, Zylstra P, Hunt ER Jr, Danson FM, Qi Y, Jurdao S (2013). A global review of remote sensing of live fuel moisture content for fire danger assessment. *RSE* **136**:455–468. doi:10.1016/j.rse.2013.05.029 | The mechanistic link between thermal dryness and fire; the strongest justification for our feature block. |
| Archibald S, Lehmann CER, Gómez-Dans JL, Bradstock RA (2013). Defining pyromes and global syndromes of fire regimes. *PNAS* **110**(16):6442–6447. doi:10.1073/pnas.1211466110 | **Recommended new block** — fire-regime typology, the natural framing for "why do two Mediterranean regions behave as different concepts?" |
| Pausas JG, Keeley JE (2021). Wildfires and global change. *Frontiers in Ecology and the Environment* **19**(7):387–395. doi:10.1002/fee.2359 | Mediterranean fire-regime context for the Introduction. |
| Tuia D, Persello C, Bruzzone L (2016). Domain adaptation for the classification of remote sensing data: an overview of recent advances. *IEEE Geoscience and Remote Sensing Magazine* **4**(2):41–57. doi:10.1109/MGRS.2016.2548504 | Domain adaptation in remote sensing — the survey that frames our adaptation block. |
| Persello C, Bruzzone L (2012). Active learning for domain adaptation in the supervised classification of remote sensing images. *IEEE TGRS* **50**(11):4468–4483. doi:10.1109/TGRS.2012.2192740 | Supports the few-shot / active-learning future-work argument with an actual remote-sensing precedent. |
| Maffei C, Menenti M (2019). Predicting forest fires burned area and rate of spread from pre-fire multispectral satellite measurements. *ISPRS J. Photogramm. Remote Sens.* **158**:263–278. doi:10.1016/j.isprsjprs.2019.10.013 | Found during verification; completes the Maffei pre-fire-prediction series and is directly on our topic. |

### Consolidated open verification items (swept 2026-08-08 — the single list)

Everything still open after the 2026-08-08 sweep. Resolved-this-sweep items are recorded at the
end for the audit trail.

STILL OPEN:
1. **E2 (WildfireGenome)** — arXiv preprint only; re-check for a peer-reviewed version before
   submission. *Deferred by decision to the pre-submission pass; stays on the list.*

CLOSED 2026-08-08 (second round — decisions, not new evidence):
2. **Copernicus DEM GLO-30** — **CLOSED, no bib entry.** The candidate DataCite DOI
   `10.5270/ESA-c5d3d65` returns HTTP 404 and is not used. First, which DEM actually ran was
   verified rather than assumed: `repo/src/step2b_dem.py` *prefers* GLO-30 and falls back to
   SRTMGL1 only on exception, so the source could not be read off the code alone. The frozen
   `drive_new/kozan-legacy/step2b/step2b_dem_metadata.json` records
   `"dataset": "COPERNICUS/DEM/GLO30"`, `"used_fallback": false`, `"preferred_error": null` —
   GLO-30 ran, the fallback was never exercised. Decision: cite the official ESA Copernicus Data
   Space product page inline in Methods §3.4 with an access date and no DOI; do **not** cite
   Farr et al. 2007, since SRTM contributed nothing to the reported numbers.
3. **Bejís 2022 event description** — **CLOSED, uncited.** Crossref returned no record for the
   event; a follow-up search for an EFFIS or Generalitat Valenciana report on the individual fire
   found only press coverage and EU-wide season summaries (the JRC 2022 season report covers
   Spain in aggregate, not Bejís). Decision: force nothing. The manuscript carries no narrative
   description of the event; extent, dates and prevalence are reported from MCD64A1.
4. **Muğla 2021 event description** — **CLOSED, reference removed.** `Cosandal2022` deleted from
   `REFERENCES.bib`; it was a tourism-impact study, was never cited in the body text, and is a
   poor fit for an event description. The event is described from MCD64A1 without a citation.
5. **Huang et al. [@Huang2026]** — **CLOSED, abstract sufficient.** The manuscript quotes no
   effect coefficient and no numerical result from this paper. §2.4 cites it only for the
   existence and direction of the decomposition ("concept shift dominant"), which the abstract
   supports; an explicit sentence to that effect now stands in §2.4 in place of the marker. Full
   text is not required. If any Huang number is ever added, this item reopens.

RESOLVED IN THIS SWEEP (2026-08-08, all via Crossref/arXiv API):
- **A4 article number** — Crossref reports article-number 00921; DOI 10.1007/s44163-026-00921-0
  is unambiguous; cite by DOI. Bib comment updated.
- **D2 (Sun et al. 2016)** — DOI 10.1609/aaai.v30i1.10306 confirmed; added to bib.
- **Deep CORAL (Sun & Saenko 2016)** — *Computer Vision – ECCV 2016 Workshops*, LNCS,
  pp 443–450, doi:10.1007/978-3-319-49409-8_35 — volume/pages now verified.
- **arXiv:2103.05898** — Burns C, Steinhardt J, *"Limitations of Post-Hoc Feature Alignment for
  Robustness"*; arXiv listing states accepted to CVPR 2021. Authors/venue verified.
- **Manavgat 2021 event description** — Soydan O (2022), *TURJAF* 10(sp2):3029–3035,
  doi:10.24925/turjaf.v10isp2.3029-3035.5764; metadata verified, full text unread; `Soydan2022`.
- **North Evia 2021 event description** — Varela V et al. (2022), *Advances in Forest Fire
  Research 2022*, pp 666–672, doi:10.14195/978-989-26-2298-9_101; metadata verified, full text
  unread; `Varela2022`.
- **Dimarco et al. (E1)** — full text read by YEC; details in the E1 row above and in 02 §2.5.

---

## Novelty audit (adversarial): attempt to refute the four claims

An independent search was run with the explicit goal of **finding prior work that scoops each
claim**. Every citation below was re-verified against Crossref by the author of this file, not
taken on trust from the search. **Headline: the specific combination — pre-fire thermal/dryness →
burned-area classification, spatially blocked, transferred across regions with label-blind
adaptation and a covariate/concept decomposition — was not found in the literature. The core
contribution stands. But three of the four claims are overstated as worded and must be rewritten.**

### N1 — "the transferability of pre-fire thermal state has never been tested"

**Verdict: SURVIVES in substance, but the word "never" is indefensible.**

The Maffei line is larger than the two papers we had: besides Maffei et al. (2018) and Maffei et
al. (2021), there is **Maffei & Menenti (2019)**, *ISPRS J.* **158**:263–278 — pre-fire
multispectral prediction of burned area and rate of spread — and a **2026 book chapter**
consolidating the group's probabilistic fire-danger work (in *Satellite Remote Sensing for Forest
and Environmental Monitoring*, pp. 285–327, doi:10.1016/B978-0-443-40296-8.00010-0). The 2021
paper is the stronger threat than the 2018 one, because it benchmarks pre-fire LST anomaly against
the FWI. All of it is single-region, without spatial cross-validation and without any transfer test.

The real problem for the absolute wording is **Gelabert PJ, Jiménez-Ruano A, Ochoa C, Alcasena F,
Sjöström J, Marrs C, Ribeiro LM, Palaiologou P, Bentu Martínez C, Chuvieco E, Vega-García C,
Rodrigues M (2025). Assessing human-caused wildfire ignition likelihood across Europe. *Natural
Hazards and Earth System Sciences* 25:4713–4729. doi:10.5194/nhess-25-4713-2025** — verified. Their
most influential predictor is **dead fine fuel moisture content and its yearly anomalies**, a
dynamic dryness-anomaly variable structurally analogous to our LST anomaly, and they *do* test
spatial generalisation: a pooled model over five European pilot sites evaluated per site, with an
AUC drop of about 0.10 in Southern Sweden and Attica. It is a pooled-fit/local-evaluation design
rather than strict train-A/test-B, the target is human-caused ignition rather than burned area, and
there is no adaptation and no shift decomposition — but a dryness-anomaly-dominated model *is*
being generalised across European regions.

Also adjacent: **Marino E, Yáñez L, Guijarro M, Madrigal J, Senra F, Rodríguez S, Tomé JL (2024).
Transferability of empirical models derived from satellite imagery for live fuel moisture content
estimation and fire risk prediction. *Fire* 7(8):276. doi:10.3390/fire7080276** — verified. It
transfers a *moisture-retrieval* model to an uncalibrated region, not a burned/unburned classifier,
but a reviewer will raise it.

**Action:** reword to *"no study has tested whether the predictive skill of pre-fire thermal/dryness
state transfers between fire regions under label-free adaptation."* Never write "never been tested."

### N2 — "the only Mediterranean transfer study is Geomatics 2026, and it is purely anthropogenic"

**Verdict: WEAKENED. Both halves are wrong as written.**

Dimarco et al. (2026) is **not anthropogenic-only by design**. Its own abstract frames the study as
comparing "the relative influence of **anthropogenic and biophysical** drivers", using harmonised
500 m predictors "integrating **vegetation condition, topography, climatic context**, and human
pressure". Anthropogenic dominance is their *result*, not their predictor design. Setting them up
as an anthropogenic straw man would be a factual error a reviewer would catch immediately.

It is also not the only Mediterranean cross-region study: Gelabert et al. (2025) covers Attica and
other Mediterranean pilot sites with a cross-site generalisation test.

Their transfer result is the **opposite** of ours (within-region AUC > 0.90, mean transfer AUC
≈ 0.85). That contrast is our strongest framing device — a stable anthropogenic gradient transfers,
dynamic biophysical dryness does not — but it must be presented as a contrast with a
*biophysically-inclusive* study.

#### `[RESOLVED 2026-07-23]` Dimarco et al. (2026) full text read by the author

The blocking item is closed. The full text was obtained and read manually (MDPI continues to refuse
automated retrieval). Verified contents:

**Predictor set (their Section 2.3 and correlation analysis), complete:** NDVI; slope (ASTER GDEM);
T2M, WS10M and RH (all ERA5-Land, **long-term seasonal means**); gHM (global human modification);
VIIRS night-time lights, plus a log1p transform of it; population density.

**There is no LST and no TVDI in their predictor set.** Their only temperature variable is a
*static reanalysis climatology*, not a satellite-observed thermal anomaly. This is the decisive
detail for our framing.

> **Discrepancy to handle carefully.** Their Results sections refer to "LST anomalies", which
> contradicts their own Methods. We treat the Methods as authoritative, and we should say so
> explicitly in a footnote rather than silently choosing one reading — a reviewer who has read only
> their Results will otherwise think we have misdescribed them.

**Target definition:** MCD64A1 burned-pixel centroids treated as an **ignition proxy**, matched
against a **1:1 balanced background** sample. (Ours is burned-area classification at the true, very
imbalanced base rate — a materially different problem.)

**Validation:** 80/20 split, with 5-fold spatial cross-validation used for hyperparameter selection.

**Transfer design:** leave-one-country-out **plus a full 4 × 4 transfer matrix** (their Table 10).
**No domain adaptation of any kind.**

**Findings:** all transfers exceed AUC 0.80; transfers between bioclimatically similar countries are
higher; transfers to Morocco are systematically lower — and they attribute that drop **not to
climate alone** but to differences in anthropogenic drivers, fire management and data reporting.

**Consequences for our claims.**

- **N2 must be reframed as an empirical contrast, not as a criticism of their predictor design.**
  The correct statement: within the same Mediterranean cross-region transfer setup, static
  anthropogenic and topographic predictors transfer above AUC 0.80, while dynamic pre-fire thermal
  state collapses below chance. The proposed mechanism is that human infrastructure and terrain are
  spatially stationary, whereas the thermal-dryness–fire relationship is locally reparameterised.
- **Their study is 4 regions and 12 ordered pairs — the same n as ours.** This removes the "your n
  is too small" objection *as a matter of design*: n = 12 is evidently not disqualifying, since the
  strongest opposing result rests on exactly that many pairs. Our claim still needs more careful
  wording, but only because it runs in the opposite direction, not because our design is weaker.
- **Their Morocco finding actively supports our N4 reframing.** In their own data, bioclimatic
  similarity does not fully account for transfer performance; non-climatic factors are needed. That
  is our argument, arrived at from their side.

### N3 — "nobody decomposes fire-model transfer failure into covariate vs concept shift"

**Verdict: the wildfire-specific and instrument-specific claim SURVIVES; the general
"in environmental remote sensing" claim is REFUTED.**

The refutation, verified: **Huang Y, Liu N, Chen W, Tan W, Deng Y, Wang Z, Chlus A, Shen J,
Townsend PA (2026). Enhancing transferability of foliar trait retrieval models: a comparative
analysis of transfer learning strategies and domain shift characterization. *Remote Sensing of
Environment* 337:115336. doi:10.1016/j.rse.2026.115336.** They quantitatively decompose domain
shift into components across four transfer scenarios and report concept shift as the primary factor
limiting transferability. This is hyperspectral *regression* of foliar traits, not fire, and —
importantly — they measure shift components with statistical shift metrics and a regression on the
transferability gap, **not** by using label-free adaptation performance as the measuring instrument.
Our instrument (`recovered = adapted − raw`, `residual = within − adapted`) appears to remain ours.
`[TO VERIFY: the reported effect coefficients — read the paper before quoting any number from it.]`

**Action:** cite Huang et al. explicitly and narrow the claim to wildfire + the adaptation-as-
instrument formulation.

No application of CORAL or region-wise feature alignment to fire susceptibility, fire occurrence or
burned-area *prediction* was found. Everything under "domain adaptation + fire" is image-level
post-fire mapping or smoke detection, which does not touch our problem. That part of N3 is solid.

### N4 — "nobody has shown that proximity fails to predict transferability"

**Verdict: SURVIVES within the fire literature, but this is the weakest claim, and the risk is not
being scooped — it is being contradicted.**

Outside fire, the finding is already published, and these are conceptual precedents we must cite
rather than novelty we can claim: **Vesk PA, Morris WK, Neal WC, Mokany K, Pollock LJ (2021).
Transferability of trait-based species distribution models. *Ecography* 44(1):134–147.
doi:10.1111/ecog.05179** (online 2020, issue 2021) reports that prediction in target regions did
*not* worsen with increasing geographic, environmental or compositional distance; **Rousseau JS,
Betts MG (2022). Factors influencing transferability in species distribution models. *Ecography*
2022(7):e06060. doi:10.1111/ecog.06060** reports environmental similarity was *not* a significant
predictor of transferability. Meyer & Pebesma (2021) and Ludwig et al. (2023) already argue that
*feature-space* dissimilarity rather than geographic distance governs applicability.

Within fire, the two multi-region transfer studies both report that similarity **does** predict
transfer — i.e. they contradict us. WildfireGenome reports ecologically similar county pairs
transferring well and dissimilar pairs collapsing below chance across seven US counties (42 ordered
pairs); Dimarco et al. report higher transfer between bioclimatically similar countries.

**Revised position after reading Dimarco et al. (2026) in full — the claim is now narrowed
logically rather than demoted evidentially.**

The original wording, "similarity does not predict transferability", is a claim about a *correlation
across pairs*, and at 12 ordered pairs it is indeed weakly supported. But that is not the claim we
need. The defensible claim is about **sufficiency**:

> Geographic and bioclimatic similarity are **not sufficient** for transfer.

A sufficiency claim is refuted by a **single** strong counterexample and therefore requires no n at
all. Manavgat→Muğla is that counterexample: same country, same fire year, ~200 km apart, comparable
bioclimate — about as similar as two independent fire regions can be — and transfer collapses.
Nothing about the sample size weakens a counterexample.

Two supporting notes:

- **The "n is too small" objection does not survive contact with the comparison.** Dimarco et al.
  also use 4 regions and a 4 × 4 matrix, i.e. the same 12 ordered pairs. Our claim is formulated
  more cautiously than theirs not because our design is weaker but because ours runs against the
  prevailing expectation, and a claim that contradicts the field should carry the heavier burden.
- **Their own Morocco result supports us.** They attribute the systematically lower transfer to
  Morocco to anthropogenic drivers, fire management and data-reporting differences rather than to
  climate alone — i.e. in their data too, bioclimatic similarity is not the whole story.

**Positioning:** present this as a live disagreement rather than a settled result. Vesk et al.
(2021) and Rousseau & Betts (2022) align with our direction; Dimarco et al. (2026) and WildfireGenome
(2025) run against it. The honest reading is that the relationship between domain similarity and
transfer success is *predictor-class dependent* — stationary predictors track similarity, dynamic
ones need not — which is a hypothesis our data support and cannot prove.

### Additional defensive citations (verified; do not scoop us, will be asked for)

- **Podschwit H, Jolly W, Alvarado E, Verma S, Ponce B, Markos A, Aliaga-Nestares V,
  Rodriguez-Zimmermann D (2022).** Reliability of cross-regional applications of global fire danger
  models: a Peruvian case study. *Fire Ecology* **18**(1):25. doi:10.1186/s42408-022-00150-7 — the
  classic "fire danger indices do not port" reference.
- **Kondylatos S, Prapas I, Camps-Valls G, Papoutsis I (2023).** Mesogeos: a multi-purpose dataset
  for data-driven wildfire modeling in the Mediterranean. *Advances in Neural Information
  Processing Systems* **36**:50661–50676 — a 1 km Mediterranean datacube. Expect the reviewer
  question "why did you not use this?"; it is also the natural vehicle for scaling our transfer
  experiment.
- **Xu Y, Dai Y, Chang L, Wang Q, Dong Y (2026).** Does your wildfire prediction model actually
  work, or just score well? arXiv:2605.18911 (v1 14 May 2026; v2 21 May 2026) — argues wildfire
  transfer conclusions depend strongly on evaluation design and task formulation. Could be used
  against our decomposition; pre-empt it.
- **arXiv:2103.05898** — VERIFIED 2026-08-08: Burns C, Steinhardt J, *"Limitations of Post-Hoc
  Feature Alignment for Robustness"*; arXiv listing states accepted to CVPR 2021. Supports our
  negative result that post-hoc alignment cannot close a conditional-distribution gap. If cited,
  fetch the IEEE CVPR DOI at that point (not yet retrieved).
- **Sun B, Saenko K (2016).** Deep CORAL — VERIFIED 2026-08-08: *Computer Vision – ECCV 2016
  Workshops*, LNCS, pp 443–450, doi:10.1007/978-3-319-49409-8_35.

### Blocking action items

1. ~~Manually read the Dimarco et al. (2026) predictor table.~~ **`[CLOSED 2026-07-23]`** — full
   text read; findings recorded under N2 above. No LST, no TVDI; temperature is ERA5-Land static
   seasonal climatology. N2 reframed as an empirical contrast.
2. ~~Read Huang et al. (2026, *RSE* 337:115336) before citing any of its numbers.~~
   **`[CLOSED 2026-08-08]`** — closed by decision, not by reading. The manuscript quotes no number
   from it; §2.4 now states explicitly that no effect coefficient is quoted and that the citation
   supports only the existence and direction of the decomposition, both of which the abstract
   carries. Reopens only if a Huang number is added.
3. ~~Decide whether N4 remains a contribution claim.~~ **`[CLOSED 2026-07-23]`** — resolved by
   logical narrowing rather than by a new test: the claim is now about **sufficiency**, refuted by
   the single Manavgat→Muğla counterexample, so no cross-pair correlation test is required. A
   distance-versus-transfer correlation may still be reported as supporting description, but the
   claim no longer rests on it.
4. `[NEW — footnote required]` Dimarco et al.'s Results text mentions "LST anomalies" while their
   Methods lists no LST. We rely on their Methods and must say so in a footnote, so that a reviewer
   reading only their Results does not conclude we misdescribed their predictor set.
