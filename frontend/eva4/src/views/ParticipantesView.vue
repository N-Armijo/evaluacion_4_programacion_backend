<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import participantesService from '@/services/participantesService';
import eventosService from '@/services/eventosService';
import usuariosService from '@/services/usuariosService'; // Importar servicio de usuarios
import FormParticipante from '@/components/FormParticipante.vue';
import TablaParticipantes from '@/components/TablaParticipantes.vue';

const participantes = ref([]); // Lista de participantes
const eventos = ref([]); // Lista de eventos disponibles
const usuarios = ref([]); // Lista de usuarios registrados
const filtros = ref({
  nombre: '',
  evento: '',
  orden: 'asc',
});
const currentPage = ref(1); // Página actual
const itemsPerPage = 10; // Tamaño de página
const totalPages = ref(0); // Total de páginas
const error = ref(null);

// Nuevo participante y estado de actualización
const nuevoParticipante = ref({
  id: null,
  nombre: '',
  correo: '',
  evento: '',
});
const isUpdating = ref(false);

// Computed para calcular el total de participantes filtrados
const totalFiltrados = computed(() => participantes.value.length);

// Computed para ordenar participantes localmente
const participantesOrdenados = computed(() => {
  const sortedParticipantes = [...participantes.value];
  sortedParticipantes.sort((a, b) => {
    const nombreA = a.nombre.toLowerCase();
    const nombreB = b.nombre.toLowerCase();
    if (filtros.value.orden === 'asc') {
      return nombreA.localeCompare(nombreB);
    } else {
      return nombreB.localeCompare(nombreA);
    }
  });
  return sortedParticipantes;
});

// Obtener participantes del backend con filtros y paginación
const fetchParticipantes = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: itemsPerPage,
      search: filtros.value.nombre || undefined,
      evento: filtros.value.evento || undefined,
    };

    const response = await participantesService.getParticipantes(params);
    participantes.value = response.data.results || [];
    totalPages.value = Math.ceil(response.data.count / itemsPerPage);
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar participantes';
  }
};

// Obtener eventos del backend
const fetchEventos = async () => {
  try {
    const response = await eventosService.getEventos();
    eventos.value = response.data.results || response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar eventos';
  }
};

// Obtener usuarios del backend
const fetchUsuarios = async () => {
  try {
    const response = await usuariosService.getUsuarios();
    usuarios.value = response.data || [];
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar usuarios';
  }
};

// Crear o actualizar participante
const crearOActualizarParticipante = async (participante) => {
  try {
    if (isUpdating.value) {
      await participantesService.updateParticipante(participante.id, participante);
      alert('Participante actualizado con éxito');
    } else {
      await participantesService.createParticipante(participante);
      alert('Participante creado con éxito');
    }
    await fetchParticipantes();
    resetFormulario();
  } catch (err) {
    error.value = err.response?.data || 'Error al crear/actualizar participante';
  }
};

// Eliminar participante
const eliminarParticipante = async (id) => {
  try {
    await participantesService.deleteParticipante(id);
    alert('Participante eliminado con éxito');
    await fetchParticipantes();
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al eliminar participante';
  }
};

// Preparar formulario para edición
const cargarParticipanteParaActualizar = (participante) => {
  isUpdating.value = true;
  nuevoParticipante.value = { ...participante };
};

// Resetear formulario
const resetFormulario = () => {
  nuevoParticipante.value = {
    id: null,
    nombre: '',
    correo: '',
    evento: '',
  };
  isUpdating.value = false;
};

// Recalcular participantes al cambiar los filtros
watch(
  () => filtros.value,
  async () => {
    currentPage.value = 1;
    await fetchParticipantes();
  },
  { deep: true }
);

// Cambiar página
const cambiarPagina = async (page) => {
  if (page > 0 && page <= totalPages.value) {
    currentPage.value = page;
    await fetchParticipantes();
  }
};

// Cargar datos al montar
onMounted(() => {
  fetchParticipantes();
  fetchEventos();
  fetchUsuarios(); // Cargar usuarios al iniciar
});
</script>

<template>
  <div>
    <h2 class="text-center my-4">Gestión de Participantes</h2>

    <!-- Formulario de Participante -->
    <FormParticipante
      :participante="nuevoParticipante"
      :eventos="eventos"
      :usuarios="usuarios" 
      :isUpdating="isUpdating"
      @submitForm="crearOActualizarParticipante"
      @cancelForm="resetFormulario"
    />

    <!-- Total de participantes filtrados -->
    <div class="text-center mt-3">
      <h4>Participantes encontrados: {{ totalFiltrados }}</h4>
    </div>

    <!-- Filtros -->
    <div class="col-8 mx-auto">
      <div class="row mt-4">
        <div class="col-md-4">
          <label for="filtroNombre" class="form-label">Buscar por Nombre</label>
          <input
            id="filtroNombre"
            v-model="filtros.nombre"
            class="form-control"
            type="text"
            placeholder="Nombre del Participante"
          />
        </div>
        <div class="col-md-4">
          <label for="filtroEvento" class="form-label">Filtrar por Evento</label>
          <select id="filtroEvento" v-model="filtros.evento" class="form-select">
            <option value="">Todos los Eventos</option>
            <option v-for="evento in eventos" :key="evento.id" :value="evento.id">
              {{ evento.titulo }}
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="orden" class="form-label">Ordenar por Nombre</label>
          <select id="orden" v-model="filtros.orden" class="form-select">
            <option value="asc">Ascendente</option>
            <option value="desc">Descendente</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Tabla de Participantes -->
    <TablaParticipantes 
    :participantes="participantesOrdenados"
    @editParticipante="cargarParticipanteParaActualizar"
    @deleteParticipante="eliminarParticipante"
    />

    <!-- Paginación -->
    <nav v-if="totalPages > 1" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="cambiarPagina(currentPage - 1)">Anterior</button>
        </li>
        <li
          class="page-item"
          v-for="page in totalPages"
          :key="page"
          :class="{ active: currentPage === page }"
        >
          <button class="page-link" @click="cambiarPagina(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="cambiarPagina(currentPage + 1)">Siguiente</button>
        </li>
      </ul>
    </nav>

    <!-- Mostrar error si existe -->
    <p v-if="error" class="text-danger text-center mt-3">Error: {{ error }}</p>
  </div>
</template>
