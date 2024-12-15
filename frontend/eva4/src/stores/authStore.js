import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: !!localStorage.getItem('access_token'), // Estado inicial basado en el token
    token: localStorage.getItem('access_token'), // Guardar el token JWT
    isAdmin: false, // Determinado al decodificar el token
  }),
  actions: {
    // Acción para iniciar sesión
    login(token) {
      localStorage.setItem('access_token', token); // Guardar el token
      this.token = token;
      this.isAuthenticated = true; // Actualizar estado
      this.decodeToken(); // Decodificar el token para obtener información adicional
    },
    // Acción para cerrar sesión
    logout() {
      localStorage.removeItem('access_token'); // Eliminar el token
      this.token = null;
      this.isAuthenticated = false; // Actualizar estado
      this.isAdmin = false; // Reiniciar rol
    },
    // Decodificar el token JWT
    decodeToken() {
      if (this.token) {
        try {
          // Decodificar el payload del token
          const payload = JSON.parse(atob(this.token.split('.')[1]));
          console.log('Decoded token:', payload); // Depuración: Verificar las claves del token

          // Verificar si el backend incluye is_superuser
          if ('is_superuser' in payload) {
            this.isAdmin = payload.is_superuser;
          } else {
            console.warn('El token no contiene la clave is_superuser.');
            this.isAdmin = false;
          }
        } catch (error) {
          console.error('Error al decodificar el token:', error);
          this.isAdmin = false; // Asumir que no es admin si falla
        }
      } else {
        console.warn('No hay token disponible para decodificar.');
        this.isAdmin = false;
      }
    },
  },
  getters: {
    // Getter para verificar el estado de admin
    getIsAdmin(state) {
      return state.isAdmin;
    },
    // Getter para el estado de autenticación
    getIsAuthenticated(state) {
      return state.isAuthenticated;
    },
  },
});
