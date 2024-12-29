<script setup lang="ts">
import { ref } from "vue"
import { useField, useForm } from "vee-validate"
import { EyeInvisibleOutlined, EyeOutlined } from "@ant-design/icons-vue"
import { useAuthStore } from "@/stores/auth"

interface LoginForm {
  username: string
  password: string
}

const { handleSubmit, isSubmitting, errors } = useForm<LoginForm>({
  initialValues: {
    username: "admin",
    password: "admin"
  },
  validationSchema: {
    username(value: string) {
      if (value) return true
      return "Username is required"
    },
    password(value: string) {
      if (value) return true
      return "Password is required"
    }
  }
})

const show = ref(false)
const username = useField("username")
const password = useField("password")

const doLogin = handleSubmit((values, { setErrors }) => {
  const authStore = useAuthStore()
  return authStore
    .login(values.username, values.password)
    .catch((error: Error) => setErrors({ username: error.message }))
})
</script>

<template>
  <v-row class="bg-containerBg position-relative" no-gutters>
    <v-col cols="12" lg="12" class="d-flex align-center">
      <v-container>
        <div class="d-flex align-center justify-center" style="min-height: calc(100vh - 148px)">
          <v-row justify="center">
            <v-col cols="12" md="12">
              <v-card elevation="0" class="loginBox">
                <v-card elevation="24">
                  <v-card-text class="pa-sm-10 pa-6">
                    <v-responsive class="align-centerfill-height mx-auto" max-width="900">
                      <v-img class="mb-4" height="150" src="@/assets/logo.svg" />
                      <div class="text-center">
                        <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>
                        <h1 class="text-h2 font-weight-bold">saturn</h1>
                      </div>
                      <div class="py-4" />
                    </v-responsive>
                    <v-form @submit="doLogin" class="mt-7 loginForm">
                      <div class="mb-6">
                        <v-text-field
                          aria-label="username"
                          v-model="username.value.value"
                          :error-messages="username.errorMessage.value"
                          class="mt-2"
                          required
                          hide-details="auto"
                          variant="outlined"
                          color="primary"
                          label="Username"
                        ></v-text-field>
                      </div>
                      <div>
                        <v-text-field
                          aria-label="password"
                          v-model="password.value.value"
                          :error-messages="password.errorMessage.value"
                          required
                          variant="outlined"
                          color="primary"
                          hide-details="auto"
                          :type="show ? 'text' : 'password'"
                          class="mt-2"
                          label="Password"
                        >
                          <template v-slot:append-inner>
                            <EyeInvisibleOutlined
                              :style="{ color: 'rgb(var(--v-theme-primary))' }"
                              v-if="show == false"
                              @click="show = !show"
                            />
                            <EyeOutlined
                              :style="{ color: 'rgb(var(--v-theme-secondary))' }"
                              v-if="show == true"
                              @click="show = !show"
                            />
                          </template>
                        </v-text-field>
                      </div>
                      <v-btn
                        color="primary"
                        :loading="isSubmitting"
                        block
                        class="mt-5"
                        variant="flat"
                        size="large"
                        type="submit"
                      >
                        Login
                      </v-btn>
                    </v-form>
                  </v-card-text>
                </v-card>
              </v-card>
            </v-col>
          </v-row>
        </div>
      </v-container>
    </v-col>
  </v-row>
</template>
<style lang="scss">
.loginBox {
  max-width: 475px;
  margin: 0 auto;
}

.loginForm {
  .v-text-field .v-field--active input {
    font-weight: 500;
  }
}
</style>

<route lang="yaml">
meta:
  layout: blank
</route>
