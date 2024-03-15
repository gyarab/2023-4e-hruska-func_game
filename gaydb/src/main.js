import './assets/styles.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@/assets/styles.css'
import axios from 'axios'

const app = createApp(App)

axios.defaults.baseURL = 'http://127.0.0.1:8000' // http://127.0.0.1:5173 na production to může být jiný bacha

app.use(router)

app.mount('#app')
