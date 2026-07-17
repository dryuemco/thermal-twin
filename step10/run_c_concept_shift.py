"""
step10/run_c_concept_shift.py  --  IS 3: Concept-shift kaniti

Her bolge icin (BİRİNCİL popülasyon = burnable_tree_shrub_grass) her numerik
feature'in burned'a karsi ISARETLI univariate ROC-AUC'sini + spatial-block
bootstrap %95 CI'sini hesaplar. Iki bolge arasinda 0.5'in TERS taraflarina dusen
(yon reversal) feature'lari tablolar.

Reversal siniflandirmasi:
    - "bootstrap_supported": iki bolgenin univariate AUC %95 CI'leri AYRIK
      (ustuste binmiyor) VE 0.5'in ters taraflarinda -> guclu concept-shift kaniti.
    - "point_reversal": nokta tahminleri ters tarafta ama CI'ler ustuste biniyor.

Cikti:
    experiments/cross_region/step10/concept_shift.json
    experiments/cross_region/step10/concept_shift_univariate_auc.csv
    experiments/cross_region/step10/concept_shift_reversals.csv
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from config10 import (
    ALL_NUMERIC_FEATURES,
    CONCEPT_SHIFT_BLOCK_SIZE_CELLS,
    CROSS_REGION_DIR,
    N_BOOTSTRAP,
    PRIMARY_POPULATION,
    REGIONS,
    SEED,
    TARGET_COLUMN,
)
from data_io import add_spatial_block_id, assert_no_leakage, load_region
from metrics import univariate_signed_auc
from spatial_bootstrap import block_bootstrap_ci

OUT_DIR = CROSS_REGION_DIR / "step10"
REGION_KEYS = list(REGIONS.keys())  # [manavgat_2021, bejis_2022]


def _feature_auc_ci(col: np.ndarray, y: np.ndarray, block_ids: np.ndarray) -> dict:
    """Bir feature icin ISARETLI univariate AUC + spatial-block bootstrap %95 CI.
    NaN feature satirlari (ve o satirlarin bloklari) dislanir; AUC isareti korunur
    (feature dogrudan skor olarak verilir, max(auc,1-auc) YAPILMAZ)."""
    col = np.asarray(col, dtype="float64")
    mask = np.isfinite(col)
    point = univariate_signed_auc(col, y)
    if point["auc"] is None:
        return {"auc": None, "ci95": [None, None], "n_used": point["n_used"]}
    ci = block_bootstrap_ci(
        y[mask], col[mask], block_ids[mask], n_bootstrap=N_BOOTSTRAP, seed=SEED
    )
    return {
        "auc": point["auc"],
        "ci95": ci["roc_auc_ci95"],
        "ci_lo": ci["roc_auc_ci95"][0],
        "ci_hi": ci["roc_auc_ci95"][1],
        "n_used": point["n_used"],
        "n_blocks": ci["n_blocks"],
    }


def _disjoint(ci_a: list, ci_b: list) -> bool:
    """Iki %95 CI ayrik mi (ustuste binmiyor mu)?"""
    if None in ci_a or None in ci_b:
        return False
    a_lo, a_hi = ci_a
    b_lo, b_hi = ci_b
    return a_hi < b_lo or b_hi < a_lo


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    assert_no_leakage(ALL_NUMERIC_FEATURES)

    per_region = {}
    for key in REGION_KEYS:
        df = load_region(key, population=PRIMARY_POPULATION)
        y = df[TARGET_COLUMN].astype(int).to_numpy()
        # Emrehan step9g ile AYNI: 10 hucre (~5km) spatial bloklar.
        block_ids = add_spatial_block_id(df, CONCEPT_SHIFT_BLOCK_SIZE_CELLS).to_numpy()
        feats = {}
        for f in ALL_NUMERIC_FEATURES:
            col = df[f].to_numpy(dtype="float64")
            ac = _feature_auc_ci(col, y, block_ids)
            feats[f] = {
                "auc": ac["auc"],
                "ci95": ac["ci95"],
                "n_used": ac["n_used"],
                "mean": float(np.nanmean(col)) if np.isfinite(col).any() else None,
                "std": float(np.nanstd(col)) if np.isfinite(col).any() else None,
            }
        per_region[key] = {
            "n": int(len(df)),
            "burned": int(y.sum()),
            "population": PRIMARY_POPULATION,
            "features": feats,
        }
        print(f"[region] {key} ({PRIMARY_POPULATION}): n={len(df)}, burned={int(y.sum())}")

    r0, r1 = REGION_KEYS[0], REGION_KEYS[1]

    rows = []
    reversal_rows = []
    n_bootstrap_supported = 0
    for f in ALL_NUMERIC_FEATURES:
        f0 = per_region[r0]["features"][f]
        f1 = per_region[r1]["features"][f]
        a0, a1 = f0["auc"], f1["auc"]
        ci0, ci1 = f0["ci95"], f1["ci95"]
        reversal = (a0 is not None and a1 is not None and (a0 - 0.5) * (a1 - 0.5) < 0)
        disjoint = _disjoint(ci0, ci1)
        support = ("bootstrap_supported" if (reversal and disjoint)
                   else ("point_reversal" if reversal else "none"))
        auc_gap = abs(a0 - a1) if (a0 is not None and a1 is not None) else None
        rows.append({
            "feature": f,
            f"auc_{r0}": a0, f"auc_{r0}_ci_lo": ci0[0], f"auc_{r0}_ci_hi": ci0[1],
            f"auc_{r1}": a1, f"auc_{r1}_ci_lo": ci1[0], f"auc_{r1}_ci_hi": ci1[1],
            "auc_abs_gap": auc_gap,
            "direction_reversal": bool(reversal),
            "ci_disjoint": bool(disjoint),
            "reversal_support": support,
            f"mean_{r0}": f0["mean"], f"mean_{r1}": f1["mean"],
            f"std_{r0}": f0["std"], f"std_{r1}": f1["std"],
        })
        if reversal:
            if disjoint:
                n_bootstrap_supported += 1
            reversal_rows.append({
                "feature": f,
                f"auc_{r0}": a0, f"auc_{r0}_ci95": ci0,
                f"auc_{r1}": a1, f"auc_{r1}_ci95": ci1,
                f"relation_{r0}": "positive" if a0 > 0.5 else "negative",
                f"relation_{r1}": "positive" if a1 > 0.5 else "negative",
                "ci_disjoint": bool(disjoint),
                "reversal_support": support,
            })

    univ_df = pd.DataFrame(rows).sort_values("auc_abs_gap", ascending=False, na_position="last")
    univ_df.to_csv(OUT_DIR / "concept_shift_univariate_auc.csv", index=False)
    rev_df = pd.DataFrame(reversal_rows)
    rev_df.to_csv(OUT_DIR / "concept_shift_reversals.csv", index=False)

    concept_json = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "step": "step10_run_c_concept_shift",
        "population": PRIMARY_POPULATION,
        "regions": REGION_KEYS,
        "features_analyzed": ALL_NUMERIC_FEATURES,
        "n_bootstrap": N_BOOTSTRAP,
        "bootstrap_block_size_cells": CONCEPT_SHIFT_BLOCK_SIZE_CELLS,
        "per_region": per_region,
        "reversal_features": [r["feature"] for r in reversal_rows],
        "n_reversals": len(reversal_rows),
        "n_reversals_bootstrap_supported": n_bootstrap_supported,
        "n_reversals_point_only": len(reversal_rows) - n_bootstrap_supported,
        "method": (
            "Her feature icin burned'a karsi ISARETLI univariate ROC-AUC + "
            "spatial-block bootstrap %95 CI (max(auc,1-auc) YAPILMADI). Reversal: "
            "(auc_r0-0.5)*(auc_r1-0.5)<0. bootstrap_supported: iki bolgenin CI'leri "
            "AYRIK; point_reversal: nokta ters ama CI'ler ustuste biniyor."
        ),
    }
    (OUT_DIR / "concept_shift.json").write_text(
        json.dumps(concept_json, indent=2, default=str), encoding="utf-8"
    )

    print("\n" + "=" * 72)
    print(f"CONCEPT SHIFT ({PRIMARY_POPULATION}): {len(reversal_rows)} reversal "
          f"({n_bootstrap_supported} bootstrap-supported, "
          f"{len(reversal_rows) - n_bootstrap_supported} point-only)")
    print("=" * 72)
    show_cols = [c for c in univ_df.columns if c.startswith("auc_") or c in ("feature", "reversal_support")]
    print(univ_df[show_cols].to_string(index=False))
    print(f"\n[done] Cikti: {OUT_DIR}")


if __name__ == "__main__":
    main()
