"""Pair large-block robustness v1 (TSG) and the all_valid variant for manavgat+bejis.
The all_valid module hard-codes V1_EXPECTED_ANALYSIS_ID (the analysis_id of the frozen v1 run);
the v1 analysis_id is a hash that includes absolute input paths and input hashes, so a re-run in
any staging tree necessarily has a new id. The ONLY patch: set it, in-process, to the id the v1 run
in this same tree just wrote. Nothing else is changed. Usage: largeblock.py <tree>"""
import sys, os, json
sys.dont_write_bytecode = True
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
os.chdir(tree); sys.path.insert(0, str(tree))
from scripts.run_step8_large_block_robustness import main as v1
r1 = v1(experiments=["manavgat_2021", "bejis_2022"], block_sizes_cells=[10, 20], force=True)
print("V1:", json.dumps(r1, default=str)[:1500])
import src.step8_large_block_robustness_primary_all_valid as av
rep = json.loads((av.V1_OUTPUT_ROOT / "step8_large_block_final_report.json").read_text())
print("PATCH V1_EXPECTED_ANALYSIS_ID", av.V1_EXPECTED_ANALYSIS_ID, "->", rep["analysis_id"])
av.V1_EXPECTED_ANALYSIS_ID = rep["analysis_id"]
g = av.run_analysis(force=True, run_large_block_fit=False)
print("GATE:", json.dumps(g, default=str)[:2000])
if g.get("blocked"):
    sys.exit("equivalence gate failed")
r2 = av.run_analysis(force=True, run_large_block_fit=True)
print("ALLVALID:", json.dumps(r2, default=str)[:1500])
