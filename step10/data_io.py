"""
step10/data_io.py

Veri yukleme, leakage-guvenli feature secimi ve spatial-block id turetme.
Mevcut parquet dosyalarini SADECE okur, DEGISTIRMEZ.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from config10 import (
    CATEGORICAL_FEATURES,
    FORBIDDEN_FEATURE_COLUMNS,
    REGIONS,
    TARGET_COLUMN,
)


class Step10DataError(RuntimeError):
    pass


def load_region(region_key: str) -> pd.DataFrame:
    """Bir bolgenin step8a parquet'ini yukler, valid_for_modeling==True
    satirlarini filtreler ve index'i sifirlar."""
    if region_key not in REGIONS:
        raise Step10DataError(f"Bilinmeyen bolge: {region_key}. Secenekler: {list(REGIONS)}")
    path = Path(REGIONS[region_key])
    if not path.exists():
        raise Step10DataError(f"Veri bulunamadi: {path}")
    df = pd.read_parquet(path)
    if "valid_for_modeling" not in df.columns:
        raise Step10DataError(f"{region_key}: valid_for_modeling kolonu yok.")
    if TARGET_COLUMN not in df.columns:
        raise Step10DataError(f"{region_key}: hedef kolon '{TARGET_COLUMN}' yok.")
    df = df[df["valid_for_modeling"] == True].reset_index(drop=True)  # noqa: E712
    if len(df) == 0:
        raise Step10DataError(f"{region_key}: valid_for_modeling==True satir yok.")
    return df


def assert_no_leakage(feature_list: list[str]) -> None:
    """Feature listesinde yasak (leakage) kolon varsa fail-fast."""
    leaked = sorted(set(feature_list) & set(FORBIDDEN_FEATURE_COLUMNS))
    if leaked:
        raise Step10DataError(
            f"LEAKAGE: yasak kolon(lar) feature setine sizmis: {leaked}. "
            "Bu Step10'un temel guvenlik kontrolu ve asla gecilemez."
        )


def add_spatial_block_id(df: pd.DataFrame, block_size_cells: int) -> pd.Series:
    """step8b/step8c ile bire bir ayni blok id: row_500m//k, col_500m//k."""
    k = max(int(block_size_cells), 1)
    if "row_500m" not in df.columns or "col_500m" not in df.columns:
        raise Step10DataError("row_500m/col_500m yok; spatial block turetilemez.")
    r = (df["row_500m"].astype(int) // k).astype(int)
    c = (df["col_500m"].astype(int) // k).astype(int)
    return (r.astype(str) + "_" + c.astype(str)).rename("spatial_block_id")


def get_xy(
    df: pd.DataFrame, numeric_features: list[str], categorical_features: list[str] | None = None
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    """Numerik ve kategorik feature cerceveleri + hedef vektorunu dondurur.
    Leakage kontrolu yapilir."""
    categorical_features = categorical_features or []
    assert_no_leakage(numeric_features + categorical_features)
    x_num = df[numeric_features].astype("float64").copy()
    x_cat = df[categorical_features].copy() if categorical_features else pd.DataFrame(index=df.index)
    y = df[TARGET_COLUMN].astype(int).to_numpy()
    return x_num, x_cat, y
