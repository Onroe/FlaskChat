import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/register',
    name: 'Register',
    component() {
      return import(/* webpackChunkName: "about" */ '../views/Register.vue');
    },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component() {
      return import(/* webpackChunkName: "about" */ '../views/Dashboard.vue');
    },
  },
  {
    path: '/login',
    name: 'Login',
    component() {
      return import(/* webpackChunkName: "about" */ '../views/Login.vue');
    },
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component() {
      return import(/* webpackChunkName: "about" */ '../views/About.vue');
    },
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  if (sessionStorage.getItem('authToken') !== null || to.path === '/login') {
    next();
  } else {
    next();
  }
});
export default router;
