<template>
  <section class="card">
    <h2>{{ msg }}</h2>
    <p>开始构建你的第一个 Vue 组件吧！</p>
    <button type="button" @click="count++">当前点击次数：{{ count }}</button>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  msg: {
    type: String,
    required: true,
  },
})

const count = ref(0)
</script>

<style scoped>

.card {
  margin-top: 2rem;
  padding: 1.5rem;
  border-radius: 0;
  background: #f6f8fa;
  box-shadow: 0 10px 30px -20px rgba(15, 23, 42, 0.35);
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1.2rem;
  border-radius: 0;
  border: none;
  background-color: #42b983;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 24px -16px rgba(66, 185, 131, 0.6);
}
</style>
