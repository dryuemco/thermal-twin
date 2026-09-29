"""Analysis 3 (SPEC.md): frame cost (A - B per scar) against the region's far-field share."""
import numpy as np
import pandas as pd
from scipy import stats

import ems_geometry_common as G


def ols(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    r = stats.linregress(x, y)
    n = len(x)
    h = stats.t.ppf(0.975, n - 2) * r.stderr
    return {"slope": r.slope, "t_lo": r.slope - h, "t_hi": r.slope + h, "intercept": r.intercept,
            "r": r.rvalue, "p": r.pvalue, "n": n, "df": n - 2}


scar_rows, reg_rows = [], []
for reg in G.REGIONS:
    R = G.Region(reg)
    oof = G.oof_row_a(R)
    a = G.auc(R.y, oof)
    share = float((R.dist_collar > 10).mean())
    share_band = float((R.dist_band > 10).mean())
    c10 = R.dist_collar <= 10
    a10 = G.auc(R.y[c10], oof[c10])
    bs = []
    for sc in R.scars():
        b = G.auc(R.y[sc["held"]], oof[sc["held"]])
        bs.append(b)
        scar_rows.append({"region": reg, "scar": sc["scar"], "far_share": share, "far_share_band": share_band,
                          "A": a, "B": b, "A_minus_B": a - b})
    reg_rows.append({"region": reg, "far_share": share, "far_share_band": share_band, "A": a, "A_10km": a10,
                     "A_minus_A10": a - a10, "mean_A_minus_B": a - float(np.mean(bs)), "n_scars": len(bs)})
S, Rg = pd.DataFrame(scar_rows), pd.DataFrame(reg_rows)
S.to_csv(G.OUT / "a3_scar_values.csv", index=False)
Rg.to_csv(G.OUT / "a3_region_values.csv", index=False)
out = {
    "scar_level_pseudoreplicated": ols(S.far_share, S.A_minus_B),
    "scar_level_eight_table2": ols(S[S.region != "bejis_2022"].far_share, S[S.region != "bejis_2022"].A_minus_B),
    "region_level_primary": ols(Rg.far_share, Rg.mean_A_minus_B),
    "region_level_band_convention": ols(Rg.far_share_band, Rg.mean_A_minus_B),
    "region_level_spearman": float(stats.spearmanr(Rg.far_share, Rg.mean_A_minus_B).statistic),
    "secondary_A_minus_A10_on_share": ols(Rg.far_share, Rg.A_minus_A10),
    "secondary_spearman": float(stats.spearmanr(Rg.far_share, Rg.A_minus_A10).statistic),
    "leave_one_region_out_primary_slope": {
        r: ols(Rg[Rg.region != r].far_share, Rg[Rg.region != r].mean_A_minus_B)["slope"] for r in G.REGIONS},
}
G.dump(out, "a3_summary.json")
pd.set_option("display.width", 200)
print(S.round(4).to_string()); print(Rg.round(4).to_string())
import json; print(json.dumps(out, indent=1, default=float))
