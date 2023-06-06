import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import GrafView from '../views/GrafView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: ''
      }
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: {
        title: 'O nás'
      }
    },
    {
      path: '/graf',
      name: 'graf',
      component: GrafView,
      meta: {
        title: 'graf'
      }
    }
  ]
})

export default router
