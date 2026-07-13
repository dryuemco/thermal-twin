# CLAUDE.md — Uydu-Termal Yangın-Öncesi Kuruluk Çalışması

## Proje amacı
Yangın-öncesi (pre-fire) termal/kuruluk durumunun yanmış alanı ne kadar öngördüğünü, ve
bu öngörünün **bölgeler arası transfer edilip edilmediğini** test etmek. Nihai çerçeve:
kendini kalibre eden bir **"satellite thermal digital twin"**.

- Danışman: Yunus Emre Cogurcu · Öğrenci (kod sahibi): Emrehan Metin
- Bu **yayın hedefli** bir araştırma. Metodolojik dürüstlük her şeyin önünde:
  leakage yok, spatial CV, bootstrap CI, sayı süslenmez.
- Pipeline Step1–Step9 kurulu. **Biz Step10'u ekliyoruz.**

## Değiştirme yasağı (KATI)
- `repo/` (Emrehan'ın kodu: `src/step1..step9`, `core/config.py`) → **sadece oku/referans, DEĞİŞTİRME.**
- `experiments/<bolge>/step8*`, `step9*` mevcut çıktıları → **DEĞİŞTİRME.**
- Sadece **yeni** Step10 dosyaları ve çıktıları oluştur.

## Klasör yapısı
```
repo/                         # Emrehan'ın kodu — SALT OKUNUR
  src/step1_*.py .. step9e_*.py
  core/config.py              # tüm sabitler, seed'ler, blok boyutları
experiments/
  manavgat_2021/  (anchor_wildfire)
    step8a/step8a_500m_modeling_dataset.parquet   # ASIL VERİ
    step8b/ step8c/ step8d/ step8e/final_step8_report.json
  bejis_2022/     (aynı yapı)
  kozan_2023/     (şimdilik sadece step0)
  cross_region/   # <-- Step10 cross-region çıktıları BURAYA (henüz yok)
outputs/          # Drive'dan inen zip'ler (step1..step8e arşivleri)
data/
```
**Step10 çıktıları:** bölge-içi → `experiments/<bolge>/step10/`,
cross-region → `experiments/cross_region/`.

## Veri (iki parquet, 500m MCD64A1 native grid hücreleri)
| Bölge | Yol | Satır | Yanmış | Taban oran |
|-------|-----|-------|--------|-----------|
| Manavgat 2021 | `experiments/manavgat_2021/step8a/step8a_500m_modeling_dataset.parquet` | 24150 | 796 | %3.3 |
| Bejís 2022 | `experiments/bejis_2022/step8a/step8a_500m_modeling_dataset.parquet` | 15759 | 1103 | %7.0 |

Parquet 77 kolonlu. Kullanılacaklar:

- **Etiket:** `burned` (0/1)
- **Baseline feature'lar:** `ndvi_mean`, `elevation_mean`, `slope_mean`,
  `landcover_dominant` (kategorik → one-hot)
- **Thermal feature'lar (baseline + bunlar):** `lst_anomaly_mean`, `current_lst_mean`,
  `current_tvdi_mean`, `tvdi_difference_mean`, `downscaled_lst_mean`, `fused_lst_mean`
- **Filtre:** yalnızca `valid_for_modeling == True` satırları
- **Spatial CV için:** `row_500m`, `col_500m` (bloklar bunlardan türetilir)

### Leakage kuralları (İHLAL ETME)
- `lon`/`lat` ve `burn_*` kolonları (`burn_date`, `burn_month`, `burn_day_of_year`,
  `label_source`, `burn_date_pixel_agreement_fraction`, `out_of_window_burndate`) **ASLA feature olmaz.**
- **NOT:** parquet'te `spatial_block_id` kolonu **yoktur** — bloklar `row_500m`/`col_500m`'den
  (blok_boyutu hücre cinsinden) türetilir. step8b `core/config.py`'de
  `STEP8B_SPATIAL_BLOCK_SIZE_CELLS = 2` (≈1km blok) kullanır.

## Mevcut durum (önceki sonuçlar)
- **Within-region** (Emrehan, spatial-block CV, step8e): termal katkı iki bölgede de
  bootstrap-destekli pozitif, delta CI'leri sıfırı kesmiyor.
  - Manavgat: ROC-AUC baseline **0.828** → thermal **0.887** (ΔAUC +0.059, ΔPR-AUC +0.100)
  - Bejís: baseline **0.86** → thermal **0.92**
  - Doğal vejetasyonda (tree+shrub+grass) da korunuyor.
- **Cross-region transfer (naif):** AUC **0.5 ALTINDA (~0.33–0.44)** → anti-öngörücü. Domain shift.

## Prototip bulgu (Step10'un doğrulayacağı hedef)
- Ham transfer AUC ~**0.39**.
- Transferden önce feature'ları **her bölgede kendi mean/std'siyle z-score standardize**
  edince (unsupervised, target etiketi kullanılmadan) transfer AUC ~**0.56** (0.5 üstü).
- **CORAL** standardizasyondan daha iyi çıkmadı.
- 0.56, within-region 0.87'nin çok altında.
- **Yorum:** başarısızlığın bir kısmı kurtarılabilir **COVARIATE shift** (self-kalibrasyon çözer),
  asıl kısmı kurtarılamaz **CONCEPT shift** (elevation ve LST feature'ları bölgeler arası
  yön değiştiriyor).

## Step10'un yapacağı (henüz KOD YAZILMADI — sadece plan)
1. **Cross-region transfer** — iki yön (Man→Bej, Bej→Man) × üç varyant:
   (a) ham, (b) per-region z-score standardizasyon, (c) CORAL.
   Her biri için target **ROC-AUC + PR-AUC + spatial-block bootstrap %95 CI**.
2. **Decomposition raporu:** within-region (step8e'den) vs ham transfer vs adapte transfer.
   - kurtarılan = adapte − ham
   - kalan (concept) = within − adapte
3. **Concept-shift kanıtı:** her bölge için her feature'ın `burned`'a karşı univariate AUC'si;
   iki bölge arası 0.5'in **ters taraflarına** düşen (yön reversal) feature tablosu.
4. **Within-region robustness:** step8b mantığını **5–10km bloklarla**
   (`STEP8B_SPATIAL_BLOCK_SIZE_CELLS ≈ 10–20`) tekrar koş; termal delta CI'si hâlâ pozitif mi?

## Model (Step10 standardı)
- `RandomForestClassifier(n_estimators=300, min_samples_leaf=2, random_state=42)`
- `landcover_dominant` → one-hot
- Standardizasyon/CORAL **target etiketi kullanmadan** (unsupervised) yapılır.

## Step10 Sonuçları (tamamlandı)
Kod: `step10/` (config10, data_io, metrics, adaptation, transfer, spatial_bootstrap,
within_cv, run_a..run_d). Ortam: proje kökünde ayrı `.venv-step10/` (scikit-learn 1.9,
pandas 3.0, numpy 2.5 — `repo/` sklearn içermiyordu). seed=42, leakage hard-exclude,
`repo/` ve mevcut `step8*/step9*` çıktılarına dokunulmadı.

### 1) Cross-region transfer, 3 varyant (thermal feature seti, primary)
Kaynak: `experiments/cross_region/step10/transfer_metrics.json` (+ `.csv`, `sanity_gate.json`)
| Yön | ham | per-region z-score | CORAL |
|-----|-----|--------------------|-------|
| Man→Bej | 0.386 `[0.363,0.412]` | **0.557** `[0.531,0.586]` | 0.553 `[0.528,0.578]` |
| Bej→Man | 0.407 `[0.375,0.442]` | **0.568** `[0.531,0.605]` | 0.558 `[0.533,0.584]` |

ROC-AUC, `[...]` = spatial-block bootstrap %95 CI (n=1000). **Sanity gate GEÇTİ**:
ham < 0.5 (iki yön), z-score 0.55–0.57 bandında, CORAL z-score'u geçmedi. Prototip deseni tuttu.

### 2) Bonus bulgu: z-score kazanımı yalnız thermal feature'larda
Kaynak: `experiments/cross_region/step10/transfer_metrics.csv`
- Thermal set: z-score ham'ı **yukarı** çekiyor (0.386→0.557, 0.407→0.568).
- Baseline set: z-score **yardım etmiyor / düşürüyor** — Man→Bej 0.386→**0.464**, Bej→Man 0.487→0.528.
- Yorum: self-kalibrasyonun transfer kaldıracı termal sinyale özgü; baseline (ndvi/elev/slope)
  covariate hizalamasıyla kurtarılamıyor.

### 3) Concept-shift kanıtı (işaretli univariate AUC, yön reversal)
Kaynak: `experiments/cross_region/step10/concept_shift.json`, `concept_shift_univariate_auc.csv`,
`concept_shift_reversals.csv`. 9 numerik feature'ın **5'i** 0.5'in ters taraflarına düşüyor:
| Feature | AUC Manavgat | AUC Bejís | yön |
|---------|-------------|-----------|-----|
| **elevation_mean** | 0.453 | 0.641 | neg→poz (en büyük sapma, gap 0.19) |
| current_lst_mean | 0.548 | 0.462 | poz→neg |
| downscaled_lst_mean | 0.560 | 0.468 | poz→neg |
| fused_lst_mean | 0.550 | 0.466 | poz→neg |
| tvdi_difference_mean | 0.464 | 0.512 | neg→poz |

Elevation ve LST feature'ları bölgeler arası yön değiştiriyor → kurtarılamayan concept shift'in mekanizması.

### 4) Within-region robustness (blok 2/10/20)
Kaynak: `experiments/<bolge>/step10/within_robustness.json`,
`experiments/cross_region/step10/within_robustness_summary.csv`.
step8b-replika CV (StratifiedGroupKFold n=5, RF min_samples_leaf=3, class_weight=balanced).
**Reprodüksiyon (blok=2) tuttu**: sapma 0.0001 (±0.02 içinde; sklearn 1.9 vs 1.4.2'ye rağmen).
| Bölge | Blok | baseline | thermal | ΔAUC | ΔAUC %95 CI | sonuç |
|-------|------|----------|---------|------|-------------|-------|
| Manavgat | 2 (~1km) | 0.828 | 0.887 | +0.059 | `[+0.050,+0.068]` | poz destek |
| Manavgat | 10 (~5km) | 0.771 | 0.824 | +0.053 | `[+0.032,+0.076]` | poz destek |
| Manavgat | 20 (~10km) | 0.719 | 0.763 | +0.044 | `[+0.014,+0.077]` | poz destek |
| Bejís | 2 (~1km) | 0.869 | 0.917 | +0.048 | `[+0.040,+0.057]` | poz destek |
| Bejís | 10 (~5km) | 0.790 | 0.846 | +0.056 | `[+0.033,+0.079]` | poz destek |
| Bejís | 20 (~10km) | 0.716 | 0.777 | +0.061 | `[+0.039,+0.087]` | poz destek |

Termal ΔAUC CI'si **her blok boyutunda sıfırın üstünde**, hiçbir yerde sıfırı kesmedi.
Mutlak AUC'ler blok büyüdükçe düşüyor (spatial autocorrelation iyimserliği kalkıyor); ΔAUC trendi
zayıf ve bölgeye göre farklı (Man hafif ↓, Bej hafif ↑), net erime yok. En dar CI: Man ~10km, alt sınır +0.014.

### 5) Decomposition (İş2) — transfer açığının ayrışması
Kaynak: `experiments/cross_region/step10/decomposition.json` (+ `.csv`). within = hedef bölgenin
kendi thermal AUC'si; adapte = z-score.
| Hedef | within | ham | adapte(z) | toplam açık | kurtarılan (covariate) | kalan (concept) |
|-------|--------|-----|-----------|-------------|------------------------|-----------------|
| Bejís (Man→Bej) | 0.917 | 0.386 | 0.557 | 0.531 | +0.172 (**%32**) | +0.360 (**%68**) |
| Manavgat (Bej→Man) | 0.887 | 0.407 | 0.568 | 0.480 | +0.161 (**%34**) | +0.318 (**%66**) |

Transfer açığının ~1/3'ü kurtarılabilir covariate shift, ~2/3'ü kurtarılamaz concept shift (iki yönde tutarlı).

## Genel kurallar
- **Tüm rastgelelikte `seed=42`.**
- Sonuçlar dürüst raporlanır, sayı süslenmez.
- Metodolojik dürüstlük (leakage yok, spatial CV, bootstrap CI) önceliklidir.
- Kod yazmadan önce onay al.
