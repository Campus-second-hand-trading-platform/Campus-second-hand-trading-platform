import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import 'font-awesome/css/font-awesome.css'
// import './assets/css/global.css'
import axios from 'axios'
Vue.config.productionTip = false
// 配置请求的根路径
axios.defaults.baseURL = 'http://127.0.0.1:9000'
Vue.prototype.$http = axios

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
