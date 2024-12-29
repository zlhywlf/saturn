import { defineStore } from "pinia"
import router from "@/router"
import request from "@/utils/requests"

interface State {
  user: string | null
  returnUrl: string | null
}

export const useAuthStore = defineStore("auth", {
  state: (): State => ({
    user: window.sessionStorage.getItem("user"),
    returnUrl: null
  }),
  actions: {
    async login(username: string, password: string) {
      const rep = await request.post("auth", {
        username,
        password
      })
      if (rep.status == 200) {
        const token = rep.data.token
        window.sessionStorage.setItem("token", token)
        window.sessionStorage.setItem("user", username)
        this.user = username
        await router.push(this.returnUrl || "/")
      } else {
        throw Error("Authentication failed")
      }
    },
    async logout() {
      this.user = null
      window.sessionStorage.removeItem("token")
      window.sessionStorage.removeItem("user")
      await router.push("/login")
    }
  }
})
