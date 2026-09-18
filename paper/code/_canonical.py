"""Canonical inputs and leakage control shared by every script in paper/code.

Why this exists: until 2026-09-19 these scripts read
repo/outputs/experiments/<region>/step8a/..., a location a QC rebuild overwrote on
2026-08-14 for Manavgat and Mugla. Both files differ from the frozen exports in
downscaled_lst_mean and fused_lst_mean. The frozen exports are identified by the
pipeline's own record, repo/src/multi_region_window_closure/inputs.py
(CANONICAL_STEP8A_SHA256), which this module copies. A file whose hash does not
match is refused, so the incident cannot recur silently.

Leakage: Methods 3.13 states that a forbidden-column set is asserted at every model
fit. That was true for step10 and the upstream pipeline but not here, where scripts
used whitelists. assert_no_leakage() is that assertion; call it on every feature list
before a fit. The set is step10's FORBIDDEN_FEATURE_COLUMNS plus the label-derived
columns present in the parquet but absent from that list.
"""
from __future__ import annotations

import hashlib
import os
from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA_ROOT = Path(os.environ.get(
    "THERMAL_TWIN_DATA", r"C:\Users\CORSAIR\projects\thermal-twin\drive_new"))
STEP8A = "experiments/{}/step8a/step8a_500m_modeling_dataset.parquet"

# repo/src/multi_region_window_closure/inputs.py, CANONICAL_STEP8A_SHA256 (commit 6381f4c)
CANONICAL_SHA256 = {
    "manavgat_2021": "054a1961fc0582a33d36413263668b63074b21ae8b03d12269b6e228787f3439",
    "bejis_2022": "3dec785a7d8e31db2d67ed283546bbfbca1559f56df46663488d0afc24d9e393",
    "mugla_2021": "c4ab107db2207f9f20775ccc0b3bf39381173fd07d4e82f6821ce7f40be7db8e",
    "evia_2021_extended": "bdce859cf482f575d0f273174b157f47efd61779953fdd23d9486c5face5e553",
    "montiferru_2021": "ffb008f977445076835ae35a70776b0b813d0a36655d2c656fd21e6fedd4ac50",
}
REGIONS = tuple(CANONICAL_SHA256)

# step10/config10.py FORBIDDEN_FEATURE_COLUMNS ...
FORBIDDEN = {
    "burned", "burn_date", "burn_month", "burn_day_of_year", "label_source",
    "burn_date_pixel_agreement_fraction", "out_of_window_burndate", "cell_id",
    "row_500m", "col_500m", "valid_for_modeling", "invalid_reason",
    "source_mask_majority", "observed_fraction", "gapfilled_fraction",
    "invalid_source_fraction", "lon", "lat",
    # ... plus label-derived and population columns present in the parquet
    "pre_label_burn_excluded", "historical_burn_excluded", "analysis_eligible",
    "burnable_tree_shrub_grass", "burnable_tree_shrub",
}

BASELINE = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant"]
THERMAL = BASELINE + ["lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
                      "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]


class LeakageError(RuntimeError):
    pass


class ProvenanceError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@lru_cache(maxsize=None)
def path(region: str) -> Path:
    """Path of the canonical parquet for a region, verified by SHA-256."""
    p = DATA_ROOT / STEP8A.format(region)
    got = sha256(p)
    if got != CANONICAL_SHA256[region]:
        raise ProvenanceError(f"{region}: {p} has SHA-256 {got}, expected "
                              f"{CANONICAL_SHA256[region]}")
    return p


def load(region: str, columns=None) -> pd.DataFrame:
    """The canonical step8a table for a region, unfiltered. Callers apply their own
    population filter, exactly as before."""
    return pd.read_parquet(path(region), columns=columns)


def assert_no_leakage(features) -> None:
    """Fail fast if any feature is forbidden. Features may be one-hot names derived
    from landcover_dominant; those are allowed."""
    leaked = sorted(set(features) & FORBIDDEN)
    if leaked:
        raise LeakageError(f"forbidden columns in feature set: {leaked}")
