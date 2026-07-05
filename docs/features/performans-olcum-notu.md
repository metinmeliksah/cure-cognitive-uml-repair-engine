# Performans Olcum Notu: Tablo IV Latency Kapsami

Bu not, Tablo IV'te raporlanan "50 ardisik analiz istegi" olcumunun hangi
endpoint ve kod yolu uzerinden geldigini aciklar.

## Dogrulanan endpoint

Tablo IV'teki performans olcumu `/api/analyze` endpoint'ine aittir.
`backend/src/api/endpoints.py` icinde `tam_analiz_yap` fonksiyonu su akisi
calistirir:

```python
parse_sonuc = srs_to_plantuml(girdi.metin)
uml = parse_sonuc["plantuml_kodu"]
ocl_sonuc = ocl_dogrula(uml)
eval_sonuc = semantik_sadakat_skoru(girdi.metin, uml)
```

Bu uc fonksiyonun hicbiri LLM cagrisi yapmaz.

## LLM kullanilmadigina dair import kaniti

`backend/src/parsers/srs_parser.py` yalnizca su importlari yapar:

```python
import re
from typing import Optional
```

`backend/src/ocl_engine/ocl_validator.py` yalnizca su importlari yapar:

```python
import re
from typing import Optional
```

`backend/src/evaluators/semantic_eval.py` yalnizca su importlari yapar:

```python
import re
from typing import Optional
```

Bu dosyalarda `OpenAI`, `ChatOpenAI`, `langchain_openai` veya baska bir LLM
istemcisi import edilmez. Dolayisiyla `/api/analyze` latency degeri regex,
deterministik OCL kontrolu ve deterministik semantik skor hesaplamasini kapsar.

## Gercek LLM tabanli onarim nerede?

Gercek LLM tabanli onarim `/api/autonomous-repair` endpoint'indedir.
`backend/src/api/endpoints.py` icinde baslangic compile testi basarisiz olursa:

```python
agent = UMLMultiAgentSystem(max_iterations=girdi.max_iterasyon)
aktif_kod = agent.run(original_text=srs_metni, initial_uml=aktif_kod)
```

Bu sinif `ai_core/src/ai/agent_workflow.py` icinde `ChatOpenAI` kullanir:

```python
from langchain_openai import ChatOpenAI
```

Sonuc: Tablo IV'teki `/api/analyze` olcumu gercek LLM onarimini icermez.
LLM latency'si olculmek isteniyorsa `/api/autonomous-repair` icin ayri deney
calistirilmalidir.
