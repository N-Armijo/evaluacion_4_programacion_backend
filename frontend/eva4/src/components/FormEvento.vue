<script setup>
import { ref, watch } from 'vue';

// Declarar eventos emitidos por el hijo
const emit = defineEmits(['submitForm', 'cancelForm']);

// Declarar props recibidas del padre
const props = defineProps(['evento', 'categorias', 'isUpdating']);

// Estado local del formulario
const localEvento = ref({
  id: null,
  titulo: '',
  fecha: '',
  hora: '',
  ubicacion: '',
  descripcion: '',
  categoria: '',
});

// Sincronizar datos del padre con el formulario
watch(
  () => props.evento,
  (newValue) => {
    localEvento.value = { ...newValue };
  },
  { immediate: true }
);

// Manejar el envío del formulario
const handleSubmit = () => {
  emit('submitForm', localEvento.value); // Emitir los datos del formulario al padre
};

// Manejar la cancelación del formulario
const handleCancel = () => {
  emit('cancelForm'); // Notificar al padre que se canceló la edición
};
</script>

<template>
  <div class="col-12 col-md-4 mx-auto">
    <form @submit.prevent="handleSubmit" class="mb-4">
      <div class="mb-3">
        <label for="titulo" class="form-label">Título</label>
        <input
          type="text"
          id="titulo"
          v-model="localEvento.titulo"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="fecha" class="form-label">Fecha</label>
        <input
          type="date"
          id="fecha"
          v-model="localEvento.fecha"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="hora" class="form-label">Hora</label>
        <input
          type="time"
          id="hora"
          v-model="localEvento.hora"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="ubicacion" class="form-label">Ubicación</label>
        <input
          type="text"
          id="ubicacion"
          v-model="localEvento.ubicacion"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="descripcion" class="form-label">Descripción</label>
        <textarea
          id="descripcion"
          v-model="localEvento.descripcion"
          class="form-control"
          rows="3"
          required
        ></textarea>
      </div>

      <div class="mb-3">
        <label for="categoria" class="form-label">Categoría</label>
        <select
          id="categoria"
          v-model="localEvento.categoria"
          class="form-select"
          required
        >
          <option value="" disabled>Selecciona una categoría</option>
          <option
            v-for="categoria in categorias"
            :key="categoria.id"
            :value="categoria.id"
          >
            {{ categoria.nombre }}
          </option>
        </select>
      </div>

      <button type="submit" class="btn btn-primary">
        {{ isUpdating ? 'Guardar Cambios' : 'Crear Evento' }}
      </button>
      <button
        type="button"
        class="btn btn-secondary ms-2"
        v-if="isUpdating"
        @click="handleCancel"
      >
        Cancelar
      </button>
    </form>
  </div>
</template>
