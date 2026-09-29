"""WS4 blocker check (2026-09-29): recompute Table 1 Manavgat rows from the corrected, SHA-verified
parquet with step10's own functions (import, don't reimplement). Writes nothing under thermal-twin-main."""
import os, sys, json
os.environ["THERMAL_TWIN_LABELS"] = "corrected"
MAIN = r"C:\Users\CORSAIR\projects\thermal-twin-main"
sys.path[:0] = [MAIN + r"\step10", MAIN + r"\paper\code"]
os.chdir(MAIN)
import _canonical, config10
for name in dir(config10):
    v = getattr(config10, name)
    if isinstance(v, dict) and "n_jobs" in v: v["n_jobs"] = 4
from data_io import add_spatial_block_id, load_region
from metrics import roc_pr
from spatial_bootstrap import delta_block_bootstrap_ci
from within_cv import run_oof
p = _canonical.path("manavgat_2021"); sha = _canonical.sha256(p)
print("input", p, sha)
assert sha.startswith("e4ab8b85") or sha.startswith("5a5e876c"), sha
PRINTED = {2: (0.841, 0.908, 0.067, 0.060, 0.073), 10: (0.820, 0.882, 0.062, 0.040, 0.082), 20: (0.798, 0.845, 0.047, 0.016, 0.081)}
df = load_region("manavgat_2021", population=config10.PRIMARY_POPULATION)
print("n", len(df), "burned", int(df.burned.sum()))
out = {"input": str(p), "sha256": sha, "n": len(df), "burned": int(df.burned.sum()), "rows": {}}
ok = True
for k in (2, 10, 20):
    b = add_spatial_block_id(df, k).to_numpy()
    oof = run_oof(df, b)
    mb, mt = roc_pr(oof["y"], oof["oof_baseline"]), roc_pr(oof["y"], oof["oof_thermal"])
    d = delta_block_bootstrap_ci(oof["y"], oof["oof_baseline"], oof["oof_thermal"], b, n_bootstrap=config10.N_BOOTSTRAP, seed=config10.SEED)
    got = (mb["roc_auc"], mt["roc_auc"], mt["roc_auc"] - mb["roc_auc"], *d["delta_auc_ci95"])
    match = all(abs(round(g, 3) - e) < 1e-9 for g, e in zip(got, PRINTED[k]))
    ok &= match
    out["rows"][k] = {"got": got, "printed": PRINTED[k], "match_3dp": match, "n_blocks": oof["n_blocks"]}
    print(k, [round(g, 4) for g in got], "printed", PRINTED[k], "MATCH" if match else "DIFF")
out["all_match"] = ok
json.dump(out, open(r"C:\Users\CORSAIR\projects\thermal-twin\scratch\verify_20260929\table1_manavgat.json", "w"), indent=1)
print("ALL MATCH" if ok else "MISMATCH")
