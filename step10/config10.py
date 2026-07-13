"""
step10/config10.py

Step10 icin tek kaynak yapilandirma. repo/core/config.py'yi DEGISTIRMEZ;
step8b/step8c'den bire bir kopyalanan sabitler burada yeniden tanimlanir ki
Step10 kendi kendine yeter (repo salt-okunur).

KURALLAR:
    - seed = 42 her yerde
    - leakage kolonlari hard-exclude (FORBIDDEN_FEATURE_COLUMNS)
    - mevcut experiments/* ve repo/* dosyalarina DOKUNULMAZ
"""

from __future__ import annotations

from pathlib import Path

# --- Kokler ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"
CROSS_REGION_DIR = EXPERIMENTS_DIR / "cross_region"

SEED = 42

# --- Bolgeler ve veri yollari ---
REGIONS = {
    "manavgat_2021": EXPERIMENTS_DIR / "manavgat_2021" / "step8a" / "step8a_500m_modeling_dataset.parquet",
    "bejis_2022": EXPERIMENTS_DIR / "bejis_2022" / "step8a" / "step8a_500m_modeling_dataset.parquet",
}

TARGET_COLUMN = "burned"

# --- Feature setleri (step8b ile bire bir) ---
BASELINE_FEATURES = [
    "ndvi_mean",
    "elevation_mean",
    "slope_mean",
    "landcover_dominant",  # kategorik -> one-hot
]
THERMAL_ONLY_FEATURES = [
    "lst_anomaly_mean",
    "current_lst_mean",
    "current_tvdi_mean",
    "tvdi_difference_mean",
    "downscaled_lst_mean",
    "fused_lst_mean",
]
THERMAL_MODEL_FEATURES = BASELINE_FEATURES + THERMAL_ONLY_FEATURES
CATEGORICAL_FEATURES = ["landcover_dominant"]

# Numerik feature'lar (standardizasyon/CORAL yalniz bunlara uygulanir;
# kategorik one-hot standardize EDILMEZ).
BASELINE_NUMERIC = [f for f in BASELINE_FEATURES if f not in CATEGORICAL_FEATURES]
THERMAL_NUMERIC = [f for f in THERMAL_MODEL_FEATURES if f not in CATEGORICAL_FEATURES]

# Univariate concept-shift analizinde kullanilacak tum numerik feature'lar.
ALL_NUMERIC_FEATURES = THERMAL_NUMERIC  # baseline numerics + thermal

# --- Leakage: ASLA feature olamaz (step8b FORBIDDEN listesi + guvenlik) ---
FORBIDDEN_FEATURE_COLUMNS = [
    "burned",
    "burn_date",
    "burn_month",
    "burn_day_of_year",
    "label_source",
    "burn_date_pixel_agreement_fraction",
    "out_of_window_burndate",
    "cell_id",
    "row_500m",
    "col_500m",
    "valid_for_modeling",
    "invalid_reason",
    "source_mask_majority",
    "observed_fraction",
    "gapfilled_fraction",
    "invalid_source_fraction",
    "lon",
    "lat",
]

# --- Is1 (cross-region transfer) model spec (kullanicinin Step10 RF spec'i) ---
TRANSFER_RF_PARAMS = dict(
    n_estimators=300,
    min_samples_leaf=2,
    random_state=SEED,
    n_jobs=-1,
)

# --- Is4 (within-region robustness) model spec: step8b'nin BIREBIR kopyasi ---
# step8e degerlerini yeniden uretebilmek icin step8b'nin RF'i kullanilir.
STEP8B_RF_PARAMS = dict(
    n_estimators=300,
    max_depth=None,
    min_samples_leaf=3,
    class_weight="balanced",
    random_state=SEED,
    n_jobs=-1,
)
STEP8B_N_SPLITS = 5
STEP8B_SPATIAL_BLOCK_SIZE_CELLS = 2  # 1 km; step8e reproduce kontrolu icin

# --- Bootstrap (step8c ile ayni parametreler) ---
N_BOOTSTRAP = 1000
CI_LOWER = 2.5
CI_UPPER = 97.5
# Target-bolge transfer bootstrap'inda blok boyutu (step8c ile ayni: 2 hucre).
BOOTSTRAP_BLOCK_SIZE_CELLS = 2

# --- Transfer varyantlari ---
ADAPTATION_VARIANTS = ["raw", "zscore", "coral"]

# --- Transfer yonleri ---
TRANSFER_DIRECTIONS = [
    ("manavgat_2021", "bejis_2022"),
    ("bejis_2022", "manavgat_2021"),
]

# --- Sanity gate (Is1) esikleri ---
# Prototip deseni: ham transfer AUC < 0.5 (iki yon), zscore ~0.55-0.57.
GATE_RAW_AUC_MAX = 0.50          # ham her iki yonde bunun ALTINDA olmali
GATE_ZSCORE_AUC_MIN = 0.50       # zscore 0.5 USTUNDE olmali (sert kosul)
GATE_ZSCORE_EXPECT_LOW = 0.55    # beklenen bant (yumusak bilgi)
GATE_ZSCORE_EXPECT_HIGH = 0.57
