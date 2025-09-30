<template>
  <nav class="breadcrumbs" aria-label="breadcrumb">
    <ol>
      <li v-for="(item, idx) in items" :key="idx">
        <template v-if="item.link">
          <router-link :to="item.link">{{ item.label }}</router-link>
        </template>
        <template v-else>
          <span>{{ item.label }}</span>
        </template>
      </li>
    </ol>
  </nav>
</template>

<script setup lang="ts">
interface Crumb { label: string; link?: string }
const props = defineProps<{ items: Crumb[] }>()
</script>

<style scoped>
.breadcrumbs { padding: 8px 16px; color: #666; }
.breadcrumbs ol { display: flex; gap: 8px; list-style: none; padding: 0; margin: 0; }
.breadcrumbs li::after { content: '/'; margin: 0 4px; color: #aaa; }
.breadcrumbs li:last-child::after { content: ''; }
.breadcrumbs a { color: #2563eb; text-decoration: none; }
</style>
