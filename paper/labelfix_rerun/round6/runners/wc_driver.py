"""Window-closure (Manavgat) driver, round 3 (refreeze copy, 2026-09-23: Linux-path rebase only applied to Linux paths). Usage: wc_driver.py <tree_root> <arm> <from_stage> <to_stage> [dry]
Programmatic entry src.window_closure_sensitivity.run_analysis (the CLI blocks Manavgat), cwd = tree,
default output/experiments roots (= <tree>/outputs/...).
Earth Engine is NOT contacted. The two EE stages use the module's own dependency-injection points
(prelabel_exporter, predictor_engine) with copy-only engines that materialise the FROZEN drive_new EE
exports byte-for-byte at the planned paths (these rasters are label-free: MCD64A1 pre-label BurnDate
before DOY 209 and the Landsat/MODIS predictor composites). The module then inspects them and writes its
own metadata bound to the new analysis id. Everything label-dependent (local-downstream Step5->8A with the
tree's label rasters, model, compare) runs unmodified."""
import sys, os, json, shutil, hashlib
sys.dont_write_bytecode = True
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); arm, fs, ts = sys.argv[2], sys.argv[3], sys.argv[4]
dry = len(sys.argv) > 5 and sys.argv[5] == "dry"
noresume = len(sys.argv) > 5 and sys.argv[5] == "noresume"
os.chdir(tree); sys.path.insert(0, str(tree))
import src.window_closure_sensitivity as wc
FROZEN = Path(r"C:\Users\CORSAIR\projects\thermal-twin\drive_new\diagnostics\window_closure_sensitivity\manavgat_2021")
NEW = wc.experiment_root("manavgat_2021")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def frozen_counterpart(out_path):
    rel = Path(out_path).resolve().relative_to(NEW.resolve())
    src = FROZEN / rel
    if not src.is_file(): raise FileNotFoundError(f"no frozen EE export for {rel}")
    return src
COPIES = []
def prelabel_exporter(experiment_id, pre_label_start, pre_label_end, raw_out):
    src = frozen_counterpart(raw_out); Path(raw_out).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, raw_out); COPIES.append((str(src), str(raw_out), sha(raw_out)))
    return {"path": str(raw_out), "transport": "round3_copy_of_frozen_ee_export", "source": str(src),
            "pre_label_start": pre_label_start, "pre_label_end": pre_label_end}
def predictor_engine(variant_context, variant, jobs):
    out = {}
    for job in jobs:
        dst = Path(job["output_path"]); src = frozen_counterpart(dst)
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
        COPIES.append((str(src), str(dst), sha(dst)))
        out[job["artifact_id"]] = {"path": str(dst), "transport": "round3_copy_of_frozen_ee_export"}
    return out
# Portability shim (round 3b). The canonical step8a_dataset_stats.json records predictor_paths as absolute
# paths on the exporting machine (/home/emrehan-metin/...), so step8a_predictor_lineage's relative_to(root)
# fails on any other machine. Only while that function runs, the recorded prefix is rebased onto this tree's
# experiments root; every path must carry the prefix. The result is asserted equal to the lineage the frozen
# (Linux) run recorded, so the shim cannot change what is classified as timing-derived.
import json as _json, types as _types
LINUX_PREFIX = "/home/emrehan-metin/satellite-thermal-digital-twin/outputs/experiments/"
FROZEN_LINEAGE = {"static": ["elevation", "slope"], "timing": ["current_lst", "current_tvdi", "downscaled_lst",
                  "fused_lst", "lst_anomaly", "ndvi", "tvdi_difference"]}
_orig_lineage = wc.step8a_predictor_lineage
def _rebasing_loads(text, *a, **k):
    obj = _json.loads(text, *a, **k)
    pp = obj.get("predictor_paths") if isinstance(obj, dict) else None
    if isinstance(pp, dict):
        local = str((tree / "outputs" / "experiments").resolve()).replace("\\", "/") + "/"
        for name, p in pp.items():
            # refreeze trees: Step8A was rebuilt here, so its stats already hold this tree's own paths
            if str(p).startswith(LINUX_PREFIX): pp[name] = local + str(p)[len(LINUX_PREFIX):]
    return obj
def step8a_predictor_lineage(experiment_id, experiments_root=None):
    wc.json = _types.SimpleNamespace(**{n: getattr(_json, n) for n in dir(_json) if not n.startswith("__")})
    wc.json.loads = _rebasing_loads
    try: out = _orig_lineage(experiment_id, experiments_root)
    finally: wc.json = _json
    assert out["static_predictors"] == FROZEN_LINEAGE["static"], out["static_predictors"]
    assert out["timing_derived_predictors"] == FROZEN_LINEAGE["timing"], out["timing_derived_predictors"]
    return out
wc.step8a_predictor_lineage = step8a_predictor_lineage

res = wc.run_analysis("manavgat_2021", from_stage=fs, to_stage=ts, dry_run=dry, resume=not (dry or noresume),
                      prelabel_exporter=prelabel_exporter, predictor_engine=predictor_engine)
print(json.dumps({k: res.get(k) for k in ("ran", "dry_run", "analysis_id", "stages_run", "files_written_count", "reused",
                  "prerequisites_ready", "missing_required_inputs", "actual_plan_prerequisites")}, indent=1, default=str))
if dry:
    for k in ("predictor_export_summary", "local_downstream_summary", "model_stage_summary"):
        print(k, json.dumps(res.get(k), default=str)[:1500])
print("EE copies:", len(COPIES))
if COPIES:
    Path(tree / "outputs" / "diagnostics" / "window_closure_sensitivity" / f"round3_ee_copy_manifest_{fs}_{ts}.json").write_text(
        json.dumps([{"frozen_source": a, "copy": b, "sha256": c} for a, b, c in COPIES], indent=1))
print("WC_DRIVER_DONE")
