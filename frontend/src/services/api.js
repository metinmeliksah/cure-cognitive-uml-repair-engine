import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function getErrorMessage(error, fallback) {
  const data = error.response?.data;
  if (!data) return fallback;
  if (typeof data.message === 'string') return data.message;
  if (typeof data.detail === 'string') return data.detail;
  if (Array.isArray(data.detail) && data.detail[0]?.msg) {
    return data.detail.map((d) => d.msg).join(' ');
  }
  return fallback;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 1. Sadece Parse (UML Üretimi) ve Doğrulama
export const parseDocument = async (metin, dil = "en") => {
  try {
    const response = await api.post('/api/parse', { metin, dil });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Metin işlenirken bir hata oluştu');
  }
};

// 2. Tam Analiz (Parse + OCL + Semantik Değerlendirme)
export const analyzeDocument = async (metin, dil = "en") => {
  try {
    const response = await api.post('/api/analyze', { metin, dil });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Tam analiz yapılırken bir hata oluştu');
  }
};

// 3. Otonom Onarım Döngüsü (Healer)
export const autonomousRepair = async (plantuml_kodu, srs_metni = null, max_iterasyon = 3) => {
  try {
    const response = await api.post('/api/autonomous-repair', { 
        plantuml_kodu, 
        srs_metni,
        max_iterasyon
    });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Otonom onarım sırasında bir hata oluştu');
  }
};

export default api;