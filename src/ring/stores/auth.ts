import { defineStore } from "pinia"
import router from "@/router"
import request from "@/utils/requests"

interface State {
  user: string | null
  returnUrl: string | null
}

export const useAuthStore = defineStore("auth", {
  state: (): State => ({
    user: null,
    returnUrl: null
  }),
  actions: {
    async login(username: string, password: string) {
      this.user = username
      const rep = await request.post("auth", {
        username,
        password
      })
      if (rep.status == 200) {
        const token = rep.data.token
        window.sessionStorage.setItem("token", token)
        await router.push(this.returnUrl || "/")
      } else {
        throw Error("Authentication failed")
      }
    }
  }
})
