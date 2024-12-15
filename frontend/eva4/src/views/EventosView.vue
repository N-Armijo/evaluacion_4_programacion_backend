<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import FormEvento from '@/components/FormEvento.vue';
import TablaEventos from '@/components/TablaEventos.vue';
import eventosService from '@/services/eventosService';
import categoriasService from '@/services/categoriasService';

const router = useRouter();
const eventos = ref([]);
const categorias = ref([]);
const pagination = ref({ count: 0, next: null, previous: null });
const currentPage = ref(1);
const nuevoEvento = ref({
  id: null,
  titulo: '',
  fecha: '',
  hora: '',
  ubicacion: '',
  descripcion: '',
  categoria: '',
});
const error = ref(null);
const isUpdating = ref(false);

// Filtros
const filtros = ref({
  categoria: '',
  fecha: '',
});

const totalPages = computed(() => Math.ceil(pagination.value.count / 10));

// Verificar autenticación
const verificarAutenticacion = () => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    alert('Debes iniciar sesión para acceder a esta página.');
    router.push('/login');
  }
};

// Cargar eventos con filtros y paginación
const fetchEventos = async (page = 1) => {
  try {
    const params = {
      page, // Número de página
      categoria: filtros.value.categoria || undefined, // Filtrar por categoría si se selecciona
      fecha: filtros.value.fecha || undefined, // Filtrar por fecha si se selecciona
    };

    const response = await eventosService.getEventos(params); // Enviar los parámetros al servicio
    eventos.value = response.data.results || [];
    pagination.value = {
      count: response.data.count,
      next: response.data.next,
      previous: response.data.previous,
    };
    currentPage.value = page;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar eventos';
  }
};


// Cargar categorías
const fetchCategorias = async () => {
  try {
    const response = await categoriasService.getCategorias();
    categorias.value = response.data.results || [];
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar categorías';
  }
};

// Crear o actualizar evento
const crearOActualizarEvento = async (evento) => {
  try {
    if (isUpdating.value) {
      await eventosService.updateEvento(evento.id, evento);
      alert('Evento actualizado con éxito');
    } else {
      await eventosService.createEvento(evento);
      alert('Evento creado con éxito');
    }
    await fetchEventos(currentPage.value);
    resetFormulario();
  } catch (err) {
    error.value = err.response?.data || 'Error al crear/actualizar evento';
  }
};

// Eliminar evento
const eliminarEvento = async (id) => {
  try {
    await eventosService.deleteEvento(id);
    alert('Evento eliminado con éxito');
    await fetchEventos(currentPage.value);
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al eliminar evento';
  }
};

// Preparar formulario para edición
const cargarEventoParaActualizar = (evento) => {
  isUpdating.value = true;
  nuevoEvento.value = { ...evento };
};

// Resetear formulario
const resetFormulario = () => {
  nuevoEvento.value = {
    id: null,
    titulo: '',
    fecha: '',
    hora: '',
    ubicacion: '',
    descripcion: '',
    categoria: '',
  };
  isUpdating.value = false;
};

// Cambiar de página
const cambiarPagina = (page) => {
  if (page > 0 && page <= totalPages.value) {
    fetchEventos(page);
  }
};

// Aplicar filtros
const aplicarFiltros = () => {
  fetchEventos();
};

// Limpiar filtros
const limpiarFiltros = () => {
  filtros.value = { categoria: '', fecha: '' };
  fetchEventos();
};

onMounted(() => {
  verificarAutenticacion();
  fetchEventos();
  fetchCategorias();
});
</script>

<template>
  <div class="mx-auto">
    <h2 class="text-center my-4">Gestión de Eventos</h2>



    <!-- Formulario -->
    <FormEvento :evento="nuevoEvento" :categorias="categorias" :isUpdating="isUpdating"
      @submitForm="crearOActualizarEvento" @cancelForm="resetFormulario" />

    <!-- Filtros -->
    <div class="col-12 col-md-8 mx-auto">
      <div class="row">
        <div class="col-md-4">
          <label for="filtroCategoria" class="form-label">Categoría</label>
          <select id="filtroCategoria" v-model="filtros.categoria" class="form-select">
            <option value="">Todas las categorías</option>
            <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
              {{ categoria.nombre }}
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="filtroFecha" class="form-label">Fecha</label>
          <input type="date" id="filtroFecha" v-model="filtros.fecha" class="form-control" />
        </div>

        <div class="col-md-4 d-flex align-items-end">
          <button class="btn btn-primary me-2" @click="aplicarFiltros">
            Aplicar Filtros
          </button>
          <button class="btn btn-secondary" @click="limpiarFiltros">
            Limpiar Filtros
          </button>
        </div>
      </div>


    </div>

    <!-- Tabla -->
    <TablaEventos :eventos="eventos" :currentPage="currentPage" :totalPages="totalPages"
      @editEvento="cargarEventoParaActualizar" @deleteEvento="eliminarEvento" @pageChange="cambiarPagina" />

    <p v-if="error" class="text-danger text-center mt-3">Error: {{ error }}</p>
  </div>
</template>
