"""Manavgat 2021 label-window correction: corrected BurnDate raster and modelling table.

The frozen Manavgat label raster (drive_new/.../validation/labels/mcd64a1_raw.tif,
exported 2026-07-08) predates repo commit 183be42 (2026-07-11), which fixed the
month-aligned MCD64A1 collection query in repo/src/step6_validate_fire_relation.py.
With the old query the July 2021 monthly image was never selected, so every burn dated
28-31 July (DOY 209-212) is missing although the label window opens on 2021-07-28.

This script
  1. rebuilds the raw BurnDate raster for the full label window with the pipeline's
     fixed build_raw_burndate_image (via ems_labels_common, whose fetch() reads it on
     the frozen raster's exact 30 m grid), verifies it against the frozen raster and
     writes it (+ the binary mask, raw.gt(0), as the pipeline's export does);
  2. runs step8a's build_dataset label code path (imported, not reimplemented) on the
     FROZEN raster as a control that must reproduce the canonical label columns with
     0 disagreements, then on the corrected raster, and writes the corrected table:
     canonical non-label columns unchanged, label columns recomputed;
  3. re-runs the step6b burned-landcover gate (compute_gate, imported) on both rasters;
  4. writes labelfix_verification.json next to the outputs.

Nothing is written into repo/ or drive_new/: bytecode is disabled and the pipeline's
setup_logger (which writes repo/logs/*.log) is replaced by a stream-only logger before
any pipeline module is imported.

Usage (from anywhere):
  set PYTHONDONTWRITEBYTECODE=1
  .venv-step10\\Scripts\\python.exe paper\\code\\manavgat_labelfix.py [--cache DIR] [--fresh]
--cache DIR  : directory holding / receiving manavgat_2021_labelwin.npy (the EE read).
--fresh      : always re-read from Earth Engine; if a cached array exists, it must match.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
import logging
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TREE = HERE.parents[1]
UPSTREAM = Path(r"C:\Users\CORSAIR\projects\thermal-twin")
REPO = UPSTREAM / "repo"
FROZEN_EXP = UPSTREAM / "drive_new" / "experiments" / "manavgat_2021"
FROZEN_RAW = FROZEN_EXP / "validation/labels/mcd64a1_raw.tif"
FROZEN_BIN = FROZEN_EXP / "validation/labels/mcd64a1_burned.tif"
FROZEN_GATE = FROZEN_EXP / "validation/labels/burned_landcover_gate.json"
GATE_REF = FROZEN_EXP / "gate_inputs/reference_30m.tif"
GATE_LC = FROZEN_EXP / "gate_inputs/landcover_esa_worldcover_v200_aligned_to_reference.tif"
OUT = TREE / "paper" / "data" / "manavgat_2021"
OUT_RAW = OUT / "mcd64a1_raw_labelfix.tif"
OUT_BIN = OUT / "mcd64a1_burned_labelfix.tif"
OUT_PARQUET = OUT / "step8a_500m_modeling_dataset_labelfix.parquet"
OUT_JSON = OUT / "labelfix_verification.json"
REG = "manavgat_2021"
LABEL_COLS = ["burned", "burn_date", "burn_month", "burn_day_of_year", "label_source",
              "burn_date_pixel_agreement_fraction", "out_of_window_burndate"]
FIX_DOYS = (209, 210, 211, 212)

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

# ---- keep the pipeline from writing repo/logs/*.log -------------------------------
import core.io_utils as _iou  # noqa: E402


def _stream_only_logger(step_name: str):
    lg = logging.getLogger(step_name)
    lg.setLevel(logging.WARNING)
    lg.propagate = False
    for h in lg.handlers[:]:
        lg.removeHandler(h)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s [%(name)s] %(message)s"))
    lg.addHandler(h)
    return lg, None


_iou.setup_logger = _stream_only_logger

import rasterio  # noqa: E402

import _canonical as C  # noqa: E402


def log(*a):
    print(*a, flush=True)


def sha256(p: Path) -> str:
    return C.sha256(p)


def rebuild_raster(cache: Path | None, fresh: bool) -> tuple[np.ndarray, dict]:
    """The EE read, via ems_labels_common (same route the r5 analysis validated)."""
    import ems_labels_common as E
    x = E.experiment(REG)
    info = {"label_window": [x["label_start_date"], x["label_end_date"]]}
    cached = None
    if cache is not None and (cache / f"{REG}_labelwin.npy").exists():
        cached = np.load(cache / f"{REG}_labelwin.npy")
    if cached is not None and not fresh:
        info["source"] = f"cached computePixels read {cache / f'{REG}_labelwin.npy'}"
        return cached, info
    s6 = E.s6()
    qb = s6._mcd64a1_collection_query_bounds(x["label_start_date"], x["label_end_date"])
    info["collection_query_window_exclusive_end"] = list(qb)
    img = s6.build_raw_burndate_image(E.region_geometry(REG), x["label_start_date"],
                                      x["label_end_date"])
    a = E.fetch(img, REG, "BurnDate")
    info["source"] = "fresh Earth Engine computePixels read"
    if cached is not None:
        same = bool(np.array_equal(a, cached))
        info["fresh_equals_cache"] = same
        if not same:
            raise SystemExit("fresh EE read differs from the cached array")
    elif cache is not None:
        cache.mkdir(parents=True, exist_ok=True)
        np.save(cache / f"{REG}_labelwin.npy", a)
    return a, info


def verify_raster(new: np.ndarray, frozen: np.ndarray) -> dict:
    assert new.shape == frozen.shape and new.dtype == frozen.dtype == np.int16
    nodata_new = int((new == -32768).sum())
    fpos = frozen > 0
    added = (frozen == 0) & (new > 0)
    u_add, c_add = np.unique(new[added], return_counts=True)
    u_new, c_new = np.unique(new, return_counts=True)
    u_old, c_old = np.unique(frozen, return_counts=True)
    r = {
        "shape": list(new.shape),
        "nodata_pixels_corrected": nodata_new,
        "nodata_pixels_frozen": int((frozen == -32768).sum()),
        "frozen_positive_pixels": int(fpos.sum()),
        "frozen_positive_identical_in_corrected": int((new[fpos] == frozen[fpos]).sum()),
        "frozen_positive_changed_in_corrected": int((new[fpos] != frozen[fpos]).sum()),
        "frozen_zero_pixels": int((frozen == 0).sum()),
        "added_pixels": int(added.sum()),
        "added_by_doy": {int(k): int(v) for k, v in zip(u_add, c_add)},
        "corrected_positive_pixels": int((new > 0).sum()),
        "values_frozen": {int(k): int(v) for k, v in zip(u_old, c_old)},
        "values_corrected": {int(k): int(v) for k, v in zip(u_new, c_new)},
    }
    r["check_a_frozen_values_preserved"] = (r["frozen_positive_changed_in_corrected"] == 0
                                            and nodata_new == 0)
    r["check_b_additions_only_doy_209_212"] = bool(set(r["added_by_doy"]) <= set(FIX_DOYS))
    r["check_no_positive_removed"] = bool(((frozen > 0) & (new <= 0)).sum() == 0)
    if not (r["check_a_frozen_values_preserved"] and r["check_b_additions_only_doy_209_212"]
            and r["check_no_positive_removed"]):
        raise SystemExit(f"raster verification failed: {json.dumps(r, indent=1)}")
    return r


def write_rasters(new: np.ndarray) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    with rasterio.open(FROZEN_RAW) as s:
        prof_raw = s.profile.copy()
        tags = s.tags()
    with rasterio.open(FROZEN_BIN) as s:
        prof_bin = s.profile.copy()
    with rasterio.open(OUT_RAW, "w", **prof_raw) as d:
        d.write(new, 1)
        d.update_tags(**tags)
    # the pipeline's binary export is raw_image.gt(0), uint8 with nodata=0
    with rasterio.open(OUT_BIN, "w", **prof_bin) as d:
        d.write((new > 0).astype("uint8"), 1)
        d.update_tags(**tags)
    out = {}
    for p, ref in ((OUT_RAW, FROZEN_RAW), (OUT_BIN, FROZEN_BIN)):
        with rasterio.open(p) as a, rasterio.open(ref) as b:
            same = {k: (a.profile[k] == b.profile[k]) for k in
                    ("driver", "dtype", "nodata", "width", "height", "count", "crs",
                     "transform", "blockxsize", "blockysize", "tiled", "compress")}
            if not all(same.values()):
                raise SystemExit(f"{p}: profile differs from {ref}: {same}")
            back = a.read(1)
        out[p.name] = {"profile_matches_frozen": same, "sha256": sha256(p)}
    with rasterio.open(OUT_RAW) as a:
        if not np.array_equal(a.read(1), new):
            raise SystemExit("written raw raster does not read back identically")
    with rasterio.open(OUT_BIN) as a, rasterio.open(FROZEN_BIN) as b:
        fb = b.read(1)
        nb = a.read(1)
        out[OUT_BIN.name]["frozen_mask_subset_of_corrected"] = bool(((fb == 1) & (nb != 1)).sum() == 0)
    with rasterio.open(FROZEN_RAW) as a, rasterio.open(FROZEN_BIN) as b:
        out["frozen_binary_equals_frozen_raw_gt0"] = bool(np.array_equal(b.read(1) == 1, a.read(1) > 0))
    return out


def step8a_labels(label_path: Path, window: list[str]) -> tuple[pd.DataFrame, dict]:
    import src.step8a_prepare_500m_modeling_dataset as S8
    with rasterio.open(label_path) as a, rasterio.open(GATE_REF) as r:
        assert (a.width, a.height, a.crs, a.transform) == (r.width, r.height, r.crs, r.transform)
    diag = S8.inspect_label_raster(label_path, S8.LABEL_KIND_RAW, *window)
    with tempfile.TemporaryDirectory() as td:
        res = S8.build_dataset(
            reference_path=GATE_REF, label_path=label_path, label_kind=S8.LABEL_KIND_RAW,
            predictor_paths={}, landcover_path=GATE_LC, source_mask_path=None,
            output_dir=Path(td), min_valid_fraction=S8.STEP8A_MIN_30M_VALID_FRACTION,
            burnable_threshold=S8.STEP8A_BURNABLE_FRACTION_THRESHOLD,
            label_start=window[0], label_end=window[1],
            pre_label_excluded_cell_ids=None, historical_excluded_cell_ids=None)
    c = res["counters"]
    return res["dataframe"], {"inspect_label_raster": diag,
                              "burned_cell_count": c["burned_cell_count"],
                              "burn_month_counts": {str(k): v for k, v in c["burn_month_counts"].items()},
                              "out_of_window_burndate_cells": c["out_of_window_burndate_cells"],
                              "block_size_pixels": res["block_size_pixels"],
                              "min_valid_fraction": S8.STEP8A_MIN_30M_VALID_FRACTION,
                              "burnable_threshold": S8.STEP8A_BURNABLE_FRACTION_THRESHOLD}


def col_equal(a: pd.Series, b: pd.Series) -> tuple[bool, int]:
    """Exact equality with NaN==NaN; floats compared bit for bit."""
    if a.dtype.kind == "f" and b.dtype.kind == "f":
        x, y = a.to_numpy(), b.to_numpy()
        both_nan = np.isnan(x) & np.isnan(y)
        diff = ~(both_nan | (x.view(np.int64) == y.view(np.int64)))
        return int(diff.sum()) == 0, int(diff.sum())
    x = a.astype(object).to_numpy()
    y = b.astype(object).to_numpy()
    diff = np.array([not ((pd.isna(u) and pd.isna(v)) or u == v) for u, v in zip(x, y)])
    return int(diff.sum()) == 0, int(diff.sum())


def align(canon: pd.DataFrame, built: pd.DataFrame) -> pd.DataFrame:
    b = built.set_index("cell_id").loc[canon.cell_id.to_numpy()].reset_index()
    assert (b.row_500m.to_numpy() == canon.row_500m.to_numpy()).all()
    assert (b.col_500m.to_numpy() == canon.col_500m.to_numpy()).all()
    return b


def compare_labels(canon: pd.DataFrame, b: pd.DataFrame) -> dict:
    out = {}
    for col in LABEL_COLS:
        ok, n = col_equal(canon[col], b[col].astype(canon[col].dtype))
        out[col] = {"equal": ok, "disagreements": n}
    return out


def gate(label_path: Path, window: list[str]) -> dict:
    import src.step6b_burned_landcover_gate as G
    import src.step8a_prepare_500m_modeling_dataset as S8
    from core.config import (STEP6_BURNED_LANDCOVER_GATE_MIN_POSITIVES as MINP,
                             STEP6_BURNED_LANDCOVER_GATE_NATURAL_THRESHOLD as NAT,
                             STEP6_BURNED_LANDCOVER_GATE_CROPLAND_THRESHOLD as CROP)
    with tempfile.TemporaryDirectory() as td:
        g = G.compute_gate(label_path=label_path, label_kind=S8.LABEL_KIND_RAW,
                           reference_path=GATE_REF, landcover_path=GATE_LC,
                           label_start=window[0], label_end=window[1], output_dir=Path(td),
                           min_positives=MINP, natural_threshold=NAT, cropland_threshold=CROP)
    g.pop("pre_label_excluded_manifest_rows", None)
    return g


GATE_KEYS = ["total_valid_cells_or_pixels_considered", "burned_count", "unburned_count",
             "burned_landcover_dominant_counts", "unburned_landcover_dominant_counts",
             "burned_tree_cover_count", "burned_shrubland_count", "burned_grassland_count",
             "burned_cropland_count", "burned_tree_shrub_grass_count", "burned_tree_shrub_count",
             "burned_cropland_dominant_count", "burned_natural_vegetation_fraction",
             "burned_cropland_fraction", "burned_tree_shrub_fraction",
             "burned_cells_without_valid_landcover", "unburned_cells_without_valid_landcover",
             "decision", "reason", "thresholds"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path, default=None)
    ap.add_argument("--fresh", action="store_true")
    args = ap.parse_args()
    rep: dict = {"script": "paper/code/manavgat_labelfix.py"}

    # ---------------------------------------------------------------- 1. raster
    new, info = rebuild_raster(args.cache, args.fresh)
    rep["rebuild"] = info
    window = info["label_window"]
    with rasterio.open(FROZEN_RAW) as s:
        frozen = s.read(1)
    rep["raster_verification"] = verify_raster(new, frozen)
    log("raster:", {k: v for k, v in rep["raster_verification"].items()
                    if not k.startswith("values_")})
    rep["raster_files"] = write_rasters(new)
    log("rasters written:", rep["raster_files"])

    # ---------------------------------------------------------------- 2. table
    canon = C.load(REG, labels="frozen")
    rep["canonical"] = {"path": str(C.path(REG, labels="frozen")),
                        "sha256": C.CANONICAL_SHA256[REG], "shape": list(canon.shape)}
    built_f, meta_f = step8a_labels(FROZEN_RAW, window)
    bf = align(canon, built_f)
    ctrl = compare_labels(canon, bf)
    rep["control_frozen_raster"] = {"label_columns": ctrl, "step8a": meta_f}
    # bonus grid sanity: landcover-derived columns from the same build_dataset call
    lc_cols = [c for c in canon.columns if c.startswith("landcover_") or c.startswith("burnable_")]
    rep["control_frozen_raster"]["landcover_columns"] = {
        c: col_equal(canon[c], bf[c].astype(canon[c].dtype))[1] for c in lc_cols}
    log("control:", ctrl)
    if not all(v["equal"] for v in ctrl.values()):
        OUT.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(rep, indent=1, default=str), encoding="utf-8")
        raise SystemExit("CONTROL FAILED: step8a label path does not reproduce the canonical labels")

    built_n, meta_n = step8a_labels(OUT_RAW, window)
    bn = align(canon, built_n)
    fixed = canon.copy()
    for col in LABEL_COLS:
        fixed[col] = bn[col].astype(canon[col].dtype).to_numpy()
    fixed.to_parquet(OUT_PARQUET, index=False)
    back = pd.read_parquet(OUT_PARQUET)
    percol = {}
    assert list(back.columns) == list(canon.columns)
    for col in canon.columns:
        ok, n = col_equal(canon[col], back[col])
        percol[col] = {"dtype_equal": str(back[col].dtype) == str(canon[col].dtype),
                       "equal_to_canonical": ok, "cells_differing": n,
                       "role": "label (recomputed)" if col in LABEL_COLS else "non-label"}
        if col in LABEL_COLS:
            ok2, n2 = col_equal(bn[col].astype(canon[col].dtype), back[col])
            percol[col]["equal_to_recomputed"] = ok2
            assert ok2, col
        else:
            assert ok and percol[col]["dtype_equal"], col
    rep["corrected_table"] = {"path": str(OUT_PARQUET), "sha256": sha256(OUT_PARQUET),
                              "shape": list(back.shape), "per_column": percol, "step8a": meta_n}
    log("non-label columns identical:",
        all(v["equal_to_canonical"] for k, v in percol.items() if k not in LABEL_COLS))

    # counts
    tsg = (canon.valid_for_modeling == True) & (canon.burnable_tree_shrub_grass == True)  # noqa: E712
    pops = {"all_cells": np.ones(len(canon), bool), "all_valid": canon.valid_for_modeling.to_numpy(bool),
            "natural_vegetation": tsg.to_numpy()}
    counts = {}
    for name, m in pops.items():
        f, n = canon[m], back[m]
        counts[name] = {
            "n": int(m.sum()), "burned_frozen": int(f.burned.sum()), "burned_corrected": int(n.burned.sum()),
            "prevalence_frozen": float(f.burned.mean()), "prevalence_corrected": float(n.burned.mean()),
            "gained": int(((f.burned == 0) & (n.burned == 1)).sum()),
            "lost": int(((f.burned == 1) & (n.burned == 0)).sum()),
            "burned_by_doy_corrected": {int(k): int(v) for k, v in
                                        n[n.burned == 1].burn_day_of_year.value_counts().sort_index().items()},
            "burned_by_doy_frozen": {int(k): int(v) for k, v in
                                     f[f.burned == 1].burn_day_of_year.value_counts().sort_index().items()},
            "burned_by_month_corrected": {int(k): int(v) for k, v in
                                          n[n.burned == 1].burn_month.value_counts().sort_index().items()},
            "previously_burned_with_changed_burn_date": int(
                ((f.burned == 1) & (f.burn_day_of_year != n.burn_day_of_year)).sum()),
            "previously_burned_with_changed_agreement": int(
                ((f.burned == 1) & (f.burn_date_pixel_agreement_fraction
                                    != n.burn_date_pixel_agreement_fraction)).sum()),
        }
    rep["cell_counts"] = counts
    log("counts:", {k: (v["n"], v["burned_frozen"], v["burned_corrected"]) for k, v in counts.items()})

    # ---------------------------------------------------------------- 3. gate
    frozen_gate = json.loads(FROZEN_GATE.read_text(encoding="utf-8"))
    g_ctrl = gate(FROZEN_RAW, window)
    g_new = gate(OUT_RAW, window)
    rep["gate"] = {
        "frozen_json": {k: frozen_gate.get(k) for k in GATE_KEYS},
        "recomputed_on_frozen_raster": {k: g_ctrl.get(k) for k in GATE_KEYS},
        "control_mismatches": [k for k in GATE_KEYS if frozen_gate.get(k) != g_ctrl.get(k)],
        "corrected": {k: g_new.get(k) for k in GATE_KEYS},
    }
    log("gate control mismatches:", rep["gate"]["control_mismatches"])
    log("gate corrected:", g_new["decision"], g_new["burned_count"],
        g_new["burned_natural_vegetation_fraction"])

    rep["hashes"] = {"frozen_raw": sha256(FROZEN_RAW), "frozen_binary": sha256(FROZEN_BIN),
                     "canonical_parquet": sha256(C.DATA_ROOT / C.STEP8A.format(REG)),
                     "corrected_raw": sha256(OUT_RAW), "corrected_binary": sha256(OUT_BIN),
                     "corrected_parquet": sha256(OUT_PARQUET)}
    OUT_JSON.write_text(json.dumps(rep, indent=1, default=str), encoding="utf-8")
    log("hashes:", rep["hashes"])
    log("done")


if __name__ == "__main__":
    main()
