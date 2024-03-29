import './assets/styles.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import store from './store/stores'

axios.defaults.baseURL = 'http://127.0.0.1:8000' // Use the appropriate base URL for your environment

createApp(App)
    .use(router)
    .use(store)
    .mount('#app')