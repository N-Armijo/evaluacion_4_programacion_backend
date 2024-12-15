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

const totalPages = computed(() => Math.ceil(pagination.value.count / 10));

// Verificar autenticación
const verificarAutenticacion = () => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    alert('Debes iniciar sesión para acceder a esta página.');
    router.push('/login');
  }
};

// Cargar eventos
const fetchEventos = async (page = 1) => {
  try {
    const response = await eventosService.getEventos(page);
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

onMounted(() => {
  verificarAutenticacion();
  fetchEventos();
  fetchCategorias();
});
</script>

<template>
  <div class="mx-auto">
    <h2 class="text-center my-4">Gestión de Eventos</h2>

    <FormEvento
      :evento="nuevoEvento"
      :categorias="categorias"
      :isUpdating="isUpdating"
      @submitForm="crearOActualizarEvento"
      @cancelForm="resetFormulario"
    />

    <TablaEventos
      :eventos="eventos"
      :currentPage="currentPage"
      :totalPages="totalPages"
      @editEvento="cargarEventoParaActualizar"
      @deleteEvento="eliminarEvento"
      @pageChange="cambiarPagina"
    />

    <p v-if="error" class="text-danger text-center mt-3">Error: {{ error }}</p>
  </div>
</template>
