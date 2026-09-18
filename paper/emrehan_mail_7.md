# Emrehan'a cevap — 17 Eylül mailine (taslak, 2026-09-19; GÖNDERİLMEDİ)

Merhaba Emrehan,

Teşekkürler, eline sağlık. Gecikme hiç sorun değil, tadilatın kolay geçsin.

Cevaplarını makaleye işledim. Envanteri güncellerken iki maddede "çözülemedi" yerine daha kesin bir ifade kullanabilirsin, çünkü cevap arşivde var:

1) MODIS QC: Bu üç bölgede kural uygulanmamış. QC kuralı export betiğine 2026-07-23'te girmiş, Manavgat/Bejís/Muğla export'ları ondan önce yapılmış. Envantere "UNRESOLVED" yerine "not applied — regions exported before the rule was added (2026-07-23)" yazabilirsin. Paper 2 §4.2 bu farkı ve maliyetini zaten ölçüyor.

4) EE kernel: Hiçbir EE çağrısında explicit resample()/reproject() yok (git geçmişinde de hiç olmamış), export'lar yalnız scale + crs veriyor (step4_export_geotiff.py:155-165). Bu durumda EE'nin belgelenmiş varsayılanı, yani nearest-neighbour geçerli. Ölçekler de native'e çok yakın (MODIS 1000 m, diğerleri native), dolayısıyla pyramid seviyesi de devreye girmiyor. "Belirlenemez" yerine "no explicit kernel; Earth Engine default (nearest-neighbour) applies" yazabilirsin.

5) Window-closure: Burada haklısın, iyi yakaladın. Plan aşamasındaki kayıt sensitivity koşusundan önce ama kanonik sonuçlar görüldükten sonra. Bizim notumuz bunu atlamıştı; makalede hiçbir zaman "performanstan bağımsız önceden belirlendi" demeyeceğiz.

2) AOI: Senin bulgunu repo'nun git geçmişiyle birleştirip makalede bölge bazında yazdım. "Hiçbiri gate sonucuna göre ayarlanmadı" iddiasını kaldırdım; her bölge için kaydın tam olarak neyi gösterdiğini yazdım. Tek bir şey soracağım: Manavgat bbox'ı 968d27d'de (8 Temmuz) gate-only workflow ile aynı commit'te geliyor. regions.py'deki yorumlardan biri "refined manually; should be checked against MCD64A1" diyor, Bejís yorumu ise Manavgat'ı "gate sonrası netleştirilmiş" diye anıyor. Kuzeye kaydırılmış dikdörtgeni ilk gate koşusundan önce mi çizdin, sonra mı, hatırlıyor musun? Kayıt yoksa sorun değil, makalede zaten "belirlenemez" olarak duruyor.

3) ve 6) tamam, teşekkürler.

İyi çalışmalar.
Yunus Emre
