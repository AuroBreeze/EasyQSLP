<template>
  <div>
    <button type="button" @click="handleSendCode">获取验证码</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'EmailSend',
  setup() {
    const handleSendCode = async () => {
      // 发送验证码逻辑
    };

    return {
      handleSendCode
    };
  }
});
</script>

<style scoped>
/* 保留原有样式 */
</style>