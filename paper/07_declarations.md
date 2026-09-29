# Statements and Declarations

## Funding

This work was supported by the Çukurova University Scientific Research Projects Coordination Unit
(Bilimsel Araştırma Projeleri Koordinasyon Birimi) under its Career Starter Project scheme, project
code FKB-2025-17608 ("Early detection and prevention of forest fires with a thermal digital
twin-based UAV swarm system"). The funder had no role in the study design, the analysis, the
interpretation of the results, the writing of the manuscript or the decision to submit it.

## Competing interests

The authors have no relevant financial or non-financial interests to disclose.

## Author contributions

Stated in CRediT terms. **Emrehan Metin:** Software, Data curation, Investigation, Validation,
Writing (review and editing). **Yunus Emre Cogurcu:** Conceptualization, Methodology, Formal
analysis, Investigation, Visualization, Writing (original draft), Writing (review and editing),
Supervision, Project administration, Funding acquisition. Both authors read and approved the final
manuscript.

## Data availability

All satellite inputs are public and were retrieved through Google Earth Engine. Burned-area labels were taken
from MODIS MCD64A1 v061 [@MCD64A1], land surface temperature from MODIS MOD11A1 v061 [@MOD11A1],
surface reflectance and surface temperature from Landsat 8 Collection 2 Level-2 [@LandsatC2L2],
terrain from the Copernicus DEM GLO-30 [@CopernicusDEM] and land cover from ESA WorldCover v200
[@Zanaga2022]. The MODIS and Landsat products are courtesy of NASA's Land Processes Distributed Active
Archive Center and the U.S. Geological Survey. WorldCover is distributed under a CC BY 4.0 licence
(© ESA WorldCover project 2021, contains modified Copernicus Sentinel data (2021) processed by the
ESA WorldCover consortium). The Copernicus DEM was produced using Copernicus WorldDEM-30 © DLR e.V.
2010 to 2014 and © Airbus Defence and Space GmbH 2014 to 2018, provided under COPERNICUS by the European
Union and ESA; all rights reserved. No proprietary or restricted data were used.

The five modelling datasets, one per region, and the frozen numeric outputs behind every reported
number are released with the analysis code [@ThermalTwinRepo]. Each dataset is identified by SHA-256
in `paper/code/_canonical.py`, and every analysis script verifies that hash on load. For Bejís, Muğla,
North Evia and Montiferru the hash equals the canonical-input record of the upstream pipeline at
commit `6381f4c`. For Manavgat it is the corrected-label re-freeze (`5a5e876c…`), produced at the same
commit. The two small changes needed for this are given in Section S3.6.2. The pipeline's own
record still names the original-label table (`054a1961…`), which is not used here.

## Code availability

The upstream processing pipeline, `satellite-thermal-digital-twin` (E. Metin), is public at
<https://github.com/emrehann17/satellite-thermal-digital-twin> under the MIT licence. The analysis
code, figure scripts and checks are at <https://github.com/dryuemco/thermal-twin>. Figs. 1 to 8 are drawn
by the scripts in `paper/figures/`, which also assert Table 1 and every plotted value against the
frozen outputs. The supplementary tables S2 to S7 and S9 to S18 are rebuilt row by row by
`paper/code/appendix_tables.py` from source files whose SHA-256 values are pinned in
`paper/labelfix_rerun/round5/tables/SOURCES.sha256`; the other tables name their source files in
their captions. `paper/figures/check_all.py` runs all of these checks. Software: Python 3.12.10 with
NumPy 2.4.4, pandas 3.0.2 and scikit-learn 1.9.0. Point estimates depend on the scikit-learn version
(Section 3.13), so exact reproduction needs this environment.

## Ethics approval

Not applicable. This study involved no human participants, animal subjects or personally
identifiable data.

## Use of generative AI

Claude (Anthropic) was used in the research and in preparing this manuscript, as described in
Section 3.13: to write and run analysis, verification and figure code, to check reported numbers
against the frozen outputs, to run simulated internal reviews, and to draft and edit text. The
authors reviewed and edited all of this material and take full responsibility for the content of the
publication.
