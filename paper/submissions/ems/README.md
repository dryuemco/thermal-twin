# Manuscript package: Environmental Modelling & Software

Manuscript "A predictor-free geographic reference for evaluating wildfire susceptibility models, tested on
31 Mediterranean fires and five published datasets", prepared for Environmental Modelling & Software.

## Files

- `manuscript.tex`: the manuscript (Elsevier elsarticle class, author-year citations).
- `values.tex`: every result of the study quoted in the manuscript, as LaTeX macros. Generated, do not edit.
- `build_values_figures.py`: writes `values.tex` and `figures/Figure_1.pdf` to `Figure_5.pdf` from the analysis outputs.
- `references.bib`: the bibliography.
- `elsarticle.cls`, `elsarticle-harv.bst`: the Elsevier class and bibliography style (LPPL, from CTAN).
- `highlights.docx`, `graphical_abstract.png`: the separate submission files.

## Rebuilding

1. Run the analysis on branch `scaleup-31fires` of this repository: the scripts in `scripts/scaleup/`, in the
   order given in `docs/scaleup/ANALYSIS_PLAN.md`, section 5. They write their outputs to one folder.
2. Point the build at that folder and at the analysis checkout, then build values and figures:

   ```
   THERMAL_TWIN_ANALYSIS=<analysis output folder> THERMAL_TWIN_REPO=<checkout of scaleup-31fires> python build_values_figures.py
   ```

3. Compile: `pdflatex manuscript`, `bibtex manuscript`, then `pdflatex manuscript` twice.

The analysis outputs, the modelling tables of the 31 fires and the Sentinel-2 and multi-year label rasters
will be archived in a versioned Zenodo release together with the code.
