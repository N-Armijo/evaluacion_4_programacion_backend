<script setup>
const props = defineProps({
  participantes: Array, // Lista de participantes
});

const emit = defineEmits(['editParticipante', 'deleteParticipante']);

const editParticipante = (participante) => {
  emit('editParticipante', participante);
};

const deleteParticipante = (id) => {
  if (confirm('¿Estás seguro de que deseas eliminar este participante?')) {
    emit('deleteParticipante', id);
  }
};
</script>

<template>
  <div class="col-12 col-md-8 mx-auto">
    <h4 class="mt-3">Lista de Participantes</h4>
    <table class="table table-hover text-center table-striped mt-4">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Correo Electrónico</th>
          <th>Evento</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="participante in participantes" :key="participante.id">
          <td>{{ participante.nombre }}</td>
          <td>{{ participante.correo }}</td>
          <td>{{ participante.evento }}</td>
          <td>
            <button
              class="btn btn-warning btn-sm text-dark"
              @click="editParticipante(participante)"
            >
              Editar
            </button>
            <button
              class="btn btn-danger btn-sm ms-2"
              @click="deleteParticipante(participante.id)"
            >
              Eliminar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!participantes.length" class="text-center mt-3">No hay participantes registrados.</p>
  </div>
</template>
