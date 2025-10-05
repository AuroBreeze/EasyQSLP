<template>
  <article class="card">
    <img :src="poster" :alt="title" loading="lazy" />
    <div class="card-overlay">
      <h3>{{ title }}</h3>
      <p>{{ subtitle }}</p>
      <div class="meta">
        <span>{{ rating }}</span>
        <span>·</span>
        <span>{{ year }}</span>
      </div>
    </div>
  </article>
</template>

<script setup>
const props = defineProps({
  title: String,
  subtitle: String,
  poster: String,
  rating: String,
  year: String,
})
</script>

<style scoped>
.card {
  position: relative;
  width: 200px;
  flex: 0 0 auto;
  border-radius: 0;
  overflow: hidden;
  background: #1b1b1b;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card img {
  width: 100%;
  height: 120px;
  object-fit: cover;
  display: block;
}

.card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 24px 40px -24px rgba(0, 0, 0, 0.85);
}

.card-overlay {
  padding: 12px;
  color: #fff;
  background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.85) 100%);
}

.card h3 {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 600;
}

.card p {
  margin: 0 0 6px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
}

.meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
}
</style>
