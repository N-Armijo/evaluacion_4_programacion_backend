<script setup>
import { ref, onMounted } from 'vue';
import participantesService from '@/services/participantesService';
import usuariosService from '@/services/usuariosService';
import eventosService from '@/services/eventosService';
import FormParticipante from '@/components/FormParticipante.vue';
import TablaParticipantes from '@/components/TablaParticipantes.vue';

const participantes = ref([]); // Lista de participantes
const eventos = ref([]); // Lista de eventos disponibles
const usuarios = ref([]); // Lista de usuarios registrados
const nuevoParticipante = ref({
  id: null,
  correo: '',
  evento: '',
});
const isUpdating = ref(false); // Define si estamos actualizando un participante
const error = ref(null);

// Cargar lista de participantes desde el backend
const fetchParticipantes = async () => {
  try {
    const response = await participantesService.getParticipantes();
    participantes.value = response.data.results || response.data; // Adaptar según formato del backend
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar participantes';
  }
};

// Cargar lista de eventos
const fetchEventos = async () => {
  try {
    const response = await eventosService.getEventos();
    eventos.value = response.data.results || response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar eventos';
  }
};

// Cargar lista de usuarios registrados
const fetchUsuarios = async () => {
  try {
    const response = await usuariosService.getUsuarios();
    usuarios.value = response.data; // Asegúrate de que el backend devuelva [{id, username, email}]
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
    correo: '',
    evento: '',
  };
  isUpdating.value = false;
};

// Cargar datos al montar la vista
onMounted(() => {
  fetchParticipantes();
  fetchEventos();
  fetchUsuarios();
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

    <!-- Tabla de Participantes -->
    <TablaParticipantes
      :participantes="participantes"
      @editParticipante="cargarParticipanteParaActualizar"
      @deleteParticipante="eliminarParticipante"
    />

    <!-- Mostrar error si existe -->
    <p v-if="error" class="text-danger text-center mt-3">Error: {{ error }}</p>
  </div>
</template>
