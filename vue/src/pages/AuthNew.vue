<script setup lang="ts">
import { reactive, ref, onMounted, nextTick, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AuthBackdrop from '@/components/AuthBackdrop.vue'
import { 
  apiLogin,
  apiRegister,
  apiSendRegisterCode,
  apiSendForgotPasswordCode,
  checkEmailExists as apiCheckEmailExists
} from '@/services/realApi'

const router = useRouter()
const route = useRoute()

// 页面状态
const pageState = ref<'email-input' | 'login' | 'register-step1' | 'register-step2' | 'register-step3' | 'verify-email' | 'user-confirm' | 'forgot-password' | 'reset-password'>('email-input')
const authMode = ref<'login' | 'register'>('login')

// 表单数据
const emailForm = reactive({
  email: '',
})

const loginForm = reactive({
  email: '',
  password: '',
  remember: true,
})

const registerForm = reactive({
  email: '',
  password: '',
  confirm: '',
  username: '',
  birthYear: '',
  birthMonth: '',
  birthDay: '',
  gender: 'male',
})

const verifyForm = reactive({
  code: ['', '', '', '', '', ''],
  email: '',
})

const userConfirm = reactive({
  user: null as any,
  confirmed: false,
})

const forgotForm = reactive({
  email: '',
})

const resetForm = reactive({
  email: '',
  code: '',
  password: '',
  confirm: '',
})

// 状态管理
const loading = ref(false)
const emailVerifying = ref(false)
const errorMsg = ref('')
const infoMsg = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const countdown = ref(0)
const isAnimating = ref(false)
const emailExists = ref(false)
const registeredEmails = ref(new Set<string>())

// 注册步骤状态
const registerStep = ref(1)
const isTermsScrolledToBottom = ref(false)
const passwordStrength = reactive({
  hasLetter: false,
  hasNumberOrSymbol: false,
  hasMinLength: false,
})

// 辅助函数
function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

function checkPasswordStrength(password: string) {
  passwordStrength.hasLetter = /[a-zA-Z]/.test(password)
  passwordStrength.hasNumberOrSymbol = /[\d!@#$%^&*(),.?":{}|<>]/.test(password)
  passwordStrength.hasMinLength = password.length >= 10
}

function getYearOptions() {
  const currentYear = new Date().getFullYear()
  const years = []
  for (let i = currentYear; i >= currentYear - 100; i--) {
    years.push(i.toString())
  }
  return years
}

function getMonthOptions() {
  return [
    '一月', '二月', '三月', '四月', '五月', '六月',
    '七月', '八月', '九月', '十月', '十一月', '十二月'
  ]
}

function getDayOptions() {
  const days = []
  for (let i = 1; i <= 31; i++) {
    days.push(i.toString().padStart(2, '0'))
  }
  return days
}

function nextRegisterStep() {
  if (registerStep.value < 3) {
    registerStep.value++
    updateRegisterPageState()
  }
}

function prevRegisterStep() {
  if (registerStep.value > 1) {
    registerStep.value--
    updateRegisterPageState()
  }
}

function updateRegisterPageState() {
  if (registerStep.value === 1) {
    pageState.value = 'register-step1'
  } else if (registerStep.value === 2) {
    pageState.value = 'register-step2'
  } else if (registerStep.value === 3) {
    pageState.value = 'register-step3'
  }
}

function handleTermsScroll(event: Event) {
  const target = event.target as HTMLElement
  const isAtBottom = target.scrollTop + target.clientHeight >= target.scrollHeight - 10
  isTermsScrolledToBottom.value = isAtBottom
}

function switchState(newState: typeof pageState.value) {
  if (isAnimating.value) return
  
  errorMsg.value = ''
  infoMsg.value = ''
  isAnimating.value = true
  
  setTimeout(() => {
    pageState.value = newState
    isAnimating.value = false
  }, 300)
}

// 注册步骤处理函数
function handleRegisterStep1() {
  if (loading.value) return
  
  errorMsg.value = ''
  
  if (!registerForm.password) {
    errorMsg.value = '请输入密码'
    return
  }
  
  if (registerForm.password !== registerForm.confirm) {
    errorMsg.value = '两次输入的密码不一致'
    return
  }
  
  if (!passwordStrength.hasLetter || !passwordStrength.hasNumberOrSymbol || !passwordStrength.hasMinLength) {
    errorMsg.value = '密码强度不符合要求'
    return
  }
  
  nextRegisterStep()
}

function handleRegisterStep2() {
  if (loading.value) return
  
  errorMsg.value = ''
  
  if (!registerForm.username.trim()) {
    errorMsg.value = '请输入用户名'
    return
  }
  
  if (!registerForm.birthYear || !registerForm.birthMonth || !registerForm.birthDay) {
    errorMsg.value = '请选择完整的出生日期'
    return
  }
  
  nextRegisterStep()
}

async function handleRegisterStep3() {
  if (loading.value) return
  
  errorMsg.value = ''
  
  if (!isTermsScrolledToBottom.value) {
    errorMsg.value = '请先阅读完所有条款与条件'
    return
  }
  
  loading.value = true
  
  try {
    await apiSendRegisterCode(registerForm.email)
    
    verifyForm.email = registerForm.email
    verifyForm.code = ['', '', '', '', '', '']
    switchState('verify-email')
    infoMsg.value = `验证码已发送到 ${registerForm.email}`
    
  } catch (err) {
    console.error('发送验证码失败:', err)
    errorMsg.value = '发送验证码失败，请稍后再试'
  } finally {
    loading.value = false
  }
}

// 监听密码变化
watch(() => registerForm.password, (newPassword) => {
  checkPasswordStrength(newPassword)
})

watch(() => registerForm.confirm, () => {
  if (registerForm.confirm && registerForm.password !== registerForm.confirm) {
    errorMsg.value = '两次输入的密码不一致'
  } else {
    errorMsg.value = ''
  }
})

// 提交处理
function onSubmit() {
  switch (pageState.value) {
    case 'register-step1':
      handleRegisterStep1()
      break
    case 'register-step2':
      handleRegisterStep2()
      break
    case 'register-step3':
      handleRegisterStep3()
      break
  }
}
</script>

<template>
  <section class="auth-page">
    <AuthBackdrop />
    
    <div class="auth-container">
      <Transition name="page" mode="out-in">
        <div key="auth-card" class="auth-card">
          
          <!-- 注册步骤1：创建密码 -->
          <template v-if="pageState === 'register-step1'">
            <div class="auth-header">
              <button class="back-btn" @click="switchState('email-input')">
                <i class="back-icon">←</i>
              </button>
              <div class="step-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: '33%' }"></div>
                </div>
                <p class="step-text">第1步，共3步</p>
              </div>
              <h1 class="auth-title">创建密码</h1>
            </div>

            <div class="auth-body">
              <Transition name="message">
                <div v-if="infoMsg" class="message message--info">{{ infoMsg }}</div>
              </Transition>
              <Transition name="message">
                <div v-if="errorMsg" class="message message--error">{{ errorMsg }}</div>
              </Transition>

              <form class="auth-form" @submit.prevent="onSubmit">
                <div class="form-group">
                  <label class="form-label">密码</label>
                  <div class="input-wrapper">
                    <input
                      v-model="registerForm.password"
                      :type="showPassword ? 'text' : 'password'"
                      class="form-input"
                      placeholder="请输入密码"
                      required
                    />
                    <button
                      type="button"
                      class="password-toggle"
                      @click="showPassword = !showPassword"
                    >
                      {{ showPassword ? '🙈' : '👁' }}
                    </button>
                  </div>
                </div>

                <div class="form-group">
                  <div class="input-wrapper">
                    <input
                      v-model="registerForm.confirm"
                      :type="showConfirmPassword ? 'text' : 'password'"
                      class="form-input"
                      placeholder="请确认密码"
                      required
                    />
                    <button
                      type="button"
                      class="password-toggle"
                      @click="showConfirmPassword = !showConfirmPassword"
                    >
                      {{ showConfirmPassword ? '🙈' : '👁' }}
                    </button>
                  </div>
                </div>

                <div class="password-requirements">
                  <p class="requirements-title">密码须至少包含</p>
                  <div class="requirement-item" :class="{ 'requirement-met': passwordStrength.hasLetter }">
                    <span class="requirement-icon">{{ passwordStrength.hasLetter ? '✅' : '⭕' }}</span>
                    <span>1个字母</span>
                  </div>
                  <div class="requirement-item" :class="{ 'requirement-met': passwordStrength.hasNumberOrSymbol }">
                    <span class="requirement-icon">{{ passwordStrength.hasNumberOrSymbol ? '✅' : '⭕' }}</span>
                    <span>1个数字或特殊字符（例如：#?!&）</span>
                  </div>
                  <div class="requirement-item" :class="{ 'requirement-met': passwordStrength.hasMinLength }">
                    <span class="requirement-icon">{{ passwordStrength.hasMinLength ? '✅' : '⭕' }}</span>
                    <span>10个字符</span>
                  </div>
                </div>

                <button
                  type="submit"
                  class="submit-btn"
                  :disabled="loading"
                >
                  下一步
                </button>
              </form>
            </div>
          </template>

          <!-- 注册步骤2：个人信息 -->
          <template v-else-if="pageState === 'register-step2'">
            <div class="auth-header">
              <button class="back-btn" @click="prevRegisterStep">
                <i class="back-icon">←</i>
              </button>
              <div class="step-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: '66%' }"></div>
                </div>
                <p class="step-text">第2步，共3步</p>
              </div>
              <h1 class="auth-title">介绍一下自己</h1>
            </div>

            <div class="auth-body">
              <Transition name="message">
                <div v-if="errorMsg" class="message message--error">{{ errorMsg }}</div>
              </Transition>

              <form class="auth-form" @submit.prevent="onSubmit">
                <div class="form-group">
                  <label class="form-label">名称</label>
                  <p class="form-desc">此名称会显示在你的个人资料上</p>
                  <input
                    v-model="registerForm.username"
                    type="text"
                    class="form-input"
                    placeholder="请输入用户名"
                    required
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">出生日期</label>
                  <p class="form-desc">为什么我们需要你提供出生日期？了解更多。</p>
                  <div class="date-group">
                    <select v-model="registerForm.birthYear" class="date-select" required>
                      <option value="">年份</option>
                      <option v-for="year in getYearOptions()" :key="year" :value="year">{{ year }}</option>
                    </select>
                    <select v-model="registerForm.birthMonth" class="date-select" required>
                      <option value="">月份</option>
                      <option v-for="(month, index) in getMonthOptions()" :key="index" :value="index + 1">{{ month }}</option>
                    </select>
                    <select v-model="registerForm.birthDay" class="date-select" required>
                      <option value="">日</option>
                      <option v-for="day in getDayOptions()" :key="day" :value="day">{{ day }}</option>
                    </select>
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">性别</label>
                  <p class="form-desc">我们会根据你的性别来推送个性化精选推荐内容和广告。</p>
                  <div class="gender-options">
                    <label class="gender-option">
                      <input v-model="registerForm.gender" type="radio" value="male" />
                      <span class="gender-label">男</span>
                    </label>
                    <label class="gender-option">
                      <input v-model="registerForm.gender" type="radio" value="female" />
                      <span class="gender-label">女</span>
                    </label>
                  </div>
                </div>

                <button type="submit" class="submit-btn">下一步</button>
              </form>
            </div>
          </template>

          <!-- 注册步骤3：条款与条件 -->
          <template v-else-if="pageState === 'register-step3'">
            <div class="auth-header">
              <button class="back-btn" @click="prevRegisterStep">
                <i class="back-icon">←</i>
              </button>
              <div class="step-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: '100%' }"></div>
                </div>
                <p class="step-text">第3步，共3步</p>
              </div>
              <h1 class="auth-title">条款与条件</h1>
            </div>

            <div class="auth-body">
              <Transition name="message">
                <div v-if="errorMsg" class="message message--error">{{ errorMsg }}</div>
              </Transition>

              <div class="terms-content" @scroll="handleTermsScroll">
                <div class="terms-section">
                  <h3>服务条款</h3>
                  <p>欢迎使用我们的服务。使用我们的服务即表示您同意这些条款。请仔细阅读。</p>
                  
                  <h4>使用我们的服务</h4>
                  <p>您必须遵守我们服务中提供的所有政策。请勿滥用我们的服务。例如，请勿干扰我们的服务或尝试使用除我们提供的界面和说明以外的方法访问这些服务。</p>
                  
                  <h4>您的账户</h4>
                  <p>您可能需要一个账户才能使用我们的某些服务。您可以创建自己的账户，或者您的账户可能由管理员为您分配。</p>
                  
                  <h4>隐私和版权保护</h4>
                  <p>我们的隐私政策解释了我们在您使用我们的服务时如何处理您的个人数据和保护您的隐私。</p>
                  
                  <h4>服务的商业使用</h4>
                  <p>如果您代表企业使用我们的服务，该企业接受这些条款。</p>
                  
                  <h4>关于这些条款</h4>
                  <p>我们可能会修改这些条款或适用于某项服务的任何附加条款，例如，为了反映法律的变更或我们服务的变化。</p>
                </div>
              </div>

              <form class="auth-form" @submit.prevent="onSubmit">
                <button
                  type="submit"
                  class="submit-btn submit-btn--register"
                  :disabled="loading || !isTermsScrolledToBottom"
                >
                  <template v-if="!loading">
                    注册
                  </template>
                  <template v-else>
                    <div class="loading-dots">
                      <div class="dot"></div>
                      <div class="dot"></div>
                      <div class="dot"></div>
                    </div>
                    发送验证码中...
                  </template>
                </button>
              </form>
            </div>
          </template>

        </div>
      </Transition>
    </div>
  </section>
</template>

<style scoped>
/* 基础样式 */
.auth-page {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f1e 100%);
  overflow: hidden;
}

.auth-container {
  width: 100%;
  max-width: 500px;
  padding: 0 20px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.auth-card {
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 32px 64px rgba(0, 0, 0, 0.4);
}

.auth-header {
  padding: 40px 32px 32px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  text-align: center;
}

.back-btn {
  position: absolute;
  left: 20px;
  top: 20px;
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.step-progress {
  margin-bottom: 24px;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00d4aa, #00b894);
  transition: width 0.5s ease;
}

.step-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

.auth-title {
  color: #fff;
  font-size: 32px;
  font-weight: 700;
  margin: 0;
}

.auth-body {
  padding: 32px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.form-desc {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  color: #fff;
  font-size: 16px;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #00d4aa;
  background: rgba(255, 255, 255, 0.08);
}

.password-toggle {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  font-size: 18px;
}

.password-requirements {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
}

.requirements-title {
  color: #fff;
  font-size: 14px;
  margin: 0 0 12px;
  font-weight: 600;
}

.requirement-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.requirement-item.requirement-met {
  color: #00d4aa;
}

.requirement-icon {
  font-size: 16px;
}

.date-group {
  display: flex;
  gap: 12px;
}

.date-select {
  flex: 1;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 16px;
}

.gender-options {
  display: flex;
  gap: 24px;
}

.gender-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.gender-option input[type="radio"] {
  width: 20px;
  height: 20px;
  accent-color: #00d4aa;
}

.gender-label {
  color: #fff;
  font-size: 16px;
}

.terms-content {
  max-height: 300px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.terms-section h3 {
  color: #fff;
  font-size: 18px;
  margin: 0 0 16px;
}

.terms-section h4 {
  color: #00d4aa;
  font-size: 16px;
  margin: 16px 0 8px;
}

.terms-section p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 16px;
}

.submit-btn {
  width: 100%;
  padding: 20px;
  background: linear-gradient(135deg, #00d4aa, #00b894);
  border: none;
  border-radius: 16px;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0, 212, 170, 0.3);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-dots {
  display: flex;
  gap: 4px;
}

.dot {
  width: 8px;
  height: 8px;
  background: #fff;
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  } 40% {
    transform: scale(1);
  }
}

.message {
  padding: 16px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 20px;
}

.message--error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.message--info {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: #93c5fd;
}

/* 过渡动画 */
.page-enter-active,
.page-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: scale(0.95) translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: scale(1.05) translateY(-20px);
}

.message-enter-active,
.message-leave-active {
  transition: all 0.3s ease;
}

.message-enter-from {
  opacity: 0;
  transform: translateY(-30px) scale(0.9);
}

.message-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}
</style>
