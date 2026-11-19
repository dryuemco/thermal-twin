# EMS gönderi paketi: seçim sonucu makalesi

Makale: "Within-event spatial cross-validation selects coordinate-only wildfire models that rank later burning worse: evidence from 31 Mediterranean fires". Hedef dergi Environmental Modelling & Software, tür Research article. Bu klasör `../ems/` paketinden bağımsız. 14 Kasım taslağı değiştirilmedi.

Bu README iç not, dergiye yüklenmez. `_internal/` klasörü de yüklenmez (Codex denetim raporları).

## Durum (19 Kasım 2026)

QA biti hatası düzeltildi. Plan Amendment 15 (920e9fe) koşumdan önce push edildi, kod f2422e6, sonuçlar fb21316, kayıt defteri ee90c35 (dal `scaleup-31fires`). Eski etiket bir yangında birebir yeniden üretildikten sonra iki pencere bit 1 ile yeniden üretildi. Uygun yangın kümeleri değişmedi. Tek değişen kural sonucu pencere B'de termal RF + uzaklık çifti (Holm p 0.0254'ten 0.0238'e). Metin, özet ve vurgular düzeltilmiş sonuçları kullanıyor, ek Tablo S3 eski ve yeni sonuçları yan yana veriyor.

İkinci Codex denetimi (`_internal/codex_audit_2_preaudit.md`, ön gönderim hakem denetimi) sonrası metin, kapak mektubu ve derleme betiği güncellendi. Ek Tablo S4 plandaki her analizin durumunu, Tablo S5 üç yangın çiftini veriyor.

## Göndermeden önce senin yapman gerekenler

1. Emrehan'ın onayı. Kapak mektubunda "Both authors approved the submission" yazıyor.
2. Hakemlerin indirebileceği arşiv. Metin, kodun, modelleme tablolarının, etiketlerin ve dondurulmuş skorların sürümlü bir Zenodo kaydına konacağını söylüyor. Denetim bunun gönderimden önce yapılmasını istiyor: sabit commit kimliği, SHA-256 listesi ve etiket rasterlarıyla tek bir indirilebilir sürüm. Zenodo kaydı dışa açık bir işlem, ben yapmadım. DOI gelince `manuscript.tex`'teki yazılım ve veri bölümüne ve kapak mektubuna bağlantı eklenmeli.
3. Depo `dryuemco/thermal-twin` dalı `scaleup-31fires` herkese açık mı, kontrol et. Dalda iç süreç notları var (`docs/scaleup/SESSION_HANDOFF_*.md`, `reviews/`). Hakemlere verilecek arşivde bunların olup olmayacağına karar ver. Zamanlama kanıtı olan commit'ler korunmalı.
4. JCR'de EMS'in CS Interdisciplinary Applications çeyrekliğini teyit et.

## Dosyalar

Yüklenecekler: `manuscript.tex` ve `manuscript.pdf` (LaTeX gönderiminde `values.tex`, `values_frozen.tex`, `references.bib`, `elsarticle.cls`, `elsarticle-harv.bst`, `figures/` de), `figures/Figure_1-3.pdf`, `graphical_abstract.png`, `highlights.docx`, `supplementary.pdf`, `cover_letter.docx`.

Üretim: `build_values.py` sayıları, ek tabloları, şekilleri ve grafik özeti `thermal-twin/repo/results/scaleup` sonuçlarından üretir (varsayılan `THERMAL_TWIN_LABEL_SUFFIX=_qa1`, düzeltilmiş etiketler). `make_highlights.py` ve `make_cover_letter.py` sayıları değer dosyalarından alır.

```
python build_values.py
python make_highlights.py
python make_cover_letter.py
pdflatex manuscript && bibtex manuscript && pdflatex manuscript && pdflatex manuscript
pdflatex supplementary && pdflatex supplementary
```
