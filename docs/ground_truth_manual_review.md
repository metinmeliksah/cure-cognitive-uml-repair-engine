# CURE Backend Manual Review Sample

Bu iç doküman, Zeynep Karataş'ın sorumluluk alanındaki `backend/src/ocl_engine/`
ve `backend/src/evaluators/` çıktılarının küçük bir elle doğrulama örneklemiyle
gözden geçirilmesi için hazırlanmıştır. Makale metnine eklenmemelidir; yalnızca
proje içi kontrol ve danışmanla paylaşılabilecek destek materyali olarak
kullanılmalıdır.

## Amaç

- `ocl_engine` tarafından üretilen ihlal/uyarı çıktılarının insan gözüyle
  makul olup olmadığını kontrol etmek.
- Bağımsız ground truth veri seti bulunmadığı durumda, küçük bir doğrulama
  örneklemiyle sınırlı fakat izlenebilir bir kalite notu üretmek.
- Onay sütunları doldurulduktan sonra makaleye yalnızca kısa bir metodolojik
  not eklemek; bu tabloyu makaleye koymamak.

## İnceleme Şablonu

| No | PlantUML girdisi / senaryo | Beklenen ihlal türü | Sistem çıktısı | Skor | Zeynep onayı | Not |
|---:|---|---|---|---:|---|---|
| 1 | `class UserManager {}\n@enduml` | Eksik başlangıç etiketi | Hata: `@startuml etiketi eksik` | %80.0 |  |  |
| 2 | `@startuml\nclass UserManager {}` | Eksik bitiş etiketi | Hata: `@enduml etiketi eksik` | %80.0 |  |  |
| 3 | `@startuml\n@enduml` | Boş diyagram | Hata: `Hic sinif tanimlanmamis` | %80.0 |  |  |
| 4 | `class UserManager {}` | Eksik başlangıç ve bitiş etiketi | Hata: `@startuml etiketi eksik`; `@enduml etiketi eksik` | %60.0 |  |  |
| 5 | `class userManager {}` | PascalCase ihlali | Uyarı: `Sinif isimlendirme kurali ihlali` | %95.0 |  |  |
| 6 | İki kez `class UserManager {}` | Tekrarlanan sınıf adı | Hata: `Tekrar eden sinif ismi`; uyarı: izole sınıf | %75.0 |  |  |
| 7 | İki ilişkisiz sınıf | İzole sınıf | Uyarı: `Izole sinif` | %95.0 |  |  |
| 8 | `Aaaa --> Bbbb` ve `Bbbb --> Aaaa` | Döngüsel bağımlılık | Uyarı: `Dongusel bagimlilik tespit edildi` | %95.0 |  |  |
| 9 | 11 metotlu `HugeService` | God Class | Uyarı: `God Class: sinif cok fazla metot iceriyor (>10)` | %95.0 |  |  |
| 10 | 21 sınıflı diyagram | Karmaşıklık | Uyarı: `Cok fazla sinif`; ayrıca izole sınıf uyarıları | %90.0 |  |  |
| 11 | Eksik `@enduml`, `class badName {}`, `class OtherClass {}` | Karışık hata/uyarı | Hata: eksik bitiş etiketi; uyarı: PascalCase ve izole sınıf | %70.0 |  |  |
| 12 | Duplicate sınıf + döngü | Karışık hata/uyarı | Hata: tekrar eden sınıf; uyarı: döngüsel bağımlılık | %75.0 |  |  |
| 13 | `UserManager --> DiagramService` içeren geçerli basit diyagram | İhlal yok | Hata/uyarı yok | %100.0 |  |  |

## Kullanım Notu

`Zeynep onayı` sütunu elle `Onaylandı`, `Kısmen`, `Reddedildi` gibi kısa bir
etiketle doldurulabilir. `Not` sütununda sistem çıktısının neden doğru veya
tartışmalı olduğu bir cümleyle açıklanmalıdır. Bu tablo tamamlanırsa makalenin
metodoloji/sınırlamalar bölümünde, bağımsız uzman doğrulaması yerine yalnızca
sınırlı bir elle inceleme örneklemi yapıldığı açıkça belirtilmelidir.
