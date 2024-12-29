import { createRouter, createWebHashHistory } from "vue-router/auto"
import { setupLayouts } from "virtual:generated-layouts"
import { routes } from "vue-router/auto-routes"
import { useAppStore } from "@/stores/app"
import { useAuthStore } from "@/stores/auth"

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: setupLayouts(routes)
})

router.onError((err, to) => {
  if (err?.message?.includes?.("Failed to fetch dynamically imported module")) {
    if (!localStorage.getItem("vuetify:dynamic-reload")) {
      console.log("Reloading page to fix dynamic import error")
      localStorage.setItem("vuetify:dynamic-reload", "true")
      location.assign(to.fullPath)
    } else {
      console.error("Dynamic import error, reloading page did not fix it", err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem("vuetify:dynamic-reload")
})

router.beforeEach(async (to, from, next) => {
  const publicPages = ["/login"]
  const authRequired = !publicPages.includes(to.path)
  const auth = useAuthStore()
  if (authRequired && !auth.user) {
    auth.returnUrl = to.fullPath
    return next("/login")
  } else {
    next()
  }
})

router.beforeEach(() => {
  useAppStore().loading = true
})

router.afterEach(() => {
  useAppStore().loading = false
})

export default router
