import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  {
    path: '/eventos',
    name: 'Eventos',
    component: () => import('../views/EventosView.vue')
  }, //=> lazy load permitecargan componentes de manera dinamica cuando se navega entre rutas
  {
    path: '/categorias',
    name: 'Categorias',
    component: () => import('../views/CategoriasView.vue'), 
  },
  {
    path: '/participantes',
    name: 'Participantes',
    component: () => import('../views/ParticipantesView.vue'), 
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Auth/RegisterView.vue'), // Lazy load
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Auth/LoginView.vue'), // Lazy load
  },  
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;