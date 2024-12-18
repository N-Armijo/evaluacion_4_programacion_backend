<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  participante: Object, // Participante para edición o creación
  eventos: Array, // Lista de eventos disponibles
  usuarios: Array, // Lista de usuarios registrados
  isUpdating: Boolean, // Modo de edición
});

const emit = defineEmits(['submitForm', 'cancelForm']);

const localParticipante = ref({
  id: props.participante?.id || null,
  nombre: props.participante?.nombre || '',
  correo: props.participante?.correo || '',
  evento: props.participante?.evento || '',
});

// Sincronizar datos locales con el prop `participante`
watch(
  () => props.participante,
  (newParticipante) => {
    localParticipante.value = {
      id: newParticipante?.id || null,
      nombre: newParticipante?.nombre || '',
      correo: newParticipante?.correo || '',
      evento: newParticipante?.evento || '',
    };
  },
  { immediate: true }
);

// Manejar envío del formulario
const handleSubmit = () => {
  if (!localParticipante.value.evento || !localParticipante.value.correo) {
    alert('Por favor, selecciona un evento y un usuario.');
    return;
  }

  // Buscar el nombre del usuario seleccionado
  const usuarioSeleccionado = props.usuarios.find(
    (usuario) => usuario.email === localParticipante.value.correo
  );

  if (!usuarioSeleccionado) {
    alert('Usuario seleccionado no encontrado.');
    return;
  }

  // Asignar el nombre basado en el usuario seleccionado
  localParticipante.value.nombre = usuarioSeleccionado.username;

  emit('submitForm', localParticipante.value);
};

// Cancelar y limpiar el formulario
const handleCancel = () => {
  emit('cancelForm');
};
</script>

<template>
  <div class="mt-4 col-12 col-md-6 mx-auto">
    <h3>{{ isUpdating ? 'Actualizar Participante' : 'Crear Participante' }}</h3>
    <form @submit.prevent="handleSubmit" class="mt-3">
      <!-- Selección de evento -->
      <div class="mb-3">
        <label for="evento" class="form-label">Evento</label>
        <select
          id="evento"
          v-model="localParticipante.evento"
          class="form-select"
          required
        >
          <option value="" disabled>Selecciona un evento</option>
          <option v-for="evento in eventos" :key="evento.id" :value="evento.id">
            {{ evento.titulo }}
          </option>
        </select>
      </div>

      <!-- Selección de usuario -->
      <div class="mb-3">
        <label for="usuario" class="form-label">Usuario</label>
        <select
          id="usuario"
          v-model="localParticipante.correo"
          class="form-select"
          required
        >
          <option value="" disabled>Selecciona un usuario</option>
          <option v-for="usuario in usuarios" :key="usuario.email" :value="usuario.email">
            {{ usuario.username }} - {{ usuario.email }}
          </option>
        </select>
      </div>

      <div class="mt-3">
        <button type="submit" class="btn btn-primary">
          {{ isUpdating ? 'Guardar Cambios' : 'Crear Participante' }}
        </button>
        <button type="button" class="btn btn-secondary ms-2" @click="handleCancel">
          Cancelar
        </button>
      </div>
    </form>
  </div>
</template>
