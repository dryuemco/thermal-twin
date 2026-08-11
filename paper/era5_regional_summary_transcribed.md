# ERA5-Land bölgesel meteoroloji özeti — TRANSKRİPSİYON

> **DURUM (2026-08-11): SÜPERSEDE EDİLDİ — ARTIK KAYNAK DEĞİL.**
> Ham dosyalar geldi ve `paper/era5_raw/<analysis_id>/` altına açıldı
> (hash'ler `paper/era5_raw/SHA256SUMS.txt`). **Makaledeki tüm ERA5 sayıları artık
> doğrudan `era5_land_regional_summary.json`'dan okunuyor.** Bu dosya yalnızca
> tarihsel kayıt olarak duruyor.
>
> **Transkripsiyonun doğruluğu kaynağa karşı denetlendi: 80 değerin 80'i de doğru çıktı.**
> Yani xlsx→sohbet→bu dosya zinciri hata üretmemişti. Yine de artık kullanılmıyor —
> kaynak varken türetilmiş kopyaya dayanmak için sebep yok.
>
> **İki şey değişti, aşağıdaki tablolar bu yüzden yanıltıcı olabilir:**
> 1. **z-skorları makaleden tamamen çıkarıldı** (karar, 2026-08-11). İklimatolojik sd'ler
>    bölgeler arası 2,7–6,0 kat (label penceresinde 11,5 kata kadar) değişiyor; z'ler
>    bölgeler arası karşılaştırılamaz. Makale yalnız fiziksel birimde anomali raporluyor.
>    Aşağıdaki z sütunlarını **kullanma**.
> 2. **B4 çözüldü: H1 (küçük-sd) doğrulandı, H2 (mevsimsel pencere) elendi.** Ayrıntı
>    [aşağıda](#3-️-bejís-label-sıcaklık-z566-için-küçük-sd-tek-açıklama-değil--mevsim-karışıklığı-confound-alternatifi-var).

> **⚠️ BU BİR TRANSKRİPSİYONDUR — HAM JSON'DAN DOĞRULANMADI.**
> Sayılar kullanıcı (Yunus Emre Cogurcu) tarafından sohbet üzerinden aktarıldı ve
> buraya elle yazıldı. Ham çıktı dosyaları (`era5_land_regional_summary.json` /
> `.csv`) **okunamadı**, dolayısıyla hiçbir değer kaynağına karşı doğrulanmış
> değildir. Metne işlenmeden önce ham JSON'a karşı doğrulanmalıdır.

## Provenance

| Alan | Değer |
|------|-------|
| Üreten | Emrehan Metin (ERA5-Land bölgesel tanılama) |
| Aktarım yolu | Drive üzerinden okundu → sohbette elle aktarıldı → bu dosyaya transkribe edildi |
| İkinci okuma | Web tarafında ayrı bir Claude oturumu, Drive connector ile **xlsx'ten** kontrol etti (2026-08-11). **Ham JSON'dan DEĞİL.** Bkz. [ikinci okumanın kapsamı](#ikinci-okuma-neyi-kapatır-neyi-kapatmaz) |
| Ham dosyaya erişim | **HİÇ KİMSE OKUMADI.** Ne bu oturum, ne web oturumu. Drive arama indeksi alt klasör içeriğini kapsamıyor (`parentId` sorgusu boş, başlık aramaları sonuçsuz); yalnız klasörün kendisi indeksli. Lokal senkron da hidrate değil. |
| Yakın kaynak | `ozet_sonuclar_window_closure_era5.xlsx`, **"ERA5 Meteoroloji"** sayfası |
| Nihai kaynak (okunamadı) | `drive_new/diagnostics/era5_land_regional/4850c16556eb8be02594374831cfb7e3b1703c813a998638f99f418eb1ce05b2/` |
| Doğrulama durumu (sayılar) | **DOĞRULANMADI** — ham JSON/CSV açılamadı |
| Doğrulama durumu (yöntem) | ✅ **KODDAN DOĞRULANDI** — `repo/src/era5_land_regional_diagnostic.py` @ `48b56e7`, bkz. [Yöntem](#yöntem--koddan-doğrulandı) |
| Lokal erişim | **YOK** — Drive senkron alt ağacı hidrate değil; `Test-Path`/`Get-ChildItem` zaman aşımı ve `IOException` verdi. Drive API araması da bu dosyaları indekslemiyor (`parentId` sorgusu boş döndü). |
| Transkripsiyon tarihi | 2026-08-11 |

### İkinci okuma: neyi kapatır, neyi kapatmaz

> **Bu bölüm 2026-08-11'de düzeltildi.** Önceki hali "web oturumu ham dosyadan okudu"
> diyordu; bu **yanlıştı**. Doğrusu: ikinci okuma da `ozet_sonuclar_window_closure_era5.xlsx`
> üzerinden yapıldı. **Ham JSON/CSV'yi bu zincirde hiç kimse okumadı.**

Her iki okuma da aynı türetilmiş dosyaya (xlsx) dayanıyor, yani **bağımsız kaynak
değiller — bağımsız okuyucular.**

**Kapattığı risk:** xlsx → sohbet → bu dosya zincirindeki **aktarım/yazım hatası**.
İki ayrı okuyucu aynı xlsx'ten aynı sayıları çıkardığına göre, tablodaki 80 değerin
xlsx'tekilerle uyuşmaması düşük olasılıklı.

**Kapatmadığı risk — asıl olan bu:** xlsx'in kendisi `era5_land_regional_summary.json`'dan
doğru üretilmiş mi? Bu adım **hiç denetlenmedi** ve iki okuyucu da aynı xlsx'e baktığı için
denetlenemez de. xlsx ile JSON arasında bir kopyalama/biçimlendirme/yuvarlama adımı varsa,
tekrarlanan okuma o hatayı yakalamaz — yalnız çoğaltır.

**Ayrıca hâlâ elde olmayanlar:**

1. **`climatology_sd` değerleri** — Uyarı 1'deki "küçük-sd artefaktı" iddiasının sayısal
   dayanağı. xlsx bu sütunu taşımıyor.
2. **`climatology_realizations`** (dört yıllık ham değer) — kodda JSON'a yazıldığı
   doğrulandı (bkz. A20), ama xlsx'te yok.
3. **Metrik anahtarlarının tam adı** — xlsx başlıkları istatistiği söylüyor (aşağıya bak),
   JSON anahtar adlarını değil.
4. **`n_hours_observed`** — pencere bütünlüğü kanıtı.

**Sonuç:** transkripsiyon güvenilirliği yükseldi, **doğrulama durumu değişmedi.**
Dosyanın başındaki uyarı geçerliliğini koruyor.

**Doğrulanabilen yan kanıtlar** (bu tablolardaki sayıları doğrulamaz, yalnız
çıktının varlığını destekler):

- `era5_land_regional/` klasörü hem lokal listelemede hem Drive API'de görünüyor
  (Drive ID `1oiIqtChE-RO27qufx9OEp3P_0lq6hHwA`); `analysis_id` alt klasörü
  `4850c165...05b2` (Drive ID `1fajHhBwxS6cMj5xO53YJQo4vGXhjgwaa`), oluşturma 2026-08-08.
- `ozet_sonuclar_window_closure_era5.xlsx` `drive_new/` kökünde mevcut
  (41.254 byte, değişiklik 2026-08-10 11:39).
- Kaynak kod `repo/`'da mevcut, commit `48b56e7`:
  `src/era5_land_regional_diagnostic.py`,
  `scripts/run_era5_land_regional_diagnostic.py`,
  `scripts/validate_era5_land_regional_diagnostic.py`,
  `tests/test_era5_land_regional_diagnostic.py`.

---

## ⚠️ İKİ ZORUNLU UYARI — HER KULLANIMDA BİRLİKTE GİTMELİ

Bu tablolardan alıntılanan **her** sayı, aşağıdaki iki uyarıyla birlikte
taşınmalıdır. Uyarılardan biri olmadan alıntı yapılmaz.

### Uyarı 1 — z-skorları n=4'lük iklimatolojiden, çok kararsız

İklimatoloji yalnızca **4 yıl** (2017–2020). z-skorları n=4'ten hesaplanan bir
standart sapmaya bölünüyor, dolayısıyla **çok kararsız**. Uç değerler küçük-sd
artefaktıdır, gerçek sigma değildir:

- **Bejís label sıcaklık z = +5.66** → küçük-sd artefaktı, 5 sigma DEĞİL.
- **Muğla predictor rüzgar z = +5.32** → küçük-sd artefaktı, 5 sigma DEĞİL.

**|z| > 2 olan hiçbir değer harfiyen yorumlanmamalıdır.**

### Uyarı 2 — Label penceresi yangın havası DEĞİL

Label penceresi **tutuşma anıyla başlıyor** ve sonbahar yağışlarını kapsıyor
(ör. **Bejís 121,41 mm**). Bu pencere yangın-günü hava koşullarını temsil etmez.

> **Koddan düzeltme:** uyarının orijinal ifadesi label penceresini "45–60 gün"
> diyordu; registry'deki gerçek uzunluklar **35–59 gün** (Manavgat 35, Montiferru
> 39 — ikisi de 45'in altında). Uyarının özü değişmiyor, yalnız sayı düzeltildi.
> Tam tarihler aşağıdaki [pencere tablosunda](#pencereler-registryden-doğrulandı).

**Betimsel karakterizasyon için yalnızca predictor penceresi kullanılmalıdır.**
Label penceresi tabloları buraya bütünlük için yazıldı, yorum için değil.

---

## Predictor penceresi

*(Betimsel karakterizasyon için kullanılabilecek olan pencere budur — Uyarı 1 geçerli.)*

| Bölge | Sıcaklık (°C) | Sıcaklık z | RH (%) | RH z | Rüzgar (m/s) | Rüzgar z | Yağış (mm) | Yağış z |
|-------|--------------:|-----------:|-------:|-----:|-------------:|---------:|-----------:|--------:|
| Manavgat | 22.72 | −0.11 | 54.05 | −1.25 | 1.80 | +1.71 | 48.08 | −0.05 |
| Bejís | 24.05 | +1.94 | 55.40 | −0.14 | 2.02 | +0.14 | 81.52 | +2.89 |
| Muğla | 25.28 | +0.50 | 51.61 | −1.48 | 2.97 | **+5.32** | 27.70 | −0.45 |
| Evia Extended | 25.73 | +2.68 | 59.64 | −2.96 | 2.06 | −2.21 | 19.72 | −1.28 |
| Montiferru | 22.57 | +0.42 | 64.17 | −0.43 | 2.22 | +0.76 | 14.95 | −1.04 |

## Label penceresi

*(**Yangın havası değildir** — Uyarı 2. Betimsel karakterizasyonda kullanılmaz.)*

| Bölge | Sıcaklık (°C) | Sıcaklık z | RH (%) | RH z | Rüzgar (m/s) | Rüzgar z | Yağış (mm) | Yağış z |
|-------|--------------:|-----------:|-------:|-----:|-------------:|---------:|-----------:|--------:|
| Manavgat | 26.13 | +2.32 | 41.73 | −1.93 | 2.05 | +3.88 | 8.98 | −0.60 |
| Bejís | 20.69 | **+5.66** | 63.57 | −0.69 | 1.96 | +0.19 | 121.41 | +1.10 |
| Muğla | 27.24 | +1.21 | 45.22 | −3.27 | 2.95 | +3.99 | 8.20 | −1.02 |
| Evia Extended | 24.48 | +1.91 | 60.52 | −0.89 | 2.63 | −0.84 | 68.35 | −0.31 |
| Montiferru | 25.25 | +0.33 | 60.29 | −0.11 | 2.17 | +0.23 | 2.42 | −0.99 |

---

## Yöntem — koddan doğrulandı

> **Durum: ✅ Emrehan'ın tarifinin her maddesi kodda teyit edildi.** Kaynak
> `repo/src/era5_land_regional_diagnostic.py` (1724 satır) ve `repo/core/regions.py`,
> commit `48b56e7`. Aşağıdaki satır numaraları o commit'e aittir.
> **Bu doğrulama yöntemi kapsar, sayıları değil** — yukarıdaki iki tablo hâlâ
> doğrulanmamış transkripsiyondur.

| Tarif edilen | Kod | Durum |
|---|---|---|
| `ECMWF/ERA5_LAND/HOURLY` | `COLLECTION_ID` (:187) | ✅ |
| 5 bant: `temperature_2m`, `dewpoint_temperature_2m`, u/v 10 m, `total_precipitation_hourly` | `SOURCE_BANDS` (:188) | ✅ birebir |
| Pencereler registry'den, hard-code tarih yok | `observed_windows()` → `get_experiment()` (:538); `OBSERVED_WINDOW_SOURCE = "core.regions.EXPERIMENTS (registry)"` (:212) | ✅ |
| İklimatoloji = aynı takvim penceresinin 2017–2020 karşılıkları | `CLIMATOLOGY_YEARS = (2017, 2018, 2019, 2020)` (:196); `map_window_to_year()` ay/gün'ü her referans yılına taşıyor (:566) | ✅ |
| Piksel-alan ağırlıklı AOI ortalaması, ERA5-Land native grid | `_weighted_regional_means()` (:1024) | ✅ ve **açıkça uygulanmış** |

### Tarifin ötesinde, koddan çıkan ek detaylar

**Ağırlıklandırma gerçekten alan ağırlıklı** (:1024–1056). `sum(value × pixelArea) / sum(pixelArea)`,
`ee.Reducer.sum()` ile, ERA5-Land'in kendi `crs` + `crsTransform`'unda (`bestEffort=False`).
Payda **her değişkenin kendi maskesiyle** maskeleniyor, yani AOI'nin bir kısmında tanımsız olan
bir değişken o alanla kredilendirilmiyor. Kod ayrıca `ee.Reducer.mean()`'in alan ağırlıklandırma
**olmadığını** ve kullanılmadığını yazılı olarak belirtiyor (:250–252).

**z-skoru aritmetiği** (:47–50, :662–673):
`anomaly = observed − climatology_mean`, `standardized_anomaly = anomaly / climatology_sd`,
burada `climatology_sd` = **örneklem SD'si, `SD_DDOF = 1`** (:197). → Uyarı 1'in dayanağı
kodda: payda n=4'ten ddof=1 ile, yani 3 serbestlik dereceli bir SD. `climatology_sd == 0`
ise standardize anomali `None` yazılıyor (asla `inf`, asla 0) ve `zero_climatology_sd = True`
kaydediliyor (:52, :721).

**Türetilmiş değişkenler piksel-saat düzeyinde, asla pencere ortalamasından** (:58–72):
- `temperature_c = temperature_2m − 273.15`
- RH: ECMWF/Tetens, **su fazı üzerinden** (T0=273.16 K, a1=611.21 Pa, a3=17.502, a4=32.19 K),
  `RH = 100·es(Td)/es(T)`. Buz/karışık faz dalı yok. **RH `[0,100]`'e kırpılmıyor** —
  yalnız sonluluk QA'sı yapılıyor (:66–67, :231).
- `wind_speed_m_s = sqrt(u10² + v10²)`
- `precipitation_mm = total_precipitation_hourly × 1000`; **kümülatif `total_precipitation`
  bandı asla kullanılmıyor**, dolayısıyla koşan toplamın farkını alma işlemi yok (:70–72).

**Zamansal agregasyon saatlik bölgesel ortalamalar serisi üzerinde** (:74–84, :632–652).
`VARIABLES` tablosu (:264):

| Değişken | Üretilen istatistikler |
|---|---|
| `temperature_c` | mean, max |
| `relative_humidity_percent` | mean, max |
| `wind_speed_m_s` | mean, max |
| `precipitation_mm` | mean, max, **total** |

`max` = **maksimum bölgesel-saat koşulu**, AOI içindeki en uç tek piksel değil.

**Pencere bütünlüğü fail-closed** (:200–207): her pencerenin zaman damgaları
`[start 00:00, end_exclusive 00:00)` tam bitişik UTC saatlik dizisine eşit olmalı
(`n_days_inclusive × 24` saat). Eksik/yinelenen/sırasız/kaymış/fazla saat sıralanmıyor,
tekilleştirilmiyor, interpolasyon yapılmıyor — **hata veriyor**.

**29 Şubat** bir referans yılında temsil edilemezse kaydırılmıyor, hata veriliyor (:53–55).
Beş AOI'de böyle bir sınır yok.

**Kapsam beyanı** (:14, :1148): diagnostic kendini `"is_model_predictor": False` olarak
kaydediyor — "model predictor DEĞİL, feature kaynağı DEĞİL, Step5'in parçası DEĞİL".
Bu, Uyarı 2'nin çerçevesini kodun kendisi destekliyor.

### Pencereler — registry'den doğrulandı

`core/regions.py`'den okunan tam sınırlar. Registry bitiş tarihleri **dahil** (inclusive);
EE filtresi `[start 00:00 UTC, end_inclusive + 1 gün 00:00 UTC)` (:213–216).

| AOI | Predictor | Gün | Saat | Label | Gün | Saat |
|-----|-----------|----:|-----:|-------|----:|-----:|
| manavgat_2021 | 2021-06-01 → 2021-07-27 | 57 | 1368 | 2021-07-28 → 2021-08-31 | **35** | 840 |
| bejis_2022 | 2022-06-15 → 2022-08-14 | 61 | 1464 | 2022-08-15 → 2022-09-30 | 47 | 1128 |
| mugla_2021 | 2021-06-01 → 2021-07-28 | 58 | 1392 | 2021-07-29 → 2021-09-15 | 49 | 1176 |
| evia_2021_extended | 2021-06-05 → 2021-08-02 | 59 | 1416 | 2021-08-03 → 2021-09-30 | 59 | 1416 |
| montiferru_2021 | 2021-05-25 → 2021-07-23 | 60 | 1440 | 2021-07-24 → 2021-08-31 | **39** | 936 |

Predictor **57–61 gün**, label **35–59 gün**. Her AOI'de label penceresi predictor'ın
bittiği günün ertesi günü başlıyor (bitişiklik beşinde de doğrulandı) — yani label
penceresinin başlangıcı tutuşma günü. Uyarı 2'deki "tutuşmayla başlıyor" ifadesi doğru.

### Kohort — doğrulandı

`DEFAULT_EXPERIMENTS` (:168) tam olarak beş AOI, tam bu sırayla: `manavgat_2021`,
`bejis_2022`, `mugla_2021`, `evia_2021_extended`, `montiferru_2021` — transkripsiyondaki
satır sırasıyla aynı. `mugla_2022` `NON_DEFAULT_EXPERIMENTS`'te (:180), gerekçe:
"provisional temporal contract awaiting supervisor decision". Yalnız açık `--experiments`
talebiyle girebiliyor, o da `analysis_id`'yi değiştiriyor.

---

## ⚠️ Transkripsiyonla uyuşmayan / eksik kalan noktalar

**1. ✅ ÇÖZÜLDÜ — tablo tek satırda karışık istatistik taşıyor.**
Kod yağış için üç istatistik üretiyor (`mean`, `max`, `total`), diğer üç değişken için
ikisini (`mean`, `max`). Hangisinin alındığını **xlsx sütun başlıkları kanıtlıyor**:

> **"Sıcaklık ort." · "RH ort." · "Rüzgâr ort." · "Yağış toplam"**

Yani T/RH/rüzgar = **pencere ortalaması** (`mean`), yağış = **pencere toplamı** (`total`).
Bu, büyüklükten yaptığım çıkarımı doğruluyor (Manavgat predictor 48,08 mm / 1368 saat →
saatlik ortalama 0,035 mm olurdu; 48 mm/saat 57 gün boyunca absürt).

Kalan tek belirsizlik JSON anahtarının tam adı (`predictor_precipitation_mm_total_observed`
biçiminde olmalı) — bilimsel olarak önemsiz. **Metne girerken sütun başlığı
"Yağış toplamı (mm)" olmalı, "Yağış (mm)" değil.**

**2. Yağış z-skoru da toplam üzerinden.** Aynı gerekçeyle Bejís predictor +2,89 ve
label +1,10 gibi değerler pencere **toplamının** iklimatolojik toplamlara göre anomalisi.
Pencere uzunlukları AOI'ler arasında farklı (predictor 57–61 gün, label 35–59 gün)
olduğundan **yağış toplamları AOI'ler arası doğrudan kıyaslanamaz** — z-skorları
kıyaslanabilir (her AOI kendi takvim penceresine göre normalize), ham mm sütunu değil.

**3. ⚠️ Bejís label sıcaklık z=+5.66 için küçük-sd TEK açıklama değil — mevsim
karışıklığı (confound) alternatifi var.**

Bejís'in label sıcaklığı **20,69 °C ile beş bölgenin mutlak en düşüğü** (diğerleri
24–27 °C) ama z-skoru **en yükseği** (+5,66). İki rakip açıklama:

| Hipotez | Mekanizma | Beklenen imza |
|---|---|---|
| **H1: küçük-sd artefaktı** | n=4 iklimatolojide 2017–2020 sıcaklıkları birbirine çok yakın → `climatology_sd` küçük → z şişiyor | `climatology_sd` ≈ 0,1–0,3 °C |
| **H2: mevsim confound'u** | Label penceresi sonbahara uzanıyor; hem gözlem hem iklimatoloji düşük ama pencere kompozisyonu farklı davranıyor | Bejís label penceresi diğerlerinden daha geç bitiyor |

**H2 lehine gözlem:** Bejís yağışı 121,41 mm ile açık ara en yüksek — sonbahar yağışı
imzası. **H2 aleyhine gözlem:** registry tarihleri (koddan okundu) Bejís label penceresini
2022-08-15 → 2022-09-30 olarak veriyor; Muğla (→09-15) ve Evia (→09-30) de eylüle uzanıyor,
yani Bejís mevsimsel olarak **tekil değil**. Evia'nın label penceresi Bejís'le aynı gün
bitiyor ve z'si yalnız +1,91.

Bu, H2'yi zayıflatır ama elemez: Bejís'in label penceresi 47 gün ve **15 Ağustos'ta**
başlıyor — beş AOI'nin en geç başlangıcı. Yani penceresi orantısal olarak daha fazla
sonbahar içeriyor olabilir.

**✅ ÇÖZÜLDÜ 2026-08-11, ham JSON'dan: H1 doğrulandı, H2 elendi.**

Bejís label `temperature_c_mean` — dört referans yılı: **19,643 / 19,953 / 19,942 / 19,909 °C**.
Dördü üçte bir derecelik bir aralıkta; `climatology_sd = 0,1470 °C`. Fiziksel anomali
yalnızca **+0,83 °C**, ama 0,147'ye bölününce z = **+5,655**. H1 (küçük-sd artefaktı)
doğrulandı.

Muğla predictor `wind_speed_m_s_mean` — **2,688 / 2,670 / 2,576 / 2,561 m/s**,
`climatology_sd = 0,0647`, anomali **+0,344 m/s**, z = **+5,323**. Aynı mekanizma.

**H2 (mevsimsel pencere) elendi.** Evia'nın label penceresi Bejís'le **aynı gün** kapanıyor
(2021-09-30) ve **12 gün daha uzun** (59'a karşı 47) — mevsim kompozisyonu açıklaması Evia'ya
en az Bejís kadar uygulanmalıydı. Ama Evia'nın karşılaştırılabilir **+0,67 °C** anomalisi
yalnız **+1,91** z veriyor, çünkü sd'si **0,351 °C** (Bejís'in 2,4 katı). İki bölgenin fiziksel
anomalisi benzer; farklı olan sadece payda.

Bu bulgu z-skorlarını makaleden çıkarma kararının doğrudan gerekçesi oldu.

**4. Hâlâ ham JSON gerektirenler.** Aşağıdaki kontroller
`era5_land_regional_summary.json` açılmadan kapanamaz:
- 80 değerin birebir eşleşmesi (**ve xlsx'in JSON'dan doğru türetildiği** — bu adım
  hiç denetlenmedi, bkz. [ikinci okuma](#ikinci-okuma-neyi-kapatır-neyi-kapatmaz));
- `climatology_sd` değerleri — Uyarı 1'in sayısal dayanağı;
- `climatology_realizations` (dört yıllık ham değer) — yukarıdaki H1/H2 ayrımı;
- `n_hours_observed` — pencere bütünlüğü (beklenen: Manavgat pred. 1368, Bejís 1464,
  Muğla 1392, Evia 1416, Montiferru 1440);
- `zero_climatology_sd` bayrağının hiçbir hücrede `True` olmadığı;
- `scientific_contract.json` hash'inin `4850c165…05b2` `analysis_id`'siyle tutarlılığı.

**Kapanan açık uçlar:** ddof sorusu (**ddof=1**, kesin), iklimatoloji yıl aralığı
(**2017–2020**, kesin), ağırlıklı ortalama tanımı (kesin), AOI başına pencere tarihleri
(kesin), kohort bileşimi (kesin), **hangi istatistik alındığı** (kesin — xlsx başlıkları).

---

## Runner ve validator — koddan (Methods için ek malzeme)

Kaynak: `scripts/run_era5_land_regional_diagnostic.py` (182 satır),
`scripts/validate_era5_land_regional_diagnostic.py` (669 satır), commit `48b56e7`.

### Runner

Bilimsel mantık taşımayan ince bir dispatcher; kohort, pencere dönüşümü, türetme
reçeteleri, alan ağırlıklandırma ve iklimatoloji aritmetiğinin tamamı modülde
(:5–7). İki mod: `--dry-run` (Earth Engine oturumu açmaz, sorgu atmaz, dizin
yaratmaz, dosya yazmaz) ve normal koşu. Dry-run çıktısı iklimatolojiyi
`"(sample SD, ddof=1)"` olarak basıyor (:63) — ddof=1 bulgusunun ikinci bağımsız teyidi.

CLI açıklaması diagnostic'in kapsamını yazılı olarak sınırlıyor (:106–108):
*"Explanatory only — not a model predictor and not part of Step5/Step7/Step8/Step9/Step10.
Produces a table; no raster is exported."*

### Validator — makalede alıntılanabilir garantiler

İki mod (dry-run = yalnız sözleşme; actual = üretilmiş namespace'e karşı tüm kontroller).
Her kontrol `{check_id, status, expected, observed, evidence_path}` üretiyor; **tek bir
FAIL genel durumu FAIL yapıyor ve exit kodu 1** (:11–12). Toplam ~30 kontrol. Methods
açısından en anlamlı olanlar:

| Kontrol | Ne garanti ediyor |
|---|---|
| **A20** | `climatology_mean` ve `climatology_sd`, JSON'da saklanan **dört yıllık ham değerden** yeniden hesaplanabiliyor (`rel_tol=1e-12`). → İklimatoloji aritmetiği denetlenebilir; H1/H2 ayrımı ham dosyayla **yapılabilir**. |
| **A25** | Her gözlem penceresi saatlik tam: `n_hours_observed == n_days_inclusive × 24`. |
| **A26** | **Her iklimatoloji realizasyonu da** saatlik tam — 2017–2020'nin dördü ayrı ayrı. |
| **A16** | `standardized_anomaly` **tam olarak** `climatology_sd == 0` olduğunda null; başka hiçbir durumda değil. |
| **A15 / A18 / A19** | `observed`, `climatology_mean`, `climatology_sd`, `anomaly` sonlu; JSON'da hiç `inf`/`NaN` yok, serileştirilmiş metinde `Infinity`/`NaN` **literali** bile yok. |
| **A17** | CSV ve JSON değerleri birebir aynı (her metrik, her alan). |
| **A02** | `analysis_id`, bilimsel konfigürasyonun hash'i — klasör adıyla eşleşmeli. |
| **A09 / A11** | Referans yıllar tam olarak 2017–2020; koleksiyon ve bant listesi sözleşmeyle aynı. |
| **A07** | `mugla_2022` varsayılan beş-AOI analizinde **yok**. |
| **A24** | Namespace yalnız beklenen dört dosyayı içeriyor — **hiçbir raster/export sızmamış**. |
| **A27** | Saatlik bütünlük kuralı ve `incomplete_window_policy: fail_closed` hash'lenmiş sözleşmenin parçası. |

**Methods'a şu cümle kurulabilir:** iklimatoloji ortalaması ve standart sapması, saklanan
dört yıllık realizasyondan 1e-12 toleransla yeniden üretilebilir; gözlem ve iklimatoloji
pencerelerinin tamamı saatlik eksiksizdir; eksik pencere politikası fail-closed'dır.

> **Not:** Bunlar validator'ın **kontrol ettiği** garantiler. Validator'ın bu çıktı
> üzerinde gerçekten **koşturulduğuna** ve PASS verdiğine dair elimde kanıt yok —
> bir validator raporu görmedim. Ham dosyalar gelince Emrehan'dan validator çıktısını
> da istemek gerekir.
