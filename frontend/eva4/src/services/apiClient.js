import axios from 'axios';

// Configuración base de Axios
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // URL base de la API Django
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para incluir el token JWT automáticamente
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
