"""G2 check (PLAN_R4.md): rows that do not involve Manavgat must equal the frozen canonical re-run.
Usage: g2_check.py <frozen_file> <corrected_file> [tol]
CSV or JSON (any list of flat dicts inside the JSON is compared). Rows are aligned by their non-numeric
fields. A row "involves Manavgat" if any string field contains 'manavgat'. Rows present in only one file, and
region-free rows (aggregates over regions), are listed, not failed: they may legitimately change."""
import sys, json, math, re
import pandas as pd

A, B = sys.argv[1], sys.argv[2]
TOL = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-5


def tables(path):
    if path.endswith(".csv"):
        return {"<csv>": pd.read_csv(path)}
    out = {}

    def walk(o, key):
        if isinstance(o, list) and o and all(isinstance(r, dict) for r in o):
            flat = [r for r in o if all(not isinstance(v, (dict, list)) for v in r.values())]
            if flat:
                out[key] = pd.DataFrame(flat)
        elif isinstance(o, dict):
            for k, v in o.items():
                walk(v, f"{key}.{k}")
    walk(json.load(open(path, encoding="utf-8")), "$")
    return out


ta, tb = tables(A), tables(B)
fail = False
for key in sorted(set(ta) | set(tb)):
    if key not in ta or key not in tb:
        print(f"[{key}] only in {'frozen' if key in ta else 'corrected'}"); continue
    a, b = ta[key], tb[key]
    isnum = lambda s: pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s)
    num = [c for c in a.columns if c in b.columns and isnum(a[c]) and isnum(b[c])]
    VOL = re.compile(r"path|sha|hash|analysis_id|created|timestamp|_utc|root|dir$|file$", re.I)
    keys = [c for c in a.columns if c in b.columns and c not in num and not VOL.search(c)]
    a, b = a.copy(), b.copy()
    man = lambda df: df[keys].astype(object).astype(str).apply(lambda r: r.str.contains("manavgat", case=False).any(), axis=1) \
        if keys else pd.Series(False, index=df.index)
    a, b = a.assign(_m=man(a).values), b.assign(_m=man(b).values)
    # region-free rows: none of the key fields names a region
    regionish = lambda df: df[keys].astype(object).astype(str).apply(
        lambda r: r.str.contains("manavgat|bejis|mugla|evia|montiferru|kozan", case=False, regex=True).any(), axis=1) if keys else pd.Series(False, index=df.index)
    a["_r"], b["_r"] = regionish(a).values, regionish(b).values
    a["_k"] = a[keys].astype(object).astype(str).agg(lambda r: "|".join(map(str, r)), axis=1) + "#" + a.groupby(keys, dropna=False).cumcount().astype(str) if keys else a.index.astype(str)
    b["_k"] = b[keys].astype(object).astype(str).agg(lambda r: "|".join(map(str, r)), axis=1) + "#" + b.groupby(keys, dropna=False).cumcount().astype(str) if keys else b.index.astype(str)
    m = a.merge(b, on="_k", suffixes=("_f", "_c"), how="outer", indicator=True)
    only = m[m["_merge"] != "both"]
    both = m[m["_merge"] == "both"]
    nonman = both[(~both["_m_f"].astype(bool)) & (both["_r_f"].astype(bool))]
    agg = both[~both["_r_f"].astype(bool)]
    worst, bad = 0.0, []
    for c in num:
        d = (nonman[f"{c}_f"] - nonman[f"{c}_c"]).abs()
        both_nan = nonman[f"{c}_f"].isna() & nonman[f"{c}_c"].isna()
        d = d.where(~both_nan, 0.0).fillna(math.inf)
        if len(d) and d.max() > worst:
            worst = float(d.max())
        for k, v in d[d > TOL].items():
            bad.append((nonman.at[k, "_k"], c, nonman.at[k, f"{c}_f"], nonman.at[k, f"{c}_c"]))
    # an unmatched non-Manavgat regional row means one of its text fields (e.g. a verdict) changed: fail
    for side in ("f", "c"):
        mm, rr = only[f"_m_{side}"], only[f"_r_{side}"]
        sel = only[(mm == False) & (rr == True)]  # noqa: E712 (NaN on the other side must not match)
        for k in sel.index:
            bad.append((only.at[k, "_k"], "<row only in " + ("frozen" if side == "f" else "corrected") + ">", "", ""))
    status = "PASS" if not bad else "FAIL"
    fail |= bool(bad)
    print(f"[{key}] {status}: non-Manavgat rows {len(nonman)}, max|diff| {worst:.3g}; Manavgat rows "
          f"{int(both['_m_f'].astype(bool).sum())}; region-free rows {len(agg)}; unmatched {len(only)}")
    for r in bad[:15]:
        print("   DIFF", r)
print("G2", "FAIL" if fail else "PASS")
sys.exit(1 if fail else 0)
