<template>
  <div class="page-container">
    <!-- 顶部导航栏 -->
    <TopNavBar />
    <!-- 波浪背景容器 -->
    <WaveBackground />
    <div class="content-wrapper">
      <!-- 左侧个人资料卡片 -->
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

      <!-- 右侧内容区域 -->
      <div class="right-content">
        <!-- 默认显示用户荣誉 -->
        <div class="user-honors" v-if="!showEdit && !showPassword">
          <h3>个人荣誉</h3>
          <div class="honor-item" v-for="honor in user.honors" :key="honor.id">
            <div class="honor-title">{{ honor.title }}</div>
            <div class="honor-date">{{ formatDate(honor.date) }}</div>
            <div class="honor-description">{{ honor.description }}</div>
          </div>
          <div v-if="!user.honors || user.honors.length === 0" class="no-honors">
            暂无荣誉记录
          </div>
        </div>

        <!-- 编辑资料表单 -->
        <div class="form-container" v-if="showEdit">
          <ProfileForm 
            :user="user"
            @submit="handleProfileUpdate"
            @cancel="hideEditForm"
          />
        </div>

        <!-- 修改密码表单 -->
        <div class="form-container" v-if="showPassword">
          <PasswordForm
            @submit="handlePasswordChange"
            @cancel="hidePasswordForm"
          />
        </div>
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
import TopNavBar from '@/components/navigation/TopNavBar.vue'
import { useRouter, useRoute } from 'vue-router'
import WaveBackground from '@/components/background/WaveBackground.vue'
import AvatarUpload from '@/components/profile/AvatarUpload.vue'
import ProfileForm from '@/components/profile/ProfileForm.vue'
import PasswordForm from '@/components/profile/PasswordForm.vue'

const router = useRouter()
const route = useRoute()
const userId = ref(Number(route.params.id) || 0)

interface Honor {
  id: number
  title: string
  date: string
  description: string
}

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
  user_Login: '',
  honors: [] as Honor[]
})

const showEdit = ref(false)
const showPassword = ref(false)
const successMessage = ref('')

// 初始化加载用户数据
const loadUserData = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
      return
    }
    
    const response = await fetch(`http://localhost:8000/api/v1/user/profile/${userId.value}/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data = await response.json()
      Object.assign(user, data.data)
    } else if (response.status === 401) {
      router.push('/login')
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
    }
  } catch (error) {
    console.error('更新用户资料失败:', error)
  }
}

// 处理密码修改
const handlePasswordChange = async (passwordData: { old_password: string, new_password: string }) => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/api/v1/user/password/', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(passwordData)
    })

    if (response.ok) {
      showPassword.value = false
      showSuccess('密码修改成功')
    } else {
      const errorData = await response.json()
      showSuccess(errorData.message || '密码修改失败')
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    showSuccess('网络错误，请稍后重试')
  }
}

// 显示成功消息
const showSuccess = (message: string) => {
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

onMounted(async () => {
  await loadUserData()
})
</script>

<style scoped>
.page-container {
  height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  margin-top: 60px;
  width: 100%;
}

.content-wrapper {
  flex: 1;
  padding: 20px;
  overflow: hidden;
  display: flex;
  gap: 20px;
  min-width: 0;
  width: 100%;
}

.profile-container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.1),
    0 10px 10px rgba(0, 0, 0, 0.08);
  padding: 30px;
  width: 400px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  flex-shrink: 0;
}

.right-content {
  flex: 1;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.1),
    0 10px 10px rgba(0, 0, 0, 0.08);
  padding: 30px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  margin-left: 20px;
  min-width: 0;
  width: 100%;
}

.user-honors {
  padding: 20px;
}

.honor-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.honor-title {
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 5px;
}

.honor-date {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}

.honor-description {
  color: #333;
}

.no-honors {
  color: #999;
  text-align: center;
  padding: 40px 0;
}

.form-container {
  padding: 20px;
}

/* 其他样式保持不变... */
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
</style>
