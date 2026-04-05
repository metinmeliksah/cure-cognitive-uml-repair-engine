import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

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

export const uploadFile = async (srsFile, existingUmlFile = null) => {
  const formData = new FormData();
  formData.append('file', srsFile);
  if (existingUmlFile) {
    formData.append('existing_uml', existingUmlFile);
  }

  try {
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Dosya yüklenirken bir hata oluştu');
  }
};

export const processDocument = async (fileId) => {
  try {
    const response = await api.post(`/process/${fileId}`);
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Belge işlenirken bir hata oluştu');
  }
};

export const getResults = async (jobId) => {
  try {
    const response = await api.get(`/results/${jobId}`);
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Sonuçlar alınırken bir hata oluştu');
  }
};

export default api;
