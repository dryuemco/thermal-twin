> **CANCELLED 2026-09-23. Never sent.** Emrehan is no longer active on the project, so this draft is
> withdrawn and archived unchanged below. Its item 3 ("re-running Manavgat is not needed for the paper")
> is superseded: the Manavgat re-freeze on the corrected label is to be done on this side
> (`paper/labelfix_rerun/round4/`). Nothing in this file is a current statement.

# Emrehan'a cevap — 19 Eylül (taslak; GÖNDERİLMEDİ)

Merhaba Emrehan,

Teşekkürler, çok faydalı oldu. Manavgat'ı kendi tarafımda da doğruladım: `step0/aoi_preview.geojson` final koordinatları (31.05, 36.72, 31.85, 37.35) taşıyor ve 7 Temmuz 18:10 tarihli; ilk gate sonucu 8 Temmuz 13:13. Makalede §3.1'i buna göre düzelttim: Manavgat'ın kutusu artık "ilk gate sonucundan önce tarihli" olarak geçiyor. Bejís ve Muğla için mevcut ifade kalıyor.

Asıl yazmam gereken başka bir şey var. Hakem simülasyonu sırasında yaptığımız etiket kalitesi kontrollerinde Manavgat'ın donmuş etiketinde bir sorun çıktı ve doğruladık:

- Label penceresi 28 Temmuz 2021'de (DOY 209) açılıyor, ama donmuş `validation/labels/mcd64a1_raw.tif` yalnızca DOY 213–241 içeriyor. 28–31 Temmuz tamamen eksik.
- Sebep, `step6_validate_fire_relation.py`'deki ay-hizalı MCD64A1 sorgu hatası (`_mcd64a1_collection_query_bounds`). Senin düzeltmen `183be42`'de, 11 Temmuz'da geldi; Manavgat etiket raster'ı ise 8 Temmuz'da, düzeltmeden önce export edilmiş. Label başlangıcı ayın 1'i olmadığı için Temmuz görüntüsü sessizce dışlanmış.
- Etkisi büyük: doğal vejetasyonda yanık hücre 784 yerine 2.935 olmalı; makale Manavgat'ın yanık hücrelerinin %27'sini kullanıyordu. Diğer bölgeler etkilenmiyor (pencereleri ilk label gününde açılıyor).

Ne yaptık: raster'ı senin düzeltilmiş `build_raw_burndate_image` fonksiyonunla aynı grid üzerinde yeniden kurduk ve step8a etiket kolonlarını yine senin `build_dataset` koduyla yeniden hesapladık. Kontrol olarak aynı yolu donmuş raster'a uyguladığımızda kanonik parquet'in 7 etiket kolonunu 0 farkla üretiyor; düzeltilmiş tabloda etiket dışındaki 72 kolon bit düzeyinde aynı. Gate sonucu değişmiyor (pass, doğal oran 0.955). Düzeltilmiş veriyi birincil yaptık ve Manavgat'a bağlı her sonucu, pipeline'ın kopyası üzerinde yeniden koşturduk; `repo/` ve `drive_new/`'e hiç yazılmadı. Her adımda önce donmuş etiketle drive_new'i yeniden üretip kontrol ettik (≤1.3e-5, RF thread gürültüsü).

Sonuçlar: bölge içi termal katkı değişmiyor (+0.067), ama transfer ve işaret dönmesi tarafı belirgin değişiyor; bazı iddiaları yeniden yazıyorum. Ayrıntı ve komutlar repoda: `paper/data/manavgat_2021/LABEL_CORRECTION.md` ve `paper/labelfix_rerun/`.

Senden istediklerim:
1. Bu teşhise katılıyor musun, gözden kaçırdığım bir şey var mı? Özellikle Manavgat etiketinin düzeltmeden sonra yeniden export edilip edilmediğini hatırlıyor musun?
2. Envantere bu hatayı ve düzeltmeyi bir madde olarak ekler misin?
3. Kendi pipeline çıktılarında Manavgat'ı yeniden üretmek istersen düzeltme komutları dosyada; ama makale için gerekli değil.

Bir de yön değişikliği var. Hakem simülasyonu ve bu düzeltmeler, mevcut beş bölgelik tasarımın yapısal
sınırlarını netleştirdi: elle çizilmiş AOI'ler, bölge başına tek yangın sezonu (bölge ile olay ayrılamıyor),
hava durumu ve insan etkisi değişkenlerinin olmaması. Bu makaleyi göndermek yerine pilot olarak
dondurduk (`paper/PILOT_FROZEN.md`, tag `pilot-v1-frozen`) ve çalışmayı baştan tasarlıyoruz:

- Sabit bir gridden kuralla seçilen ~10 karo (0.5°), her birinde 3–5 yangın sezonu (2015–2024), 2 mühürlü
  dış doğrulama karosu ve 1 negatif kontrol karosu;
- MCD64A1'in kendi 463 m gridi (etiket yeniden örneklenmiyor), testli sorgu, EFFIS ile bağımsız doğrulama;
- sezon öncesi (31 Mayıs'a kadar) predictor'lar: arazi, yakıt, vejetasyon, termal (iki kanal), öncül hava
  durumu ve ERA5-Land'den hesaplanan FWI kodları, insan erişimi, yangın geçmişi;
- sezon içi / yıllar arası / bölgeler arası transferin ayrı ölçüldüğü, sonuçlar görülmeden kaydedilen bir
  analiz planı;
- testli, hash doğrulamalı, konteynerli yeni bir altyapı. Senin doğrulanmış parçaların (düzeltilmiş
  MCD64A1 sorgusu, gate, blok ataması) atıfla yeniden kullanılacak.

Tasarım `design/STUDY_DESIGN.md`'de (v0.3). Bu çalışmada katkı veren ortak yazar olmanı istiyoruz; özellikle
Earth Engine export'ları ve pipeline tarafında. Ön kayıt birkaç gün içinde hazır olacak; yayımlanmadan
önce senin de okumanı ve itirazın varsa belirtmeni isterim, çünkü yayımlandıktan sonra değişiklikler
ancak sapma olarak kaydedilebiliyor. Hedef, yaklaşık iki ay içinde EMS'e göndermek.

İyi çalışmalar.
Yunus Emre
