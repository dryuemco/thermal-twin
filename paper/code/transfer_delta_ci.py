"""Interval on the mean paired thermal-minus-baseline transfer delta, on canonical inputs.

The abstract, highlights, Section 4.3 and Appendix A(o) quote "+0.004 [-0.028, +0.036]
across twenty transfer directions". That figure had no stored source artefact in this
tree: it was computed by paper/referee2_numbers.mjs (block A, 20,000 replicates) from
the step9b point deltas. This script recomputes it, and the equalised-frame intervals of
Section 4.4 (paper/equalised_delta_interval.json, also without a stored script), from
the twenty per-direction thermal and baseline AUCs in aoi_frame_transfer.csv, which
paper/code/regen_transfer_ci.py regenerates from _canonical.load() inputs.

Resampling units, as Appendix A(o) defines them. The twenty ordered directions are not
independent (each region appears in eight), so:
  pair cluster      resample the 10 unordered region pairs with replacement; both
                    directions of a drawn pair enter together (the headline unit)
  target cluster    resample the 5 target regions; each brings its 4 incoming directions
  naive             resample the 20 directions (percentile) and Student t over them
  pair t            Student t on the 10 pair means
  region jackknife  leave-one-region-out over the 5 regions, t with 4 df
Methods 3.13 states 1000 bootstrap replicates throughout, so 1000 is the primary count.
The published figures used 20,000; that count is also reported, so that Monte Carlo
change can be separated from data change. Seed 42.

No model is fitted here (the fits are in regen_transfer_ci.py, which asserts leakage).

Usage: transfer_delta_ci.py   (reads/writes under $PAPER_ARTEFACTS, default paper)
"""
import json
import os
from collections import defaultdict

import numpy as np
import pandas as pd
from scipy import stats

ART = os.environ.get("PAPER_ARTEFACTS", "paper")
SRC = f"{ART}/aoi_frame_transfer.csv"
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
FRAMES = {"as drawn": ("full", "full"), "equalised 10 km": ("10km", "10km"),
          "equalised 5 km": ("5km", "5km")}
SEED = 42
PRIMARY_B, PUBLISHED_B = 1000, 20000


def deltas(frame):
    d = pd.read_csv(SRC)
    d = d[(d.source_frame == frame[0]) & (d.target_frame == frame[1])].copy()
    d["source"] = d.direction.str.split("_to_").str[0]
    d["target"] = d.direction.str.split("_to_").str[1]
    d["pair"] = [tuple(sorted((s, t))) for s, t in zip(d.source, d.target)]
    d["delta"] = d.thermal - d.baseline
    assert len(d) == 20 and d.pair.nunique() == 10, (frame, len(d))
    return d.reset_index(drop=True)


def cluster_boot(d, key, nboot, seed=SEED):
    groups = defaultdict(list)
    for k, v in zip(d[key], d.delta):
        groups[k].append(v)
    keys = list(groups)
    rng = np.random.default_rng(seed)
    out = np.empty(nboot)
    for b in range(nboot):
        pick = rng.integers(0, len(keys), len(keys))
        out[b] = np.mean([v for i in pick for v in groups[keys[i]]])
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


def naive_boot(d, nboot, seed=SEED):
    x = d.delta.to_numpy()
    rng = np.random.default_rng(seed)
    out = np.array([x[rng.integers(0, len(x), len(x))].mean() for _ in range(nboot)])
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


def t_ci(x):
    x = np.asarray(x, float)
    h = stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
    return [float(x.mean() - h), float(x.mean() + h)]


def jackknife(d):
    m = d.delta.mean()
    loo = {r: float(d[(d.source != r) & (d.target != r)].delta.mean()) for r in REGIONS}
    g = len(REGIONS)
    pseudo = np.array([g * m - (g - 1) * loo[r] for r in REGIONS])
    h = stats.t.ppf(0.975, g - 1) * pseudo.std(ddof=1) / np.sqrt(g)
    return [float(pseudo.mean() - h), float(pseudo.mean() + h)], loo


r4 = lambda v: [round(x, 4) for x in v] if isinstance(v, list) else round(v, 4)
results = {}
for name, frame in FRAMES.items():
    d = deltas(frame)
    jk, loo = jackknife(d)
    res = {"mean": float(d.delta.mean()), "n": 20,
           "n_positive": int((d.delta > 0).sum()), "n_negative": int((d.delta < 0).sum()),
           "min": float(d.delta.min()), "max": float(d.delta.max())}
    for B in (PRIMARY_B, PUBLISHED_B):
        res[f"B{B}"] = {
            "ci_pair_cluster": cluster_boot(d, "pair", B),
            "ci_target_region_cluster": cluster_boot(d, "target", B),
            "ci_naive_percentile": naive_boot(d, B),
        }
    res["ci_naive_t"] = t_ci(d.delta)
    res["ci_pair_t"] = t_ci(d.groupby("pair").delta.mean())
    res["ci_region_jackknife_t"] = jk
    res["leave_one_region_out"] = loo
    res["spans_zero_pair_cluster"] = bool(res[f"B{PRIMARY_B}"]["ci_pair_cluster"][0] < 0
                                          < res[f"B{PRIMARY_B}"]["ci_pair_cluster"][1])
    res["per_direction"] = {k: float(v) for k, v in zip(d.direction, d.delta)}
    results[name] = res
    p = res[f"B{PRIMARY_B}"]["ci_pair_cluster"]
    q = res[f"B{PUBLISHED_B}"]["ci_pair_cluster"]
    print(f"{name:16s} mean {res['mean']:+.4f}  pair-cluster B=1000 [{p[0]:+.4f}, {p[1]:+.4f}]"
          f"  B=20000 [{q[0]:+.4f}, {q[1]:+.4f}]  target-cluster B=1000 "
          f"[{res['B1000']['ci_target_region_cluster'][0]:+.4f}, "
          f"{res['B1000']['ci_target_region_cluster'][1]:+.4f}]")

# cross-check the as-drawn deltas against the frozen step9b export (4 dp)
ref = pd.read_csv("paper/baseline_vs_thermal_transfer.csv").set_index("direction")
dd = results["as drawn"]["per_direction"]
xdiff = max(abs(dd[k] - (ref.loc[k, "thermal_roc"] - ref.loc[k, "baseline_roc"])) for k in dd)
print(f"max |canonical refit delta - step9b delta (4 dp)| = {xdiff:.5f}")

doc = {
    "what": ("Mean paired thermal-minus-baseline transfer delta over the twenty ordered "
             "directions, with the resampling units of Appendix A(o). Deltas from "
             f"{SRC}, regenerated by regen_transfer_ci.py from _canonical.load() inputs. "
             f"Primary B={PRIMARY_B} (Methods); B={PUBLISHED_B} as the published figures used. "
             "Seed 42."),
    "abstract_quantity": {
        "frame": "as drawn (full/full)",
        "mean": results["as drawn"]["mean"],
        "ci_pair_cluster_B1000": results["as drawn"]["B1000"]["ci_pair_cluster"],
        "ci_pair_cluster_B20000": results["as drawn"]["B20000"]["ci_pair_cluster"],
        "published": {"mean": 0.004, "ci_pair_cluster": [-0.028, 0.036],
                      "source": "paper/referee2_numbers.json A_mean_paired_contribution "
                                "(step9b deltas, 20000 replicates, JS mulberry32 seed 42)"},
    },
    "check_vs_step9b_max_abs_diff_4dp": xdiff,
    "results": results,
}
json.dump(doc, open(f"{ART}/transfer_delta_ci.json", "w"), indent=1)

# the same quantities in the layout of paper/equalised_delta_interval.json
eq = {"what": ("Paired thermal-minus-baseline contribution to transfer, by evaluation frame, "
               "with the resampling units of Appendix A(o). Source aoi_frame_transfer.csv "
               f"regenerated on canonical inputs. {PRIMARY_B} replicates, seed 42 "
               f"(the published file used 20000; see transfer_delta_ci.json for both)."),
      "results": {n: {"mean": r4(r["mean"]), "n": 20,
                      "ci_pair_cluster": r4(r["B1000"]["ci_pair_cluster"]),
                      "ci_target_region_cluster": r4(r["B1000"]["ci_target_region_cluster"]),
                      "ci_naive_t": r4(r["ci_naive_t"]),
                      "spans_zero_pair_cluster": r["spans_zero_pair_cluster"]}
                  for n, r in results.items()}}
json.dump(eq, open(f"{ART}/equalised_delta_interval.json", "w"), indent=1)
print(f"wrote {ART}/transfer_delta_ci.json and {ART}/equalised_delta_interval.json")
