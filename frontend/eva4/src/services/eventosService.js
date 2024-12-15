import apiClient from './apiClient';

const getEventos = async () => {
  return apiClient.get('eventos/');
};

const getEvento = async (id) => {
  return apiClient.get(`eventos/${id}/`);
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
  getEvento,
  createEvento,
  updateEvento,
  deleteEvento,
};
