Konu: Makale için sonuçlar üzerine — öncelikli istekler ve Evia kararı

Merhaba Emrehan,

Elindeki üç bölgenin sonuçlarıyla makalenin yönünü netleştirdik ve gidişat sağlam. Kısaca
söyleyeyim: makalenin ana tezi artık "termal kuruluk yangın öncesi durumu iyileştiriyor" değil —
o bulgu doğru ama tek başına yeni değil. Asıl tez şu oldu: **dinamik pre-fire termal blok, bölge
içinde en çok kazandıran feature seti ama bölgeler arasında en çok kaybettiren blok.** Yerel beceri
ile taşınabilirlik arasında bir ödünleşim var ve bunu ölçüyoruz. Aşağıdaki isteklerin çoğu bu
çerçeveyi desteklemek için.

Bir de güzel bir haber: işaretli univariate AUC'lere ~5 km mekansal-blok bootstrap aralıklarını
yeniden hesapladım (senin run_c'nin CI'larını ~0.01 içinde yeniden ürettim, yani tutuyor). İki
bölgede yalnız elevation tersiniyordu; Muğla girince **dört mutlak termal kanal da (current_lst,
current_tvdi, downscaled_lst, fused_lst) Manavgat–Muğla arasında ayrık CI'larla işaret değiştiriyor**
— yani "concept shift" mekanizması artık istatistiksel olarak kanıtlı.

Şimdi senden istediklerim, öncelik sırasıyla:

—— ÖNCE ÇÖZÜLMESİ GEREKENLER ——

1) TAM ARŞİVİ YENİDEN YÜKLE.
Bana ulaşan zip'ler 002, 006, 007, 008 parçalarıydı; 001, 003, 004, 005 EKSİK. Her zip bağımsız
bir alt küme olduğu için verinin kabaca yarısı gelmemiş. Kesin eksikler: Evia'nın step8b/step8e
raporu, Evia'nın gate kararı (burned_landcover_gate.json), ve Evia'nın step8a parquet'i. Tümünü
(ya da eksik parçaları) yeniden yükleyip başka bir şeyin kırpılmadığını teyit eder misin?

2) EVIA KARARI.
Evia'nın AOI'si çok küçük (0.40°×0.40°) ve yangın alanın büyük kısmını yakmış: yanmış oran doğal
vejetasyonda %67, diğer üç bölgede %3.8–7.2. Bu prevalansla Evia'nın AUC'leri diğerleriyle
kıyaslanabilir değil. Üç seçenek var, kararı sen ver ama bana söyle çünkü makale yapısı buna göre
dallanıyor:
   (a) AOI'yi belirgin şekilde büyütüp Step1'den yeniden koş (en güçlü sonuç, dört bölgelik matris);
   (b) Evia'yı transferden çıkar, sadece within-region tekrarı olarak tut (çalışır, gerekçesini
       yazarız);
   (c) yeniden koşup farklı bir yangın rejimi gibi davranırsa ikinci kontrol olarak kullanırız.

—— TEZİ SAĞLAMLAŞTIRANLAR ——

3) MARJİNAL AoA İNDEKSİ (her sıralı bölge çifti için).
Makalede artık şunu basılı olarak iddia ediyoruz: prediktör-uzayı mesafesine dayalı marjinal
teşhisler transfer sonuçlarını sıralayamıyor, ama koşullu teşhis (işaret tersinmesi) sıralıyor.
Koşullu yarı bende var; marjinal yarıyı hesaplamadık. Her çift için şunları üretebilir misin:
Meyer & Pebesma tarzı, önem-ağırlıklı prediktör-uzayı benzemezlik indeksi (RF'in zaten önemleri
veriyor), artı basit bir iklimsel mesafe ve coğrafi (centroid) mesafe. Bunlar üretilmezse ilgili
iki cümleyi yumuşatmak zorunda kalırız, o yüzden bu da bir bakıma bloke edici.

4) PENCERE-KAPANMA DUYARLILIĞI.
Her bölgede prediktör penceresi etiket penceresinden bir gün önce kapanıyor. Hakem "son günlerde
duman/erken ısı termal kompozite sızmış olabilir mi?" diye soracaktır. Termal prediktörleri her
bölgenin prediktör penceresinin SON 7 ve 14 GÜNÜ çıkarılmış olarak yeniden kompozitleyip
within-region ΔAUC'nin hâlâ ayakta kaldığını gösterir misin? Ucuz bir kontrol ama bariz bir itirazı
peşinen kapatıyor.

5) EVIA İÇİN İŞARETLİ-AUC BOOTSTRAP.
Evia'nın parquet'i gelince üç-bölgelik tabloyu ben genişletebilirim, ya da sen Evia için run_c'yi
koşarsın. İkisi de olur.

—— NEGATİF BULGUYU YAPICIYA ÇEVİRENLER ——

6) FEW-SHOT KURTARMA EĞRİSİ.
Kalan açık concept shift olduğu ve etiketsiz hizalama bunu kapatamadığı (dahası çalışan çifti
BOZDUĞU) için mantıklı bir sonraki adım: transfer edilen modeli hedef bölgeden küçük, mekansal-bloklu
bir etiketli örneklemle yeniden kalibre et, ve "within-region tavanının %X'ini geri kazanmak için
kaç etiketli hücre gerekiyor" eğrisini çiz. Bu muhtemelen makalenin son figürü olur.

7) DEKOMPOZİSYON — NEGATİF KURTARMA KONVANSİYONU.
Muğla girince çalışan çiftte (Bejís↔Muğla) `kurtarılan = adapte − ham` NEGATİF çıkıyor, çünkü
adaptasyon orada zarar veriyor. Eski %27–31/%69–73 rakamı iki-bölgeliydi ve adaptasyonun hep
yardım ettiğini varsayıyordu. Bütün yönler için yeniden hesaplayıp `adapte < ham` durumu için açık
bir konvansiyon belirleyelim (benim önerim: bölümü "şansa doğru sıkışma" gözlemi etrafında yeniden
kurmak).

8) MUĞLA'NIN ÖZEL ROLÜNÜ AYRIŞTIR.
Muğla hem tek başarılı transfer katılımcısı, hem en büyük within-region deltaya sahip, hem de en
büyük AOI / en çok hücre. Discussion'da bunu yangın rejimine bağlamadan önce, davranışın bölgeden mi
yoksa veri hacminden mi geldiğini bilmemiz lazım — Muğla'yı Manavgat'ın hücre sayısına altörnekleyip
tekrar bakabilir misin?

9) CORAL λ DUYARLILIĞI (yeni çiftler).
Mevcut tarama yalnız Manavgat↔Bejís'i kapsıyor. Muğla çiftleri için de — özellikle transfer olan tek
yön olan Bejís↔Muğla için — genişletir misin?

—— KISA TEYİTLER ——

- Son export'un ortam sürümleri (scikit-learn / pandas / numpy) ve git commit'i. Elimdeki transfer
  JSON'ları commit c648486... gösteriyor; son export bununla eşleşiyor mu?
- Evia'nın gate kararı ve out_of_window_burndate sayısı (ikisi de eksik parçada).
- Son bölgenin tahmini bitiş süresi, ve Evia AOI'sinin büyütülebilir olup olmadığı.

Bir de altın kural: mevcut kısmi export'tan hiçbir sayı makaleye girmeyecek — her rakam son tam
koşumdan gelip yeniden doğrulanacak. O yüzden acele etme, tam ve temiz olsun.

Eline sağlık, gidişat gerçekten iyi.

Sevgiler,
Yunus Emre
