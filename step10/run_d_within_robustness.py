"""
step10/run_d_within_robustness.py  --  IS 4: Within-region robustness

step8b'nin baseline-vs-thermal spatial-block CV'sini BAGIMSIZ yeniden yazip
(within_cv.py) farkli blok boyutlarinda kosar:
    blok = 2  (~1 km, step8e ile ayni)
    blok = 10 (~5 km)
    blok = 20 (~10 km)
Iki bolge (Manavgat, Bejis) icin baseline vs thermal ROC-AUC + PR-AUC ve
delta_auc/delta_pr_auc'nin spatial-block bootstrap %95 CI'si.

ONCE dogrulama: blok=2'de Manavgat baseline ~0.83 / thermal ~0.87 (step8e)
+-0.02 icinde uretiliyor mu? (sklearn surum farki nedeniyle birebir eslesme
beklenmez; sapma >0.05 ise DUR ve raporla.)

ASIL SORU: blok buyudukce termal delta_auc CI'si hala sifirin ustunde mi
kaliyor, yoksa sifiri kesmeye mi basliyor? Sonuc oldugu gibi raporlanir.

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
    REGIONS,
    SEED,
)
from data_io import add_spatial_block_id, load_region
from metrics import roc_pr
from spatial_bootstrap import delta_block_bootstrap_ci
from within_cv import run_oof

BLOCK_SIZES = [2, 10, 20]
BLOCK_KM = {2: "~1km", 10: "~5km", 20: "~10km"}

# step8e referans degerleri (sklearn 1.4.2 ile uretildi); blok=2 dogrulama.
STEP8E_REF = {
    "manavgat_2021": {"baseline": 0.8277, "thermal": 0.8866, "delta_auc": 0.0589,
                      "delta_auc_ci95": [0.0490, 0.0684]},
    "bejis_2022": {"baseline": 0.8688, "thermal": 0.9171, "delta_auc": 0.0482,
                   "delta_auc_ci95": [0.0398, 0.0571]},
}
REPRO_TOL = 0.02   # basari bandi
REPRO_HARD = 0.05  # bu asilirsa DUR


def main() -> None:
    summary_rows: list[dict] = []
    all_results: dict = {}
    repro_flags: dict = {}

    for region in REGIONS:
        df = load_region(region)
        all_results[region] = {}
        print(f"\n[region] {region}: n={len(df)}, burned={int(df['burned'].sum())}")

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
                "block_size_cells": k,
                "block_km": BLOCK_KM[k],
                "n_blocks": oof["n_blocks"],
                "n_splits_used": oof["n_splits_used"],
                "baseline_roc_auc": mb["roc_auc"],
                "thermal_roc_auc": mt["roc_auc"],
                "baseline_pr_auc": mb["pr_auc"],
                "thermal_pr_auc": mt["pr_auc"],
                "delta_auc_point": delta_auc_point,
                "delta_pr_auc_point": delta_pr_point,
                "delta_auc_ci95": dci["delta_auc_ci95"],
                "delta_pr_auc_ci95": dci["delta_pr_auc_ci95"],
                "delta_auc_interpretation": dci["delta_auc_interpretation"],
                "delta_pr_auc_interpretation": dci["delta_pr_auc_interpretation"],
                "delta_auc_prob_gt_0": dci["delta_auc"]["prob_gt_0"],
                "bootstrap": dci,
            }
            all_results[region][f"block_{k}"] = entry
            summary_rows.append({
                "region": region, "block_size_cells": k, "block_km": BLOCK_KM[k],
                "n_blocks": oof["n_blocks"],
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

        # --- blok=2 reproduction kontrolu ---
        b2 = all_results[region]["block_2"]
        ref = STEP8E_REF[region]
        db = abs(b2["baseline_roc_auc"] - ref["baseline"])
        dt = abs(b2["thermal_roc_auc"] - ref["thermal"])
        max_dev = max(db, dt)
        status = "PASS" if max_dev <= REPRO_TOL else ("WARN" if max_dev <= REPRO_HARD else "FAIL")
        repro_flags[region] = {
            "step8e_baseline": ref["baseline"], "repro_baseline": b2["baseline_roc_auc"],
            "step8e_thermal": ref["thermal"], "repro_thermal": b2["thermal_roc_auc"],
            "baseline_abs_dev": db, "thermal_abs_dev": dt, "max_abs_dev": max_dev,
            "tolerance": REPRO_TOL, "hard_limit": REPRO_HARD, "status": status,
            "note": "sklearn 1.9 vs step8e 1.4.2; birebir eslesme beklenmez.",
        }
        print(
            f"  [repro blok=2] base {b2['baseline_roc_auc']:.4f} vs {ref['baseline']} "
            f"(dev {db:.4f}); therm {b2['thermal_roc_auc']:.4f} vs {ref['thermal']} "
            f"(dev {dt:.4f}) -> {status}"
        )

        # Bolge JSON'i yaz.
        out_region = EXPERIMENTS_DIR / region / "step10"
        out_region.mkdir(parents=True, exist_ok=True)
        (out_region / "within_robustness.json").write_text(
            json.dumps({
                "created_at": datetime.now(timezone.utc).isoformat(),
                "step": "step10_run_d_within_robustness",
                "region": region,
                "seed": SEED,
                "n_bootstrap": N_BOOTSTRAP,
                "model": "RandomForest step8b params (min_samples_leaf=3, class_weight=balanced)",
                "cv": "StratifiedGroupKFold n_splits=5 shuffle random_state=42",
                "reproduction_check_block2": repro_flags[region],
                "results_by_block": all_results[region],
            }, indent=2, default=str),
            encoding="utf-8",
        )

    # --- Ozet CSV + kombine JSON ---
    out_cross = CROSS_REGION_DIR / "step10"
    out_cross.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).to_csv(out_cross / "within_robustness_summary.csv", index=False)

    # Hard-fail kontrolu (>0.05 sapma).
    hard_fail = [r for r, f in repro_flags.items() if f["status"] == "FAIL"]

    print("\n" + "=" * 72)
    print("IS4 REPRODUCTION (blok=2 vs step8e):")
    for r, f in repro_flags.items():
        print(f"  {r}: base dev {f['baseline_abs_dev']:.4f}, therm dev "
              f"{f['thermal_abs_dev']:.4f} -> {f['status']}")
    if hard_fail:
        print(f"\n!! HARD FAIL (>{REPRO_HARD}): {hard_fail} -- durup raporlanmali.")
    print("=" * 72)

    print("\nBLOK BUYUDUKCE TERMAL delta_auc CI (asil soru):")
    for region in REGIONS:
        print(f"  {region}:")
        for k in BLOCK_SIZES:
            e = all_results[region][f"block_{k}"]
            lo, hi = e["delta_auc_ci95"]
            print(f"    blok={k:2d} ({BLOCK_KM[k]:>6s}): dAUC={e['delta_auc_point']:+.4f} "
                  f"CI=[{lo:+.4f},{hi:+.4f}] -> {e['delta_auc_interpretation']}")

    print(f"\n[done] Cikti: experiments/<bolge>/step10/within_robustness.json")
    print(f"       {out_cross / 'within_robustness_summary.csv'}")


if __name__ == "__main__":
    main()
