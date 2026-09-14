# Mail 6 — Methods envanteri dönüşü (taslak, 2026-09-14)

**Kime:** emrehann17@gmail.com
**Konu:** (Re: — mevcut dizinin devamı, 11 Eylül mailine cevap)

---

Merhaba Emrehan,

Envanter için teşekkürler, eline sağlık. Tamamını makale taslağıyla satır satır karşılaştırdım; çekirdek modelleme bölümleri (2.3, 2.5–2.8) taslakla neredeyse birebir tutuyor. Pre-label burn exclusion için verdiğin kesin sayılar (Muğla 49, Evia 16, Montiferru 61) de doğrudan makaleye girecek.

Önce önemli olanı söyleyeyim: **2.3.8'de haklısın.** Taslakta valid_for_modeling tanımını "hiçbir termal kanal eksik değil" diye yazmıştım; bugün beş bölgenin donmuş parquet'lerinde kontrol ettim, termal tamlık tanımın parçası değil — valid hücrelerin Manavgat'ta %8.5'inde, Muğla'da %33'ünde, Evia'da %57.5'inde en az bir termal kanal NaN. Bu cümleyi ve eksik termal değerlerin nasıl işlendiğini ben düzelteceğim. İyi yakalama, bu hakem önünde bizi kurtaran türden bir düzeltme.

İkinci not: pipeline bu makinede hâlâ çalışır ve tekrar üretir durumda. Bugün step8b'yi 48b56e7'de hiç değiştirmeden donmuş Manavgat step8a'ya koştum; arşivdeki metriklerle 142 sayısal alanın tamamı tuttu (en büyük fark 1e-16 mertebesinde, tablo rakamları 16 haneye kadar aynı). Yani koşu gerektiren her şeyi buradan yapabiliyorum — **senden yeniden koşu istemeyeceğim, sadece bilgi/kayıt düzeyinde şu işaretli noktaları kapatmanı rica ediyorum:**

1. **MODIS QC provenance (2.2.2d):** QC kuralının (LST_Day_1km > 0, QC_Day & 3 == 0, count ≥ 3) Manavgat/Bejís/Muğla koşularında da aynı olduğunu gösteren bir kayıt — commit, config veya frozen rapor referansı yeterli.
2. **Muğla AOI dondurma tarihçesi (2.1.3):** Muğla bbox'ının gate/performans sonuçları görülmeden önce sabitlendiğini gösteren tarihli bir iz (commit, not, mesaj). Bejís için de kenar seçim gerekçesini bir-iki cümleyle yazarsan yeter — makalede AOI-seçimi iddiasının gücünü bölge bazında kanıta göre ayarlayacağım.
3. **DEM düşey datumu (2.4.4i):** GLO-30 için hangi datum (EGM2008?) — kaynak linkiyle.
4. **EE interpolasyon çekirdeği (2.2.6c):** Upstream Earth Engine export/reproject'lerinde kullanılan kernel'in ne olduğu netleşebilir mi, yoksa "belirlenemez" olarak mı kalmalı?
5. **Window-closure eşikleri (2.9.3a):** −7/−14 gün varyantlarının önceden tanımlı olduğuna dair kayıt var mı?
6. **AoA kapsamı (2.9.5c):** 12 yönlük özet mi kaldı, yoksa 20 yönün tamamı bir yerde mevcut mu? Sadece net cevap lazım, koşu değil.

Bundan sonrası için: envanteri Methods düzyazısına çevirmene gerek yok, o dönüşümü ben yapacağım — makale yazımı bende. Bir de bilgin olsun: çalışmayı iki makaleye ayırdık (transfer analizi + preprocessing/veri-işleme). 2.2 ve 2.4'te çıkardığın malzeme ikinci makalenin Methods çekirdeği olacak, yani o emek fazlasıyla yerini bulacak.

Küçük bir yazım notu: 2.9.4'te kanonik lambda "λ=105" yazılmış, 10⁻⁵ olacak.

İyi çalışmalar.

---

## Dahili not (maile girmedi)
- Sistem kontrolü 2026-09-14: env pinleri birebir (numpy 2.4.4, pandas 3.0.2, sklearn 1.9.0); step8b drive_new Manavgat → arşivle bit-for-bit (0.8696419777927898).
- `repo/outputs` Manavgat parquet'i QC-varyantı çıktı (thermal 0.868963, downscaled_lst_mean 1841 NaN) — kanonik kıyaslar SADECE `drive_new/experiments/` ile.
- Envanterde olmayan Paper 1 bölümleri (LORO, feature-drop, scar kontrolleri, Muğla 2021↔2022) bizim tarafta koşuldu; Emrehan'dan istenmedi, bilerek.
