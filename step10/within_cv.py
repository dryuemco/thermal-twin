"""
step10/within_cv.py

step8b'nin within-region spatial-block CV mantiginin BAGIMSIZ ama BIREBIR
yeniden yazimi (repo import EDILMEZ). step8e degerlerini yeniden uretmek ve
farkli blok boyutlarinda robustness testi icin kullanilir.

Bire bir eslesen unsurlar:
    - StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    - Ayni baseline vs thermal feature setleri
    - Numerik: SimpleImputer(median); kategorik landcover_dominant:
      SimpleImputer(most_frequent) + OneHotEncoder(handle_unknown='ignore')
    - RandomForest step8b parametreleri (min_samples_leaf=3, class_weight
      'balanced', n_estimators=300, random_state=42)
    - OOF (out-of-fold) tahmin toplama
    - blok = row_500m // k, col_500m // k
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from config10 import (
    BASELINE_FEATURES,
    CATEGORICAL_FEATURES,
    SEED,
    STEP8B_N_SPLITS,
    STEP8B_RF_PARAMS,
    TARGET_COLUMN,
    THERMAL_MODEL_FEATURES,
)
from data_io import assert_no_leakage


def _build_pipeline(feature_list: list[str]) -> Pipeline:
    assert_no_leakage(feature_list)
    num = [f for f in feature_list if f not in CATEGORICAL_FEATURES]
    cat = [f for f in feature_list if f in CATEGORICAL_FEATURES]
    transformers = []
    if num:
        transformers.append(("num", Pipeline([("imp", SimpleImputer(strategy="median"))]), num))
    if cat:
        transformers.append((
            "cat",
            Pipeline([
                ("imp", SimpleImputer(strategy="most_frequent")),
                ("oh", OneHotEncoder(handle_unknown="ignore")),
            ]),
            cat,
        ))
    pre = ColumnTransformer(transformers)
    clf = RandomForestClassifier(**STEP8B_RF_PARAMS)
    return Pipeline([("pre", pre), ("clf", clf)])


def run_oof(
    df: pd.DataFrame, block_ids: np.ndarray, n_splits: int = STEP8B_N_SPLITS, seed: int = SEED
) -> dict:
    """Baseline ve thermal modelleri ayni spatial-block foldlarda egitip OOF
    tahminlerini toplar. Doner: oof diziler + fold sayisi."""
    y = df[TARGET_COLUMN].astype(int).to_numpy()
    n = len(df)

    n_groups = len(np.unique(block_ids))
    if n_groups < n_splits:
        raise RuntimeError(
            f"Spatial-block sayisi ({n_groups}) < n_splits ({n_splits}); "
            "CV kurulamaz (random split'e DUSULMEZ)."
        )

    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    folds = list(splitter.split(np.zeros(n), y, groups=block_ids))

    oof_base = np.full(n, np.nan)
    oof_therm = np.full(n, np.nan)

    for train_idx, test_idx in folds:
        y_tr = y[train_idx]
        pa = _build_pipeline(BASELINE_FEATURES)
        pa.fit(df.iloc[train_idx][BASELINE_FEATURES], y_tr)
        oof_base[test_idx] = pa.predict_proba(df.iloc[test_idx][BASELINE_FEATURES])[:, 1]

        pb = _build_pipeline(THERMAL_MODEL_FEATURES)
        pb.fit(df.iloc[train_idx][THERMAL_MODEL_FEATURES], y_tr)
        oof_therm[test_idx] = pb.predict_proba(df.iloc[test_idx][THERMAL_MODEL_FEATURES])[:, 1]

    return {
        "y": y,
        "oof_baseline": oof_base,
        "oof_thermal": oof_therm,
        "n_splits_used": n_splits,
        "n_blocks": int(n_groups),
    }
