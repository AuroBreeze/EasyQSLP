<template>
  <div class="password-form-container">
    <form @submit.prevent="handleSubmit">
      <h3>修改密码</h3>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div class="input-group">
        <input 
          type="password" 
          placeholder="当前密码" 
          id="currentPassword" 
          v-model="formData.current_password" 
          required
        />
        <label for="currentPassword">当前密码</label>
      </div>

      <div class="input-group">
        <input 
          type="password" 
          placeholder="新密码" 
          id="newPassword" 
          v-model="formData.new_password" 
          required
        />
        <label for="newPassword">新密码</label>
      </div>

      <div class="input-group">
        <input 
          type="password" 
          placeholder="确认新密码" 
          id="confirmPassword" 
          v-model="formData.new_password_confirm" 
          required
        />
        <label for="confirmPassword">确认新密码</label>
      </div>

      <div class="form-actions">
        <button type="submit" class="submit-btn">确认修改</button>
        <button type="button" class="cancel-btn" @click="handleCancel">取消</button>
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'

const emit = defineEmits(['submit', 'cancel'])

const formData = reactive({
  current_password: '',
  new_password: '',
  new_password_confirm: ''
})

const error = ref('')

const handleSubmit = () => {
  if (formData.new_password !== formData.new_password_confirm) {
    error.value = '两次输入的新密码不一致'
    return
  }

  if (formData.new_password.length < 6) {
    error.value = '密码长度不能少于6位'
    return
  }

  error.value = ''
  emit('submit', {
    old_password: formData.current_password,
    new_password: formData.new_password
  })
}

const handleCancel = () => {
  formData.current_password = ''
  formData.new_password = ''
  formData.new_password_confirm = ''
  error.value = ''
  emit('cancel')
}
</script>

<style scoped>
.password-form-container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.1),
    0 10px 10px rgba(0, 0, 0, 0.08);
  padding: 30px;
  width: 100%;
  max-width: 500px;
  margin: 30px auto;
}

.password-form-container h3 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 25px;
}

.submit-btn {
  background: linear-gradient(to right, #FF4B2B, #FF416C);
  border-radius: 20px;
  padding: 12px 20px;
  color: white;
  font-size: 14px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  background: linear-gradient(to right, #FF416C, #FF4B2B);
}

.cancel-btn {
  background: #999;
  border-radius: 20px;
  padding: 12px 20px;
  color: white;
  font-size: 14px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #777;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #ffe6e6;
  border: 1px solid red;
  border-radius: 5px;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
}

.input-group {
  position: relative;
  width: 100%;
  margin: 8px 0;
}

.input-group label {
  position: absolute;
  left: 15px;
  top: 12px;
  color: #999;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  font-size: 12px;
  background-color: transparent;
  padding: 0 5px;
  transform-origin: left center;
}

.input-group input {
  background-color: #eee;
  border: none;
  padding: 12px 15px;
  margin: 0;
  width: 100%;
  transition: all 0.3s ease;
}

.input-group input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 75, 43, 0.2);
}

.input-group input:focus + label,
.input-group input:not(:placeholder-shown) + label {
  transform: translateY(-22px) scale(0.85);
  color: #FF4B2B;
  background-color: white;
  padding: 0 5px;
  left: 10px;
}

.input-group input::placeholder {
  color: transparent;
  transition: color 0.3s ease;
}

.input-group input:focus {
  color: #999;
}
</style>
