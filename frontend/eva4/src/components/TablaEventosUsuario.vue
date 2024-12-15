<script setup>
const props = defineProps({
  eventos: Array, // Lista de eventos paginada
  currentPage: Number, // Página actual
  totalPages: Number, // Total de páginas
});

const emit = defineEmits(['inscribirse', 'desinscribirse', 'verDetalles', 'pageChange']);

// Emitir evento para inscribirse
const handleInscribirse = (id) => {
  emit('inscribirse', id);
};

// Emitir evento para desinscribirse
const handleDesinscribirse = (id) => {
  emit('desinscribirse', id);
};

// Emitir evento para ver detalles
const handleVerDetalles = (id) => {
  emit('verDetalles', id);
};

// Cambiar página
const goToPage = (page) => {
  emit('pageChange', page);
};
</script>

<template>
  <div class="col-12 col-md-8 mx-auto">
    <table class="table table-hover text-center table-striped mt-4">
      <thead>
        <tr>
          <th>Título</th>
          <th>Fecha</th>
          <th>Ubicación</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="evento in eventos" :key="evento.id">
          <td>{{ evento.titulo }}</td>
          <td>{{ evento.fecha }}</td>
          <td>{{ evento.ubicacion }}</td>
          <td>
            <!-- Botón de inscribirse -->
            <button class="btn btn-primary btn-sm" @click="handleInscribirse(evento.id)">
              Inscribirse
            </button>

            <!-- Botón de desinscribirse -->
            <button class="btn btn-danger btn-sm ms-2" @click="handleDesinscribirse(evento.id)">
              Desinscribirse
            </button>

            <!-- Botón para ver detalles -->
            <button class="btn btn-info btn-sm ms-2" @click="handleVerDetalles(evento.id)">
              Ver Detalles
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Paginación -->
    <nav v-if="totalPages > 1" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="goToPage(currentPage - 1)">Anterior</button>
        </li>
        <li
          class="page-item"
          v-for="page in totalPages"
          :key="page"
          :class="{ active: currentPage === page }"
        >
          <button class="page-link" @click="goToPage(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="goToPage(currentPage + 1)">Siguiente</button>
        </li>
      </ul>
    </nav>
  </div>
</template>
