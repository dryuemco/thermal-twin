"""G1 check (PLAN_R4.md): the control arm reproduces the frozen artefact, ALL rows.
Usage: g1_check.py <frozen_dir> <control_dir> <relpath> [relpath ...] [--tol=1e-5]
CSVs: aligned by row order, same shape and columns required; numeric max|diff| <= tol, text columns equal.
Columns whose names say they hold paths/hashes/ids/timestamps are reported, not failed (they encode the
machine and the analysis id, which hashes absolute paths)."""
import sys, re
import pandas as pd
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--tol=")]
tol = float(next((a[6:] for a in sys.argv[1:] if a.startswith("--tol=")), 1e-5))
F, C, rels = Path(args[0]), Path(args[1]), args[2:]
VOLATILE = re.compile(r"path|sha|hash|analysis_id|created|timestamp|_utc|root|dir$|file$", re.I)
fail = False
for rel in rels:
    a, b = pd.read_csv(F / rel), pd.read_csv(C / rel)
    if a.shape != b.shape or list(a.columns) != list(b.columns):
        print(f"FAIL {rel}: shape/columns {a.shape} vs {b.shape}"); fail = True; continue
    isnum = lambda s: pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s)
    num = [c for c in a.columns if isnum(a[c]) and isnum(b[c])]
    d = max([float(((a[c] - b[c]).abs().where(~(a[c].isna() & b[c].isna()), 0)).fillna(float("inf")).max())
             for c in num] or [0.0])
    txt = [c for c in a.columns if c not in num]
    neq = [c for c in txt if not a[c].astype(str).equals(b[c].astype(str))]
    hard = [c for c in neq if not VOLATILE.search(c)]
    ok = d <= tol and not hard
    fail |= not ok
    print(f"{'PASS' if ok else 'FAIL'} {rel}: max|diff| {d:.3g} ({len(num)} num cols); text diffs {hard}"
          + (f"; volatile text diffs (ignored) {[c for c in neq if c not in hard]}" if len(neq) > len(hard) else ""))
print("G1", "FAIL" if fail else "PASS")
sys.exit(1 if fail else 0)
