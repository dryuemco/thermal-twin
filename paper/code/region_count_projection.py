"""What would more regions do to Contribution 2's portability null?

NOT A RESULT. This is a projection from the five regions actually analysed. It
asks one question: if regions beyond these five behave like these five, how wide
would the interval on the equalised paired thermal delta be at k regions, and
would it still contain zero?

Design. Each ordered direction i->j carries a paired delta. A direction's value
is modelled as a source effect, a target effect and a residual,

    delta_ij = mu + a_i + b_j + e_ij,

whose variance components are estimated from the twenty observed directions by
the usual moment identities. New regions are then drawn with those components,
every ordered pair among k regions is formed, and the paper's own pair-cluster
bootstrap is run on the simulated matrix. Repeating gives the distribution of
interval widths and the share of runs whose interval excludes zero.

Two assumptions are doing real work and neither is a fact:
  1. mu is taken to be the observed +0.023. If the truth is nearer zero, no
     number of regions produces an interval that excludes it.
  2. new regions are exchangeable with these five. The five were not sampled at
     random from anything, so this is a modelling convenience.

Read the output as "what precision would buy", not as "what we would find".

Usage:  python paper/code/region_count_projection.py [replicates]
"""
import csv
import statistics as st
import sys
from collections import defaultdict

import os

import numpy as np

SRC = os.path.join(os.environ.get("PAPER_ARTEFACTS", "paper"), "aoi_frame_transfer_frozen_mugla.csv")
FRAME = ("10km", "10km")          # the equalised frame the claim is made on
REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
SEED = 42
KS = [5, 6, 8, 10, 12]


def observed():
    """Per-direction paired delta on the equalised frame."""
    out = {}
    for r in csv.DictReader(open(SRC, encoding="utf-8")):
        if (r["source_frame"], r["target_frame"]) != FRAME:
            continue
        s, t = r["direction"].split("_to_")
        out[(s, t)] = float(r["thermal"]) - float(r["baseline"])
    return out


def components(d):
    """mu, and the source, target and residual standard deviations."""
    vals = list(d.values())
    mu = st.mean(vals)
    src, tgt = defaultdict(list), defaultdict(list)
    for (s, t), v in d.items():
        src[s].append(v); tgt[t].append(v)
    # variance of the region means, corrected for the averaging of residuals
    def comp(groups):
        means = [st.mean(v) for v in groups.values()]
        m = max(st.variance(means) - st.variance(vals) / len(next(iter(groups.values()))), 0.0)
        return m ** 0.5
    sa, sb = comp(src), comp(tgt)
    resid = max(st.variance(vals) - sa ** 2 - sb ** 2, 1e-12) ** 0.5
    return mu, sa, sb, resid


def pair_cluster_ci(delta, rng, nboot=1000):
    """The paper's unit: resample unordered region pairs, both directions together."""
    pairs = defaultdict(list)
    for (s, t), v in delta.items():
        pairs[tuple(sorted((s, t)))].append(v)
    keys = list(pairs)
    means = np.empty(nboot)
    for b in range(nboot):
        pick = rng.integers(0, len(keys), len(keys))
        vals = [v for i in pick for v in pairs[keys[i]]]
        means[b] = np.mean(vals)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def main() -> None:
    d = observed()
    mu, sa, sb, se = components(d)
    lo, hi = pair_cluster_ci(d, np.random.default_rng(SEED))
    print(f"  observed, {len(d)} directions from 5 regions")
    print(f"    mean paired delta      {mu:+.4f}")
    print(f"    pair-cluster 95% CI    [{lo:+.4f}, {hi:+.4f}]   width {hi-lo:.4f}"
          f"   {'excludes 0' if lo > 0 or hi < 0 else 'contains 0'}")
    print(f"    source sd {sa:.4f}   target sd {sb:.4f}   residual sd {se:.4f}")
    print()
    print(f"  projection, {REPS} simulated cohorts per k, mu held at the observed value")
    print(f"  {'k':>3s} {'directions':>11s} {'median width':>13s} {'excludes 0':>11s}")
    rng = np.random.default_rng(SEED)
    for k in KS:
        widths, excl = [], 0
        for _ in range(REPS):
            a = rng.normal(0, sa, k); b = rng.normal(0, sb, k)
            sim = {}
            for i in range(k):
                for j in range(k):
                    if i == j:
                        continue
                    sim[(f"r{i}", f"r{j}")] = mu + a[i] + b[j] + rng.normal(0, se)
            l, h = pair_cluster_ci(sim, rng, nboot=1000)
            widths.append(h - l)
            excl += (l > 0 or h < 0)
        print(f"  {k:3d} {k*(k-1):11d} {st.median(widths):13.4f} {excl/REPS:10.0%}")
    print()
    print("  A projection, not a finding. It assumes the observed mean is the truth and that")
    print("  further regions behave like these five; neither is established.")


if __name__ == "__main__":
    main()
