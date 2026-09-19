"""Runs step10/run_e_coral_lambda_sensitivity.main() with RF n_jobs=4 (shared machine; RF output
does not depend on n_jobs). Labelfix re-run, 2026-09-19."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "step10"))
import config10
for name in dir(config10):
    v = getattr(config10, name)
    if isinstance(v, dict) and "n_jobs" in v:
        v["n_jobs"] = 4
import run_e_coral_lambda_sensitivity as m
m.main()
