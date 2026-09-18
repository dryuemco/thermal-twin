"""EMS referee round, R2 major 3: the frame-matched hardening ladder. SPEC: ems_analyses/inference/SPEC.md.

Fits (all canonical data, TSG population, the paper's RF):
  * blocked CV (B = 10 and 2) on the full frame, the 10 km collar, and (B = 10) the 5 km collar;
    full-frame OOF predictions are also scored on every scar area (scar + 2 km);
  * leave-one-scar-out on the full frame and on the 10 km collar;
  * half-split (positive_control.py) on the full frame and on the 10 km collar;
  * foreign full-frame source models scored on every scar area.
Writes ladder_raw.json (every per-unit number) and ladder_summary.json.
"""
import json
import time

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

import ems_inference_common as E

T0 = time.time()


def log(*a):
    print(f"[{time.time()-T0:7.0f}s]", *a, flush=True)


def frame(d, tag):
    return d if tag == "full" else d[d.dist_km <= {"10km": 10, "5km": 5}[tag]].reset_index(drop=True)


data = {r: E.load(r) for r in E.REGIONS}
raw = {"blocked": [], "blocked_scar": [], "loso": [], "halfsplit": [], "foreign": []}

# ------------------------------------------------------------------ scar areas (full frame)
scar_sets = {}
for r in E.REGIONS:
    d = data[r]
    scar_sets[r] = [(s, held) for s, held in E.scars(d)]
    log(r, "scars", [(s, int(h.sum()), int(d.burned[h].sum())) for s, h in scar_sets[r]])

# ------------------------------------------------------------------ blocked CV
for tag, Bs in (("full", (10, 2)), ("10km", (10, 2)), ("5km", (10,))):
    for r in E.REGIONS:
        d = frame(data[r], tag)
        for B in Bs:
            oof = {lbl: E.blocked_oof(d, fe, B) for lbl, fe in (("baseline", E.BASELINE),
                                                                  ("thermal", E.THERMAL))}
            a = {lbl: float(roc_auc_score(d.burned, oof[lbl])) for lbl in oof}
            raw["blocked"].append({"frame": tag, "B": B, "region": r, "n": int(len(d)),
                                   "pos": int(d.burned.sum()), **a,
                                   "increment": a["thermal"] - a["baseline"]})
            log("blocked", tag, B, r, f"{a['baseline']:.4f} {a['thermal']:.4f} "
                f"{a['thermal']-a['baseline']:+.4f}")
            if tag == "full":
                for s, held in scar_sets[r]:
                    y = d.burned[held]
                    if y.nunique() < 2:
                        continue
                    b = {lbl: float(roc_auc_score(y, oof[lbl][held])) for lbl in oof}
                    raw["blocked_scar"].append({"B": B, "region": r, "scar": s, **b,
                                                "increment": b["thermal"] - b["baseline"]})

# ------------------------------------------------------------------ leave-one-scar-out
for tag in ("full", "10km"):
    for r in E.REGIONS:
        d = data[r]
        keep = np.ones(len(d), bool) if tag == "full" else (d.dist_km <= 10).to_numpy()
        for s, held in scar_sets[r]:
            tgt = d[held & keep]
            src = d[~held & keep]
            lost = int((held & ~keep).sum())
            if tgt.burned.nunique() < 2 or src.burned.nunique() < 2:
                continue
            out = {"frame": tag, "region": r, "scar": s, "src_pos": int(src.burned.sum()),
                   "tgt_pos": int(tgt.burned.sum()), "tgt_n": int(len(tgt)),
                   "target_cells_lost_to_collar": lost}
            for lbl, fe in (("baseline", E.BASELINE), ("thermal", E.THERMAL)):
                out[lbl] = float(roc_auc_score(tgt.burned,
                                               E.fit(fe, src).predict_proba(tgt[fe])[:, 1]))
            out["increment"] = out["thermal"] - out["baseline"]
            raw["loso"].append(out)
            log("loso", tag, r, s, f"{out['increment']:+.4f}", "lost", lost)

# ------------------------------------------------------------------ half-split
for tag in ("full", "10km"):
    for r in E.REGIONS:
        df = frame(data[r], tag)
        for axis, col in (("east_west", "col_500m"), ("north_south", "row_500m")):
            cut = df[col].median()
            a, b = df[df[col] <= cut], df[df[col] > cut]
            for src, tgt, name in ((a, b, "low_to_high"), (b, a, "high_to_low")):
                row = {"frame": tag, "region": r, "axis": axis, "direction": name,
                       "src_pos": int(src.burned.sum()), "tgt_pos": int(tgt.burned.sum())}
                if src.burned.nunique() < 2 or tgt.burned.nunique() < 2:
                    row["skipped"] = True
                    raw["halfsplit"].append(row)
                    continue
                for lbl, fe in (("baseline", E.BASELINE), ("thermal", E.THERMAL)):
                    row[lbl] = float(roc_auc_score(tgt.burned,
                                                   E.fit(fe, src).predict_proba(tgt[fe])[:, 1]))
                row["increment"] = row["thermal"] - row["baseline"]
                raw["halfsplit"].append(row)
                log("half", tag, r, axis, name, f"{row['increment']:+.4f}")

# ------------------------------------------------------------------ foreign on scar areas
models = {r: {lbl: E.fit(fe, data[r]) for lbl, fe in (("baseline", E.BASELINE),
                                                      ("thermal", E.THERMAL))}
          for r in E.REGIONS}
for r in E.REGIONS:
    d = data[r]
    for s, held in scar_sets[r]:
        tgt = d[held]
        if tgt.burned.nunique() < 2:
            continue
        for o in E.REGIONS:
            if o == r:
                continue
            row = {"region": r, "scar": s, "source": o}
            for lbl, fe in (("baseline", E.BASELINE), ("thermal", E.THERMAL)):
                row[lbl] = float(roc_auc_score(tgt.burned,
                                               models[o][lbl].predict_proba(tgt[fe])[:, 1]))
            row["increment"] = row["thermal"] - row["baseline"]
            raw["foreign"].append(row)
    log("foreign done", r)

json.dump(raw, open(E.OUTDIR / "ladder_raw.json", "w"), indent=1)
log("wrote ladder_raw.json")
