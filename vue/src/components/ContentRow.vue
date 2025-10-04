<template>
  <section class="row">
    <header class="row-header">
      <h2>{{ title }}</h2>
      <button type="button">查看全部</button>
    </header>
    <div class="row-content">
      <ContentCard
        v-for="item in items"
        :key="item.id"
        :title="item.title"
        :subtitle="item.subtitle"
        :poster="item.poster"
        :rating="item.rating"
        :year="item.year"
      />
    </div>
  </section>
</template>

<script setup>
import ContentCard from './ContentCard.vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  items: {
    type: Array,
    default: () => [],
  },
})
</script>

<style scoped>
.row {
  display: flex;
  flex-direction: column;
  gap: 16px;
  color: #fff;
}

.row-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.row-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
}

.row-header button {
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  cursor: pointer;
  transition: color 0.2s ease;
}

.row-header button:hover {
  color: rgba(255, 255, 255, 0.85);
}

.row-content {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 12px;
  scrollbar-width: thin;
}

.row-content::-webkit-scrollbar {
  height: 8px;
}

.row-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0;
}
</style>
