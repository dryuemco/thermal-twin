# Author statements

## Data availability

All satellite inputs are public and were retrieved through Google Earth Engine. Burned-area labels were taken from MODIS MCD64A1 v061 [@MCD64A1], land surface temperature from MODIS MOD11A1 v061 [@MOD11A1], surface reflectance and surface temperature from Landsat 8 Collection 2 Level-2 [@LandsatC2L2], terrain from the Copernicus DEM GLO-30 [@CopernicusDEM] and land cover from ESA WorldCover v200 [@Zanaga2022]. For the sensitivity analyses, burned area was also taken from VIIRS VNP64A1 v002 [@VNP64A1] and land cover from ESA WorldCover v100 [@Zanaga2021], and regional weather anomalies came from ERA5-Land [@MunozSabater2021] as computed by the processing pipeline. The MODIS, VIIRS and Landsat products are courtesy of NASA's Land Processes Distributed Active Archive Center and the U.S. Geological Survey. WorldCover is distributed under a CC BY 4.0 licence (© ESA WorldCover project 2021, contains modified Copernicus Sentinel data (2021) processed by the ESA WorldCover consortium). The Copernicus DEM was produced using Copernicus WorldDEM-30 © DLR e.V. 2010 to 2014 and © Airbus Defence and Space GmbH 2014 to 2018, provided under COPERNICUS by the European Union and ESA; all rights reserved. The ERA5-Land values contain modified Copernicus Climate Change Service information. No proprietary or restricted data were used.

The five modelling datasets, one per region, and the frozen numeric outputs behind every reported number are released with the analysis code [@ThermalTwinRepo]. Each dataset is identified by its SHA-256 hash, which every analysis verifies on load. For Bejís, Muğla, North Evia and Montiferru the hash equals the canonical-input record of the upstream pipeline at commit `6381f4c`. For Manavgat it is the corrected-label re-freeze, produced at the same commit. The two small changes needed for this are given in Supplementary Section S5.7. The pipeline's own record still names the original-label table, which is not used here.

The upstream processing pipeline, `satellite-thermal-digital-twin` (E. Metin), is public at <https://github.com/emrehann17/satellite-thermal-digital-twin> under the MIT licence. The analysis code, figure scripts and checks are at <https://github.com/dryuemco/thermal-twin>, and version 1.2.0 is archived at Zenodo [@ThermalTwinRepo]. The repository holds the scripts that draw every figure and rebuild every table, and its checks assert every reported and plotted value against the frozen outputs. We used Python 3.12.10 with NumPy 2.4.4, pandas 3.0.2 and scikit-learn 1.9.0. Point estimates depend on the scikit-learn version, so exact reproduction needs this environment.

## Conflicts of interest

The authors declare that they have no conflicts of interest.

## Declaration of funding

This work was supported by the Çukurova University Scientific Research Projects Coordination Unit (Bilimsel Araştırma Projeleri Koordinasyon Birimi) under its Career Starter Project scheme, project code FKB-2025-17608 ("Early detection and prevention of forest fires with a thermal digital twin-based UAV swarm system"). The funder had no role in the study design, the analysis, the interpretation of the results, the writing of the manuscript or the decision to submit it.

## Acknowledgements

The authors thank the Department of Computer Engineering at Çukurova University for the laboratory environment in which this work was carried out.

## Author contributions

In CRediT terms, Emrehan Metin contributed software, data curation, investigation, validation and writing (review and editing). Yunus Emre Cogurcu contributed conceptualisation, methodology, formal analysis, investigation, visualisation, writing (original draft), writing (review and editing), supervision, project administration and funding acquisition. Both authors read and approved the final manuscript.

## Declaration of use of AI

Claude (Anthropic; Opus-family models, July to October 2026) was used to write code, including the code that draws the figures, to check reported numbers, and to check grammar and improve sentence clarity. The authors reviewed all of its output, made every scientific decision and take full responsibility for the content of the publication.

## Ethics statement

No ethics approval was needed. This study involved no human participants, animal subjects or personally identifiable data.
