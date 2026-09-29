"""Round 7 (2026-09-29): four quantities an internal review asked for, computed from
hash-verified inputs so that every number the revised text prints has a tracked source.

  R7a  PR-AUC per transfer direction with a 10-cell (~5 km) target-block bootstrap (F59 / gap audit).
       Same scheme as the pipeline's step9c (1000 replicates, numpy default_rng(42), single-class
       replicates skipped), with 10-cell instead of 2-cell blocks. The ROC column is a control: it
       must reproduce round5/out_official/transfer_ci_blocksize.csv (10-cell ROC bounds).
  R7b  The thermal sign held against terrain (F39): current LST within elevation deciles, and LST
       detrended on elevation by the region's own least-squares fit, on the full frame and the 10 km
       collar. Stratified AUC exactly as S1.11 (verify_matched_gap.strat, copied below).
  R7c  Frame cost A - B over all nine scars, scar-level t and region-clustered t over five regions
       (F10), from labelfix_rerun/code/matched_holdout.json.
  R7d  Pooled leave-one-region-out against the MEAN single source rather than the best of four (F61),
       from labelfix_rerun/code/loro_all.json and round5/collar/aoi_frame_transfer.csv.

Run from thermal-twin-main with .venv-step10:  python paper/labelfix_rerun/round7/round7.py
Writes only into paper/labelfix_rerun/round7/.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage, stats
from sklearn.metrics import average_precision_score, roc_auc_score

os.environ.setdefault("THERMAL_TWIN_LABELS", "corrected")
ROOT = Path(__file__).resolve().parents[3]          # thermal-twin-main
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "paper" / "code"))
import _canonical  # noqa: E402

LF = ROOT / "paper" / "labelfix_rerun"
DRIVE = ROOT.parent / "thermal-twin" / "drive_new" / "cross_region"
REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
SEED, NBOOT, CELL_KM = 42, 1000, 0.45
inputs = {}


def sha(p):
    h = hashlib.sha256(Path(p).read_bytes()).hexdigest()
    inputs[Path(os.path.abspath(p)).relative_to(ROOT.parent).as_posix()] = h  # drive_new is a link; keep its name
    return h


def tt(v):
    v = np.asarray(v, float)
    n = len(v)
    m = v.mean()
    h = stats.t.ppf(0.975, n - 1) * v.std(ddof=1) / np.sqrt(n)
    return {"mean": m, "lo": m - h, "hi": m + h, "n": n}


# ---------------------------------------------------------------- R7a
# Manavgat pairs: the corrected pipeline tree. Other pairs: the frozen drive_new export, which the
# label correction does not touch (CHANGES.md section 2).
PAIRS = {
    "manavgat_2021__bejis_2022": LF / "pipeline" / "cross_region",
    "manavgat_2021__mugla_2021": LF / "pipeline" / "cross_region",
    "manavgat_2021__evia_2021_extended": LF / "pipeline" / "cross_region",
    "montiferru_2021__manavgat_2021": LF / "pipeline" / "cross_region",
    "bejis_2022__evia_2021_extended": DRIVE,
    "bejis_2022__mugla_2021": DRIVE,
    "montiferru_2021__bejis_2022": DRIVE,
    "montiferru_2021__evia_2021_extended": DRIVE,
    "montiferru_2021__mugla_2021": DRIVE,
    "mugla_2021__evia_2021_extended": DRIVE,
}
# The per-cell prediction files are not tracked under their pipeline paths (.gitignore). Gzipped
# copies are released in round7/frozen_predictions/, with the SHA-256 of the uncompressed bytes in
# SHA256SUMS_uncompressed.txt; a clone without the pipeline trees reads those and checks the hash.
FROZEN = OUT / "frozen_predictions"
SUMS = dict(l.split()[::-1] for l in (FROZEN / "SHA256SUMS_uncompressed.txt").read_text().split("\n") if l.strip())
preds = []
for pair, root in PAIRS.items():
    f = root / pair / "step9b" / "cross_region_transfer_predictions.csv"
    if f.exists():
        raw = f.read_bytes()
    else:
        import gzip
        import io
        raw = gzip.decompress((FROZEN / f"{pair}.csv.gz").read_bytes())
    h = hashlib.sha256(raw).hexdigest()
    assert h == SUMS[f"{pair}.csv"], f"{pair}: prediction file does not match its recorded hash"
    inputs[f"frozen_predictions/{pair}.csv"] = h
    import io
    d = pd.read_csv(io.BytesIO(raw))
    preds.append(d[d.population == "burnable_tree_shrub_grass"])
P = pd.concat(preds).drop_duplicates(["transfer_direction", "target_cell_id"])
DIRS = sorted(P.transfer_direction.unique())
assert len(DIRS) == 20, DIRS


def boot(y, s, blocks, fn):
    rng = np.random.default_rng(SEED)
    ub, inv = np.unique(blocks, return_inverse=True)
    idx_by = [np.flatnonzero(inv == k) for k in range(len(ub))]
    vals = []
    for _ in range(NBOOT):
        pick = rng.integers(0, len(ub), len(ub))
        ii = np.concatenate([idx_by[k] for k in pick])
        if y[ii].min() == y[ii].max():
            continue
        vals.append(fn(y[ii], s[ii]))
    return np.percentile(vals, [2.5, 97.5]), len(vals)


def mulberry32(a):
    """Port of mulberry32 in round5/code_control/transfer_ci_blocksize.mjs (32-bit JS arithmetic)."""
    a &= 0xFFFFFFFF

    def imul(x, y):
        return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF

    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


def boot_js(y, blocks, scores):
    """The paper's 10-cell scheme: blocks indexed in order of first appearance, one mulberry32(42)
    stream, replicate weights = block draw counts, invalid (single-class) replicates skipped, linear
    percentiles. Returns (lo, hi) per score function."""
    rng = mulberry32(SEED)
    order, first = [], {}
    for b in blocks:
        if b not in first:
            first[b] = len(order)
            order.append(b)
    inv = np.array([first[b] for b in blocks])
    members = [np.flatnonzero(inv == k) for k in range(len(order))]
    nb = len(order)
    out = {name: [] for name in scores}
    for _ in range(NBOOT):
        w = np.zeros(len(y))
        for _s in range(nb):
            w[members[int(rng() * nb)]] += 1
        m = w > 0
        if y[m].min() == y[m].max():
            continue
        for name, (fn, s) in scores.items():
            out[name].append(fn(y[m], s[m], sample_weight=w[m]))
    return {k: np.percentile(v, [2.5, 97.5]) for k, v in out.items()}, len(out[next(iter(out))])


rows = []
for dname in DIRS:
    d = P[P.transfer_direction == dname]
    rc = d.target_cell_id.str.extract(r"r(\d+)_c(\d+)").astype(int)
    b2 = d.target_spatial_block_id.to_numpy()
    same2 = ((rc[0] // 2).astype(str) + "_" + (rc[1] // 2).astype(str)).to_numpy() == b2
    assert same2.all(), f"{dname}: 2-cell id is not (row//2, col//2)"
    b10 = ((rc[0] // 10).astype(str) + "_" + (rc[1] // 10).astype(str)).to_numpy()
    y = d.burned.to_numpy().astype(int)
    s = d.thermal_probability.to_numpy()
    prev = y.mean()
    ci10, nv = boot_js(y, b10, {"roc": (roc_auc_score, s), "pr": (average_precision_score, s)})
    roc10, pr10 = ci10["roc"], ci10["pr"]
    pr2, _ = boot(y, s, b2, average_precision_score)  # auxiliary; the published 2-cell PR bounds are step9c's
    pr = average_precision_score(y, s)
    rows.append({"direction": dname, "prevalence": prev, "pr_auc": pr,
                 "pr_ci2_lo": pr2[0], "pr_ci2_hi": pr2[1], "pr_ci10_lo": pr10[0], "pr_ci10_hi": pr10[1],
                 "valid_reps_10": nv, "below_baseline_point": pr < prev,
                 "below_supported_2cell": pr2[1] < prev, "below_supported_10cell": pr10[1] < prev,
                 "roc_auc": roc_auc_score(y, s), "roc_ci10_lo": roc10[0], "roc_ci10_hi": roc10[1]})
pr = pd.DataFrame(rows)
REF = LF / "round5" / "out_official" / "transfer_ci_blocksize.csv"
sha(REF)
ref = pd.read_csv(REF)


def key(s):
    s = s.lower().replace("evia_2021_extended", "evia").replace("_2021", "").replace("_2022", "")
    return s.replace("mugla", "mugla")


ref["k"] = ref.direction.str.lower().str.replace("ğ", "g")
pr["k"] = pr.direction.map(key)
m = pr.merge(ref[["k", "ci_10cell_lo", "ci_10cell_hi"]], on="k", how="left")
assert m.ci_10cell_lo.notna().all(), m.loc[m.ci_10cell_lo.isna(), "direction"].tolist()
roc_ctrl = float(np.max(np.abs(np.r_[m.roc_ci10_lo - m.ci_10cell_lo, m.roc_ci10_hi - m.ci_10cell_hi])))
pr.drop(columns="k").to_csv(OUT / "r7a_pr_auc_10cell.csv", index=False)
below = pr.below_baseline_point
r7a = {"mean_pr_auc": pr.pr_auc.mean(), "mean_prevalence": pr.prevalence.mean(),
       "below_point": int(below.sum()),
       "below_supported_2cell": int((below & pr.below_supported_2cell).sum()),
       "below_supported_10cell": int((below & pr.below_supported_10cell).sum()),
       "below_supported_10cell_directions": pr.loc[below & pr.below_supported_10cell, "direction"].tolist(),
       "above_2x_baseline": pr.loc[pr.pr_auc > 2 * pr.prevalence, "direction"].tolist(),
       "roc10_control_max_abs_diff_vs_round5": roc_ctrl}
print("R7a", json.dumps(r7a, indent=1))

# ---------------------------------------------------------------- R7b


def load(r):
    d = _canonical.load(r)
    inputs[f"_canonical:{r}"] = _canonical.sha256(_canonical.path(r))
    d = d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H, W = int(d.row_500m.max()) - r0 + 1, int(d.col_500m.max()) - c0 + 1
    rr, cc = d.row_500m.to_numpy().astype(int) - r0, d.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), dtype=bool)
    b = d.burned.to_numpy() == 1
    bg[rr[b], cc[b]] = False
    d["dist_km"] = ndimage.distance_transform_edt(bg)[rr, cc] * CELL_KM
    return d


def strat(sub, feat, by, nbin=10):  # copied verbatim from paper/code/verify_matched_gap.py
    s = sub[[feat, by, "burned"]].dropna()
    if s.burned.nunique() < 2:
        return np.nan
    try:
        s["bin"] = pd.qcut(s[by], nbin, labels=False, duplicates="drop")
    except ValueError:
        return np.nan
    num = den = 0.0
    for _, g in s.groupby("bin"):
        if g.burned.nunique() < 2:
            continue
        w = (g.burned == 1).sum() * (g.burned == 0).sum()
        num += roc_auc_score(g.burned, g[feat]) * w
        den += w
    return num / den if den else np.nan


def auc(sub, feat):
    ok = sub[feat].notna()
    return roc_auc_score(sub.burned[ok], sub[feat][ok])


rows = []
for r in REG:
    d = load(r)
    ok = d.current_lst_mean.notna() & d.elevation_mean.notna()
    slope, icpt = np.polyfit(d.elevation_mean[ok], d.current_lst_mean[ok], 1)
    d["lst_detrended"] = d.current_lst_mean - (slope * d.elevation_mean + icpt)
    for frame, sub in [("full", d), ("10km", d[d.dist_km <= 10])]:
        rows.append({"region": r, "frame": frame, "lst_raw": auc(sub, "current_lst_mean"),
                     "lst_within_elevation": strat(sub, "current_lst_mean", "elevation_mean"),
                     "lst_detrended_on_elevation": auc(sub, "lst_detrended"),
                     "lst_elevation_slope_K_per_km": slope * 1000,
                     "elevation_raw": auc(sub, "elevation_mean")})
r7b = pd.DataFrame(rows)
r7b.to_csv(OUT / "r7b_lst_given_terrain.csv", index=False)
print("R7b\n", r7b.round(3).to_string())

# ---------------------------------------------------------------- R7c
MH = LF / "code" / "matched_holdout.json"
sha(MH)
h = pd.DataFrame(json.load(open(MH)))
x = h.A_region_blocked - h.B_seen_same_cells
s7 = h[h.C_unseen_same_region.notna()]
x7 = s7.A_region_blocked - s7.B_seen_same_cells
r7c = {"nine_scars_scar_t": tt(x), "nine_scars_region_t_G5": tt(x.groupby(h.region).mean()),
       "seven_scars_scar_t": tt(x7), "seven_scars_region_t_G3": tt(x7.groupby(s7.region).mean()),
       "regions_nine": h.region.value_counts().to_dict()}
print("R7c", json.dumps(r7c, indent=1, default=float))

# ---------------------------------------------------------------- R7d
LO = LF / "code" / "loro_all.json"
sha(LO)
L = pd.DataFrame(json.load(open(LO)))
L = L[(L.scaling == "raw") & (L.feature_set == "thermal")].set_index("target").roc_auc
FT = LF / "round5" / "collar" / "aoi_frame_transfer.csv"
sha(FT)
T = pd.read_csv(FT)
T = T[(T.source_frame == "full") & (T.target_frame == "full")].copy()
T["target"] = T.direction.str.split("_to_").str[1]
g = T.groupby("target").thermal
r7d = pd.DataFrame({"pooled": L, "mean_single": g.mean(), "best_single_oracle": g.max(), "worst_single": g.min()})
r7d["pooled_minus_mean"] = r7d.pooled - r7d.mean_single
r7d.to_csv(OUT / "r7d_pooled_vs_single.csv")
print("R7d\n", r7d.round(3).to_string())

json.dump({"created": "2026-09-29", "inputs_sha256": inputs, "r7a": r7a, "r7c": r7c,
           "r7d_pooled_beats_mean_single": int((r7d.pooled_minus_mean > 0).sum()),
           "r7d_pooled_beats_best_single": int((r7d.pooled > r7d.best_single_oracle).sum())},
          open(OUT / "round7_summary.json", "w"), indent=1, default=float)
print("wrote", OUT)
