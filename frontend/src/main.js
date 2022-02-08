import BootstrapVue from 'bootstrap-vue'
import '@/../bootstrap/css/bootstrap.css'

import Vue from 'vue'
import App from './App.vue'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faMapMarkerAlt, faShoppingBasket, faUser, faLock, faTrashAlt } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faMapMarkerAlt, faShoppingBasket, faUser, faLock, faTrashAlt)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(BootstrapVue)
Vue.config.productionTip = false

new Vue({
  router,
  render: (h) => h(App),
  components: { App }
}).$mount('#app')
