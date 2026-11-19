"""claim15_followup.py: plan 10.5. Leave-one-country-out with LSIB countries, G1d shared cells with a
half-cell tolerance, and the descriptive D interval of the distance-feature pair. Writes claim15_followup.json.
THERMAL_TWIN_LABEL_SUFFIX unset or empty selects original names. Set it to _qa1 to read the suffixed
Claim 15 location CSV and append _qa1 before the output extension. All other values are errors.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from label_variant import variant_name  # noqa: E402
import analysis_official as A  # noqa: E402
import claim14_future as C14  # noqa: E402
import claim15_location as C15  # noqa: E402

COUNTRY = json.loads((Path(__file__).resolve().parent / "selection" / "fire_countries.json").read_text())


def main():
    F = A.load_fires()
    R = pd.read_csv(A.OUT / variant_name("claim15_g2_per_fire.csv"))
    R["country"] = R.fire.map(COUNTRY)
    S = {"countries": R.country.value_counts().to_dict()}
    for name in ("coord_rf", "thermal_coord", "thermal_dist", "coord_knn"):
        d = (R.fut_thermal - R[f"{name}_fut"]).to_numpy()
        S[name] = {"leave_one_country_out": {c: float(d[(R.country != c).to_numpy()].mean()) for c in R.country.unique()}}
    D = (R.thermal_dist_loss_auc - R.thermal_dist_loss_cauc).to_numpy()
    S["thermal_dist_D"] = C15.boot(D, C14.clusters(F, R.fire.tolist()))
    pairs = []
    for early, late in (("rp01_2020", "px17_2022"), ("px16_2022", "rp02_2023"), ("evia_2021_extended", "rp03_2023")):
        T = {}
        for k in (early, late):
            T[k] = F[k].df if k in F else pd.read_parquet(A.find_scaleup(k))
        e, l = T[early], T[late]
        tree = cKDTree(np.c_[e.lon, e.lat])
        dist = tree.query(np.c_[l.lon, l.lat])[0]
        pairs.append({"earlier": early, "later": late, "later_cells_total": int(len(l)),
                      "shared_cells_half_cell": int((dist <= 0.0023).sum())})
    S["g1d_shared"] = pairs
    (A.OUT / variant_name("claim15_followup.json")).write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
