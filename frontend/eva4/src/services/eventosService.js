import apiClient from './apiClient';

// Cambiar para aceptar un objeto con parámetros (e.g., { page: 1, categoria: 2, fecha: '2024-12-16' })
const getEventos = async (params) => {
  return apiClient.get('eventos/', { params }); // Axios maneja automáticamente los parámetros
};

const createEvento = async (data) => {
  return apiClient.post('eventos/', data);
};

const updateEvento = async (id, data) => {
  return apiClient.put(`eventos/${id}/`, data);
};

const deleteEvento = async (id) => {
  return apiClient.delete(`eventos/${id}/`);
};

export default {
  getEventos,
  createEvento,
  updateEvento,
  deleteEvento,
};
