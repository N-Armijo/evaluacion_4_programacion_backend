<script setup>
import { ref } from 'vue';

const emit = defineEmits(['filtrosCambiados']);
const props = defineProps(['categorias']);

// Estado local de los filtros
const filtros = ref({
  categoria: '',
  fecha: '',
});

// Emitir cambios cuando se actualicen los filtros
const actualizarFiltros = () => {
  emit('filtrosCambiados', { ...filtros.value });
};
</script>

<template>
  <div class="row mb-4">
    <div class="col-md-6">
      <label for="filtro-categoria" class="form-label">Filtrar por Categoría</label>
      <select
        id="filtro-categoria"
        v-model="filtros.categoria"
        class="form-select"
        @change="actualizarFiltros"
      >
        <option value="">Todas las Categorías</option>
        <option
          v-for="categoria in categorias"
          :key="categoria.id"
          :value="categoria.id"
        >
          {{ categoria.nombre }}
        </option>
      </select>
    </div>
    <div class="col-md-6">
      <label for="filtro-fecha" class="form-label">Filtrar por Fecha</label>
      <input
        type="date"
        id="filtro-fecha"
        v-model="filtros.fecha"
        class="form-control"
        @change="actualizarFiltros"
      />
    </div>
  </div>
</template>
