"""field_checks.py: plan 8.6 (G4). Realised correlation of the simulated field against distance (0.5 to 40 km) in
five fires of different size, against exp(-r/L), with padding 2x (as used) and 4x. 20 fields per setting, pair
sample of up to 200,000 cell pairs per field, distance bins of 1 km. Writes field_checks.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402


def grf(f, L, rng, pad):
    km_ns = A.CELL_DEG * A.M_PER_DEG / 1000.0
    km_ew = km_ns * np.cos(np.radians(f.meta["lat"]))
    H, W = pad * (f.rr.max() + 1), pad * (f.cc.max() + 1)
    kx, ky = np.fft.fftfreq(H, d=km_ns), np.fft.fftfreq(W, d=km_ew)
    k2 = (kx[:, None] ** 2 + ky[None, :] ** 2) * (2 * np.pi) ** 2
    spec = 2 * np.pi * L ** 2 / (1 + k2 * L ** 2) ** 1.5
    v = np.real(np.fft.ifft2(np.fft.fft2(rng.standard_normal((H, W))) * np.sqrt(spec)))[f.rr, f.cc]
    return (v - v.mean()) / v.std()


def main():
    F = A.load_fires()
    ids = sorted([i for i in F if i != "montiferru_2021"], key=lambda i: F[i].n)
    pick = [ids[int(q * (len(ids) - 1))] for q in (0, 0.25, 0.5, 0.75, 1.0)]
    edges = np.arange(0.5, 41, 1.0)
    out = {}
    for fid in pick:
        f = F[fid]
        ext = float(np.ptp(f.xy[:, 0]) + np.ptp(f.xy[:, 1])) / 2
        out[fid] = {"cells": f.n, "mean_extent_km": ext}
        for L in (2, 10):
            for pad in (2, 4):
                rng = np.random.default_rng(7)
                sums = np.zeros(len(edges) - 1); cnts = np.zeros(len(edges) - 1)
                for _ in range(20):
                    v = grf(f, L, rng, pad)
                    i = rng.integers(0, f.n, 200_000); j = rng.integers(0, f.n, 200_000)
                    d = np.linalg.norm(f.xy[i] - f.xy[j], axis=1)
                    b = np.digitize(d, edges) - 1
                    ok = (b >= 0) & (b < len(edges) - 1)
                    np.add.at(sums, b[ok], v[i[ok]] * v[j[ok]]); np.add.at(cnts, b[ok], 1)
                corr = sums / np.maximum(cnts, 1)
                mid = (edges[:-1] + edges[1:]) / 2
                sel = [0, 1, 4, 9, 19, 39]
                out[fid][f"L{L}_pad{pad}"] = {f"{mid[k]:.1f}km": [round(float(corr[k]), 3), round(float(np.exp(-mid[k] / L)), 3)]
                                              for k in sel if k < len(mid) and cnts[k] > 100}
    (A.OUT / "field_checks.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
