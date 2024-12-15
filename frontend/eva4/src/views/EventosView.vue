<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import eventosService from '@/services/eventosService';
import categoriasService from '@/services/categoriasService';

const router = useRouter();
const eventos = ref([]); // Lista de eventos
const categorias = ref([]); // Lista de categorías
const pagination = ref({
  count: 0,
  next: null,
  previous: null,
}); // Estado de la paginación
const currentPage = ref(1); // Página actual
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

const fetchEventos = async (page = 1) => {
  try {
    const response = await eventosService.getEventos(page); // Enviar la página como parámetro
    eventos.value = response.data.results || [];
    pagination.value = {
      count: response.data.count,
      next: response.data.next,
      previous: response.data.previous,
    };
    currentPage.value = page; // Actualiza la página actual
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

const goToPage = (page) => {
  if (page > 0 && (pagination.value.next || pagination.value.previous)) {
    fetchEventos(page);
  }
};

const crearOActualizarEvento = async () => {
  try {
    if (isUpdating.value) {
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
      await eventosService.createEvento(nuevoEvento.value);
      alert('Evento creado con éxito');
    }
    await fetchEventos(currentPage.value); // Refresca la página actual
    resetFormulario();
  } catch (err) {
    error.value = err.response?.data || 'Error al crear/actualizar evento';
  }
};

const eliminarEvento = async (id) => {
  try {
    await eventosService.deleteEvento(id);
    alert('Evento eliminado con éxito');
    await fetchEventos(currentPage.value); // Refresca la página actual
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

      <!-- Paginación -->
      <nav v-if="pagination.count > 10" class="mt-4">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: !pagination.previous }">
            <button class="page-link" @click="goToPage(currentPage - 1)">Anterior</button>
          </li>
          <li
            class="page-item"
            v-for="page in Math.ceil(pagination.count / 10)"
            :key="page"
            :class="{ active: currentPage === page }"
          >
            <button class="page-link" @click="goToPage(page)">{{ page }}</button>
          </li>
          <li class="page-item" :class="{ disabled: !pagination.next }">
            <button class="page-link" @click="goToPage(currentPage + 1)">Siguiente</button>
          </li>
        </ul>
      </nav>
    </div>

    <p v-if="error" class="text-danger text-center mt-3">Error: {{ error }}</p>
  </div>
</template>
