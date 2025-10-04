<template>
  <section class="drawer">
    <div class="drawer-header">
      <h2>正在浏览</h2>
    </div>
    <div class="poster-track">
      <button
        v-for="item in items"
        :key="item.id"
        type="button"
        :class="['poster-button', { active: item.id === modelValue }]"
        @click="$emit('update:modelValue', item.id)"
      >
        <img :src="item.poster" :alt="item.title" loading="lazy" />
        <span>{{ item.title }}</span>
      </button>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  modelValue: {
    type: String,
    default: null,
  },
})
</script>

<style scoped>
.drawer {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 16px;
  height: 100%;
  padding: 16px 0 12px;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.65) 0%, rgba(0, 0, 0, 0.95) 100%);
}

.drawer-header h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
  letter-spacing: 6px;
  text-transform: uppercase;
}

.poster-track {
  display: flex;
  gap: 18px;
  overflow-x: auto;
  padding: 4px 0 12px;
  scrollbar-width: thin;
}

.poster-track::-webkit-scrollbar {
  height: 6px;
}

.poster-track::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 0;
}

.poster-button {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 140px;
  border: none;
  padding: 0;
  background: transparent;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.65);
  transition: transform 0.2s ease, color 0.2s ease;
}

.poster-button img {
  width: 100%;
  height: 210px;
  object-fit: cover;
  border: 3px solid transparent;
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.poster-button span {
  font-size: 14px;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.poster-button:hover {
  color: #fff;
  transform: translateY(-4px);
}

.poster-button:hover img {
  transform: scale(1.02);
}

.poster-button.active img {
  border-color: #ffffff;
}

.poster-button.active {
  color: #fff;
}
</style>
