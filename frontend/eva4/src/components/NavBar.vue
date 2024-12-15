<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = () => {
  localStorage.removeItem('access_token'); // Eliminar token
  alert('Sesión cerrada con éxito');
  router.push('/login'); // Redirigir al inicio de sesión
};
</script>
<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary sticky-top">
    <div class="container-fluid">
      <RouterLink to="/" class="d-inline-block align-text-top navbar-brand">
        <img
          src="@/assets/logo.svg"
          alt="Logo"
          width="30"
          height="24"
          class="d-inline-block align-text-top"
        />
        Evaluacion 4
      </RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse d-flex justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <RouterLink to="/" active-class="active" class="nav-link">Home</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/eventos" active-class="active" class="nav-link"
              >Eventos</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink to="/categorias" active-class="active" class="nav-link">Categorias</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/participantes" active-class="active" class="nav-link">Participantes</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/register" active-class="active" class="nav-link">Registrarse</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/login" active-class="active" class="nav-link">Iniciar Sesion</RouterLink>
          </li>
          <li class="nav-item">
            <button class="btn btn-danger" @click="logout">Cerrar Sesión</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<style scoped lang="scss">
.navbar {
  a {
    font-weight: bold;
    color: #012e5b;

    &.active {
      color: #f59619;
    }
  }
}
</style>