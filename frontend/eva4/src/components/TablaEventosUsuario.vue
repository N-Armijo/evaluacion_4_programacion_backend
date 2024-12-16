<script setup>
import { ref, watch, onMounted } from 'vue';
import participantesService from '@/services/participantesService';

const props = defineProps({
  eventos: Array, // Lista de eventos paginada
  currentPage: Number, // Página actual
  totalPages: Number, // Total de páginas
});

const emit = defineEmits(['pageChange']);

// Estado local para manejar inscripciones
const estadoEventos = ref({});

// Emitir evento para inscribirse
const handleInscribirse = async (id) => {
  console.log(`Intentando inscribirse al evento con ID: ${id}`);
  try {
    const response = await participantesService.createParticipante({ evento: id });
    console.log(`Inscripción exitosa: ${JSON.stringify(response.data)}`);
    estadoEventos.value[id] = response.data.id; // Guardar ID del participante
    alert('Te has inscrito en el evento.');
  } catch (err) {
    console.error('Error al inscribirse:', err.response?.data || err.message);
    alert('Error al inscribirse en el evento.');
  }
};

// Emitir evento para desinscribirse
const handleDesinscribirse = async (eventoId) => {
  console.log(`Intentando desinscribirse del evento con ID: ${eventoId}`);
  try {
    const participanteId = estadoEventos.value[eventoId];
    if (!participanteId) {
      alert('No estás inscrito en este evento.');
      return;
    }
    await participantesService.deleteParticipante(participanteId); // Usar el ID del participante
    console.log(`Desinscripción exitosa del evento con ID: ${eventoId}`);
    estadoEventos.value[eventoId] = null; // Limpiar estado
    alert('Te has desinscrito del evento.');
  } catch (err) {
    console.error('Error al desinscribirse:', err.response?.data || err.message);
    alert('Error al desinscribirse del evento.');
  }
};

// Emitir evento para ver detalles
const handleVerDetalles = (id) => {
  console.log(`Intentando ver detalles del evento con ID: ${id}`);
};

// Cambiar página
const goToPage = (page) => {
  console.log(`Cambiando a la página: ${page}`);
  emit('pageChange', page);
};

// Inicializar el estado de los eventos
const inicializarEstado = () => {
  props.eventos.forEach((evento) => {
    if (!estadoEventos.value[evento.id]) {
      estadoEventos.value[evento.id] = null; // Inicializar como no inscrito (null)
    }
  });
};

// Sincronizar estado de eventos inscritos desde el backend
const sincronizarEstadoEventos = async () => {
  try {
    const response = await participantesService.getParticipantes();
    const participantes = response.data;

    // Recorrer todos los eventos y asignar estado basado en inscripción
    props.eventos.forEach((evento) => {
      const participante = participantes.find((p) => p.evento === evento.id);
      estadoEventos.value[evento.id] = participante ? participante.id : null; // Guardar ID del participante
    });
  } catch (err) {
    console.error('Error al sincronizar eventos inscritos:', err.response?.data || err.message);
  }
};

// Recalcular estado cuando cambien los eventos
watch(() => props.eventos, inicializarEstado);

onMounted(() => {
  inicializarEstado();
  sincronizarEstadoEventos();
});
</script>

<template>
  <div class="col-12 col-md-8 mx-auto">
    <table class="table table-hover text-center table-striped mt-4">
      <thead>
        <tr>
          <th>Título</th>
          <th>Fecha</th>
          <th>Ubicación</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="evento in eventos" :key="evento.id">
          <td>{{ evento.titulo }}</td>
          <td>{{ evento.fecha }}</td>
          <td>{{ evento.ubicacion }}</td>
          <td>
            <!-- Botón de inscribirse -->
            <button
              class="btn btn-primary btn-sm"
              @click="handleInscribirse(evento.id)"
              :disabled="estadoEventos[evento.id] !== null"
            >
              Inscribirse
            </button>

            <!-- Botón de desinscribirse -->
            <button
              class="btn btn-danger btn-sm ms-2"
              @click="handleDesinscribirse(evento.id)"
              :disabled="estadoEventos[evento.id] === null"
            >
              Desinscribirse
            </button>

            <!-- Botón para ver detalles -->
            <button class="btn btn-info btn-sm ms-2" @click="handleVerDetalles(evento.id)">
              Ver Detalles
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Paginación -->
    <nav v-if="totalPages > 1" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="goToPage(currentPage - 1)">Anterior</button>
        </li>
        <li
          class="page-item"
          v-for="page in totalPages"
          :key="page"
          :class="{ active: currentPage === page }"
        >
          <button class="page-link" @click="goToPage(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="goToPage(currentPage + 1)">Siguiente</button>
        </li>
      </ul>
    </nav>
  </div>
</template>
