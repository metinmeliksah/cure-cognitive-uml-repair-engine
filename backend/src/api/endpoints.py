from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import sys, os

# Modülleri import et
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parsers.srs_parser import srs_to_plantuml
from evaluators.semantic_eval import semantik_sadakat_skoru
from ocl_engine.ocl_validator import ocl_dogrula

# FastAPI uygulaması
app = FastAPI(
    title="CURE Backend API",
    description="Cognitive UML Repair Engine - Backend Services",
    version="1.0.0"
)

# CORS ayarı (Metin'in frontend'i farklı porttan bağlanacak)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için herkese açık
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Veri modelleri ──────────────────────────────

class SRSGirdisi(BaseModel):
    metin: str = Field(..., min_length=10, description="SRS belgesi metni")
    dil: str = Field(default="en", description="Metin dili (en/tr)")

class UMLDogrulamaGirdisi(BaseModel):
    plantuml_kodu: str = Field(..., description="Dogrulanacak PlantUML kodu")

class TamAnalizGirdisi(BaseModel):
    srs_metni: str = Field(..., min_length=10, description="SRS metni")
    plantuml_kodu: Optional[str] = Field(None, description="Varsa mevcut PlantUML")

# ── Endpoint'ler ──────────────────────────────

@app.get("/")
def ana_sayfa():
    return {
        "servis": "CURE Backend API",
        "versiyon": "1.0.0",
        "durum": "aktif",
        "endpoints": ["/api/parse", "/api/validate", "/api/evaluate", "/api/analyze", "/health"]
    }

@app.get("/health")
def saglik_kontrolu():
    """Servis sağlık kontrolü."""
    return {"durum": "aktif", "versiyon": "1.0.0"}

@app.post("/api/parse")
def srs_parse_et(girdi: SRSGirdisi):
    """
    SRS metnini PlantUML diyagramına çevirir.
    Girdi: SRS metni
    Çıktı: PlantUML kodu, bulunan sınıflar, ilişkiler
    """
    try:
        sonuc = srs_to_plantuml(girdi.metin)
        if sonuc.get("hata"):
            raise HTTPException(status_code=400, detail=sonuc["hata"])
        return {
            "basarili": True,
            "plantuml_kodu": sonuc["plantuml_kodu"],
            "siniflar": sonuc["bulunan_siniflar"],
            "iliskiler": sonuc["iliskiler"],
            "sinif_sayisi": sonuc["sinif_sayisi"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parser hatasi: {str(e)}")

@app.post("/api/validate")
def uml_dogrula(girdi: UMLDogrulamaGirdisi):
    """
    PlantUML kodunu OCL kurallarına göre doğrular.
    Girdi: PlantUML kodu
    Çıktı: Geçerliliik, hatalar, uyarılar, skor
    """
    try:
        sonuc = ocl_dogrula(girdi.plantuml_kodu)
        return {
            "basarili": True,
            "gecerli_mi": sonuc["gecerli_mi"],
            "skor": sonuc["skor"],
            "yuzde": sonuc["yuzde"],
            "hatalar": sonuc["hatalar"],
            "uyarilar": sonuc["uyarilar"],
            "sinif_sayisi": sonuc["sinif_sayisi"],
            "detaylar": sonuc["detaylar"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCL dogrulama hatasi: {str(e)}")

@app.post("/api/evaluate")
def semantik_degerlendir(girdi: TamAnalizGirdisi):
    """
    SRS metni ile PlantUML'i IEEE/ISO 29148'e göre karşılaştırır.
    Girdi: SRS metni + PlantUML kodu
    Çıktı: Semantik sadakat skoru, halüsinasyonlar, eksik sınıflar
    """
    if not girdi.plantuml_kodu:
        raise HTTPException(
            status_code=400, 
            detail="Degerlendirme icin plantuml_kodu gerekli"
        )
    try:
        sonuc = semantik_sadakat_skoru(girdi.srs_metni, girdi.plantuml_kodu)
        return {
            "basarili": True,
            "genel_skor": sonuc["genel_skor"],
            "yuzde": sonuc["yuzde"],
            "gecti_mi": sonuc["gecti_mi"],
            "halusinasyonlar": sonuc["halusinasyonlar"],
            "eksik_siniflar": sonuc["eksik_siniflar"],
            "ieee_kriterleri": sonuc["ieee_kriterleri"],
            "sinif_metrikleri": sonuc["sinif_metrikleri"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Degerlendirme hatasi: {str(e)}")

@app.post("/api/analyze")
def tam_analiz_yap(girdi: SRSGirdisi):
    """
    Tam pipeline: SRS → UML üret → OCL doğrula → Semantik değerlendir.
    Tek endpoint'te her şeyi yapar.
    """
    try:
        # 1. Parse
        parse_sonuc = srs_to_plantuml(girdi.metin)
        if parse_sonuc.get("hata"):
            raise HTTPException(status_code=400, detail=parse_sonuc["hata"])
        
        uml = parse_sonuc["plantuml_kodu"]
        
        # 2. OCL Doğrula
        ocl_sonuc = ocl_dogrula(uml)
        
        # 3. Semantik Değerlendir
        eval_sonuc = semantik_sadakat_skoru(girdi.metin, uml)
        
        return {
            "basarili": True,
            "uretilen_uml": uml,
            "siniflar": parse_sonuc["bulunan_siniflar"],
            "iliskiler": parse_sonuc["iliskiler"],
            "ocl": {
                "gecerli_mi": ocl_sonuc["gecerli_mi"],
                "skor": ocl_sonuc["skor"],
                "hatalar": ocl_sonuc["hatalar"],
                "uyarilar": ocl_sonuc["uyarilar"]
            },
            "semantik": {
                "genel_skor": eval_sonuc["genel_skor"],
                "yuzde": eval_sonuc["yuzde"],
                "halusinasyonlar": eval_sonuc["halusinasyonlar"],
                "ieee_kriterleri": eval_sonuc["ieee_kriterleri"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analiz hatasi: {str(e)}")
