import { defineStore } from "pinia"

interface State {
  drawerSidebar: boolean
  miniSidebar: boolean
}

export const useAppStore = defineStore("app", {
  state: (): State => ({
    drawerSidebar: true,
    miniSidebar: false
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
