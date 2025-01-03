import AutoImport from "unplugin-auto-import/vite"
import Components from "unplugin-vue-components/vite"
import Fonts from "unplugin-fonts/vite"
import Layouts from "vite-plugin-vue-layouts"
import Vue from "@vitejs/plugin-vue"
import VueRouter from "unplugin-vue-router/vite"
import Vuetify, { transformAssetUrls } from "vite-plugin-vuetify"
import { defineConfig, loadEnv } from "vite"
import { fileURLToPath, URL } from "node:url"

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "VITE")
  return {
    plugins: [
      VueRouter({
        dts: "src/ring/typed-router.d.ts",
        routesFolder: "src/ring/pages"
      }),
      Layouts({
        layoutsDirs: "src/ring/layouts"
      }),
      AutoImport({
        imports: [
          "vue",
          {
            "vue-router/auto": ["useRoute", "useRouter"]
          }
        ],
        dts: "src/ring/auto-imports.d.ts",
        eslintrc: {
          enabled: true
        },
        vueTemplate: true
      }),
      Components({
        dts: "src/ring/components.d.ts",
        dirs: ["src/ring/components"]
      }),
      Vue({
        template: { transformAssetUrls }
      }),
      Vuetify({
        autoImport: true
      }),
      Fonts({
        google: {
          families: [
            {
              name: "Roboto",
              styles: "wght@100;300;400;500;700;900"
            }
          ]
        }
      })
    ],
    define: { "process.env": {} },
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src/ring", import.meta.url))
      },
      extensions: [".js", ".json", ".jsx", ".mjs", ".ts", ".tsx", ".vue"]
    },
    server: {
      port: 3000,
      proxy: {
        "/api": {
          target: env.VITE_API_URL,
          changeOrigin: true
        }
      },
      watch: {
        ignored: ["!src/ring/**"]
      }
    },
    css: {
      preprocessorOptions: {
        sass: {
          api: "modern-compiler"
        }
      }
    },
    build: {
      chunkSizeWarningLimit: 1024 * 1024
    }
  }
})
