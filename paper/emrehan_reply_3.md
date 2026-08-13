# Emrehan'ın yanıtı — 2026-08-13 (emrehan_mail_2.md'deki dört isteğe)

Aşağıdaki metin gelen mailin aynen kopyasıdır. Ekleri: `reproduction_check.json` (arşiv:
`paper/reproduction_check/reproduction_check_5region.json`, sha256 `7f7e41f5…09c8be`) ve Drive
klasörü `mugla_2021__mugla_2022_event_relative` (arşiv:
`paper/mugla_transfer_raw/emrehan_run_20260809/`, kaynak zip sha256 `c06fdf07…20ef`).

---

Merhaba Hocam,

Son mailde istediklerinizi methods haricinde tamamladım:

1-) Beş bölgeli reproduction check'i donmuş çıktılar kullanarak oluşturdum. Sonuçları içeren JSON
dosyasını mailin sonunda bırakıyorum. Başlıca sonuçlar şöyle:
- within-region maksimum ROC-AUC farkı: 0.0
- CORAL maksimum ROC-AUC farkı: 1.62×10^-7
- 20/20 CORAL yönü tamam

2-) Muğla 2022 - 2021 tarafında ise tahminimce yine arşiv problemi yaşıyoruz. Zira daha önce bu
transferi koşup sonuçlarını da size iletmiştim. İki yönün Step9-10 çıktıları da arşivde mevcut.
Bendeki sonuçlar da sizin elde ettiğiniz sonuçlara çok yakın:
mugla_2021__mugla_2022_event_relative:
https://drive.google.com/drive/folders/1LjPsedzTKnMvySUGVSLLL4BV6PPycwwt?usp=sharing

Muğla 2021 -> Muğla 2022:
    Baseline: 0.6421
    Thermal: 0.5588
    ΔROC-AUC: -0.0833, %95 CI [-0.1269, -0.0396]

Muğla 2022 -> Muğla 2021:
    Baseline: 0.5809
    Thermal: 0.6692
    ΔROC-AUC: +0.0883, %95 CI [+0.0721, +0.1040]

Hocam sonuçlar var olduğu için koşmadım ama dilerseniz tekrar koşup size iletebilirim.

3-) Few-shot analizi için kararım: ek materyale girebilir. Üç bölge ve altı yönlük mevcut analiz
tamam ve metodolojik sınırları da korunuyor. Validator'daki self-reference kaynaklı iki
false-positive kontrolünü de düzelttim; validator şu anda PASS veriyor.

4-) Methods konusu: bir teknik envanter oluşturdum. Envanteri kod ve donmuş çıktılar üzerinden
çıkardım. Ayrıca size ileteceğim.

Çok teşekkür ederim. Sizin de emeğinize sağlık hocam.

---

## Doğrulama kaydı (YEC + Claude, 2026-08-13) — sayılar kaynaktan okundu

**Madde 1 — reproduction_check.json.** Mailde verilen üç sayı JSON'la birebir tutuyor:
within-region `max_abs_roc_auc_difference` = 0 (tam sıfır; 20 karşılaştırma = 5 bölge × 2 model
ailesi × 2 metrik, hepsi üretilmiş), CORAL `max_abs_roc_auc_difference` = 1.6164523e-7
(20 yön; yön başına 2 aile × 2 metrik = 80 karşılaştırma, `missing_directions` boş; 80'in 69'u
bit-özdeş, kalan 11'i ≤1.6e-7). PR-AUC farkları da aynı tolerans içinde. Tolerans kriteri JSON'un
kendi ifadesiyle deponun `src/step10c_paired_evaluation_bootstrap.py` içindeki mevcut 1e-6
fail-fast kriteri, değiştirilmeden uygulanmış. Kohort üç bağımsız yoldan çözülmüş ve üçü aynı
sıralı kümeyi veriyor (`routes_agree: true`); Kozan `negative_control`, Muğla 2022
`temporal_transfer_wildfire` rolüyle dışlanmış. İki sırasız çiftte (Bejís–Muğla, Manavgat–Muğla)
diskte mükerrer Step10 namespace'i var; referans artefaktı dizin listesi değil donmuş sentez
manifesti seçmiş. Hepsi §3.13'e yazıldı.

**Madde 2 — Muğla kolları: mailde yazandan daha güçlü.** Emrehan'ın kendi koşumunun çıktıları da
elimize geçti (2026-08-09, commit `a07ea33`, sklearn 1.9.0 / pandas 3.0.2 / numpy 2.4.4; bizimki
2026-08-11, commit `48b56e7`, sklearn 1.9.0 / pandas 3.0.5 / numpy 2.5.2). Girdi step8a
parquet'lerinin sha256'ları iki koşumda aynı. Uyum mailde tahmin edilen 1e-3 değil **≤1×10⁻⁷**:
2021→2022 yönü bütün metriklerde bit-özdeş, çiftteki en büyük fark 9.9e-8, bootstrap ΔAUC sınırları
≤3.4e-8 içinde, step9b/step9c özet `.md` dosyaları ise bayt-özdeş. §3.16.4 buna göre güncellendi;
"bu iki yön makale yazarlarınca üretildi" cümlesi "iki bağımsız ortamda üretildi" oldu.

**Madde 3 — few-shot.** `paper/S1_few_shot_recovery.md` yazıldı, §5.5 işaretçisi Supplementary S1'e
bağlandı. Elimizdeki donmuş çıktının kendi validator raporu zaten 64 PASS / 1 SKIPPED
(`FSR-35[mugla_2021]`, Muğla'nın donmuş blok-10 artefaktı olmadığı için). Emrehan'ın bahsettiği iki
self-reference false-positive düzeltmesi bu donmuş rapordan **sonra** yapılmış olmalı; elimizdeki
artefakt 2026-08-02 / commit `19d825b` damgalı, dolayısıyla o düzeltmeyi buradan doğrulayamıyoruz
ve S1'de öyle yazıldı.

**Madde 4 — Methods envanteri.** Henüz gelmedi; ayrı tur.

## Depo kaynağından doğrulama (2026-08-13, `repo/` @ 48b56e7)

Yukarıdaki maddelerin JSON/config'in **kendi beyanına** dayanan kısımları koddan geçirildi:

- **Tolerans (en kritik).** `RAW_REPRODUCTION_TOLERANCE` ve `WITHIN_REGION_REPRODUCTION_TOLERANCE`
  = 1e-6, `src/step10c_paired_evaluation_bootstrap.py:59-60`; ihlalde `Step10Error` fırlatıyor
  (:373). `git log -S` ikisinin de **bccc258 / 2026-07-13** commit'inde girdiğini ve o gün bugündür
  değişmediğini gösteriyor — reproduction check'ten (2026-08-11) dört hafta önce. "Sonuca göre
  seçilmedi" iddiası artık JSON'un kendi cümlesine değil, commit geçmişine dayanıyor.
- **Kohort rotası 1.** `core/regions.py`'de 9 kayıt var. canonical = `superseded_by` taşımayan
  kayıt (bu filtre `evia_2021` ve `mugla_2022`'yi düşürüyor), artı `negative_control` ve
  `temporal_transfer_wildfire` rollerinin çıkarılması → tam olarak beş. §3.13'te supersession
  filtresi yazılı değildi, eklendi.
- **DÜZELTME — §3.16.4 fazla iddia ediyordu.** `A07_mugla_2022_absent_from_default_analysis`
  (`scripts/validate_era5_land_regional_diagnostic.py:317-321`) literal `"mugla_2022"` dizgesinin
  üyeliğini test ediyor — yani registry'deki **superseded takvim-kaydırma kaydını**. Bizim analiz
  ettiğimiz `mugla_2022_event_relative` farklı bir dizge, dolayısıyla A07 onu yakalamaz. Gerçek
  güvence `A08_cohort_is_the_frozen_five` (DEFAULT_EXPERIMENTS ile birebir sıralı tuple eşitliği).
  Paragraf ikisini de söyleyecek şekilde düzeltildi.
- **S1 protokol iddiaları.** `src/few_shot_recovery.py`: tier sabitleri :125-127, blake2b seed
  türetimi :324, blok id'ye göre sırala-sonra-karıştır :719-720, `FORBIDDEN_UNCERTAINTY_TERMS`
  :196. Hepsi config.json'un beyanıyla uyuşuyor.
