"""Marginal AoA completion driver (round 3). Usage: aoa_driver.py <tree_root> <corrected|control>
cwd = tree, PROJECT_ROOT = tree. run_analysis(strict_hashes=False) for the corrected tree (as the plan names);
the control tree keeps strict_hashes=True (frozen Manavgat hash).
The only non-module step: the 'climate-export' stage is a LIVE Earth Engine export of a label-free
TerraClimate raster. It is not re-exported: the frozen drive_new raster and its export metadata are copied
byte-identically into the new namespace and the stage marker is written by the module's own
write_stage_marker; run_analysis then takes the module's own 'reuse existing export' path, which re-validates
the raster (validate_exported_raster). A reuse-only engine object is injected so the module's EE opt-in guard
is satisfied; it raises if any EE method is called."""
import sys, os, json, shutil
sys.dont_write_bytecode = True
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); arm = sys.argv[2]
os.chdir(tree); sys.path.insert(0, str(tree))
import src.marginal_aoa_completion as m
FROZEN = Path(r"C:\Users\CORSAIR\projects\thermal-twin\drive_new\diagnostics\marginal_aoa_completion\4b2a1c86c0c197c2a331c133d1120f9531ce385441d86af0d8c6154024417492")
strict = (arm == "control")
class ReuseOnly:
    name = "round3_reuse_only_no_earth_engine"
    def __getattr__(self, k): raise RuntimeError(f"Earth Engine method {k!r} called; reuse path expected")
r1 = m.run_analysis(from_stage="plan", to_stage="plan", strict_hashes=strict, resume=True)
aid = r1.get("analysis_id"); print("plan:", json.dumps({k: r1.get(k) for k in ("analysis_id", "ran", "resumed")}, default=str))
root = m.analysis_root(aid)
cd = root / "climate_distance"; cd.mkdir(parents=True, exist_ok=True)
for f in (m.CLIMATE_RASTER_FILENAME, "climate_export_metadata.json"):
    if not (cd / f).exists(): shutil.copy2(FROZEN / "climate_distance" / f, cd / f)
if m.read_stage_marker(aid, "climate-export") is None:
    m.write_stage_marker(aid, "climate-export", extra={"requires": ["plan"], "round3_note":
        "frozen label-free TerraClimate raster + metadata copied from drive_new 4b2a1c86...; no EE call"})
res = m.run_analysis(from_stage="climate-export", to_stage="compare", strict_hashes=strict, resume=True,
                     climate_export_engine=ReuseOnly())
print(json.dumps(res, indent=1, default=str)[:3000])
print("ANALYSIS_ID", aid, "ROOT", root)
print("AOA_DRIVER_DONE")
