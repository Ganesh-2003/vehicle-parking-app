import { createRouter, createWebHistory } from 'vue-router';

import Login from './views/Login.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },

  {
    path: '/login',
    name: 'Login',
    component: Login
  },

  {
    path: '/register',
    name: 'Register',
    component: () => import('./views/Register.vue')
  },

  {
    path: "/admin/dashboard",
    component: () => import("./views/admin/dashboard.vue")
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
