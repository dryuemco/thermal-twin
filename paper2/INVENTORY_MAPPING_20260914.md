# Paper 2 Methods ↔ Methods Inventory eşlemesi (2026-09-14)

Kaynaklar: `paper2/03_methods.md` (mevcut iskelet, 3.1–3.4), `paper2/04_results.md` (eksen
içerikleri), `paper/methods_inventory_20260911.txt` (Emrehan'ın envanteri, bölüm 2.1–2.9),
`paper/03_methods.md` (Paper 1'de kalan anlatım — mükerrerlik ölçütü).

**Okuma anahtarı.** Paper 2'nin Methods'u kasıtlı olarak incedir: §3.1 kohortu Paper 1'e havale
eder ("described there in full"), §3.3 sekiz ekseni birer paragrafla tanımlar. Bu yüzden eşleme iki
katmanlıdır: (i) her eksenin **vardığı kanonik zincir** — bunu envanter besler; (ii) her eksenin
**müdahale/ölçüm protokolü** — bu Paper 2'ye özgüdür ve envanterde çoğunlukla yoktur. "Doluluk"
sütunu yalnız (i) içindir; (ii) eksikleri Bölüm C'deki gap listesindedir. Paper 1
`03_methods.md` §3.1–§3.7'de zaten anlatılan kohort/pipeline ayrıntıları gap sayılmadı.

---

## A. Eşleme tablosu

| Paper 2 Methods slotu | Envanter alt bölümü | Doluluk (kanonik zincir) | Not |
|---|---|---|---|
| §3.1 Kohort ve sabit tutulanlar | 2.1.1–2.1.2 (AOI + pencereler, bbox), 2.2.1–2.2.5 (veri kaynakları), 2.3.7–2.3.8 (popülasyonlar, valid_for_modeling), 2.5.4–2.5.8 (feature setleri, RF), 2.5.8/2.6 (spatial CV, bootstrap 1000), 2.7.14 (imputasyon) | **Tam** | Paper 1 §3.1–§3.7 ile mükerrer; Paper 2'de tek paragraf yeterli. Envanter tutarlılığı doğruluyor. |
| §3.2 Eksen nasıl değiştirilir (protokol) | — (2.8.9–2.8.10 frozen-config/bütünlük kontrolleri dolaylı destek) | **Boş** | "Reproduce before you vary", staging/provenance repointing, primitives-import yöntemi Paper 2'ye özgü; envanterin kapsamı dışında. |
| §3.3 Eksen 1: Hücre geometrisi | 2.3.1 (17×30 m = "510 m"), 2.3.2 (native-grid rekonstrüksiyonu), 2.2.6(a,b) (EPSG:4326, ~30 m açısal operasyonel ölçek), 2.1.2 (bbox'lar) | **Kısmi** | Kanonik grid tanımı tam; ama derece-adımı türetimi, yer-mesafesi hesabı (390–407 m D-B), hücre-sayısı reprodüksiyonu envanterde yok. 2.2.6(b) anizotropiyi ima ediyor, 2.3.1 etmiyor (bkz. D.1). |
| §3.3 Eksen 2: Kaba-termal QC taraması | 2.2.2(d) (QC_Day bit kuralı, count≥3, −9999), 2.4.5(e) (MOD11A1 ürün/band/ölçekleme) | **Kısmi** | Kuralın kendisi tam tanımlı. Beş-bölge tarihsel uygulaması envanterde **çözülmemiş** ([PARTIALLY VERIFIED]); Paper 2 §4.2 bunu kendi kanıtıyla (export tarihi 2026-07-23) çözüyor — kanıt yükü Paper 2'de (bkz. D.2). Yeniden-hesaplama ve downstream propagasyon protokolü envanterde yok. |
| §3.3 Eksen 3: Nodata konvansiyonu | 2.2.2(d) tek cümle ("Current export no data −9999; count threshold verified only for later frozen exports") | **Boşa yakın** | Sıfır-dolgu forensiği (exact-0.0 sayımı, %5 şüpheli-sıfır muhafızı, su-baskın hücre payı eşleştirmesi) tümüyle Paper 2 malzemesi. |
| §3.3 Eksen 4: Kompozit zinciri | 2.4.1(f) (scene_weighted kanonik / date_balanced duyarlılık), 2.4.3(k) (seam/coverage teşhisi), 2.9.6 (seam_audit artefaktları), 2.2.6(f) (median kompozit) | **Kısmi** | İki zincirin varlığı ve kanoniklik tam. Sınır-tipolojisi (same-day multiplicity vs unique-date-count kenarları), eşli bootstrap, dört bölgeye genişletme, WRS satır-sayısı kuralı envanterde yok. |
| §3.3 Eksen 5: İndeks normalizasyonu (TVDI) | 2.4.2 (b–i: girdiler, 20 bin, 2./98. persantil kenarlar, min 30 piksel/bin, min kenar aralığı 1.0 °C, formül; l–s: baseline TVDI, fark, z-score) | **Kısmi (kanonik tam)** | Kanonik TVDI en iyi belgelenmiş bölüm — Methods'un "canonical arm" paragrafı buradan yazılır. Kara-piksel yeniden-fit'i ve beş-bölge havuzlanmış kenar fit'i (müdahaleler) envanterde yok. |
| §3.3 Eksen 6: Etiket kalitesi | 2.2.3 (MCD64A1, DOY, pencere), 2.3.3 (mode BurnDate), 2.3.4 (ikili kural), 2.3.5 (pre-label dışlama), 2.8.4 (FIRMS hedef değil) | **Kısmi** | Kanonik etiket zinciri tam. Üç probun protokolü (agreement-eşiği 0.75/0.90, FIRMS ile yeniden-etiketleme, kırpılmamış ürünle pre-label maruziyet ölçümü) envanterde yok; agreement-fraction değişkeninin tanımı da yok. |
| §3.3 Eksen 7: Türetilmiş kanallar ve tasarım seçimleri | 2.4.5(d,i) (downscaling feature'larında lon/lat/row/col — koordinat-taşıyan kanalların mekanizması), 2.4.6 (füzyon kuralı, source_mask), 2.3.7 (all_valid vs TSG), 2.9.10 (gap-fill duyarlılığı), 2.6.12–2.6.17 (büyük-blok) | **Kısmi** | Mekanizmalar (koordinatın downscaled/fused'a nasıl girdiği, gap-fill'in ne olduğu) envanterden yazılır. Koordinat-kanalı düşürme deneyi, boyut/pozitif eşleştirme (10 katmanlı çekiliş), 5 km transfer yeniden-bloklama envanterde yok. 2.9.10'un popülasyonu all_valid — Paper 2'nin birincil-popülasyon sonucuyla aynı artefakt değil (bkz. D.4). |
| §3.3 Eksen 8: Yazılım | 2.8.9 (frozen config), 2.8.10 (korumalı-artefakt bütünlüğü), 2.9.4 (CORAL λ duyarlılığı, λ seçimi yok) | **Boşa yakın** | Kütüphane-versiyon probları, farklı-OS ortam yeniden-kurulumu ve alan-alan karşılaştırma tümüyle Paper 2 malzemesi. 2.9.4 yalnız λ-sweep'in "seçim değil" statüsünü destekler. |
| §3.4 Raporlama konvansiyonları | 2.9.2 (işaretli univariate AUC, <0.5 = yön, asla katlanmaz; bootstrap-supported vs point-reversal), 2.6.7–2.6.10 (CI yorumu), 2.6.11–2.6.13 (blok boyutları, sonuca göre seçilmedi) | **Tam** | Paper 2 §3.4'ün her iki kuralı (katlamama; ayrık-CI desteği) envanterde birebir var. |

Özet: envanter **§3.1 ve §3.4'ü tam**, sekiz eksenin **kanonik tanım yarısını** doldurur;
**§3.2 ile eksenlerin müdahale/ölçüm yarısı** Paper 2'nin kendi analiz raporlarından
(`paper/` altındaki, örn. `modis_qc_downstream_propagation.md`) gelmek zorundadır.

---

## B. Envanterde işaretli olup Paper 2'yi etkileyen maddeler

Sıralama: etki büyüklüğüne göre.

1. **2.2.2(d)** — MOD11A1 QC kuralının beş-bölge tarihsel uygulaması: "Evia Extended + Montiferru
   frozen; Manavgat/Bejís/Muğla provenance unresolved" **[PARTIALLY VERIFIED]** (satır 165;
   "VERIFIED EXCEPT FIVE REGION", satır 170). Eksen 2'nin ve C3 katkısının tam merkezi. Paper 2
   bunu çözülmüş olarak sunuyor; kanıt (script değişiklik tarihi, export metadata karşılaştırması)
   Methods'ta Paper 2'nin kendi tespiti olarak, envantere yaslanmadan verilmeli.
2. **2.4.5(e)** — Aynı sorun downscaling girdisi tarafında: "temporal/product definition verified;
   historical QC provenance unresolved for three AOIs" **[PARTIALLY VERIFIED]** (satır 1137).
   Eksen 2'nin propagasyon kolunu (downscaling → füzyon) etkiler.
3. **2.2.6(c)** — Upstream Earth Engine export/reprojeksiyonlarında kullanılan enterpolasyon
   çekirdeği **[UNRESOLVED]** (satır 444; "MOSTLY VERIFIED"). Eksen 1'in (grid geometrisi) ve
   Eksen 4'ün (seam) "export nasıl üretildi" cümlelerini sınırlar; Methods'ta kapsam kaydıyla
   ("pipeline-içi hizalama bilinear/nearest; EE-içi kernel çözülmemiş") verilmeli.
4. **2.2.6(a)** — Ortak CRS iddiası "VERIFIED WITH SCOPE LIMIT" (satır 414): EPSG:4326 frozen
   çıktılar için doğru, her kaynak verinin native depolaması için genellenemez. Eksen 1'in
   açısal-adım türetimi tam bu kapsama yaslanıyor; cümle aynı kayıtla kurulmalı.
5. **2.2.3(d,e)** — BurnDate yorum kuralı ve ~510 m gride aktarım "PARTIALLY COMPLETED" +
   açık **Missing** bloğu (satır 238–243: exact grid yöntemi, piksel→hücre agregasyonu, cell-ID
   eşleşmesi, agregasyon istatistiği). İçerik büyük ölçüde 2.3.1–2.3.3'te kapanıyor; Methods bu
   maddeler için 2.2.3'e değil 2.3'e atıf yapmalı. Eksen 1 ve 6'yı ilgilendirir.
6. **2.2.5** — DEM: dikey datum çözülmemiş ("VERIFIED EXCEPT – Vertical datum", satır 365; 1076'da
   tekrar) ve DEM ön işleme "PARTIALLY COMPLETED" + **Missing** bloğu (satır 386–393: orijinal
   çözünürlük, yeniden örnekleme yöntemi, hücre-içi agregasyon). Eksen 2'nin ana bulgusu
   (QC kaymasının **yükseklikle** +0.615 korelasyonu) elevation rasterine dayandığı için, DEM'in
   hangi agregasyonla hücreye indiği Methods'ta söylenemiyorsa bu bir sınırlılık notu ister.
7. **2.4.4(g)** — Topografik değişkenlerin 30 m→510 m aktarımı "Status: VERIFY FROM CODE"
   (satır 1066). 6. maddeyle aynı boşluğun ikinci ucu.
8. **2.8.12 / satır 2046** — "Tüm AOI'ların performans görülmeden dondurulduğu iddiası
   doğrulanamıyor" **[PARTIALLY VERIFIED]**. Paper 2 §3.1'in "held fixed" çerçevesini doğrudan
   yıkmaz (Paper 2 kohortu miras alır), ama POSITIONING'in "holding data fixed" dili bu kayıtla
   uyumlu kurulmalı; Evia/Montiferru için pozitif kanıt var (2.1.3), Bejís/Muğla için yok.
9. **2.1.3** — Bejís AOI kenar-seçim gerekçesi **[PARTIALLY VERIFIED – unresolved]** (satır 74);
   Muğla freeze-tarihi doğrulanamıyor (satır 75). §3.1'i yalnız dolaylı etkiler (Paper 1'e havale).
10. **2.2.6(e)** — Baseline vs current pencere yapısı "PARTIALLY COMPLETED" (satır 457). Eksen 4
    ve 5'in baseline tanımlarını besleyen bölüm; baseline yılları 2.1.1 tablosundan alınmalı.
11. **2.6.14** — Büyük bloklarda nelerin yeniden kurulduğu "PARTIALLY COMPLETED" (satır 1644).
    Eksen 7'nin "blocking scale" maddesinin within tarafını etkiler.
12. **2.7.14** — Medyan imputasyon "PARTIALLY COMPLETED" (satır 1821). §3.1 "held fixed"
    listesinde imputasyon anılacaksa ayrıntısı Paper 1'den/koddan doğrulanmalı.

Etkilemeyen işaretli maddeler (kayıt için): **2.9.3(a)** predictor-window replay eşikleri
[UNRESOLVED] (satır 2164) — pencere kayması Paper 2'nin sekiz ekseninden biri değil.

---

## C. Gap listesi — envanterde olmayan, Paper 2 Methods'un muhtemelen isteyeceği konular

(Paper 1 §3.1–§3.7'de anlatılanlar mükerrerlik sayılıp listelenmedi. Aşağıdakiler Paper 2'ye
özgü müdahale/ölçüm protokolleridir; kaynakları `paper/` altındaki analiz raporları olmalı.)

**Genel (§3.2):**
- G1. "Reproduce before you vary" kabul kriterleri: bir kolun frozen karşılığını "tuttu" sayma
  eşiği (kaç alan, hangi tolerans), tutmayınca karşılaştırmanın düşürülmesi kuralı.
- G2. Staging/provenance-repointing yöntemi: girdiler başka konuma taşınırken pointer'ların
  nasıl güncellendiği ve bunun kaydı.
- G3. "Pipeline'ın kendi primitifleri import edilerek sürüldü" iddiasının somutlanması: hangi
  modüller/fonksiyonlar, hangi eksende.

**Eksen 1:** G4. Derece-adımı türetimi (30/111319.49 = 0.00026949°; ×17), enlem-bağımlı D-B
kenar hesabı, AOI açıklığı/adım + dışa yuvarlama ile beş frozen hücre sayısının reprodüksiyonu.

**Eksen 2:** G5. QC'li/QC'siz pencere-ortalaması yeniden-hesaplama protokolü (hangi kod, hangi
girdi arşivi) ve kayma−elevation korelasyonunun tanımı (piksel mi hücre mi, hangi korelasyon).
G6. Downstream propagasyon deseni: iki kolun da yeniden kurulması (rebuild-drift'ten izolasyon),
karşılaştırılan alanlar. G7. Export-tarihi kanıtı (script değişikliği 2026-07-23, metadata farkı).

**Eksen 3:** G8. Exact-0.0 sayım yöntemi, %5 şüpheli-sıfır muhafızının pipeline'daki yeri
(envanterde adı geçmiyor), su-baskın hücre payının hesabı ve eşleştirme mantığı.

**Eksen 4:** G9. Sahne envanteri sayımı (WRS path/row, sahne/tarih oranı, same-day kenar sayısı).
G10. Sınır-tipolojisi tanımları ve eşli bootstrap'ın kurulumu; "supported reduction / uncertain /
no effect" karar kuralı. G11. Downstream ROC-AUC kıyasının hangi koşulda kabul edildiği
(yalnız Manavgat; diğerlerinde reddin gerekçesi).

**Eksen 5:** G12. Kara-piksel maskesiyle kenar yeniden-fit protokolü (su maskesi neyden türedi).
G13. Beş-bölge havuzlanmış kenar fit'i (26.2 M piksel): havuzlama, bin desteği, yeniden hesap ve
hücre agregasyonu. G14. İşaretli birlikteliğin 10-hücre spatial-block bootstrap'ı bu bağlamda.

**Eksen 6:** G15. `burn_date_pixel_agreement_fraction` değişkeninin tanımı (envanterde hiç yok)
ve 0.75/0.90 eşik probu. G16. FIRMS aktif-ateş gözlemiyle omisyon probu: eşleştirme kuralı,
kasıtlı aşırı-düzeltme (hepsini burned yapma) tasarımı, FIRMS'in ürün-bağımsızlık gerekçesi.
G17. Kırpılmamış MCD64A1 ile pre-label maruziyet ölçümü (arşivden neden ölçülemediği dahil).
G18. "İkinci burned-area ürünü 2020'de bitiyor" sınırlılığının ürün adıyla belgelenmesi.

**Eksen 7:** G19. Koordinat-kanalı düşürme deneyi (thermal setten downscaled/fused çıkarımı) ve
"increment'in %82–103'ü korunur" hesabı. G20. all_valid popülasyonunun deniz içeriğinin sayımı.
G21. Boyut/pozitif eşleştirme: 10 katmanlı çekilişin katmanlama değişkeni ve medyan raporlama.
G22. Transfer aralıklarının 5 km yeniden-bloklaması (verdict sayım kuralı dahil).

**Eksen 8:** G23. Kütüphane-versiyon probları: hangi versiyon çiftleri, hangi frozen problar.
G24. Farklı-OS ortam yeniden-kurulumu: pin kaynağı, alan-alan karşılaştırmanın kapsamı
(142/168 alan), maksimum fark raporlama biçimi. G25. Sweep'in atladığı regularizasyon sabitinin
hangisi olduğu ve doğrudan yeniden-hesap yöntemi (envanter 2.9.4 grid'i λ=1e-5'i **içeriyor**;
Paper 2 §4.7'nin "omits" dediği sabit netleştirilmeli — bkz. D.5).

---

## D. Çelişkiler / gerilimler (envanter ↔ paper2 mevcut metni)

1. **Hücre boyutu dili.** Envanter 2.3.1: "17×30 = 510 m" — hücreyi izotropik ~510 m gibi kurar;
   2.2.6(b) ise 30 m'nin "sabit açısal adım, her enlemde aynı metrik genişlik değil" olduğunu
   söyler. Paper 2 §4.1/C4'ün ana bulgusu tam bu izotropi varsayımının yanlışlığı (510 × 390–407 m).
   Çelişki envanterin iki alt bölümü arasında ve 2.3.1 ile Paper 2 arasında: Methods kanonik grid'i
   anlatırken 2.3.1'in "510 m" dilini **aynen almamalı**; "nominal ~500/510 m, gerçek geometri
   §4.1'de" diye kurmalı.
2. **QC provenansının epistemik statüsü.** Envanter (2.2.2d, 2.4.5e): üç AOI için **çözülmemiş**.
   Paper 2 (§4.2, abstract, POSITIONING C3): **çözülmüş** — split export tarihiyle, kural
   2026-07-23'te eklendi. İçerik çelişkisi değil, kanıt-yükü çelişkisi: envanter 2026-09-11
   tarihli ve Paper 2'nin tespitini yansıtmıyor. Ya envanter güncellenmeli ya Paper 2 Methods bu
   tespitin kanıtını kendi içinde taşımalı; ikisi yan yana yayınlanırsa hakem tutarsızlık görür.
3. **Füzyon geçerlilik aralığı.** Envanter 2.4.1(d): Step5 fiziksel maske **−30 < LST < 80**;
   2.4.6(c): füzyon kabulü **−20 ≤ LST ≤ 80**. Envanter-içi bir tutarsızlık/aşama farkı; Paper 2
   Methods füzyonu anlatırken tek bir aralık verecekse aşamaya göre doğrusunu seçmeli.
4. **Gap-fill duyarlılığının popülasyonu.** Envanter 2.9.10: frozen gap-fill analizi **all_valid**
   üzerinde ("primary TSG/TS üzerinde mevcut değil"). Paper 2 §4.6 gap-fill kısıtının "beş bölgede
   de increment'i bootstrap-destekli bıraktığını" birincil sonuç diliyle veriyor. Paper 2 kendi
   TSG-popülasyonlu koşusunu yaptıysa sorun yok ama Methods bunu **frozen artefakttan ayrı, yeni
   bir koşu** olarak açıkça işaretlemeli; aksi halde envanterle çelişir.
5. **CORAL λ sweep'i.** Envanter 2.9.4: sensitivity grid'i [0, 1e-8 … 1e-1], kanonik λ=1e-5
   (metindeki "λ=105" bariz dizgi hatası) ve grid 1e-5'i içeriyor. Paper 2 §4.7: "a regularisation
   constant that the released sensitivity sweep **omits** was also recomputed". Hangi sabitin
   atlandığı iki metinden tutarlı okunmuyor; Methods'ta netleştirilmeli.
6. **Küçük sayı tutarsızlığı (paper2-içi, kayıt için).** §4.4 su-baskın pay "%57.6", §4.6 aynı
   nicelik "%57.7". Envanterle ilgisiz ama aynı düzeltme turunda kapatılmalı.

---

## E. Kullanım önerisi (tek paragraf)

Paper 2 Methods'un mevcut iskeleti korunmalı; envanter §3.1 ve §3.4'ü olduğu gibi, sekiz eksenin
"kanonik kol" cümlelerini de büyük ölçüde doldurur (en güçlüsü Eksen 5/TVDI: 2.4.2 neredeyse
yayına hazır). Eksenlerin müdahale/ölçüm protokolleri (C listesi) envanterden gelemez; bunların
kaynağı `paper/` altındaki analiz raporlarıdır ve Methods'a G1–G3 (genel protokol) ile G5–G7,
G15–G17 (en çok taşıyan iki eksen: 2 ve 6) öncelikli yazılmalıdır. B listesindeki 1–4. maddeler
yayın öncesi ya envanter tarafında kapatılmalı ya Methods'ta açık kapsam kaydıyla taşınmalıdır.
