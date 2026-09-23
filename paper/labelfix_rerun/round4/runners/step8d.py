"""Run the pipeline's run_step8d(ctx) for one experiment inside a staging tree (same pattern as
_runners/step8bc.py). Usage: step8d.py <tree> <experiment_id>"""
import sys, os
sys.dont_write_bytecode = True
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); exp = sys.argv[2]
os.chdir(tree); sys.path.insert(0, str(tree))
from core.experiment_context import build_experiment_context
from src.step8d_thermal_feature_ablation import run_step8d
ctx = build_experiment_context(exp)
assert str(ctx["step8d_output_dir"]).startswith(str(tree)), ctx["step8d_output_dir"]
print(run_step8d(ctx=ctx, force=True))
print("STEP8D_DONE")
