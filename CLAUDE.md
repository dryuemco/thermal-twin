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

## Prototip bulgu (tarihsel — DÜZELTİLDİ, aşağıdaki "Step10 Sonuçları"na bak)
- İlk prototip **karışık popülasyonda (all_valid)**: ham ~0.39, z-score ~0.56 (0.5 üstü).
- **DÜZELTME:** birincil analiz doğal-vejetasyon popülasyonuyla (burnable) tekrarlanınca
  z-score transferi 0.5 **üstüne çıkarmıyor** (~0.45–0.48). Eski "self-kalibrasyon işareti
  kurtarıyor" yorumu **geri çekildi** — o kazanım büyük ölçüde arazi-örtüsü kompozisyonu
  artefaktıydı (karışık popülasyona özgü). Concept shift baskın; etiketsiz hizalama kapatamıyor.

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
- **Birincil RF (primary):** `RandomForestClassifier(n_estimators=300, max_depth=None,
  min_samples_leaf=3, class_weight="balanced", random_state=42)` — Emrehan/step8b ile birebir.
- Sensitivity RF (eski): `min_samples_leaf=2`, class_weight yok.
- **Birincil popülasyon:** doğal vejetasyon (`valid_for_modeling AND burnable_tree_shrub_grass`).
  Sensitivity: `all_valid`. İkisi de `config10.py`'de seçilebilir.
- `landcover_dominant` → one-hot. Standardizasyon/CORAL **target etiketi kullanmadan** (unsupervised).

## Step10 Sonuçları (tamamlandı — BİRİNCİL = doğal vejetasyon)
Kod: `step10/` (config10, data_io, metrics, adaptation, transfer, spatial_bootstrap,
within_cv, run_a..run_d). Ortam: proje kökünde ayrı `.venv-step10/` (scikit-learn 1.9,
pandas 3.0, numpy 2.5). seed=42, leakage hard-exclude, `repo/` ve mevcut `step8*/step9*`
çıktılarına dokunulmadı. **Birincil popülasyon = burnable_tree_shrub_grass**, birincil RF =
msl3+balanced. Emrehan'ın reposundaki (`core/step10_shared.py`) CORAL tanımıyla (λ=1e-5,
ddof=0) eşitlendi; raw/z-score/CORAL reprodüksiyonu tuttu (`reproduction_check.json`).

**ANA BULGU (dürüst):** Doğal vejetasyonda naif transfer 0.5 altında; **etiketsiz adaptasyon
(z-score / CORAL) transferi güvenilir biçimde şans üstüne ÇIKARAMIYOR** — en iyi CORAL ~0.51–0.56,
ve **yalnız bir yönde (Bej→Man CORAL) CI'si 0.5 üstünde** — o da **λ≤0.1'e bağlı, λ=1'de şansa düşüyor** (§6).
within-region 0.87–0.92'ye kıyasla kalan açık ezici → **concept shift baskın** (best-CORAL decomp ~%69–73).
Concept mekanizması: spatial-block (~5km) CI ile **yalnız elevation reversalı istatistiksel** (kanıtlanmış),
LST/TVDI reversalları düşündürücü ama n=2'de değil. Etiketsiz hizalama sign-flip'i kapatamaz.

### 1) Cross-region transfer, 3 varyant (thermal, BİRİNCİL burnable + msl3+bal)
Kaynak: `transfer_metrics.json/.csv`, `reproduction_check.json`
| Yön | ham | per-region z-score | CORAL (after regionwise z-score) |
|-----|-----|--------------------|-------|
| Man→Bej | 0.3245 `[0.304,0.348]` | 0.4834 `[0.455,0.509]` | **0.5108** `[0.486,0.534]` |
| Bej→Man | 0.4444 `[0.411,0.477]` | 0.4520 `[0.413,0.489]` | **0.5571** `[0.529,0.586]` |

Hiçbir adapte varyant noktasal olarak sağlamca 0.5 üstünde değil; yalnız **Bej→Man CORAL** CI'si
tümüyle 0.5 üstünde. Man→Bej CORAL 0.5'i kesiyor. Reprodüksiyon: raw ±0.03, z-score ±0.01, CORAL ±0.002.

### 2) Popülasyon kontrastı: z-score "kurtarma"sı arazi-örtüsü artefaktı
RF sabit (msl3+bal), yalnız popülasyon değişiyor (thermal z-score):
| Popülasyon | Man→Bej z | Bej→Man z |
|-----------|-----------|-----------|
| all_valid (karışık) | **0.5423** (>0.5) | **0.5907** (>0.5) |
| burnable (doğal vej., BİRİNCİL) | 0.4834 (<0.5) | 0.4520 (<0.5) |

Aynı model/feature/adaptasyon — sadece popülasyon farkı. z-score karışık popülasyonda 0.5 üstüne
çıkarıyor, doğal vejetasyonda çıkaramıyor → eski "kurtarma" büyük ölçüde **kompozisyon artefaktı**.
Baseline feature seti (doğal vej.) de kurtarmıyor: Man→Bej z 0.407, Bej→Man z 0.442 (ikisi <0.5).

### 3) Concept-shift kanıtı (işaretli univariate AUC + SPATIAL-BLOCK bootstrap CI)
Kaynak: `concept_shift.json`, `concept_shift_univariate_auc.csv`, `concept_shift_reversals.csv`.
CI'ler **10 hücre (~5km) spatial-block** bootstrap ile (Emrehan step9g ile aynı). Önceki 2-hücre
(1km) bootstrap mekansal otokorelasyonu yok sayıp CI'yi ~4× daraltmıştı; DÜZELTİLDİ.
9 feature'ın **5'i** nokta tahminde ters tarafa düşüyor; ama **yalnız elevation bootstrap-supported**
(CI'ler ayrık), 4'ü point-reversal (CI'ler örtüşüyor) — Emrehan'ın muhafazakar sonucuyla aynı:
| Feature | AUC Manavgat (CI) | AUC Bejís (CI) | destek |
|---------|-------------------|----------------|--------|
| **elevation_mean** | 0.374 `[0.290,0.472]` | 0.643 `[0.559,0.727]` | **bootstrap-supported** |
| current_lst_mean | 0.538 `[0.450,0.619]` | 0.477 `[0.405,0.540]` | point-reversal |
| downscaled_lst_mean | 0.552 `[0.460,0.635]` | 0.484 `[0.405,0.553]` | point-reversal |
| fused_lst_mean | 0.540 `[0.452,0.621]` | 0.481 `[0.407,0.544]` | point-reversal |
| tvdi_difference_mean | 0.449 `[0.385,0.507]` | 0.512 `[0.446,0.581]` | point-reversal |

Dürüst kanıt gücü: **elevation kanıtlanmış, LST/TVDI reversalları düşündürücü ama n=2'de istatistiksel değil.**

### 4) Within-region robustness (blok 2/10/20, BİRİNCİL burnable)
Kaynak: `experiments/<bolge>/step10/within_robustness.json` (`by_population`),
`within_robustness_summary.csv`. **Reprodüksiyon (blok=2) tuttu**: sapma ≤0.0001.
| Bölge | Blok | baseline | thermal | ΔAUC | ΔAUC %95 CI | sonuç |
|-------|------|----------|---------|------|-------------|-------|
| Manavgat | 2 (~1km) | 0.803 | 0.870 | +0.067 | `[+0.055,+0.078]` | poz destek |
| Manavgat | 10 (~5km) | 0.747 | 0.798 | +0.050 | `[+0.023,+0.078]` | poz destek |
| Manavgat | 20 (~10km) | 0.682 | 0.731 | +0.049 | `[+0.015,+0.086]` | poz destek |
| Bejís | 2 (~1km) | 0.862 | 0.918 | +0.056 | `[+0.048,+0.065]` | poz destek |
| Bejís | 10 (~5km) | 0.779 | 0.825 | +0.046 | `[+0.019,+0.069]` | poz destek |
| Bejís | 20 (~10km) | 0.738 | 0.795 | +0.057 | `[+0.031,+0.090]` | poz destek |

Termal ΔAUC CI'si **her blok boyutunda sıfırın üstünde** (all_valid sensitivity'de de öyle).
Mutlak AUC blok büyüdükçe düşüyor; ΔAUC net erime göstermiyor.

### 5) Decomposition (İş2) — transfer açığının ayrışması (BİRİNCİL burnable)
Kaynak: `decomposition.json/.csv`. Within, raw, adapte HEPSİ burnable + msl3+bal (geçerli kıyas).
Kurtarılabilir pay **en iyi etiketsiz yöntemle** tanımlanır = CORAL (iki yönde de z-score'u geçiyor);
z-score ikincil satır. "Etiketsiz hizalama açığın ne kadarını kapatabilir?" → en iyisinin kadar.
| Hedef | within | ham | adapte | toplam açık | kurtarılan | kalan (concept) |
|-------|--------|-----|--------|-------------|-----------|-----------------|
| **Bejís (Man→Bej) CORAL (best)** | 0.918 | 0.324 | 0.511 | 0.593 | +0.186 (**%31**) | +0.407 (**%69**) |
| **Manavgat (Bej→Man) CORAL (best)** | 0.870 | 0.444 | 0.557 | 0.425 | +0.113 (**%27**) | +0.313 (**%73**) |
| Bejís (Man→Bej) z (ikincil) | 0.918 | 0.324 | 0.483 | 0.593 | +0.159 (%27) | +0.434 (%73) |
| Manavgat (Bej→Man) z (ikincil) | 0.870 | 0.444 | 0.452 | 0.425 | +0.008 (%2) | +0.418 (%98) |

En iyi etiketsiz (CORAL) ile: kurtarılan **~%27–31 covariate**, kalan **~%69–73 concept shift**
(iki yönde tutarlı). z-score bazlı %2 rakamı kurtarılabilir kısmı olduğundan az gösterir (yanlış payda).

### 6) CORAL λ duyarlılığı — tek şansüstü sonuç ne kadar sağlam?
Kaynak: `coral_lambda_sensitivity.csv/.json`. Tek CI'si 0.5 üstünde olan sonuç = Bej→Man CORAL.
λ ∈ {1e-5,1e-3,1e-1,1.0}: Bej→Man CORAL sırasıyla 0.557/0.564/0.547/**0.485** — λ≤0.1'de CI 0.5 üstünde,
**λ=1'de şansa düşüyor** (CI 0.5'i kesiyor). Man→Bej hiçbir λ'da 0.5 üstüne çıkmıyor. Yorum: sonuç
küçük λ'da (3 mertebe) sağlam ama λ'dan bağımsız değil; ağır regularizasyon siliyor. λ=1e-5 (Emrehan
ile aynı, minimal reg.) savunulabilir seçim; bağımlılık açıkça raporlanıyor.

## Genel kurallar
- **Tüm rastgelelikte `seed=42`.**
- Sonuçlar dürüst raporlanır, sayı süslenmez.
- Metodolojik dürüstlük (leakage yok, spatial CV, bootstrap CI) önceliklidir.
- Kod yazmadan önce onay al.
