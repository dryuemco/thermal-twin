"""session_20261118_checks.py: exploratory numbers quoted in docs/scaleup/SESSION_HANDOFF_20261118.md.

Reads only committed result files; fits nothing. Run from the repository root:
    python scripts/explore/session_20261118_checks.py
Needs pandas and numpy. Everything printed here is exploratory (development data, seen results).
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2] / "results"
TR = ROOT / "tma" / "dev" / "tma_cell_transitions.csv"
C9 = ROOT / "scaleup" / "claim9" / "claim9_synthetic_runs.csv"
C14 = ROOT / "scaleup" / "claim14" / "claim14_future_per_fire.csv"
C15 = ROOT / "scaleup" / "claim15" / "claim15_g2_per_fire.csv"
C16 = ROOT / "scaleup" / "claim16" / "claim16_per_fire.csv"


def spearman(a, b):
    return pd.Series(np.asarray(a)).rank().corr(pd.Series(np.asarray(b)).rank())


def loo_mean_mae(y):
    y = np.asarray(y, float)
    return np.abs(y - (y.sum() - y) / (len(y) - 1)).mean()


def transitions():
    print("== 1. Year-to-year spread and detectable difference (task G-A, target all) ==")
    t = pd.read_csv(TR)
    t = t[t.target == "all"]
    cols = ["tma_cell", "f_only", "density", "pooled_density_rank", "standard_spatial", "coord_dist_forest"]
    c = t.dropna(subset=cols)
    print("site-years", len(c), "sites", c.site.nunique())
    print("mean AUC", c[cols].mean().round(3).to_dict())
    print("mean within-site SD across years", c.groupby("site")[cols].std().mean().round(3).to_dict())
    d = c.tma_cell - c.density
    sm = d.groupby(c.site).mean()
    n = len(sm)
    print("tma_cell - density: site-year mean %+.4f | equal-site mean %+.4f, SD of site means %.3f, SE %.4f"
          % (d.mean(), sm.mean(), sm.std(), sm.std() / np.sqrt(n)))
    print("minimum detectable paired difference, 80%% power, two-sided 0.05: %.3f; sites needed for 0.01: %d"
          % (2.8 * sm.std() / np.sqrt(n), round((2.8 * sm.std() / 0.01) ** 2)))


def later():
    print("\n== 2. Focal-event models on 2024-2026 burning (claim16, eligible sites) ==")
    c = pd.read_csv(C16)
    e = c[c.eligible]
    cols = ["late_thermal", "baseline_late", "thermal_coord_late", "thermal_dist_late", "coord_rf_late", "coord_knn_late"]
    print("n", len(e), e[cols].mean().round(3).to_dict())
    for a in cols[1:]:
        d = e.late_thermal - e[a]
        print("  thermal minus %-18s mean %+.3f SE %.3f" % (a, d.mean(), d.std() / np.sqrt(len(d))))


def focal_errors():
    print("\n== 3. Error of focal estimates against later AUC (later burning to end of 2023) ==")
    c14 = pd.read_csv(C14).set_index("fire")
    c15 = pd.read_csv(C15).set_index("fire")
    rows = {"thermal": (c14.focal_thermal_auc, c14.focal_thermal_cauc, c14.focal_thermal_saucc,
                        c14.coord_primary_fut_thermal)}
    for m in ["thermal_dist", "thermal_coord", "coord_rf", "coord_knn"]:
        rows[m] = (c15[m + "_focal_auc"], c15[m + "_focal_cauc"], c15[m + "_focal_saucc"], c15[m + "_fut"])
    print("model: signed error (MAE) of raw AUC, cAUC, sAUC_c; each on the fires where that measure exists")
    for m, (a, c, s, f) in rows.items():
        out = []
        for est in (a, c, s):
            e = (est - f).dropna()
            out.append("%+.3f (%.3f, n %d)" % (e.mean(), e.abs().mean(), len(e)))
        print("  %-13s raw %s | cAUC %s | sAUC_c %s" % (m, *out))
    print("\n== 4. Do focal measures carry site-level information? (fires where sAUC_c is supported) ==")
    print("model: n, Spearman of later AUC with raw / cAUC / sAUC_c; MAE of sAUC_c, constant 0.5, mean of other sites")
    for m, (a, c, s, f) in rows.items():
        d = pd.concat([a, c, s, f], axis=1).dropna()
        d.columns = ["a", "c", "s", "f"]
        print("  %-13s %2d  %+.2f %+.2f %+.2f | %.3f %.3f %.3f" % (
            m, len(d), spearman(d.a, d.f), spearman(d.c, d.f), spearman(d.s, d.f),
            (d.s - d.f).abs().mean(), (0.5 - d.f).abs().mean(), loo_mean_mae(d.f)))
    models = ["thermal_dist", "thermal_coord", "coord_rf", "coord_knn"]
    for meas in ["auc", "cauc", "saucc"]:
        rs = []
        for fire in c15.index:
            x = [c14.loc[fire, "focal_thermal_" + meas]] + [c15.loc[fire, m + "_focal_" + meas] for m in models]
            y = [c14.loc[fire, "coord_primary_fut_thermal"]] + [c15.loc[fire, m + "_fut"] for m in models]
            if np.all(np.isfinite(x)):
                rs.append(spearman(x, y))
        print("  within-site rank correlation of the 5 models, focal %s against later AUC: %+.2f (n %d)"
              % (meas, np.mean(rs), len(rs)))
    c16 = pd.read_csv(C16).set_index("fire")
    j = pd.concat([c14.coord_primary_fut_thermal.rename("p1"), c16[c16.eligible].late_thermal.rename("p2")],
                  axis=1).dropna()
    print("  thermal later AUC, to 2023 against 2024-2026: n %d, Spearman %+.2f" % (len(j), spearman(j.p1, j.p2)))


def synthetic():
    print("\n== 5. Synthetic runs of plan 6.2: labels with no environmental signal as a placebo ==")
    d = pd.read_csv(C9)
    d = d[d.b > 0]
    p = d[d.a == 0]
    print("a = 0, b > 0: runs %d | env forest AUC %.3f (truth %.3f) | coordinate forest %.3f | null %.3f"
          % (len(p), p.auc_env.mean(), p.truth_env.mean(), p.auc_geo.mean(), p.auc_null.mean()))
    q = p[(p.b == 4) & (p.L == 10)]
    print("  b = 4, L = 10: env %.3f | coordinate %.3f | null %.3f" % (q.auc_env.mean(), q.auc_geo.mean(), q.auc_null.mean()))
    pl = p.set_index(["fire", "b", "L"])[["auc_env", "auc_geo"]].rename(columns={"auc_env": "pl_env", "auc_geo": "pl_geo"})
    x = d[d.a > 0].join(pl, on=["fire", "b", "L"]).reset_index(drop=True)
    print("runs with a > 0 and b > 0:", len(x), "(one placebo draw per fire and (b, L): the same fire's a = 0 run)")
    for m in ["env", "geo"]:
        o, pp, t = x["auc_" + m], x["pl_" + m], x["truth_" + m]
        est = {"raw": o, "cAUC": x["cauc_" + m], "sAUC_c": x["saucc_" + m], "additive": 0.5 + (o - pp),
               "ratio": 0.5 + 0.5 * (o - pp) / (1 - pp)}
        for k, v in est.items():
            e = v - t
            print("  %s %-8s bias %+.4f MAE %.4f corr %+.3f" % (m, k, e.mean(), e.abs().mean(), np.corrcoef(v, t)[0, 1]))
    tr = (x.truth_env >= x.truth_geo).values
    gap = (x.truth_env - x.truth_geo).abs().values
    rules = {"raw AUC": (x.auc_env >= x.auc_geo).values, "cAUC": (x.cauc_env >= x.cauc_geo).values,
             "sAUC_c": (x.saucc_env >= x.saucc_geo).values,
             "placebo difference": ((x.auc_env - x.pl_env) >= (x.auc_geo - x.pl_geo)).values,
             "always environmental": np.ones(len(x), bool)}
    print("  truth prefers the environmental model in %.3f of runs" % tr.mean())
    for k, ch in rules.items():
        bal = ((ch & tr).sum() / tr.sum() + ((~ch) & (~tr)).sum() / (~tr).sum()) / 2
        print("  selection by %-21s loss %.4f balanced accuracy %.3f" % (k, np.where(ch == tr, 0, gap).mean(), bal))


if __name__ == "__main__":
    transitions()
    later()
    focal_errors()
    synthetic()
