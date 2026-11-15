"""tma_cell.py: the single TMA-cell attempt of plan 13.14, with the corrected pooled-forest + density comparator and the
stopping rule. Exploratory. Reuses tma_dev.py for data, calibration, targets and evaluation.
Outputs in $THERMAL_TWIN_SCALEUP/analysis/tma/dev/ (tma_cell_*).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tma_dev as D  # noqa: E402
import env_baseline as E  # noqa: E402
import baseline_explore as BX  # noqa: E402

KAPPAS = (1.0, 3.0, 10.0, 30.0, 100.0)
TAUS = (None, 8.0)
GAMMAS = (0.0, 0.25, 0.5, 1.0)
H_KM = 2.0
CELL = 0.0045814 * 111.32


def smoothed(g, col, T):
    H, W = g.row.max() + 1, g.col.max() + 1
    out = {}
    for t in range(D.T_FIRST, T):
        gt = g[(g.year == t) & (g.incomplete == 0) & g.logit_pe.notna()]
        if gt.empty:
            continue
        m = np.zeros((H, W))
        m[gt.row, gt.col] = gt[col].to_numpy()
        out[t] = ndimage.gaussian_filter(m, sigma=H_KM / CELL)
    return out


def main():
    S = D.calibrate(D.load())
    S["pe"] = 1 / (1 + np.exp(-S.logit_pe))
    groups = json.loads((HERE.parent / "scaleup" / "selection" / "site_groups.json").read_text())
    grp = {s: i for i, (_, ss) in enumerate(sorted(groups.items())) for s in ss}
    S["grp"] = S.site.map(grp)
    names = [f"c_k{k}_t{t or 'inf'}_g{gm}" for k in KAPPAS for t in TAUS for gm in GAMMAS]
    for n in names:
        S[n] = np.nan
    for site, g in S.groupby("site"):
        for T in range(D.T_FIRST + 1, 2027):
            cur = g[g.year == T]
            if cur.empty or cur.logit_pe.isna().all():
                continue
            O = smoothed(g, "y", T)
            Ex = smoothed(g, "pe", T)
            rr, cc = cur.row.to_numpy(), cur.col.to_numpy()
            for tau in TAUS:
                so = sum(((1.0 if tau is None else np.exp(-(T - t) / tau)) * O[t]) for t in O) if O else 0
                se = sum(((1.0 if tau is None else np.exp(-(T - t) / tau)) * Ex[t]) for t in Ex) if Ex else 0
                for k in KAPPAS:
                    lrr = np.log((np.asarray(so)[rr, cc] + k) / (np.asarray(se)[rr, cc] + k)) if O else np.zeros(len(cur))
                    for gm in GAMMAS:
                        S.loc[cur.index, f"c_k{k}_t{tau or 'inf'}_g{gm}"] = cur.logit_pe.to_numpy() + gm * lrr
        print(site, "TMA-cell", flush=True)
    TRg = D.transitions(S, names)
    TRg = TRg[TRg.target == "all"]
    TRg["grp"] = TRg.site.map(grp)
    S["tma_cell"] = np.nan
    log = []
    for (gidx, T), cur in S.groupby(["grp", "year"]):
        h = TRg[(TRg.grp != gidx) & (TRg.year <= T - 1)]
        if h.empty:
            continue
        best = max(names, key=lambda n: h[n].mean())
        S.loc[cur.index, "tma_cell"] = S.loc[cur.index, best]
        log.append({"grp": int(gidx), "T": int(T), "choice": best, "estimated_auc": float(h[best].mean())})
    # corrected comparator: pooled forest + density rank within the site-year
    P = BX.add_extra(E.load())
    P = P[P.year >= D.T_FIRST - 1].merge(S[["site", "year", "row", "col", "density_h2_tauinf"]], on=["site", "year", "row", "col"], how="left")
    P["density_rank"] = P.groupby(["site", "year"]).density_h2_tauinf.rank(pct=True)
    P["grp"] = P.site.map(grp)
    TS = E.training_sample(P)
    TS["grp"] = TS.site.map(grp)
    P["pooled_density_rank"] = BX.pooled_scores(P, TS, E.FEATS + ["months_since_burn", "density_rank"])
    S = S.merge(P[["site", "year", "row", "col", "pooled_density_rank"]], on=["site", "year", "row", "col"], how="left")
    prev = pd.read_parquet(D.OUT / "tma_scores.parquet", columns=["site", "year", "row", "col", "tma", "standard_spatial", "coord_dist_forest"])
    S = S.merge(prev, on=["site", "year", "row", "col"], how="left")
    S["f_only"] = S.logit_pe
    S["density"] = S.density_h2_tauinf
    cols = ["tma_cell", "tma", "f_only", "density", "pooled_density_rank", "standard_spatial", "coord_dist_forest"]
    TR = D.transitions(S, cols)
    LT = D.later(S, cols)
    TR.to_csv(D.OUT / "tma_cell_transitions.csv", index=False)
    LT.to_csv(D.OUT / "tma_cell_later.csv", index=False)
    pd.DataFrame(log).to_csv(D.OUT / "tma_cell_gate_log.csv", index=False)
    summ = {}
    for name, Dd in (("transitions", TR), ("later", LT)):
        for keys, g in Dd.groupby(["target"] + (["horizon"] if name == "later" else [])):
            kk = name + "_" + "_".join(map(str, keys if isinstance(keys, tuple) else (keys,)))
            cc = g.dropna(subset=cols)
            summ[kk] = {"n_common": int(len(cc)), **{c: float(cc[c].mean()) for c in cols}}
    t = TR[TR.target == "all"].dropna(subset=["tma_cell", "density"])
    diff = float((t.tma_cell - t.density).mean())
    summ["stopping_rule"] = {"site_years": int(len(t)), "tma_cell_minus_density": diff, "continue": bool(diff >= 0.01)}
    gl = pd.DataFrame(log)
    hon = []
    for r in gl.itertuples():
        real = TR[(TR.target == "all") & (TR.year == r.T) & TR.site.map(grp).eq(r.grp)].tma_cell
        if len(real):
            hon.append(r.estimated_auc - real.mean())
    summ["honesty_gate_estimated_minus_realised"] = float(np.mean(hon)) if hon else None
    (D.OUT / "tma_cell_summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
