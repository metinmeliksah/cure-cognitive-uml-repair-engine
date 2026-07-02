# Data Pipeline

## Aciklama

Veri hazirlik dosyalari `data_pipeline/` altinda toplandi. Kok dizindeki daginik
CSV ve preprocessing scriptleri ilgili alt klasorlere tasindi.

## Amac

Dataset, preprocessing, vector DB hazirligi ve manuel degerlendirme dosyalarini
tekrar uretilebilir bir klasor yapisinda tutmak.

## Kurulum

Ek kurulum yoktur. Scriptler Python standart kutuphaneleri ile calisir.

## Konfigurasyon

Yok.

## Kullanim

```bash
python data_pipeline/preprocessing/xml_to_csv.py
python data_pipeline/preprocessing/cure_veri_hazirlik.py
```

## Bagimliliklar

Mevcut scriptlerin kendi importlari kullanilir.

## Dosya Yapisi

- `data_pipeline/datasets/pure_dataset.csv`
- `data_pipeline/preprocessing/cure_veri_hazirlik.py`
- `data_pipeline/preprocessing/xml_to_csv.py`
- `data_pipeline/vector_db/README.md`
- `data_pipeline/evaluation/ground_truth_manual_review.md`

## API

Yok.

## Veritabani Degisiklikleri

Yok.

## Test

Scriptler kaynak veri ile calistirilip cikti CSV dosyalari kontrol edilir.

## Hata Senaryolari

- Kaynak XML/CSV yoksa script dosya bulunamadi hatasi verir.
- Manuel review tablosu guncellenmezse deney sonuclari akademik olarak izlenemez.

## Gelistiren

Isim: CURE Team
Tarih: 2026-07-02

## Degisiklik Gecmisi

v1.0 - Data pipeline klasor yapisi dokumante edildi.
