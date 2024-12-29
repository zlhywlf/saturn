import { registerPlugins } from "@/plugins"
import App from "./App.vue"
import { createApp } from "vue"
import "@/scss/style.scss"

const app = createApp(App)

registerPlugins(app)

app.mount("#app")
