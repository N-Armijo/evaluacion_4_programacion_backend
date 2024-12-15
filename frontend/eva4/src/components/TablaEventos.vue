<script setup>
const props = defineProps({
  eventos: Array,
  currentPage: Number,
  totalPages: Number,
});
const emit = defineEmits(['editEvento', 'deleteEvento', 'pageChange']);

const handleEdit = (evento) => {
  emit('editEvento', evento);
};

const handleDelete = (id) => {
  emit('deleteEvento', id);
};

const goToPage = (page) => {
  emit('pageChange', page);
};
</script>

<template>
  <div class="col-12 col-md-8 mx-auto">
    <table class="table table-hover text-center table-striped mt-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Título</th>
          <th>Fecha</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="evento in eventos" :key="evento.id">
          <td>{{ evento.id }}</td>
          <td>{{ evento.titulo }}</td>
          <td>{{ evento.fecha }}</td>
          <td>
            <button class="btn btn-warning btn-sm" @click="handleEdit(evento)">Actualizar</button>
            <button class="btn btn-danger btn-sm ms-2" @click="handleDelete(evento.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
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