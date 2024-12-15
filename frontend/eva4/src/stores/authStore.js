import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: !!localStorage.getItem('access_token'), // Estado inicial basado en el token
  }),
  actions: {
    login(token) {
      localStorage.setItem('access_token', token); // Guardar el token
      this.isAuthenticated = true; // Actualizar estado
    },
    logout() {
      localStorage.removeItem('access_token'); // Eliminar el token
      this.isAuthenticated = false; // Actualizar estado
    },
  },
});
