<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import HeroBanner from '@/components/HeroBanner.vue'
import { highlights } from '@/data/shows'

const route = useRoute()

const content = computed(() => {
  const id = String(route.params.id || '')
  return highlights.find(h => h.id === id) || highlights[0]
})

const items = computed(() => highlights)
</script>

<template>
  <section class="topic-detail">
    <HeroBanner v-if="content" :model-value="content && content.id" :content="content" :items="items" />
  </section>
</template>

<style scoped>
.topic-detail {
  height: 100%;
}
</style>
