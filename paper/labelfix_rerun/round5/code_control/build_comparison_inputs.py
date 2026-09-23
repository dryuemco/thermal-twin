"""Build comparison_inputs.json (the step9b/step8c reference file the harnesses read) from an overlay root.
Usage: build_comparison_inputs.py <out_dir>   (env R3ROOT = overlay root with drive_new/ and paper/)
transfer: every cross_region/<pair>/step9b/cross_region_transfer_metrics.json, TSG, not skipped ->
  {thermal, baseline} ROC-AUC (anomaly_stage.py logic; baseline added for loro_merge.mjs).
within: experiments/<r>/step8c/step8c_bootstrap_metrics.json -> overall_point_estimates_from_predictions
  .burnable_tree_shrub_grass.{auc_thermal, auc_baseline} (as the canonical re-run did; anomaly_stage's walker
  finds nothing in this layout).
conditional_by_pair: from $R3ROOT/paper/conditional_similarity_transfer.json per_direction {cosine_9,
  agree_count_9} keyed by the sorted pair 'a|b' (the field loro_merge.mjs reads; its original builder is not in
  the tree; both measures are symmetric, and the builder asserts both directions agree)."""
import json, os, sys
from pathlib import Path
ROOT = Path(os.environ["R3ROOT"]); OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
POP = "burnable_tree_shrub_grass"
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
transfer = {}
for d in sorted((ROOT / "drive_new" / "cross_region").glob("*__*")):
    m = d / "step9b" / "cross_region_transfer_metrics.json"
    if not m.exists(): continue
    for row in json.loads(m.read_text(encoding="utf-8")).get("results", []):
        if row.get("population") != POP or row.get("skipped"): continue
        k = f"{row['source_experiment_id']}_to_{row['target_experiment_id']}"
        tm, bm = row.get("thermal_metrics") or {}, row.get("baseline_metrics") or {}
        transfer[k] = {"thermal": float(tm["roc_auc"]), "baseline": float(bm["roc_auc"]), "_source": f"{d.name}/step9b"}
within = {}
for r in REGIONS:
    p = ROOT / "drive_new" / "experiments" / r / "step8c" / "step8c_bootstrap_metrics.json"
    e = json.loads(p.read_text(encoding="utf-8"))["overall_point_estimates_from_predictions"][POP]
    within[r] = {"thermal_auc": float(e["auc_thermal"]), "baseline_auc": float(e["auc_baseline"]),
                 "_source": f"{r}/step8c/step8c_bootstrap_metrics.json overall_point_estimates_from_predictions.{POP}.auc_thermal/auc_baseline"}
doc = {"transfer": transfer, "within": within}
cs = ROOT / "paper" / "conditional_similarity_transfer.json"
if cs.exists():
    cbp = {}
    for d in json.loads(cs.read_text(encoding="utf-8"))["per_direction"]:
        s, t = d["direction"].split("_to_")
        k = "|".join(sorted([s, t])); v = {"cosine_9": d["cosine_9"], "agree_count_9": d["agree_count_9"]}
        if k in cbp: assert abs(cbp[k]["cosine_9"] - v["cosine_9"]) < 1e-12 and cbp[k]["agree_count_9"] == v["agree_count_9"], k
        cbp[k] = v
    doc["conditional_by_pair"] = cbp
(OUT / "comparison_inputs.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")
print(f"transfer {len(transfer)}, within {len(within)}, conditional_by_pair {len(doc.get('conditional_by_pair', {}))} -> {OUT/'comparison_inputs.json'}")
for r in REGIONS: print(f"  within {r:22s} base {within[r]['baseline_auc']:.4f} thermal {within[r]['thermal_auc']:.4f}")
