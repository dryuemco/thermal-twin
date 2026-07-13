"""
step10/run_a_cross_region.py  --  IS 1: Cross-region transfer

Iki yon (Man->Bej, Bej->Man) x uc varyant (raw / zscore / coral) x iki feature
seti (thermal [primary] ve baseline). Her biri icin hedef ROC-AUC + PR-AUC ve
spatial-block bootstrap %95 CI.

Ardindan SANITY GATE: prototip desenini (ham AUC < 0.5, zscore > 0.5) kontrol
eder ve sonucu raporlar. Gate tutmazsa Is2-4'e gecilmemesi gerektigi acikca
belirtilir (bu script yalniz Is1'i uretir).

Cikti:
    experiments/cross_region/step10/transfer_metrics.json
    experiments/cross_region/step10/transfer_metrics.csv
    experiments/cross_region/step10/<src>__<tgt>/predictions.parquet (+ .csv)
    experiments/cross_region/step10/sanity_gate.json
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

from config10 import (
    ADAPTATION_VARIANTS,
    BASELINE_NUMERIC,
    BOOTSTRAP_BLOCK_SIZE_CELLS,
    CATEGORICAL_FEATURES,
    CROSS_REGION_DIR,
    GATE_RAW_AUC_MAX,
    GATE_ZSCORE_AUC_MIN,
    GATE_ZSCORE_EXPECT_HIGH,
    GATE_ZSCORE_EXPECT_LOW,
    N_BOOTSTRAP,
    SEED,
    TARGET_COLUMN,
    THERMAL_NUMERIC,
    TRANSFER_DIRECTIONS,
)
from data_io import add_spatial_block_id, assert_no_leakage, load_region
from metrics import roc_pr
from spatial_bootstrap import block_bootstrap_ci
from transfer import run_transfer

OUT_DIR = CROSS_REGION_DIR / "step10"

FEATURE_SETS = {
    "thermal": THERMAL_NUMERIC,   # primary (digital-twin modeli)
    "baseline": BASELINE_NUMERIC,
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Leakage guvenlik kontrolu (fail-fast).
    for feats in FEATURE_SETS.values():
        assert_no_leakage(feats + CATEGORICAL_FEATURES)

    # Bolgeleri bir kez yukle.
    regions = {}
    for key in {r for pair in TRANSFER_DIRECTIONS for r in pair}:
        df = load_region(key)
        df = df.copy()
        df["spatial_block_id"] = add_spatial_block_id(df, BOOTSTRAP_BLOCK_SIZE_CELLS).values
        regions[key] = df
        print(f"[load] {key}: n={len(df)}, burned={int(df[TARGET_COLUMN].sum())}")

    flat_rows: list[dict] = []
    results: dict = {}

    for src, tgt in TRANSFER_DIRECTIONS:
        direction = f"{src}__{tgt}"
        results[direction] = {}
        source_df = regions[src]
        target_df = regions[tgt]
        block_ids = target_df["spatial_block_id"].to_numpy()

        pred_frames: list[pd.DataFrame] = []

        for fs_name, numeric_feats in FEATURE_SETS.items():
            results[direction][fs_name] = {}
            for variant in ADAPTATION_VARIANTS:
                out = run_transfer(
                    source_df, target_df,
                    numeric_features=numeric_feats,
                    categorical_features=CATEGORICAL_FEATURES,
                    target_col=TARGET_COLUMN,
                    variant=variant,
                )
                pm = roc_pr(out["y_target"], out["y_prob"])
                ci = block_bootstrap_ci(
                    out["y_target"], out["y_prob"], block_ids,
                    n_bootstrap=N_BOOTSTRAP, seed=SEED,
                )
                entry = {
                    "n_source": out["n_source"],
                    "n_target": out["n_target"],
                    "target_positive_count": pm["positive_count"],
                    "target_negative_count": pm["negative_count"],
                    "roc_auc": pm["roc_auc"],
                    "pr_auc": pm["pr_auc"],
                    "roc_auc_ci95": ci["roc_auc_ci95"],
                    "pr_auc_ci95": ci["pr_auc_ci95"],
                    "bootstrap": ci,
                }
                results[direction][fs_name][variant] = entry
                flat_rows.append({
                    "direction": direction, "source": src, "target": tgt,
                    "feature_set": fs_name, "variant": variant,
                    "roc_auc": pm["roc_auc"], "pr_auc": pm["pr_auc"],
                    "roc_auc_ci_lo": ci["roc_auc_ci95"][0],
                    "roc_auc_ci_hi": ci["roc_auc_ci95"][1],
                    "pr_auc_ci_lo": ci["pr_auc_ci95"][0],
                    "pr_auc_ci_hi": ci["pr_auc_ci95"][1],
                    "target_positive_count": pm["positive_count"],
                    "target_negative_count": pm["negative_count"],
                    "n_source": out["n_source"], "n_target": out["n_target"],
                })
                print(
                    f"[transfer] {direction} | {fs_name:8s} | {variant:6s} "
                    f"ROC-AUC={pm['roc_auc']:.4f} "
                    f"CI95=[{ci['roc_auc_ci95'][0]:.4f},{ci['roc_auc_ci95'][1]:.4f}] "
                    f"PR-AUC={pm['pr_auc']:.4f}"
                )

                # Tahminleri tabloya ekle (primary=thermal, tum varyantlar).
                pred_frames.append(pd.DataFrame({
                    "cell_id": target_df["cell_id"].to_numpy() if "cell_id" in target_df else range(len(target_df)),
                    "spatial_block_id": block_ids,
                    "burned": out["y_target"],
                    "feature_set": fs_name,
                    "variant": variant,
                    "y_prob": out["y_prob"],
                }))

        # Predictions yaz.
        dir_out = OUT_DIR / direction
        dir_out.mkdir(parents=True, exist_ok=True)
        preds = pd.concat(pred_frames, ignore_index=True)
        preds.to_csv(dir_out / "predictions.csv", index=False)
        try:
            preds.to_parquet(dir_out / "predictions.parquet", index=False)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] parquet yazilamadi ({direction}): {exc}")

    # --- SANITY GATE (primary feature set = thermal) ---
    gate = evaluate_gate(results)
    print("\n" + "=" * 64)
    print("SANITY GATE (Is1, feature_set=thermal):", "GECTI" if gate["passed"] else "KALDI")
    for line in gate["detail_lines"]:
        print("  " + line)
    print("=" * 64)

    # --- Yaz ---
    metrics_json = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "step": "step10_run_a_cross_region_transfer",
        "seed": SEED,
        "n_bootstrap": N_BOOTSTRAP,
        "bootstrap_block_size_cells": BOOTSTRAP_BLOCK_SIZE_CELLS,
        "feature_sets": {k: v for k, v in FEATURE_SETS.items()},
        "categorical_features": CATEGORICAL_FEATURES,
        "variants": ADAPTATION_VARIANTS,
        "directions": [f"{s}__{t}" for s, t in TRANSFER_DIRECTIONS],
        "results": results,
        "sanity_gate": gate,
        "notes": (
            "Tum onisleme unsupervised (hedef etiketi kullanilmadi). ROC/PR-AUC "
            "hedef bolgenin TUM valid_for_modeling hucrelerinde. Bootstrap birimi "
            "spatial_block_id. Sayilar oldugu gibi raporlanir."
        ),
    }
    (OUT_DIR / "transfer_metrics.json").write_text(
        json.dumps(metrics_json, indent=2, default=str), encoding="utf-8"
    )
    pd.DataFrame(flat_rows).to_csv(OUT_DIR / "transfer_metrics.csv", index=False)
    (OUT_DIR / "sanity_gate.json").write_text(
        json.dumps(gate, indent=2, default=str), encoding="utf-8"
    )

    print(f"\n[done] Cikti: {OUT_DIR}")
    print("  - transfer_metrics.json / .csv")
    print("  - sanity_gate.json")
    print("  - <direction>/predictions.parquet (+ .csv)")


def evaluate_gate(results: dict) -> dict:
    """Prototip desenini kontrol eder (feature_set=thermal):
      - ham (raw) AUC < GATE_RAW_AUC_MAX her iki yonde
      - zscore AUC > GATE_ZSCORE_AUC_MIN her iki yonde
    """
    detail_lines: list[str] = []
    raw_ok = True
    zscore_ok = True
    checks = {}

    for direction, fs in results.items():
        thermal = fs["thermal"]
        raw_auc = thermal["raw"]["roc_auc"]
        z_auc = thermal["zscore"]["roc_auc"]
        coral_auc = thermal["coral"]["roc_auc"]
        d_raw_ok = raw_auc is not None and raw_auc < GATE_RAW_AUC_MAX
        d_z_ok = z_auc is not None and z_auc > GATE_ZSCORE_AUC_MIN
        z_in_band = (
            z_auc is not None and GATE_ZSCORE_EXPECT_LOW <= z_auc <= GATE_ZSCORE_EXPECT_HIGH
        )
        raw_ok = raw_ok and d_raw_ok
        zscore_ok = zscore_ok and d_z_ok
        checks[direction] = {
            "raw_auc": raw_auc, "raw_below_0.5": d_raw_ok,
            "zscore_auc": z_auc, "zscore_above_0.5": d_z_ok,
            "zscore_in_0.55_0.57_band": z_in_band,
            "coral_auc": coral_auc,
        }
        detail_lines.append(
            f"{direction}: raw={raw_auc:.4f} (<0.5? {d_raw_ok}) | "
            f"zscore={z_auc:.4f} (>0.5? {d_z_ok}, in-band? {z_in_band}) | "
            f"coral={coral_auc:.4f}"
        )

    passed = raw_ok and zscore_ok
    return {
        "passed": bool(passed),
        "raw_below_0.5_both_directions": bool(raw_ok),
        "zscore_above_0.5_both_directions": bool(zscore_ok),
        "checks": checks,
        "thresholds": {
            "raw_auc_max": GATE_RAW_AUC_MAX,
            "zscore_auc_min": GATE_ZSCORE_AUC_MIN,
            "zscore_expected_band": [GATE_ZSCORE_EXPECT_LOW, GATE_ZSCORE_EXPECT_HIGH],
        },
        "detail_lines": detail_lines,
        "action_if_failed": (
            "Gate KALIRSA Is2 (decomposition) ve Is4 (robustness) baslatilmamali; "
            "cikti kullaniciya raporlanip beklenmeli."
        ),
    }


if __name__ == "__main__":
    main()
