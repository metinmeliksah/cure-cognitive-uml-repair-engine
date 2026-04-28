import re
from typing import Optional

# Yazılım gereksinim belgelerinde sık geçen ilişki kalıpları
RELATIONSHIP_PATTERNS = [
    (r'(\w+)\s+(?:uses?|utilizes?)\s+(?:the\s+)?(\w+)', 'uses'),
    (r'(\w+)\s+(?:extends?|inherits?)\s+(?:the\s+)?(\w+)', 'extends'),
    (r'(\w+)\s+(?:implements?)\s+(?:the\s+)?(\w+)', 'implements'),
    (r'(\w+)\s+(?:contains?|has)\s+(?:a|an|one|many|the)?\s*(\w+)', 'has'),
    (r'(\w+)\s+(?:manages?|handles?)\s+(?:the\s+)?(\w+)', 'manages'),
    (r'(\w+)\s+(?:creates?|generates?)\s+(?:the\s+)?(\w+)', 'creates'),
    (r'(\w+)\s+(?:communicates?\s+with|connects?\s+to)\s+(?:the\s+)?(\w+)', 'connects'),
    (r'(\w+)\s+(?:sends?|notifies?)\s+(?:the\s+)?(\w+)', 'sends'),
    (r'(\w+)\s+(?:stores?|retrieves?)\s+(?:the\s+)?(\w+)', 'stores'),
]

# İngilizce stop word listesi (bunlar sınıf adı olamaz)
STOP_WORDS = {
    'the','a','an','is','are','was','were','be','been','being',
    'have','has','had','do','does','did','will','would','could',
    'should','may','might','shall','can','need','must','ought',
    'this','that','these','those','it','its','they','them','their',
    'when','where','which','who','how','what','all','each','every',
    'system','user','data','information','process','function',
    'the','and','or','but','not','with','from','into','onto',
    'shall','must','should','will','can','may','need',
    'uml','api','rest','json','xml','html','css','sql','url',
    'http','https','pdf','csv','srs','ocl','llm','ai','ui','ux',
}

def extract_classes(text: str) -> list:
    """Metinden sınıf adaylarını çıkarır."""
    # Büyük harfle başlayan birleşik isimler (CamelCase veya tekil büyük)
    camel = re.findall(r'\b[A-Z][a-zA-Z]{2,}(?:[A-Z][a-zA-Z]*)?\b', text)
    
    # Yazılım domaininde sınıf olmaya aday isimler
    domain_nouns = re.findall(
        r'\b(manager|controller|service|handler|engine|validator|'
        r'parser|generator|processor|repository|factory|builder|'
        r'monitor|analyzer|evaluator|executor|scheduler)\b',
        text, re.IGNORECASE
    )
    
    # Teknik varlıklar
    tech_entities = re.findall(
        r'\b(database|server|client|interface|module|component|'
        r'subsystem|layer|agent|model|diagram|report|document)\b',
        text, re.IGNORECASE
    )
    
    # Hepsini birleştir ve temizle
    raw = camel + [w.capitalize() for w in domain_nouns + tech_entities]
    
    # Filtrele: stop word değil, en az 3 karakter
    classes = []
    seen = set()
    for c in raw:
        clean = c.strip()
        if (clean.lower() not in STOP_WORDS 
                and len(clean) >= 3 
                and clean not in seen):
            classes.append(clean)
            seen.add(clean)
    
    return classes[:15]  # Maksimum 15 sınıf

def extract_relationships(text: str, classes: list) -> list:
    """Metinden sınıflar arası ilişkileri çıkarır."""
    relationships = []
    class_set = {c.lower() for c in classes}
    
    for pattern, rel_type in RELATIONSHIP_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for src, tgt in matches:
            src_clean = src.strip()
            tgt_clean = tgt.strip()
            # Sınıf listesinde büyük/küçük harf farkı olmadan ara
            src_match = next((c for c in classes if c.lower() == src_clean.lower()), None)
            tgt_match = next((c for c in classes if c.lower() == tgt_clean.lower()), None)
            if not src_match or not tgt_match:
                continue
            src_clean = src_match
            tgt_clean = tgt_match
            if (src_clean.lower() in class_set 
                    and tgt_clean.lower() in class_set
                    and src_clean != tgt_clean):
                rel = {
                    "source": src_clean,
                    "target": tgt_clean,
                    "type": rel_type
                }
                if rel not in relationships:
                    relationships.append(rel)
    
    return relationships

def generate_plantuml(classes: list, relationships: list) -> str:
    """Sınıf ve ilişkilerden PlantUML kodu üretir."""
    lines = ["@startuml", "skinparam classAttributeIconSize 0", ""]
    
    # Sınıf tanımları
    for cls in classes:
        lines.append(f"class {cls} {{")
        lines.append("}")
        lines.append("")
    
    # İlişkiler
    if relationships:
        lines.append("' Iliskiler")
        for rel in relationships:
            if rel["type"] in ("extends", "implements"):
                lines.append(f'{rel["source"]} --|> {rel["target"]}')
            elif rel["type"] == "has":
                lines.append(f'{rel["source"]} *-- {rel["target"]}')
            else:
                lines.append(f'{rel["source"]} --> {rel["target"]}')
    
    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)

def srs_to_plantuml(srs_metni: str) -> dict:
    """
    Ana fonksiyon: SRS metnini PlantUML diyagramına çevirir.
    
    Girdi:
        srs_metni (str): Doğal dil yazılım gereksinim belgesi
    
    Çıktı:
        dict:
            plantuml_kodu    : str  - Üretilen PlantUML kodu
            bulunan_siniflar : list - Tespit edilen sınıf adları
            iliskiler        : list - Tespit edilen ilişkiler
            sinif_sayisi     : int  - Toplam sınıf sayısı
            hata             : str|None - Hata varsa açıklama
    """
    if not srs_metni or len(srs_metni.strip()) < 10:
        return {
            "plantuml_kodu": "@startuml\n@enduml",
            "bulunan_siniflar": [],
            "iliskiler": [],
            "sinif_sayisi": 0,
            "hata": "Metin çok kısa veya boş"
        }
    
    try:
        classes = extract_classes(srs_metni)
        relationships = extract_relationships(srs_metni, classes)
        plantuml = generate_plantuml(classes, relationships)
        
        return {
            "plantuml_kodu": plantuml,
            "bulunan_siniflar": classes,
            "iliskiler": relationships,
            "sinif_sayisi": len(classes),
            "hata": None
        }
    except Exception as e:
        return {
            "plantuml_kodu": "@startuml\n@enduml",
            "bulunan_siniflar": [],
            "iliskiler": [],
            "sinif_sayisi": 0,
            "hata": str(e)
        }


if __name__ == "__main__":
    test_srs = """
    The UserManager handles user authentication and registration.
    The DiagramService generates PlantUML diagrams from SRS documents.
    The ValidationEngine validates diagrams against OCL constraints.
    The ReportGenerator creates PDF reports from evaluation results.
    The UserManager uses the DiagramService to process uploaded documents.
    The ValidationEngine extends the base Validator component.
    """
    result = srs_to_plantuml(test_srs)
    print("=== Bulunan Siniflar ===")
    print(result["bulunan_siniflar"])
    print("\n=== Iliskiler ===")
    print(result["iliskiler"])
    print("\n=== PlantUML Kodu ===")
    print(result["plantuml_kodu"])
