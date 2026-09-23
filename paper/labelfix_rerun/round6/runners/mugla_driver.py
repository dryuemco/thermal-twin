"""Muğla subsampling in a re-freeze tree. Only in-process change: CANONICAL_STEP8A_SHA256['manavgat_2021'] is set to
the SHA-256 COMPUTED from this tree's Manavgat step8a parquet. The repo literal is 054a1961 (frozen 79-column
file); the refreeze trees hold the 80-column HEAD file, hash 5a5e876c official / 607a6359 control. The Muğla and
Bejís digests are untouched and still enforced. Then the module's own validator.
Usage: mugla_driver.py <tree>"""
import sys, os, json, hashlib
sys.dont_write_bytecode = True
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); os.chdir(tree); sys.path.insert(0, str(tree))
import src.mugla_subsampling as ms
p = tree / "outputs/experiments/manavgat_2021/step8a/step8a_500m_modeling_dataset.parquet"
h = hashlib.sha256(p.read_bytes()).hexdigest()
print("manavgat step8a sha256 (computed):", h, "| repo literal:", ms.CANONICAL_STEP8A_SHA256["manavgat_2021"])
ms.CANONICAL_STEP8A_SHA256["manavgat_2021"] = h
res = ms.run_analysis(force=True)
print(json.dumps(res, indent=1, default=str)[:3000])
sys.argv = [sys.argv[0]]; sys.path.insert(0, str(tree / "scripts"))
import validate_mugla_subsampling as v
rep = v.run_validation()
print("VALIDATION:", json.dumps({k: rep.get(k) for k in ("overall_status", "status", "n_pass", "n_fail")}, default=str))
fails = [c for c in rep.get("checks", []) if str(c.get("status")) not in ("PASS", "True")]
print(json.dumps(fails, indent=1, default=str)[:4000]); print("MUGLA_DRIVER_DONE")
