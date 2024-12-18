<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  participante: Object, // Datos del participante a crear/editar
  eventos: Array, // Lista de eventos disponibles
  isUpdating: Boolean, // Define si estamos en modo edición
});

const emit = defineEmits(['submitForm', 'cancelForm']);

const localParticipante = ref({ ...props.participante });

// Sincronizar cuando cambian las props
watch(
  () => props.participante,
  (newVal) => {
    localParticipante.value = { ...newVal };
  }
);

const submitForm = () => {
  emit('submitForm', { ...localParticipante.value });
};

const cancelForm = () => {
  emit('cancelForm');
};
</script>

<template>
  <div class="col-12 col-md-4 mx-auto mb-4">
    <h4>{{ isUpdating ? 'Editar Participante' : 'Nuevo Participante' }}</h4>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="nombre" class="form-label">Nombre</label>
        <input
          type="text"
          id="nombre"
          v-model="localParticipante.nombre"
          class="form-control"
          required
        />
      </div>
      <div class="mb-3">
        <label for="correo" class="form-label">Correo Electrónico</label>
        <input
          type="email"
          id="correo"
          v-model="localParticipante.correo"
          class="form-control"
          required
        />
      </div>
      <div class="mb-3">
        <label for="evento" class="form-label">Evento</label>
        <select id="evento" v-model="localParticipante.evento" class="form-select" required>
          <option value="" disabled>Seleccione un evento</option>
          <option v-for="evento in eventos" :key="evento.id" :value="evento.id">
            {{ evento.titulo }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">
        {{ isUpdating ? 'Guardar Cambios' : 'Crear Participante' }}
      </button>
      <button
        type="button"
        class="btn btn-secondary ms-2"
        v-if="isUpdating"
        @click="cancelForm"
      >
        Cancelar
      </button>
    </form>
  </div>
</template>
