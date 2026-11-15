"""select_holdout.py: the held-out test fires (declared 15 November 2026). The rule of make_registry.py applied to
the 2013-2016 scan (holdout_candidates_2013_2016.json): anchor May to October, event share >= 0.9, rectangle at
most 1.1 degree on a side, largest first; a candidate whose rectangle overlaps any rectangle already used (the five
study areas, the 26 scale-up fires, the 3 repeat fires) or a holdout fire already kept is dropped. Only the
selection rule is applied; no model is run here. Writes holdout_fires.json."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXISTING = {"manavgat_2021": (31.05, 36.72, 31.85, 37.35), "bejis_2022": (-1.05, 39.68, -0.35, 40.15),
            "mugla_2021": (27.10, 36.60, 28.90, 37.45), "evia_2021_extended": (23.05, 38.55, 23.85, 39.15),
            "montiferru_2021": (8.45, 40.05, 8.75, 40.27)}


def overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


used = dict(EXISTING)
for f in ("batch_candidates.json", "repeat_candidates.json"):
    for r in json.loads((HERE / f).read_text(encoding="utf-8")):
        used[r["experiment"]] = tuple(r["aoi"])
cands = json.loads((HERE / "holdout_candidates_2013_2016.json").read_text(encoding="utf-8"))
first = [r for r in cands if 5 <= int(r["anchor"][5:7]) <= 10 and r["event_share"] >= 0.9 and max(r["aoi_deg"]) <= 1.1]
keep, dropped = [], []
for r in first:
    hit = [k for k, b in used.items() if overlap(r["aoi"], b)] + [k["anchor"] for k in keep if overlap(r["aoi"], k["aoi"])]
    (dropped if hit else keep).append({**r, "overlaps": hit})
for i, r in enumerate(keep, 1):
    r["experiment"] = f"ho{i:02d}_{r['year']}"
(HERE / "holdout_fires.json").write_text(json.dumps({"kept": keep, "dropped": dropped,
                                                     "scanned": len(cands), "pass_filters": len(first)}, indent=1), encoding="utf-8")
print(len(cands), "scanned,", len(first), "pass the filters,", len(keep), "kept,", len(dropped), "dropped")
for r in keep:
    print(" kept", r["experiment"], r["anchor"], r["event_pixels"], r["aoi"], "baseline", r["baseline_years"])
for r in dropped:
    print(" dropped", r["anchor"], r["aoi"], r["overlaps"])
