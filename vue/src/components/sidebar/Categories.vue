<template>
  <section class="panel">
    <h3 class="panel-title">📂 分类导航</h3>
    <ul class="tree">
      <li v-for="node in trees" :key="node.id">
        <div class="node" @click="$emit('select', node.id)">{{ node.name }}</div>
        <ul v-if="node.children?.length" class="children">
          <li v-for="c in node.children" :key="c.id">
            <div class="node child" @click.stop="$emit('select', c.id)">{{ c.name }}</div>
          </li>
        </ul>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { CategoryNode } from '@/utils/home/homeService'
const props = defineProps<{ trees: CategoryNode[] }>()
const emit = defineEmits<{ (e: 'select', id: number): void }>()
</script>

<style scoped>
.panel { background: #fff; border: 1px solid #eee; border-radius: 12px; padding: 12px; }
.panel-title { margin: 0 0 8px; font-size: 16px; }
.tree { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
.node { cursor: pointer; padding: 6px 8px; border-radius: 8px; }
.node:hover { background: #f9fafb; }
.child { padding-left: 18px; }
.children { list-style: none; margin: 4px 0 0 0; padding: 0; display: grid; gap: 4px; }
</style>
