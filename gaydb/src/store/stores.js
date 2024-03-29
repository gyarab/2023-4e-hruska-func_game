import { createStore } from 'vuex'

const store = createStore({
  state() {
    return {
      prihlasen: false
    }
  },
  mutations: {
    setPrihlasen(state, value) {
      state.prihlasen = value
    }
  }
})

export default store