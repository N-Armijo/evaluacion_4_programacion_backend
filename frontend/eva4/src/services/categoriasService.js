import apiClient from './apiClient';

// const getCategorias = async () => {
//   return apiClient.get('categorias/');
// };

const getCategorias = async (params = {}) => {
  return apiClient.get('categorias/', { params });
};


const getCategoria = async (id) => {
  return apiClient.get(`categorias/${id}/`);
};

const createCategoria = async (data) => {
  return apiClient.post('categorias/', data);
};

const updateCategoria = async (id, data) => {
  return apiClient.put(`categorias/${id}/`, data);
};

const deleteCategoria = async (id) => {
  return apiClient.delete(`categorias/${id}/`);
};

export default {
  getCategorias,
  getCategoria,
  createCategoria,
  updateCategoria,
  deleteCategoria,
};
