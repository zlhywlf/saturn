<script setup>
const props = defineProps({ item: Object, level: Number })
</script>

<template>
  <v-list-group no-action>
    <template v-slot:activator="{ props }">
      <v-list-item v-bind="props" :value="item.title" rounded class="mb-1" color="primary">
        <template v-slot:prepend>
          <component :is="item.icon" class="iconClass" :level="level"></component>
        </template>
        <v-list-item-title class="mr-auto">{{ item.title }}</v-list-item-title>
        <v-list-item-subtitle v-if="item.subCaption" class="text-caption mt-n1 hide-menu">
          {{ item.subCaption }}
        </v-list-item-subtitle>
      </v-list-item>
    </template>
    <template v-for="(subitem, i) in item.children" :key="i">
      <NavCollapse :item="subitem" v-if="subitem.children" :level="props.level + 1" />
      <NavItem :item="subitem" :level="props.level + 1" v-else></NavItem>
    </template>
  </v-list-group>
</template>
