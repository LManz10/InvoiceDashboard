import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FilterView from '../views/FilterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/dashboard/:runId',
      name: 'dashboard',
      component: () => import('../views/DashboardHomeView.vue'),
      props: true,
    },
    {
      path: '/filterrun/:runId',
      name: 'filterview',
      component: () => import('../views/FilterView.vue'),
      props: true
    },
  

  ],
})

export default router
