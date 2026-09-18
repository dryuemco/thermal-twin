# Manuscript outline — pre-fire thermal dryness and its cross-region transferability

**Target journal:** *Environmental Modelling & Software* (Elsevier, hybrid, JCR Q1), retargeted 2026-09-19 from *Ecological Informatics* to avoid an APC; see `JOURNAL_OPTIONS.md`
**Language:** English
**Status of this outline:** drafting stage. Results are **not** closed. Three regions complete
(Manavgat 2021, Bejís 2022, Muğla 2021), a fourth (North Evia 2021) partially processed with
diagnostics pending. **Results and Discussion are deliberately not written yet.**

---

## 0. Working title (candidates, to be fixed after results close)

- *Pre-fire thermal dryness improves burned-area discrimination within regions but does not
  transfer between them: a four-region Mediterranean test with label-blind domain adaptation*
- *Concept shift, not covariate shift, limits the transferability of satellite thermal fire
  susceptibility models*
- *When does a fire susceptibility model travel? Geographic and climatic proximity do not predict
  cross-region transfer*

Selection criterion: the title must carry the **negative/limiting** result, not only the positive
within-region one, since the transferability failure is the scientifically novel part.

---

## 1. Fixed core findings (the claims the paper is built on)

These are stable across the analysis and do not depend on the pending diagnostics. They are stated
here so every section can be written against them; the **numbers** attached to them stay out of the
Introduction and appear only in Results.

1. **Within-region, pre-fire thermal/dryness state adds a robust increment over a static
   topography-plus-fuel baseline.** Replicated in three regions, and the improvement survives
   progressively coarser spatial cross-validation up to ~10 km blocks.
2. **Cross-region transfer is heterogeneous and unreliable.** Naive transfer is frequently at or
   below chance.
3. **Label-blind domain adaptation closes only a minority of the transfer gap.** Region-wise
   z-scoring and CORAL recover roughly a quarter to a third of the deficit; the remaining ~69–73%
   behaves as concept shift.
4. **Geographic and bioclimatic similarity are not *sufficient* for transfer.** Manavgat→Muğla
   (same country, same fire year, ~200 km apart, comparable bioclimate) fails, while Bejís→Muğla
   (different country, different year, ~2500 km apart) works.
   **Status: reframed, not demoted** (`LITERATURE.md`, N4). The claim is now about *sufficiency*
   rather than about correlation across pairs, so it is refuted-by-counterexample and needs no
   sample of pairs to stand. The earlier "n = 12 is too small" worry also turned out to be
   misplaced: Dimarco et al. (2026), the strongest opposing result, uses four regions and a 4 × 4
   matrix — exactly the same twelve ordered pairs. Our wording is more cautious than theirs only
   because our claim runs against the prevailing expectation.
   Supporting note: Dimarco et al. attribute their own weakest transfer (to Morocco) to
   anthropogenic drivers, fire management and data reporting rather than to climate — bioclimatic
   similarity does not account for transfer performance in their data either.

5. **The empirical contrast with Dimarco et al. (2026).** Same design skeleton — four Mediterranean
   regions, twelve ordered pairs, 500 m cells, MCD64A1-derived target, tree ensembles, spatially
   aware validation — but their predictors are spatially stationary attributes of a place (slope,
   human modification, night-time lights, population density, ERA5-Land seasonal climatologies) and
   transfer everywhere above AUC 0.80, while ours describe the dynamic pre-fire state and collapse
   below chance. **This is the sharpest framing device the paper has** and belongs in the abstract.
   Bounding differences to state honestly: ignition proxy at a 1:1 balanced base rate versus
   burned-area classification at the true base rate; static reanalysis climatology versus
   event-specific satellite thermal observation; no adaptation versus label-blind adaptation.

Findings 1–3 carry the paper; findings 4–5 give it its argument. The load-bearing claim for the
abstract is the contrast in finding 5, supported by the sufficiency claim in finding 4 —
**transferability is predictor-class dependent, and must be measured rather than assumed from
regional similarity.**

---

## 2. Section plan

| § | Section | Status | Blocking dependency |
|---|---------|--------|---------------------|
| — | Abstract | **wait** | needs the final numbers for findings 1–4 |
| — | Highlights (Elsevier, 3–5 bullets, ≤85 chars each) | **wait** | same |
| — | Graphical abstract | **wait** | Fig. 8 + Fig. 4 composite (numbering per figure_captions.tex) |
| 1 | Introduction | **writable now** (`01_introduction.md`) | contribution claims left as placeholders |
| 2 | Related work / background | **writable now** (`02_related_work.md`) | citation gaps flagged inline |
| 3 | Materials and methods | **writable now** (`03_methods.md`) | region-specific windows verified from code; sample counts for Muğla/Evia pending |
| 4 | Results | **DO NOT WRITE** | Muğla transfer matrix + Evia completion + pending diagnostics |
| 5 | Discussion | **DO NOT WRITE** | depends on §4 |
| 6 | Limitations and threats to validity | partially writable | the pre-registered limitation list exists; region-count-dependent wording pending |
| 7 | Conclusions | **DO NOT WRITE** | depends on §4–5 |
| — | Data and code availability | writable near submission | repository DOI, archived environment |
| — | CRediT author contributions | writable near submission | — |
| — | Appendix / Supplementary | skeleton now | see §4 below |

---

## 3. Detailed section skeleton

### 1. Introduction (`01_introduction.md`)
1.1 Fire susceptibility models are widely produced, rarely tested outside the region that trained
them.
1.2 Most operational and published maps are built from *static* predictors (terrain, fuel type,
long-term climate) plus incident history; the *dynamic* pre-fire surface state is
under-exploited despite being what physically changes between a fire year and a non-fire year.
1.3 Satellite land surface temperature and thermal-optical dryness indices offer a route to that
dynamic state at moderate resolution and with global, free coverage.
1.4 Gap statement: (a) does dynamic pre-fire thermal state add measurable skill over a static
baseline, once spatial autocorrelation is properly controlled; (b) does whatever skill it adds
*travel* to a new region; (c) if not, is the failure covariate shift (fixable without labels)
or concept shift (not fixable without labels).
1.5 Contributions — left as explicit placeholders `[CONTRIBUTION CLAIM — pending results]`.

### 2. Related work (`02_related_work.md`)
- (a) Fire susceptibility mapping and machine learning, including Mediterranean and Türkiye-specific
  work.
- (b) Thermal dryness indicators: LST, LST anomalies, TVDI, and the fuel-moisture literature they
  proxy.
- (c) Spatial transferability, dataset/domain shift, spatial cross-validation, and unsupervised
  domain adaptation.
- Closing paragraph positions this study at the intersection: (b) evaluated under (c)'s standards
  inside (a)'s application domain.

### 3. Materials and methods (`03_methods.md`) — most detailed section, read from code
3.1 Study areas and pre-fire / label windows
3.2 Burned-area label: MCD64A1 and the reconstructed ~500 m native grid
3.3 Burned-landcover gate (region admissibility, negative control)
3.4 Predictors: Landsat LST and NDVI, TVDI, DEM, MODIS→Landsat downscaling and fusion, land cover
3.5 Cell-level aggregation, validity mask, and the natural-vegetation population
3.6 Feature sets: baseline vs thermal
3.7 Classifier and preprocessing
3.8 Spatial-block cross-validation and block-size robustness
3.9 Spatial-block bootstrap uncertainty
3.10 Cross-region transfer protocol
3.11 Label-blind domain adaptation (region-wise z-score, CORAL)
3.12 Transfer-gap decomposition and the concept-shift diagnostic
3.13 Leakage control and reproducibility

### 4. Results (**not written**)
Planned subsections, so the figure/table budget can be reserved now:
4.1 Within-region baseline vs thermal, per region
4.2 Block-size robustness (1 / 5 / 10 km)
4.3 Cross-region transfer matrix, all ordered pairs, raw
4.4 Effect of label-blind adaptation on the same matrix
4.5 Decomposition into recovered (covariate) and residual (concept) fractions
4.6 Concept-shift mechanism: signed univariate AUC reversals
4.7 Proximity is not predictive of transfer (the Manavgat/Muğla vs Bejís/Muğla contrast)
4.8 Sensitivity analyses (population, RF profile, CORAL λ)

### 5. Discussion (**not written**)
Planned argument order: why within-region skill is real but local; why concept shift is the
expected outcome for a physically ambiguous predictor such as absolute LST; what this implies for
"global" fire susceptibility products; what would actually be needed (few-shot recalibration,
physically normalised rather than statistically normalised predictors); the self-calibrating
digital-twin framing as future work rather than as an achieved result.

### 6. Limitations
Pre-existing, pre-registered list to be carried over and updated for region count: single fire
event per region confounds regional concept with event meteorology; MCD64A1 cell-level label
granularity; mild optimism of fine-block AUCs; scikit-learn version drift between pipeline stages;
AOI rectangles are place-based, not fire perimeters.

---

## 4. Figure and table budget

**Figures** (Elsevier allows generous supplementary; keep ≤7 in the main text)

| Fig. | Content | Section | Status |
|------|---------|---------|--------|
| 1 | Study-area map: four AOIs on a Mediterranean basemap, with fire year, pre-fire window and burned fraction annotated | §3.1 | can be produced now |
| 2 | Methods schematic: acquisition → 500 m aggregation → gate → feature sets → spatial-block CV → transfer/adaptation | §3 | can be produced now |
| 3 | Within-region baseline vs thermal ROC-AUC and ΔAUC with spatial-block bootstrap CIs, per region | §4.1 | waits |
| 4 | Block-size robustness: ΔAUC vs block size (1/5/10 km) per region | §4.2 | waits |
| 5 | Transfer matrix heatmaps: raw, z-score, CORAL (source × target), with 0.5 marked | §4.3–4.4 | waits |
| 6 | Decomposition bars: within / raw / adapted, split into recovered vs concept fractions | §4.5 | waits |
| 7 | Signed univariate AUC per feature per region, with spatial-block CIs; reversals highlighted | §4.6 | waits |
| S1+ | Sensitivity panels (population contrast, RF profile, CORAL λ sweep), PR-AUC versions of Figs. 3–5 | Suppl. | waits |

**Tables**

| Tab. | Content | Section | Status |
|------|---------|---------|--------|
| 1 | Study areas: region, country, fire year, AOI bbox, predictor window, label window, baseline years, cells, burned cells, prevalence | §3.1 | partially ready (Muğla/Evia counts `[TO VERIFY]`) |
| 2 | Feature dictionary: variable, source product, upstream processing step, unit, temporal window, feature set membership | §3.4/3.6 | ready |
| 3 | Within-region results, per region × block size | §4.1–4.2 | waits |
| 4 | Full transfer matrix with 95% CIs for the three variants | §4.3–4.4 | waits |
| 5 | Transfer-gap decomposition per ordered pair | §4.5 | waits |
| 6 | Reversing features with per-region signed AUC and CIs | §4.6 | waits |
| S1 | Complete hyperparameter, seed and threshold inventory | Suppl. | ready |
| S2 | Leakage-excluded column list | Suppl. | ready |

---

## 5. What is missing before Results can be written

1. **Muğla 2021** — cross-region transfer runs against Manavgat and Bejís in both directions, all
   three adaptation variants, with spatial-block bootstrap CIs. The local working copy currently
   contains an **empty** `experiments/mugla_2021/` directory, so all Muğla numbers must come from
   the run environment and be re-verified before they enter the manuscript.
2. **North Evia 2021** — completion of the Step1–Step8a chain, burned-landcover gate verdict, and
   entry into the transfer matrix. Until then the paper is a three-region study with a fourth
   region reported as in progress, or Evia is dropped entirely — this decision is not yet made and
   affects the abstract, Fig. 1 and Table 1.
3. **Pending diagnostics** — the outstanding checks on the new regions (grid alignment, gate
   verdicts, reproduction against the frozen two-region results).
4. **Decision on the negative control** — whether Kozan 2023 appears as a validity check or is
   omitted from the manuscript.
5. **Recomputation of every two-region number** with the final region set, so that no figure mixes
   a two-region and a four-region analysis.

---

## 6. Honesty constraints carried into every section

- No result number appears in the Introduction; contribution claims stay as placeholders until §4
  is final.
- No citation is invented. Every unverified attribution is marked `[CITATION NEEDED: topic]`.
- Every number whose provenance was not confirmed against an actual output file is marked
  `[TO VERIFY]`.
- The transferability failure is reported as a **primary finding**, not as a limitation buried in
  §6.
- The "self-calibrating thermal digital twin" framing is presented as the motivating long-term
  goal and as future work, never as something this paper demonstrates.
