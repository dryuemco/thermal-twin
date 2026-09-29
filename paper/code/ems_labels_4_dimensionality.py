"""Request 4 (R3): effective dimensionality of the six-channel thermal block, per region,
TSG population. Correlation matrix, correlation-matrix PCA (complete cases; median-imputed
as secondary), components for 90 % / 95 %, and exact fused == current equality.
No model is fitted.
"""
import ems_labels_common as E
import numpy as np
import pandas as pd

TH6 = [f for f in E.C.THERMAL if f not in E.C.BASELINE]
res = {}


def pca(X):
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    ev = np.linalg.eigvalsh(np.cov(Z, rowvar=False))[::-1]
    r = ev / ev.sum()
    cum = np.cumsum(r)
    return {"explained_variance_ratio": r.tolist(), "cumulative": cum.tolist(),
            "k90": int(np.searchsorted(cum, 0.90) + 1), "k95": int(np.searchsorted(cum, 0.95) + 1),
            "participation_ratio": float(ev.sum() ** 2 / (ev ** 2).sum())}


for reg in E.REGIONS:
    d = E.tsg(reg, columns=["valid_for_modeling", "burnable_tree_shrub_grass"] + TH6)
    cc = d[TH6].dropna()
    imp = d[TH6].fillna(d[TH6].median())
    corr = cc.corr()
    f, c = d.fused_lst_mean, d.current_lst_mean
    both = f.notna() & c.notna()
    eq = {"rows": int(len(d)), "both_finite": int(both.sum()),
          "exactly_equal": int((f[both] == c[both]).sum()),
          "fraction_equal_of_both_finite": float((f[both] == c[both]).mean()),
          "fused_only_finite": int((f.notna() & c.isna()).sum()),
          "current_only_finite": int((f.isna() & c.notna()).sum()),
          "both_missing": int((f.isna() & c.isna()).sum()),
          "max_abs_diff_both_finite": float((f[both] - c[both]).abs().max())}
    res[reg] = {"n_tsg": int(len(d)), "n_complete": int(len(cc)),
                "correlation": corr.round(4).to_dict(),
                "pca_complete_case": pca(cc.to_numpy()),
                "pca_median_imputed": pca(imp.to_numpy()),
                "fused_vs_current": eq}
    p = res[reg]["pca_complete_case"]
    E.log(f"{reg}: n={len(d)} complete={len(cc)}  EVR={np.round(p['explained_variance_ratio'], 3)} "
          f"k90={p['k90']} k95={p['k95']} PR={p['participation_ratio']:.2f}")
    E.log(corr.round(3).to_string())
    E.log("  fused==current:", eq)

E.dump(res, "r4_dimensionality.json")
