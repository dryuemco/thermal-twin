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

Metin bittiğinde son hâlini onayına göndereceğim.

İyi çalışmalar.
Yunus Emre
