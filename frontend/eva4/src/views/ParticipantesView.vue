<script setup>
import { ref, onMounted, computed } from 'vue';
import FormParticipante from '@/components/FormParticipante.vue';
import TablaParticipantes from '@/components/TablaParticipantes.vue';
import participantesService from '@/services/participantesService';
import eventosService from '@/services/eventosService';

const participantes = ref([]);
const eventos = ref([]);
const nuevoParticipante = ref({
  id: null,
  nombre: '',
  correo: '',
  evento: '',
});
const isUpdating = ref(false);
const error = ref(null);

// Filtros
const filtroTexto = ref('');
const filtroEvento = ref('');

// Paginación
const pagination = ref({ count: 0, next: null, previous: null });
const currentPage = ref(1);

// Computed para aplicar filtros dinámicamente
const participantesFiltrados = computed(() => {
  let filtrados = participantes.value.filter((participante) =>
    participante.nombre.toLowerCase().includes(filtroTexto.value.toLowerCase()) ||
    participante.correo.toLowerCase().includes(filtroTexto.value.toLowerCase())
  );

  if (filtroEvento.value) {
    filtrados = filtrados.filter(
      (participante) => participante.evento === parseInt(filtroEvento.value, 10)
    );
  }

  return filtrados;
});

// Cargar participantes desde el backend
const fetchParticipantes = async (page = 1) => {
  try {
    const response = await participantesService.getParticipantes({ page });
    participantes.value = response.data.results;
    pagination.value = {
      count: response.data.count,
      next: response.data.next,
      previous: response.data.previous,
    };
    currentPage.value = page;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar participantes';
  }
};

// Cargar eventos desde el backend
const fetchEventos = async () => {
  try {
    const response = await eventosService.getEventos();
    eventos.value = response.data.results || response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar eventos';
  }
};

// Crear o actualizar un participante
const crearOActualizarParticipante = async (participante) => {
  try {
    if (isUpdating.value) {
      await participantesService.updateParticipante(participante.id, participante);
      alert('Participante actualizado con éxito');
    } else {
      await participantesService.createParticipante(participante);
      alert('Participante creado con éxito');
    }
    await fetchParticipantes(currentPage.value);
    resetFormulario();
  } catch (err) {
    error.value = err.response?.data || 'Error al crear/actualizar participante';
  }
};

// Eliminar un participante
const eliminarParticipante = async (id) => {
  try {
    await participantesService.deleteParticipante(id);
    alert('Participante eliminado con éxito');
    await fetchParticipantes(currentPage.value);
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al eliminar participante';
  }
};

// Cargar datos del participante en el formulario para edición
const cargarParticipanteParaActualizar = (participante) => {
  isUpdating.value = true;
  nuevoParticipante.value = { ...participante };
};

// Resetear el formulario
const resetFormulario = () => {
  nuevoParticipante.value = {
    id: null,
    nombre: '',
    correo: '',
    evento: '',
  };
  isUpdating.value = false;
};

// Cambiar página
const cambiarPagina = (page) => {
  if (page > 0 && (pagination.value.next || pagination.value.previous)) {
    fetchParticipantes(page);
  }
};

onMounted(() => {
  fetchParticipantes();
  fetchEventos();
});
</script>

<template>
  <div class="mx-auto">
    <h2 class="text-center my-4">Gestión de Participantes</h2>

    <!-- Filtros -->
    <div class="col-12 col-md-8 mx-auto mb-3">
      <div class="row">
        <div class="col-md-6">
          <input
            type="text"
            class="form-control"
            placeholder="Buscar por nombre o correo"
            v-model="filtroTexto"
          />
        </div>
        <div class="col-md-6">
          <select
            class="form-select"
            v-model="filtroEvento"
          >
            <option value="">Todos los eventos</option>
            <option v-for="evento in eventos" :key="evento.id" :value="evento.id">
              {{ evento.titulo }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Formulario -->
    <FormParticipante
      :participante="nuevoParticipante"
      :eventos="eventos"
      :isUpdating="isUpdating"
      @submitForm="crearOActualizarParticipante"
      @cancelForm="resetFormulario"
    />

    <!-- Tabla -->
    <TablaParticipantes
      :participantes="participantesFiltrados"
      @editParticipante="cargarParticipanteParaActualizar"
      @deleteParticipante="eliminarParticipante"
    />

    <!-- Paginación -->
    <nav v-if="pagination.count > participantes.length" class="mt-3">
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
