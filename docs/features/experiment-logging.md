# Experiment Logging

## Aciklama

`experiments/run_autonomous_repair.py`, autonomous repair endpointini birden
fazla senaryo uzerinde calistirir ve `results/` altina CSV/JSON loglari yazar.

## Amac

Basari orani gibi makale metriklerini elle yazilmis dosyalara dayandirmadan,
tekrar uretilebilir deney ciktilariyla hesaplamak.

## Kurulum

```bash
pip install -r backend/requirements.txt
pip install -r ai_core/requirements.txt
```

## Konfigurasyon

Opsiyonel:

```bash
python experiments/run_autonomous_repair.py --max-iterations 3 --output-dir results
```

## Kullanim

```bash
python experiments/run_autonomous_repair.py
python ai_core/log_analiz.py results/autonomous_repair_results.json
```

## Bagimliliklar

- Backend autonomous repair endpoint fonksiyonu
- Python csv/json standart kutuphaneleri

## Dosya Yapisi

- `experiments/run_autonomous_repair.py`
- `results/.gitkeep`
- `ai_core/log_analiz.py`

## API

Script, backend fonksiyonunu process icinde cagirir. Calisan HTTP sunucu gerekmez.

## Veritabani Degisiklikleri

Yok.

## Test

```bash
python experiments/run_autonomous_repair.py --max-iterations 1
python ai_core/log_analiz.py results/autonomous_repair_results.json
```

## Hata Senaryolari

- AI ajan calismazsa endpoint fallback healer durumunu son iterasyon statusu olarak loglar.
- Output klasoru yoksa script otomatik olusturur.

## Gelistiren

Isim: CURE Team
Tarih: 2026-07-02

## Degisiklik Gecmisi

v1.0 - Deney loglama dokumantasyonu eklendi.
