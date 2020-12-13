import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
// import VueSocketIO from 'vue-socket.io';
// import SocketIO from 'socket.io-client';
import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import store from './store';

// const SocketInstance = socketio('http://localhost:4113');
// Vue.use(VueSocketIO, SocketInstance);
// const socket = SocketIO('http://localhost:1923');
// Vue.use(VueSocketIO, socket);

Vue.use(BootstrapVue);
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render(h) { return h(App); },
}).$mount('#app');
