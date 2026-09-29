"""R8o. Descriptive comparison of the thermal channels with ERA5-Land weather anomalies (reviewer 1).

For each region: the mean of the Landsat LST anomaly channel (lst_anomaly_mean, a per-pixel z-score
against four baseline years) and of the TVDI difference over the primary population, against the
ERA5-Land standardised anomalies of mean air temperature and mean relative humidity in the same
predictor window (paper/era5_raw/.../era5_land_regional_summary.csv, from the pipeline). With five
regions this is descriptive only; Spearman correlations are reported without intervals.
"""
import json
import sys
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import _canonical  # noqa: E402

ERA = pd.read_csv(next((ROOT / "paper/era5_raw").glob("*/era5_land_regional_summary.csv"))).set_index("experiment_id")
rows = []
for reg in ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]:
    d = _canonical.load(reg)
    d = d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)]  # noqa: E712
    rows.append({"region": reg, "lst_anomaly_mean": float(d.lst_anomaly_mean.mean()),
                 "tvdi_difference_mean": float(d.tvdi_difference_mean.mean()),
                 "era5_temperature_anomaly": float(ERA.loc[reg, "predictor_temperature_c_mean_standardized_anomaly"]),
                 "era5_humidity_anomaly": float(ERA.loc[reg, "predictor_relative_humidity_percent_mean_standardized_anomaly"])})
T = pd.DataFrame(rows)
out = {"table": T.round(3).to_dict(orient="records"),
       "spearman_lst_anomaly_vs_era5_temperature": float(spearmanr(T.lst_anomaly_mean, T.era5_temperature_anomaly).statistic),
       "spearman_lst_anomaly_vs_era5_humidity": float(spearmanr(T.lst_anomaly_mean, T.era5_humidity_anomaly).statistic),
       "spearman_tvdi_difference_vs_era5_humidity": float(spearmanr(T.tvdi_difference_mean, T.era5_humidity_anomaly).statistic)}
json.dump(out, open(HERE / "r8o_summary.json", "w"), indent=1)
print(T.round(3).to_string(index=False))
print({k: round(v, 2) for k, v in out.items() if k != "table"})
