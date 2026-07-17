# Iterasyon Limiti Notu

`UMLMultiAgentSystem` icindeki iterasyon limiti artik sabit `3` degeri yerine
`max_iterations` parametresiyle belirlenir. Backend tarafinda
`/api/autonomous-repair` endpoint'ine gelen `max_iterations` alani da bu
parametreye aktarilir.

## Neden varsayilan limit 3?

Varsayilan deger olan `3`, uc pratik riski dengelemek icin korunmustur:

- Token maliyeti: Her dongude Critic ve gerekirse Healer LLM cagrisi yapar.
  Limit artinca maliyet ve kota kullanimi dogrudan artar.
- Sonsuz veya verimsiz dongu riski: LLM ayni hatayi tekrar uretebilir ya da
  Critic/Healer arasinda ilerleme saglanmadan gidip gelebilir.
- Zaman-performans dengesi: `/api/autonomous-repair` kullaniciya donen bir API
  endpoint'idir. Yuksek limitler basari olasiligini artirabilir, fakat SLA ve
  kullanici bekleme suresi uzerinde dogrudan maliyet olusturur.

## Dikkat edilmesi gereken nokta

Bu varsayim henuz deneysel olarak dogrulanmis bir duyarlilik analizi degildir.
Limit `2`, `4` ve `5` icin gercek OpenAI API anahtariyla
`backend/evaluation/iteration_limit_sensitivity_experiment.py` calistirilip CSV sonucu
uretilmeden "3 en iyi degerdir" seklinde kesin bir iddia kurulmamali.
