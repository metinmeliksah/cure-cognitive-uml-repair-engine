import re
from typing import Optional

def extract_srs_entities(srs_metni: str) -> dict:
    """SRS metninden varlıkları çıkarır."""
    # Sınıf adayları (CamelCase)
    siniflar = set(re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', srs_metni))
    
    # Stop words temizle
    stop = {'The','This','These','That','When','Where','Which','Each',
            'All','Any','Some','Both','For','And','But','Or','Not',
            'With','From','Into','Upon','After','Before'}
    siniflar = {s for s in siniflar if s not in stop and len(s) > 3}
    
    # İlişki kalıpları
    iliski_patterns = [
        r'\b(\w+)\s+uses?\s+(\w+)\b',
        r'\b(\w+)\s+manages?\s+(\w+)\b',
        r'\b(\w+)\s+extends?\s+(\w+)\b',
        r'\b(\w+)\s+contains?\s+(\w+)\b',
        r'\b(\w+)\s+handles?\s+(\w+)\b',
    ]
    iliskiler = set()
    for pat in iliski_patterns:
        for src, tgt in re.findall(pat, srs_metni, re.IGNORECASE):
            iliskiler.add((src.capitalize(), tgt.capitalize()))
    
    return {"siniflar": siniflar, "iliskiler": iliskiler}

def extract_uml_entities(plantuml_kodu: str) -> dict:
    """PlantUML kodundan varlıkları çıkarır."""
    # Tanımlı sınıflar
    siniflar = set(re.findall(r'class\s+(\w+)', plantuml_kodu))
    
    # Interface tanımları
    interfaceler = set(re.findall(r'interface\s+(\w+)', plantuml_kodu))
    tum_siniflar = siniflar | interfaceler
    
    # İlişkiler
    iliski_patterns = [
        r'(\w+)\s*-->\s*(\w+)',    # association
        r'(\w+)\s*\*--\s*(\w+)',   # composition
        r'(\w+)\s*o--\s*(\w+)',    # aggregation
        r'(\w+)\s*\|>\s*(\w+)',    # inheritance
        r'(\w+)\s*\.\.\>\s*(\w+)', # dependency
    ]
    iliskiler = set()
    for pat in iliski_patterns:
        for src, tgt in re.findall(pat, plantuml_kodu):
            iliskiler.add((src, tgt))
    
    return {"siniflar": tum_siniflar, "iliskiler": iliskiler}

def hesapla_f1(tahmin: set, gercek: set) -> dict:
    """Precision, Recall ve F1 skoru hesaplar."""
    if not gercek and not tahmin:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    if not gercek:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    
    # Büyük/küçük harf farkını görmezden gel
    tahmin_lower = {t.lower() for t in tahmin}
    gercek_lower = {g.lower() for g in gercek}
    
    kesisim = len(tahmin_lower & gercek_lower)
    precision = kesisim / len(tahmin_lower) if tahmin_lower else 0.0
    recall = kesisim / len(gercek_lower) if gercek_lower else 0.0
    f1 = (2 * precision * recall / (precision + recall) 
          if (precision + recall) > 0 else 0.0)
    
    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3)
    }

def semantik_sadakat_skoru(srs_metni: str, plantuml_kodu: str) -> dict:
    """
    IEEE/ISO 29148 standartlarına göre semantik sadakat değerlendirmesi.
    
    Girdi:
        srs_metni    (str): Orijinal gereksinim belgesi
        plantuml_kodu (str): Değerlendirilecek PlantUML diyagramı
    
    Çıktı:
        dict:
            genel_skor       : float (0.0-1.0)
            yuzde            : str   ("%85.0" formatında)
            sinif_metrikleri : dict  (precision, recall, f1)
            iliski_metrikleri: dict  (precision, recall, f1)
            halusinasyonlar  : list  (UML'de var, SRS'de yok)
            eksik_siniflar   : list  (SRS'de var, UML'de yok)
            ieee_kriterleri  : dict  (her kriter için ayrı skor)
            gecti_mi         : bool  (hedef: %90 üzeri)
    """
    srs_varlik = extract_srs_entities(srs_metni)
    uml_varlik = extract_uml_entities(plantuml_kodu)
    
    srs_siniflar = srs_varlik["siniflar"]
    uml_siniflar = uml_varlik["siniflar"]
    
    # Metrikler
    sinif_metrik = hesapla_f1(uml_siniflar, srs_siniflar)
    iliski_metrik = hesapla_f1(uml_varlik["iliskiler"], srs_varlik["iliskiler"])
    
    # Halüsinasyon tespiti: UML'de var ama SRS'de yok
    uml_lower = {u.lower(): u for u in uml_siniflar}
    srs_lower = {s.lower() for s in srs_siniflar}
    halusinasyonlar = [uml_lower[u] for u in uml_lower if u not in srs_lower]
    
    # Eksik sınıflar: SRS'de var ama UML'de yok
    eksik = [s for s in srs_siniflar if s.lower() not in uml_lower]
    
    # IEEE/ISO 29148 kriterleri
    # C1: Sınıf doğruluğu (class correctness)
    # C2: İlişki doğruluğu (relationship correctness)  
    # C3: Bütünlük (completeness) - eksik varlık yok mu?
    # C4: Tutarlılık (consistency) - halüsinasyon yok mu?
    c1 = sinif_metrik["f1"]
    c2 = iliski_metrik["f1"] if srs_varlik["iliskiler"] else 1.0
    c3 = 1.0 - (len(eksik) / len(srs_siniflar)) if srs_siniflar else 1.0
    c4 = 1.0 - (len(halusinasyonlar) / len(uml_siniflar)) if uml_siniflar else 1.0
    
    # Ağırlıklı genel skor
    genel_skor = round((c1 * 0.35) + (c2 * 0.25) + (c3 * 0.25) + (c4 * 0.15), 3)
    
    return {
        "genel_skor": genel_skor,
        "yuzde": f"%{round(genel_skor * 100, 1)}",
        "sinif_metrikleri": sinif_metrik,
        "iliski_metrikleri": iliski_metrik,
        "halusinasyonlar": halusinasyonlar,
        "eksik_siniflar": eksik,
        "ieee_kriterleri": {
            "C1_sinif_dogrulugu": round(c1, 3),
            "C2_iliski_dogrulugu": round(c2, 3),
            "C3_butunluk": round(c3, 3),
            "C4_tutarlilik": round(c4, 3)
        },
        "gecti_mi": genel_skor >= 0.90
    }


if __name__ == "__main__":
    srs = """
    The UserManager handles user authentication.
    The DiagramService generates PlantUML diagrams.
    The ValidationEngine validates diagrams.
    The UserManager uses the DiagramService.
    """
    uml = """
    @startuml
    class UserManager {}
    class DiagramService {}
    class ValidationEngine {}
    class FakeHallucinatedClass {}
    UserManager --> DiagramService
    @enduml
    """
    r = semantik_sadakat_skoru(srs, uml)
    print(f"Genel Skor: {r['yuzde']}")
    print(f"Halüsinasyonlar: {r['halusinasyonlar']}")
    print(f"Eksik Sınıflar: {r['eksik_siniflar']}")
    print(f"IEEE Kriterleri: {r['ieee_kriterleri']}")
