# Manuscript package: Environmental Modelling & Software

Manuscript "A predictor-free geographic reference for evaluating wildfire susceptibility models, tested on
31 Mediterranean fires and five published datasets", prepared for Environmental Modelling & Software.

## Files

- `manuscript.tex`: the manuscript (Elsevier elsarticle class, author-year citations).
- `values.tex`: every result of the study quoted in the manuscript, as LaTeX macros. Generated, do not edit.
- `build_values_figures.py`: writes `values.tex`, `manuscript_statistics.json`, `figures/Figure_1.pdf` to
  `Figure_5.pdf` and `graphical_abstract.png` from the analysis outputs.
- `manuscript_statistics.json`: statistics computed by the build step, not by the analysis scripts (the
  fire-level transfer intervals, the paired cAUC difference, the matched-pair AUC, the buffer coverage and the
  near and far band AUC under every label variant). Its transfer intervals supersede the direction-level
  intervals in `claim4_summary.json`.
- `make_highlights.py`, `highlights.docx`: the separate highlights file, built from the manuscript.
- `references.bib`, `elsarticle.cls`, `elsarticle-harv.bst`: bibliography, class and style (LPPL, from CTAN).

## Code versions

- Analysis: branch `scaleup-31fires` of this repository, scripts in `scripts/scaleup/`, plan and its three
  amendments in `docs/scaleup/ANALYSIS_PLAN.md`. It builds on the upstream pipeline
  `emrehann17/satellite-thermal-digital-twin` at commit `6381f4c`.
- The analysis reads two files of the `main` branch through `THERMAL_TWIN_PAPER` (the `paper/` folder):
  `paper/code/_canonical.py` with the SHA-256 verified tables in `paper/data/`, and the frozen reference
  values used by the reproduction gates, `paper/labelfix_rerun/geometry/a1_band_auc.csv` and
  `paper/supplementary.md` (Table S8).

## Running the analysis

Set three environment variables:

- `THERMAL_TWIN_PAPER`: the `paper/` folder of a checkout of `main`.
- `THERMAL_TWIN_SCALEUP`: the run folder. It holds the worker clones `w1` to `w3` of the pipeline with their
  `outputs/experiments/<fire>` folders, `open_data/` with the five published datasets, and `analysis/`, where
  every script writes its results.
- `GEE_PROJECT`: the Earth Engine project for the export steps.

Then run, from `scripts/scaleup/` on branch `scaleup-31fires`:

1. `run_batch.sh` on the three worker clones (pipeline for the 31 experiments; the worker lists are in the run folder).
2. `analysis_official.py` (claims 1 and 2, with the reproduction gates).
3. `s2_label_check_export.py`, then `claim3_label_check.py` (Sentinel-2 label check).
4. `claim4_transfer.py` (transfer and pooling).
5. `aqua_lst_export.py`, then `claim5_lst_sign.py` (pre-fire temperature).
6. `multiyear_label_export.py`, then `claim6_multiyear.py` (multi-year label).
7. `claim7_open_data.py`, then `claim7_alberta_ci.py` (published datasets; download the five datasets first,
   sources in the manuscript's data availability section).

## Building the manuscript

```
THERMAL_TWIN_ANALYSIS=<run folder>/analysis THERMAL_TWIN_REPO=<checkout of scaleup-31fires> python build_values_figures.py
python make_highlights.py
pdflatex manuscript && bibtex manuscript && pdflatex manuscript && pdflatex manuscript
```

The analysis outputs, the modelling tables of the 31 fires and the Sentinel-2 and multi-year label rasters
will be archived in a versioned Zenodo release together with the code.
