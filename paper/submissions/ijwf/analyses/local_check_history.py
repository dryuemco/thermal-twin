#!/usr/bin/env python3
"""local_check_history.py: does a check against earlier local burns tell how a borrowed model will do?

Exploratory analysis added for the IJWF package on 2026-11-11, after the reviewer simulation pointed out
that the paper recommends checking a transferred model against a local burned-area record without having
tried it. It uses only data that exist before the fire season of the target region: the cells that
MCD64A1 marks as burned in the five complete calendar years before the event year (the flags of
paper/labelfix_rerun/labels/r2_history_cells_<region>.csv, the same cells as Supplementary Table S12).

For every transfer direction into a target with earlier burns, the source model (thermal feature set,
the classifier and preprocessing of the main text, no target label) scores the target cells once. The
scores are then compared with two labels: the earlier burns (the check, available before the fire) and
the event of the paper (the outcome). The question is whether the first AUC predicts the second.

Reproduction gate: the event AUC of every one of the twenty directions must equal the raw column of
Supplementary Table S8 to within 0.0015, otherwise nothing is written.

Run with the paper's environment (scikit-learn 1.9.0):
    <venv>/python paper/submissions/ijwf/analyses/local_check_history.py
Reads paper/data and paper/labelfix_rerun (read-only). Writes local_check_history.json and .csv here.
"""
import json
import re
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from scipy.stats import spearmanr
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[2]
sys.path.insert(0, str(PAPER / "code"))
import _canonical  # noqa: E402

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
        "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}
TH = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant", "lst_anomaly_mean",
      "current_lst_mean", "current_tvdi_mean", "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
CAT = "landcover_dominant"
HIST = PAPER / "labelfix_rerun" / "labels" / "r2_history_cells_{}.csv"
SUPP = HERE.parent / "text" / "supplementary.md"
MIN_HIST, NBOOT, SEED, GATE = 50, 2000, 42, 0.0015


def build():
    num = [f for f in TH if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
          ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT])]
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight="balanced",
                                                    random_state=42, n_jobs=4))])


def load(reg):
    d = _canonical.load(reg, columns=["cell_id", "burned", "valid_for_modeling", "burnable_tree_shrub_grass"] + TH)
    d = d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
    h = pd.read_csv(str(HIST).format(reg))
    d["hist5"] = d.cell_id.isin(set(h.loc[h.hist5 == True, "cell_id"])).astype(int)  # noqa: E712
    return d


def table_s8():
    """The raw column of Supplementary Table S8, as printed."""
    text = SUPP.read_text(encoding="utf-8")
    rev = {v: k for k, v in NAME.items()}
    out = {}
    for s, t, v in re.findall(r"(?m)^\| (\w+)→(\w+) \| (\d\.\d{3}) \[", text):
        out[(rev[s], rev[t])] = float(v)
    assert len(out) == 20, f"{len(out)} directions read from Table S8"
    return out


def pair_boot(df, x, y):
    """Spearman's rho with the pair-cluster bootstrap of the main text: unordered region pairs are
    resampled with replacement and carry the directions they contain."""
    rng = np.random.default_rng(SEED)
    pairs = [frozenset(p) for p in combinations(REGIONS, 2)]
    by_pair = {p: df[[frozenset((s, t)) == p for s, t in zip(df.source, df.target)]] for p in pairs}
    rhos = []
    for _ in range(NBOOT):
        take = [by_pair[pairs[i]] for i in rng.integers(0, len(pairs), len(pairs))]
        b = pd.concat(take)
        if len(b) >= 3 and b[x].nunique() > 1 and b[y].nunique() > 1:
            rhos.append(spearmanr(b[x], b[y]).statistic)
    return float(np.percentile(rhos, 2.5)), float(np.percentile(rhos, 97.5)), len(rhos)


data = {r: load(r) for r in REGIONS}
for r in REGIONS:
    _canonical.assert_no_leakage(TH)
models = {r: build().fit(data[r][TH], data[r].burned) for r in REGIONS}
s8, rows = table_s8(), []
for s in REGIONS:
    for t in REGIONS:
        if s == t:
            continue
        d = data[t]
        score = models[s].predict_proba(d[TH])[:, 1]
        event = roc_auc_score(d.burned, score)
        assert abs(event - s8[(s, t)]) <= GATE, f"{s}->{t}: {event:.4f} here, {s8[(s, t)]:.3f} in Table S8"
        n_hist = int(d.hist5.sum())
        row = {"source": s, "target": t, "auc_event": event, "hist_cells": n_hist,
               "hist_also_event": int(((d.hist5 == 1) & (d.burned == 1)).sum())}
        if n_hist >= MIN_HIST:
            row["auc_hist"] = roc_auc_score(d.hist5, score)
            keep = d.burned == 0                                      # the earlier burns that did not burn again
            row["auc_hist_event_cells_removed"] = roc_auc_score(d.hist5[keep], score[keep])
        rows.append(row)
df = pd.DataFrame(rows)
print(f"reproduction gate passed: 20 directions within {GATE} of Table S8 (scikit-learn {sklearn.__version__})")

use = df.dropna(subset=["auc_hist"]).copy()
rho = spearmanr(use.auc_hist, use.auc_event).statistic
lo, hi, nb = pair_boot(use, "auc_hist", "auc_event")
rho2 = spearmanr(use.auc_hist_event_cells_removed, use.auc_event).statistic
lo2, hi2, _ = pair_boot(use, "auc_hist_event_cells_removed", "auc_event")
same_side = int(((use.auc_hist > 0.5) == (use.auc_event > 0.5)).sum())
targets = {}
for t, g in use.groupby("target"):
    pick = g.loc[g.auc_hist.idxmax()]
    targets[t] = {"hist_cells": int(g.hist_cells.iloc[0]), "hist_also_event": int(g.hist_also_event.iloc[0]),
                  "picked_source": pick.source, "picked_auc_event": float(pick.auc_event),
                  "mean_auc_event": float(g.auc_event.mean()), "best_auc_event": float(g.auc_event.max()),
                  "best_source": g.loc[g.auc_event.idxmax(), "source"],
                  "within_target_rho": float(spearmanr(g.auc_hist, g.auc_event).statistic)}
summary = {
    "analysis": "check of transferred thermal models against the burns of the five previous years",
    "date": "2026-11-11", "status": "exploratory, added after the reviewer simulation",
    "environment": {"scikit-learn": sklearn.__version__, "pandas": pd.__version__, "numpy": np.__version__},
    "reproduction_gate": f"all 20 raw transfer AUCs within {GATE} of Supplementary Table S8",
    "min_hist_cells": MIN_HIST, "directions_used": int(len(use)),
    "targets_used": sorted(targets), "targets_without_earlier_burns": sorted(set(REGIONS) - set(targets)),
    "spearman_hist_vs_event": {"rho": float(rho), "ci95": [lo, hi], "bootstrap": "pair-cluster", "replicates": nb, "seed": SEED},
    "spearman_hist_vs_event_event_cells_removed": {"rho": float(rho2), "ci95": [lo2, hi2]},
    "same_side_of_chance": {"count": same_side, "of": int(len(use))},
    "mean_auc_hist": float(use.auc_hist.mean()), "mean_auc_event": float(use.auc_event.mean()),
    "source_picked_by_check": targets,
    "picked_minus_mean_event_auc": float(np.mean([v["picked_auc_event"] - v["mean_auc_event"] for v in targets.values()])),
    "picked_is_best": int(sum(v["picked_source"] == v["best_source"] for v in targets.values())),
}
df.to_csv(HERE / "local_check_history.csv", index=False, float_format="%.6f")
(HERE / "local_check_history.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
print(use[["source", "target", "hist_cells", "auc_hist", "auc_hist_event_cells_removed", "auc_event"]].round(3).to_string(index=False))
print(json.dumps({k: summary[k] for k in ("spearman_hist_vs_event", "spearman_hist_vs_event_event_cells_removed",
                                          "same_side_of_chance", "mean_auc_hist", "mean_auc_event",
                                          "picked_minus_mean_event_auc", "picked_is_best")}, indent=1))
print(json.dumps(targets, indent=1, ensure_ascii=False))
