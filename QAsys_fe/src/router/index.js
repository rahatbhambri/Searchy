import { createRouter, createWebHistory } from 'vue-router' ;
import home from '../components/home.vue' ;
import search from '../components/search.vue' ;

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home'
    },
    {
      path: '/searchy',
      name: 'search',
      component : search
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
    }
  ]
})

export default router ;
