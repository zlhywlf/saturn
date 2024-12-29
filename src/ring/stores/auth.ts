import { defineStore } from "pinia"
import router from "@/router"
import request from "@/utils/requests"

interface State {
  user: string | null
  returnUrl: string | null
  isLoading: boolean
}

export const useAuthStore = defineStore("auth", {
  state: (): State => ({
    user: null,
    returnUrl: null,
    isLoading: false
  }),
  actions: {
    async login(username: string, password: string) {
      this.isLoading = true
      this.user = username
      const rep = await request.post("auth", {
        username,
        password
      })
      try {
        if (rep.status == 200) {
          const token = rep.data.token
          window.sessionStorage.setItem("token", token)
          await router.push(this.returnUrl || "/")
        } else {
          throw Error("Authentication failed")
        }
      } finally {
        this.isLoading = false
      }
    },
    async logout() {
      this.user = null
      localStorage.removeItem("token")
      await router.push("/login")
    }
  }
})
