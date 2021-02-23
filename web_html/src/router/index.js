import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/home',
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    redirect: "/index",
    children:[
      {
        path: '/index',
        name: 'Index',
        component: () => import('../views/Index.vue')

      },
      {
        path: '/book_list',
        name: 'BookList',
        component: () => import('../views/BookList.vue')

      },
      {
        path: '/book_detail',
        name: 'BookDetail',
        component: () => import('../views/BookDetail.vue')
      },
      {
        path: '/book_read',
        name: 'BookRead',
        component: () => import('../views/BookRead.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
