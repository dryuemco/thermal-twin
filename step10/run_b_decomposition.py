"""
step10/run_b_decomposition.py  --  IS 2: Decomposition raporu

Her hedef bolge icin transfer basarisizligini bilesenlerine ayirir:

    within   = o bolgenin KENDI within-region thermal ROC-AUC'si (step8e)
    raw      = o bolgeye NAIF (ham) transfer AUC (Is1)
    adapted  = o bolgeye ADAPTE (z-score / CORAL) transfer AUC (Is1)

    total_gap          = within - raw        (toplam transfer kaybi)
    recovered          = adapted - raw       (adaptasyonun kurtardigi kisim)
    concept_remaining  = within - adapted    (kalan = concept shift)

Kaynaklar (mevcut dosyalar; SADECE okunur):
    experiments/<bolge>/step8e/final_step8_report.json  (within)
    experiments/cross_region/step10/transfer_metrics.json  (Is1 ciktisi)

Cikti:
    experiments/cross_region/step10/decomposition.json
    experiments/cross_region/step10/decomposition.csv
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

from config10 import CROSS_REGION_DIR, EXPERIMENTS_DIR, TRANSFER_DIRECTIONS

OUT_DIR = CROSS_REGION_DIR / "step10"
ADAPTED_VARIANTS = ["zscore", "coral"]  # zscore primary


def load_within(region: str) -> dict:
    d = json.load(open(EXPERIMENTS_DIR / region / "step8e" / "final_step8_report.json"))
    b = d["step8b_baseline_vs_fused_model"]["all_valid"]
    c = d["step8c_bootstrap_uncertainty"]["bootstrap_ci_by_population"]["all_valid"]
    return {
        "within_baseline_auc": b["overall_baseline"]["roc_auc"],
        "within_thermal_auc": b["overall_thermal"]["roc_auc"],
        "within_delta_auc": b["delta_auc"],
        "within_delta_auc_ci95": c["delta_auc_ci95"],
    }


def main() -> None:
    transfer = json.load(open(OUT_DIR / "transfer_metrics.json"))
    tr = transfer["results"]

    rows: list[dict] = []
    decomp: dict = {}

    for src, tgt in TRANSFER_DIRECTIONS:
        direction = f"{src}__{tgt}"
        within = load_within(tgt)  # decomposition hedef bolgenin within'ine gore
        w = within["within_thermal_auc"]
        raw = tr[direction]["thermal"]["raw"]["roc_auc"]
        total_gap = w - raw

        decomp[tgt] = {
            "target_region": tgt,
            "source_region": src,
            "direction": direction,
            "within_thermal_auc": w,
            "within_delta_auc": within["within_delta_auc"],
            "within_delta_auc_ci95": within["within_delta_auc_ci95"],
            "raw_transfer_auc": raw,
            "total_gap_within_minus_raw": total_gap,
            "adaptations": {},
        }

        for variant in ADAPTED_VARIANTS:
            adapted = tr[direction]["thermal"][variant]["roc_auc"]
            recovered = adapted - raw
            concept_remaining = w - adapted
            frac_recovered = recovered / total_gap if total_gap else None
            frac_concept = concept_remaining / total_gap if total_gap else None
            decomp[tgt]["adaptations"][variant] = {
                "adapted_transfer_auc": adapted,
                "recovered_adapted_minus_raw": recovered,
                "concept_remaining_within_minus_adapted": concept_remaining,
                "fraction_recovered": frac_recovered,
                "fraction_concept_remaining": frac_concept,
            }
            rows.append({
                "target_region": tgt, "source_region": src, "adaptation": variant,
                "within_thermal_auc": round(w, 4),
                "raw_transfer_auc": round(raw, 4),
                "adapted_transfer_auc": round(adapted, 4),
                "total_gap": round(total_gap, 4),
                "recovered": round(recovered, 4),
                "concept_remaining": round(concept_remaining, 4),
                "fraction_recovered": round(frac_recovered, 4) if frac_recovered is not None else None,
                "fraction_concept_remaining": round(frac_concept, 4) if frac_concept is not None else None,
            })
            print(
                f"[decomp] target={tgt:14s} adapt={variant:6s} | "
                f"within={w:.4f} raw={raw:.4f} adapted={adapted:.4f} | "
                f"gap={total_gap:.4f} recovered={recovered:+.4f} "
                f"({frac_recovered:.0%}) concept={concept_remaining:+.4f} "
                f"({frac_concept:.0%})"
            )

    out = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "step": "step10_run_b_decomposition",
        "definition": {
            "within": "target region's own within-region thermal ROC-AUC (step8e)",
            "raw": "naive cross-region transfer into target (Is1)",
            "adapted": "adapted (z-score/CORAL) cross-region transfer into target (Is1)",
            "total_gap": "within - raw",
            "recovered": "adapted - raw (covariate-shift, self-calibration kurtardigi)",
            "concept_remaining": "within - adapted (kurtarilamayan concept shift)",
        },
        "primary_adaptation": "zscore",
        "by_target_region": decomp,
    }
    (OUT_DIR / "decomposition.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    pd.DataFrame(rows).to_csv(OUT_DIR / "decomposition.csv", index=False)

    print(f"\n[done] Cikti: {OUT_DIR}/decomposition.json (+ .csv)")


if __name__ == "__main__":
    main()
