Konu: Makale taslağı tamam — son dört istek (ikisi tek satırlık)

Merhaba Emrehan,

Uzun bir turun sonundayız: makale taslak olarak **bitti**. Sekiz şekil, bütün tablolar,
bütün atıf kararları kapalı; gövde metninde tek bir açık `[PENDING]` kalmadı. Bundan
sonrası derleme turu ve gönderim. Bu yüzden bu, senden bir şey isteyeceğim son mail
olacak — ve listenin çoğu zaten "onayla, geç" cinsinden.

Önce ne yaptığımızı özetleyeyim, çünkü senin ürettiğin çıktılarla ilgili ve bilmen gerek.

---

## 1. ERA5-Land tanılaman makaleye girdi (§3.17, §4.9, §5.7)

Ham dosyaları aldım, hash'ledim, `manifest.json`'daki sha256'larla üçü de tuttu.
**Validator'ı kendim koşturdum: 27/27 PASS, 0 fail, 0 skip, exit 0** — senin aldığın
sonucun aynısı. Ortam: Python 3.12.3, `earthengine-api` 1.7.39 (sadece import zinciri
için; GEE oturumu açılmadı). Bu artık Methods'ta iddia değil, koşulmuş bir kontrol
olarak yazılı.

**Bir karar aldık: standardize anomalileri (z-skorlarını) makaleden tamamen çıkardık.**
Sebep, iklimatolojik sd'lerin bölgeler arası çok heterojen olması — predictor
penceresinde 2,7–6,0 kat, label penceresinde 11,5 kata kadar. Yani aynı z farklı
bölgelerde farklı fiziksel sapma demek ve bölgeler arası kıyaslanamaz. Makale artık
yalnız fiziksel birimde anomali raporluyor (°C, %, m/s, mm).

Bunun en net örneği senin verinde duruyor: Bejís label sıcaklığının dört referans yılı
19,643 / 19,953 / 19,942 / 19,909 °C — üçte bir derecelik aralıkta, sd 0,147 °C. Fiziksel
anomali sadece +0,83 °C ama z +5,66 çıkıyor. Karşılaştırma olarak Evia'nın label penceresi
aynı gün kapanıyor, 12 gün daha uzun, benzer +0,67 °C anomali — ama sd'si 0,351 olduğu için
z sadece +1,91. Payda farkı, sinyal farkı değil.

Tanılamanın kendisi çok temiz kurulmuş bu arada: dört realizasyonun JSON'da saklanması
(A20) sayesinde bunu doğrudan gösterebildik. Alan-ağırlıklı ortalamanın `ee.Reducer.mean()`
olmadığını kodda ayrıca belirtmen de metne girdi.

**Bilimsel sonuç, dürüst haliyle:** Manavgat'ın transferdeki aykırılığını meteorolojik
ekstremlikle açıklamayı öngörmüştük, **desteklenmedi**. Manavgat predictor penceresinde
iklimatolojik ortalamanın 0,06 °C *altında* — beşin tek negatifi, diğerleri +0,31 ile
+1,11 arası. Bunu başarısız bir öngörü olarak yazdık, rejim ön-kaydının düşmesiyle aynı
statüde.

## 2. Muğla iki-olay bloğu girdi (§3.16.4, §4.8, §5.2)

Yanık desen karşılaştırman ve step9g reversal tablon makalenin en güçlü argümanlarından
birini kurdu. Şimdiye kadar concept shift'i hep **farklı yerler** arasında gösteriyorduk
ve şu itiraz mümkündü: "farklı manzaralar, ilişki tabii ki değişir." Aynı AOI, aynı ızgara,
iki olay — ve elevation bootstrap-destekli tersiniyor (0,611 `[0,532–0,690]` → 0,296
`[0,230–0,355]`, CI'ler ayrık). İtiraz kalktı.

Mekanizma da görünür: 2021 dağınık bir kompleks, deniz seviyesinden 1975 m'ye; 2022 tek
kompakt yara, 777 m'nin altında, medyan 187 m'ye karşı 563 m. İki yangın aynı yükseklik
gradyanının farklı bölümlerinde yanmış.

Dürüstlük notu: **yalnız elevation destekli.** Dört termal kanalın reversal'ı nokta
düzeyinde — AUC *farkları* CI-destekli ama 2022 AUC'lerinin kendi CI'leri 0,5'i kesiyor
(331 pozitif). Metinde bunu açıkça yazdık, destekli gibi sunmadık.

---

## Senden istediklerim — dört madde

### 1) `reproduction_check.json`, beş bölge için (TEK GERÇEK BLOKAJ)

`03_methods.md`'de kalan **tek** `[TO VERIFY]` bu. §3.13 hâlâ iki bölgelik tarihsel
rakamları alıntılıyor (within-region ≤1×10⁻⁴, CORAL transfer ±0,002) ve metin "bu, tüm
bölgeler dahil olunca yeniden kurulmalı" diyor.

`drive_new`'ın hiçbir yerinde beş bölgelik bir `reproduction_check.json` yok. Bunu senin
üretmen gerekiyor, çünkü anlamı **senin donmuş çıktılarının bağımsız olarak yeniden
koşulup karşılaştırılması** — ben koşarsam kendi çıktımı kendimle karşılaştırmış olurum,
o da reprodüksiyon kanıtı değil.

İhtiyacım olan tek şey: beş bölge için within-region AUC'lerin ve CORAL transfer
skorlarının **ulaşılan tolerans** rakamları. Bir cümlelik özet bile yeter, JSON'u da
gönderirsen ideal.

### 2) İki Muğla transfer kolunu kendi ortamında koş (ÖNEMLİ AMA KISA)

`mugla_2021 ↔ mugla_2022_event_relative` transfer kolları hiç koşulmamıştı —
`drive_new/cross_region/` altında böyle bir çift yok ve step9f iki yönde de
`available: false`. Makalenin bu sayılara ihtiyacı vardı, ben de **senin step9b/step9c
kodunu değiştirmeden** koştum (48b56e7, seed 42, gölge PROJECT_ROOT kullandım, `repo/`'ya
ve Drive'a hiçbir şey yazılmadı).

Sonuç, birincil popülasyon, hedef ROC-AUC:

| Yön | baseline | thermal | ΔAUC |
|---|---|---|---|
| Muğla 2021 → 2022 | 0,642 `[0,606–0,674]` | 0,559 `[0,513–0,604]` | **−0,082** `[−0,127, −0,040]` |
| Muğla 2022 → 2021 | 0,581 `[0,566–0,598]` | 0,670 `[0,654–0,685]` | **+0,089** `[+0,072, +0,104]` |

İki bulgu: coğrafya sabitlenince transfer çökmüyor (iki yön de şans üstünde, oysa bölgeler
arası 20 yönün 6'sı altındaydı), **ama termal bloğun katkısı işaret değiştiriyor ve iki
işaret de CI-destekli** — üstelik blok her iki olayın içinde ayrı ayrı faydalıyken (+0,116
ve +0,078). Yani bir dinamik-durum bloğunun transferde yardım mı zarar mı vereceği bloğun
değil, çiftin özelliği. Makalenin tezinin en keskin hali bu oldu.

Ortamım: Python 3.12.3, scikit-learn **1.9.0**, pandas 3.0.5, numpy 2.5.2. Girdi hash'leri
(senin donmuş step8a parquet'lerin):

```
c4ab107db2207f9f20775ccc0b3bf39381173fd07d4e82f6821ce7f40be7db8e  mugla_2021
7c545f4da8fa7f8973575400862595d6ef85a8d55b9b25bc16fc54aba23a1d52  mugla_2022_event_relative
```

**İsteğim:** aynı iki kolu kendi ortamında koş ve sayıları bana gönder. Şu an Methods'ta
"bu iki yön, makaledeki diğer 20 yönden farklı olarak pipeline yazarı tarafından değil,
makale yazarları tarafından üretildi" diye yazıyor. Senin koşumun tutarsa bu cümleyi
"bağımsız olarak reprodüksiyonu yapıldı"ya çevirebiliriz — hakem karşısında ciddi fark
eder. Tutmazsa da bilmemiz şart.

### 3) Kendi Methods anlatın (BEKLEYEN, ACELE DEĞİL)

Sen pipeline'ı kendi cümlelerinle anlatacaktın, ben de §3.1–3.16 ile karşılaştıracaktım.
On aday tutarsızlık noktasını `03_methods.md`'nin sonundaki not bloğuna önceden listeledim.
Hazır olduğunda gönder yeter.

### 4) Few-shot: ek materyale girecek mi? (TEK SATIRLIK CEVAP)

§5.5'te "supervised few-shot recalibration analizi ek materyalde" diye bir işaretçi var ama
few-shot `04_results.md`'de hiç geçmiyor. İki seçenek: (a) girecek diyorsan cümle kalır ve
eğrini ek materyale koyarız (elindeki: 3 bölge, 6 yön), (b) girmeyecekse cümleyi silerim.
Sen söyle, ben hallederim.

---

## Bir de bilgi olsun diye: manifest'teki commit'i biz çözdük, sormuyorum

ERA5 `manifest.json`'ı `git_commit: a07ea33` kaydediyor ama o commit'te ne tanılama kaynağı
ne de `montiferru_2021` registry kaydı var — ikisi de 48b56e7'de eklenmiş. Yani koşuyu
commit'lenmemiş bir çalışma ağacından yapmışsın.

Bunu şöyle çözdük, kanıtla: çıktı Montiferru'yu registry pencereleriyle taşıyor, ki a07ea33
bunu veremez; `core/regions.py` a07ea33→48b56e7 arasında **saf ekleme** (529 satır eklenmiş,
hiç silinmemiş) ve ortak dört bölgenin kaydı bit-aynı; `core/paths.py` ile `core/config.py`
hiç değişmemiş; validator'ın A14'ü de beş bölgenin pencerelerinin 48b56e7 registry'siyle
uyuştuğunu doğruluyor. Dolayısıyla koşan kod 48b56e7'nin içeriğiydi.

Methods'a böyle yazdım. **Yanlış bir yeri varsa söyle**, yoksa bir şey yapmana gerek yok.

Ayrıca deponu artık makale deposuna **submodule olarak bağladık**, `48b56e7`'e sabitli —
Methods satır numarası verdiği için commit'in sabitlenmesi provenance'ın parçası oldu.

---

Özetle: (1) blokaj, (2) önemli ama kısa, (3) ve (4) hazır olduğunda. Bunlar gelince makale
gönderime hazır.

Emeğine gerçekten sağlık — pipeline'ın hem temiz hem denetlenebilir çıktı, validator ve
hash'li manifest'ler olmasa bu turun yarısını yapamazdık.

Sevgiler,
Yunus Emre
