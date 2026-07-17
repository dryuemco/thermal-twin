"""
step10/run_d_within_robustness.py  --  IS 4: Within-region robustness

step8b'nin baseline-vs-thermal spatial-block CV'sini BAGIMSIZ yeniden yazip
(within_cv.py) farkli blok boyutlarinda kosar:
    blok = 2  (~1 km, step8e ile ayni)
    blok = 10 (~5 km)
    blok = 20 (~10 km)

BİRİNCİL popülasyon = burnable_tree_shrub_grass (doğal vejetasyon); all_valid
SENSITIVITY olarak da kosulur. Her (popülasyon, blok) icin baseline vs thermal
ROC-AUC + PR-AUC ve delta_auc/delta_pr_auc'nin spatial-block bootstrap %95 CI'si.

ONCE dogrulama (blok=2): step8e'nin AYNI popülasyon degerleri +-0.02 icinde
uretiliyor mu? (sklearn surum farki nedeniyle birebir eslesme beklenmez;
sapma >0.05 ise DUR ve raporla.)

ASIL SORU: blok buyudukce termal delta_auc CI'si hala sifirin ustunde mi kaliyor?

Cikti:
    experiments/<bolge>/step10/within_robustness.json
    experiments/cross_region/step10/within_robustness_summary.csv
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

from config10 import (
    CROSS_REGION_DIR,
    EXPERIMENTS_DIR,
    N_BOOTSTRAP,
    POPULATION_RUN_ORDER,
    POPULATIONS,
    PRIMARY_POPULATION,
    REGIONS,
    SEED,
)
from data_io import add_spatial_block_id, load_region
from metrics import roc_pr
from spatial_bootstrap import delta_block_bootstrap_ci
from within_cv import run_oof

BLOCK_SIZES = [2, 10, 20]
BLOCK_KM = {2: "~1km", 10: "~5km", 20: "~10km"}
REPRO_TOL = 0.02   # basari bandi
REPRO_HARD = 0.05  # bu asilirsa DUR


def load_step8e_ref(region: str, population: str) -> dict:
    """step8e final raporundan verilen popülasyonun blok=2 (~1km) referans
    baseline/thermal ROC-AUC ve delta_auc CI'sini okur."""
    d = json.load(open(EXPERIMENTS_DIR / region / "step8e" / "final_step8_report.json"))
    b = d["step8b_baseline_vs_fused_model"][population]
    c = d["step8c_bootstrap_uncertainty"]["bootstrap_ci_by_population"][population]
    return {
        "baseline": b["overall_baseline"]["roc_auc"],
        "thermal": b["overall_thermal"]["roc_auc"],
        "delta_auc": b["delta_auc"],
        "delta_auc_ci95": c["delta_auc_ci95"],
    }


def run_population(population: str) -> tuple[dict, list[dict]]:
    """Bir popülasyon icin tum bolge/blok robustness'ini kosar."""
    all_results: dict = {}
    repro_flags: dict = {}
    summary_rows: list[dict] = []

    for region in REGIONS:
        df = load_region(region, population=population)
        all_results[region] = {}
        print(f"\n[region] {region} ({population}): n={len(df)}, burned={int(df['burned'].sum())}")

        for k in BLOCK_SIZES:
            block_ids = add_spatial_block_id(df, k).to_numpy()
            oof = run_oof(df, block_ids)
            mb = roc_pr(oof["y"], oof["oof_baseline"])
            mt = roc_pr(oof["y"], oof["oof_thermal"])
            delta_auc_point = mt["roc_auc"] - mb["roc_auc"]
            delta_pr_point = mt["pr_auc"] - mb["pr_auc"]
            dci = delta_block_bootstrap_ci(
                oof["y"], oof["oof_baseline"], oof["oof_thermal"], block_ids,
                n_bootstrap=N_BOOTSTRAP, seed=SEED,
            )
            entry = {
                "block_size_cells": k, "block_km": BLOCK_KM[k],
                "n_blocks": oof["n_blocks"], "n_splits_used": oof["n_splits_used"],
                "baseline_roc_auc": mb["roc_auc"], "thermal_roc_auc": mt["roc_auc"],
                "baseline_pr_auc": mb["pr_auc"], "thermal_pr_auc": mt["pr_auc"],
                "delta_auc_point": delta_auc_point, "delta_pr_auc_point": delta_pr_point,
                "delta_auc_ci95": dci["delta_auc_ci95"], "delta_pr_auc_ci95": dci["delta_pr_auc_ci95"],
                "delta_auc_interpretation": dci["delta_auc_interpretation"],
                "delta_pr_auc_interpretation": dci["delta_pr_auc_interpretation"],
                "delta_auc_prob_gt_0": dci["delta_auc"]["prob_gt_0"],
                "bootstrap": dci,
            }
            all_results[region][f"block_{k}"] = entry
            summary_rows.append({
                "population": population, "region": region,
                "block_size_cells": k, "block_km": BLOCK_KM[k], "n_blocks": oof["n_blocks"],
                "baseline_roc_auc": round(mb["roc_auc"], 4),
                "thermal_roc_auc": round(mt["roc_auc"], 4),
                "delta_auc": round(delta_auc_point, 4),
                "delta_auc_ci_lo": round(dci["delta_auc_ci95"][0], 4),
                "delta_auc_ci_hi": round(dci["delta_auc_ci95"][1], 4),
                "delta_auc_verdict": dci["delta_auc_interpretation"],
                "baseline_pr_auc": round(mb["pr_auc"], 4),
                "thermal_pr_auc": round(mt["pr_auc"], 4),
                "delta_pr_auc": round(delta_pr_point, 4),
                "delta_pr_auc_ci_lo": round(dci["delta_pr_auc_ci95"][0], 4),
                "delta_pr_auc_ci_hi": round(dci["delta_pr_auc_ci95"][1], 4),
                "delta_pr_auc_verdict": dci["delta_pr_auc_interpretation"],
            })
            print(
                f"  blok={k:2d} ({BLOCK_KM[k]:>6s}) n_blocks={oof['n_blocks']:5d} | "
                f"base={mb['roc_auc']:.4f} therm={mt['roc_auc']:.4f} "
                f"dAUC={delta_auc_point:+.4f} CI=[{dci['delta_auc_ci95'][0]:+.4f},"
                f"{dci['delta_auc_ci95'][1]:+.4f}] -> {dci['delta_auc_interpretation']}"
            )

        # --- blok=2 reproduction (step8e ayni popülasyon) ---
        b2 = all_results[region]["block_2"]
        ref = load_step8e_ref(region, population)
        db = abs(b2["baseline_roc_auc"] - ref["baseline"])
        dt = abs(b2["thermal_roc_auc"] - ref["thermal"])
        max_dev = max(db, dt)
        status = "PASS" if max_dev <= REPRO_TOL else ("WARN" if max_dev <= REPRO_HARD else "FAIL")
        repro_flags[region] = {
            "population": population,
            "step8e_baseline": ref["baseline"], "repro_baseline": b2["baseline_roc_auc"],
            "step8e_thermal": ref["thermal"], "repro_thermal": b2["thermal_roc_auc"],
            "baseline_abs_dev": db, "thermal_abs_dev": dt, "max_abs_dev": max_dev,
            "tolerance": REPRO_TOL, "hard_limit": REPRO_HARD, "status": status,
            "note": "sklearn 1.9 vs step8e 1.4.2; birebir eslesme beklenmez.",
        }
        print(
            f"  [repro blok=2 {population}] base {b2['baseline_roc_auc']:.4f} vs "
            f"{ref['baseline']:.4f} (dev {db:.4f}); therm {b2['thermal_roc_auc']:.4f} vs "
            f"{ref['thermal']:.4f} (dev {dt:.4f}) -> {status}"
        )

    return {"results": all_results, "repro": repro_flags}, summary_rows


def main() -> None:
    per_pop: dict = {}
    all_summary_rows: list[dict] = []

    for population in POPULATION_RUN_ORDER:
        role = "primary" if population == PRIMARY_POPULATION else "sensitivity"
        print("\n" + "#" * 72)
        print(f"# POPULATION: {population} ({role}) — {POPULATIONS[population]['label']}")
        print("#" * 72)
        data, rows = run_population(population)
        per_pop[population] = {"role": role, **data}
        all_summary_rows.extend(rows)

    # Bolge JSON'lari (her bolge icin tum popülasyonlar).
    for region in REGIONS:
        out_region = EXPERIMENTS_DIR / region / "step10"
        out_region.mkdir(parents=True, exist_ok=True)
        by_population = {
            pop: {
                "role": per_pop[pop]["role"],
                "reproduction_check_block2": per_pop[pop]["repro"][region],
                "results_by_block": per_pop[pop]["results"][region],
            }
            for pop in POPULATION_RUN_ORDER
        }
        (out_region / "within_robustness.json").write_text(
            json.dumps({
                "created_at": datetime.now(timezone.utc).isoformat(),
                "step": "step10_run_d_within_robustness",
                "region": region,
                "seed": SEED,
                "n_bootstrap": N_BOOTSTRAP,
                "primary_population": PRIMARY_POPULATION,
                "model": "RandomForest step8b params (min_samples_leaf=3, class_weight=balanced)",
                "cv": "StratifiedGroupKFold n_splits=5 shuffle random_state=42",
                "by_population": by_population,
            }, indent=2, default=str),
            encoding="utf-8",
        )

    out_cross = CROSS_REGION_DIR / "step10"
    out_cross.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(all_summary_rows).to_csv(out_cross / "within_robustness_summary.csv", index=False)

    # Hard-fail kontrolu.
    hard_fail = [(pop, r) for pop in POPULATION_RUN_ORDER
                 for r, f in per_pop[pop]["repro"].items() if f["status"] == "FAIL"]

    print("\n" + "=" * 72)
    print("IS4 REPRODUCTION (blok=2 vs step8e, popülasyon bazli):")
    for pop in POPULATION_RUN_ORDER:
        for r, f in per_pop[pop]["repro"].items():
            print(f"  {pop:26s} {r}: base dev {f['baseline_abs_dev']:.4f}, "
                  f"therm dev {f['thermal_abs_dev']:.4f} -> {f['status']}")
    if hard_fail:
        print(f"\n!! HARD FAIL (>{REPRO_HARD}): {hard_fail} -- durup raporlanmali.")
    print("=" * 72)

    print("\nBLOK BUYUDUKCE TERMAL delta_auc CI (asil soru):")
    for pop in POPULATION_RUN_ORDER:
        print(f"[{pop}]")
        for region in REGIONS:
            print(f"  {region}:")
            for k in BLOCK_SIZES:
                e = per_pop[pop]["results"][region][f"block_{k}"]
                lo, hi = e["delta_auc_ci95"]
                print(f"    blok={k:2d} ({BLOCK_KM[k]:>6s}): dAUC={e['delta_auc_point']:+.4f} "
                      f"CI=[{lo:+.4f},{hi:+.4f}] -> {e['delta_auc_interpretation']}")

    print(f"\n[done] Cikti: experiments/<bolge>/step10/within_robustness.json")
    print(f"       {out_cross / 'within_robustness_summary.csv'}")


if __name__ == "__main__":
    main()
