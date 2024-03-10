import { createApp } from 'vue'
// import { createPinia } from 'pinia'

// import App from './App.vue'
import router from './router'
import home from './components/home.vue' 
import { pinia } from './stores'


import './assets/main.css'



// const app = createApp(App) ;
const app = createApp(home) ;

// app.use(createPinia()) ;
app.use(router) ;
app.use(pinia) ;

// console.log("working") ;
app.mount('#app') ;



