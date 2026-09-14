# Envanterin "çözülmemiş" maddeleri — lokal kapanışlar (2026-09-14)

Emrehan'ın methods envanterinde (11 Eylül) işaretli kalan maddelerin koddan/arşivden kapatılması.
Araştırma: alt ajan taraması + ana oturumda nokta doğrulama. Emrehan'a giden 14 Eylül mailinin
6 sorusundan 4'ü burada cevaplandı; onun cevabı çapraz teyit olarak kullanılacak.

## S1. DEM agregasyonu (envanter 2.2.5/2.4.4g "Missing/VERIFY FROM CODE") — KAPANDI
- 30 m → ~510 m: **aritmetik mean**, elevation/slope'a istisna yok — diğer continuous
  predictor'larla aynı `continuous_stats()` yolu.
  Kanıt: `repo/src/step8a_prepare_500m_modeling_dataset.py:160-197` (kayıt defteri),
  `:955-964` (mean), `:1271-1297` (uygulama döngüsü). Model `elevation_mean`/`slope_mean` tüketir.
- DEM'in 30 m grid'e inişi: **EE'de değil, lokalde rasterio ile bilinear**.
  Kanıt: `repo/scripts/prepare_dem_for_experiment.py:70` (scale=30), `:126-187`
  (`_reproject_to_reference`, `:168` `Resampling.bilinear`); doküman `repo/docs/experiments.md:288`.
- Kalan tek alt madde: **düşey datum** — kod cevaplamıyor; Copernicus GLO-30 ürün dokümanından
  (EGM2008 beklenir) kaynakla kapatılacak ya da Emrehan teyit edecek.

## S2. EE interpolasyon çekirdeği (envanter 2.2.6c [UNRESOLVED]) — KAPANDI (negatif bulgu)
- Repo'nun hiçbir EE çağrısında explicit `resample()`/`reproject()` yok (95 commit'lik geçmişte de
  hiç olmamış; `git log -S` boş). Tüm export'lar yalnız `scale` + `crs` bildirir
  (`repo/src/step4_export_geotiff.py:155-165`).
- Dolayısıyla Landsat/MODIS/WorldCover/DEM/MCD64A1 export'larının hepsinde **EE'nin belgelenmiş
  varsayılanı olan nearest-neighbour** geçerli. Pipeline-içi hizalamalar lokalde ve explicit:
  continuous=bilinear (`step5_preprocess_timeseries.py:799`), kategorik=nearest
  (`step6a_prepare_gate_inputs.py:301-302`, `step8a...py:794`).
- **Makale aksiyonu:** bu örtük varsayılan hiçbir yerde belgelenmemişti; Paper 2 §3.3 Eksen 1'e
  kapsam cümlesi eklendi (2026-09-14). Envanter cevabı: "belirlenemez" değil — "explicit seçim yok,
  platform varsayılanı nearest".

## S3. AoA kapsamı (envanter 2.9.5c) — KAPANDI
- **12 yönlü** (4 AOI × 3; Montiferru AoA'ya hiç dahil edilmemiş). 20 hiçbir artefaktta yok.
  Kanıt: `repo/scripts/run_marginal_aoa_completion.py:52`; preregistration
  `drive_new/diagnostics/marginal_aoa_completion/4b2a1c86.../config/preregistration.json`
  → `pair_cardinality = 12`, `directed_pairs` len=12 (ana oturumda sayıldı);
  `comparison/multi_aoi_marginal_aoa_comparison.csv` 12 veri satırı.
- Paper 2 §2.9.5/AoA anlatımı "12 yön, Montiferru hariç" diye net yazılabilir; Emrehan'dan yalnız
  "kalan 8 yön hiç koşulmadı" teyidi beklenir (koşulmadığı arşivden bellidir).

## S4. Window-closure ön-tanım kanıtı (envanter 2.9.3a [UNRESOLVED]) — KAPANDI
- Offset'ler sabit kodlu: `DEFAULT_SHIFTS = (0, 7, 14)` — `repo/src/window_closure_sensitivity.py:84`,
  `repo/src/multi_region_window_closure/contract.py:237-240`; CLI help "Preregistered closure
  shifts" (`run_window_closure_sensitivity.py:60-61`); 5 validator aynı sabiti kullanır.
- **En güçlü artefakt:** `drive_new/diagnostics/window_closure_sensitivity/manavgat_2021/config/
  preregistration.json` — `preregistered_shifts_days=[0,7,14]`, `stage="plan"`, `model_fit=false`,
  `bootstrap_run=false`; mtime 2026-07-30 11:16, model aşaması 2026-07-31 11:20 (≈24 saat sonra).
  `analysis_id` = config'in SHA-256'sı → offset sonradan değişse tüm namespace kırılır; model/compare
  aşamaları shift eşitliğini fail-fast doğrular (`window_closure_sensitivity.py:2581-2588`).
- Dört bölgenin regional koşularında da aynı `[0,7,14]` + `stage=plan` kayıtları var.
- Zayıflık: preregistration.json'da `created_at` alanı yok; sıralama mtime + hash bağına dayanıyor.
  Makalede bu çerçeveyle ("plan-stage record, hash-bound, file-time ordered") yazılmalı.

## Emrehan'a giden 6 sorunun güncel durumu
1. MODIS QC provenance → **lokalde cevaplı** (3 bölge kural öncesi export; Paper 2 §4.2 kanıtı).
2. Muğla AOI dondurma tarihçesi + Bejís gerekçesi → **hâlâ Emrehan'da** (tek gerçek bağımlılık).
3. DEM düşey datumu → yarı-açık (ürün dokümanından kapatılabilir).
4. EE kernel → **lokalde cevaplı** (S2).
5. Window-closure ön-tanım → **lokalde cevaplı** (S4).
6. AoA 12/20 → **lokalde cevaplı** (S3; 12).
