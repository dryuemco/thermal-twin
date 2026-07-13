"""
step10/transfer.py

Tek yonlu, tek varyantli cross-region transfer: kaynakta egit, hedefte tahmin.
Model: RandomForest (TRANSFER_RF_PARAMS). Kategorik landcover_dominant one-hot.
Tum onisleme (impute, standardize/CORAL) UNSUPERVISED'dir; hedef etiketi
ASLA kullanilmaz.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder

from adaptation import adapt_numeric
from config10 import TRANSFER_RF_PARAMS


def _impute_by_own_median(x_num: pd.DataFrame) -> tuple[np.ndarray, dict]:
    """Her kolonu KENDI medyaniyla doldurur (unsupervised, etiketsiz)."""
    med = x_num.median(numeric_only=True)
    filled = x_num.fillna(med)
    # Tamamen NaN kolon kalirsa 0'a cek (medyan NaN olur).
    filled = filled.fillna(0.0)
    return filled.to_numpy(dtype="float64"), med.to_dict()


def _make_onehot(
    xs_cat: pd.DataFrame, xt_cat: pd.DataFrame
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Kaynakta fit edilmis one-hot; hedefte gorulmeyen kategori 'ignore'."""
    if xs_cat.shape[1] == 0:
        return np.empty((len(xs_cat), 0)), np.empty((len(xt_cat), 0)), []
    enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    xs_oh = enc.fit_transform(xs_cat.astype("object"))
    xt_oh = enc.transform(xt_cat.astype("object"))
    names = list(enc.get_feature_names_out(list(xs_cat.columns)))
    return xs_oh, xt_oh, names


def run_transfer(
    source_df: pd.DataFrame,
    target_df: pd.DataFrame,
    numeric_features: list[str],
    categorical_features: list[str],
    target_col: str,
    variant: str,
) -> dict:
    """Kaynakta egitip hedefte tahmin uretir.

    Doner: {"y_target": np.ndarray, "y_prob": np.ndarray,
            "n_source": int, "n_target": int}
    """
    xs_num_df = source_df[numeric_features]
    xt_num_df = target_df[numeric_features]
    xs_num, _ = _impute_by_own_median(xs_num_df)
    xt_num, _ = _impute_by_own_median(xt_num_df)

    xs_num_a, xt_num_a = adapt_numeric(xs_num, xt_num, variant)

    xs_cat = source_df[categorical_features] if categorical_features else pd.DataFrame(index=source_df.index)
    xt_cat = target_df[categorical_features] if categorical_features else pd.DataFrame(index=target_df.index)
    xs_oh, xt_oh, _ = _make_onehot(xs_cat, xt_cat)

    xs = np.hstack([xs_num_a, xs_oh])
    xt = np.hstack([xt_num_a, xt_oh])

    ys = source_df[target_col].astype(int).to_numpy()
    yt = target_df[target_col].astype(int).to_numpy()

    clf = RandomForestClassifier(**TRANSFER_RF_PARAMS)
    clf.fit(xs, ys)
    y_prob = clf.predict_proba(xt)[:, 1]

    return {
        "y_target": yt,
        "y_prob": y_prob,
        "n_source": int(len(xs)),
        "n_target": int(len(xt)),
    }
