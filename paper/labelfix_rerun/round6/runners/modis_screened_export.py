"""QC arm B input: the pipeline's own scripts/prepare_modis_for_step7.main(export=True) for manavgat_2021, with the
runner-level GEE project override 'thermaltwin'. The screened MODIS is label-free.
Usage: modis_screened_export.py <tree>"""
import sys, os, json
sys.dont_write_bytecode = True
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); os.chdir(tree); sys.path.insert(0, str(tree))
import core.config as cfg
cfg.GEE_PROJECT = "thermaltwin"
from scripts.prepare_modis_for_step7 import main
print(json.dumps(main("manavgat_2021", export=True, force=True), default=str, indent=1)[:2500]); print("MODIS_EXPORT_DONE")
