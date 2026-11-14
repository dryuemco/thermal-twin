"""claim9_rereport.py: re-reporting of claim9 and claim10 (plan 8.1), no new computation.

For each source (claim9 rho 0; claim10 rho 0, 0.5, 0.8) and measure (pooled AUC, cAUC, sAUC_c), over the runs with
b > 0, split by a = 0 and a > 0 and pooled:
  preference      share of runs in which the measure chooses M_env
  truth_env       share of runs whose truth is M_env (base rate)
  agreement       share of runs in which the choice equals the truth (ties and missing count as wrong)
  balanced_acc    mean of the recall for truth = env and truth = geo
  kappa           Cohen's kappa of choice against truth
  auc_loss        mean truth AUC of the better model minus truth AUC of the chosen model (missing choice = worse)
  spearman        mean over scenarios of Spearman's rho over fires between (env - geo) of the measure and of the truth
Also the constant rules "always env" and "always geo" for reference, and heat maps of preference and balanced
accuracy over a x b, one panel per L, for claim9.

Writes claim9_rereport.json, claim9_rereport_scenarios.csv and claim9_rereport_heatmap.pdf in the analysis folder.
"""
import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402

MEAS = ("auc", "cauc", "saucc")


def choices(R):
    out = {}
    for m in MEAS:
        e, g = R[f"{m}_env"].to_numpy(float), R[f"{m}_geo"].to_numpy(float)
        c = np.where(~(np.isfinite(e) & np.isfinite(g)) | (e == g), "none", np.where(e > g, "env", "geo"))
        out[m] = c
    out["always_env"] = np.full(len(R), "env")
    out["always_geo"] = np.full(len(R), "geo")
    return out


def stats_for(R):
    t = np.where(R.truth_env > R.truth_geo, "env", np.where(R.truth_env < R.truth_geo, "geo", "tie"))
    best = np.maximum(R.truth_env, R.truth_geo).to_numpy()
    worst = np.minimum(R.truth_env, R.truth_geo).to_numpy()
    res = {"runs": int(len(R)), "truth_env": float((t == "env").mean())}
    for m, c in choices(R).items():
        ok = c == t
        rec = [ok[t == k].mean() for k in ("env", "geo") if (t == k).any()]
        po = ok.mean()
        pe = (c == "env").mean() * (t == "env").mean() + (c == "geo").mean() * (t == "geo").mean()
        chosen = np.where(c == "env", R.truth_env, np.where(c == "geo", R.truth_geo, worst))
        d = {"preference_env": float((c == "env").mean()), "agreement": float(po),
             "balanced_acc": float(np.mean(rec)), "kappa": float((po - pe) / (1 - pe)) if pe < 1 else np.nan,
             "auc_loss": float(np.mean(best - chosen))}
        if m in MEAS:
            rhos = []
            for _, g in R.groupby(["a", "b", "L"]):
                x, y = g[f"{m}_env"] - g[f"{m}_geo"], g.truth_env - g.truth_geo
                if x.notna().sum() > 3 and x.std() > 0 and y.std() > 0:
                    rhos.append(spearmanr(x, y, nan_policy="omit")[0])
            d["spearman"] = float(np.nanmean(rhos))
        res[m] = d
    return res


def main():
    src = {"claim9_rho0": pd.read_csv(A.OUT / "claim9_synthetic_runs.csv")}
    c10 = pd.read_csv(A.OUT / "claim10_persistent_runs.csv")
    for r in sorted(c10.rho.unique()):
        src[f"claim10_rho{r}"] = c10[c10.rho == r].drop(columns="rho")
    S, scen = {}, []
    for name, R in src.items():
        R = R[R.b > 0]
        S[name] = {"all": stats_for(R), "a_zero": stats_for(R[R.a == 0]), "a_positive": stats_for(R[R.a > 0])}
        for (a, b, L), g in R.groupby(["a", "b", "L"]):
            st = stats_for(g)
            scen.append({"source": name, "a": a, "b": b, "L": L, "truth_env": st["truth_env"],
                         **{f"{m}_{q}": st[m][q] for m in MEAS for q in ("preference_env", "balanced_acc", "agreement", "auc_loss")}})
    T = pd.DataFrame(scen)
    T.to_csv(A.OUT / "claim9_rereport_scenarios.csv", index=False)
    (A.OUT / "claim9_rereport.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    # heat maps, claim9
    g9 = T[T.source == "claim9_rho0"]
    fig, axs = plt.subplots(2, 6, figsize=(10, 3.8), sharex=True, sharey=True)
    for row, q, lab in ((0, "preference_env", "chooses M_env"), (1, "balanced_acc", "balanced accuracy")):
        col = 0
        for L in (2, 10):
            for m, ml in (("auc", "pooled AUC"), ("cauc", "cAUC"), ("saucc", "sAUC_c")):
                ax = axs[row, col]
                M = g9[g9.L == L].pivot(index="a", columns="b", values=f"{m}_{q}")
                im = ax.imshow(M.values, vmin=0, vmax=1, cmap="viridis", origin="lower")
                for i in range(M.shape[0]):
                    for j in range(M.shape[1]):
                        ax.text(j, i, f"{M.values[i, j]:.2f}", ha="center", va="center", fontsize=5,
                                color="white" if M.values[i, j] < 0.6 else "black")
                ax.set_xticks(range(M.shape[1]), M.columns), ax.set_yticks(range(M.shape[0]), M.index)
                if row == 0:
                    ax.set_title(f"{ml}, L={L} km", fontsize=7)
                if col == 0:
                    ax.set_ylabel(f"a ({lab})", fontsize=7)
                if row == 1:
                    ax.set_xlabel("b", fontsize=7)
                col += 1
    fig.colorbar(im, ax=axs, shrink=0.6)
    fig.savefig(A.OUT / "claim9_rereport_heatmap.pdf")
    for name, v in S.items():
        a = v["all"]
        print(name, "truth_env", round(a["truth_env"], 3), {m: {q: round(a[m][q], 3) for q in ("preference_env", "agreement", "balanced_acc", "kappa", "auc_loss")} | ({"spearman": round(a[m]["spearman"], 3)} if m in MEAS else {}) for m in (*MEAS, "always_env")})


if __name__ == "__main__":
    main()
