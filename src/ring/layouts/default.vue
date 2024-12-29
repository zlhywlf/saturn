<template>
  <v-app>
    <Sidebar />
    <Header />
    <v-main class="page-wrapper">
      <v-container fluid>
        <div>
          <LoaderWrapper />
          <router-view />
        </div>
      </v-container>
      <v-container fluid class="pt-0">
        <div>
          <FooterPanel />
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>
