import re

def ocl_dogrula(plantuml_kodu: str) -> dict:
    ihlaller = []
    uyarilar = []
    if "@startuml" not in plantuml_kodu:
        ihlaller.append("KURAL-01: @startuml eksik")
    if "@enduml" not in plantuml_kodu:
        ihlaller.append("KURAL-02: @enduml eksik")
    siniflar = re.findall(r'class\s+(\w+)', plantuml_kodu)
    if len(siniflar) == 0:
        ihlaller.append("KURAL-03: Hic sinif tanimlanmamis")
    bloklar = re.findall(r'class\s+\w+\s*\{([^}]*)\}', plantuml_kodu, re.DOTALL)
    for i, blok in enumerate(bloklar):
        metot = len(re.findall(r'\+\w+\(', blok))
        if metot > 10:
            uyarilar.append(f"UYARI: '{siniflar[i]}' God Class riski ({metot} metot)")
    iliski = len(re.findall(r'--|-->|\.\.>|<\|--', plantuml_kodu))
    if len(siniflar) > 2 and iliski == 0:
        uyarilar.append("UYARI: Siniflar arasi iliski yok")
    skor = max(0.0, round(1.0 - len(ihlaller) * 0.2, 2))
    return {
        "gecerli_mi": len(ihlaller) == 0,
        "skor": skor,
        "ihlaller": ihlaller,
        "uyarilar": uyarilar,
        "sinif_sayisi": len(siniflar)
    }
