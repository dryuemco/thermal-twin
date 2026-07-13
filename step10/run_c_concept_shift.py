"""
step10/run_c_concept_shift.py  --  IS 3: Concept-shift kaniti

Her bolge icin her numerik feature'in burned'a karsi ISARETLI univariate
ROC-AUC'sini hesaplar. Iki bolge arasinda 0.5'in TERS taraflarina dusen
(yon reversal) feature'lari tablolar. Bu, transferin kurtarilamayan kismi
olan concept-shift'in dogrudan kanitidir.

Ek olarak her feature icin bolge bazli mean/std verilir (covariate-shift
baglami; bu kismi z-score kurtarabiliyor).

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
    CROSS_REGION_DIR,
    REGIONS,
    TARGET_COLUMN,
)
from data_io import assert_no_leakage, load_region
from metrics import univariate_signed_auc

OUT_DIR = CROSS_REGION_DIR / "step10"
REGION_KEYS = list(REGIONS.keys())  # [manavgat_2021, bejis_2022]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    assert_no_leakage(ALL_NUMERIC_FEATURES)

    per_region = {}
    for key in REGION_KEYS:
        df = load_region(key)
        y = df[TARGET_COLUMN].astype(int).to_numpy()
        feats = {}
        for f in ALL_NUMERIC_FEATURES:
            col = df[f].to_numpy(dtype="float64")
            res = univariate_signed_auc(col, y)
            feats[f] = {
                "auc": res["auc"],
                "n_used": res["n_used"],
                "mean": float(np.nanmean(col)) if np.isfinite(col).any() else None,
                "std": float(np.nanstd(col)) if np.isfinite(col).any() else None,
            }
        per_region[key] = {
            "n": int(len(df)),
            "burned": int(y.sum()),
            "features": feats,
        }
        print(f"[region] {key}: n={len(df)}, burned={int(y.sum())}")

    r0, r1 = REGION_KEYS[0], REGION_KEYS[1]

    # Univariate AUC tablosu.
    rows = []
    reversal_rows = []
    for f in ALL_NUMERIC_FEATURES:
        a0 = per_region[r0]["features"][f]["auc"]
        a1 = per_region[r1]["features"][f]["auc"]
        reversal = (
            a0 is not None and a1 is not None
            and (a0 - 0.5) * (a1 - 0.5) < 0
        )
        # Isaretli katkinin (yonun) mutlak degisimi.
        auc_gap = abs(a0 - a1) if (a0 is not None and a1 is not None) else None
        row = {
            "feature": f,
            f"auc_{r0}": a0,
            f"auc_{r1}": a1,
            "auc_abs_gap": auc_gap,
            "direction_reversal": bool(reversal),
            f"mean_{r0}": per_region[r0]["features"][f]["mean"],
            f"mean_{r1}": per_region[r1]["features"][f]["mean"],
            f"std_{r0}": per_region[r0]["features"][f]["std"],
            f"std_{r1}": per_region[r1]["features"][f]["std"],
        }
        rows.append(row)
        if reversal:
            reversal_rows.append({
                "feature": f,
                f"auc_{r0}": a0,
                f"auc_{r1}": a1,
                f"relation_{r0}": "positive" if a0 > 0.5 else "negative",
                f"relation_{r1}": "positive" if a1 > 0.5 else "negative",
            })

    univ_df = pd.DataFrame(rows).sort_values("auc_abs_gap", ascending=False, na_position="last")
    univ_df.to_csv(OUT_DIR / "concept_shift_univariate_auc.csv", index=False)

    rev_df = pd.DataFrame(reversal_rows)
    rev_df.to_csv(OUT_DIR / "concept_shift_reversals.csv", index=False)

    concept_json = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "step": "step10_run_c_concept_shift",
        "regions": REGION_KEYS,
        "features_analyzed": ALL_NUMERIC_FEATURES,
        "per_region": per_region,
        "reversal_features": [r["feature"] for r in reversal_rows],
        "n_reversals": len(reversal_rows),
        "method": (
            "Her feature icin burned'a karsi isaretli univariate ROC-AUC "
            "(max(auc,1-auc) YAPILMADI). Reversal: (auc_r0-0.5)*(auc_r1-0.5)<0, "
            "yani feature iki bolgede 0.5'in ters taraflarinda -> concept shift."
        ),
    }
    (OUT_DIR / "concept_shift.json").write_text(
        json.dumps(concept_json, indent=2, default=str), encoding="utf-8"
    )

    print("\n" + "=" * 64)
    print(f"CONCEPT SHIFT: {len(reversal_rows)} feature yon degistirdi (reversal)")
    print("=" * 64)
    print(univ_df.to_string(index=False))
    if reversal_rows:
        print("\nYon degistiren feature'lar:")
        print(rev_df.to_string(index=False))
    print(f"\n[done] Cikti: {OUT_DIR}")


if __name__ == "__main__":
    main()
