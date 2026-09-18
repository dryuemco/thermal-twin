"""EMS referee round, R2 major 5: resampling units for the three direction-level headlines.
SPEC: ems_analyses/inference/SPEC.md, Task 3. No model fits; reads frozen per-direction files.

Also exposes intervals(y, src, tgt, level) for Task 2 (TOST uses 90 % intervals).
"""
import json

import numpy as np
import pandas as pd
from scipy import stats

import ems_inference_common as E

R_BOOT = 20000
REG = E.REGIONS


def _pct(a, level):
    a = np.asarray(a)
    q = (1 - level) / 2
    return float(np.percentile(a, 100 * q)), float(np.percentile(a, 100 * (1 - q)))


def intervals(y, src, tgt, level=0.95, R=R_BOOT, seed=E.SEED):
    y = np.asarray(y, float)
    src = np.asarray(src)
    tgt = np.asarray(tgt)
    n = len(y)
    m = y.mean()
    e = y - m
    s2 = y.var(ddof=1)
    out = {"mean": m, "n": n}
    rng = np.random.default_rng(seed)

    # 1 naive directions
    bs = y[rng.integers(0, n, (R, n))].mean(1)
    out["naive_directions_boot"] = _pct(bs, level) + (float(bs.var(ddof=1)),)

    # 2 unordered pairs
    pair = np.array(["__".join(sorted([a, b])) for a, b in zip(src, tgt)])
    def cboot(cl, seed_off):
        r = np.random.default_rng(seed + seed_off)
        gs = np.unique(cl)
        idx = [np.where(cl == g)[0] for g in gs]
        sums = np.array([y[i].sum() for i in idx])
        cnts = np.array([len(i) for i in idx])
        pick = r.integers(0, len(gs), (R, len(gs)))
        b = sums[pick].sum(1) / cnts[pick].sum(1)
        return _pct(b, level) + (float(b.var(ddof=1)),)
    out["pair_cluster_boot"] = cboot(pair, 1)
    out["target_cluster_boot"] = cboot(tgt, 2)
    out["source_cluster_boot"] = cboot(src, 3)

    # 5a pigeonhole (Owen 2007)
    r5 = np.random.default_rng(seed + 4)
    ri = {g: k for k, g in enumerate(REG)}
    si = np.array([ri[s] for s in src])
    ti = np.array([ri[t] for t in tgt])
    vals = []
    for _ in range(R):
        ns = np.bincount(r5.integers(0, 5, 5), minlength=5)
        nt = np.bincount(r5.integers(0, 5, 5), minlength=5)
        w = ns[si] * nt[ti]
        if w.sum() > 0:
            vals.append((w * y).sum() / w.sum())
    vals = np.array(vals)
    out["pigeonhole_boot"] = _pct(vals, level) + (float(vals.var(ddof=1)),)
    out["pigeonhole_valid_reps"] = int(len(vals))

    tq = stats.t.ppf(0.5 + level / 2, 4)

    # 5b CGM two-way, CR0 components
    def crv(cl):
        return sum(e[cl == g].sum() ** 2 for g in np.unique(cl)) / n ** 2
    v_s, v_t, v_d = crv(src), crv(tgt), (e ** 2).sum() / n ** 2
    v_cgm = v_s + v_t - v_d
    out["cgm_twoway_t4"] = ((m - tq * np.sqrt(v_cgm), m + tq * np.sqrt(v_cgm), float(v_cgm))
                            if v_cgm > 0 else (np.nan, np.nan, float(v_cgm)))

    # 5c dyadic-robust (Aronow, Samii & Assenova 2015)
    share = ((src[:, None] == src[None, :]) | (src[:, None] == tgt[None, :]) |
             (tgt[:, None] == src[None, :]) | (tgt[:, None] == tgt[None, :]))
    v_dy = float((np.outer(e, e) * share).sum() / n ** 2)
    out["dyadic_robust_t4"] = ((m - tq * np.sqrt(v_dy), m + tq * np.sqrt(v_dy), v_dy)
                               if v_dy > 0 else (np.nan, np.nan, v_dy))

    # 6 leave-one-region-out jackknife, t(4)
    loo = np.array([y[(src != g) & (tgt != g)].mean() for g in REG])
    ps = 5 * m - 4 * loo
    v_j = ps.var(ddof=1) / 5
    out["loro_jackknife_t4"] = (float(ps.mean() - tq * np.sqrt(v_j)),
                                float(ps.mean() + tq * np.sqrt(v_j)), float(v_j))
    out["loro_means"] = {E.SHORT[g]: float(v) for g, v in zip(REG, loo)}
    out["loro_pseudo_mean"] = float(ps.mean())

    # effective n = s^2 / V_unit
    out["n_eff"] = {k: (float(s2 / out[k][2]) if out[k][2] and out[k][2] > 0 else None)
                    for k in ("naive_directions_boot", "pair_cluster_boot", "target_cluster_boot",
                              "source_cluster_boot", "pigeonhole_boot", "cgm_twoway_t4",
                              "dyadic_robust_t4", "loro_jackknife_t4")}
    return out


UNITS = ["naive_directions_boot", "pair_cluster_boot", "target_cluster_boot",
         "source_cluster_boot", "pigeonhole_boot", "cgm_twoway_t4", "dyadic_robust_t4",
         "loro_jackknife_t4"]


def quantities():
    tb = pd.DataFrame(json.load(open(E.PAPER / "transfer_ci_blocksize.json")))
    tb["src"] = tb.direction.str.split("_to_").str[0]
    tb["tgt"] = tb.direction.str.split("_to_").str[1]
    af = pd.read_csv(E.PAPER / "aoi_frame_transfer_frozen_mugla.csv")
    af["src"] = af.direction.str.split("_to_").str[0]
    af["tgt"] = af.direction.str.split("_to_").str[1]
    eq = af[(af.source_frame == "10km") & (af.target_frame == "10km")]
    e5 = af[(af.source_frame == "5km") & (af.target_frame == "5km")]
    ff = af[(af.source_frame == "full") & (af.target_frame == "full")]
    return {
        "Q1_asdrawn_delta": (tb.point_delta.to_numpy(), tb.src.to_numpy(), tb.tgt.to_numpy(), 0.0),
        "Q2_equalised10_delta": (eq.delta.to_numpy(), eq.src.to_numpy(), eq.tgt.to_numpy(), 0.0),
        "Q3_equalised10_mean_transfer": (eq.thermal.to_numpy(), eq.src.to_numpy(),
                                         eq.tgt.to_numpy(), 0.5),
        "S_asdrawn_delta_frozen_refit": (ff.delta.to_numpy(), ff.src.to_numpy(),
                                         ff.tgt.to_numpy(), 0.0),
        "S_equalised5_delta": (e5.delta.to_numpy(), e5.src.to_numpy(), e5.tgt.to_numpy(), 0.0),
    }


if __name__ == "__main__":
    res = {}
    for name, (y, s, t, null) in quantities().items():
        r = intervals(y, s, t)
        r["null"] = null
        r["verdicts"] = {}
        for u in UNITS:
            lo, hi = r[u][0], r[u][1]
            r["verdicts"][u] = ("undefined" if np.isnan(lo) else
                                ("excludes" if (lo > null or hi < null) else "spans"))
        res[name] = r
        print(f"\n== {name}: mean {r['mean']:+.4f} (null {null})")
        for u in UNITS:
            lo, hi, v = r[u]
            ne = r["n_eff"][u]
            print(f"  {u:24s} [{lo:+.4f}, {hi:+.4f}]  n_eff {ne if ne is None else round(ne, 1)}"
                  f"  {r['verdicts'][u]}")
        print("  LORO means", {k: round(v, 4) for k, v in r["loro_means"].items()})
    json.dump(res, open(E.OUTDIR / "units.json", "w"), indent=1, default=float)
