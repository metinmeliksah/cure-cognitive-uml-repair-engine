# Ground Truth Manual Review

13 ornek icin manuel kontrol tablosu. `Zeynep onayi` sutunu dolduruldu; ileride
deney CSV/JSON sonuclariyla karsilastirma icin bu tablo referans alinabilir.

| # | Senaryo | Beklenen sonuc | Zeynep onayi | Not |
|---|---|---|---|---|
| 1 | Eksik @startuml | Onarilmali | Onaylandi | Basit healer etiketi ekleyebilir. |
| 2 | Eksik @enduml | Onarilmali | Onaylandi | Kapanis etiketi eklenmeli. |
| 3 | Bos diyagram | Onarilmali | Onaylandi | Minimum sinif uretilmeli. |
| 4 | PascalCase olmayan sinif | Uyari/Hata | Onaylandi | OCL validator yakalamali. |
| 5 | Tekrarlanan sinif | Hata | Onaylandi | Duplicate class tespiti gerekir. |
| 6 | Izole sinif | Uyari | Onaylandi | OCL uyari olarak raporlayabilir. |
| 7 | God Class | Uyari | Onaylandi | Asiri sorumluluk bildirilmeli. |
| 8 | Dairesel bagimlilik | Uyari/Hata | Onaylandi | Iliski grafigi kontrol edilmeli. |
| 9 | Gecerli tek sinif | Basarili | Onaylandi | Compile ve render gecmeli. |
| 10 | Gecerli iliskili diyagram | Basarili | Onaylandi | OCL skoru yuksek olmali. |
| 11 | SRS-UML eksik sinif | Semantik dusuk | Onaylandi | Eksik sinif listelenmeli. |
| 12 | SRS disi halusinasyon sinif | Semantik dusuk | Onaylandi | Halusinasyon raporlanmali. |
| 13 | Otonom repair final akisi | Tekrar test edilebilir | Onaylandi | Deney scripti sonuc dosyasi uretmeli. |
