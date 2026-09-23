"""Stage A manifest for the official Manavgat re-freeze tree.
Writes <tree>/REFREEZE_MANIFEST.json, <tree>/REFREEZE_MANIFEST.md and <tree>/SHA256SUMS.txt covering every
Manavgat-dependent output the re-freeze produced (label, gate, step8a-e, robustness, 6 pair folders).
Usage: make_manifest.py <official_tree> <control_tree> <g1_json>"""
import sys, json, hashlib, platform, subprocess, datetime
from pathlib import Path

tree, ctrl, g1_path = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
O = tree / "outputs"
PAIRS = ["manavgat_2021__bejis_2022", "manavgat_2021__mugla_2021", "manavgat_2021__evia_2021_extended",
         "mugla_2021__manavgat_2021", "montiferru_2021__manavgat_2021", "manavgat_2021__evia_2021"]
SCOPE = [O / "experiments/manavgat_2021/validation/labels"] + \
        [O / f"experiments/manavgat_2021/{s}" for s in ("step8a", "step8b", "step8c", "step8d", "step8e", "robustness")] + \
        [O / "robustness/step8_large_block", O / "robustness/step8_large_block_primary_all_valid"] + \
        [O / "cross_region" / p for p in PAIRS] +         [O / "diagnostics/step9g_univariate_feature_auc_direction_reversal" / p for p in PAIRS] +         [O / "diagnostics/step9g_univariate_feature_auc_direction_reversal/comparison",
         O / "diagnostics/four_aoi_transfer_decomposition", O / "diagnostics/multi_aoi_transfer_synthesis",
         O / "diagnostics/burned_pattern_audit", O / "diagnostics/reproduction_check"]
COPIED = [O / "cross_region" / p for p in ("bejis_2022__evia_2021", "bejis_2022__evia_2021_extended", "bejis_2022__mugla_2021",
          "montiferru_2021__bejis_2022", "montiferru_2021__evia_2021_extended", "montiferru_2021__mugla_2021", "mugla_2021__bejis_2022",
          "mugla_2021__evia_2021", "mugla_2021__evia_2021_extended", "mugla_2021__mugla_2022_event_relative")] +          [O / "diagnostics/step9g_univariate_feature_auc_direction_reversal" / p for p in ("bejis_2022__evia_2021",
          "bejis_2022__evia_2021_extended", "bejis_2022__mugla_2021", "montiferru_2021__bejis_2022", "montiferru_2021__evia_2021_extended",
          "montiferru_2021__mugla_2021", "mugla_2021__evia_2021", "mugla_2021__evia_2021_extended")] +          [O / "diagnostics/step9g_univariate_feature_auc_direction_reversal_integration_v2/bejis_2022__mugla_2021"] +          [O / "experiments" / r for r in ("bejis_2022", "evia_2021", "evia_2021_extended", "montiferru_2021", "mugla_2021")]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


files = sorted(f for d in SCOPE if d.exists() for f in d.rglob("*") if f.is_file())
sums = [(sha(f), f.relative_to(tree).as_posix()) for f in files]
(tree / "SHA256SUMS.txt").write_text("".join(f"{h}  {p}\n" for h, p in sums), encoding="utf-8", newline="\n")
H = {p: h for h, p in sums}
cfiles = sorted(f for d in COPIED if d.exists() for f in d.rglob("*") if f.is_file())
(tree / "COPIED_INPUTS.txt").write_text("# Copied unchanged from drive_new as inputs (label-unaffected; NOT rebuilt)" + chr(10) + "".join(f"{sha(f)}  {f.relative_to(tree).as_posix()}" + chr(10) for f in cfiles), encoding="utf-8", newline=chr(10))

import sklearn, numpy, pandas  # noqa: E402
step8a = "outputs/experiments/manavgat_2021/step8a/step8a_500m_modeling_dataset.parquet"
ctrl8a = sha(ctrl / step8a)
g1 = json.loads(g1_path.read_text(encoding="utf-8"))
gate = json.loads((O / "experiments/manavgat_2021/validation/labels/burned_landcover_gate.json").read_text(encoding="utf-8"))

m = {
    "schema": "manavgat_refreeze_manifest.v1",
    "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "provenance_statement": (
        "The re-freeze tree was built from the pipeline repository at commit 6381f4c "
        "(6381f4cd752d77a3069fcaa2364d10109b5adaf7), run unchanged. Manavgat's original label raster was exported "
        "on 2026-07-08; the month-boundary alignment fix of the MCD64A1 query is commit 183be42 of 2026-07-11. "
        "The label defect was therefore not a code defect at the time of this re-freeze: it was an export made "
        "before the fix and never renewed."),
    "repo_commit": (tree / "REPO_COMMIT.txt").read_text().strip(),
    "label_fix_commit": {"sha": "183be42488cf12a1ebc9b3e8c8fee98be8f649e2", "date": "2026-07-11",
                         "function": "src/step6_validate_fire_relation.py:_mcd64a1_collection_query_bounds"},
    "original_label_export_date": "2026-07-08",
    "label": {
        "producer": "src.step6_validate_fire_relation.export_raw_mcd64a1_labels(experiment_id='manavgat_2021')",
        "label_window": "2021-07-28 .. 2021-08-31 (DOY 209-243)",
        "gee_project": "thermaltwin",
        "gee_project_note": ("Runner-level override of GEE_PROJECT (repo default 'b7-thermal-digital-twin' belongs to "
                             "the pipeline author; this account has no role on it). Infrastructure only: the label is "
                             "read from MODIS/061/MCD64A1, not modelled."),
        "positive_pixels": 803797, "frozen_positive_pixels": 179667, "added_pixels_doy_209_212": 624130,
        "identical_to_2026_09_19_independent_rebuild": "pixel-identical and profile-identical; file bytes differ (the 09-19 rebuild was written by a different writer, SHA-256 8940e706...)",
        "sha256_raw": H.get("outputs/experiments/manavgat_2021/validation/labels/mcd64a1_raw.tif"),
        "sha256_binary": H.get("outputs/experiments/manavgat_2021/validation/labels/mcd64a1_burned.tif"),
    },
    "gate": {"decision": gate.get("decision"), "burned_count": gate.get("burned_count"),
             "note": ("Run through scripts/run_label_gate_only.py --skip-export without --force, so Step6A reused "
                      "the frozen label-free gate inputs and made no EE call. HEAD writes 48 QA fields that the "
                      "frozen gate JSON (2026-07-08) does not have; all 87 frozen fields are reproduced by the "
                      "control arm.")},
    "step8a_schema": {
        "columns": 80, "extra_column": "historical_burn_excluded", "extra_column_values": "False for all 24,150 cells",
        "sha256_official": H.get(step8a), "sha256_control_frozen_label": ctrl8a,
        "sha256_frozen_canonical": "054a1961fc0582a33d36413263668b63074b21ae8b03d12269b6e228787f3439",
        "note": ("Repo HEAD's step8a writes an 80th column, historical_burn_excluded, all False for Manavgat. With the "
                 "frozen label the control arm reproduces all 79 frozen columns exactly; its hash differs from "
                 "054a1961 only because of that column. Kept as HEAD writes it, not edited."),
    },
    "burned_cells": {"tsg_frozen": 784, "tsg_corrected": 2935, "all_frozen": 796, "all_corrected": 3046,
                     "cells_removed": 0},
    "environment": {"python": platform.python_version(), "platform": platform.platform(),
                    "scikit_learn": sklearn.__version__, "numpy": numpy.__version__, "pandas": pandas.__version__,
                    "venv": ".venv-step10",
                    "note": "Library versions equal those recorded by the frozen reproduction check (WSL2, 3.12.3)."},
    "model": "Pipeline defaults at 6381f4c (RF 300 trees, min_samples_leaf 3, class_weight balanced, seed 42); unchanged.",
    "scope": [d.relative_to(tree).as_posix() for d in SCOPE],
    "untouched": "The other four regions' inputs are copied from drive_new with canonical hashes; none is rebuilt.",
    "commands": "refreeze/_runners/run_tree.sh (and build_trees.sh, step6_label.py, bigblock.py, largeblock.py)",
    "control_arm": {"tree": "refreeze/_control_frozenlabel", "label": "frozen (054a1961 / raster 74b600bd)",
                    "g1": g1,
                    "g1_acceptance": ("ACCEPTED by the user on 2026-09-23: legacy manavgat_2021__evia_2021 exceeds the 1e-5 tolerance (metrics 1.3e-5, bootstrap samples 1.2e-4, calibration bin counts +/-1). RF parallel nondeterminism; the 2026-09-19 control showed the same magnitude on the same pair; the pair is outside the eight modern directions. The step8e and large_block input_audit differences are file paths and a column list shifted by the 80th column, with numbers equal to 2.2e-16. The tolerance itself was not changed.")},
    "file_count": len(sums), "sha256sums": "SHA256SUMS.txt",
    "copied_inputs": {"file": "COPIED_INPUTS.txt", "count": len(cfiles),
                      "note": "The other regions' inputs, the 10 non-Manavgat pair folders and the non-Manavgat Step9G reports, copied from drive_new; label-unaffected, not rebuilt."},
    "stage_b": {"reproduction_check": "outputs/diagnostics/reproduction_check/reproduction_check.json",
                "note": ("scripts/run_reproduction_check.py at repo 6381f4c, unchanged. The re-freeze and this reproduction "
                         "check come from the same side; the pipeline author did not independently verify them. "
                         "Tolerance: the repository's own 1e-6 (Step10C).")},
}
(tree / "REFREEZE_MANIFEST.json").write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
md = [f"# Manavgat re-freeze manifest\n", m["provenance_statement"] + "\n",
      f"- Repo commit: `{m['repo_commit']}`; label fix `183be42` (2026-07-11); original export 2026-07-08.",
      f"- GEE project: `thermaltwin` (runner override; infrastructure only).",
      f"- Environment: Python {m['environment']['python']}, scikit-learn {sklearn.__version__}, numpy {numpy.__version__}, pandas {pandas.__version__} ({platform.system()}).",
      f"- Label: {m['label']['positive_pixels']:,} positive pixels ({m['label']['added_pixels_doy_209_212']:,} added, all DOY 209–212); identical to the 2026-09-19 rebuild.",
      f"- Burned cells, TSG 784 → 2,935; all valid 796 → 3,046; none removed. Gate: {gate.get('decision')} (burned_count {gate.get('burned_count')}).",
      f"- step8a: 80 columns; extra `historical_burn_excluded` (all False). SHA-256 official `{H.get(step8a)}`, control `{ctrl8a}`, frozen canonical `054a1961…`. The control hash differs from frozen only by that column; the official hash also differs by the label.",
      f"- Gate JSON: HEAD adds 48 QA fields; all 87 frozen fields reproduced by the control arm.",
      f"- Files hashed: {len(sums)} (`SHA256SUMS.txt`).",
      f"- Raw label raster SHA-256 `{H.get('outputs/experiments/manavgat_2021/validation/labels/mcd64a1_raw.tif')}`: pixel- and profile-identical to the 2026-09-19 rebuild (`8940e706…`), different bytes.",
      f"- G1, control arm (frozen label) vs drive_new, tolerance 1e-5: step8b/8c/8d, robustness (big_blocks_v2, large_block, all_valid) and the five modern pair folders PASS (max 6.2e-6). Not PASS: step8e (9 text diffs, all `results_ran` file paths; numbers max 2.2e-16); large_block `input_audit` (72 diffs, all the column list shifted by the 80th column); legacy `manavgat_2021__evia_2021` (metrics 1.3e-5, bootstrap samples 1.2e-4, calibration bin counts ±1; same magnitude as the 2026-09-19 control, RF thread nondeterminism). Full record: `REFREEZE_MANIFEST.json` → `control_arm.g1`.",
      "- G1 exceptions ACCEPTED by the user on 2026-09-23 (legacy pair: RF nondeterminism, same magnitude on 2026-09-19, outside the eight modern directions); tolerance not changed."]
(tree / "REFREEZE_MANIFEST.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("MANIFEST_DONE", len(sums))
