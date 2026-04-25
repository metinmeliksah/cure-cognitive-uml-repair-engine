from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CURE Backend API", version="0.1.0")

class SRSGirdi(BaseModel):
    metin: str
    dil: str = "en"

@app.post("/api/parse")
def srs_analiz_et(girdi: SRSGirdi):
    if len(girdi.metin.strip()) < 10:
        raise HTTPException(status_code=400, detail="Metin cok kisa")
    return {
        "mesaj": "Parser hazir",
        "metin_uzunlugu": len(girdi.metin),
        "durum": "basarili"
    }

@app.get("/health")
def saglik():
    return {"durum": "aktif", "versiyon": "0.1.0"}
