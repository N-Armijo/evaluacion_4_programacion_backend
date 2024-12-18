import apiClient from './apiClient';

const getUsuarios = async () => {
  return apiClient.get('usuarios/'); 
};

export default {
  getUsuarios,
};
