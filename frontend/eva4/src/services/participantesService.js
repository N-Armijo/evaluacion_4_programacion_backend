import apiClient from './apiClient';

const getParticipantes = async () => {
  return apiClient.get('participantes/');
};

const getParticipante = async (id) => {
  return apiClient.get(`participantes/${id}/`);
};

const createParticipante = async (data) => {
  return apiClient.post('participantes/', data);
};

const updateParticipante = async (id, data) => {
  return apiClient.put(`participantes/${id}/`, data);
};

const deleteParticipante = async (id) => {
  return apiClient.delete(`participantes/${id}/`);
};

export default {
  getParticipantes,
  getParticipante,
  createParticipante,
  updateParticipante,
  deleteParticipante,
};
