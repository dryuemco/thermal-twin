"""label_counts_11.py: label counts seen before amendment 11 (no model scored). Per primary fire: years 2013 to the
year before the focal predictor window with at least 100 burned cells outside the focal scar (population cells),
and burned cells outside the scar in 2024, 2025 and 2026 (to the last published month). Writes label_counts_11.json."""
import json
import sys
from datetime import date
from pathlib import Path

import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402
from s2_label_check_export import regions  # noqa: E402


def main():
    F = A.load_fires()
    out = {}
    for fid, f in F.items():
        if fid == "montiferru_2021":
            continue
        with rasterio.open(A.OUT / "yearly" / f"{fid}.tif") as r:
            a = r.read()
        v = a[:, f.df.row_500m.to_numpy(int), f.df.col_500m.to_numpy(int)] >= 0.5
        off = f.y == 0
        fy = date.fromisoformat(regions.EXPERIMENTS[fid]["predictor_start_date"]).year
        out[fid] = {"focal_year": fy,
                    "past_cells_by_year": {str(2013 + i): int(v[i][off].sum()) for i in range(v.shape[0]) if 2013 + i < fy},
                    "later_2024_2026": {str(y): int(v[y - 2013][off].sum()) for y in (2024, 2025, 2026)}}
        out[fid]["past_years_100"] = [y for y, n in out[fid]["past_cells_by_year"].items() if n >= 100]
    (A.OUT / "label_counts_11.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(sum(len(v["past_years_100"]) >= 3 for v in out.values()), "sites with >= 3 past years")


if __name__ == "__main__":
    main()
