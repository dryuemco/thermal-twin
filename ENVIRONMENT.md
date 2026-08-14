# Analysis environment on this machine

Set up 2026-08-14, after Emrehan's internship ended, so that the pipeline can be run here rather
than only read. It is **verified**, not merely installed: see "Proof" below.

## What was installed

| Component | Version | Why this version |
|---|---|---|
| Python | 3.12.10 | The frozen runs used 3.12.3. The patch level was deliberately raised for the security fixes; the proof below shows it changes no number. |
| NumPy | **2.4.4** | Exactly what `paper/reproduction_check/reproduction_check_5region.json` records. |
| pandas | **3.0.2** | Same. |
| scikit-learn | **1.9.0** | Same. This is the one that matters most: §4.7e measures a ±0.02 to 0.03 cross-region tolerance between scikit-learn versions. |
| SciPy | 1.18.0 | `requirements-lock.txt` |
| pyarrow | 24.0.0 | `requirements-lock.txt` |
| matplotlib | 3.11.0 | `requirements-lock.txt` |
| rasterio | 1.5.0 | `requirements-lock.txt`; needed to read the 30 m GeoTIFFs |
| earthengine-api | 1.7.34 | `core/regions.py` imports `ee` at module level, so even the modelling steps need it present. No authentication is required to import it. |
| openpyxl, python-dotenv, geographiclib | lock versions | `requirements-lock.txt` |

Location: `.venv-step10/` at the project root (git-ignored). Interpreter:
`.venv-step10\Scripts\python.exe`.

> **Do not install from `repo/requirements.txt` directly.** Its ranges (`numpy>=2.4,<3`,
> `pandas>=3.0,<4`) resolve to newer releases than the ones that produced the paper's numbers.
> `repo/requirements-lock.txt` is closer but is **also not the production environment**: it pins
> NumPy 2.5.1 and pandas 3.0.3, while the frozen artefacts record 2.4.4 and 3.0.2. The table above
> is the authority.

## How it was built

```powershell
winget install --id Python.Python.3.12 --exact --scope user
python -m venv .venv-step10
.\.venv-step10\Scripts\python.exe -m pip install --upgrade pip
.\.venv-step10\Scripts\python.exe -m pip install `
  "numpy==2.4.4" "pandas==3.0.2" "scikit-learn==1.9.0" "scipy==1.18.0" `
  "joblib==1.5.3" "threadpoolctl==3.6.0" "pyarrow==24.0.0" "matplotlib==3.11.0"
.\.venv-step10\Scripts\python.exe -m pip install `
  "rasterio==1.5.0" "geographiclib==2.1" "openpyxl==3.1.5" "python-dotenv==1.2.2" `
  "earthengine-api==1.7.34"
```

## How to run a pipeline step

`BASE_DIR / arg` returns the argument unchanged when it is absolute, so absolute paths for both
`--input` and `--output-dir` keep every byte out of the `repo/` submodule. Keep it that way: the
project rule is that `repo/` and the existing `step8*` / `step9*` outputs are read-only.

```powershell
$env:PYTHONPATH = "C:\Users\CORSAIR\projects\thermal-twin\repo"
Push-Location repo
& ..\.venv-step10\Scripts\python.exe -m src.step8b_train_baseline_vs_thermal_model `
    --input  "C:\...\drive_new\experiments\manavgat_2021\step8a\step8a_500m_modeling_dataset.parquet" `
    --output-dir "C:\...\scratch\repro_manavgat_step8b" `
    --force
Pop-Location
```

Earth Engine authentication (`earthengine authenticate`) is needed **only** for the export steps
(Step 1 to Step 7). Everything from Step 8 onward reads local parquet and needs no credentials, and
those are the steps that produce every number in the paper.

## Proof that the environment is right

`src/step8b_train_baseline_vs_thermal_model.py` was run unmodified at `48b56e7` against the frozen
Step 8A parquet, and every numeric field of the output was compared with the archived
`step8b_model_comparison_metrics.json`:

| Region | numeric fields compared | max abs difference | fields differing by > 1e-9 |
|---|---|---|---|
| Manavgat 2021 | 142 | 6.9e-18 (a Brier score) | 0 |
| Montiferru 2021 | 168 | **exactly 0** | 0 |

Manavgat's Table 3 row reproduces to all sixteen digits: baseline `0.8027358197042693`, thermal
`0.8696419777927898`, ΔAUC `0.06690615808852052`. This is now stated in §3.13 of the manuscript,
because it partly answers the open blocker that the reproduction-check script itself is absent from
the released repository.

## What this unblocks

Work that previously had to wait for the pipeline author:

1. **The land-only TVDI edge refit** (`emrehan_mail_5.md` item 10). `rasterio` is installed and the
   30 m rasters are in `drive_new/experiments/<region>/step5c/` and `step5/`, with the aligned
   land-cover raster in `gate_inputs/`.
2. **The calendar-matched Muğla 2022 arm** (item 8), which would separate year from season in the
   two-event control, currently the design's main confound.
3. Any re-run a referee asks for on the within-region or transfer analyses.

## What it does not unblock

- The **transfer-arm reproduction check**: its script (`scripts/run_reproduction_check.py`,
  `src/reproduction_validation/`) is not in the released repository at all.
- **Earth Engine exports**, which need credentials and an EE-enabled Cloud project.
- **The LaTeX compile.** No TeX distribution is installed. `paper/tex/verify_tex.mjs` checks the
  source, not the typeset output.
