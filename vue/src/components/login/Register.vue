<template>
  <div class="form-container sign-up-container">
    <form @submit.prevent="handleRegister">
      <h1>创建账户😀</h1>
      <span>使用邮箱注册</span>
      <div class="input-group">
        <input type="text" placeholder="姓名" v-model="formData.name" />
        <label for="nameInput">姓名</label>
      </div>
      <div style="display: flex; align-items: center;">
        <div class="input-group" style="flex-grow: 1;">
          <input type="email" placeholder="邮箱" v-model="formData.email" />
          <label for="signupEmail">邮箱</label>
        </div>
        <button type="button" @click="handleGetCode">获取验证码</button>
      </div>
      <div class="input-group">
        <input type="text" placeholder="验证码" v-model="formData.code" />
        <label for="signupCode">验证码</label>
      </div>
      <div class="input-group">
        <input type="password" placeholder="密码" v-model="formData.password" />
        <label for="signupPassword">密码</label>
      </div>
      <button>注册</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';

export default defineComponent({
  name: 'Register',
  setup() {
    const formData = reactive({
      name: '',
      email: '',
      code: '',
      password: ''
    });

    const handleRegister = async () => {
      // 注册逻辑
    };

    const handleGetCode = async () => {
      // 获取验证码逻辑
    };

    return {
      formData,
      handleRegister,
      handleGetCode
    };
  }
});
</script>

<style scoped>
/* 保留原有样式 */
</style>