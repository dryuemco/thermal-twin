"""Few-shot recovery driver (round 3). Usage: fsr_driver.py <tree_root> <corrected|control>
Runs src.few_shot_recovery.run_analysis(force=True) inside a staging tree (cwd = tree, PROJECT_ROOT = tree),
then the module's own validator in the same process.
Only in-process change (corrected tree only): FROZEN_CEILING_REFERENCE['manavgat_2021']['roc_auc'] is set to
the block-10 values READ from the same tree's corrected large-block run (not typed); the task-stated
values 0.82032 / 0.88222 are asserted to 5 dp as a guard."""
import sys, os, json
sys.dont_write_bytecode = True
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); arm = sys.argv[2]
os.chdir(tree); sys.path.insert(0, str(tree))
import src.few_shot_recovery as fsr
ref = fsr.FROZEN_CEILING_REFERENCE["manavgat_2021"]
m = json.loads((tree / ref["metrics_path"]).read_text(encoding="utf-8"))
print("tree ceiling file:", ref["metrics_path"], "baseline", m["baseline_roc_auc"], "thermal", m["thermal_roc_auc"])
print("module reference before:", ref["roc_auc"], "hash:", fsr.CANONICAL_STEP8A_SHA256["manavgat_2021"])
if arm == "corrected":
    assert round(m["baseline_roc_auc"], 5) == 0.82032 and round(m["thermal_roc_auc"], 5) == 0.88222, m
    ref["roc_auc"] = {"baseline": m["baseline_roc_auc"], "thermal": m["thermal_roc_auc"]}
    print("PATCHED FROZEN_CEILING_REFERENCE[manavgat_2021].roc_auc ->", ref["roc_auc"])
else:
    assert fsr.CANONICAL_STEP8A_SHA256["manavgat_2021"].startswith("054a1961"), "control tree must keep frozen hash"
res = fsr.run_analysis(force=True)
print(json.dumps(res, indent=1, default=str)[:4000])
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(tree / "scripts"))
import validate_few_shot_recovery as v
payload = v.run_validation()
if payload.get("namespace"):
    fsr._atomic_write_text(Path(payload["namespace"]) / "validation_report.json", fsr._json_document(payload))
fails = [c for c in payload.get("checks", []) if c.get("status") not in ("PASS", True)]
print("OVERALL STATUS:", payload["overall_status"], "namespace:", payload.get("namespace"))
print(json.dumps([c for c in payload.get("checks", []) if str(c.get("status")) != "PASS"], indent=1, default=str)[:6000])
print("FSR_DRIVER_DONE")
