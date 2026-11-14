"""buffer_coverage.py: coverage of the buffered validation of claim 1, written as a versioned analysis output.

For every buffer (1, 2, 5, 10 km) and fire of the primary set: the number of population cells, the number
scored (folds skipped for too few training cells leave their test cells unscored) and the SHA-256 of the
prediction cache file used, beside the SHA-256 of the fire's step8a table. The manuscript build reads this
file and never the cache.

Writes buffer_coverage.json in $THERMAL_TWIN_SCALEUP/analysis.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def table_path(fid):
    return A.C.path(fid) if fid in A.PAPER_REGIONS else A.find_scaleup(fid)


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    out = {"tables_sha256": {fid: sha(table_path(fid)) for fid in ids}, "buffers": {}}
    for b in A.BUFFERS_KM:
        per = {}
        for fid in ids:
            f = F[fid]
            c = f._cache(f"buffer{b}_b10")
            assert c.exists(), c
            o = np.load(c)[0]
            assert len(o) == f.n, (fid, b)
            per[fid] = {"cells": int(f.n), "cells_scored": int(np.isfinite(o).sum()), "cache_sha256": sha(c)}
        tot = sum(v["cells"] for v in per.values())
        sc = sum(v["cells_scored"] for v in per.values())
        out["buffers"][f"{b}_km"] = {"cells_total": tot, "cells_scored": sc,
                                     "fires_with_scored_cells": sum(v["cells_scored"] > 0 for v in per.values()), "per_fire": per}
    (A.OUT / "buffer_coverage.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print({k: (v["cells_scored"], v["cells_total"], v["fires_with_scored_cells"]) for k, v in out["buffers"].items()})


if __name__ == "__main__":
    main()
