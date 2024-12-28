import axios from "axios"

const request = axios.create({
  baseURL: "/api",
  timeout: 3000
})

request.interceptors.request.use(config => {
  config.headers.Authorization = `Bearer ${window.sessionStorage.getItem("token")}`
  return config
})

export default request
