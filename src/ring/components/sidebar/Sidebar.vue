<script setup lang="ts">
import { shallowRef, ref } from "vue"
import { DashboardOutlined, LoginOutlined } from "@ant-design/icons-vue"
import { useAppStore } from "@/stores/app"

interface menu {
  header?: string
  title?: string
  icon?: object
  to?: string
  divider?: boolean
  chip?: string
  chipColor?: string
  chipVariant?: string
  chipIcon?: string
  children?: menu[]
  disabled?: boolean
  type?: string
  subCaption?: string
}

const sidebarItems: menu[] = [
  { header: "Navigation" },
  {
    title: "Dashboard",
    icon: DashboardOutlined,
    to: "/dashboard"
  },
  { header: "Authentication" },
  {
    title: "Login",
    icon: LoginOutlined,
    to: "/login"
  }
]

const sidebarMenu = shallowRef(sidebarItems)
const appStore = useAppStore()
</script>

<template>
  <v-navigation-drawer
    left
    v-model="appStore.drawerSidebar"
    elevation="0"
    rail-width="60"
    mobile-breakpoint="lg"
    app
    class="leftSidebar"
    :rail="appStore.miniSidebar"
    expand-on-hover
  >
    <div class="pa-5">
      <v-img class="mb-4" height="150" src="@/assets/logo.svg" />
    </div>
    <perfect-scrollbar class="scrollnavbar">
      <v-list aria-busy="true" aria-label="menu list">
        <template v-for="(item, i) in sidebarMenu" :key="i">
          <NavGroup :item="item" v-if="item.header" :key="item.title" />
          <v-divider class="my-3" v-else-if="item.divider" />
          <NavCollapse class="leftPadding" :item="item" :level="0" v-else-if="item.children" />
          <NavItem :item="item" v-else />
        </template>
      </v-list>
      <div class="pa-4">
        <ExtraBox />
      </div>
    </perfect-scrollbar>
  </v-navigation-drawer>
</template>
