# Data Pipeline

Bu klasor, CURE veri hazirlik ve degerlendirme akislarini kok dizinden ayirir.

- `datasets/`: Ham veya hazirlanmis veri dosyalari.
- `preprocessing/`: XML/CSV donusumu ve veri temizleme scriptleri.
- `vector_db/`: RAG/OCL kural indeksleri icin hazirlik notlari.
- `evaluation/`: Elle degerlendirme, ground truth ve deney kontrol dosyalari.

Kok dizindeki eski `pure_dataset.csv`, `cure_veri_hazirlik.py` ve `xml_to_csv.py`
dosyalari bu yapi altina tasinmistir.
