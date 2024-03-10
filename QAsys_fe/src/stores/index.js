// import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { createPinia } from 'pinia'

export const pinia = createPinia()

export default pinia

export const dataStore = defineStore('dataStore', {
  state: () => ({
    email: "jimmy@gmail.com",
  }),
  getters: {
    getMail: (state) => state.email,
  },
}) ;
