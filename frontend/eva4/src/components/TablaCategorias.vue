<script setup>
defineProps({
  categorias: Array,
});

const emit = defineEmits(['editCategoria', 'deleteCategoria']);

const handleEdit = (categoria) => {
  emit('editCategoria', categoria);
};

const handleDelete = (id) => {
  if (confirm('¿Estás seguro de eliminar esta categoría?')) {
    emit('deleteCategoria', id);
  }
};
</script>

<template>
  <div class="col-12 col-md-6 mx-auto">
    <table class="table table-hover text-center table-striped mt-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="categoria in categorias" :key="categoria.id">
          <td>{{ categoria.id }}</td>
          <td>{{ categoria.nombre }}</td>
          <td>
            <button
              class="btn btn-warning btn-sm text-dark"
              @click="handleEdit(categoria)"
            >
              Actualizar
            </button>
            <button
              class="btn btn-danger btn-sm ms-2"
              @click="handleDelete(categoria.id)"
            >
              Eliminar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
