<script setup>
import { ref, onMounted } from 'vue';
import FormCategoria from '@/components/FormCategoria.vue';
import TablaCategorias from '@/components/TablaCategorias.vue';
import categoriasService from '@/services/categoriasService';

const categorias = ref([]);
const nuevoCategoria = ref({
  id: null,
  nombre: '',
});
const isUpdating = ref(false);
const error = ref(null);

// Cargar categorías desde el backend
const fetchCategorias = async () => {
  try {
    const response = await categoriasService.getCategorias();
    categorias.value = response.data.results || response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar categorías';
  }
};

// Crear o actualizar una categoría
const crearOActualizarCategoria = async (categoria) => {
  try {
    if (isUpdating.value) {
      await categoriasService.updateCategoria(categoria.id, categoria);
      alert('Categoría actualizada con éxito');
    } else {
      await categoriasService.createCategoria(categoria);
      alert('Categoría creada con éxito');
    }
    await fetchCategorias();
    resetFormulario();
  } catch (err) {
    error.value = err.response?.data || 'Error al crear/actualizar categoría';
  }
};

// Eliminar una categoría
const eliminarCategoria = async (id) => {
  try {
    await categoriasService.deleteCategoria(id);
    alert('Categoría eliminada con éxito');
    await fetchCategorias();
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al eliminar categoría';
  }
};

// Cargar datos de la categoría en el formulario para edicion
const cargarCategoriaParaActualizar = (categoria) => {
  isUpdating.value = true;
  nuevoCategoria.value = { ...categoria };
};

// Resetear el formulario
const resetFormulario = () => {
  nuevoCategoria.value = {
    id: null,
    nombre: '',
  };
  isUpdating.value = false;
};

onMounted(() => {
  fetchCategorias();
});
</script>

<template>
  <div class="mx-auto">
    <h2 class="text-center my-4">Gestión de Categorías</h2>

    <!-- Formulario -->
    <FormCategoria
      :categoria="nuevoCategoria"
      :isUpdating="isUpdating"
      @submitForm="crearOActualizarCategoria"
      @cancelForm="resetFormulario"
    />

    <!-- Tabla -->
    <TablaCategorias
      :categorias="categorias"
      @editCategoria="cargarCategoriaParaActualizar"
      @deleteCategoria="eliminarCategoria"
    />

    <p v-if="error" class="text-danger text-center mt-3">Error: {{ error }}</p>
  </div>
</template>
