# ENVIRONMENT_FIRE2 — pinned software environment of the fire2 study

Built and verified 2026-09-19. Lock file: `design/requirements-lock.txt`
(PREREGISTRATION.md §6.3 "Software (M9)"; FWI_SPEC.md §2).

**SHA-256 of `design/requirements-lock.txt`:**
`ed6cdaca6466b3a7e25f7a6ab522430ec048582a90bda9fb2731f25b3a767b2b`

## 1. How it was built

- Interpreter: CPython **3.12.10**, `C:\Users\CORSAIR\AppData\Local\Programs\Python\Python312\python.exe`,
  Windows 11 Pro 10.0.26200.
- Venv: `.venv-fire2\` at the repository root (git-ignored). Separate from `.venv-step10`, which
  belongs to another study and was not touched.
- Commands (Git Bash):
  ```
  python -m venv .venv-fire2
  .venv-fire2/Scripts/python.exe -m pip install --upgrade pip          # -> pip 26.2.1
  .venv-fire2/Scripts/python.exe -m pip install xclim==0.62.0 numba==0.67.0 llvmlite==0.49.0 \
      numpy==2.5.3 xarray==2026.7.0 pandas==3.0.6 scipy==1.18.1 dask==2026.8.0 Pint==0.26.1 \
      cf_xarray==0.11.3 boltons==26.2.0 Bottleneck==1.6.0 cftime==1.6.5 pyarrow==25.0.1 \
      scikit-learn earthengine-api rasterio geopandas shapely matplotlib pytest
  .venv-fire2/Scripts/python.exe -m pip freeze   # -> requirements-lock.txt (3 header comment lines added)
  ```
- The FWI_SPEC §2 pins were used exactly. The remaining packages were left unpinned and pip chose the
  latest compatible release. `pip check`: no broken requirements. `pip list --outdated`: empty, so
  every installed package, the FWI_SPEC pins included, is the latest release on PyPI as of 2026-09-19.
- 76 packages in the lock file.
- Rebuild: `python3.12 -m pip install -r design/requirements-lock.txt`. The lock was frozen on Windows.
  `colorama` is a Windows-only dependency, but it is pure Python and installs on Linux too. All
  binary packages in the lock have Linux wheels on PyPI; the container build is still to be verified
  and its image digest recorded (§6.3).

## 2. Key versions

| Package | Version | Package | Version |
|---|---|---|---|
| Python | 3.12.10 | scikit-learn | 1.9.1 |
| xclim | 0.62.0 | numpy | 2.5.3 |
| numba | 0.67.0 | scipy | 1.18.1 |
| llvmlite | 0.49.0 | pandas | 3.0.6 |
| xarray | 2026.7.0 | pyarrow | 25.0.1 |
| dask | 2026.8.0 | earthengine-api | 1.7.43 |
| Pint | 0.26.1 | rasterio | 1.5.1 |
| cf_xarray | 0.11.3 | geopandas | 1.1.4 |
| cftime | 1.6.5 | shapely | 2.1.2 |
| Bottleneck | 1.6.0 | pyproj | 3.8.0 |
| boltons | 26.2.0 | pyogrio | 0.13.0 |
| matplotlib | 3.11.2 | pytest | 9.1.1 |

## 3. Verification (2026-09-19, all passed)

**Imports.** numpy, scipy, pandas, pyarrow, xarray, xclim, numba, llvmlite, sklearn, ee, rasterio,
geopandas, shapely, matplotlib, pytest, dask, pint, cf_xarray, cftime and bottleneck all import.
`import ee` works; no authentication was attempted.

**§6.3 models.** On a toy data set (seed 42), each model was instantiated with its exact §6.3
arguments and fitted:
- `RandomForestClassifier(..., max_features="sqrt", class_weight="balanced", random_state=42)`.
- `HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=31,
  min_samples_leaf=20, l2_regularization=0.0, class_weight="balanced", early_stopping=False,
  random_state=42)`.
- `SplineTransformer(n_knots=5, degree=3)` followed by `LogisticRegression(penalty="l2", C=1.0,
  class_weight="balanced", max_iter=5000)`.

`StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)` produced 5 splits.

**FWI reference test (FWI_SPEC §4 T1 and T2).** The inputs were the 49 rows of
`design/fwi_reference_rows.csv` (13 Apr – 31 May 1985), taken directly as noon values. The call was
the FWI_SPEC §2 canonical call: `xclim.indices.fire.cffwis_indices(..., season_method=None,
overwintering=False, dry_start=None, ffmc_start=85, dmc_start=6, dc_start=15)`. The units were
`degC`, `mm/d`, `km/h`, `%` and `degrees_north`. It was run at lat 40 and at lat 46.

| Code | Match with published value after rounding to 1 dp | max \|out − published\| (row) | max \|out − xclim0620_*\| |
|---|---|---|---|
| FFMC | 49/49 | 0.0494 (29) | 4.98e-5 |
| DMC | 49/49 | 0.0498 (44) | 4.89e-5 |
| DC | 49/49 | 0.0499 (43) | 3.76e-5 |
| ISI | 49/49 | 0.0500 (12) | 4.90e-5 |
| BUI | 49/49 | 0.0496 (29) | 4.91e-5 |
| FWI | 49/49 | 0.0498 (46) | 4.96e-5 |

- **T1 passed.** 294/294 values equal the published value after rounding, and 294/294 lie within
  ≤ 0.051 of it. The largest deviations are identical to those recorded in FWI_SPEC §5.
- **T2 passed.** All 294 values agree with the `xclim0620_*` columns to within 1e-4, the FWI_SPEC
  criterion, and therefore also to within 1e-3. The largest deviation is 4.98e-5, which is within
  the rounding of the stored 4-decimal values.
- Lat 40 and lat 46 give identical output (max difference 0.0).

## 4. NUMBA_CACHE_DIR note

FWI_SPEC §2 records that on Windows, numba's cache write can fail with `FileNotFoundError` at import
when site-packages sits under a long path. In this venv, whose path is short
(`C:\Users\CORSAIR\projects\thermal-twin-main\.venv-fire2`), `import xclim.indices.fire` succeeded
**without** `NUMBA_CACHE_DIR`. The verification itself ran with `NUMBA_CACHE_DIR=C:\nbc`. It is still
recommended that scripts set it before importing xclim, because the failure depends on path length
and the container path may differ:
```python
import os; os.environ.setdefault("NUMBA_CACHE_DIR", r"C:\nbc")   # or /tmp/nbc in the container
```
