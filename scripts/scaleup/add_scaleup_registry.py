"""add_scaleup_registry.py: registers the scale-up fires in core/regions.py of the official checkout.

Entries: the 26 fires of the pilot list (batch_candidates.json, Rhodes included), the three repeat fires
(repeat_candidates.json, rp..) and montiferru_2021_fullwindow, a copy of montiferru_2021 that differs only
in its id, output namespace and the MODIS month filter. Every new entry sets
modis_predictor_month_filter = False (decision of 14 Nov 2026: the MODIS predictor uses the whole 58-day
window). The experiments of the manuscript are not changed.

The fires, windows and rectangles are those of the pilot (selection rule in scan_fires.py and
make_registry.py of the pilot folder). The script starts from regions.py of main (git show main:core/regions.py),
so it can be run again without piling up edits, and keeps the file's CRLF line endings.

Usage: python add_scaleup_registry.py <repo> <pilot folder>
"""
import json
import subprocess
import sys
from pathlib import Path

repo, pilot = Path(sys.argv[1]), Path(sys.argv[2])
main = json.loads((pilot / "batch_candidates.json").read_text(encoding="utf-8"))
rep = json.loads((pilot / "repeat_candidates.json").read_text(encoding="utf-8"))
assert len(main) == 26 and len(rep) == 3, (len(main), len(rep))

base = subprocess.run(["git", "-C", str(repo), "show", "main:core/regions.py"],
                      capture_output=True, check=True).stdout.decode("utf-8").replace("\r\n", "\n")

geoms, keys, entries = [], [], []
for kind, rows in (("main", main), ("repeat", rep)):
    for r in rows:
        exp = r["experiment"]
        key = "rhodes_aoi" if exp == "rhodes_2023" else f"{exp}_aoi"
        a = r["aoi"]
        geoms.append(f"    {key} = ee.Geometry.BBox({a[0]}, {a[1]}, {a[2]}, {a[3]})   # scale-up fire {exp}\n")
        keys.append(f'        "{key}": {key},\n')
        partner = "" if kind == "main" else (
            f" Repeat fire: same region as {', '.join(r['partners'])} in another year; its rectangle shares "
            "cells with the partner, so it is used only for the same-region check.")
        entries.append(f'''    "{exp}": {{
        "enabled": True,
        "variant_status": "canonical",
        "region_key": "{key}",
        "display_name": "Scale-up {exp} ({r['anchor']}, centre {round((a[0] + a[2]) / 2, 2)} E {round((a[1] + a[3]) / 2, 2)} N)",
        "role": "scaleup_wildfire",
        "country": "not assigned (scale-up)",
        "predictor_start_date": "{r['predictor_start']}",
        "predictor_end_date": "{r['predictor_end']}",
        "label_start_date": "{r['label_start']}",
        "label_end_date": "{r['label_end']}",
        "baseline_years": {r['baseline_years']},
        "output_namespace": "{exp}",
        "exclude_pre_label_burns": True,
        "pre_label_burn_window": ["{r['predictor_start']}", "{r['predictor_end']}"],
        "modis_predictor_month_filter": False,
        "notes": (
            "Scale-up run (31 fires, November 2026). Event and rectangle defined by rule from MCD64A1: "
            "anchor = first burn date of the dominant event, 58-day predictor window, 49-day label "
            "window, rectangle = bounds of the labelled pixels plus 0.15 degree. MODIS predictor over the "
            "whole predictor window (no month filter).{partner}"
        ),
    }},
''')

# montiferru_2021_fullwindow: textual copy of the montiferru_2021 record
i = base.index('    "montiferru_2021": {\n')
j = base.index("\n    },\n", i) + len("\n    },\n")
block = base[i:j]
assert block.count('"montiferru_2021"') == 2, "id and output namespace expected once each"
block = block.replace('    "montiferru_2021": {\n', '    "montiferru_2021_fullwindow": {\n', 1)
block = block.replace('"output_namespace": "montiferru_2021",', '"output_namespace": "montiferru_2021_fullwindow",', 1)
block = block.replace('"display_name": "Montiferru / Oristano, Sardinia 2021",',
                      '"display_name": "Montiferru / Oristano, Sardinia 2021 (MODIS over the whole predictor window)",', 1)
role = '        "role": "mediterranean_transfer_wildfire",\n'
assert block.count(role) == 1
block = block.replace(role, '        "role": "scaleup_wildfire",\n', 1)
anchor = '        "pre_label_burn_window": ["2021-05-25", "2021-07-23"],\n'
assert block.count(anchor) == 1
block = block.replace(anchor, anchor + '        "modis_predictor_month_filter": False,\n'
                      '        # Scale-up run (Nov 2026): identical to montiferru_2021 except that the MODIS predictor\n'
                      '        # uses all 60 days of the window (montiferru_2021 drops 25-31 May by the month filter).\n', 1)
assert '"modis_predictor_month_filter": False' in block and block.count('"montiferru_2021_fullwindow"') == 2
entries.append(block)

s = base
old = "    montiferru_aoi = montiferru_aoi_candidate_bbox\n"
assert s.count(old) == 1
s = s.replace(old, old + "".join(geoms))
old = '        "montiferru_aoi_candidate_bbox": montiferru_aoi_candidate_bbox,\n    }\n'
assert s.count(old) == 1
s = s.replace(old, '        "montiferru_aoi_candidate_bbox": montiferru_aoi_candidate_bbox,\n' + "".join(keys) + "    }\n")
i = s.index("EXPERIMENTS = {")
j = s.index("\n}\n", i)
s = s[:j + 1] + "".join(entries) + s[j + 1:]
ids = [r["experiment"] for r in main] + [r["experiment"] for r in rep] + ["montiferru_2021_fullwindow"]
j = s.index("\n}\n", s.index("EXPERIMENTS = {")) + 3
s = (s[:j] + "\n# Experiments of the scale-up run (November 2026), listed explicitly so that the registry\n"
     "# key-set tests name every addition deliberately.\nSCALEUP_EXPERIMENT_IDS = (\n"
     + "".join(f'    "{e}",\n' for e in ids) + ")\n" + s[j:])
(repo / "core" / "regions.py").write_bytes(s.replace("\n", "\r\n").encode("utf-8"))
ids = [r["experiment"] for r in main] + [r["experiment"] for r in rep] + ["montiferru_2021_fullwindow"]
print(len(ids), "experiments registered:", " ".join(ids))
