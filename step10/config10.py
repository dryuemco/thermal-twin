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

# --- Popülasyonlar (analiz altkümeleri) ---
# BİRİNCİL analiz SADECE doğal vejetasyon hücrelerinde: cropland/çıplak yüzey
# confound'unu dışlamak icin (Emrehan'ın PRIMARY_POPULATIONS kuralı). Filtre:
#   valid_for_modeling==True AND burnable_tree_shrub_grass==True.
# all_valid (tüm valid_for_modeling) SENSITIVITY/secondary olarak korunur.
POPULATIONS = {
    "burnable_tree_shrub_grass": {
        "mask_column": "burnable_tree_shrub_grass",  # ek boolean filtre
        "label": "Doğal vejetasyon (tree+shrub+grass)",
    },
    "all_valid": {
        "mask_column": None,  # ek filtre yok; sadece valid_for_modeling==True
        "label": "Tüm valid_for_modeling hücreleri (cropland/çıplak dahil)",
    },
}
PRIMARY_POPULATION = "burnable_tree_shrub_grass"
SECONDARY_POPULATIONS = ["all_valid"]
POPULATION_RUN_ORDER = [PRIMARY_POPULATION] + SECONDARY_POPULATIONS

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

# --- Is1 (cross-region transfer) RF profilleri ---
# BİRİNCİL (primary): Emrehan/step8b ile BİREBİR ayni RF (min_samples_leaf=3,
# class_weight='balanced'). Transfer'in within-region step8b ile ayni
# siniflandirici olmasi decomposition'i tutarli kilar.
TRANSFER_RF_PARAMS_PRIMARY = dict(
    n_estimators=300,
    max_depth=None,
    min_samples_leaf=3,
    class_weight="balanced",
    random_state=SEED,
    n_jobs=-1,
)
# SENSITIVITY: önceki Step10 ayari (min_samples_leaf=2, class_weight yok).
TRANSFER_RF_PARAMS_SENSITIVITY = dict(
    n_estimators=300,
    min_samples_leaf=2,
    random_state=SEED,
    n_jobs=-1,
)
TRANSFER_RF_PROFILES = {
    "primary": TRANSFER_RF_PARAMS_PRIMARY,
    "sensitivity": TRANSFER_RF_PARAMS_SENSITIVITY,
}
PRIMARY_RF_PROFILE = "primary"
# Geriye donuk uyum (eski isim -> artik birincil profil).
TRANSFER_RF_PARAMS = TRANSFER_RF_PARAMS_PRIMARY

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
# Concept-shift univariate AUC bootstrap'i: Emrehan step9g ile AYNI 10 hucre
# (~5km) bloklar. Naif (kucuk blok) bootstrap mekansal otokorelasyonu yok sayip
# CI'yi yapay daraltir; 10 hucre onun muhafazakar semasidir.
CONCEPT_SHIFT_BLOCK_SIZE_CELLS = 10

# --- Transfer varyantlari ---
# CORAL: önce her bölge kendi mean/std'siyle z-score, SONRA CORAL kaynağın
# kovaryansını hedefe hizalar; CORAL yalnız SOURCE'a uygulanır, TARGET z-score'lu
# haliyle DEĞİŞMEDEN kalır. Emrehan'ın tanımıyla aynı => variant adı bunu yansıtır.
CORAL_VARIANT = "coral_after_regionwise_zscore"
ADAPTATION_VARIANTS = ["raw", "zscore", CORAL_VARIANT]
# CORAL regularizasyonu: Emrehan core/config.py STEP10_CORAL_LAMBDA ile BİREBİR.
# Kovaryans ddof=0, eigenvalue tabani 1e-12 (Emrehan step10_shared._sym_matrix_power).
CORAL_LAMBDA = 1e-5
CORAL_EIGVAL_FLOOR = 1e-12
# λ duyarlılık taraması: birincil sonuç (Bej→Man CORAL ~0.557) λ seçimine
# ne kadar bagimli? {1e-5 (birincil), 1e-3, 1e-1, 1.0}.
CORAL_LAMBDA_GRID = [1e-5, 1e-3, 1e-1, 1.0]

# --- Transfer yonleri ---
TRANSFER_DIRECTIONS = [
    ("manavgat_2021", "bejis_2022"),
    ("bejis_2022", "manavgat_2021"),
]

# --- Reprodüksiyon hedefleri (BİRİNCİL popülasyon = burnable, thermal set) ---
# Emrehan'ın pipeline sonuçları (primary RF: msl=3, balanced).
EMREHAN_TRANSFER_TARGETS = {
    "manavgat_2021__bejis_2022": {"raw": 0.326, "zscore": 0.477, CORAL_VARIANT: 0.511},
    "bejis_2022__manavgat_2021": {"raw": 0.444, "zscore": 0.457, CORAL_VARIANT: 0.555},
}
# Yunus'un bağımsız replikasyonu (sklearn sürüm farkı beklenir).
YUNUS_REPLICATION_TARGETS = {
    "manavgat_2021__bejis_2022": {"raw": 0.352, "zscore": 0.480},
    "bejis_2022__manavgat_2021": {"raw": 0.439, "zscore": 0.452},
}
# Kabul toleranslari (Yunus replikasyonuna karsi): raw ±0.03, zscore ±0.01.
# CORAL icin acik tolerans verilmedi; Emrehan hedefine karsi gevsek ±0.05.
REPRO_TOL_RAW = 0.03
REPRO_TOL_ZSCORE = 0.01
REPRO_TOL_CORAL = 0.05
