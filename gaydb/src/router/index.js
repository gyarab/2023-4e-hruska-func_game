import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import GrafView from '../views/GrafView.vue'
import PrihlaseniView from '../views/PrihlaseniView.vue'

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
    },
    {
      path: '/prihlaseni',
      name: 'prihlaseni',
      component: PrihlaseniView,
      meta: {
        title: 'Přihlásit se'
      }
    }
  ]
})

export default router
