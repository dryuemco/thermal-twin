"""EMS referee round, R2 major 6 (multiplicity half). SPEC: ems_analyses/inference/SPEC.md, Task 4.

Reversal family: 9 features x 10 unordered region pairs, signed univariate AUC, 10-cell block
bootstrap per region, independent regions, difference of index-paired replicates -- the instrument
of verify_matched_gap.py, extended from lst_anomaly_mean to all nine features and run on the 10 km
collar (R1, primary) and the frame as drawn (R2); strict-criterion IUT on both (R3). Holm.

Diagnostic family: the 19 computable rows of all_diagnostics_vs_transfer.csv, Spearman rho against
raw thermal transfer, unordered-pair cluster bootstrap. Benjamini-Hochberg.

The block bootstrap uses the paper's draw sequence (default_rng(42) per region, choice of blocks
with replacement, single-class replicates skipped) but evaluates each replicate's AUC as a weighted
Mann-Whitney statistic (block multiplicities as weights), which equals roc_auc_score on the
duplicated rows; checked against sklearn on the first replicates.
"""
import json

import numpy as np
import pandas as pd
from scipy import sparse, stats
from sklearn.metrics import roc_auc_score

import ems_inference_common as E

R = 20000
BLK = 10
FEATS9 = [f for f in E.THERMAL if f != E.CAT]
PAIRS = [(a, b) for i, a in enumerate(E.REGIONS) for b in E.REGIONS[i + 1:]]


def boot_reps(sub, feat, nrep=R, seed=E.SEED, check=3):
    ok = sub[feat].notna().to_numpy()
    y = sub.burned.to_numpy()[ok].astype(int)
    x = sub[feat].to_numpy()[ok]
    blk = ((sub.row_500m // BLK).astype(str) + "_" + (sub.col_500m // BLK).astype(str)).to_numpy()[ok]
    u, bcode = np.unique(blk, return_inverse=True)
    vals, vcode = np.unique(x, return_inverse=True)
    nb, nv = len(u), len(vals)
    H1 = sparse.csr_matrix((y.astype(float), (bcode, vcode)), shape=(nb, nv))
    H0 = sparse.csr_matrix((1.0 - y, (bcode, vcode)), shape=(nb, nv))
    rng = np.random.default_rng(seed)
    out, draws = [], []
    batch = 200
    done = 0
    while done < nrep:
        k = min(batch, nrep - done)
        picks = np.stack([rng.choice(np.arange(nb), nb, replace=True) for _ in range(k)])
        cnt = np.stack([np.bincount(p, minlength=nb) for p in picks]).astype(float)
        w1 = np.asarray((sparse.csr_matrix(cnt) @ H1).todense())
        w0 = np.asarray((sparse.csr_matrix(cnt) @ H0).todense())
        W1, W0 = w1.sum(1), w0.sum(1)
        cum0 = np.cumsum(w0, 1) - w0
        num = (w1 * (cum0 + 0.5 * w0)).sum(1)
        for j in range(k):
            if W1[j] > 0 and W0[j] > 0:
                out.append(num[j] / (W1[j] * W0[j]))
                if len(draws) < check:
                    draws.append(picks[j])
        done += k
    # verification against sklearn on duplicated rows
    idx = {b: np.where(bcode == b)[0] for b in range(nb)}
    for j, p in enumerate(draws):
        ii = np.concatenate([idx[b] for b in p])
        ref = roc_auc_score(y[ii], x[ii])
        assert abs(ref - out[j]) < 1e-9, (feat, ref, out[j])
    return float(roc_auc_score(y, x)), np.array(out)


def holm(p):
    p = np.asarray(p)
    m = len(p)
    o = np.argsort(p)
    adj = np.empty(m)
    run = 0.0
    for k, i in enumerate(o):
        run = max(run, min(1.0, (m - k) * p[i]))
        adj[i] = run
    return adj


def bh(p):
    p = np.asarray(p)
    m = len(p)
    o = np.argsort(p)[::-1]
    adj = np.empty(m)
    run = 1.0
    for k, i in enumerate(o):
        rank = m - k
        run = min(run, p[i] * m / rank)
        adj[i] = run
    return adj


def pct_p(d, null=0.0):
    d = np.asarray(d)
    return max(2 * min((d <= null).mean(), (d >= null).mean()), 1.0 / len(d))


def reversal_families():
    data = {r: E.load(r) for r in E.REGIONS}
    per_region, fam = [], []
    reps = {}
    for tag in ("collar10", "full"):
        for r in E.REGIONS:
            sub = data[r] if tag == "full" else data[r][data[r].dist_km <= 10]
            for f in FEATS9:
                pt, rp = boot_reps(sub, f)
                reps[(tag, r, f)] = (pt, rp)
                sd = rp.std(ddof=1)
                per_region.append({
                    "frame": tag, "region": r, "feature": f, "auc": pt,
                    "lo_1000": float(np.percentile(rp[:1000], 2.5)),
                    "hi_1000": float(np.percentile(rp[:1000], 97.5)),
                    "lo": float(np.percentile(rp, 2.5)), "hi": float(np.percentile(rp, 97.5)),
                    "sd": float(sd), "p_norm_vs_half": float(2 * stats.norm.sf(abs(pt - 0.5) / sd)),
                    "p_pct_vs_half": float(pct_p(rp, 0.5)), "n_reps": int(len(rp))})
                print(tag, r, f, f"{pt:.3f}", flush=True)
    pr = pd.DataFrame(per_region)
    for tag in ("collar10", "full"):
        for f in FEATS9:
            for a, b in PAIRS:
                pa, ra = reps[(tag, a, f)]
                pb, rb = reps[(tag, b, f)]
                n1 = min(len(ra[:1000]), len(rb[:1000]))
                d1 = ra[:1000][:n1] - rb[:1000][:n1]
                n = min(len(ra), len(rb))
                d = ra[:n] - rb[:n]
                sd = d.std(ddof=1)
                qa = pr[(pr.frame == tag) & (pr.region == a) & (pr.feature == f)].iloc[0]
                qb = pr[(pr.frame == tag) & (pr.region == b) & (pr.feature == f)].iloc[0]
                opp = (pa - 0.5) * (pb - 0.5) < 0
                fam.append({
                    "frame": tag, "feature": f, "region_a": a, "region_b": b,
                    "auc_a": pa, "auc_b": pb, "diff": pa - pb,
                    "diff_lo_1000": float(np.percentile(d1, 2.5)),
                    "diff_hi_1000": float(np.percentile(d1, 97.5)),
                    "diff_lo": float(np.percentile(d, 2.5)), "diff_hi": float(np.percentile(d, 97.5)),
                    "opposite_sides": bool(opp),
                    "p_norm": float(2 * stats.norm.sf(abs(pa - pb) / sd)),
                    "p_pct": float(pct_p(d)),
                    "p_iut_norm": float(max(qa.p_norm_vs_half, qb.p_norm_vs_half)) if opp else 1.0,
                    "p_iut_pct": float(max(qa.p_pct_vs_half, qb.p_pct_vs_half)) if opp else 1.0,
                    "strict_supported_1000": bool(opp and (qa.lo_1000 > .5 or qa.hi_1000 < .5)
                                                  and (qb.lo_1000 > .5 or qb.hi_1000 < .5)),
                })
    F = pd.DataFrame(fam)
    for tag in ("collar10", "full"):
        m = F.frame == tag
        for col in ("p_norm", "p_pct", "p_iut_norm", "p_iut_pct"):
            F.loc[m, col + "_holm"] = holm(F.loc[m, col].to_numpy())
        for col in ("p_norm", "p_pct"):
            F.loc[m, col + "_bh"] = bh(F.loc[m, col].to_numpy())
        F.loc[m, "diff_excl0_1000"] = (F.loc[m, "diff_lo_1000"] > 0) | (F.loc[m, "diff_hi_1000"] < 0)
    return pr, F


def diagnostic_family():
    rg = json.load(open(E.PAPER / "regime_transfer_correlation.json"))
    cs = json.load(open(E.PAPER / "conditional_similarity_transfer.json"))
    no = json.load(open(E.PAPER / "niche_overlap_transfer.json"))
    tab = pd.read_csv(E.PAPER / "all_diagnostics_vs_transfer.csv")
    per = {}
    for src in (rg["per_direction"], cs["per_direction"], no["per_direction"]):
        for row in src:
            per.setdefault(row["direction"], {}).update(row)
    D = pd.DataFrame(per.values())
    D["transfer"] = D["raw_thermal_roc_auc"].fillna(D.get("thermal_roc"))
    D["pair"] = D.direction.map(lambda s: "__".join(sorted(s.split("_to_"))))
    out = []
    rng_seed = E.SEED
    for _, t in tab.iterrows():
        k = t["measure"]
        if k not in D or D[k].notna().sum() < 4:
            out.append({"measure": k, "label": t["label"], "computable": False})
            continue
        s = D[D[k].notna()]
        x, y, pr = s[k].to_numpy(float), s.transfer.to_numpy(float), s.pair.to_numpy()
        rho = stats.spearmanr(x, y).statistic
        gs = np.unique(pr)
        idx = [np.where(pr == g)[0] for g in gs]
        rng = np.random.default_rng(rng_seed)
        bs = []
        for _ in range(R):
            ii = np.concatenate([idx[j] for j in rng.integers(0, len(gs), len(gs))])
            if np.ptp(x[ii]) == 0 or np.ptp(y[ii]) == 0:
                continue
            v = stats.spearmanr(x[ii], y[ii]).statistic
            if np.isfinite(v):
                bs.append(v)
        bs = np.array(bs)
        out.append({"measure": k, "label": t["label"], "family": t["side"], "computable": True,
                    "n_directions": int(len(s)), "n_pairs": int(len(gs)),
                    "rho_published": float(t["spearman_rho"]), "rho": float(rho),
                    "ci_published": [float(t["spearman_ci_low"]), float(t["spearman_ci_high"])],
                    "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                    "valid_reps": int(len(bs)),
                    "p_boot": float(pct_p(bs)),
                    "p_iid": float(stats.spearmanr(x, y).pvalue)})
    O = pd.DataFrame(out)
    m = O.computable == True  # noqa: E712
    O.loc[m, "p_boot_bh"] = bh(O.loc[m, "p_boot"].to_numpy())
    O.loc[m, "p_iid_bh"] = bh(O.loc[m, "p_iid"].to_numpy())
    O.loc[m, "p_boot_holm"] = holm(O.loc[m, "p_boot"].to_numpy())
    return O


if __name__ == "__main__":
    # The diagnostic family reads class-B->M files; skipped when the redirected inputs directory
    # lacks them (labelfix re-run, 2026-09-19). The reversal family below is label-data only.
    if (E.PAPER / "all_diagnostics_vs_transfer.csv").exists():
        O = diagnostic_family()
        O.to_csv(E.OUTDIR / "diagnostics_bh.csv", index=False)
        print(O[["measure", "n_directions", "rho_published", "rho", "ci", "p_boot", "p_boot_bh",
                 "p_iid", "p_iid_bh"]].to_string())
    else:
        print("diagnostic family SKIPPED: class-B inputs absent from", E.PAPER)
    pr, F = reversal_families()
    pr.to_csv(E.OUTDIR / "reversal_per_region.csv", index=False)
    F.to_csv(E.OUTDIR / "reversal_family_holm.csv", index=False)
    for tag in ("collar10", "full"):
        f = F[F.frame == tag]
        print(f"\n== {tag}: diff CI excl 0 at 1000 reps: {int(f.diff_excl0_1000.sum())}/90; "
              f"opposite & excl: {int((f.diff_excl0_1000 & f.opposite_sides).sum())}; "
              f"strict (1000) {int(f.strict_supported_1000.sum())}")
        for col in ("p_norm", "p_pct", "p_iut_norm", "p_iut_pct"):
            print(f"   Holm<0.05 on {col}: {int((f[col + '_holm'] < 0.05).sum())}")
        print(f.sort_values("p_norm").head(12)[["feature", "region_a", "region_b", "diff",
                                                 "diff_lo", "diff_hi", "p_norm", "p_pct",
                                                 "p_norm_holm", "p_pct_holm", "p_iut_norm_holm"]]
              .to_string())
