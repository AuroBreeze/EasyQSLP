<template>
  <div class="avatar-upload-container">
    <div class="avatar-preview">
      <img 
        :src="avatar" 
        alt="用户头像"
        class="avatar-image"
      />
      <div v-if="uploading" class="upload-progress">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
        <span class="progress-text">{{ progress }}%</span>
      </div>
    </div>

    <div class="upload-controls">
      <label for="avatarInput" class="upload-btn">
        选择图片
        <input 
          id="avatarInput"
          type="file"
          accept="image/*"
          @change="handleFileChange"
          style="display: none;"
        />
      </label>
      <button 
        class="confirm-btn"
        :disabled="!selectedFile || uploading"
        @click="uploadAvatar"
      >
        {{ uploading ? '上传中...' : '确认上传' }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'
import type { AxiosProgressEvent } from 'axios'

const props = defineProps({
  avatar: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update'])

const selectedFile = ref<File | null>(null)
const uploading = ref(false)
const progress = ref(0)
const error = ref('')

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    
    // 验证文件类型
    if (!file.type.match('image.*')) {
      error.value = '请选择图片文件'
      return
    }

    // 验证文件大小 (限制2MB)
    if (file.size > 2 * 1024 * 1024) {
      error.value = '图片大小不能超过2MB'
      return
    }

    selectedFile.value = file
    error.value = ''

    // 预览图片
    const reader = new FileReader()
    reader.onload = (e) => {
      if (e.target) {
        emit('update', e.target.result as string)
      }
    }
    reader.readAsDataURL(file)
  }
}

const uploadAvatar = async () => {
  if (!selectedFile.value) return

  uploading.value = true
  progress.value = 0
  error.value = ''

  const formData = new FormData()
  formData.append('avatar', selectedFile.value)

  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.post('http://localhost:8000/api/v1/user/profile/revise/', formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent: AxiosProgressEvent) => {
        if (progressEvent.total) {
          progress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        }
      }
    })

    if (response.status === 200) {
      emit('update', response.data.avatar)
    } else {
      error.value = response.data?.message || '头像上传失败'
    }
  } catch (err) {
    console.error('上传头像失败:', err)
    error.value = '网络错误，请稍后重试'
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.avatar-upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.avatar-preview {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #FF4B2B;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 20px;
  background-color: rgba(0, 0, 0, 0.5);
}

.progress-bar {
  height: 100%;
  background-color: #FF4B2B;
  transition: width 0.3s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.upload-controls {
  display: flex;
  gap: 15px;
}

.upload-btn, .confirm-btn {
  border-radius: 20px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-btn {
  background-color: #2196F3;
  color: white;
  border: 1px solid #2196F3;
}

.upload-btn:hover {
  background-color: #1565C0;
}

.confirm-btn {
  background-color: #4CAF50;
  color: white;
  border: 1px solid #4CAF50;
}

.confirm-btn:hover {
  background-color: #2E7D32;
}

.confirm-btn:disabled {
  background-color: #cccccc;
  border-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
  padding: 8px 12px;
  background-color: #ffe6e6;
  border: 1px solid red;
  border-radius: 5px;
  text-align: center;
}
</style>
