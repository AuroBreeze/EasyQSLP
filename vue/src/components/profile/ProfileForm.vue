<template>
  <div class="profile-form-container">
    <form @submit.prevent="handleSubmit">
      <h3>编辑个人资料</h3>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div class="input-group">
        <input
          type="text"
          placeholder="用户名"
          id="username"
          v-model="formData.username"
          required
        />
        <label for="username">用户名</label>
      </div>

      <div class="input-group">
        <input
          type="email"
          placeholder="邮箱"
          id="email"
          v-model="formData.email"
          required
        />
        <label for="email">邮箱</label>
      </div>

      <div class="input-group">
        <select
          id="sex"
          v-model="formData.sex"
        >
          <option value="" disabled selected>请选择性别</option>
          <option value="MALE">男</option>
          <option value="FEMALE">女</option>
          <option value="OTHER">其他</option>
        </select>
        <label for="sex">性别</label>
      </div>

      <div class="input-group">
        <input
          type="date"
          placeholder="生日"
          id="birthday"
          v-model="formData.birthday"
        />
        <label for="birthday">生日</label>
      </div>

      <div class="input-group">
        <input
          type="text"
          placeholder="学校"
          id="school"
          v-model="formData.school"
        />
        <label for="school">学校</label>
      </div>

      <div class="input-group">
        <textarea
          placeholder="自我介绍"
          id="introduction"
          v-model="formData.introduction"
          rows="3"
        ></textarea>
        <label for="introduction">自我介绍</label>
      </div>

      <div class="form-actions">
        <button type="submit" class="submit-btn">保存</button>
        <button type="button" class="cancel-btn" @click="handleCancel">取消</button>
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formData = reactive({
  username: props.user.username,
  email: props.user.email,
  sex: props.user.sex || '',
  birthday: props.user.birthday || '',
  school: props.user.school || '',
  introduction: props.user.introduction || ''
})

const error = ref('')

  // 当props.user变化时更新表单数据
  watch(() => props.user, (newUser) => {
    formData.username = newUser.username
    formData.email = newUser.email
    formData.sex = newUser.sex || ''
    formData.birthday = newUser.birthday || ''
    formData.school = newUser.school || ''
    formData.introduction = newUser.introduction || ''
  }, { deep: true })

const handleSubmit = () => {
  // 基本验证
  if (!formData.username.trim()) {
    error.value = '用户名不能为空'
    return
  }

  if (!formData.email.trim()) {
    error.value = '邮箱不能为空'
    return
  }

  // 简单的邮箱格式验证
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(formData.email)) {
    error.value = '请输入有效的邮箱地址'
    return
  }

  error.value = ''
  emit('submit', formData)
}

const handleCancel = () => {
  // 重置表单为原始值
  formData.username = props.user.username
  formData.email = props.user.email
  error.value = ''
  emit('cancel')
}
</script>

<style scoped>
.profile-form-container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.1),
    0 10px 10px rgba(0, 0, 0, 0.08);
  padding: 30px;
  width: 100%;
  max-width: 500px;
  margin: 30px auto;
}

.profile-form-container h3 {
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

/* 继承自Sign.vue的样式 */
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
