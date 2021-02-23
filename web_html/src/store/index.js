import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    bookChapter:{},
    SideBarIndex:"0"
  },
  mutations: {
    getChapter(state, data){
      state.bookChapter = data
    },
    changeSideBarIndex(state, val){
      state.SideBarIndex = val
    }
  },
  actions: {
  },
  modules: {
  }
})
