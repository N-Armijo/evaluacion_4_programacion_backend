<script setup>
import { ref } from 'vue';
import apiClient from '@/services/apiClient';

const form = ref({
  username: '',
  password: '',
});

const error = ref(null);

const loginUser = async () => {
  try {
    const response = await apiClient.post('token/', form.value);
    const token = response.data.access;
    // Guardar el token en localStorage
    localStorage.setItem('access_token', token);
    alert('Inicio de sesión exitoso');
    // Redirigir al dashboard u otra página
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al iniciar sesión';
  }
};
</script>
<template>
    <div class="container mt-4">
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
  

  