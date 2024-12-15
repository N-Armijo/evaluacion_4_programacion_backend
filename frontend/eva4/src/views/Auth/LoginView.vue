<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore'; // Importar el store de autenticación
import apiClient from '@/services/apiClient';

const router = useRouter(); // Manejar redirecciones
const authStore = useAuthStore(); // Usar el store para manejar autenticación

const form = ref({
  username: '',
  password: '',
});

const error = ref(null);

const loginUser = async () => {
  try {
    // Enviar solicitud de autenticación al backend
    const response = await apiClient.post('token/', form.value);

    // Obtener el token de la respuesta
    const token = response.data.access;

    // Actualizar el estado de autenticación usando el store
    authStore.login(token);

    alert('Inicio de sesión exitoso');

    // Redirigir a la página de inicio
    router.push('/');
  } catch (err) {
    // Manejo de errores
    error.value = err.response?.data?.detail || 'Error al iniciar sesión';
  }
};
</script>

<template>
  <div class="col-12 col-md-3 mx-auto mt-4">
    <h2>Inicio de Sesión</h2>
    <form @submit.prevent="loginUser">
      <div class="mb-3">
        <label for="username" class="form-label">Nombre de Usuario</label>
        <input
          type="text"
          id="username"
          v-model="form.username"
          class="form-control"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Contraseña</label>
        <input
          type="password"
          id="password"
          v-model="form.password"
          class="form-control"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Iniciar Sesión</button>
    </form>
    <p v-if="error" class="text-danger mt-2">Error: {{ error }}</p>
  </div>
</template>
