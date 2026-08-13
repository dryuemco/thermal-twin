Konu: 9 madde — ikisi hatırlatma, biri CORAL λ=1, altısı ikinci hakem turundan

Merhaba Emrehan,

İç hakem turunu yaptık: makaleyi bir dış hakemin sorabileceği sorularla baştan taradık. Çıkan
dört maddeyi topluca yazıyorum. İlk ikisi 13 Ağustos'ta yazdığım maddelerin aynısı (acele yok,
sadece hâlâ açık olduklarını teyit ediyorum), üçüncüsü yeni, dördüncüsü geçen sefer yazmayı
unuttuğum soru.

---

**1. Reproduction check'in kodu hâlâ depoda yok.** (mail 4, madde 1'in tekrarı)
Bugün tekrar baktım: `48b56e7`'de `*reproduction*` araması hiçbir şey döndürmüyor.
`scripts/run_reproduction_check.py` ve `src/reproduction_validation/` yok. Makalenin §3.13'ü
tamamen `reproduction_check.json`'a dayanıyor ve biz depoyu "authoritative source" ilan ediyoruz;
yani hakem şu an bu kontrolü **yeniden üretemez**. Bu, reprodüksiyon iddiamızın en zayıf noktası.
**Commit'leyip push'lar mısın, hash'i de yazar mısın?**

**2. Few-shot commit'i `19d825b` hâlâ çekilemiyor.** (mail 4, madde 2'nin tekrarı)
Tam clone'da 92 commit var, bu commit içlerinde yok (`git cat-file -t 19d825b` → *not a valid
object name*). Supplementary S1'in provenance satırı okuyucunun ulaşamayacağı bir şeyi
gösteriyor. İki seçenek, hangisi kolaysa:
- o commit'i push/tag et, **veya**
- tek satır teyit: *"`src/few_shot_recovery.py`, `19d825b` ile `48b56e7` arasında değişmedi."*
  (Dosya `48b56e7`'de mevcut, o yüzden ikinci seçenek muhtemelen yeterli.)

**3. (Yeni, isteğe bağlı ama faydalı) CORAL λ = 1 kolu — beş bölgelik sette.**
Donmuş `coral_lambda_sensitivity` çıktısını okudum: grid **0, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3,
1e-2, 1e-1** (9 değer), **4 yön** (Bejís↔Muğla 2021, Manavgat↔Muğla 2021), 2 model ailesi.
Yani **λ = 1 hiç koşulmamış**. Hakem tam olarak bunu soracak, çünkü 1 kanonik CORAL değeri.

Bizim cevabımız hazır ve savunulabilir: kanonik λ=1, **standardize edilmemiş** feature'lar için
tanımlı; biz CORAL'ı region-wise z-score'dan **sonra** uyguladığımız için her feature'ın varyansı
zaten 1, dolayısıyla λ=1 köşegeni ikiye katlayıp hizalamanın taşımaya çalıştığı kovaryans yapısını
büyük ölçüde siliyor. Bunu Methods §3.11'e gerekçesiyle yazdım. Elimizdeki tek λ=1 kanıtı **eski
iki bölgelik** analizden geliyor (Manavgat–Bejís; λ ∈ {1e-5, 1e-3, 1e-1, 1}) ve orada tek
şansüstü yön λ=1'de şansa düşüyordu — yani beklediğimiz davranış. Ama o analiz artık geçersiz
(beş bölgelik sete taşınmadı) ve makalede öyle yazıyor.

**Sana masrafı azsa:** mevcut sensitivity diagnostic'inin grid'ine sadece `1.0` eklemek
(aynı 4 yön × 2 aile = 8 ek fit) bu itirazı tamamen kapatır. Zorunlu değil; koşmazsan da
gerekçeyi yazdığımız gibi bırakırız. **Koşarsan hiçbir sonucu değiştirmeyeceğini bekliyorum,
ama "koşmadık" demek zorunda kalmamak daha iyi.**

**4. ERA5-Land manifest commit uyuşmazlığı** (geçen mailde yazmayı unuttum, kusura bakma).
`manifest.git_commit` = `a07ea33`, ama diagnostic'in kaynağı (`src/era5_land_regional_diagnostic.py`)
ve Montiferru registry kaydı o commit'te **yok**; ikisi de ilk kez `48b56e7`'de görünüyor. Yani
üretim koşusu commit'lenmemiş bir working tree'den yapılmış. Contract'taki bütün semantik string'ler
`48b56e7` ile birebir aynı ve validator 27/27 PASS veriyor, o yüzden çıktının anlattığımız kodla
**tutarlı** olduğundan eminiz; ama bit-özdeşliği kurulmuş değil. Tek satırlık teyit yeter:
*"Koşu sırasındaki working tree, `48b56e7`'nin diagnostic + registry içeriğini taşıyordu."*
(Bu madde 1 ve 2 ile aynı sınıftan: yayınlanan depo ile üretim commit'i arasındaki boşluk.)

---

**Ek maddeler (14 Ağustos, ikinci iç hakem turundan).** Dört kişilik bir panel makaleyi baştan
okudu ve modelleme tarafını çok sağlam, **gözlem/veri-kökeni tarafını ince** buldu. Aşağıdakiler
hep senin donmuş çıktılarından çıktı, yani yeni bir analiz talebi değil; çoğu tek satırlık teyit.

**5. Manavgat'ın Step 7 MODIS girdisi diğer dört bölgeden farklı.** `step7c` metadata'sında
Manavgat için `"modis_lst_mean_celsius is a 4-year summer-mean MODIS context layer"` yazıyor;
Bejís, Muğla, Evia ve Montiferru'da ise `"single-season MODIS predictor-window summary layers"`.
Yani `downscaled_lst` ve `fused_lst` Manavgat'ta bir **klimatoloji**, ötekilerde **olaya özgü
kompozit** üzerinden kuruluyor. Manavgat aynı zamanda çapa bölge ve makalede "transfer davranışı
açıklanamıyor" dediğimiz bölge, bu yüzden bu fark birinci dereceden aday açıklama. **İki soru:**
(a) bu bilinçli bir tercih miydi, (b) Manavgat'ın Step 7'sini diğerleriyle aynı kontrat üzerinden
yeniden kurmak makul bir iş mi? Şu an makalede §3.4 ve §5.11(xiii)'te "test edilmemiş aday
açıklama" olarak yazılı. Aynı koşuda `modis_nodata_issue_resolved: False` de duruyor (deniz
hücreleri 0.0 °C olarak kodlanmış, kıyı AOI'sinde) — bu diğer bölgeleri de etkiliyor mu?

**6. Landsat kompozit A/B'si sadece Manavgat için var.** `landsat_composite_downstream_ab` ve
`landsat_harmonization_downstream_ab` çıktıları çok değerli: aynı kohort, aynı fold, aynı baseline
(0.804362, üçünde de bit-aynı), sadece current-LST rasterı değişiyor ve termal ΔAUC **+0.045 /
+0.064 / +0.085** çıkıyor. Bunu makaleye yeni bir duyarlılık ekseni olarak koydum (§4.7i) ve
"±0.02 kompozit toleransı, tek bölgede denetlenmiş" diye yazdım. Raporun kendisi de bir sonraki
adım olarak Bejís'i işaret ediyor. **Bejís için aynı A/B'yi koşman mümkün mü?** Mümkün değilse
sorun değil, tek bölgelik kalır ve öyle yazar.

**7. Bölge başına Landsat gözlem envanteri.** `landsat_current_support_harmonization` altındaki
`daily_inventory.json` sadece Manavgat'ta var (7 tarih, 14 sahne, iki alternatif path). Hakem
"kaç açık gözlem üzerinden medyan alındı" diye soracak ve şu an dört bölge için cevabımız yok.
**Diğer dört bölge için tarih/sahne sayısı ve piksel başına geçerli gözlem dağılımı elde var mı?**
Yoksa Earth Engine'de ucuz bir sorgu sanırım.

**8. Takvim-eşleşmiş Muğla 2022 kolu koşulabilir mi?** Bu, panelin tek anlaşmazlık konusu oldu.
İki hakem iki-olay kontrolünü makalenin en güçlü kanıtı saydı; biri ise mevsim confound'unun
elevation dönmesini **tek başına** üretebileceğini söyledi ve haklı: 2022 penceresi 24 Nisan–20
Haziran, 2021'inki 1 Haziran–28 Temmuz. Yani geç-ilkbahar ile yüksek-yaz kıyaslanıyor ve Batı
Toroslar'da yüksek kesim ilkbaharda zaten yanmaz. Registry'deki (geçersiz sayılan) `mugla_2022`
takvim-kaydırma kaydı tam da bunu veriyor gibi görünüyor. **O kolu koşabilirsek yıl ile mevsimi
ayırabiliriz** ve makalenin en cesur kontrolü en güvenli kontrolü olur. Şu an §5.2'de confound'u
açıkça yazıp iddiayı daralttım.

**9. İki küçük teyit.**
(a) `apply_qa_mask` metninde `QA_RADSAT` uygulandığı yazıyor ama kodda uygulanmıyor (sadece
`QA_PIXEL`). Hangisi doğru? (b) Bejís 2022 için Landsat 9 neden kullanılmadı — bilinçli miydi?
L9 o dönemde operasyoneldi ve açık gözlem sayısını kabaca ikiye katlardı. İkisi de makalede
şu an olduğu gibi (yani L8-only, QA_PIXEL-only) yazılı; sadece gerekçeyi bilmek istiyorum.

---

Özetle: 1, 2 ve 4 depo/provenance temizliği; 3 tamamen isteğe bağlı bir ek koşu; 5–9 ikinci
hakem turundan, çoğu tek satırlık teyit, sadece 6 ve 8 gerçek koşu gerektiriyor.
Methods envanterini hâlâ bekliyorum, acelesi yok.

Teşekkürler,

Yunus Emre
