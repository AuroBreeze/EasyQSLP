<template>
  <div class="page-container">
    <!-- 波浪背景容器 -->
    <WaveBackground />
    <div class="content-wrapper">
      <h2>个人资料管理</h2>
      <div class="profile-container">
        <!-- 头像区域 -->
        <AvatarUpload :avatar="user.avatar" @update="handleAvatarUpdate" />
        
        <!-- 基本信息展示 -->
        <div class="info-card">
          <div class="info-item">
            <span class="info-label">用户名:</span>
            <span class="info-value">{{ user.username }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">邮箱:</span>
            <span class="info-value">{{ user.email }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">注册时间:</span>
            <span class="info-value">{{ formatDate(user.join_date) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">性别:</span>
            <span class="info-value">{{ 
              user.sex === 'MALE' ? '男' : 
              user.sex === 'FEMALE' ? '女' : 
              user.sex === 'OTHER' ? '其他' : '未设置'
            }}</span>
          </div>
          <div class="info-item" v-if="user.birthday">
            <span class="info-label">生日:</span>
            <span class="info-value">{{ formatDate(user.birthday) }}</span>
          </div>
          <div class="info-item" v-if="user.school">
            <span class="info-label">学校:</span>
            <span class="info-value">{{ user.school }}</span>
          </div>
          <div class="info-item" v-if="user.introduction">
            <span class="info-label">自我介绍:</span>
            <span class="info-value">{{ user.introduction }}</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button class="edit-btn" @click="showEditForm">编辑资料</button>
          <button class="change-password-btn" @click="showPasswordForm">修改密码</button>
        </div>
      </div>

      <!-- 编辑资料表单 -->
      <ProfileForm 
        v-if="showEdit"
        :user="user"
        @submit="handleProfileUpdate"
        @cancel="hideEditForm"
      />

      <!-- 修改密码表单 -->
      <div v-if="showPassword" class="password-form-container">
        <form @submit.prevent="handlePasswordChange">
          <h3>修改密码</h3>
          
          <div v-if="passwordError" class="error-message">
            {{ passwordError }}
          </div>

          <div class="input-group">
            <input 
              type="password" 
              placeholder="当前密码" 
              id="currentPassword" 
              v-model="passwordData.current_password" 
            />
            <label for="currentPassword">当前密码</label>
          </div>

          <div class="input-group">
            <input 
              type="password" 
              placeholder="新密码" 
              id="newPassword" 
              v-model="passwordData.new_password" 
            />
            <label for="newPassword">新密码</label>
          </div>

          <div class="input-group">
            <input 
              type="password" 
              placeholder="确认新密码" 
              id="confirmPassword" 
              v-model="passwordData.new_password_confirm" 
            />
            <label for="confirmPassword">确认新密码</label>
          </div>

          <div class="form-actions">
            <button type="submit" class="submit-btn">确认修改</button>
            <button type="button" class="cancel-btn" @click="hidePasswordForm">取消</button>
          </div>
        </form>
      </div>

      <!-- 操作成功提示 -->
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import WaveBackground from '@/components/background/WaveBackground.vue'
import AvatarUpload from '@/components/profile/AvatarUpload.vue'
import ProfileForm from '@/components/profile/ProfileForm.vue'
//import { parseJWT } from '@/utils/jwt'

const router = useRouter()
const route = useRoute()
const userId = ref(Number(route.params.id) || 0)

// 用户数据
const user = reactive({
  username: '',
  email: '',
  avatar: '',
  join_date: '',
  birthday: '',
  introduction: '',
  school:'',
  sex:'',
  user_Login: ''
})

// 密码修改数据
const passwordData = reactive({
  current_password: '',
  new_password: '',
  new_password_confirm: ''
})

const showEdit = ref(false)
const showPassword = ref(false)
const passwordError = ref('')
const successMessage = ref('')

// 初始化加载用户数据
const loadUserData = async () => {
  try {
    //console.log('开始加载用户数据...')
    const token = localStorage.getItem('access_token')
    //console.log('获取到的token:', token)
    
    if (!token) {
      //console.warn('未找到access_token，跳转到登录页')
      router.push('/login')
      return
    }
    
    // 解析token获取用户信息
   // const payload = parseJWT(token)
    //console.log('解析的token payload:', payload)
    
    const response = await fetch(`http://localhost:8000/api/v1/user/profile/${userId.value}/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    //console.log('API响应状态:', response.status)

    if (response.ok) {
      const data = await response.json()
      //console.log(data)
      Object.assign(user, data.data)
    } else {
      // 处理未授权等情况
      if (response.status === 401) {
        router.push('/login')
      }
    }
  } catch (error) {
    console.error('获取用户资料失败:', error)
  }
}

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 显示/隐藏编辑表单
const showEditForm = () => {
  showEdit.value = true
  showPassword.value = false
}

const hideEditForm = () => {
  showEdit.value = false
}

// 显示/隐藏密码表单
const showPasswordForm = () => {
  showPassword.value = true
  showEdit.value = false
  passwordError.value = ''
  passwordData.current_password = ''
  passwordData.new_password = ''
  passwordData.new_password_confirm = ''
}

const hidePasswordForm = () => {
  showPassword.value = false
}

// 处理头像更新
const handleAvatarUpdate = (newAvatar: string) => {
  user.avatar = newAvatar
  showSuccess('头像更新成功')
}

// 处理资料更新
const handleProfileUpdate = async (updatedData: any) => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/api/user/profile/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updatedData)
    })

    if (response.ok) {
      const data = await response.json()
      Object.assign(user, data)
      showEdit.value = false
      showSuccess('资料更新成功')
    } else {
      const errorData = await response.json()
      // 处理错误响应
    }
  } catch (error) {
    console.error('更新用户资料失败:', error)
  }
}

// 处理密码修改
const handlePasswordChange = async () => {
  if (passwordData.new_password !== passwordData.new_password_confirm) {
    passwordError.value = '两次输入的新密码不一致'
    return
  }

  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/api/v1/user/password/', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        old_password: passwordData.current_password,
        new_password: passwordData.new_password
      })
    })

    if (response.ok) {
      showPassword.value = false
      showSuccess('密码修改成功')
    } else {
      const errorData = await response.json()
      passwordError.value = errorData.message || '密码修改失败'
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    passwordError.value = '网络错误，请稍后重试'
  }
}

// 显示成功消息
const showSuccess = (message: string) => {
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

//组件挂载时加载用户数据
onMounted(async () => {
  console.log('ProfileView组件挂载')
  try {
    await loadUserData()
    console.log('用户数据加载完成:', user)
    // 如果API没有返回username/email，从token中获取
  } catch (error) {
    console.error('加载用户数据出错:', error)
  }
})
</script>

<style scoped>
.profile-container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.1),
    0 10px 10px rgba(0, 0, 0, 0.08);
  padding: 30px;
  width: 100%;
  max-width: 800px;
  margin: 20px auto;
}

.info-card {
  margin: 30px 0;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.info-item {
  display: flex;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.info-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.info-label {
  font-weight: bold;
  color: #555;
  width: 100px;
}

.info-value {
  color: #333;
  flex: 1;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

button {
  border-radius: 20px;
  border: 1px solid #FF4B2B;
  background-color: #FF4B2B;
  color: #FFFFFF;
  font-size: 12px;
  font-weight: bold;
  padding: 12px 20px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
  cursor: pointer;
}

button:hover {
  background-color: #FF416C;
}

button:active {
  transform: scale(0.95);
}

.edit-btn {
  background: linear-gradient(to right, #4CAF50, #2E7D32);
  border-color: #2E7D32;
}

.edit-btn:hover {
  background: linear-gradient(to right, #2E7D32, #1B5E20);
}

.change-password-btn {
  background: linear-gradient(to right, #2196F3, #1565C0);
  border-color: #1565C0;
}

.change-password-btn:hover {
  background: linear-gradient(to right, #1565C0, #0D47A1);
}

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
}

.cancel-btn {
  background: #999;
  border-color: #999;
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

.success-message {
  color: #28a745;
  font-size: 14px;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #e6ffe6;
  border: 1px solid #28a745;
  border-radius: 5px;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
}

/* 输入框组样式 - 与Sign.vue保持一致 */
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
