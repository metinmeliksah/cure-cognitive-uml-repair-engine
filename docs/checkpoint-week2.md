# 📌 Checkpoint --- Hafta 2

## Ajanların (Agents) Geliştirilmesi ve RAG Entegrasyonu

- **Hafta:** 2
- **Sprint Hedefi:** Eleştirmen (Critic) ve Onarıcı (Healer) yapay zeka
ajanlarını oluşturmak ve RAG altyapısını sisteme entegre etmek

- **Durum:** 🔴 Başlanmadı
- **Görev Başlangıç Tarihi:** 10.04.2026
- **Görev Bitiş Tarihi:** 20.04.2026
- **Vize haftası sebebiyle 10 gün teslim süresi uygulanmıştır. Checkpoint 3 başlangıç tarihi etkilenmeyecektir.**
------------------------------------------------------------------------

# 🎯 Genel Hedefler

-   [ ] Critic (Eleştirmen) ajanı oluşturuldu\
-   [ ] Healer (Onarıcı) ajanı oluşturuldu\
-   [ ] Ajanlar arası iletişim mantığı kuruldu\
-   [ ] RAG altyapısı kuruldu\
-   [ ] Vektör veritabanı hazır\
-   [ ] Hata log sistemi çalışıyor\
-   [ ] Frontend hata gösterim ekranı hazır\
-   [ ] JSON hata parser sistemi hazır

------------------------------------------------------------------------

# 👥 Görev Dağılımı ve Detaylı İş Listesi

------------------------------------------------------------------------

# Metin Melikşah Dermencioğlu

## Sorumluluk: Hata uyarıları ve görsel geri bildirim sistemi oluşturmak

  -------------------------------------------------------------------------
  Görev         Açıklama               Sorumlu                Durum
  ------------- ---------------------- ---------------------- -------------
  Hata log      Halüsinasyon ve Design Frontend               [ ]
  ekranı        Smell uyarıları                               
  tasarlama                                                   

  UI hata       Hata mesajlarını       Frontend               [ ]
  listesi       listeleme                                     
  oluşturma                                                   

  Diyagram hata Hatalı alanları        Frontend               [ ]
  vurgulama     kırmızı renkle                                
                gösterme                                      

  Tooltip       Hata detayını hover    Frontend               [ ]
  sistemi       ile gösterme                                  

  Status badge  Hata türü göstergeleri Frontend               [ ]
  sistemi                                                     

  Log panel     Hata geçmişi ekranı    Frontend               [ ]
  bileşeni                                                    

  API hata      Backend'den gelen      Frontend               [ ]
  verisi        JSON'u UI'da gösterme                         
  gösterme                                                    

  Responsive    Mobil uyumlu hata      Frontend               [ ]
  tasarım       ekranı                                        

  Branch        Feature branch         Scrum Master           [ ]
  yönetimi      kullanımı                                     
  kontrolü                                                    
  -------------------------------------------------------------------------

------------------------------------------------------------------------

# Buğrahan Gökkaya

## Sorumluluk: Multi-agent sistemi geliştirmek

  ---------------------------------------------------------------------------
  Görev           Açıklama               Sorumlu                Durum
  --------------- ---------------------- ---------------------- -------------
  LangGraph ajan  Critic node oluşturma  AI Developer           [ ]
  tanımı                                                        

  Healer ajan     Onarıcı node oluşturma AI Developer           [ ]
  tanımı                                                        

  Ajan mesajlaşma Agent-to-agent         AI Developer           [ ]
  sistemi         communication                                 

  Edge mantığı    Workflow geçiş         AI Developer           [ ]
  kodlama         kuralları                                     

  Halüsinasyon    UML doğrulama promptu  AI Developer           [ ]
  tespit promptu                                                

  Onarım promptu  Hatalı UML düzeltme    AI Developer           [ ]

  Multi-agent     Sistem testleri        AI Developer           [ ]
  workflow test                                                 

  Logging         Agent çıktı loglama    AI Developer           [ ]
  entegrasyonu                                                  

  Hata            Error type             AI Developer           [ ]
  sınıflandırma   categorization                                
  ---------------------------------------------------------------------------

------------------------------------------------------------------------

# Zeynep Karataş

## Sorumluluk: Hata işleme ve doğrulama mekanizmaları

  Görev                     Açıklama                     Sorumlu   Durum
  ------------------------- ---------------------------- --------- -------
  JSON parser geliştirme    AI hata raporu ayrıştırma    Backend   [ ]
  Error response handler    Hata mesajı işleme           Backend   [ ]
  Try-catch mekanizması     Syntax hatalarını yakalama   Backend   [ ]
  PlantUML syntax kontrol   UML doğrulama                Backend   [ ]
  Error log sistemi         Hata kayıt mekanizması       Backend   [ ]
  Exception logging         Runtime hata kaydı           Backend   [ ]
  API hata endpoint         /error-log endpoint          Backend   [ ]
  Unit test yazımı          Parser testleri              Test      [ ]
  Integration test          Agent + API testleri         Test      [ ]

------------------------------------------------------------------------

# Aydın Doğan

## Sorumluluk: Vektör veritabanı ve RAG altyapısı

  --------------------------------------------------------------------------
  Görev          Açıklama               Sorumlu                Durum
  -------------- ---------------------- ---------------------- -------------
  Vektör         ChromaDB veya FAISS    Data Specialist        [ ]
  veritabanı                                                   
  kurulumu                                                     

  Veri klasörü   vector_db dizini       Data Specialist        [ ]
  oluşturma                                                    

  OCL            Metin parçalama        Data Specialist        [ ]
  kurallarını                                                  
  chunking                                                     

  Embedding      Vektör dönüşümü        Data Specialist        [ ]
  oluşturma                                                    

  Vector index   Arama indeksleme       Data Specialist        [ ]
  oluşturma                                                    

  RAG retrieval  Semantic search        Data Specialist        [ ]
  fonksiyonu                                                   

  Veri doğrulama Retrieval accuracy     Data Specialist        [ ]
  testleri       test                                          

  Dataset        Veri yönetimi          Data Specialist        [ ]
  versiyonlama                                                 

  RAG performans Query latency ölçümü   Data Specialist        [ ]
  ölçümü                                                       
  --------------------------------------------------------------------------

------------------------------------------------------------------------

# 📦 Teknik Teslimatlar (Deliverables)

  Teslimat         Açıklama                  Durum
  ---------------- ------------------------- -------
  Critic Agent     Hata tespit sistemi       [ ]
  Healer Agent     Otomatik onarım sistemi   [ ]
  RAG altyapısı    Vektör arama sistemi      [ ]
  Error parser     JSON hata ayrıştırma      [ ]
  Log sistemi      Hata kayıt mekanizması    [ ]
  UI hata paneli   Frontend hata ekranı      [ ]

------------------------------------------------------------------------

# 📈 Haftalık Başarı Kriterleri

-   [ ] Critic agent çalışıyor\
-   [ ] Healer agent çalışıyor\
-   [ ] RAG arama sistemi çalışıyor\
-   [ ] Hata raporları görüntüleniyor\
-   [ ] UML hataları yakalanıyor\
-   [ ] Sistem log üretiyor

------------------------------------------------------------------------

# 📝 Notlar

-   Tüm geliştirmeler branch üzerinde yapılacaktır\
-   Pull Request zorunludur\
-   Kod review yapılmadan merge edilmez\
-   Her görev tamamlandığında checkbox işaretlenecektir
