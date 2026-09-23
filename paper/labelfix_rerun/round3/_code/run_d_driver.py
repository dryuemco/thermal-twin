"""Round 3: step10/run_d_within_robustness.main() with (i) RF n_jobs=4 in config10 (output does not depend on
n_jobs), (ii) run_d's EXPERIMENTS_DIR / CROSS_REGION_DIR redirected in-process to a scratch tree so nothing
committed under thermal-twin-main/experiments is overwritten. The scratch tree holds the step8e references
run_d checks its block-2 reproduction against: Manavgat = the step8e report regenerated (report-only) in the
corrected pipeline tree; Bejis = the committed frozen copy (Bejis is unaffected by the correction).
Usage: run_d_driver.py <scratch_experiments_dir>"""
import sys
from pathlib import Path
X = Path(sys.argv[1])
sys.path.insert(0, r"C:\Users\CORSAIR\projects\thermal-twin-main\step10")
import config10
for name in dir(config10):
    v = getattr(config10, name)
    if isinstance(v, dict) and "n_jobs" in v:
        v["n_jobs"] = 4
import run_d_within_robustness as m
m.EXPERIMENTS_DIR = X
m.CROSS_REGION_DIR = X / "cross_region"
m.main()
