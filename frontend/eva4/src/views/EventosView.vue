<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import eventosService from '@/services/eventosService';
import categoriasService from '@/services/categoriasService';

const router = useRouter();
const eventos = ref([]); // lista de eventos
const categorias = ref([]); // listado de categorias para el select del formulario
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
const isUpdating = ref(false); // Estado para cambiar el texto del botón del formulario

// Texto dinámico del botón
const formularioBotonTexto = computed(() => (isUpdating.value ? 'Guardar Cambios' : 'Crear Evento'));

const verificarAutenticacion = () => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    alert('Debes iniciar sesión para acceder a esta página.');
    router.push('/login');
  }
};

const fetchEventos = async () => {
  try {
    const response = await eventosService.getEventos();
    eventos.value = response.data.results || response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar eventos';
  }
};

const fetchCategorias = async () => {
  try {
    const response = await categoriasService.getCategorias();
    categorias.value = response.data.results || response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar categorías';
  }
};

const crearOActualizarEvento = async () => {
  try {
    if (isUpdating.value) {
      // Actualizar evento
      await eventosService.updateEvento(nuevoEvento.value.id, {
        titulo: nuevoEvento.value.titulo,
        fecha: nuevoEvento.value.fecha,
        hora: nuevoEvento.value.hora,
        ubicacion: nuevoEvento.value.ubicacion,
        descripcion: nuevoEvento.value.descripcion,
        categoria: nuevoEvento.value.categoria,
      });
      alert('Evento actualizado con éxito');
    } else {
      // Crear evento
      await eventosService.createEvento(nuevoEvento.value);
      alert('Evento creado con éxito');
    }
    await fetchEventos();
    resetFormulario();
  } catch (err) {
    error.value = err.response?.data || 'Error al crear/actualizar evento';
  }
};

const eliminarEvento = async (id) => {
  try {
    await eventosService.deleteEvento(id);
    alert('Evento eliminado con éxito');
    await fetchEventos();
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al eliminar evento';
  }
};

const cargarEventoParaActualizar = (evento) => {
  isUpdating.value = true; // Cambiar a modo actualización
  nuevoEvento.value = { ...evento }; // Cargar los datos del evento en el formulario
};

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
  isUpdating.value = false; // Cambiar a modo creación
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

    <!-- Formulario de creación/actualización -->
    <div class="col-12 col-md-4 mx-auto">
      <form @submit.prevent="crearOActualizarEvento" class="mb-4">
        <div class="mb-3">
          <label for="titulo" class="form-label">Título</label>
          <input type="text" id="titulo" v-model="nuevoEvento.titulo" class="form-control" required />
        </div>

        <div class="mb-3">
          <label for="fecha" class="form-label">Fecha</label>
          <input type="date" id="fecha" v-model="nuevoEvento.fecha" class="form-control" required />
        </div>

        <div class="mb-3">
          <label for="hora" class="form-label">Hora</label>
          <input type="time" id="hora" v-model="nuevoEvento.hora" class="form-control" required />
        </div>

        <div class="mb-3">
          <label for="ubicacion" class="form-label">Ubicación</label>
          <input type="text" id="ubicacion" v-model="nuevoEvento.ubicacion" class="form-control" required />
        </div>

        <div class="mb-3">
          <label for="descripcion" class="form-label">Descripción</label>
          <textarea id="descripcion" v-model="nuevoEvento.descripcion" class="form-control" rows="3" required></textarea>
        </div>

        <div class="mb-3">
          <label for="categoria" class="form-label">Categoría</label>
          <select id="categoria" v-model="nuevoEvento.categoria" class="form-select" required>
            <option value="" disabled>Selecciona una categoría</option>
            <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
              {{ categoria.nombre }}
            </option>
          </select>
        </div>

        <button type="submit" class="btn btn-primary">
          {{ formularioBotonTexto }}
        </button>
        <button type="button" class="btn btn-secondary ms-2" v-if="isUpdating.value" @click="resetFormulario">
          Cancelar
        </button>
      </form>
    </div>

    <!-- Tabla de eventos -->
    <div class="col-12 col-md-8 mx-auto">
      <table class="table table-hover text-center table-striped mt-4">
        <thead>
          <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Fecha</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="evento in eventos" :key="evento.id">
            <td>{{ evento.id }}</td>
            <td>{{ evento.titulo }}</td>
            <td>{{ evento.fecha }}</td>
            <td>
              <button class="btn btn-warning btn-sm text-dark" @click="cargarEventoParaActualizar(evento)">
                Actualizar
              </button>
              <button class="btn btn-danger btn-sm ms-2" @click="eliminarEvento(evento.id)">
                Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-if="error" class="text-danger text-center mt-3">Error: {{ error }}</p>
  </div>
</template>
