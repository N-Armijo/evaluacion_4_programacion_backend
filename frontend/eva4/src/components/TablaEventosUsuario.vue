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
const estadoEventos = ref({}); // Diccionario que guarda si el usuario está inscrito en un evento

// Sincronizar estado de inscripción desde el backend
const sincronizarEstadoEventos = async () => {
  console.log('Sincronizando estado de inscripciones...');
  try {
    // Realizar la petición al backend
    const response = await participantesService.getParticipantes();
    const participantes = response.data.results || response.data; // Verifica el formato del backend

    // Verificar si los datos son un array
    if (!Array.isArray(participantes)) {
      console.error('Formato de datos inválido:', participantes);
      return;
    }

    console.log('Lista de participantes obtenida:', participantes);

    // Iterar sobre los eventos y sincronizar el estado
    props.eventos.forEach((evento) => {
      // Buscar si el usuario está inscrito en este evento
      const participante = participantes.find((p) => p.evento === evento.id);

      // Actualizar el estado del evento con el ID del participante o null
      estadoEventos.value[evento.id] = participante ? participante.id : null;

      // Depurar la información procesada
      console.log(
        `Evento ID: ${evento.id}, Participante encontrado: ${JSON.stringify(participante)}`
      );
      console.log(
        `Estado actualizado para Evento ID ${evento.id}: Participante ID = ${estadoEventos.value[evento.id]}`
      );
    });

    console.log('Estado de eventos actualizado:', estadoEventos.value);
  } catch (err) {
    // Capturar y mostrar errores de la petición
    console.error('Error al sincronizar inscripciones:', err.response?.data || err.message);
  }
};




// Emitir evento para inscribirse
const handleInscribirse = async (eventoId) => {
  console.log(`Intentando inscribirse al evento con ID: ${eventoId}`);
  try {
    const response = await participantesService.createParticipante({ evento: eventoId });
    console.log('Inscripción exitosa:', response.data);
    estadoEventos.value[eventoId] = response.data.id; // Guardar ID del participante en estado
    alert('Te has inscrito en el evento.');
  } catch (err) {
    console.error('Error al inscribirse:', err.response?.data || err.message);
    alert('Error al inscribirse en el evento.');
  }
};

// Emitir evento para desinscribirse
const handleDesinscribirse = async (eventoId) => {
  console.log(`Intentando desinscribirse del evento con ID: ${eventoId}`);
  const participanteId = estadoEventos.value[eventoId];

  // Imprimir el estado actual del participante asociado
  console.log(`Estado actual para el evento ID ${eventoId}: Participante ID = ${participanteId}`);

  if (!participanteId) {
    console.error('El participante no tiene un ID válido para desinscribirse.');
    alert('No estás inscrito en este evento.');
    return;
  }

  try {
    await participantesService.deleteParticipante(participanteId); // Usar el ID del participante
    console.log(`Desinscripción exitosa del evento con ID: ${eventoId}, Participante ID: ${participanteId}`);
    estadoEventos.value[eventoId] = null; // Limpiar estado
    console.log(`Aqui una ayuda: participanteid: ${participanteId} - eventoid: ${eventoId}`)
    alert('Te has desinscrito del evento.');
  } catch (err) {
    console.error('Error al desinscribirse:', err.response?.data || err.message);
    console.log(`Aqui una ayuda: participanteid: ${participanteId} - eventoid: ${eventoId}`)
    alert('Error al desinscribirse del evento.');
  }
};


// Cambiar página
const goToPage = (page) => {
  console.log(`Cambiando a la página: ${page}`);
  emit('pageChange', page);
};

// Inicializar estado local al cargar eventos
watch(() => props.eventos, () => {
  console.log('Eventos cambiaron, sincronizando estado...');
  sincronizarEstadoEventos();
});

// Sincronizar inscripciones al montar el componente
onMounted(() => {
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
