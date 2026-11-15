"""claim12_summary.py: summaries of plan 8.3 (Monte Carlo replicates), 8.4 (20 km blocks) and 8.5 (calibrated
scenarios), with the 8.1 and 8.7 quantities. Fire bootstrap (2000, seed 42) with draws kept within fires.
Writes claim12_summary.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402
import claim9_rereport as RR  # noqa: E402

MEAS = ("auc", "cauc", "saucc")


def per_fire_ok(R):
    t = np.where(R.truth_env > R.truth_geo, "env", np.where(R.truth_env < R.truth_geo, "geo", "tie"))
    ch = RR.choices(R)
    out = pd.DataFrame({"fire": R.fire.to_numpy()})
    for m in MEAS:
        out[m] = ch[m] == t
    return out.groupby("fire").mean()


def boot_diff(g, a, b, B=2000):
    d = (g[a] - g[b]).to_numpy(float)
    rng = np.random.default_rng(42)
    bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(B)]
    return {"mean": float(d.mean()), "lo": float(np.percentile(bs, 2.5)), "hi": float(np.percentile(bs, 97.5))}


def block(R):
    R = R[R.b > 0] if "b" in R and (R.b > 0).any() and (R.b == 0).any() else R
    s = RR.stats_for(R)
    g = per_fire_ok(R)
    s["agreement_diffs_fire_bootstrap"] = {"cauc_minus_auc": boot_diff(g, "cauc", "auc"),
                                           "saucc_minus_auc": boot_diff(g, "saucc", "auc"),
                                           "saucc_minus_cauc": boot_diff(g, "saucc", "cauc")}
    return s


def main():
    S = {}
    for k in (10, 40):
        R = pd.read_csv(A.OUT / f"claim12_runs_b{k}.csv")
        S[f"blocks_{k}"] = {"all": block(R), "a_zero": RR.stats_for(R[(R.b > 0) & (R.a == 0)]),
                            "a_positive": RR.stats_for(R[(R.b > 0) & (R.a > 0)]), "fires": int(R.fire.nunique()),
                            "draws": int(R.draw.nunique()), "auc_null_mean": float(R.auc_null.mean()),
                            "kept_share_mean": float(R.kept_share.mean())}
    C = pd.read_csv(A.OUT / "claim13_runs.csv")
    S["calibrated"] = {"all": block(C), "compare": json.loads((A.OUT / "claim13_compare.json").read_text())}
    (A.OUT / "claim12_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    for k, v in S.items():
        a = v["all"]
        print(k, "truth_env", round(a["truth_env"], 3), {m: {q: round(a[m][q], 3) for q in ("preference_env", "agreement", "balanced_acc", "relative_loss")} for m in MEAS})
        print("   diffs", {q: f"{d['mean']:+.3f} [{d['lo']:+.3f},{d['hi']:+.3f}]" for q, d in a["agreement_diffs_fire_bootstrap"].items()})


if __name__ == "__main__":
    main()
