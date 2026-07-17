# Autonomous Repair

## Aciklama

`POST /api/autonomous-repair`, hatali PlantUML kodunu compile/OCL testinden
gecirir, hata varsa AI ajanla veya deterministik fallback healer ile onarim
dener, final compile ve opsiyonel semantik sonucu dondurur.

## Amac

Makaledeki onarim basari oraninin endpoint uzerinden tekrar uretilebilir ve
olculebilir hale gelmesi.

## Kurulum

```bash
pip install -r backend/requirements.txt
pip install -r ai_core/requirements.txt
```

## Konfigurasyon

`max_iterations` request govdesinden gelir ve 1-5 arasinda sinirlanir.

## Kullanim

```bash
curl -X POST http://localhost:8000/api/autonomous-repair \
  -H "Content-Type: application/json" \
  -d "{\"plantuml_kodu\":\"class UserManager {}\",\"max_iterations\":1}"
```

## Bagimliliklar

- Backend compile/OCL validator
- AI core Critic-Healer workflow
- PlantUML renderer

## Dosya Yapisi

- `backend/src/api/endpoints.py`
- `ai_core/src/ai/agent_workflow.py`
- `experiments/run_autonomous_repair.py`

## API

Endpoint: `POST /api/autonomous-repair`

Request:

```json
{
  "plantuml_kodu": "class UserManager {}",
  "srs_metni": "The UserManager handles authentication.",
  "max_iterations": 1
}
```

Response ana alanlari:

```json
{
  "basarili": true,
  "max_iterations": 1,
  "iterasyonlar": [],
  "final_plantuml": "@startuml...",
  "final_compile": {}
}
```

## Veritabani Degisiklikleri

Yok.

## Test

```bash
python backend/tests/test_api_contracts.py
python experiments/run_autonomous_repair.py --max-iterations 1
```

## Hata Senaryolari

- AI ajan import edilemezse fallback healer devreye girer.
- Final compile basarisizsa hata log endpointine kayit eklenir.

## Gelistiren

Isim: CURE Team
Tarih: 2026-07-02

## Degisiklik Gecmisi

v1.0 - Autonomous repair dokumantasyonu eklendi.
