"""
step10/run_a_cross_region.py  --  IS 1: Cross-region transfer

BİRİNCİL (primary) konfigürasyon: popülasyon = burnable_tree_shrub_grass
(doğal vejetasyon), RF = primary (min_samples_leaf=3, class_weight='balanced';
Emrehan/step8b ile aynı). Bu konfigürasyon ana tabloyu üretir.

Aynı raporda SENSITIVITY konfigürasyonları da yer alır (all_valid popülasyon ve/veya
eski RF msl=2). Böylece "z-score kazanımı" karışık popülasyonda mı yoksa doğal
vejetasyonda da mı ortaya çıkıyor karşılaştırılabilir (arazi-örtüsü artefaktı testi).

Her konfigürasyon: iki yön (Man->Bej, Bej->Man) x uç varyant
(raw / zscore / coral_after_regionwise_zscore) x iki feature seti (thermal [primary],
baseline). Her biri icin hedef ROC-AUC + PR-AUC ve spatial-block bootstrap %95 CI.

Ardindan REPRODÜKSİYON KONTROLÜ: birincil konfigürasyonun thermal sonuçları
Emrehan pipeline'ı ve Yunus'un bağımsız replikasyonu hedefleriyle tolerans içinde mi?
(raw ±0.03, zscore ±0.01; CORAL ±0.05.) Tutmazsa DUR ve raporla; Is2-4'e gecilmez.

Cikti:
    experiments/cross_region/step10/transfer_metrics.json
    experiments/cross_region/step10/transfer_metrics.csv
    experiments/cross_region/step10/<config>/<src>__<tgt>/predictions.parquet (+ .csv)
    experiments/cross_region/step10/reproduction_check.json  (eski: sanity_gate.json korunur)
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
    CORAL_VARIANT,
    CROSS_REGION_DIR,
    EMREHAN_TRANSFER_TARGETS,
    N_BOOTSTRAP,
    PRIMARY_POPULATION,
    REPRO_TOL_CORAL,
    REPRO_TOL_RAW,
    REPRO_TOL_ZSCORE,
    SEED,
    TARGET_COLUMN,
    THERMAL_NUMERIC,
    TRANSFER_DIRECTIONS,
    TRANSFER_RF_PROFILES,
    YUNUS_REPLICATION_TARGETS,
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

# --- Konfigürasyon grid'i: (popülasyon, RF profili, rol) ---
# PRIMARY: doğal vejetasyon + Emrehan RF. Diğerleri sensitivity.
CONFIGS = [
    {"name": "primary_burnable_rf3bal",
     "population": PRIMARY_POPULATION, "rf_profile": "primary", "role": "primary"},
    {"name": "sens_allvalid_rf3bal",
     "population": "all_valid", "rf_profile": "primary", "role": "sensitivity"},
    {"name": "sens_allvalid_rf2",
     "population": "all_valid", "rf_profile": "sensitivity", "role": "sensitivity"},
    {"name": "sens_burnable_rf2",
     "population": PRIMARY_POPULATION, "rf_profile": "sensitivity", "role": "sensitivity"},
]
PRIMARY_CONFIG_NAME = "primary_burnable_rf3bal"


def _load_regions(population: str) -> dict:
    regions = {}
    for key in {r for pair in TRANSFER_DIRECTIONS for r in pair}:
        df = load_region(key, population=population).copy()
        df["spatial_block_id"] = add_spatial_block_id(df, BOOTSTRAP_BLOCK_SIZE_CELLS).values
        regions[key] = df
    return regions


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Leakage guvenlik kontrolu (fail-fast).
    for feats in FEATURE_SETS.values():
        assert_no_leakage(feats + CATEGORICAL_FEATURES)

    # Popülasyonlari bir kez yukle (rf profilleri arasi paylas).
    populations_needed = {c["population"] for c in CONFIGS}
    regions_by_pop = {}
    for pop in populations_needed:
        regions_by_pop[pop] = _load_regions(pop)
        for key, df in regions_by_pop[pop].items():
            print(f"[load] pop={pop:26s} {key}: n={len(df)}, burned={int(df[TARGET_COLUMN].sum())}")

    flat_rows: list[dict] = []
    results: dict = {}

    for cfg in CONFIGS:
        cname = cfg["name"]
        pop = cfg["population"]
        rf_params = TRANSFER_RF_PROFILES[cfg["rf_profile"]]
        regions = regions_by_pop[pop]
        results[cname] = {
            "population": pop,
            "rf_profile": cfg["rf_profile"],
            "rf_params": {k: v for k, v in rf_params.items()},
            "role": cfg["role"],
            "n_by_region": {k: int(len(df)) for k, df in regions.items()},
            "burned_by_region": {k: int(df[TARGET_COLUMN].sum()) for k, df in regions.items()},
            "directions": {},
        }
        print(f"\n### CONFIG {cname} (role={cfg['role']}, pop={pop}, rf={cfg['rf_profile']}) ###")

        for src, tgt in TRANSFER_DIRECTIONS:
            direction = f"{src}__{tgt}"
            results[cname]["directions"][direction] = {}
            source_df = regions[src]
            target_df = regions[tgt]
            block_ids = target_df["spatial_block_id"].to_numpy()
            pred_frames: list[pd.DataFrame] = []

            for fs_name, numeric_feats in FEATURE_SETS.items():
                results[cname]["directions"][direction][fs_name] = {}
                for variant in ADAPTATION_VARIANTS:
                    out = run_transfer(
                        source_df, target_df,
                        numeric_features=numeric_feats,
                        categorical_features=CATEGORICAL_FEATURES,
                        target_col=TARGET_COLUMN,
                        variant=variant,
                        rf_params=rf_params,
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
                    results[cname]["directions"][direction][fs_name][variant] = entry
                    flat_rows.append({
                        "config": cname, "role": cfg["role"],
                        "population": pop, "rf_profile": cfg["rf_profile"],
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
                        f"[transfer] {cname:22s} | {direction} | {fs_name:8s} | {variant:28s} "
                        f"ROC-AUC={pm['roc_auc']:.4f} "
                        f"CI95=[{ci['roc_auc_ci95'][0]:.4f},{ci['roc_auc_ci95'][1]:.4f}] "
                        f"PR-AUC={pm['pr_auc']:.4f}"
                    )
                    pred_frames.append(pd.DataFrame({
                        "cell_id": target_df["cell_id"].to_numpy() if "cell_id" in target_df else range(len(target_df)),
                        "spatial_block_id": block_ids,
                        "burned": out["y_target"],
                        "feature_set": fs_name,
                        "variant": variant,
                        "y_prob": out["y_prob"],
                    }))

            # Predictions yaz (config bazli).
            dir_out = OUT_DIR / cname / direction
            dir_out.mkdir(parents=True, exist_ok=True)
            preds = pd.concat(pred_frames, ignore_index=True)
            preds.to_csv(dir_out / "predictions.csv", index=False)
            try:
                preds.to_parquet(dir_out / "predictions.parquet", index=False)
            except Exception as exc:  # noqa: BLE001
                print(f"[warn] parquet yazilamadi ({cname}/{direction}): {exc}")

    # --- REPRODÜKSİYON KONTROLÜ (birincil config, thermal set) ---
    repro = evaluate_reproduction(results[PRIMARY_CONFIG_NAME])
    print("\n" + "=" * 72)
    print("REPRODÜKSİYON (birincil = burnable + msl3 + balanced, thermal set):",
          "TUTTU" if repro["passed"] else "TUTMADI")
    for line in repro["detail_lines"]:
        print("  " + line)
    print("=" * 72)

    # --- Yaz ---
    metrics_json = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "step": "step10_run_a_cross_region_transfer",
        "seed": SEED,
        "n_bootstrap": N_BOOTSTRAP,
        "bootstrap_block_size_cells": BOOTSTRAP_BLOCK_SIZE_CELLS,
        "primary_config": PRIMARY_CONFIG_NAME,
        "configs": CONFIGS,
        "feature_sets": {k: v for k, v in FEATURE_SETS.items()},
        "categorical_features": CATEGORICAL_FEATURES,
        "variants": ADAPTATION_VARIANTS,
        "coral_variant": CORAL_VARIANT,
        "directions": [f"{s}__{t}" for s, t in TRANSFER_DIRECTIONS],
        "results": results,
        "reproduction_check": repro,
        "notes": (
            "Tum onisleme unsupervised (hedef etiketi kullanilmadi). BİRİNCİL "
            "popülasyon burnable_tree_shrub_grass (doğal vejetasyon); all_valid "
            "sensitivity. ROC/PR-AUC hedef bolgenin secili popülasyon hucrelerinde. "
            "Bootstrap birimi spatial_block_id. Sayilar oldugu gibi raporlanir."
        ),
    }
    (OUT_DIR / "transfer_metrics.json").write_text(
        json.dumps(metrics_json, indent=2, default=str), encoding="utf-8"
    )
    pd.DataFrame(flat_rows).to_csv(OUT_DIR / "transfer_metrics.csv", index=False)
    (OUT_DIR / "reproduction_check.json").write_text(
        json.dumps(repro, indent=2, default=str), encoding="utf-8"
    )
    # Geriye donuk isim (icerik = reproduction).
    (OUT_DIR / "sanity_gate.json").write_text(
        json.dumps(repro, indent=2, default=str), encoding="utf-8"
    )

    print(f"\n[done] Cikti: {OUT_DIR}")
    print("  - transfer_metrics.json / .csv")
    print("  - reproduction_check.json (+ sanity_gate.json geriye donuk)")
    print("  - <config>/<direction>/predictions.parquet (+ .csv)")


def evaluate_reproduction(primary: dict) -> dict:
    """Birincil config'in thermal ROC-AUC'lerini Emrehan + Yunus hedefleriyle
    tolerans icinde karsilastirir (raw ±0.03, zscore ±0.01 [Yunus'a karsi];
    coral ±0.05 [Emrehan'a karsi]). Tum yon/varyantlar tolerans icindeyse PASS.
    """
    detail_lines: list[str] = []
    checks: dict = {}
    all_ok = True

    for direction, dirdata in primary["directions"].items():
        thermal = dirdata["thermal"]
        emr = EMREHAN_TRANSFER_TARGETS.get(direction, {})
        yun = YUNUS_REPLICATION_TARGETS.get(direction, {})
        checks[direction] = {}
        for variant in ("raw", "zscore", CORAL_VARIANT):
            got = thermal[variant]["roc_auc"]
            if variant == CORAL_VARIANT:
                ref_name, ref = "emrehan", emr.get(variant)
                tol = REPRO_TOL_CORAL
            else:
                # Yunus replikasyonu birincil referans; yoksa Emrehan.
                if variant in yun:
                    ref_name, ref = "yunus", yun[variant]
                else:
                    ref_name, ref = "emrehan", emr.get(variant)
                tol = REPRO_TOL_RAW if variant == "raw" else REPRO_TOL_ZSCORE
            dev = abs(got - ref) if (got is not None and ref is not None) else None
            ok = dev is not None and dev <= tol
            all_ok = all_ok and ok
            checks[direction][variant] = {
                "got": got, "ref_source": ref_name, "ref": ref,
                "emrehan": emr.get(variant), "yunus": yun.get(variant),
                "tol": tol, "abs_dev": dev, "within_tol": bool(ok),
            }
            detail_lines.append(
                f"{direction} | {variant:28s} got={got:.4f} "
                f"ref({ref_name})={ref} tol=±{tol} dev={dev:.4f} -> "
                f"{'OK' if ok else 'OUT'}"
            )

    return {
        "passed": bool(all_ok),
        "primary_config": {
            "population": primary["population"],
            "rf_profile": primary["rf_profile"],
            "rf_params": primary["rf_params"],
            "n_by_region": primary["n_by_region"],
        },
        "tolerances": {
            "raw": REPRO_TOL_RAW, "zscore": REPRO_TOL_ZSCORE, "coral": REPRO_TOL_CORAL,
            "raw_zscore_ref": "yunus_independent_replication",
            "coral_ref": "emrehan_pipeline",
        },
        "checks": checks,
        "detail_lines": detail_lines,
        "action_if_failed": (
            "TUTMAZSA Is2 (decomposition), Is3 (concept-shift) ve Is4 (robustness) "
            "birincil ayarla baslatilmadan once kullaniciya raporlanip beklenir; "
            "sayi zorlanmaz."
        ),
    }


if __name__ == "__main__":
    main()
