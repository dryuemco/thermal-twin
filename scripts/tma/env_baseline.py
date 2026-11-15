"""env_baseline.py: TMA checkpoint 3, the environmental baseline f(X) (plan 13.2.5 and 13.11). Exploratory.

For every target year T (2004-2026) and site group g (five fixed groups of sites), a random forest is trained on
the sites outside g and target years u <= T - 1, with equal total weight per site (negatives subsampled to
NEG_CAP per site-year and re-weighted), and predicts the sites of g at T. Groups are geographic
(selection/site_groups.json). Predictors: within-site-year z-scores of
ndvi, evi, lst_day and lst_night; their anomalies against earlier years; within-site z-scores of elevation and
slope; burn history (years since burn, censoring flag, burns in 10 years, fuel deficit). No location. A Platt map
fitted on out-of-group predictions of earlier target years calibrates the scores.

Outputs ($THERMAL_TWIN_SCALEUP/analysis/tma): env_scores.parquet (site, year, row, col, y, f_raw, f_cal),
env_baseline_transitions.csv (AUC per site-year with >= 30 positives), env_baseline_later.csv (the first-May map
after the focal fire against later burning), env_baseline_summary.json.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "geonull"))
sys.path.insert(0, str(HERE.parent / "scaleup"))
import geonull as G  # noqa: E402

ROOT = Path(os.environ["THERMAL_TWIN_SCALEUP"]) / "analysis" / "tma"
NEG_CAP, SEED, GROUPS = 1500, 42, 5
ZCOLS = ["ndvi", "evi", "lst_day", "lst_night"]
FEATS = [f"{c}_z" for c in ZCOLS] + ["lst_day_anom", "lst_night_anom", "ndvi_anom", "elevation_z", "slope_z",
                                    "years_since_burn", "censored", "burns_10y", "fuel_deficit"]


def load():
    P = pd.read_parquet(ROOT / "panel.parquet")
    g = P.groupby(["site", "year"])
    for c in ZCOLS:
        P[f"{c}_z"] = (P[c] - g[c].transform("mean")) / g[c].transform("std").replace(0, 1)
    gs = P.groupby("site")
    for c in ("elevation", "slope"):
        P[f"{c}_z"] = (P[c] - gs[c].transform("mean")) / gs[c].transform("std").replace(0, 1)
    return P


def training_sample(P):
    rng = np.random.default_rng(SEED)
    parts = []
    for (s, y), g in P.groupby(["site", "year"]):
        if g.incomplete.iloc[0]:
            continue
        pos, neg = g[g.y == 1], g[g.y == 0]
        k = min(NEG_CAP, len(neg))
        negs = neg.iloc[rng.choice(len(neg), k, replace=False)] if k else neg
        w_neg = len(neg) / max(k, 1)
        parts.append(pd.concat([pos.assign(w=1.0), negs.assign(w=w_neg)]))
    T = pd.concat(parts, ignore_index=True)
    T["w"] = T.w / T.groupby("site").w.transform("sum")          # equal total weight per site
    return T


def main():
    P = load()
    groups = json.loads((HERE.parent / "scaleup" / "selection" / "site_groups.json").read_text())
    grp = {s: i for i, (_, ss) in enumerate(sorted(groups.items())) for s in ss}
    assert set(grp) == set(P.site.unique()), "site groups do not cover the panel sites"
    P["grp"] = P.site.map(grp)
    TS = training_sample(P)
    TS["grp"] = TS.site.map(grp)
    years = range(2004, 2027)
    raw = np.full(len(P), np.nan)
    for T in years:
        for g in range(GROUPS):
            tr = TS[(TS.grp != g) & (TS.year <= T - 1)]
            te = (P.grp == g) & (P.year == T)
            if not te.any() or tr.y.sum() < 50:
                continue
            m = RandomForestClassifier(300, min_samples_leaf=5, max_features="sqrt", random_state=SEED, n_jobs=30)
            m.fit(tr[FEATS].fillna(-999), tr.y, sample_weight=tr.w)
            raw[te.to_numpy()] = m.predict_proba(P.loc[te, FEATS].fillna(-999))[:, 1]
        print(T, "done", flush=True)
    P["f_raw"] = raw
    # Platt calibration from out-of-group predictions of earlier target years only
    cal = np.full(len(P), np.nan)
    eps = 1e-4
    for T in years:
        hist = P[(P.year < T) & P.f_raw.notna() & (P.incomplete == 0)]
        cur = (P.year == T) & P.f_raw.notna()
        if len(hist) < 1000 or hist.y.sum() < 50:
            continue
        x = np.log(np.clip(hist.f_raw, eps, 1 - eps) / (1 - np.clip(hist.f_raw, eps, 1 - eps)))
        lr = LogisticRegression().fit(x.to_numpy()[:, None], hist.y)
        xc = np.log(np.clip(P.loc[cur, "f_raw"], eps, 1 - eps) / (1 - np.clip(P.loc[cur, "f_raw"], eps, 1 - eps)))
        cal[cur.to_numpy()] = lr.predict_proba(xc.to_numpy()[:, None])[:, 1]
    P["f_cal"] = cal
    P[["site", "year", "row", "col", "y", "f_raw", "f_cal", "incomplete"]].to_parquet(ROOT / "env_scores.parquet", index=False)
    # transitions: AUC within each complete site-year with >= 30 positives
    tr_rows = []
    for (s, y), g in P[P.f_raw.notna() & (P.incomplete == 0)].groupby(["site", "year"]):
        if g.y.sum() >= 30 and (1 - g.y).sum() >= 30:
            tr_rows.append({"site": s, "year": y, "auc": G.auc(g.y, g.f_raw), "positives": int(g.y.sum())})
    TR = pd.DataFrame(tr_rows)
    TR.to_csv(ROOT / "env_baseline_transitions.csv", index=False)
    print("transitions", len(TR), "mean AUC", round(TR.auc.mean(), 3))
    later(P, TR)


def later(P, TR):
    sys.path.insert(0, str(HERE.parent / "scaleup"))
    from s2_label_check_export import regions
    rows = []
    for s, g in P.groupby("site"):
        fy = int(regions.EXPERIMENTS[s]["label_start_date"][:4])
        T0 = fy + 1
        m = g[g.year == T0].set_index(["row", "col"])
        scar = g[(g.year == fy) & (g.y == 1)].set_index(["row", "col"]).index
        m = m[~m.index.isin(scar)]
        fut = g[g.year >= T0].groupby(["row", "col"]).y
        r = {"site": s, "focal_year": fy, "T0": T0, "cells": len(m)}
        for name, lo, hi in (("all", T0, 2026), ("to2022", T0, 2022), ("from2023", 2023, 2026), ("two_year", T0, T0 + 1)):
            lab = g[(g.year >= lo) & (g.year <= hi)].groupby(["row", "col"]).y.max().reindex(m.index).fillna(0)
            ok = lab.sum() >= 30 and (1 - lab).sum() >= 30
            r[f"auc_{name}"] = G.auc(lab, m.f_raw) if ok else np.nan
            r[f"pos_{name}"] = int(lab.sum())
        past = TR[(TR.site == s) & (TR.year < T0)]
        oth = TR[(TR.site != s) & (TR.year < T0)]
        r["estimated_own_past"] = float(past.auc.mean()) if len(past) else np.nan
        r["estimated_other_sites"] = float(oth.auc.mean()) if len(oth) else np.nan
        rows.append(r)
    L = pd.DataFrame(rows)
    L["low_overlap"] = L.site.isin(["px23_2023", "px17_2022", "px14_2022", "px25_2017"])
    L.to_csv(ROOT / "env_baseline_later.csv", index=False)
    S = {k: {"mean": float(L[k].mean()), "n": int(L[k].notna().sum())} for k in ("auc_all", "auc_to2022", "auc_from2023", "auc_two_year")}
    S["transitions_mean_auc"] = float(TR.auc.mean())
    S["transitions_n"] = int(len(TR))
    g = L.dropna(subset=["auc_all", "estimated_other_sites"])
    S["honesty_other_sites_minus_realised"] = float((g.estimated_other_sites - g.auc_all).mean())
    g = L.dropna(subset=["auc_all", "estimated_own_past"])
    S["honesty_own_past_minus_realised"] = float((g.estimated_own_past - g.auc_all).mean())
    S["honesty_n"] = int(len(g))
    (ROOT / "env_baseline_summary.json").write_text(json.dumps(S, indent=1), encoding="utf-8")
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
