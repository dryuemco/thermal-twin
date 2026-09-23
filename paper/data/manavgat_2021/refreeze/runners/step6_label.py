"""Stage A, official tree only: the pipeline's own export_raw_mcd64a1_labels for manavgat_2021 (repo HEAD
6381f4c, which contains the 183be42 month-alignment fix), written to the tree's namespaced label dir.
Only runner-level change: GEE project 'thermaltwin' (repo default 'b7-thermal-digital-twin' is the pipeline
author's; this account has no role on it). Usage: step6_label.py <tree>"""
import sys, os, json
sys.dont_write_bytecode = True
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); os.chdir(tree); sys.path.insert(0, str(tree))
import src.step6_validate_fire_relation as s6
s6.GEE_PROJECT = "thermaltwin"
out = tree / "outputs/experiments/manavgat_2021/validation/labels"
r = s6.export_raw_mcd64a1_labels(experiment_id="manavgat_2021", output_dir=out)
print(json.dumps(r, default=str, indent=1)); print("STEP6_LABEL_DONE")
