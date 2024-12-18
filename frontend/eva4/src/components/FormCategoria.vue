<script setup>
const props = defineProps({
  categoria: Object,
  isUpdating: Boolean,
});

const emit = defineEmits(['submitForm', 'cancelForm']);

const handleSubmit = () => {
  emit('submitForm', { ...props.categoria });
};

const handleCancel = () => {
  emit('cancelForm');
};
</script>

<template>
  <div class="col-12 col-md-4 mx-auto">
    <form @submit.prevent="handleSubmit" class="mb-4">
      <div class="mb-3">
        <label for="nombre" class="form-label">Nombre de Categoría</label>
        <input
          type="text"
          id="nombre"
          v-model="categoria.nombre"
          class="form-control"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">
        {{ isUpdating ? 'Guardar Cambios' : 'Crear Categoría' }}
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
