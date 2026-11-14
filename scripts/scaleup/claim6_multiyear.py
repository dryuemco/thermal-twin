"""claim6_multiyear.py: claim 6 of docs/scaleup/ANALYSIS_PLAN.md (amendment 2), multi-year MCD64A1 label.

The step8a tables keep their population and predictors; only `burned` is replaced by the multi-year
label from multiyear_label_export.py (burned share >= 0.5). Label (i) all years 2001-2023, label (ii)
2001 to the year before the fire. Everything else is analysis_official.analyse_fire unchanged.
Aggregation check: the label-window band against the step8a label (agreement, Cohen's kappa).

Run:  python claim6_multiyear.py   (writes $THERMAL_TWIN_SCALEUP/analysis/claim6_*)
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from sklearn.metrics import cohen_kappa_score

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402

MY = A.OUT / "multiyear"
LABELS = {"all_2001_2023": 0, "history_before_fire": 1, "prospective_label_start_to_2023": 3}
# band 3 is the one band of multiyear_prospective/<fire>.tif (amendment 5), stacked under the three others
MYP = A.OUT / "multiyear_prospective"
MIN_BURNED = 30


def full_table(fid):
    if fid in A.PAPER_REGIONS:
        return A.C.load(fid)
    return pd.read_parquet(A.find_scaleup(fid))


def main():
    F = A.load_fires()
    primary = [i for i in F if i != "montiferru_2021"]
    rows, bands, checks, skipped = [], [], [], []
    for fid in primary:
        with rasterio.open(MY / f"{fid}.tif") as r:
            a = r.read()
        with rasterio.open(MYP / f"{fid}.tif") as r:
            a = np.concatenate([a, r.read()], axis=0)
        full = full_table(fid)
        rr, cc = full.row_500m.to_numpy(int), full.col_500m.to_numpy(int)
        pop = (full.valid_for_modeling == True) & (full.burnable_tree_shrub_grass == True)  # noqa: E712
        win = a[2][rr, cc] >= 0.5
        y8 = full.burned.to_numpy() == 1
        checks.append({"fire": fid, "agreement": float((win[pop] == y8[pop]).mean()),
                       "kappa": float(cohen_kappa_score(y8[pop], win[pop])),
                       "window_burned": int(win[pop].sum()), "step8a_burned": int(y8[pop].sum())})
        for lab, band in LABELS.items():
            t = full.copy()
            t["burned"] = (a[band][rr, cc] >= 0.5).astype(int)
            nb = int(t.burned[pop].sum())
            if nb < MIN_BURNED or (pop.sum() - nb) < MIN_BURNED:
                skipped.append({"fire": fid, "label": lab, "burned": nb})
                continue
            f = A.Fire(f"{fid}__{lab}", t, F[fid].meta["lat"], {**F[fid].meta, "label": lab})
            try:
                row, b, _ = A.analyse_fire(f)
            except (ValueError, IndexError) as exc:   # too few blocks with burned cells, or a training fold with one class
                skipped.append({"fire": fid, "label": lab, "burned": nb, "reason": str(exc)[:120]})
                continue
            row["base_fire"], row["label"] = fid, lab
            b["base_fire"], b["label"] = fid, lab
            rows.append(row), bands.append(b)
            print(f"  {fid:28s} {lab:20s} burned {nb:6d}  null {row['auc_null_b10']:.3f}  rf {row['auc_rf_thermal_b10']:.3f}"
                  f"  cauc {row.get('cauc_rf_thermal_b10', np.nan):.3f}  rise {row['rise_rf_thermal']:.3f}", flush=True)
    FR, BR, CK = pd.DataFrame(rows), pd.concat(bands, ignore_index=True), pd.DataFrame(checks)
    FR.to_csv(A.OUT / "claim6_per_fire.csv", index=False)
    BR.to_csv(A.OUT / "claim6_bands.csv", index=False)
    CK.to_csv(A.OUT / "claim6_aggregation_check.csv", index=False)
    S = {"aggregation_check": {"agreement": A.boot_mean(CK.agreement), "kappa": A.boot_mean(CK.kappa)}, "skipped": skipped}
    for lab in LABELS:
        g = FR[FR.label == lab]
        S[lab] = {
            "fires": int(len(g)),
            "burned_share": A.boot_mean(g.prevalence),
            **{f"auc_{m}_b{k}": A.boot_mean(g[f"auc_{m}_b{k}"]) for m in ("null", "rf_thermal", "rf_baseline", "hgb_thermal") for k in (10, 20)},
            "null_beats_rf_b10": A.count(g.auc_null_b10.to_numpy(), g.auc_rf_thermal_b10.to_numpy()),
            "null_beats_rf_b20": A.count(g.auc_null_b20.to_numpy(), g.auc_rf_thermal_b20.to_numpy()),
            "cauc_rf_thermal_b10": A.boot_mean(g.cauc_rf_thermal_b10), "pwd_auc_null_b10": A.boot_mean(g.pwd_auc_null_b10),
            "rise_rf_thermal": A.boot_mean(g.rise_rf_thermal),
            "fires_positive_rise": f"{int((g.rise_rf_thermal > 0).sum())} of {int(g.rise_rf_thermal.notna().sum())}",
            "decision_multi_year_claim": (int((g.auc_null_b10 > g.auc_rf_thermal_b10).sum()) >= 28) if lab == "all_2001_2023" else None,
        }
    (A.OUT / "claim6_summary.json").write_text(json.dumps(S, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print(json.dumps(S, indent=1, ensure_ascii=False, default=float))


if __name__ == "__main__":
    main()
