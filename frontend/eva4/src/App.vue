<!-- <script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style> -->
<template>
  <div>
    <h1>Lista de Eventos</h1>
    <ul>
      <li v-for="evento in eventos" :key="evento.id">
        {{ evento.titulo }} - {{ evento.fecha }}
      </li>
    </ul>
    <p v-if="error" style="color: red;">Error: {{ error }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import eventosService from './services/eventosService';

export default {
  setup() {
    const eventos = ref([]); // Lista de eventos reactiva
    const error = ref(null); // Para manejar errores

    const fetchEventos = async () => {
      try {
        const response = await eventosService.getEventos();
        eventos.value = response.data.results || response.data; // Manejar paginación si existe
      } catch (err) {
        error.value = err.message;
      }
    };

    // Llama a fetchEventos cuando el componente se monta
    onMounted(() => {
      fetchEventos();
    });

    return {
      eventos,
      error,
    };
  },
};
</script>
