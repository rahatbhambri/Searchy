import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import home from './components/home.vue' 


import './assets/main.css'

const app = createApp(App) ;
// const app = createApp(home) ;

app.use(createPinia()) ;
app.use(router) ;

console.log("working") ;
app.mount('#app') ;

