# CURE Backend - Bastan Sona Sunum ve Demo Akisi

Bu dosyayi sunumdan once prova etmek ve sunum sirasinda adim adim takip etmek icin kullan.

## 0. Calistirma

Terminal:

```powershell
cd C:\Users\zeyne\Desktop\cure-zeynepkaratas-FINAL-v2\backend
C:\Users\zeyne\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m uvicorn src.api.endpoints:app --host 127.0.0.1 --port 8000
```

Tarayici:

```text
http://127.0.0.1:8000/docs
```

## 1. Acilis Konusmasi

> Ben projede backend ve test tarafindan sorumluydum. Backend katmaninda frontend veya AI tarafindan gelen gereksinim metnini API uzerinden aliyorum, UML uretiyorum, UML'i syntax ve OCL kurallariyla dogruluyorum, render response hazirliyorum, hata loglama ve otonom onarim akislarini yonetiyorum. Son checkpointte de performans metriklerini ve SLA kontrolunu ekledim.

## 2. Proje Dosyalarini Tanit

Hocaya kod nerede diye sorarsa:

- `src/api/endpoints.py`: Ana FastAPI dosyasi. Swagger'da gorunen endpointler burada.
- `src/parsers/srs_parser.py`: SRS metninden sinif ve iliski cikarip PlantUML uretir.
- `src/ocl_engine/ocl_validator.py`: PlantUML'i OCL/tasarim kurallariyla dogrular.
- `src/ocl_engine/error_handler.py`: Hatalari standart JSON formatina cevirir.
- `src/renderers/plantuml_renderer.py`: PlantUML icin SVG/PNG response hazirlar.
- `src/api/error_log_endpoint.py`: Hata log endpointleri.
- `src/api/performance.py`: Latency, SLA, P50/P95/P99 metrikleri.
- `tests/test_backend.py`, `tests/test_full.py`, `tests/test_zeynep_checkpoint_api.py`: Testler.

## 3. Demo 1 - Health Check

Swagger:

```text
GET /health
```

Adimlar:

1. Endpointi ac.
2. `Try it out` tikla.
3. `Execute` tikla.

Beklenen sonuc:

```json
{
  "durum": "aktif",
  "versiyon": "1.0.0"
}
```

Soylenecek:

> Ilk olarak backend servisinin ayakta olup olmadigini kontrol ediyorum. `durum: aktif` donmesi API'nin calistigini gosteriyor.

## 4. Demo 2 - SRS Metninden UML Uretme

Swagger:

```text
POST /generate-uml
```

Request body:

```json
{
  "metin": "The UserManager handles user authentication. The DiagramService generates PlantUML diagrams. The ValidationEngine validates diagrams. The UserManager uses the DiagramService. The DiagramService uses the ValidationEngine.",
  "dil": "en"
}
```

Beklenen alanlar:

- `basarili: true`
- `plantuml_kodu`
- `siniflar`
- `iliskiler`
- `render`
- `dogrulama.gecerli_mi: true`

Soylenecek:

> Bu endpoint checkpoint 1 icin ana API. Gereksinim metnini aliyor, parser ile siniflari ve iliskileri cikariyor, PlantUML kodu uretiyor. Sonra OCL dogrulamasi ve SVG/PNG render response ekliyor.

## 5. Demo 3 - Hazir PlantUML Render Etme

Swagger:

```text
POST /api/render
```

Request body:

```json
{
  "plantuml_kodu": "@startuml\nclass UserManager {}\nclass DiagramService {}\nUserManager --> DiagramService\n@enduml"
}
```

Soylenecek:

> Burada elimizde hazir PlantUML varsa backend once compile/syntax kontrolu yapiyor. Gecerliyse frontend'in kullanabilecegi SVG ve PNG alanlarini response olarak donduruyor.

## 6. Demo 4 - OCL Dogrulama

Swagger:

```text
POST /api/validate
```

Request body:

```json
{
  "plantuml_kodu": "@startuml\nclass UserManager {}\nclass DiagramService {}\nUserManager --> DiagramService\n@enduml"
}
```

Beklenen alanlar:

- `gecerli_mi: true`
- `skor`
- `hatalar`
- `uyarilar`
- `detaylar`

Soylenecek:

> Bu kisimda PlantUML kodunu OCL ve tasarim kurallarina gore dogruluyorum. Hata, uyari ve skor bilgileri standart JSON olarak donuyor.

## 7. Demo 5 - Semantik Degerlendirme

Swagger:

```text
POST /api/evaluate
```

Request body:

```json
{
  "srs_metni": "The UserManager handles user authentication. The DiagramService generates PlantUML diagrams. The UserManager uses the DiagramService.",
  "plantuml_kodu": "@startuml\nclass UserManager {}\nclass DiagramService {}\nUserManager --> DiagramService\n@enduml"
}
```

Soylenecek:

> Bu endpoint kaynak SRS ile uretilen UML'in ne kadar uyumlu oldugunu olcuyor. Sinif dogrulugu, iliski dogrulugu, butunluk ve tutarlilik kriterlerini donduruyor.

## 8. Demo 6 - Iterasyon Compile Testi

Swagger:

```text
POST /api/iterate
```

Request body:

```json
{
  "plantuml_kodu": "@startuml\nclass UserManager {}\nclass DiagramService {}\nUserManager --> DiagramService\n@enduml",
  "iterasyon_no": 1,
  "srs_metni": "The UserManager handles user authentication. The DiagramService generates PlantUML diagrams. The UserManager uses the DiagramService."
}
```

Soylenecek:

> Checkpoint 3'te her onarim adiminda compile testi yapmam gerekiyordu. Bu endpoint bir iterasyonun sonucunu donduruyor. Compile sonucu, semantik sonuc ve sure bilgisi birlikte geliyor.

## 9. Demo 7 - Otonom Onarim

Swagger:

```text
POST /api/autonomous-repair
```

Bilerek hatali request body:

```json
{
  "plantuml_kodu": "class UserManager {}",
  "srs_metni": "The UserManager handles user authentication.",
  "max_iterasyon": 3
}
```

Beklenen:

- Ilk iterasyonda eksik `@startuml` ve `@enduml` yakalanir.
- Hata loglanir.
- Basit healer eksik etiketleri tamamlar.
- Final UML doner.
- `basarili: true`

Soylenecek:

> Burada bilerek eksik PlantUML veriyorum. Backend once hatayi yakaliyor, hata loguna kaydediyor, sonra basit healer katmani ile eksik etiketleri tamamliyor. Maksimum 3 iterasyon siniri var, bu da sonsuz donguyu engelliyor.

## 10. Demo 8 - Hata Loglari

Swagger:

```text
GET /api/error-log
```

Soylenecek:

> Otonom onarim sirasinda yakalanan hatalar burada tutuluyor. Frontend hata paneli veya analiz ekrani bu loglari kullanabilir.

## 11. Demo 9 - Tam Analiz Pipeline

Swagger:

```text
POST /api/analyze
```

Request body:

```json
{
  "metin": "The UserManager handles user authentication. The DiagramService generates PlantUML diagrams. The ValidationEngine validates diagrams. The UserManager uses the DiagramService. The DiagramService uses the ValidationEngine.",
  "dil": "en"
}
```

Soylenecek:

> Bu endpoint tum pipeline'i tek istekte calistiriyor: SRS parse, UML uretimi, OCL dogrulama, semantik degerlendirme ve latency olcumu.

## 12. Demo 10 - Performans Raporu

Swagger:

```text
GET /api/performance
```

Beklenen alanlar:

- `toplam_istek`
- `basari_orani`
- `sla_uyum_orani`
- `latency_ms.P50`
- `latency_ms.P95`
- `latency_ms.P99`
- `sla_siniri_saniye: 15`

Soylenecek:

> Checkpoint 4 icin performans olcum katmani ekledim. Burada 15 saniye SLA, basari orani ve P50/P95/P99 latency metriklerini raporluyorum.

## 13. Kapanis

> Sonuc olarak benim backend/test kapsamimda API endpointleri, request validation, PlantUML uretimi, render response, OCL dogrulama, hata loglama, iterasyonlu onarim akisi ve performans metrikleri tamamlandi. Test paketlerinde de backend unit, integration, E2E ve API kontrat testleri basarili calisti.

Test sonuclari:

- `test_backend.py`: 10/10
- `test_full.py`: 20/20
- `test_zeynep_checkpoint_api.py`: 4/4

## 14. Sunumda Sorulabilecek Sorulara Kisa Cevaplar

**Soru: Ana backend dosyasi nerede?**  
`src/api/endpoints.py`

**Soru: Request validation nerede?**  
Pydantic modellerinde: `SRSGirdisi`, `UMLDogrulamaGirdisi`, `IterasyonGirdisi`.

**Soru: UML nasil uretiliyor?**  
`src/parsers/srs_parser.py` SRS metninden sinif ve iliski cikarip PlantUML kodu uretiyor.

**Soru: Render nasil yapiliyor?**  
`src/renderers/plantuml_renderer.py` PlantUML kodundan SVG response olusturuyor ve PNG alanini kontrat icin ekliyor.

**Soru: Hatalar nasil standartlasiyor?**  
`src/ocl_engine/error_handler.py` icindeki `hata_normalize_et` fonksiyonu ile.

**Soru: Sonsuz dongu nasil engelleniyor?**  
`OtonomOnarimGirdisi` modelinde `max_iterasyon` 1-3 arasinda sinirli. Endpoint de en fazla 3 tur calisiyor.

**Soru: Performans nasil olculuyor?**  
`src/api/performance.py` istek surelerini in-memory tutuyor, P50/P95/P99 ve SLA uyumunu hesapliyor.
