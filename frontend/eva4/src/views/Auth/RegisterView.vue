<script setup>
import { ref } from 'vue';
import apiClient from '@/services/apiClient';

const form = ref({
  username: '',
  email: '',
  password: '',
});

const error = ref(null);

const registerUser = async () => {
  try {
    await apiClient.post('register/', form.value);
    alert('Usuario registrado con éxito');
    // Redirigir al inicio de sesión (opcional)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al registrar el usuario';
  }
};
</script>
<template>
    <div class="container mt-4">
      <h2>Registro de Usuario</h2>
      <form @submit.prevent="registerUser">
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
          <label for="email" class="form-label">Correo Electrónico</label>
          <input
            type="email"
            id="email"
            v-model="form.email"
            class="form-control"
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
        <button type="submit" class="btn btn-primary">Registrar</button>
      </form>
      <p v-if="error" class="text-danger mt-2">Error: {{ error }}</p>
    </div>
  </template>
  

  