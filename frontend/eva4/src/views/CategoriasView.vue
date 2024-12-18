<script setup>
import { ref, onMounted, computed } from 'vue';
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

// Filtros
const filtroTexto = ref('');
const ordenAscendente = ref(true); // Controla el orden ascendente/descendente

// Paginación
const pagination = ref({ count: 0, next: null, previous: null });
const currentPage = ref(1);

// Computed para aplicar filtros dinámicamente
const categoriasFiltradasOrdenadas = computed(() => {
  let filtradas = categorias.value.filter((categoria) =>
    categoria.nombre.toLowerCase().includes(filtroTexto.value.toLowerCase())
  );
  return filtradas.sort((a, b) => {
    if (ordenAscendente.value) {
      return a.nombre.localeCompare(b.nombre);
    }
    return b.nombre.localeCompare(a.nombre);
  });
});

// Cargar categorías desde el backend
const fetchCategorias = async (page = 1) => {
  try {
    const response = await categoriasService.getCategorias({ page });
    categorias.value = response.data.results;
    pagination.value = {
      count: response.data.count,
      next: response.data.next,
      previous: response.data.previous,
    };
    currentPage.value = page;
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
    await fetchCategorias(currentPage.value);
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
    await fetchCategorias(currentPage.value);
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al eliminar categoría';
  }
};

// Cargar datos de la categoría en el formulario para edición
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

// Cambiar página
const cambiarPagina = (page) => {
  if (page > 0 && (pagination.value.next || pagination.value.previous)) {
    fetchCategorias(page);
  }
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
    
    <!-- Filtros -->
    <div class="col-12 col-md-6 mx-auto mb-5">
      <div class="row">
        <div class="col-md-6">
          <input
            type="text"
            class="form-control"
            placeholder="Buscar por nombre"
            v-model="filtroTexto"
          />
        </div>
        <div class="col-md-6 text-end">
          <button
            class="btn btn-outline-primary"
            @click="ordenAscendente = !ordenAscendente"
          >
            Ordenar: {{ ordenAscendente ? 'Ascendente' : 'Descendente' }}
          </button>
        </div>
      </div>
    </div>
    <!-- Tabla -->
    <TablaCategorias
      :categorias="categoriasFiltradasOrdenadas"
      @editCategoria="cargarCategoriaParaActualizar"
      @deleteCategoria="eliminarCategoria"
    />

    <!-- Paginación -->
    <nav v-if="pagination.count > categorias.length" class="mt-3">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: !pagination.previous }">
          <button class="page-link" @click="cambiarPagina(currentPage - 1)">
            Anterior
          </button>
        </li>
        <li class="page-item" :class="{ disabled: !pagination.next }">
          <button class="page-link" @click="cambiarPagina(currentPage + 1)">
            Siguiente
          </button>
        </li>
      </ul>
    </nav>

    <p v-if="error" class="text-danger text-center mt-3">Error: {{ error }}</p>
  </div>
</template>
