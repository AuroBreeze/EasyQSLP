<template>
  <div class="form-container sign-in-container">
    <form @submit.prevent="handleLogin">
      <h1>登录😃</h1>
      <span>账户密码登录</span>
      <div class="input-group">
        <input type="email" placeholder="邮箱" v-model="formData.email" />
        <label for="signinEmail">邮箱</label>
      </div>
      <div class="input-group">
        <input type="password" placeholder="密码" v-model="formData.password" />
        <label for="signinPassword">密码</label>
      </div>
      <a href="#" @click.prevent="handleForgotPassword">忘记密码?</a>
      <button>登录</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';

export default defineComponent({
  name: 'Login',
  setup() {
    const formData = reactive({
      email: '',
      password: ''
    });

    const handleLogin = async () => {
      // 登录逻辑
    };

    const handleForgotPassword = () => {
      // 处理忘记密码逻辑
    };

    return {
      formData,
      handleLogin,
      handleForgotPassword
    };
  }
});
</script>

<style scoped>
/* 保留原有样式 */
</style>