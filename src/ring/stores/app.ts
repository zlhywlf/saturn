import { defineStore } from "pinia"

interface State {
  drawerSidebar: boolean
  miniSidebar: boolean
  loading: boolean
}

export const useAppStore = defineStore("app", {
  state: (): State => ({
    drawerSidebar: true,
    miniSidebar: false,
    loading: false
  }),
  actions: {
    setMiniSidebar() {
      this.miniSidebar = !this.miniSidebar
    },
    setDrawer() {
      this.drawerSidebar = !this.drawerSidebar
    }
  }
})
