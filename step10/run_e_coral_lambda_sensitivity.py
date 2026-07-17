"""
step10/run_e_coral_lambda_sensitivity.py  --  CORAL λ duyarlilik taramasi

Calismadaki TEK sansustu sonuc (Bej->Man CORAL ~0.557) CORAL regularizasyon
λ'sina ne kadar bagimli? λ ∈ {1e-5 (birincil), 1e-3, 1e-1, 1.0} icin CORAL
transferini iki yonde, thermal feature setiyle, BİRİNCİL popülasyonda (burnable)
+ msl3+balanced RF ile kosar; her biri icin spatial-block bootstrap %95 CI.

Not: ilk (yanlis) koşuda λ=1 CORAL'i ~0.485 veriyordu, λ=1e-5 ise 0.557 --
bu tablo o bagimliligi acikca gosterir. z-score referans olarak da yazilir
(λ'dan bagimsiz).

Cikti:
    experiments/cross_region/step10/coral_lambda_sensitivity.csv (+ .json)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

from config10 import (
    BOOTSTRAP_BLOCK_SIZE_CELLS,
    CATEGORICAL_FEATURES,
    CORAL_LAMBDA,
    CORAL_LAMBDA_GRID,
    CORAL_VARIANT,
    CROSS_REGION_DIR,
    N_BOOTSTRAP,
    PRIMARY_POPULATION,
    SEED,
    TARGET_COLUMN,
    THERMAL_NUMERIC,
    TRANSFER_DIRECTIONS,
    TRANSFER_RF_PARAMS_PRIMARY,
)
from data_io import add_spatial_block_id, assert_no_leakage, load_region
from metrics import roc_pr
from spatial_bootstrap import block_bootstrap_ci
from transfer import run_transfer

OUT_DIR = CROSS_REGION_DIR / "step10"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    assert_no_leakage(THERMAL_NUMERIC + CATEGORICAL_FEATURES)

    regions = {}
    for key in {r for pair in TRANSFER_DIRECTIONS for r in pair}:
        df = load_region(key, population=PRIMARY_POPULATION).copy()
        df["spatial_block_id"] = add_spatial_block_id(df, BOOTSTRAP_BLOCK_SIZE_CELLS).values
        regions[key] = df

    rows: list[dict] = []
    results: dict = {}

    for src, tgt in TRANSFER_DIRECTIONS:
        direction = f"{src}__{tgt}"
        results[direction] = {}
        source_df, target_df = regions[src], regions[tgt]
        block_ids = target_df["spatial_block_id"].to_numpy()

        # z-score referansi (λ'dan bagimsiz).
        z_out = run_transfer(
            source_df, target_df, numeric_features=THERMAL_NUMERIC,
            categorical_features=CATEGORICAL_FEATURES, target_col=TARGET_COLUMN,
            variant="zscore", rf_params=TRANSFER_RF_PARAMS_PRIMARY,
        )
        z_pm = roc_pr(z_out["y_target"], z_out["y_prob"])
        z_ci = block_bootstrap_ci(z_out["y_target"], z_out["y_prob"], block_ids,
                                  n_bootstrap=N_BOOTSTRAP, seed=SEED)
        results[direction]["zscore_reference"] = {
            "roc_auc": z_pm["roc_auc"], "roc_auc_ci95": z_ci["roc_auc_ci95"],
        }
        print(f"[{direction}] zscore(ref) ROC={z_pm['roc_auc']:.4f} "
              f"CI=[{z_ci['roc_auc_ci95'][0]:.4f},{z_ci['roc_auc_ci95'][1]:.4f}]")

        for lam in CORAL_LAMBDA_GRID:
            out = run_transfer(
                source_df, target_df, numeric_features=THERMAL_NUMERIC,
                categorical_features=CATEGORICAL_FEATURES, target_col=TARGET_COLUMN,
                variant=CORAL_VARIANT, rf_params=TRANSFER_RF_PARAMS_PRIMARY,
                coral_lambda=lam,
            )
            pm = roc_pr(out["y_target"], out["y_prob"])
            ci = block_bootstrap_ci(out["y_target"], out["y_prob"], block_ids,
                                    n_bootstrap=N_BOOTSTRAP, seed=SEED)
            lo, hi = ci["roc_auc_ci95"]
            ci_above_half = lo > 0.5
            results[direction][f"coral_lambda_{lam:g}"] = {
                "lambda": lam, "roc_auc": pm["roc_auc"], "pr_auc": pm["pr_auc"],
                "roc_auc_ci95": ci["roc_auc_ci95"], "ci_entirely_above_0.5": ci_above_half,
                "is_primary_lambda": lam == CORAL_LAMBDA,
            }
            rows.append({
                "direction": direction, "source": src, "target": tgt,
                "variant": CORAL_VARIANT, "lambda": lam,
                "is_primary_lambda": lam == CORAL_LAMBDA,
                "roc_auc": round(pm["roc_auc"], 4), "pr_auc": round(pm["pr_auc"], 4),
                "roc_auc_ci_lo": round(lo, 4), "roc_auc_ci_hi": round(hi, 4),
                "ci_entirely_above_0.5": ci_above_half,
                "zscore_reference_roc_auc": round(z_pm["roc_auc"], 4),
            })
            print(f"[{direction}] CORAL λ={lam:<6g} ROC={pm['roc_auc']:.4f} "
                  f"CI=[{lo:.4f},{hi:.4f}] {'CI>0.5' if ci_above_half else 'crosses/below 0.5'}"
                  f"{'  <-- birincil' if lam == CORAL_LAMBDA else ''}")

    pd.DataFrame(rows).to_csv(OUT_DIR / "coral_lambda_sensitivity.csv", index=False)
    (OUT_DIR / "coral_lambda_sensitivity.json").write_text(
        json.dumps({
            "created_at": datetime.now(timezone.utc).isoformat(),
            "step": "step10_run_e_coral_lambda_sensitivity",
            "population": PRIMARY_POPULATION,
            "feature_set": "thermal",
            "rf": "primary (msl=3, class_weight=balanced)",
            "primary_lambda": CORAL_LAMBDA,
            "lambda_grid": CORAL_LAMBDA_GRID,
            "seed": SEED, "n_bootstrap": N_BOOTSTRAP,
            "bootstrap_block_size_cells": BOOTSTRAP_BLOCK_SIZE_CELLS,
            "results": results,
            "note": (
                "Birincil sonuc Bej->Man CORAL'in sansustu olup olmadigi λ'ya bagli. "
                "Sonuclar oldugu gibi raporlanir."
            ),
        }, indent=2, default=str), encoding="utf-8"
    )
    print(f"\n[done] {OUT_DIR}/coral_lambda_sensitivity.csv (+ .json)")


if __name__ == "__main__":
    main()
