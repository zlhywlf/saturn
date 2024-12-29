import vuetify from "./vuetify"
import pinia from "../stores"
import router from "../router"
import type { App } from "vue"
import { PerfectScrollbarPlugin } from "vue3-perfect-scrollbar"

export function registerPlugins(app: App) {
  app.use(vuetify).use(router).use(pinia).use(PerfectScrollbarPlugin)
}
