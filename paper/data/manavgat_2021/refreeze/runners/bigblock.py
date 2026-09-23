"""Big-block robustness v2 for Manavgat (block 10, 20) via the pipeline runner's main()
with the v2 output_root keyword. Usage: bigblock.py <tree>"""
import sys, os, json
sys.dont_write_bytecode = True
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
os.chdir(tree); sys.path.insert(0, str(tree))
from scripts.run_step8_big_block_robustness import main
root = tree / "outputs/experiments/manavgat_2021/robustness/step8_big_blocks_v2"
print(json.dumps(main("manavgat_2021", [10, 20], force=True, output_root=root), indent=1, default=str)[:3000])
