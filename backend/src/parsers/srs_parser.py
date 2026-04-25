import re

def srs_to_plantuml(srs_metni: str) -> dict:
    temiz = srs_metni.strip()
    sinif_adaylari = re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', temiz)
    siniflar = list(set(sinif_adaylari))[:10]
    satirlar = ["@startuml", ""]
    for s in siniflar:
        satirlar.append(f"class {s} {{")
        satirlar.append("}")
        satirlar.append("")
    satirlar.append("@enduml")
    return {
        "plantuml_kodu": "\n".join(satirlar),
        "bulunan_siniflar": siniflar,
        "sinif_sayisi": len(siniflar)
    }
