<script setup>
defineProps({
  participantes: Array, // Lista de participantes
});

const emit = defineEmits(['editParticipante', 'deleteParticipante']);

// Emitir evento para editar un participante
const handleEdit = (participante) => {
  emit('editParticipante', participante);
};

// Emitir evento para eliminar un participante
const handleDelete = (id) => {
  emit('deleteParticipante', id);
};
</script>

<template>
  <div class="col-12 col-md-8 mx-auto">
    <table class="table table-hover text-center table-striped mt-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Correo</th>
          <th>Nombre</th>
          <th>Evento</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="participante in participantes" :key="participante.id">
          <td>{{ participante.id }}</td>
          <td>{{ participante.correo }}</td>
          <td>{{ participante.nombre }}</td>
          <td>{{ participante.evento }}</td>
          <td>
            <!-- Botón de Actualizar -->
            <button
              class="btn btn-warning btn-sm text-dark"
              @click="handleEdit(participante)"
            >
              Actualizar
            </button>

            <!-- Botón de Eliminar -->
            <button
              class="btn btn-danger btn-sm ms-2"
              @click="handleDelete(participante.id)"
            >
              Eliminar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
