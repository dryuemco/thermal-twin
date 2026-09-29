"""
Stage the inputs feature_drop.py expects, so the anomaly-only feature set runs on
exactly the harness that already reproduces step9b and step8c.

That harness aborts unless its `full` configuration lands on the frozen numbers.
That is the reason for reusing it: a new feature set is only interpretable if the
reference arm computed beside it still reproduces the published result. The
reference values are therefore read from the frozen exports, never typed.

Read-only with respect to drive_new.
"""
import json
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\CORSAIR\projects\thermal-twin")
STAGING = Path(__file__).parent / "anomaly_staging"
STAGING.mkdir(exist_ok=True)

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
POP = "burnable_tree_shrub_grass"

for r in REGIONS:
    dst = STAGING / f"{r}.parquet"
    if not dst.exists():
        shutil.copy2(
            ROOT / "drive_new" / "experiments" / r / "step8a" / "step8a_500m_modeling_dataset.parquet",
            dst)
    print(f"staged {r}: {dst.stat().st_size/1e6:6.1f} MB")

# ---- transfer references, from every frozen step9b export -------------------
transfer = {}
for d in sorted((ROOT / "drive_new" / "cross_region").glob("*__*")):
    m = d / "step9b" / "cross_region_transfer_metrics.json"
    if not m.exists():
        continue
    doc = json.loads(m.read_text(encoding="utf-8"))
    for row in doc.get("results", []):
        if row.get("population") != POP or row.get("skipped"):
            continue
        src, tgt = row["source_experiment_id"], row["target_experiment_id"]
        tm = row.get("thermal_metrics") or {}
        auc = tm.get("roc_auc", tm.get("auc"))
        if auc is None:
            continue
        transfer[f"{src}_to_{tgt}"] = {"thermal": float(auc)}

print(f"\ntransfer references: {len(transfer)} directions")
for k in sorted(transfer):
    print(f"   {k:52s} {transfer[k]['thermal']:.4f}")

# ---- within-region references, from the frozen step8c -----------------------
within = {}
for r in REGIONS:
    hits = list((ROOT / "drive_new" / "experiments" / r).rglob("*step8c*.json"))
    for h in hits:
        try:
            doc = json.loads(h.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        found = None

        def walk(o):
            global found
            if found is not None:
                return
            if isinstance(o, dict):
                pop = o.get("population") or o.get("population_name")
                if pop == POP:
                    for key in ("thermal_roc_auc", "thermal_auc"):
                        if isinstance(o.get(key), (int, float)):
                            found = float(o[key]); return
                    tm = o.get("thermal_metrics") or o.get("thermal")
                    if isinstance(tm, dict):
                        v = tm.get("roc_auc", tm.get("auc"))
                        if isinstance(v, (int, float)):
                            found = float(v); return
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)

        walk(doc)
        if found is not None:
            within[r] = {"thermal_auc": found, "_source": h.name}
            break

print(f"\nwithin references: {len(within)}/5")
for r in REGIONS:
    print(f"   {r:24s} {within.get(r, {}).get('thermal_auc', 'MISSING')}")

(STAGING / "comparison_inputs.json").write_text(
    json.dumps({"transfer": transfer, "within": within}, indent=2), encoding="utf-8")
print(f"\nwrote {STAGING/'comparison_inputs.json'}")
