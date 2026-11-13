import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Earth Engine project; the GEE_PROJECT environment variable overrides it (the scale-up run uses
# another account's project). Unset, the value is the original one.
GEE_PROJECT = os.getenv("GEE_PROJECT", "b7-thermal-digital-twin")

MODIS_COLLECTION = "MODIS/061/MOD11A1"
LANDSAT_COLLECTION = "LANDSAT/LC08/C02/T1_L2"

START_DATE = "2019-01-01"
END_DATE = "2023-12-31"

EXPORT_FOLDER = "B7_Thermal_Digital_Twin"

# Drive export task polling ayarları
DRIVE_TASK_POLLING_ENABLED = True
DRIVE_TASK_POLL_INTERVAL_SECONDS = 60
DRIVE_TASK_TIMEOUT_SECONDS = 6 * 60 * 60

# Export görevleri tamamlandıktan sonra Drive klasörünü geemap/gdown ile indir.
# Google Drive klasörünün paylaşılabilir URL'si veya klasör ID'si gerekir.
DRIVE_AUTO_DOWNLOAD_AFTER_EXPORT = True
GOOGLE_DRIVE_EXPORT_FOLDER_URL = os.getenv("GOOGLE_DRIVE_EXPORT_FOLDER_URL", "")
GOOGLE_DRIVE_EXPORT_FOLDER_ID = os.getenv("GOOGLE_DRIVE_EXPORT_FOLDER_ID", "")
DRIVE_DOWNLOAD_STAGING_SUBDIR = "drive_exports"
DRIVE_DOWNLOAD_OVERWRITE = True

MODIS_EXPORT = {
    "description": "export_modis_lst_4y_summer_mean",
    "file_name_prefix": "modis_lst_dogu_akdeniz_4y_summer_mean",
    "scale": 1000,
}

LANDSAT_EXPORT = {
    "file_name_prefix": "landsat_lst_dogu_akdeniz",
    "scale": 30,
}

# Landsat NDVI export ayarları. LST ile aynı QA mask / grid / pencere mantığı kullanılır.
LANDSAT_NDVI_EXPORT = {
    "file_name_prefix": "landsat_ndvi_dogu_akdeniz",
    "scale": 30,
}

ENABLE_MODIS_EXPORT = True
ENABLE_LANDSAT_EXPORT = True
ENABLE_MODIS_STEP5_CONTEXT = True
ENABLE_LANDCOVER_EXPORT = True

# DEM (statik yükseklik/eğim yardımcı katmanı). MODIS/Landsat ile aynı lifecycle:
# Step2B prepare + metadata, Step4 export task, Step4b Drive download.
# DEM henüz Step5+ içinde KULLANILMAZ; ileride RF/XGBoost MODIS downscaling için
# statik yardımcı predictor (elevation, slope) olarak hazırlanır.
ENABLE_DEM_EXPORT = True

# Tercih edilen DEM kaynağı: Copernicus DEM GLO-30 (ImageCollection, 30 m).
# Fallback: USGS SRTMGL1 003 (tek Image, 30 m). Step2B tercih edileni dener,
# bulunamazsa fallback'e düşer ve bunu metadata'ya yazar.
DEM_COLLECTION = "COPERNICUS/DEM/GLO30"
DEM_COLLECTION_BAND = "DEM"
DEM_FALLBACK_DATASET = "USGS/SRTMGL1_003"
DEM_FALLBACK_BAND = "elevation"

# DEM export ayarları. Landsat ile aynı 30 m grid ve EXPORT_CRS kullanılır.
# Her ürün (elevation, slope) ayrı GeoTIFF olarak export edilir.
DEM_EXPORT = {
    "elevation": {
        "description": "export_dem_elevation_dogu_akdeniz",
        "file_name_prefix": "dem_elevation_dogu_akdeniz",
        "band": "elevation",
    },
    "slope": {
        "description": "export_dem_slope_dogu_akdeniz",
        "file_name_prefix": "dem_slope_dogu_akdeniz",
        "band": "slope",
    },
    "scale": 30,
}

# NDVI ve TVDI ürünleri (yeni bilimsel yön). Mevcut LST anomaly pipeline'ından bağımsız.
ENABLE_NDVI_EXPORT = True
ENABLE_TVDI_STEP5 = True

LANDSAT_SCALE = 0.00341802
LANDSAT_OFFSET = 149.0

# Landsat 8 Collection 2 Level 2 yüzey yansıması (SR) bantları için scale/offset.
# SR_B4 = Red, SR_B5 = NIR. Reflectance = DN * SR_SCALE + SR_OFFSET.
LANDSAT_SR_SCALE = 0.0000275
LANDSAT_SR_OFFSET = -0.2
LANDSAT_RED_BAND = "SR_B4"
LANDSAT_NIR_BAND = "SR_B5"

# NDVI = (NIR - RED) / (NIR + RED). Payda (NIR + RED) sıfıra yakınken bölme
# fiziksel olmayan dev değerler (ör. -270, +400) üretir. Bu yüzden:
#   - |NIR + RED| < NDVI_DENOMINATOR_EPSILON olan pikseller maskelenir,
#   - hesap sonrası [NDVI_VALID_MIN, NDVI_VALID_MAX] dışındaki pikseller maskelenir
#     (sessizce clamp YAPILMAZ; fiziksel olarak imkânsız değerler maskelenir).
NDVI_DENOMINATOR_EPSILON = 1e-6
NDVI_VALID_MIN = -1.0
NDVI_VALID_MAX = 1.0

REGION_NAME = "kozan_aoi"  # Test için küçük bölge kullan

SUMMER_MONTH_START = 6
SUMMER_MONTH_END = 9

# Landsat baseline export üst sınırı. Bu değer hedef sayı değildir.
# Pencere-simetrik baseline'da gerçek export sayısı current yılından önceki
# baseline yıl sayısına bağlıdır; örn. 2019-2023 aralığı ve current=2023 ise 4.
# Production için None yapılabilir.
MAX_LANDSAT_DAILY_EXPORTS = 12

EXPORT_CRS = "EPSG:4326"

# Anomali baseline yıl aralığı.
# Step3, current period penceresinin aynı ay-gün aralığını bu yıllara taşır.
# Current yılı baseline'dan hariç tutulur.
BASELINE_START_DATE = "2019-06-01"
BASELINE_END_DATE = "2023-09-30"

# Current period - anomali hesabı için kullanılacak güncel pencere
CURRENT_PERIOD_DAYS = 60
CURRENT_PERIOD_END_DATE = "2023-07-31"

# Step5 bellek kullanımı ayarları
# Her seferinde okunacak raster pencere kenarı (piksel).
# Yaklaşık bellek: sahne_sayısı * STEP5_WINDOW_SIZE^2 * 4 byte.
STEP5_WINDOW_SIZE = 512

# Standart sapma bu eşiğin altındaysa z-score anomali NaN yazılır.
# Bu, düşük örnek sayısı veya yapay sabit piksellerde z-score patlamasını engeller.
STEP5_MIN_BASELINE_STD_CELSIUS = 1.0

# MODIS bağlam z-score hesabında standart sapma bu eşiğin altındaysa sonuç NaN bırakılır.
# MODIS (~1 km) yalnız düşük çözünürlüklü bağlam ürünü olarak kullanılır.
STEP5_MIN_MODIS_STD_CELSIUS = 1.0

# Bu eşiğin altında geçerli baseline gözlemi olan piksellerde mean/std/z-score
# hesaplanmaz; piksel NaN bırakılır.
STEP5_MIN_BASELINE_VALID_COUNT = 3

# Current period median en az bu kadar QA-temiz gözlemden oluşmalıdır.
# Aksi halde tek bulut kaçağı veya tek sahne kaynaklı soğuk pikseller anomaliye girmez.
STEP5_MIN_CURRENT_VALID_COUNT = 2

# Windowed akış ana raster çıktıları üretir. Interpolated full NetCDF çıktısı
# büyük veri için tekrar yüksek bellek/disk baskısı yaratabileceği için kapalıdır.
STEP5_WRITE_INTERPOLATED_NETCDF = False


# =============================================================================
# TVDI (Temperature Vegetation Dryness Index) ayarları
# =============================================================================
# TVDI = (LST - wet_edge) / (dry_edge - wet_edge)
# Her NDVI bin'i için wet_edge = düşük LST percentile, dry_edge = yüksek LST percentile.
# TVDI offline (Step5) katmanında hesaplanır; tiling/windowed akışı bozulmaz.

# NDVI ekseni bu kadar bin'e bölünür. LST-NDVI scatter üçgeni bu bin'lerle örneklenir.
TVDI_NDVI_BIN_COUNT = 20

# Geçerli NDVI aralığı. Bu aralık dışındaki pikseller TVDI'ye girmez.
TVDI_NDVI_MIN = 0.0
TVDI_NDVI_MAX = 1.0

# Wet/dry edge percentile'ları (her NDVI bin'i içindeki LST dağılımından).
TVDI_WET_EDGE_PERCENTILE = 2.0
TVDI_DRY_EDGE_PERCENTILE = 98.0

# Bir NDVI bin'inin edge hesabına katkı vermesi için gereken minimum geçerli piksel.
# Az örnekli bin'ler gürültülü edge üretir; bu bin'ler edge fit'ine alınmaz.
TVDI_MIN_PIXELS_PER_BIN = 30

# dry_edge - wet_edge bu eşiğin altındaysa TVDI NaN bırakılır.
MIN_TVDI_EDGE_SPAN_C = 1.0

# Geriye dönük uyumluluk için eski isim; MIN_TVDI_EDGE_SPAN_C ile aynı değer.
TVDI_MIN_EDGE_SPAN_CELSIUS = MIN_TVDI_EDGE_SPAN_C

# Baseline TVDI std bu eşiğin altındaysa tvdi_anomaly_zscore NaN/maskeli bırakılır.
# Çok küçük baseline std, z-score'u yapay olarak şişirir (küçük paydaya bölme).
# Bu yüzden epsilon eklemek yerine düşük-std piksellerini maskeliyoruz.
MIN_TVDI_BASELINE_STD = 0.05

# Geriye dönük uyumluluk için eski isim; MIN_TVDI_BASELINE_STD ile aynı değer.
TVDI_MIN_BASELINE_STD = MIN_TVDI_BASELINE_STD

# Sıfıra bölme koruması için yalnız sayısal güvenlik amacıyla kullanılan çok küçük
# epsilon. Std'yi yapay şişirmek için DEĞİL; maskeleme bundan bağımsız yapılır.
TVDI_ZSCORE_NUMERICAL_EPSILON = 1e-9

# Bu eşiğin altında geçerli baseline TVDI gözlemi olan piksellerde z-score hesaplanmaz.
TVDI_MIN_BASELINE_VALID_COUNT = 3


# =============================================================================
# Burned-area / aktif yangın validation (skeleton — Phase 2'de doldurulacak)
# =============================================================================
# Bu collection'lar henüz ağır validation için kullanılmaz; sadece config/helper
# taslağı olarak tanımlanır. TVDI/dryness katmanı ile yanmış alan çakıştırması
# (ROC/AUC) bir sonraki bilimsel adımdır.
ENABLE_BURNED_AREA_VALIDATION = False

# MODIS yanmış alan (500 m, aylık)
MCD64A1_COLLECTION = "MODIS/061/MCD64A1"
MCD64A1_BURNDATE_BAND = "BurnDate"

# ESA FireCCI51 yanmış alan (250 m, aylık)
FIRECCI51_COLLECTION = "ESA/CCI/FireCCI/5_1"
FIRECCI51_BURNDATE_BAND = "BurnDate"

# FIRMS aktif yangın (MODIS/MCD14ML türevi, günlük)
FIRMS_COLLECTION = "FIRMS"
FIRMS_FIRE_BAND = "T21"

# FIRMS VIIRS aktif yangın (375 m, günlük). MODIS'ten bağımsız ikinci aktif-yangın
# kaynağıdır; cross-check için kullanılır. bright_ti4/bright_ti5 parlaklık bantları.
FIRMS_VIIRS_COLLECTION = "FIRMS"  # MODIS T21 ile aynı arşiv; VIIRS ayrı koleksiyonla denenir
FIRMS_VIIRS_COLLECTIONS = (
    "NASA/LANCE/NOAA20_VIIRS/C2",
    "NASA/LANCE/SNPP_VIIRS/C2",
)
FIRMS_VIIRS_FIRE_BAND = "Bright_ti4"
# VIIRS bright_ti4 (parlaklık sıcaklığı, Kelvin) eşiği.
VALIDATION_FIRMS_VIIRS_BRIGHTNESS_THRESHOLD = 330.0


# =============================================================================
# Step6: burned-area association testing (ilk doğrulama)
# =============================================================================
# Step6, predictor rasterlarını (LST anomaly, current TVDI, TVDI difference,
# TVDI z-score) aynı sezon/AOI yanmış alan etiketlerine karşı test eder.
# Bu bir RF/XGBoost modeli DEĞİL; ilk burned-area ilişki (association) testidir.

# Yanmış alan etiketleri için sezon penceresi. Boş bırakılırsa current period
# baseline ile aynı sezon kullanılır. Yangın sezonu genelde current period'dan
# daha geniştir; bu yüzden ayrı tanımlanabilir.
VALIDATION_SEASON_START = "2023-06-01"
VALIDATION_SEASON_END = "2023-10-31"

# FIRMS aktif yangını BAĞIMSIZ CROSS-CHECK olarak çalıştır (opsiyonel).
# ÖNEMLİ: True olması FIRMS'i birincil yanmış-alan etiketine DAHİL ETMEZ.
# MCD64A1 birincil etiket olarak kalır; FIRMS (MODIS+VIIRS) yalnızca bağımsız
# aktif-yangın çapraz kontrolü olarak ayrı bir bölümde raporlanır.
VALIDATION_INCLUDE_FIRMS = True

# Sınıf dengesizliği: yanmış pikseller genelde çok azdır. Dengeli metrikler için
# yanmayan pikseller bu oranda (burned_count * ratio) rastgele alt-örneklenir.
VALIDATION_BALANCED_UNBURNED_RATIO = 1.0

# Alt-örnekleme tekrarlanabilirliği için sabit seed.
VALIDATION_RANDOM_SEED = 42

# FIRMS aktif yangın parlaklık eşiği (T21, Kelvin). Bu değerin üzerindeki pikseller
# aktif yangın kabul edilir.
VALIDATION_FIRMS_BRIGHTNESS_THRESHOLD = 330.0

# Step6 etiket export çözünürlüğü (predictor grid'ine resample edilmeden önce GEE
# export ölçeği). Predictor 30 m olduğu için etiketler de 30 m'ye resample edilir.
VALIDATION_LABEL_EXPORT_SCALE = 30

# JSON çıktısında tutulacak ROC önizleme noktası üst sınırı. Full ROC array'leri
# (milyonlarca nokta olabilir) JSON'a YAZILMAZ; sadece bu kadar noktaya downsample
# edilmiş bir önizleme tutulur. ROC PNG'si full array'lerle bellekte üretilir.
VALIDATION_MAX_ROC_PREVIEW_POINTS = 500

# --- Validation modu ---
# "same_season": predictor ve label aynı sezon penceresinden (ilk association testi).
# "pre_fire":    predictor window ve label window ayrı (yangın öncesi kuruluk sinyali).
#
# DİKKAT: Geçerli değerler yalnız "same_season" ve "pre_fire". Geçersiz bir değer
# girilirse Step6 sessizce same_season'a düşmez; fail-fast hata verir.
VALIDATION_MODE = "pre_fire"

VALIDATION_VALID_MODES = ("same_season", "pre_fire")

# pre_fire modunda predictor ve label pencereleri ayrı tanımlanır.
# Predictor window: yangından ÖNCEKi kuruluk durumu.
# Label window:     sonraki yanmış alan kayıtları.
# Açık (explicit) isimler — Step6 pre_fire modunda bunları kullanır.
PREDICTOR_START_DATE = "2023-06-01"
PREDICTOR_END_DATE = "2023-07-31"
LABEL_START_DATE = "2023-08-01"
LABEL_END_DATE = "2023-10-31"

# Geriye dönük uyumluluk: eski VALIDATION_PREFIRE_* isimleri açık isimlere işaret eder.
VALIDATION_PREFIRE_PREDICTOR_START = PREDICTOR_START_DATE
VALIDATION_PREFIRE_PREDICTOR_END = PREDICTOR_END_DATE
VALIDATION_PREFIRE_LABEL_START = LABEL_START_DATE
VALIDATION_PREFIRE_LABEL_END = LABEL_END_DATE

# pre_fire modunda predictor ve label pencerelerinin çakışmasına bilerek izin
# vermek istersen True yap. Varsayılan False: çakışma fail-fast hata verir.
VALIDATION_ALLOW_OVERLAPPING_WINDOWS = False

# FireCCI51 veri kapsamı (yaklaşık). Bu aralık dışındaki label window'ları için
# FireCCI51 Earth Engine'e SORULMADAN skip edilir (2023 verisi yoktur).
FIRECCI51_AVAILABLE_START = "2001-01-01"
FIRECCI51_AVAILABLE_END = "2020-12-31"

# Geçersiz mode'u erken yakala (sessizce same_season'a düşmeyi önler).
if VALIDATION_MODE not in VALIDATION_VALID_MODES:
    raise ValueError(
        f"Geçersiz VALIDATION_MODE: '{VALIDATION_MODE}'. "
        f"Geçerli değerler: {VALIDATION_VALID_MODES}."
    )

# =============================================================================
# Pre-fire modunda current period'u predictor window'a hizala
# =============================================================================
# VALIDATION_MODE == "pre_fire" iken, Step3/Step4/Step5/Step5C'nin ürettiği
# "current period" rasterları pre_fire PREDICTOR window'unu temsil etmelidir
# (yangından ÖNCEKi dönem). Aksi halde predictor verisi label/yangın dönemine
# sızar ve pre-fire deneyi bilimsel olarak geçersiz olur.
#
# Burada CURRENT_PERIOD_END_DATE ve CURRENT_PERIOD_DAYS, predictor window'dan
# TÜRETİLİR. Böylece tek kaynak (PREDICTOR_*_DATE) kullanılır ve iki tarih tanımı
# arasında tutarsızlık olamaz. Baseline yılları aynı takvim penceresini önceki
# yıllarda kullanmaya devam eder (Step3 bunu otomatik yapar).
#
# same_season modunda bu blok hiçbir şeyi değiştirmez; yukarıdaki varsayılan
# CURRENT_PERIOD_* değerleri aynen korunur.
if VALIDATION_MODE == "pre_fire":
    from datetime import datetime as _dt

    _pred_start = _dt.strptime(PREDICTOR_START_DATE, "%Y-%m-%d")
    _pred_end = _dt.strptime(PREDICTOR_END_DATE, "%Y-%m-%d")
    _label_start = _dt.strptime(LABEL_START_DATE, "%Y-%m-%d")
    _label_end = _dt.strptime(LABEL_END_DATE, "%Y-%m-%d")

    # Pencere gün sayısı (dahil): örn. 2023-06-01 -> 2023-07-31 = 61 gün.
    CURRENT_PERIOD_DAYS = (_pred_end - _pred_start).days
    CURRENT_PERIOD_END_DATE = PREDICTOR_END_DATE

    # Fail-fast: predictor ve label pencereleri aynı veya çakışıyorsa
    # (VALIDATION_ALLOW_OVERLAPPING_WINDOWS açık değilse) hata ver.
    _identical = (
        PREDICTOR_START_DATE == LABEL_START_DATE
        and PREDICTOR_END_DATE == LABEL_END_DATE
    )
    _overlapping = _pred_end > _label_start
    if (_identical or _overlapping) and not VALIDATION_ALLOW_OVERLAPPING_WINDOWS:
        raise ValueError(
            "pre_fire yapılandırması geçersiz: predictor window ve label window "
            f"aynı veya çakışıyor "
            f"(predictor={PREDICTOR_START_DATE}->{PREDICTOR_END_DATE}, "
            f"label={LABEL_START_DATE}->{LABEL_END_DATE}). "
            "Predictor window yangın/label döneminden ÖNCE bitmelidir. "
            "Bilerek çakışma istiyorsan VALIDATION_ALLOW_OVERLAPPING_WINDOWS=True yap."
        )


# =============================================================================
# Step6 label export cleanup + burned-landcover gate
# =============================================================================
# Step6 artik "onemli/dogru" MCD64A1 etiket dosyalarinin (raw BurnDate DOY +
# binary burned mask) TEK SAHIBIDIR. Bu dosyalar Step6'nin kendi ic
# association-test calismasindan (outputs/step6/labels/) AYRI, sabit/paylasilan
# bir konumda (asagida) tutulur; boylece Step8A ve ileride diger deneyler
# (Manavgat vb.) bu konumu guvenle arayabilir.
#
# ONEMLI: Bu yollar Step0/deney-namespace'li degildir (henuz). Manavgat
# pipeline'i CALISTIRILMADAN once bu alan experiment-aware hale getirilmelidir
# (bkz. docs/experiments.md "Current scope limitation").
STEP6_LABEL_OUTPUT_DIR = "outputs/step6/labels"

# Burned-landcover gate karar esikleri (supervisor talebi). Degistirilirse
# Kozan 2023 icin beklenen "cropland_dominated_control" sonucu da degisebilir.
STEP6_BURNED_LANDCOVER_GATE_MIN_POSITIVES = 30
STEP6_BURNED_LANDCOVER_GATE_NATURAL_THRESHOLD = 0.50
STEP6_BURNED_LANDCOVER_GATE_CROPLAND_THRESHOLD = 0.50

# Gate'in calistigi agregasyon seviyesi. "500m_reconstructed_mcd64a1_cell":
# Step8A ile AYNI block/tile mantigi (bkz. core.utils.tiling.make_tile_grid +
# STEP8A_MCD64A1_NATIVE_CELL_SIZE_M / STEP8A_REFERENCE_PIXEL_SIZE_M orani)
# kullanilarak 30 m referans gridi yaklasik native ~500 m MCD64A1 hucrelerine
# geri toplanir. Bu, gate sayilarinin Step8A'nin ürettigi sayilarla mumkun
# oldugunca karsilastirilabilir olmasini saglar (bkz. docs/label_gate.md).
STEP6_BURNED_LANDCOVER_GATE_LEVEL = "500m_reconstructed_mcd64a1_cell"


# =============================================================================
# Step0F: experiment-aware MODIS mean/std/valid-count input QA
# (scripts/prepare_modis_for_step7.py). Independent from the legacy Kozan
# Step2 MODIS baseline (src/step2_modis_5year_mean.py / data/modis/), which
# is UNCHANGED by these constants.
# =============================================================================
# MOD11A1 QC_Day conservative acceptance rule (documented MODIS product bits,
# https://lpdaac.usgs.gov MOD11A1 QC layer bit description):
#   bits 0-1 (Mandatory QA flag):  0b00 = "LST produced, good quality, not
#       necessary to examine detailed QA"
#   bits 2-3 (Data quality flag):  0b00 = "good data quality"
# A pixel-day is accepted ONLY if BOTH fields are exactly 0 (conservative --
# every other documented value for these two fields means either no
# retrieval, cloud, or a quality caveat). Bits 4-5 (emissivity error) and
# bits 6-7 (LST error) are NOT used here (task scope: mandatory QA + data
# quality bits only; no undocumented bit semantics are invented).
STEP7_MODIS_QC_MANDATORY_QA_MASK = 0b0011      # bits 0-1
STEP7_MODIS_QC_MANDATORY_QA_ACCEPT = 0b0000    # "good quality" only
STEP7_MODIS_QC_DATA_QUALITY_SHIFT = 2
STEP7_MODIS_QC_DATA_QUALITY_MASK = 0b0011      # bits 2-3 (after shifting right by 2)
STEP7_MODIS_QC_DATA_QUALITY_ACCEPT = 0b0000    # "good data quality" only

# Minimum number of QC-accepted daily MODIS scenes required at a pixel within
# the experiment's predictor window before that pixel's mean/std is
# considered statistically supported (below this, the pixel stays nodata in
# BOTH modis_lst_mean_celsius.tif and modis_lst_std_celsius.tif). This is a
# generic, conservative statistical-support floor -- a sample stdDev needs
# n>=2 to be non-degenerate, +1 for margin -- and is NOT tuned against any
# specific experiment's (e.g. evia_2021) downstream model performance.
STEP7_MODIS_MIN_VALID_OBSERVATIONS = 3

# Explicit finite nodata sentinel for the experiment-aware MODIS mean/std
# GeoTIFFs. Zero is NEVER used as nodata (0.0 deg C is a physically valid
# Celsius temperature). Earth Engine's local/tiled GeoTIFF export path cannot
# encode NaN directly, so the EE image is `.unmask(STEP7_MODIS_NODATA_VALUE)`
# before download and the value is then stamped as the GeoTIFF's `nodata` tag
# (no further rewriting) -- a documented finite sentinel, as allowed as an
# alternative to NaN.
STEP7_MODIS_NODATA_VALUE = -9999.0

# Suspicious-zero-fraction guard used by Step7B's pre-alignment MODIS source
# validation (src/step7b_prepare_downscaling_dataset.py
# validate_modis_source_rasters()): if a MODIS mean input has NO nodata tag
# defined AND at least this fraction of its "valid" pixels are exact 0.0,
# Step7B fails fast rather than silently treating a masked/no-observation
# region (e.g. sea) as valid Celsius data.
STEP7B_MODIS_SUSPICIOUS_ZERO_FRACTION = 0.05

# =============================================================================
# Step7B: MODIS downscaling training dataset builder
# =============================================================================
# Step7B, MODIS->Landsat LST downscaling için pencere/tile-bazlı bir EĞİTİM
# VERİSETİ hazırlar. Model EĞİTMEZ, fire-risk modeli ÜRETMEZ; yalnızca temiz,
# hizalanmış tabular örnekler (target=Landsat LST, features=MODIS context, NDVI,
# DEM, slope, land cover, koordinatlar) üretir.
STEP7B_TILE_SIZE = 512
STEP7B_MAX_SAMPLES = 500000
STEP7B_RANDOM_SEED = 42
STEP7B_SAMPLE_FRACTION = None
STEP7B_STRATIFY_BY_MODIS_PIXEL = True
STEP7B_MIN_TARGET_CELSIUS = -20.0
STEP7B_MAX_TARGET_CELSIUS = 80.0
STEP7B_REQUIRE_NDVI = True
STEP7B_REQUIRE_DEM = True
STEP7B_OUTPUT_FORMATS = ["parquet", "csv"]
STEP7B_INCLUDE_OPTIONAL_TVDI_FEATURES = True
STEP7B_INCLUDE_OPTIONAL_ANOMALY_FEATURES = True

# =============================================================================
# Step7C: Pure MODIS-to-Landsat LST downscaling model training
# =============================================================================
# Step7C, Step7B veri setini kullanarak SAF bir MODIS->Landsat LST downscaling
# modeli eğitir. Fire-risk modeli DEĞİLDİR; MCD64A1/FIRMS etiketi KULLANMAZ.
# Target-turevi ozellikler (anomaly_zscore, current_tvdi, tvdi_difference,
# modis_context_zscore) leakage riski nedeniyle egitim ozellik setinden haric
# tutulur (bkz. STEP7C_EXCLUDE_LEAKAGE_FEATURES).
# STEP7C_SPLIT_MODE secenekleri: "spatial_block" (varsayilan, saglam mekansal
# blok grouping; row//BLOCK, col//BLOCK), "modis_pixel_group" (modis_pixel_id;
# Step7B ciktisinda bu ID pratikte ornek-basina benzersiz olabilir, bu durumda
# grouped split ETKISIZ hale gelir), "tile_group" (source_tile_id),
# "random" (yalniz --allow-random-split ile, uyariyla).
STEP7C_RANDOM_SEED = 42
STEP7C_MODEL_TYPE = "random_forest"
STEP7C_TEST_SIZE = 0.15
STEP7C_VAL_SIZE = 0.15
STEP7C_SPLIT_MODE = "spatial_block"
STEP7C_SPATIAL_BLOCK_SIZE_PIXELS = 64
STEP7C_EXCLUDE_LEAKAGE_FEATURES = True
STEP7C_MAX_TRAIN_SAMPLES = None
STEP7C_FAST_N_ESTIMATORS = 50
STEP7C_RF_N_ESTIMATORS = 200
STEP7C_RF_MIN_SAMPLES_LEAF = 2
STEP7C_OUTPUT_DIR = "outputs/step7c"


# =============================================================================
# Step7D: Apply Step7C model to full raster grid (30 m downscaled LST)
# =============================================================================
# Step7D, egitilmis Step7C modelini TAM raster gridine uygulayarak 30 m
# Landsat-benzeri downscaled LST GeoTIFF uretir. Fire-risk modeli DEGILDIR;
# MCD64A1/FIRMS etiketi KULLANMAZ; Step7C leakage guard'ina uyar.
STEP7D_TILE_SIZE = 512
STEP7D_OUTPUT_DIR = "outputs/step7d"
STEP7D_MODEL_PATH = "outputs/step7c/downscaling_model.joblib"
STEP7D_MODEL_METADATA_PATH = "outputs/step7c/downscaling_model_metadata.json"
STEP7D_MIN_PREDICTED_CELSIUS = -20.0
STEP7D_MAX_PREDICTED_CELSIUS = 80.0
STEP7D_WRITE_RESIDUAL_PRODUCTS = True
STEP7D_PLOT_SAMPLE_SIZE = 50000


# =============================================================================
# Step7E: Fuse observed Landsat LST with Step7D downscaled LST (gap-filling)
# =============================================================================
# Step7E, gozlemlenen Landsat current-period LST ile Step7D downscaled LST'yi
# BİRLEŞTİRİR (fusion/gap-filling). MODEL EĞİTMEZ, fire-risk modeli DEĞİLDİR,
# yanmis alan etiketi KULLANMAZ. Gozlemlenen Landsat HER ZAMAN ONCELIKLIDIR;
# downscaled LST YALNIZCA gozlem eksik oldugunda kullanilir (ortalama/blend YOK).
STEP7E_OUTPUT_DIR = "outputs/step7e"
STEP7E_TILE_SIZE = 512
STEP7E_MIN_CELSIUS = -20.0
STEP7E_MAX_CELSIUS = 80.0
STEP7E_OBSERVED_LST_PATH = "outputs/step5/current_period_median_celsius.tif"
STEP7E_DOWNSCALED_LST_PATH = "outputs/step7d/downscaled_lst_celsius.tif"
STEP7E_DOWNSCALED_VALID_MASK_PATH = "outputs/step7d/downscaled_lst_valid_mask.tif"
STEP7E_WRITE_DIAGNOSTICS = True


# =============================================================================
# Step8A: native-MCD64A1-grid (500 m) burned-area modeling dataset preparation
# =============================================================================
# Step8A, 30 m predictor rasterlarini MCD64A1'in NATIVE ~500 m gridine agregat
# eder. ONEMLI (label-resolution honesty): onceki validation (Step6) MCD64A1
# etiketini predictor 30 m gridine (nearest-neighbor) resample ediyordu; bu her
# native 500 m yanmis hucreyi cok sayida 30 m piksele COGALTIYOR ve piksel
# sayilarini/anlamli confidence-p-value hesaplarini YANILTICI hale getiriyordu.
# Step8A MODEL EGITMEZ, RF/XGBoost calistirmaz, nihai fire-risk dogrulamasi
# YAPMAZ; yalnizca her satirin bir native 500 m MCD64A1 hucresi oldugu temiz
# bir modelleme tablosu hazirlar. MCD64A1 birincil yanmis-alan etiketi olarak
# kalir; FIRMS Step8A'da hedef olarak KULLANILMAZ (yok sayilir).
STEP8A_OUTPUT_DIR = "outputs/step8a"
STEP8A_MIN_30M_VALID_FRACTION = 0.3
STEP8A_BURNABLE_FRACTION_THRESHOLD = 0.5
STEP8A_WRITE_CSV = True
STEP8A_WRITE_PARQUET = True
STEP8A_RANDOM_SEED = 42

# MCD64A1'in yaklasik native hucre boyutu (m) ve mevcut 30 m referans predictor
# gridinin nominal piksel boyutu (m). Yerelde gercek native-CRS'li 500 m
# MCD64A1 rasteri SAKLANMADIGI icin (Step6 etiketi GEE'den dogrudan 30 m
# olcekte export eder), Step8A native gridi, bu iki degerin oranindan turetilen
# kare piksel-blok boyutuyla (round(500/30)) referans 30 m grid uzerinde
# yaklasik olarak yeniden olusturur. Bu, native 500 m hucre etiketini (mode ile)
# tek deger olarak geri toplayarak duplikasyon sorununu duzeltir.
STEP8A_MCD64A1_NATIVE_CELL_SIZE_M = 500.0
STEP8A_REFERENCE_PIXEL_SIZE_M = 30.0


# =============================================================================
# Step8B: baseline vs baseline+thermal burned-area modeling (determining test)
# =============================================================================
# Step8B, supervisor'in istedigi BELIRLEYICI deneyi calistirir: Step8A'nin
# 500 m MCD64A1-grid modelleme tablosu uzerinde, spatial-block CV ile, Model A
# (baseline: elevation+slope+landcover+NDVI) ile Model B (baseline+thermal:
# +current TVDI+LST anomaly+TVDI difference+fused/downscaled LST) AUC/PR-AUC
# karsilastirir. MCD64A1 tek etikettir; FIRMS hedef olarak KULLANILMAZ. 30 m
# piksel ORNEK OLARAK KULLANILMAZ (yalnizca Step8A'nin 500 m hucreleri). Random
# split KULLANILMAZ; yalnizca spatial-block (StratifiedGroupKFold) CV.
STEP8B_OUTPUT_DIR = "outputs/step8b"
STEP8B_INPUT_DATASET = "outputs/step8a/step8a_500m_modeling_dataset.parquet"
STEP8B_RANDOM_SEED = 42
STEP8B_N_SPLITS = 5
STEP8B_SPATIAL_BLOCK_SIZE_CELLS = 2
STEP8B_MIN_POSITIVES_PER_POPULATION = 30
STEP8B_MIN_MONTH_POSITIVES = 10
STEP8B_PRIMARY_POPULATION = "all_valid"


# =============================================================================
# Step8C: spatial-block bootstrap uncertainty for Step8B delta metrics
# =============================================================================
# Step8C, Step8B'nin nokta tahminlerine (delta_auc, delta_pr_auc, delta_brier)
# belirsizlik/duyarlilik analizi ekler. YENI MODEL EGITMEZ; Step8B'nin mevcut
# out-of-fold tahminlerini (outputs/step8b/step8b_predictions.parquet)
# kullanir. Bootstrap birimi SATIR DEGIL, spatial_block_id'dir (500 m
# hucrelerin mekansal bloklari) -- boylece mekansal bagimlilik saygi gorur.
# FIRMS KULLANILMAZ, 30 m piksel KULLANILMAZ. Klasik p-value/anlamlilik testi
# İDDİA EDİLMEZ; yalnizca bootstrap guven araligi (CI) destegi raporlanir.
STEP8C_OUTPUT_DIR = "outputs/step8c"
STEP8C_INPUT_PREDICTIONS = "outputs/step8b/step8b_predictions.parquet"
STEP8C_N_BOOTSTRAP = 1000
STEP8C_RANDOM_SEED = 42
STEP8C_CI_LOWER = 2.5
STEP8C_CI_UPPER = 97.5
STEP8C_MIN_POSITIVES = 30
STEP8C_MIN_MONTH_POSITIVES = 10


# =============================================================================
# Step8D: thermal feature ablation study for Step8B burned-area modeling
# =============================================================================
# Step8D, Step8B'nin baseline+thermal iyilesmesine HANGI termal ozellik
# grubunun/ozelligin en cok katki sagladigini belirlemek icin ablation
# calismasidir. Step8A'nin 500 m MCD64A1-grid veri setini, ayni spatial-block
# CV stratejisini (Step8B ile birebir) ve MCD64A1 burned hedefini kullanir.
# FIRMS hedef olarak KULLANILMAZ; 30 m piksel ORNEK OLARAK KULLANILMAZ.
# Random split KULLANILMAZ. Her populasyon icin: baseline + 10 termal
# ozellik grubu/tekil ozellik (toplam 11 model), AYNI CV fold'lariyla
# egitilir; delta_pr_auc (birincil, cunku burned nadir) ve delta_auc'a gore
# siralanir. Varsayilan calisma yalnizca nokta tahmini uretir; spatial-block
# bootstrap CI --bootstrap bayragi ile opsiyonel (yavas olabilecegi icin
# varsayilan KAPALI, yalnizca top-K grup icin calisir).
STEP8D_OUTPUT_DIR = "outputs/step8d"
STEP8D_INPUT_DATASET = "outputs/step8a/step8a_500m_modeling_dataset.parquet"
STEP8D_RANDOM_SEED = 42
STEP8D_N_SPLITS = 5
STEP8D_SPATIAL_BLOCK_SIZE_CELLS = 2
STEP8D_MIN_POSITIVES_PER_POPULATION = 30
STEP8D_MIN_MONTH_POSITIVES = 10
STEP8D_N_ESTIMATORS = 300
STEP8D_BOOTSTRAP_DEFAULT = False
STEP8D_BOOTSTRAP_N = 500
STEP8D_BOOTSTRAP_TOP_K = 3


# =============================================================================
# Step8E: final burned-area modeling report (aggregation only, no new science)
# =============================================================================
# Step8E YENI MODEL EGITMEZ, ONCEKI CIKTILARI DEGISTIRMEZ. Yalnizca Step8A-8D
# ciktilarini (stats JSON'lari) okuyup tek bir tutarli bilimsel ozet raporuna
# birlestirir (markdown + JSON + Excel + CSV).
STEP8E_OUTPUT_DIR = "outputs/step8e"


# =============================================================================
# Step0: deney (experiment) kayit defteri uyumluluk koprusu (compatibility bridge)
# =============================================================================
# core/regions.py icindeki EXPERIMENTS kayit defterini bu modulden de
# erisilebilir kilar. ONEMLI: yukaridaki mevcut REGION_NAME, PREDICTOR_*_DATE,
# LABEL_*_DATE gibi degiskenler BILEREK degistirilmedi/uzerine yazilmadi --
# Step1-Step8 script'leri bugun oldugu gibi bu legacy degiskenleri kullanmaya
# devam eder ve bu Step0 katmanindan ETKILENMEZ.
#
# Asagidaki ACTIVE_EXPERIMENT_ID / ACTIVE_EXPERIMENT / EXPERIMENT_* isimleri
# yeni, saf-ek (additive) degiskenlerdir; sadece yeni namespaced cikti katmani
# ve gelecekteki kademeli Step1-Step8 migration'i icin saglanir.
#
# ACTIVE_EXPERIMENT_ID varsayilani "kozan_2023"tur -- bu, yukaridaki legacy
# REGION_NAME ("kozan_aoi") ve PREDICTOR_*_DATE/LABEL_*_DATE degerleriyle
# birebir ayni deneydir; bu yuzden varsayilan calistirmada hicbir bilimsel
# fark YARATMAZ.
from core.regions import (  # noqa: E402
    get_active_experiment as _get_active_experiment,
    get_experiment_output_root as _get_experiment_output_root,
)

ACTIVE_EXPERIMENT_ID = os.getenv("ACTIVE_EXPERIMENT_ID", "kozan_2023")
ACTIVE_EXPERIMENT = _get_active_experiment(ACTIVE_EXPERIMENT_ID)

# Deneyden turetilen, "EXPERIMENT_" onekli saf-ek degiskenler. Bunlar legacy
# REGION_NAME / PREDICTOR_*_DATE / LABEL_*_DATE degiskenlerinin YERINE GECMEZ;
# Step1-Step8 script'leri hala legacy isimleri kullanir.
EXPERIMENT_REGION_NAME = ACTIVE_EXPERIMENT["region_key"]
EXPERIMENT_PREDICTOR_START_DATE = ACTIVE_EXPERIMENT["predictor_start_date"]
EXPERIMENT_PREDICTOR_END_DATE = ACTIVE_EXPERIMENT["predictor_end_date"]
EXPERIMENT_LABEL_START_DATE = ACTIVE_EXPERIMENT["label_start_date"]
EXPERIMENT_LABEL_END_DATE = ACTIVE_EXPERIMENT["label_end_date"]
EXPERIMENT_BASELINE_YEARS = ACTIVE_EXPERIMENT["baseline_years"]
EXPERIMENT_OUTPUT_ROOT = _get_experiment_output_root(ACTIVE_EXPERIMENT_ID)

# Guvenlik kontrolu (sadece varsayilan deney icin): ACTIVE_EXPERIMENT_ID
# "kozan_2023" iken, EXPERIMENT_* degerlerinin legacy PREDICTOR_*_DATE /
# LABEL_*_DATE / REGION_NAME ile birebir ayni oldugunu dogrular. Bu, Step0
# kayit defterinin gelecekte yanlislikla Kozan varsayilanindan sapmasini
# erken yakalamak icin bir fail-fast kontroludur (bilimsel hesaplamayi
# DEGISTIRMEZ, yalnizca tutarliligi dogrular).
if ACTIVE_EXPERIMENT_ID == "kozan_2023":
    _mismatch = []
    if EXPERIMENT_REGION_NAME != REGION_NAME:
        _mismatch.append(f"region_key={EXPERIMENT_REGION_NAME!r} != REGION_NAME={REGION_NAME!r}")
    if EXPERIMENT_PREDICTOR_START_DATE != PREDICTOR_START_DATE:
        _mismatch.append(
            f"predictor_start_date={EXPERIMENT_PREDICTOR_START_DATE!r} != "
            f"PREDICTOR_START_DATE={PREDICTOR_START_DATE!r}"
        )
    if EXPERIMENT_PREDICTOR_END_DATE != PREDICTOR_END_DATE:
        _mismatch.append(
            f"predictor_end_date={EXPERIMENT_PREDICTOR_END_DATE!r} != "
            f"PREDICTOR_END_DATE={PREDICTOR_END_DATE!r}"
        )
    if EXPERIMENT_LABEL_START_DATE != LABEL_START_DATE:
        _mismatch.append(
            f"label_start_date={EXPERIMENT_LABEL_START_DATE!r} != "
            f"LABEL_START_DATE={LABEL_START_DATE!r}"
        )
    if EXPERIMENT_LABEL_END_DATE != LABEL_END_DATE:
        _mismatch.append(
            f"label_end_date={EXPERIMENT_LABEL_END_DATE!r} != "
            f"LABEL_END_DATE={LABEL_END_DATE!r}"
        )
    if _mismatch:
        raise ValueError(
            "Step0 EXPERIMENTS['kozan_2023'] kaydi, core/config.py icindeki "
            "legacy Kozan sabitleriyle TUTARSIZ: " + "; ".join(_mismatch)
        )

# =============================================================================
# Step10: unsupervised self-calibrated cross-region transfer (preregistered)
# =============================================================================
STEP10_RANDOM_STATE = 42
STEP10_BOOTSTRAP_REPLICATES = 1000
STEP10_BOOTSTRAP_CI_LOWER_PERCENTILE = 2.5
STEP10_BOOTSTRAP_CI_UPPER_PERCENTILE = 97.5
STEP10_CORAL_LAMBDA = 1e-5
STEP10_MIN_VALID_BOOTSTRAP_REPLICATES = 900


#landsat_support_harmozation.py içindeki sabit.
DAILY_EXPORT_NODATA = -9999.0