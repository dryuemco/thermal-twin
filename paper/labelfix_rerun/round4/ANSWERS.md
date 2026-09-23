# Üç sorunun cevabı (2026-09-23)

Bu dosyayı yazmak dışında hiçbir şey çalıştırılmadı, hiçbir dosya değiştirilmedi. Bütün sayılar
aşağıda adı geçen dosyalardan okundu.

---

## S1. Etiket düzeltmesi neydi, kapsamı ne?

**Tek cümle:** Eski Manavgat etiketi MCD64A1'i ay sınırına hizalı sorguladığı için Temmuz
görüntüsünü dışarıda bırakıyordu. Bu yüzden yangının ilk dört gününü (DOY 209–212, 28–31 Temmuz
2021) kaçırıp yalnız DOY 213–241'i taşıyordu. Yeni etiket aynı pencereyi (28 Temmuz–31 Ağustos)
eksiksiz okuyor. Sonuç olarak yalnız hücre **eklendi**, hiç hücre çıkmadı:

- Doğal vejetasyonda (TSG, birincil popülasyon) **784 → 2.935 yanık hücre** (+2.151).
- Tüm geçerli hücrelerde 796 → 3.046 (+2.250).
- TSG prevalansı 0.038 → yaklaşık 0.143.

Değişmeyenler:
- Popülasyon aynı: `valid_for_modeling`, `analysis_eligible` ve `burnable_*` etikete bağlı değil.
- Parquet'te yalnız `burned` ve dört `burn_*` kolonu değişiyor. Prediktörler bit düzeyinde aynı.

Eklenen hücreler yangının ilk günlerine ait ve daha alçaktaki alanlarda. Yanık hücre medyan
yüksekliği 508 m'den 272 m'ye iniyor; en büyük bileşen 690'dan 2.934 hücreye çıkıyor.

Kaynaklar:
- Nedeni: `repo/src/step6_validate_fire_relation.py`, `_mcd64a1_collection_query_bounds`. Emrehan
  bunu `183be42` ile 11 Temmuz'da düzeltti; Manavgat ise 8 Temmuz'da export edilmişti.
- Sayılar: `paper/MANAVGAT_RERUN_PLAN.md` §"What changes" (kaynak
  `ems_analyses/labels/r5_manavgat_labelwindow.json`), `paper/labelfix_rerun/pipeline/RUN_LOG.md`.

### Emrehan'ın drive_new çıktıları eski etiketle mi üretildi?

**Evet.** drive_new'deki Manavgat step8a parquet'i `054a1961…` hash'li eski etiket. Manavgat'a
dokunan her donmuş çıktı bu eski etikettendir:

- `experiments/manavgat_2021/` altında etiket rasterlarından step8a–8e'ye ve robustness'a kadar her şey.
- Manavgat'ı içeren 8 transfer yönü (step9b/9c/10) ve legacy `manavgat_2021__evia_2021`.
- Teşhisler: burned_pattern_audit, four_aoi_transfer_decomposition, multi_aoi_transfer_synthesis,
  step9g (iki sürüm), few_shot_recovery, marginal_aoa_completion, coral_lambda_sensitivity,
  window_closure_sensitivity, mugla_subsampling, iki Landsat A/B.
- `ozet_sonuclar*.xlsx` içindeki Manavgat satırları.
- domain_classifier_audit'in sayıları değişmiyor (etiket kullanmıyor). Yalnız kayıt tuttuğu
  n_burned=784 bayat.

Değişmeyenler: Bejís, Muğla, Evia ve Montiferru'nun bölge-içi sonuçları ile Manavgat'sız 12 yön.

### 04_results ve 05_discussion'da eski etiketten gelen kaç sayı var?

Sayım, 19 Eylül'de satır satır çıkarılmış envanterden (`paper/MANAVGAT_RERUN_PLAN.md` §1, 119
satır). Birim **"nicelik satırı"**: bir satır birden fazla basılı sayı taşıyabilir. Örneğin
"Table 3, all five rows" tek satırdır. Yani bunlar tek tek rakam sayısı değil, alt sınır niteliğinde
nicelik sayısıdır. Tek tek basılı rakam sayımı yapılmadı; istenirse yapılır.

| Bölüm | Envanterde birincil konumu burası olan satırlar | Konum sütununda bu bölümü anan satırlar |
|---|---:|---:|
| 04_results §4.1–4.2 (Table 1) | 6 | — |
| 04_results §4.3 (Table 2 ve kontroller) | 10 | — |
| 04_results §4.4 (Table 3) | 13 | — |
| 04_results §4.5–4.6 | 16 | — |
| **04_results toplam** | **45** | **50** |
| **05_discussion** (+ Ek C.5) | **9** | **11** |
| 04 ∪ 05 | — | **57** |

- **Etkilenen tablolar:**
  - Ana metin: **Table 1** (Manavgat satırları), **Table 2** (skar tablosu; Manavgat'ın C satırı
    düşüyor, 8 skar → 7), **Table 3** (beş satırın tamamı; 20 yönün ortalamaları).
  - Ek B: B1, B2, B3, B4, B6, B7, B8, B9, B10.
  - Ek A: A1–A6.
- **Etkilenen figürler:** 3, 4, 5, 6, 7, 8 ve graphical abstract. Envanterdeki figür kalemlerinin
  tamamı etkileniyor. Fig. 3–7 ve GA'nın assert'leri yeni sayılarla bilerek başarısız olacak
  (`MANAVGAT_RERUN_PLAN.md` §2.5).
- **Sonucu değişen yargılar:** `paper/labelfix_rerun/CHANGES.md` §3 (10 madde) ve bu turun
  `_round4/REPORT.md`'si.

### reproduction_check.json (0.0 ve 1.62e-7) eski etiketin frozen-vs-frozen karşılaştırması mı?

**Evet.** `paper/reproduction_check/reproduction_check_5region.json` 2026-08-11 tarihli (commit
`48b56e7`) ve durumu PASS.
- Donmuş artefaktları, **aynı donmuş girdilerden** yeniden hesaplanan değerlerle karşılaştırıyor.
  Manavgat girdisi `054a1961` hash'li eski etiket.
- En büyük fark 1.62e-7: Mont→Man CORAL thermal ROC-AUC, 0.6060780 → 0.6060778; hedef hash
  `054a1961…`.
- Bu dosya hesaplamanın yeniden üretilebildiğini kanıtlıyor, **etiketin doğruluğu hakkında hiçbir
  şey söylemiyor.** Yanlış olan bir etiketi tutarlı biçimde yeniden üretmiş.
- `experiments/cross_region/step10/reproduction_check.json` ayrı bir dosya (Temmuz; bizim step10'un
  Emrehan'la karşılaştırması). O da eski etikette.

### Emrehan'a söylenmeli mi, pipeline yeniden dondurulmalı mı?

**Söylenmeli, evet.** Önerim yeniden dondurmayı istemek. Gerekçe:
- Düzeltilmiş Manavgat pipeline çıktıları şu an yalnız bizim scratch ağacımızda duruyor
  (`rerun_labelfix/pipeline/`). Bu ağaç git'te değil ve arşivlenmemiş.
- Kanonik arşiv (drive_new) Manavgat için eski etikette kalıyor. Yani kanonik kayıt ile bizim
  sayılarımız ayrışmış durumda.
- Emrehan düzeltilmiş kodla Manavgat'ı yeniden export edip dondurursa, bizim yeniden koşumumuz ile
  onunki bağımsız iki koşum olur. RF gürültüsü düzeyinde tutmaları gerekir; bu da ayrı bir doğrulama
  sağlar.

Taslak durumu:
- **Mevcut taslak `paper/emrehan_mail_8.md` (19 Eylül) etiket hatasını doğru anlatıyor. Ama 3.
  maddesi yeniden üretimin "makale için gerekli değil" olduğunu söylüyor.** Bu, yukarıdaki gerekçeyle
  çelişiyor ve revize edilmeli.
- Aynı mesaja pencere kapanışı için `734d621` commit'i isteği de eklenebilir.
- Taslağın gönderilip gönderilmediğini bilmiyorum.

---

## S2. Karşıt çift hayatta mı?

**Önce bir düzeltme:** Donmuş pilotun *şu anki* abstract'ında karşıt-çift cümlesi yok.
- `00_abstract.md` gövdesinde (satır 133) Muğla, Montiferru ya da overlap geçmiyor.
- "Yük taşıyan cümle karşıt çift" notu 2026-08-13 tarihli eski bir taslak notu; cümle sonradan
  çıkarılmış.
- Karşıt çift bugün yalnız **Ek A(s)** ve **Fig. 8**'de (Ek D) duruyor.
- A(s) zaten *ordinal* ve nokta-tahmini bir iddia kuruyor. Bej-Mont yarısı için "5 km blokta karar
  yok" diye açıkça yazıyor.

### Dört transfer AUC'si (thermal, çizildiği gibi, step9b = Fig. 8'in kaynağı)

| Yön | Eski etiket | Düzeltilmiş | 2-hücre CI (Fig. 8'in CI'si) | 10-hücre (~5 km) CI | 10-hücre karar (eski → yeni) |
|---|---|---|---|---|---|
| Man→Muğ | 0.470 | **0.438** | [0.454, 0.486] → [0.419, 0.459] | [0.415, 0.524] → [0.364, 0.506] | belirsiz → belirsiz |
| Muğ→Man | 0.401 | **0.345** | [0.376, 0.426] → [0.332, 0.359] | [0.353, 0.455] → [0.307, 0.386] | şans altı → şans altı |
| Bej→Mont | 0.594 | 0.594 | [0.558, 0.630] (değişmez) | [0.467, 0.687] | belirsiz → belirsiz |
| Mont→Bej | 0.548 | 0.548 | [0.521, 0.578] (değişmez) | [0.479, 0.636] | belirsiz → belirsiz |

- **Doğru taraf mı?** Evet, dört yön de şansın aynı tarafında kalıyor. Man-Muğ şans altında daha
  derine iniyor. Bej-Mont Manavgat içermediği için birebir aynı.
- **CI'ler 0.5'i dışlıyor mu?**
  - 2-hücre CI ile (Fig. 8'in kullandığı): dördü de dışlıyor, eskisi gibi.
  - Mekânsal otokorelasyonu hesaba katan 10-hücre CI ile: **yalnız Muğ→Man dışlıyor.**
- **Bu, etiket düzeltmesinden bağımsız ve önceden de öyleydi.** Donmuş etikette de 10-hücrede yalnız
  Muğ→Man bir karar taşıyordu. Fig. 8'in veri dosyası (`figure_contrast_pairs.json`,
  `transfer_ci_source: drive_new/cross_region/<pair>/step9c`) 2-hücre CI kullanıyor.
  `design/precision/PRECISION.md` ise 2-hücre CI'lerin yaklaşık 3 kat dar olduğunu söylüyor. Yani
  etiket düzeltmesinden bağımsız olarak Fig. 8 bu CI'lerle fazla kesin görünüyor.
  (Kaynak: `transfer_ci_blocksize.json`, donmuş ve round3.)

### Ek A(s)'nin kullandığı çerçeveler ve 20 yön içindeki sıra (paper refit, `aoi_frame_transfer_frozen_mugla.csv`)

| Yön | Çizildiği gibi: eski → yeni (sıra /20) | 10 km collar: eski → yeni (sıra /20) |
|---|---|---|
| Man→Muğ | 0.458 (15) → 0.438 (15) | **0.550 (16) → 0.493 (17)** |
| Muğ→Man | 0.396 (18) → 0.345 (19) | **0.512 (19) → 0.433 (19)**, CI [0.381, 0.491] |
| Bej→Mont | 0.594 (7) → 0.594 (7) | 0.669 (6) → 0.669 (5) |
| Mont→Bej | 0.548 (12) → 0.548 (11) | 0.624 (10) → 0.624 (9) |

- **Ordinal iddia ("en benzer çift en zayıflar arasında, en benzemeyen daha güçlüler arasında")
  duruyor ve güçleniyor.** Man-Muğ 20 yönün 15. ve 19. sırasında, collar'da 17. ve 19. sırasında.
- **A(s)'deki bir cümle artık yanlış:** "transfer is below chance in both directions as drawn but
  above chance under the collar".
  - Düzeltilmiş etikette collar'da da iki yön şans altında: 0.493 ve 0.433.
  - Muğ→Man'in collar CI'si 0.5'i aşağıdan dışlıyor.
- **A(s)'deki uç değerler değişiyor:**
  - Collar'da en zayıf yön yine Man→Bej, ama 0.417 → 0.407.
  - En güçlü yön Muğ→Evia 0.728 → 0.728, değişmiyor.
  - Çizildiği gibi en zayıf yön artık Bej→Man (0.314).

### Niş örtüşmesi sıralaması

**Değişmedi.** Man-Muğ beş ölçünün beşinde de 10 çift içinde **1.**, Bej-Mont beşinde de **10.**
(Schoener D ve Warren I, 1D ortalama ve PCA-2D; yanık-hücre Mahalanobis).

| Ölçü | Man-Muğ, eski → yeni | Bej-Mont, eski → yeni |
|---|---|---|
| Schoener D (1D ort.) | 0.826 → 0.799 | 0.479 → 0.479 |
| Schoener D (PCA-2D) | 0.647 → 0.661 | 0.065 → 0.101 |
| Mahalanobis (yanık) | 2.71 → 2.51 | 8.11 → 7.95 |

Manavgat'sız çiftlerde de PCA-2D ve Mahalanobis değerleri biraz oynuyor. Sebebi, bu ölçülerin beş
bölgenin yanık hücreleri üzerinde ortak bir PCA/binning kullanması. Envanterin kapsam kuralı bunu
öngörüyordu.

### Yön tersinmesi (Fig. 8 panel a)

- Man-Muğ'da 9 değişkende işaret uyumu **4 → 2**, kosinüs **−0.21 → −0.80**. Tersinme belirgin
  biçimde güçleniyor.
- A(s) "as drawn five of nine point opposite ways" diyor; düzeltilmiş etikette **yedi**.
- A(s)'nin collar cümlesi ("elevation 0.561 against 0.606, on the same side of 0.5") da artık doğru
  değil. CHANGES.md §3.1'e göre Manavgat collar elevation 0.376 [0.300, 0.465]; aralık 0.5'in
  altında, Muğla ise 0.606 [0.525, 0.685] ile üstünde. Yani elevation tersinmesi collar'da da
  duruyor.
- Bej-Mont'ta uyum 7/9, kosinüs 0.487; değişmiyor.

**Kısa cevap:** Karşıt çift hayatta, hatta Man-Muğ yarısı güçleniyor. Ama iki uyarı var:
1. Etiketten bağımsız olarak dört CI'nin 0.5'i dışlaması yalnız 2-hücre CI'de geçerli. 10-hücrede
   yalnız Muğ→Man bir karar taşıyor. Bu yüzden iddia ordinal ve nokta-tahmini kalmalı; A(s) zaten
   öyle kurulu.
2. A(s)'nin collar ile ilgili iki cümlesi (collar'da şans üstü; collar'da tersinme yok) düzeltilmiş
   etikette yanlış.

Abstract bu çifti şu an taşımıyor. Dolayısıyla "hayatta değilse abstract yeniden yazılır" koşulu
tetiklenmiyor.

---

## S3. Few-shot: altı yönün tamamı

Metrik thermal ROC-AUC, TSG popülasyonu, 10-hücre (~5 km) dış bloklar. Kurtarma oranı =
(few-shot − ham) / (tavan − ham). **Parantez içindeki aralıklar CI değil, "selection
interval"**: 10 blok-seçim tekrarının %2.5–97.5 persentilleri. Yalnızca hangi blokların seçildiğine
bağlı değişkenliği gösterir. Modül hiçbir hipotez testi yapmıyor.
(Kaynak: `drive_new/.../few_shot_recovery/7e4ca051…/recovery_curve.csv` ve
`rerun_labelfix/pipeline/.../few_shot_recovery/7348dfe7…/recovery_curve.csv`.)

### Eski etiket

| Yön | ham | tavan | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|---|---|
| Bej→Man | 0.444 | 0.797 | 0.03 [−0.15, 0.11] | −0.02 | 0.17 | 0.37 | 0.55 | 0.85 [0.82, 0.86] |
| Bej→Muğ | 0.618 | 0.777 | −0.27 [−0.54, −0.01] | −0.26 | −0.25 | −0.13 | 0.12 | 0.30 [0.07, 0.48] |
| Man→Bej | 0.326 | 0.824 | 0.30 [0.17, 0.41] | 0.35 | 0.56 | 0.67 | 0.80 | 0.89 [0.87, 0.91] |
| Man→Muğ | 0.470 | 0.777 | 0.04 [−0.02, 0.10] | 0.08 | 0.13 | 0.23 | 0.39 | 0.51 [0.44, 0.56] |
| Muğ→Bej | 0.583 | 0.824 | −0.02 [−0.12, 0.10] | 0.08 | 0.17 | 0.34 | 0.66 | 0.85 [0.79, 0.89] |
| Muğ→Man | 0.401 | 0.797 | 0.03 [−0.00, 0.08] | 0.05 | 0.12 | 0.18 | 0.29 | 0.57 [0.55, 0.61] |

### Düzeltilmiş etiket

| Yön | ham | tavan | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|---|---|
| Bej→Man | 0.314 | 0.882 | **0.36** [0.07, 0.47] | 0.44 | 0.61 | 0.68 | 0.77 | 0.89 [0.88, 0.90] |
| Bej→Muğ | 0.618 | 0.777 | −0.27 [−0.54, −0.01] | −0.26 | −0.25 | −0.13 | 0.12 | 0.30 [0.07, 0.48] |
| Man→Bej | 0.396 | 0.824 | 0.12 [0.02, 0.27] | 0.14 | 0.34 | 0.47 | 0.69 | 0.83 [0.79, 0.85] |
| Man→Muğ | 0.438 | 0.777 | 0.03 [0.01, 0.06] | 0.05 | 0.09 | 0.15 | 0.28 | 0.39 [0.35, 0.45] |
| Muğ→Bej | 0.583 | 0.824 | −0.02 [−0.12, 0.10] | 0.08 | 0.17 | 0.34 | 0.66 | 0.85 [0.79, 0.89] |
| Muğ→Man | 0.345 | 0.882 | 0.02 [0.01, 0.07] | 0.07 | 0.12 | 0.17 | 0.30 | 0.52 [0.51, 0.52] |

### Altı yön birlikte ne diyor?

- **Manavgat'sız iki yön (Bej→Muğ, Muğ→Bej) birebir aynı**, olması gerektiği gibi.
- **Tek blokla kurtarma genel bir etki değil.** 1 blokta altı yönün yalnız ikisi 0.1'i geçiyor
  (Bej→Man 0.36, Man→Bej 0.12). Dördü 0.03 ya da altında; Bej→Muğ negatif (−0.27), yani az etiket
  önce zarar veriyor. Bej→Man'in 0.36'sı da geniş bir seçim aralığında: [0.07, 0.47].
  **Bej→Man'deki değişim büyük ölçüde paydadan geliyor:** ham transfer düşüyor (0.444 → 0.314),
  tavan yükseliyor (0.797 → 0.882). Bu yüzden aynı mutlak kazanç daha büyük bir oran olarak
  görünüyor. Tek başına manşet olmamalı.
- **Kaynak Manavgat olunca kurtarma yavaşlıyor:** Man→Bej 32 blokta 0.89 → 0.83, Man→Muğ
  0.51 → 0.39.
- **32 blokta ikiye ayrılma korunuyor:**
  - Eski etiket: üç yön 0.85–0.89, diğer üçü 0.30–0.57.
  - Yeni etiket: üç yön 0.83–0.89 (Bej→Man, Muğ→Bej, Man→Bej), diğer üçü 0.30–0.52 (Bej→Muğ,
    Man→Muğ, Muğ→Man).
  - Makale metnindeki "85 to 89 % in three of six directions and 30 to 57 % in the rest" cümlesi
    yapı olarak doğru kalıyor. Yalnız uç değerler değişiyor: 85 → 83 ve 57 → 52.
- **Hiçbir yön 32 blokta tavana ulaşmıyor.** Eğriler bütün yönlerde bütçeyle artıyor. Tek istisna
  küçük bütçelerdeki gürültü: eski etikette Bej→Man'in 1→2 bloktaki düşüşü, Bej→Muğ'un
  negatif başlangıcı.
