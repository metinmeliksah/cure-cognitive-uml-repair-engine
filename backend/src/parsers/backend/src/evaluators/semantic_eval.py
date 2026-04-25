import re

def semantik_sadakat_skoru(srs_metni: str, plantuml_kodu: str) -> dict:
    srs_siniflar = set(re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', srs_metni))
    uml_siniflar = set(re.findall(r'class\s+(\w+)', plantuml_kodu))
    eslesen = srs_siniflar & uml_siniflar
    halusinasyon = uml_siniflar - srs_siniflar
    skor = round(len(eslesen) / len(srs_siniflar), 2) if srs_siniflar else 0.0
    return {
        "skor": skor,
        "yuzde": f"%{round(skor*100,1)}",
        "eslesen": list(eslesen),
        "halusinasyon": list(halusinasyon),
        "gecti_mi": skor >= 0.90
    }
