"""Table 2 summaries from matched_holdout.json, as the manuscript defines them (Section 4.3):
means and Student t over the scars that have row C; region-clustered t over region means."""
import json, sys
import numpy as np, pandas as pd
from scipy import stats

def t(v):
    v = np.asarray(v, float); n = len(v); m = v.mean()
    h = stats.t.ppf(0.975, n - 1) * v.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
    return m, m - h, m + h, n

for path in sys.argv[1:]:
    d = pd.DataFrame(json.load(open(path)))
    print("==", path)
    print(d.to_string())
    s = d[d.C_unseen_same_region.notna()]
    print(f"scars with row C: {len(s)}  regions: {s.region.value_counts().to_dict()}")
    for k in ["A_region_blocked", "B_seen_same_cells", "C_unseen_same_region", "D_foreign"]:
        m, lo, hi, n = t(s[k]); print(f"  {k:22s} {m:.3f} [{lo:.3f}, {hi:.3f}] n={n}")
    for a, b in [("A_region_blocked", "B_seen_same_cells"), ("A_region_blocked", "C_unseen_same_region"),
                 ("B_seen_same_cells", "C_unseen_same_region"), ("C_unseen_same_region", "D_foreign")]:
        x = s[a] - s[b]; m, lo, hi, n = t(x)
        g = x.groupby(s.region).mean(); mc, loc, hic, nc = t(g)
        print(f"  {a[0]}-{b[0]} scar-t {m:+.3f} [{lo:+.3f}, {hi:+.3f}] n={n} | region-clustered {mc:+.3f} [{loc:+.3f}, {hic:+.3f}] G={nc} width ratio {(hic-loc)/(hi-lo):.2f}")
    ab = (s.A_region_blocked - s.B_seen_same_cells).mean(); ac = (s.A_region_blocked - s.C_unseen_same_region).mean()
    print(f"  (A-B)/(A-C) = {ab/ac:.3f}")
