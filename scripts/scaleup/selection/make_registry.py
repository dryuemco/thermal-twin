"""make_registry.py: registers the candidate fires of candidates.json in the CLONED pipeline (scratch copy only).

Pilot helper. It rebuilds repo/core/regions.py of the clone from the committed version (git show HEAD) plus
the Rhodes pilot entry and one entry per selected candidate, so it can be run again without piling up edits.
The original pipeline checkout is never touched.

Selection rule (the same filters as in the pilot notes): anchor in May to October, the dominant event holds
at least 90 % of the burned pixels of its box and the rectangle is at most 1.1 degree on a side. Candidates
are taken largest first, and one whose rectangle overlaps a study area of the manuscript or a candidate
already kept is dropped, so that no two rectangles share cells.

Repeat fires: a dropped candidate that overlaps a kept fire or a study area of ANOTHER year is registered
as well (ids rp..), because it gives a pair of fires in one region in different years. These are kept out of
the main list (their rectangles share cells with their partner) and are used only for the same-region check.

Usage: python make_registry.py <clone folder> [...]   -> writes core/regions.py in the named clones only,
       and batch_ids.txt, worker*_ids.txt, batch_candidates.json, repeat_candidates.json
"""
import sys
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE / "repo"
cands = json.loads((HERE / "candidates.json").read_text(encoding="utf-8"))
EXISTING = {  # rectangles of the five study areas of the manuscript
    "manavgat_2021": (31.05, 36.72, 31.85, 37.35), "bejis_2022": (-1.05, 39.68, -0.35, 40.15),
    "mugla_2021": (27.10, 36.60, 28.90, 37.45), "evia_2021_extended": (23.05, 38.55, 23.85, 39.15),
    "montiferru_2021": (8.45, 40.05, 8.75, 40.27),
}


def overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


first = [r for r in cands if 5 <= int(r["anchor"][5:7]) <= 10 and r["event_share"] >= 0.9
         and max(r["aoi_deg"]) <= 1.1]
keep, dropped = [], []
for r in first:                                   # largest first; a rectangle that overlaps a kept one is dropped
    hit = [k for k, b in EXISTING.items() if overlap(r["aoi"], b)]
    hit += [k["anchor"] for k in keep if overlap(r["aoi"], k["aoi"])]
    (dropped if hit else keep).append({**r, "overlaps": hit})
print(len(first), "pass the season, share and size filters;", len(dropped), "dropped for overlap:")
for r in dropped:
    print("   ", r["anchor"], r["event_pixels"], "px", r["aoi"], "overlaps", r["overlaps"])

base = subprocess.run(["git", "-C", str(REPO), "show", "HEAD:core/regions.py"], capture_output=True, check=True).stdout.decode("utf-8")
base = base.replace("\r\n", "\n")

STUDY_YEAR = {k: int(k.split("_")[1]) for k in EXISTING}
kept_year = {k["anchor"]: k["year"] for k in keep}
repeat = [r for r in dropped
          if any((STUDY_YEAR.get(h) or kept_year[h]) != r["year"] for h in r["overlaps"])]
print(len(repeat), "repeat fires (same region as a kept fire or study area, other year)")

geoms, keys, entries, ids, rp_ids = [], [], [], [], []
for rank, r in enumerate(keep + repeat, 1):
    is_rhodes = r["anchor"] == "2023-07-19" and r["aoi"][0] == 27.72
    is_repeat = rank > len(keep)
    exp = "rhodes_2023" if is_rhodes else f"px{rank:02d}_{r['year']}"
    if is_repeat:
        exp = f"rp{rank - len(keep):02d}_{r['year']}"
    key = f"{exp}_aoi" if not is_rhodes else "rhodes_aoi"
    a = r["aoi"]
    geoms.append(f"    {key} = ee.Geometry.BBox({a[0]}, {a[1]}, {a[2]}, {a[3]})   # pilot candidate {rank}\n")
    keys.append(f'        "{key}": {key},\n')
    entries.append(f'''    "{exp}": {{
        "enabled": True,
        "variant_status": "canonical",
        "region_key": "{key}",
        "display_name": "Pilot candidate {rank} ({r['anchor']}, centre {round((a[0] + a[2]) / 2, 2)} E {round((a[1] + a[3]) / 2, 2)} N)",
        "role": "mediterranean_transfer_wildfire",
        "country": "not assigned (pilot)",
        "predictor_start_date": "{r['predictor_start']}",
        "predictor_end_date": "{r['predictor_end']}",
        "label_start_date": "{r['label_start']}",
        "label_end_date": "{r['label_end']}",
        "baseline_years": {r['baseline_years']},
        "output_namespace": "{exp}",
        "exclude_pre_label_burns": True,
        "pre_label_burn_window": ["{r['predictor_start']}", "{r['predictor_end']}"],
        "notes": (
            "PILOT ONLY (scale-up timing test). Event and rectangle defined by the rule in scan_fires.py: "
            "anchor = first MCD64A1 burn date of the dominant event, 58-day predictor window, 49-day label "
            "window, rectangle = bounds of the labelled pixels plus 0.15 degree."
        ),
    }},
''')
    (rp_ids if is_repeat else ids).append(exp)

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
assert sys.argv[1:], "name the clone folder(s) to write the registry to"
for clone in sys.argv[1:]:
    (HERE / clone / "core" / "regions.py").write_text(s, encoding="utf-8", newline="\n")
    print("registry written to", clone)
(HERE / "batch_ids.txt").write_text("\n".join(ids) + "\n", encoding="utf-8")
todo = [e for e in ids if e != "rhodes_2023"]
for w in range(3):                                 # three workers, each with its own clone; largest fires spread
    (HERE / f"worker{w + 1}_ids.txt").write_text(" ".join(todo[w::3]) + "\n", encoding="utf-8")
(HERE / "batch_candidates.json").write_text(json.dumps([{"experiment": e, **r} for e, r in zip(ids, keep)], indent=1), encoding="utf-8")
anchor_id = {r["anchor"]: e for e, r in zip(ids, keep)}
(HERE / "repeat_candidates.json").write_text(json.dumps(
    [{"experiment": e, **r, "partners": [h if h in EXISTING else anchor_id[h] for h in r["overlaps"]]}
     for e, r in zip(rp_ids, repeat)], indent=1), encoding="utf-8")
print(len(ids), "experiments registered:", " ".join(ids))
print(len(rp_ids), "repeat experiments:", " ".join(rp_ids))
