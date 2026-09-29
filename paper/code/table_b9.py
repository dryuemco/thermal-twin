"""Table B9 (thermal transfer, raw / region-wise z-score / CORAL, 2-cell CIs) from the step10 outputs.

Usage: python table_b9.py <outputs_root> [--check-md A2_diagnostics.md]
  <outputs_root> is a pipeline outputs tree (drive_new for the frozen label, or
  refreeze/manavgat_2021/outputs for the corrected one). Points come from
  cross_region/<pair>/step10/step10_metrics.json, intervals from
  step10_bootstrap_summary.csv (1000 replicates, 2-cell blocks). Prints the markdown rows.
  With --check-md, asserts every printed cell of Table B9 equals this output (zero tolerance
  at 3 dp) and exits non-zero on the first mismatch.
Read-only with respect to repo/.
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(sys.argv[1])
NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
        "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}
ORDER = [("manavgat_2021", "bejis_2022"), ("bejis_2022", "manavgat_2021"),
         ("manavgat_2021", "mugla_2021"), ("mugla_2021", "manavgat_2021"),
         ("manavgat_2021", "evia_2021_extended"), ("evia_2021_extended", "manavgat_2021"),
         ("bejis_2022", "mugla_2021"), ("mugla_2021", "bejis_2022"),
         ("bejis_2022", "evia_2021_extended"), ("evia_2021_extended", "bejis_2022"),
         ("mugla_2021", "evia_2021_extended"), ("evia_2021_extended", "mugla_2021"),
         ("montiferru_2021", "manavgat_2021"), ("manavgat_2021", "montiferru_2021"),
         ("montiferru_2021", "bejis_2022"), ("bejis_2022", "montiferru_2021"),
         ("montiferru_2021", "mugla_2021"), ("mugla_2021", "montiferru_2021"),
         ("montiferru_2021", "evia_2021_extended"), ("evia_2021_extended", "montiferru_2021")]
PAIRS = ["manavgat_2021__bejis_2022", "manavgat_2021__mugla_2021", "manavgat_2021__evia_2021_extended",
         "montiferru_2021__manavgat_2021", "montiferru_2021__bejis_2022", "montiferru_2021__mugla_2021",
         "montiferru_2021__evia_2021_extended", "bejis_2022__mugla_2021", "bejis_2022__evia_2021_extended",
         "mugla_2021__evia_2021_extended"]
V = [("raw_source_only", "raw"), ("regionwise_zscore", "z"), ("coral_after_regionwise_zscore", "coral")]
pt, ci = {}, {}
for p in PAIRS:
    m = json.loads((ROOT / "cross_region" / p / "step10" / "step10_metrics.json").read_text())
    b = pd.read_csv(ROOT / "cross_region" / p / "step10" / "step10_bootstrap_summary.csv")
    for d, var in m["point_metrics"].items():
        for key, short in V:
            pt[(d, short)] = var[key]["thermal"]["roc_auc"]
            r = b[(b.direction == d) & (b.series == f"roc_auc__{key}_thermal")].iloc[0]
            ci[(d, short)] = (r.ci_2_5, r.ci_97_5)
rows = []
for s, t in ORDER:
    d = f"{s}_to_{t}"
    cells = [f"{pt[(d, k)]:.3f} [{ci[(d, k)][0]:.3f}, {ci[(d, k)][1]:.3f}]" for _, k in V]
    rows.append(f"| {NAME[s]}→{NAME[t]} | " + " | ".join(cells) + " |")
print("\n".join(rows))
if "--check-md" in sys.argv:
    md = Path(sys.argv[sys.argv.index("--check-md") + 1]).read_text(encoding="utf-8")
    missing = [r for r in rows if r not in md]
    for r in missing:
        print("NOT IN TABLE:", r)
    sys.exit(1 if missing else 0)
