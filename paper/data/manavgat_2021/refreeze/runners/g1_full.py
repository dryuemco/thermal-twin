"""Stage A, G1: control arm (frozen label) vs drive_new, every CSV and JSON in the re-freeze scope.
CSV: aligned by row order; numeric max|diff| and text equality (volatile path/hash/time columns ignored).
JSON: flattened; numeric leaves compared where the key exists in both; keys new in HEAD are counted, not failed.
Usage: g1_full.py <control_tree> <drive_new> <out.json> [tol]"""
import sys, json, math, re
from pathlib import Path
import pandas as pd

ctrl, dn, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
TOL = float(sys.argv[4]) if len(sys.argv) > 4 else 1e-5
VOL = re.compile(r"path|sha|hash|time|created|generated|root|dir|file|_at|_utc|version|python|platform|host|analysis_id|git", re.I)
PAIRS = ["manavgat_2021__bejis_2022", "manavgat_2021__mugla_2021", "manavgat_2021__evia_2021_extended",
         "mugla_2021__manavgat_2021", "montiferru_2021__manavgat_2021", "manavgat_2021__evia_2021"]
SCOPE = [f"experiments/manavgat_2021/{s}" for s in ("step8b", "step8c", "step8d", "step8e", "robustness")] + \
        ["robustness/step8_large_block", "robustness/step8_large_block_primary_all_valid"] + \
        [f"cross_region/{p}" for p in PAIRS]


def flat(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, f"{p}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flat(v, f"{p}[{i}]")
    else:
        yield p, o


rows = []
for s in SCOPE:
    cd, fd = ctrl / "outputs" / s, dn / s
    if not cd.exists():
        rows.append({"scope": s, "file": None, "status": "MISSING_IN_CONTROL"}); continue
    for f in sorted(cd.rglob("*")):
        if f.suffix not in (".csv", ".json") or not f.is_file():
            continue
        rel = f.relative_to(cd); g = fd / rel
        r = {"scope": s, "file": rel.as_posix()}
        if not g.exists():
            r["status"] = "NEW_IN_HEAD"; rows.append(r); continue
        try:
            if f.suffix == ".csv":
                a, b = pd.read_csv(g, low_memory=False), pd.read_csv(f, low_memory=False)
                if a.shape != b.shape:
                    r.update(status="SHAPE", frozen=list(a.shape), control=list(b.shape)); rows.append(r); continue
                num = [c for c in a.columns if c in b and pd.api.types.is_numeric_dtype(a[c]) and not pd.api.types.is_bool_dtype(a[c]) and pd.api.types.is_numeric_dtype(b[c])]
                d = max([float(((a[c] - b[c]).abs().where(~(a[c].isna() & b[c].isna()), 0)).fillna(math.inf).max()) for c in num] or [0.0])
                txt = [c for c in a.columns if c not in num and c in b and not VOL.search(c) and not a[c].astype(str).equals(b[c].astype(str))]
                r.update(max_abs_diff=d, text_diff_cols=txt, status="PASS" if d <= TOL and not txt else "FAIL")
            else:
                A = dict(flat(json.loads(g.read_text(encoding="utf-8"))))
                B = dict(flat(json.loads(f.read_text(encoding="utf-8"))))
                d, txt, new = 0.0, [], 0
                for k, v in B.items():
                    if k not in A:
                        new += 1; continue
                    u = A[k]
                    if isinstance(v, (int, float)) and isinstance(u, (int, float)) and not isinstance(v, bool) and not isinstance(u, bool):
                        if not (math.isnan(float(u)) and math.isnan(float(v))):
                            d = max(d, abs(float(u) - float(v)))
                    elif u != v and not VOL.search(k):
                        txt.append(k)
                missing = [k for k in A if k not in B]
                r.update(max_abs_diff=d, text_diff_keys=txt[:20], n_text_diff=len(txt), new_keys_in_head=new,
                         frozen_keys_missing=len(missing), status="PASS" if d <= TOL and not txt and not missing else "FAIL")
        except Exception as e:  # noqa: BLE001
            r.update(status="ERROR", error=f"{type(e).__name__}: {e}")
        rows.append(r)

summ = {}
for r in rows:
    summ.setdefault(r["scope"], {"PASS": 0, "FAIL": 0, "NEW_IN_HEAD": 0, "other": 0, "max_abs_diff": 0.0})
    k = r["status"] if r["status"] in ("PASS", "FAIL", "NEW_IN_HEAD") else "other"
    summ[r["scope"]][k] += 1
    summ[r["scope"]]["max_abs_diff"] = max(summ[r["scope"]]["max_abs_diff"], r.get("max_abs_diff") or 0.0)
res = {"tolerance": TOL, "overall": "PASS" if all(v["FAIL"] == 0 and v["other"] == 0 for v in summ.values()) else "FAIL",
       "by_scope": summ, "failures": [r for r in rows if r["status"] not in ("PASS", "NEW_IN_HEAD")]}
out.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
print(json.dumps({k: v for k, v in res.items() if k != "failures"}, indent=1))
print("n_failures", len(res["failures"]))
for r in res["failures"][:40]:
    print(" ", r)
