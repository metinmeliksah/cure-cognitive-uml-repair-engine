# Zeynep Karatas - Backend Sunum Rehberi

## 1. Benim sorumluluk alanim

Ben projede backend ve test tarafindan sorumluydum. Yaptigim kisim, frontend ve AI katmanindan gelen veriyi API uzerinden alip isleyen ana servis katmanidir.

Kisaca backend su isleri yapiyor:

- SRS/gereksinim metnini aliyor.
- Bu metinden PlantUML kodu uretiyor.
- Uretilen UML'i syntax ve OCL kurallariyla kontrol ediyor.
- UML'i frontend'in gosterebilecegi SVG/PNG response formatina ceviriyor.
- Hatalari standart JSON formatina normalize ediyor.
- Otonom onarim icin maksimum 3 iterasyonluk compile-test akisi calistiriyor.
- Performans olcumlerini P50/P95/P99 ve 15 saniye SLA olarak raporluyor.

## 2. Ana dosyalar

| Dosya | Ne ise yariyor? |
| --- | --- |
| `src/api/endpoints.py` | FastAPI uygulamasi ve tum Swagger endpointleri |
| `src/parsers/srs_parser.py` | SRS metninden sinif/iliski cikarip PlantUML uretir |
| `src/ocl_engine/ocl_validator.py` | PlantUML'i OCL ve tasarim kurallarina gore dogrular |
| `src/ocl_engine/error_handler.py` | JSON parser, hata normalize ve exception logging yapar |
| `src/renderers/plantuml_renderer.py` | PlantUML kodunu SVG/PNG response formatina cevirir |
| `src/api/error_log_endpoint.py` | Hata loglarini kaydeder ve listeler |
| `src/api/performance.py` | Latency, SLA ve percentile metriklerini hesaplar |
| `tests/test_backend.py` | Parser, OCL ve semantik unit testleri |
| `tests/test_full.py` | CP2, CP3, CP4 integration/E2E/performance testleri |

## 3. Hocaya anlatilacak akil

1. `GET /health`
   - Backend ayakta mi kontrol eder.
   - Sunuma bununla baslamak guvenli.

2. `POST /generate-uml`
   - Checkpoint 1 icin ana endpoint.
   - SRS metni alir, PlantUML uretir, OCL dogrulama ve render cevabi doner.

3. `POST /api/render`
   - Hazir PlantUML kodunu alir.
   - Once compile/syntax kontrolu yapar.
   - Gecerliyse SVG/PNG alanlariyla response doner.

4. `POST /api/validate`
   - PlantUML kodunu OCL kurallarina gore kontrol eder.
   - Hatalar, uyarilar, skor ve detaylari doner.

5. `POST /api/iterate`
   - Her onarim denemesi icin compile ve opsiyonel semantic test sonucu verir.
   - Maksimum 3 iterasyon mantigini destekler.

6. `POST /api/autonomous-repair`
   - Hatalı PlantUML girdisini en fazla 3 denemede onarmaya calisir.
   - Hata varsa loglar, temel syntax onarimi yapar, final UML ve render cevabi doner.

7. `GET /api/error-log`
   - Otonom onarim sirasinda kaydedilen hata loglarini gosterir.

8. `GET /api/performance`
   - CP4 icin latency, basari orani, SLA uyumu ve P50/P95/P99 raporu verir.

## 4. Demo icin ornek inputlar

### /generate-uml

```json
{
  "metin": "The UserManager handles user authentication. The DiagramService generates PlantUML diagrams. The UserManager uses the DiagramService.",
  "dil": "en"
}
```

### /api/render

```json
{
  "plantuml_kodu": "@startuml\nclass UserManager {}\nclass DiagramService {}\nUserManager --> DiagramService\n@enduml"
}
```

### /api/autonomous-repair

```json
{
  "plantuml_kodu": "class UserManager {}",
  "srs_metni": "The UserManager handles user authentication.",
  "max_iterasyon": 3
}
```

Bu ornekte bilerek `@startuml` ve `@enduml` eksik veriliyor. Backend bunu yakalayip onarim akisinda tamamliyor.

## 5. Test sonucu olarak soylenecekler

- `tests/test_backend.py`: 10/10 gecti.
- `tests/test_full.py`: 20/20 gecti.
- `tests/test_zeynep_checkpoint_api.py`: 4/4 gecti.

## 6. Calistirma komutu

```powershell
cd C:\Users\zeyne\Desktop\cure-zeynepkaratas-FINAL-v2\backend
C:\Users\zeyne\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m uvicorn src.api.endpoints:app --host 127.0.0.1 --port 8000
```

Sonra tarayicida:

```text
http://127.0.0.1:8000/docs
```
