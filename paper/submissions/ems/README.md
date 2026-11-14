# Environmental Modelling & Software paketi

Hedef dergi: Environmental Modelling & Software (Elsevier, ISSN 1364-8152). Karar 14 Kasım 2026, gerekçesi `C:\Users\CORSAIR\projects\ThermalTwin\reports\Dergi seçimi ve doçentlik uygunluğu.md`. Analizler `thermal-twin/repo` içindeki `scaleup-31fires` dalında, plan `docs/scaleup/ANALYSIS_PLAN.md`.

Bu klasör eski paketlerden bağımsızdır. Ortak kaynaklar ve diğer dergi paketleri değiştirilmez, gereken metin buraya kopyalanıp burada düzenlenir.

## Klasörler

- `template/EMS_guide_for_authors_2026-11-14.txt`: derginin yazar rehberi, 14 Kasım 2026'da ScienceDirect'ten kaydedildi.
- `template/elsarticle/`: Elsevier LaTeX şablonu (CTAN, elsarticle). `elsarticle.cls` `latex elsarticle.ins` ile üretildi. Yazar-yıl atıf için `elsarticle-template-harv.tex` ve `elsarticle-harv.bst` kullanılır.
- `literature/`: ileride gereken notlar. Kaynakların kendisi Zotero'da, koleksiyon "EMS wildfire evaluation-protocol manuscript (2026-11)" (anahtar SMIQXLB2).

## Zotero'ya PDF'i eklenecek makaleler (yazar dönünce, Çukurova girişi ya da Zotero Connector ile)

Koleksiyon SMIQXLB2. 14 Kasım 2026'da tam metni Zotero'da olanlar: Brenning 2022, Ploton 2020, Zerouali 2026 (PDF), Goodling 2024 ve Frank 2025 (açık erişim tam metni, Markdown eki). Eksik olanlar:

| Makale | DOI | Zotero anahtarı |
|---|---|---|
| Meyer vd. 2018, EMS | 10.1016/j.envsoft.2017.12.001 | LJJ4XA2K |
| Leuenberger vd. 2018, EMS | 10.1016/j.envsoft.2017.12.019 | X48KU5EH |
| Pais vd. 2021, EMS | 10.1016/j.envsoft.2021.105122 | W5ZQWUIB |
| Costa-Saura vd. 2023, EMS | 10.1016/j.envsoft.2023.105685 | BFN52W2M |
| Hijmans 2012, Ecology | 10.1890/11-0826.1 | DQ79YGUC |
| Roberts vd. 2017, Ecography | 10.1111/ecog.02881 | L6BGGMXM |

## Rehberden çıkan kurallar

- Makale türü: Research article. Başka bir tür için önce baş editöre yazmak gerekiyor.
- Hakemlik tek taraflı anonim (yazar adları açık), en az iki hakem.
- Dosya: Word (.docx, tek sütun) ya da LaTeX (.tex). PDF kaynak dosya kabul edilmez.
- Özet en çok 150 kelime. Amaç, yöntem, ana bulgular ve sonuç. Kaynak verilmez.
- Anahtar kelime 1 ile 7 arası, çok kelimeli olmamaya çalışılır.
- Highlights zorunlu, ayrı dosya, adında "highlights" geçmeli. 3 ile 5 madde, her biri en çok 85 karakter (boşluk dahil).
- Graphical abstract zorunlu, ayrı dosya, en az 1328 piksel genişlik, 13 cm'de okunur olmalı.
- Bölümler numaralı (1, 1.1, 1.1.1). Özet numaralandırılmaz.
- Şekiller ayrı dosya: vektör için EPS ya da PDF, fotoğraf için en az 300 dpi.
- Tablolar düzenlenebilir metin olmalı, dikey çizgi ve gölgelendirme yok.
- Software and/or data availability bölümü bekleniyor: yazılımın adı, geliştirici ve iletişim, ilk yayın yılı, gereken donanım ve yazılım, erişim ve maliyet, programlama dili ve boyut. "Yazara başvurun" kabul edilmez. GitHub, Zenodo gibi bir depo verilmeli. Yazılım makalenin esas parçasıysa hakemlere indirme bağlantısı verilmeli.
- Araştırma verisi için Option C: veriler bir depoya konur ve gönderimde bağlantı verilir, paylaşılamıyorsa gerekçe yazılır.
- Atıf biçimi yazar-yıl (Harvard). Gönderimde kaynak biçimi serbest ama tutarlı olmalı, DOI'ler eklenmeli. Ön baskılar "preprint" diye işaretlenir.
- CRediT yazar katkıları beyanı zorunlu.
- Üretken yapay zekâ kullanıldıysa kaynakçadan önce ayrı bir bölümde beyan edilir.
- Haritalarda yalnızca çalışma alanı gösterilir ve "map lines delineate study areas and do not necessarily depict accepted national boundaries" notu eklenir.
- Teşekkür kaynakçadan hemen önce ayrı bölümde.
- İsteğe bağlı: gönderim sırasında SSRN'de ücretsiz ön baskı. Tüm yazarların onayı gerekir.
- Kelime sınırı rehberde yazılı değil.
