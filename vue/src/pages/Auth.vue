<script setup lang="ts">
import { reactive, ref, onMounted, nextTick, onUnmounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AuthBackdrop from '@/components/AuthBackdrop.vue'
import { 
  apiLogin as mockApiLogin, 
  apiRegister as mockApiRegister 
} from '@/services/api'
import { 
  apiLogin,
  apiRegister,
  apiSendRegisterCode,
  apiSendForgotPasswordCode,
  checkEmailExists
} from '@/services/realApi'

const router = useRouter()
const route = useRoute()

// 页面状态：'email-input' | 'login' | 'register-step1' | 'register-step2' | 'register-step3' | 'verify-email' | 'user-confirm' | 'forgot-password' | 'reset-password'
const pageState = ref<'email-input' | 'login' | 'register-step1' | 'register-step2' | 'register-step3' | 'verify-email' | 'user-confirm' | 'forgot-password' | 'reset-password'>('email-input')
// 卡片切换的key：注册多步使用统一key，避免整卡片淡入淡出
const cardKey = computed(() => (['register-step1', 'register-step2', 'register-step3'].includes(pageState.value) ? 'register' : pageState.value))
const authMode = ref<'login' | 'register'>('login') // 当前认证模式

// 邮箱输入表单
const emailForm = reactive({
  email: '',
})

// 登录表单
const loginForm = reactive({
  email: '',
  password: '',
  remember: true,
})

// 注册表单
const registerForm = reactive({
  name: '',
  email: '',
  password: '',
  confirm: '',
  agree: false,
  birthYear: '',
  birthMonth: '',
  birthDay: '',
  gender: 'male',
})

// 注册步骤状态
const registerStep = ref(1)
const isTermsScrolledToBottom = ref(false)
const passwordStrength = reactive({
  hasLetter: false,
  hasNumberOrSymbol: false,
  hasMinLength: false,
})

// 验证码表单
const verifyForm = reactive({
  code: ['', '', '', '', '', ''],
  email: '',
})
// 隐藏验证码输入ref
const hiddenCodeInputRef = ref<HTMLInputElement | null>(null)

// 用户确认信息
const userConfirm = reactive({
  user: null as any,
  confirmed: false,
})

// 忘记密码表单
const forgotForm = reactive({
  email: '',
})

// 重置密码表单
const resetForm = reactive({
  email: '',
  code: '',
  password: '',
  confirm: '',
})

const loading = ref(false)
const emailVerifying = ref(false)
const errorMsg = ref('')
const infoMsg = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const countdown = ref(0)
const isAnimating = ref(false)
const emailExists = ref(false)
const registeredEmails = ref(new Set<string>()) // 防重复注册

// 倒计时定时器
let countdownTimer: number | null = null

onMounted(() => {
  // 根据路由meta或查询参数决定初始模式
  if (route.meta?.mode === 'register' || route.query.mode === 'register') {
    authMode.value = 'register'
  }
  
  if (typeof route.query.email === 'string') {
    emailForm.email = route.query.email
    loginForm.email = route.query.email
    registerForm.email = route.query.email
    forgotForm.email = route.query.email
    verifyForm.email = route.query.email
  }
  
  // 隐藏侧边栏
  document.body.classList.add('auth-fullscreen')
})

onUnmounted(() => {
  // 恢复侧边栏
  document.body.classList.remove('auth-fullscreen')
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})

// 邮箱格式验证
function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// 防重复注册检查
function checkDuplicateRegistration(email: string): boolean {
  return registeredEmails.value.has(email.toLowerCase())
}

async function switchState(newState: typeof pageState.value) {
  if (isAnimating.value) return
  
  isAnimating.value = true
  errorMsg.value = ''
  infoMsg.value = ''
  
  await nextTick()
  setTimeout(() => {
    pageState.value = newState
    isAnimating.value = false
    // 验证邮箱页：聚焦隐藏输入框，便于直接输入
    if (newState === 'verify-email') {
      nextTick(() => hiddenCodeInputRef.value?.focus())
    }
  }, 300)
}

// 启动倒计时
function startCountdown(seconds: number = 60) {
  countdown.value = seconds
  countdownTimer = window.setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer!)
      countdownTimer = null
    }
  }, 1000)
}

// 切换密码显示
function togglePasswordVisibility(field: 'password' | 'confirm') {
  if (field === 'password') {
    showPassword.value = !showPassword.value
  } else {
    showConfirmPassword.value = !showConfirmPassword.value
  }
}

// 密码强度检查
function checkPasswordStrength() {
  const password = registerForm.password
  passwordStrength.hasLetter = /[a-zA-Z]/.test(password)
  passwordStrength.hasNumberOrSymbol = /[\d!@#$%^&*(),.?":{}|<>]/.test(password)
  passwordStrength.hasMinLength = password.length >= 10
}

// 获取年份选项
function getYearOptions() {
  const currentYear = new Date().getFullYear()
  const years = []
  for (let i = currentYear; i >= currentYear - 100; i--) {
    years.push(i.toString())
  }
  return years
}

// 获取月份选项
function getMonthOptions() {
  return [
    '一月', '二月', '三月', '四月', '五月', '六月',
    '七月', '八月', '九月', '十月', '十一月', '十二月'
  ]
}

// 获取日期选项
function getDayOptions() {
  const days = []
  for (let i = 1; i <= 31; i++) {
    days.push(i.toString().padStart(2, '0'))
  }
  return days
}

// 注册步骤管理
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

// 条款滚动检查
function handleTermsScroll(event: Event) {
  const target = event.target as HTMLElement
  const isAtBottom = target.scrollTop + target.clientHeight >= target.scrollHeight - 10
  isTermsScrolledToBottom.value = isAtBottom
}

// 处理邮箱提交
async function handleEmailSubmit() {
  if (loading.value || emailVerifying.value) return
  
  const email = emailForm.email.trim()
  if (!email) {
    errorMsg.value = '请输入邮箱地址'
    return
  }
  
  if (!validateEmail(email)) {
    errorMsg.value = '请输入有效的邮箱地址'
    return
  }
  
  errorMsg.value = ''
  emailVerifying.value = true
  
  try {
    // 检查邮箱是否存在
    const exists = await checkEmailExists(email)
    emailExists.value = exists
    
    if (authMode.value === 'login') {
      if (!exists) {
        errorMsg.value = '该邮箱尚未注册，请先注册'
        return
      }
      
      // 邮箱存在，进入登录页面
      loginForm.email = email
      switchState('login')
    } else {
      // 注册模式：检查重复
      if (checkDuplicateRegistration(email)) {
        errorMsg.value = '此邮箱已被注册，请直接登录'
        return
      }
      
      if (exists) {
        errorMsg.value = '此邮箱已存在，请直接登录'
        return
      }
      
      // 邮箱可用，进入注册第一步
      registerForm.email = email
      registerStep.value = 1
      switchState('register-step1')
    }
  } catch (error) {
    errorMsg.value = '验证邮箱时出错，请稍后再试'
  } finally {
    emailVerifying.value = false
  }
}

// 处理验证码输入
function handleCodeInput(index: number, event: Event) {
  const target = event.target as HTMLInputElement
  const value = target.value.replace(/[^0-9]/g, '') // 只允许数字
  
  if (value) {
    verifyForm.code[index] = value
    
    // 自动跳转到下一个输入框
    if (index < 5) {
      const nextInput = target.parentElement?.nextElementSibling?.querySelector('input') as HTMLInputElement
      if (nextInput) {
        nextInput.focus()
      }
    }
    
    // 检查是否输入完成，自动验证
    checkAutoVerify()
  } else {
    verifyForm.code[index] = ''
  }
}

// 处理退格键
function handleCodeBackspace(index: number, event: KeyboardEvent) {
  if (event.key === 'Backspace') {
    if (!verifyForm.code[index] && index > 0) {
      const prevInput = (event.target as HTMLInputElement).parentElement?.previousElementSibling?.querySelector('input') as HTMLInputElement
      if (prevInput) {
        prevInput.focus()
      }
    } else {
      verifyForm.code[index] = ''
    }
  }
}

// 自动验证检查
function checkAutoVerify() {
  const code = verifyForm.code.join('')
  if (code.length === 6) {
    // 延迟一点时间，给用户反馈
    setTimeout(() => {
      handleVerifyEmail()
    }, 300)
  }
}

// 监听验证码变化
watch(() => verifyForm.code, () => {
  errorMsg.value = '' // 清除错误消息
}, { deep: true })

// 聚焦隐藏验证码输入
function focusHiddenCodeInput() {
  hiddenCodeInputRef.value?.focus()
}

// 处理隐藏输入的数字采集
function handleHiddenCodeInput(event: Event) {
  const input = event.target as HTMLInputElement
  let digits = (input.value || '').replace(/\D/g, '').slice(0, 6)
  // 同步到数组显示
  for (let i = 0; i < 6; i++) {
    verifyForm.code[i] = digits[i] || ''
  }
  // 满6位自动验证
  if (digits.length === 6) {
    checkAutoVerify()
  }
}

// 处理隐藏输入的退格控制
function handleHiddenCodeKeydown(event: KeyboardEvent) {
  if (event.key === 'Backspace') {
    // 删除最后一个非空位
    for (let i = 5; i >= 0; i--) {
      if (verifyForm.code[i]) {
        verifyForm.code[i] = ''
        break
      }
    }
    // 重建隐藏输入的值
    if (hiddenCodeInputRef.value) {
      hiddenCodeInputRef.value.value = verifyForm.code.join('')
    }
    event.preventDefault()
  }
}

async function handleLogin() {
  if (loading.value) return
  
  errorMsg.value = ''
  infoMsg.value = ''
  loading.value = true
  
  try {
    const result = await apiLogin({ 
      email: loginForm.email, 
      password: loginForm.password 
    })
    
    if (!result.success) {
      errorMsg.value = result.message ?? '登录失败，请检查账号与密码'
      return
    }

    // 显示用户确认页面
    userConfirm.user = {
      username: result.username,
      user_id: result.user_id,
      email: loginForm.email
    }
    userConfirm.confirmed = false
    switchState('user-confirm')
    
  } catch (err) {
    console.error('[login] unexpected error', err)
    errorMsg.value = '网络异常，请稍后再试'
  } finally {
    loading.value = false
  }
}

// 确认登录
function confirmLogin() {
  if (typeof window !== 'undefined') {
    const storage = loginForm.remember ? window.localStorage : window.sessionStorage
    storage.setItem(
      'mock_auth',
      JSON.stringify({ 
        token: 'mock_token', 
        user: userConfirm.user, 
        ts: Date.now(), 
        remember: loginForm.remember 
      })
    )
  }
  
  router.push({ name: 'home' })
}

// 注册步骤1：密码设置
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

// 注册步骤2：个人信息
function handleRegisterStep2() {
  if (loading.value) return
  
  errorMsg.value = ''
  
  if (!registerForm.name.trim()) {
    errorMsg.value = '请输入用户名'
    return
  }
  
  if (!registerForm.birthYear || !registerForm.birthMonth || !registerForm.birthDay) {
    errorMsg.value = '请选择完整的出生日期'
    return
  }
  
  nextRegisterStep()
}

// 注册步骤3：条款确认和最终注册
async function handleRegisterStep3() {
  if (loading.value) return
  
  errorMsg.value = ''
  
  if (!isTermsScrolledToBottom.value) {
    errorMsg.value = '请先阅读完所有条款与条件'
    return
  }
  
  loading.value = true
  
  try {
    // 先发送验证码
    console.log('🔍 发送注册验证码:', { email: registerForm.email, usage: 'Register' })
    await apiSendRegisterCode(registerForm.email)
    
    // 发送成功后跳转到验证码页面
    verifyForm.email = registerForm.email
    verifyForm.code = ['', '', '', '', '', '']
    switchState('verify-email')
    startCountdown(60)
    infoMsg.value = `验证码已发送到 ${registerForm.email}`
    
  } catch (err) {
    console.error('发送验证码失败:', err)
    errorMsg.value = '发送验证码失败，请稍后再试'
  } finally {
    loading.value = false
  }
}

// 最终注册提交（在验证码验证后调用）
async function handleFinalRegister() {
  if (loading.value) return
  
  loading.value = true
  try {
    // 注册需要验证码，根据API文档
    const result = await apiRegister({
      username: registerForm.name,
      email: registerForm.email,
      password: registerForm.password,
      code: verifyForm.code.join(''), // 使用验证码
    })
    if (!('success' in result) || !result.success) {
      errorMsg.value = (result as any).message || '注册失败，请稍后再试'
      // 清空验证码并聚焦隐藏输入
      verifyForm.code = ['', '', '', '', '', '']
      if (hiddenCodeInputRef.value) hiddenCodeInputRef.value.value = ''
      focusHiddenCodeInput()
      return
    }

    // 添加到已注册邮箱列表
    registeredEmails.value.add(registerForm.email.toLowerCase())
    // 预填登录邮箱
    loginForm.email = registerForm.email
    
    infoMsg.value = '注册成功！正在跳转...'
    setTimeout(() => {
      switchState('login')
    }, 2000)
  } catch (err) {
    console.error('[register] unexpected error', err)
    errorMsg.value = '网络异常，请稍后再试'
    // 清空验证码并聚焦隐藏输入
    verifyForm.code = ['', '', '', '', '', '']
    if (hiddenCodeInputRef.value) hiddenCodeInputRef.value.value = ''
    focusHiddenCodeInput()
  } finally {
    loading.value = false
  }
}

async function handleVerifyEmail() {
  if (loading.value) return
  
  const code = verifyForm.code.join('')
  if (code.length !== 6) {
    errorMsg.value = '请输入完整的验证码'
    return
  }
  
  // 如果是注册流程，调用注册API
  if (registerForm.email === verifyForm.email && registerForm.password) {
    await handleFinalRegister()
  } else if (forgotForm.email === verifyForm.email) {
    // 忘记密码流程
    loading.value = true
    errorMsg.value = ''
    
    try {
      // TODO: 调用验证码验证API
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      resetForm.email = verifyForm.email
      switchState('reset-password')
      infoMsg.value = '验证码验证成功，请重置密码'
    } catch (err) {
      console.error('[verify] unexpected error', err)
      errorMsg.value = '验证码验证失败，请稍后再试'
    } finally {
      loading.value = false
    }
  } else {
    // 其他验证流程
    loading.value = true
    errorMsg.value = ''
    
    try {
      // TODO: 调用验证码验证API
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      loginForm.email = verifyForm.email
      switchState('login')
      infoMsg.value = '验证码验证成功，请登录您的账号'
    } catch (err) {
      console.error('[verify] unexpected error', err)
      errorMsg.value = '验证码验证失败，请稍后再试'
    } finally {
      loading.value = false
    }
  }
}

async function handleForgotPassword() {
  if (loading.value) return
  
  if (!forgotForm.email) {
    errorMsg.value = '请输入邮箱地址'
    return
  }
  
  loading.value = true
  errorMsg.value = ''
  
  try {
    // 模拟发送重置密码邮件
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    resetForm.email = forgotForm.email
    switchState('reset-password')
    startCountdown(60)
    infoMsg.value = '重置密码链接已发送到您的邮箱'
  } catch (err) {
    errorMsg.value = '发送失败，请稍后再试'
  } finally {
    loading.value = false
  }
}

async function handleResetPassword() {
  if (loading.value) return
  
  if (resetForm.password !== resetForm.confirm) {
    errorMsg.value = '两次输入的密码不一致'
    return
  }
  
  loading.value = true
  errorMsg.value = ''
  
  try {
    // 模拟重置密码API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 重置成功，跳转到登录页面
    loginForm.email = resetForm.email
    switchState('login')
    infoMsg.value = '密码重置成功，请使用新密码登录'
  } catch (err) {
    errorMsg.value = '重置失败，请重试'
  } finally {
    loading.value = false
  }
}

async function resendCode() {
  if (countdown.value > 0) return
  
  try {
    // 模拟重新发送验证码
    await new Promise(resolve => setTimeout(resolve, 500))
    startCountdown(60)
    infoMsg.value = '验证码已重新发送'
    // 清空当前验证码
    verifyForm.code = ['', '', '', '', '', '']
  } catch (err) {
    errorMsg.value = '发送失败，请稍后再试'
  }
}

function onSubmit() {
  switch (pageState.value) {
    case 'email-input':
      handleEmailSubmit()
      break
    case 'login':
      handleLogin()
      break
    case 'register-step1':
      handleRegisterStep1()
      break
    case 'register-step2':
      handleRegisterStep2()
      break
    case 'register-step3':
      handleRegisterStep3()
      break
    case 'verify-email':
      handleVerifyEmail()
      break
    case 'forgot-password':
      handleForgotPassword()
      break
    case 'reset-password':
      handleResetPassword()
      break
  }
}
</script>

<template>
  <section class="auth-page">
    <AuthBackdrop />
    
    <div class="auth-container" :class="{ 'is-animating': isAnimating }">
      <Transition name="auth-card" mode="out-in">
        <div :key="cardKey" class="auth-card">
          <!-- 邮箱输入页面 -->
          <template v-if="pageState === 'email-input'">
            <div class="auth-header">
              <div class="logo">
                <h1 class="logo-title">EasyQSLP</h1>
                <p class="logo-subtitle">学习分享网站</p>
              </div>
              
              <div class="auth-tabs">
                <button 
                  class="tab-btn"
                  :class="{ active: authMode === 'login' }"
                  @click="authMode = 'login'"
                  :disabled="isAnimating || emailVerifying"
                >
                  登录
                </button>
                <button 
                  class="tab-btn"
                  :class="{ active: authMode === 'register' }"
                  @click="authMode = 'register'"
                  :disabled="isAnimating || emailVerifying"
                >
                  注册
                </button>
              </div>
            </div>

            <div class="auth-body">
              <h2 class="auth-title">{{ authMode === 'login' ? '欢迎回来' : '创建新账号' }}</h2>
              <p class="auth-desc">{{ authMode === 'login' ? '输入邮箱地址开始登录' : '输入邮箱地址开始注册' }}</p>

              <Transition name="message">
                <div v-if="infoMsg" class="message message--info">
                  <i class="message-icon">✓</i>
                  {{ infoMsg }}
                </div>
              </Transition>
              
              <Transition name="message">
                <div v-if="errorMsg" class="message message--error">
                  <i class="message-icon">✕</i>
                  {{ errorMsg }}
                </div>
              </Transition>

              <form class="auth-form" @submit.prevent="onSubmit">
                <div class="form-group">
                  <div class="input-wrapper">
                    <input
                      v-model="emailForm.email"
                      type="email"
                      placeholder="请输入邮箱地址"
                      required
                      :disabled="loading || emailVerifying"
                      class="form-input"
                      autofocus
                    />
                    <i class="input-icon">📧</i>
                    <div v-if="emailVerifying" class="email-verifying">
                      <div class="loading-spinner"></div>
                    </div>
                  </div>
                </div>

                <button 
                  type="submit" 
                  class="submit-btn"
                  :disabled="loading || emailVerifying || !emailForm.email.trim()"
                >
                  <span v-if="loading || emailVerifying" class="btn-spinner"></span>
                  {{ (loading || emailVerifying) ? '验证中…' : '继续' }}
                </button>
              </form>
            </div>
          </template>

          <!-- 登录页面 -->
          <template v-else-if="pageState === 'login'">
            <div class="auth-header">
              <div class="back-btn" @click="switchState('email-input')">
                <i class="back-icon">←</i>
              </div>
              <h2 class="page-title">登录账号</h2>
              <p class="page-subtitle">{{ loginForm.email }}</p>
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
                  <div class="input-wrapper">
                    <input
                      v-model="loginForm.password"
                      :type="showPassword ? 'text' : 'password'"
                      placeholder="请输入密码"
                      required
                      :disabled="loading"
                      class="form-input"
                      autofocus
                    />
                    <button
                      type="button"
                      class="password-toggle"
                      @click="togglePasswordVisibility('password')"
                    >
                      {{ showPassword ? '🙈' : '👁️' }}
                    </button>
                  </div>
                </div>

                <div class="form-options">
                  <label class="checkbox-label">
                    <input v-model="loginForm.remember" type="checkbox" />
                    <span class="checkbox-text">记住我</span>
                  </label>
                  <button 
                    type="button" 
                    class="forgot-link" 
                    @click="switchState('forgot-password')"
                  >
                    忘记密码？
                  </button>
                </div>

                <button type="submit" class="submit-btn" :disabled="loading">
                  <span v-if="loading" class="btn-spinner"></span>
                  {{ loading ? '登录中…' : '登录' }}
                </button>
              </form>
            </div>
          </template>

          <!-- 用户确认页面 -->
          <template v-else-if="pageState === 'user-confirm'">
            <div class="auth-header">
              <h2 class="page-title">确认登录</h2>
            </div>

            <div class="auth-body">
              <div class="user-info">
                <div class="user-avatar">
                  <img v-if="userConfirm.user?.avatar" :src="userConfirm.user.avatar" alt="头像" />
                  <div v-else class="avatar-placeholder">{{ userConfirm.user?.name?.charAt(0) || 'U' }}</div>
                </div>
                <h3 class="user-name">{{ userConfirm.user?.name || '用户' }}</h3>
                <p class="user-email">{{ userConfirm.user?.email || loginForm.email }}</p>
                <p class="confirm-text">确认以此账号登录吗？</p>
              </div>

              <div class="confirm-actions">
                <button class="cancel-btn" @click="switchState('login')">
                  取消
                </button>
                <button class="confirm-btn" @click="confirmLogin">
                  确认登录
                </button>
              </div>
            </div>
          </template>

          <!-- 注册步骤1：设置密码 -->
          <template v-else-if="pageState === 'register-step1'">
            <div class="auth-header">
              <div class="back-btn" @click="switchState('email-input')">
                <i class="back-icon">←</i>
              </div>
              <div class="step-indicator">
                <div class="step-progress">
                  <div class="progress-fill" style="width: 33.33%"></div>
                </div>
                <span class="step-text">第1步，共3步</span>
              </div>
              <h2 class="page-title">创建密码</h2>
              <p class="page-subtitle">{{ registerForm.email }}</p>
            </div>

            <Transition name="fade" mode="out-in">
              <div :key="pageState" class="auth-body">
              <Transition name="message">
                <div v-if="errorMsg" class="message message--error">
                  <i class="message-icon">✗</i>
                  {{ errorMsg }}
                </div>
              </Transition>

              <form class="auth-form" @submit.prevent="onSubmit">
                <div class="form-group">
                  <div class="input-wrapper">
                    <input
                      v-model="registerForm.password"
                      :type="showPassword ? 'text' : 'password'"
                      placeholder="密码（至少10位，包含字母和数字）"
                      required
                      :disabled="loading"
                      class="form-input"
                      autofocus
                      @input="checkPasswordStrength"
                    />
                    <button
                      type="button"
                      class="password-toggle"
                      @click="togglePasswordVisibility('password')"
                    >
                      {{ showPassword ? '🙈' : '👁️' }}
                    </button>
                  </div>
                </div>

                <div class="form-group">
                  <div class="input-wrapper">
                    <input
                      v-model="registerForm.confirm"
                      :type="showConfirmPassword ? 'text' : 'password'"
                      placeholder="确认密码"
                      required
                      :disabled="loading"
                      class="form-input"
                    />
                    <button
                      type="button"
                      class="password-toggle"
                      @click="togglePasswordVisibility('confirm')"
                    >
                      {{ showConfirmPassword ? '🙈' : '👁️' }}
                    </button>
                  </div>
                </div>

                <div class="password-requirements">
                  <p class="requirements-title">密码须至少包含：</p>
                  <div class="requirement-list">
                    <div class="requirement-item" :class="{ 'met': passwordStrength.hasLetter }">
                      <i class="requirement-icon">{{ passwordStrength.hasLetter ? '✅' : '⭕' }}</i>
                      <span>1个字母</span>
                    </div>
                    <div class="requirement-item" :class="{ 'met': passwordStrength.hasNumberOrSymbol }">
                      <i class="requirement-icon">{{ passwordStrength.hasNumberOrSymbol ? '✅' : '⭕' }}</i>
                      <span>1个数字或特殊字符（如：#?!&）</span>
                    </div>
                    <div class="requirement-item" :class="{ 'met': passwordStrength.hasMinLength }">
                      <i class="requirement-icon">{{ passwordStrength.hasMinLength ? '✅' : '⭕' }}</i>
                      <span>10个字符</span>
                    </div>
                  </div>
                </div>

                <button type="submit" class="submit-btn" :disabled="loading">
                  <span v-if="loading" class="btn-spinner"></span>
                  {{ loading ? '验证中…' : '下一步' }}
                </button>
              </form>
            </div>
            </Transition>
          </template>

          <!-- 注册步骤2：个人信息 -->
          <template v-else-if="pageState === 'register-step2'">
            <div class="auth-header">
              <div class="back-btn" @click="prevRegisterStep">
                <i class="back-icon">←</i>
              </div>
              <div class="step-indicator">
                <div class="step-progress">
                  <div class="progress-fill" style="width: 66.66%"></div>
                </div>
                <span class="step-text">第2步，共3步</span>
              </div>
              <h2 class="page-title">介绍一下自己</h2>
              <p class="page-subtitle">完善您的个人信息</p>
            </div>

            <Transition name="fade" mode="out-in">
              <div :key="pageState" class="auth-body">
              <Transition name="message">
                <div v-if="errorMsg" class="message message--error">
                  <i class="message-icon">✗</i>
                  {{ errorMsg }}
                </div>
              </Transition>

              <form class="auth-form" @submit.prevent="onSubmit">
                <div class="form-group">
                  <div class="input-wrapper">
                    <input
                      v-model="registerForm.name"
                      type="text"
                      placeholder="你的昵称"
                      required
                      :disabled="loading"
                      class="form-input"
                      autofocus
                    />
                    <i class="input-icon">👤</i>
                  </div>
                  <p class="form-desc">此名称会显示在你的个人资料上</p>
                </div>

                <div class="form-group">
                  <label class="form-label">出生日期</label>
                  <div class="date-inputs">
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
                  <p class="form-desc">为什么我们需要你提供出生日期？了解更多。</p>
                </div>

                <div class="form-group">
                  <label class="form-label">性别</label>
                  <div class="gender-options">
                    <label class="radio-option">
                      <input v-model="registerForm.gender" type="radio" value="male" />
                      <span class="radio-label">👨 男</span>
                    </label>
                    <label class="radio-option">
                      <input v-model="registerForm.gender" type="radio" value="female" />
                      <span class="radio-label">👩 女</span>
                    </label>
                  </div>
                  <p class="form-desc">我们会根据你的性别来推送个性化精选推荐内容</p>
                </div>

                <button type="submit" class="submit-btn" :disabled="loading">
                  <span v-if="loading" class="btn-spinner"></span>
                  {{ loading ? '验证中…' : '下一步' }}
                </button>
              </form>
            </div>
            </Transition>
          </template>

          <!-- 注册步骤3：服务条款 -->
          <template v-else-if="pageState === 'register-step3'">
            <div class="auth-header">
              <div class="back-btn" @click="prevRegisterStep">
                <i class="back-icon">←</i>
              </div>
              <div class="step-indicator">
                <div class="step-progress">
                  <div class="progress-fill" style="width: 100%"></div>
                </div>
                <span class="step-text">第3步，共3步</span>
              </div>
              <h2 class="page-title">服务条款</h2>
              <p class="page-subtitle">请仔细阅读并同意以下条款</p>
            </div>

            <div class="auth-body">
              <Transition name="message">
                <div v-if="errorMsg" class="message message--error">
                  <i class="message-icon">✗</i>
                  {{ errorMsg }}
                </div>
              </Transition>

              <div class="terms-container" @scroll="handleTermsScroll">
                <div class="terms-content">
                  <h3>服务条款与隐私政策</h3>
                  <p>欢迎使用EasyQSLP学习分享平台。使用我们的服务即表示您同意这些条款。请仔细阅读。</p>
                  
                  <h4>1. 服务说明</h4>
                  <p>EasyQSLP是一个专注于学习分享的在线平台，我们致力于为用户提供优质的学习资源和交流环境。</p>
                  
                  <h4>2. 用户责任</h4>
                  <p>您需要对自己账户的安全负责，包括但不限于密码保护、账户信息的准确性等。请勿分享您的账户信息。</p>
                  
                  <h4>3. 内容政策</h4>
                  <p>用户发布的内容应当遵守法律法规，不得包含违法、有害、威胁、辱骂、骚扰、侵权或其他不当内容。</p>
                  
                  <h4>4. 隐私保护</h4>
                  <p>我们重视您的隐私安全。我们会按照隐私政策的规定收集、使用和保护您的个人信息。</p>
                  
                  <h4>5. 知识产权</h4>
                  <p>平台上的内容受到知识产权法的保护。未经授权，不得复制、传播或商业使用平台内容。</p>
                  
                  <h4>6. 服务变更</h4>
                  <p>我们可能会不时修改这些条款。重要更改会通过平台通知您。继续使用服务即表示接受修改后的条款。</p>
                  
                  <h4>7. 免责声明</h4>
                  <p>在法律允许的最大范围内，我们对因使用或无法使用本服务而产生的任何损害不承担责任。</p>
                  
                  <h4>8. 联系我们</h4>
                  <p>如有任何问题，请通过平台内的联系方式与我们取得联系。我们将尽快为您处理。</p>
                  
                  <p class="terms-footer">感谢您选择EasyQSLP！</p>
                </div>
              </div>

              <form class="auth-form" @submit.prevent="onSubmit">
                <button 
                  type="submit" 
                  class="submit-btn submit-btn--register"
                  :disabled="loading || !isTermsScrolledToBottom"
                >
                  <span v-if="loading" class="loading-dots">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                  </span>
                  {{ loading ? '发送验证码中…' : '同意条款并注册' }}
                </button>
              </form>
            </div>
          </template>

          <!-- 邮箱验证页面 -->
          <template v-else-if="pageState === 'verify-email'">
            <div class="auth-header">
              <div class="back-btn" @click="switchState('register-step3')">
                <i class="back-icon">←</i>
              </div>
              <h2 class="page-title">验证邮箱</h2>
            </div>

            <Transition name="fade" mode="out-in">
              <div :key="pageState" class="auth-body">
              <div class="verify-content">
                <div class="verify-icon">📧</div>
                <h3 class="verify-subtitle">请输入验证码</h3>
                <p class="verify-desc">
                  我们已向 <strong>{{ verifyForm.email }}</strong> 发送了验证码
                </p>

                <Transition name="message">
                  <div v-if="infoMsg" class="message message--info">{{ infoMsg }}</div>
                </Transition>
                <Transition name="message">
                  <div v-if="errorMsg" class="message message--error">{{ errorMsg }}</div>
                </Transition>

                <div class="code-input-group" @click="focusHiddenCodeInput">
                  <!-- 隐藏的真实输入框，仅接收数字 -->
                  <input
                    ref="hiddenCodeInputRef"
                    class="hidden-code-input"
                    type="text"
                    inputmode="numeric"
                    autocomplete="one-time-code"
                    maxlength="6"
                    pattern="\\d*"
                    :disabled="loading"
                    @input="handleHiddenCodeInput"
                    @keydown="handleHiddenCodeKeydown"
                  />
                  <div
                    v-for="(_, index) in 6"
                    :key="index"
                    class="code-input-wrapper"
                  >
                    <input
                      :value="verifyForm.code[index]"
                      readonly
                      tabindex="-1"
                      class="code-input"
                      :class="{ 'code-input--filled': verifyForm.code[index], 'code-input--loading': loading }"
                    />
                  </div>
                </div>

                <div class="verify-status">
                  <div v-if="loading" class="verifying-status">
                    <div class="loading-spinner"></div>
                    <span>正在验证...</span>
                  </div>
                </div>

                <div class="resend-section">
                  <button
                    v-if="countdown > 0"
                    type="button"
                    class="resend-btn disabled"
                    disabled
                  >
                    {{ countdown }}秒后可重新发送
                  </button>
                  <button
                    v-else
                    type="button"
                    class="resend-btn"
                    @click="resendCode"
                  >
                    重新发送验证码
                  </button>
                </div>
              </div>
            </div>
            </Transition>
          </template>

          <!-- 忘记密码页面 -->
          <template v-else-if="pageState === 'forgot-password'">
            <div class="auth-header">
              <button class="back-btn" @click="switchState('login')">
                <i class="back-icon">←</i>
              </button>
              <div class="logo">
                <h1 class="logo-title">找回密码</h1>
              </div>
            </div>

            <div class="auth-body">
              <div class="forgot-content">
                <div class="forgot-icon">🔑</div>
                <h2 class="forgot-title">忘记密码</h2>
                <p class="forgot-desc">请输入您的邮箱地址，我们将发送重置密码的链接到您的邮箱</p>

                <Transition name="message">
                  <div v-if="infoMsg" class="message message--info">{{ infoMsg }}</div>
                </Transition>
                <Transition name="message">
                  <div v-if="errorMsg" class="message message--error">{{ errorMsg }}</div>
                </Transition>

                <form class="auth-form" @submit.prevent="onSubmit">
                  <div class="form-group">
                    <div class="input-wrapper">
                      <input
                        v-model="forgotForm.email"
                        type="email"
                        class="form-input"
                        placeholder="请输入邮箱地址"
                        required
                      />
                      <i class="input-icon">✉</i>
                    </div>
                  </div>

                  <button
                    type="submit"
                    class="submit-btn submit-btn--forgot"
                    :disabled="loading"
                  >
                    <template v-if="!loading">
                      发送重置链接
                    </template>
                    <template v-else>
                      <div class="btn-spinner"></div>
                      发送中...
                    </template>
                  </button>
                </form>

                <div class="auth-footer">
                  <p>记起密码了？
                    <button
                      type="button"
                      class="forgot-link"
                      @click="switchState('login')"
                    >
                      返回登录
                    </button>
                  </p>
                </div>
              </div>
            </div>
          </template>

          <!-- 重置密码页面 -->
          <template v-else-if="pageState === 'reset-password'">
            <div class="auth-header">
              <button class="back-btn" @click="switchState('forgot-password')">
                <i class="back-icon">←</i>
              </button>
              <div class="logo">
                <h1 class="logo-title">重置密码</h1>
              </div>
            </div>

            <div class="auth-body">
              <div class="reset-content">
                <div class="reset-icon">🔐</div>
                <h2 class="reset-title">设置新密码</h2>
                <p class="reset-desc">请输入新密码，密码长度至少6位，建议包含字母和数字</p>

                <Transition name="message">
                  <div v-if="infoMsg" class="message message--info">{{ infoMsg }}</div>
                </Transition>
                <Transition name="message">
                  <div v-if="errorMsg" class="message message--error">{{ errorMsg }}</div>
                </Transition>

                <form class="auth-form" @submit.prevent="onSubmit">
                  <div class="form-group">
                    <div class="input-wrapper">
                      <input
                        v-model="resetForm.password"
                        :type="showPassword ? 'text' : 'password'"
                        class="form-input"
                        placeholder="请输入新密码"
                        required
                        minlength="6"
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
                        v-model="resetForm.confirm"
                        :type="showConfirmPassword ? 'text' : 'password'"
                        class="form-input"
                        placeholder="请确认新密码"
                        required
                        minlength="6"
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

                  <button
                    type="submit"
                    class="submit-btn submit-btn--reset"
                    :disabled="loading"
                  >
                    <template v-if="!loading">
                      重置密码
                    </template>
                    <template v-else>
                      <div class="btn-spinner"></div>
                      重置中...
                    </template>
                  </button>
                </form>

                <div class="auth-footer">
                  <p>记起密码了？
                    <button
                      type="button"
                      class="forgot-link"
                      @click="switchState('login')"
                    >
                      返回登录
                    </button>
                  </p>
                </div>
              </div>
            </div>
          </template>
        </div>
      </Transition>
    </div>
  </section>
</template>

<style scoped>
/* 全屏隐藏侧边栏样式 */
:global(.auth-fullscreen) {
  --sidenav-w: 0px !important;
}

:global(.auth-fullscreen .sidenav) {
  display: none !important;
}

:global(.auth-fullscreen #app) {
  margin-left: 0 !important;
}

/* 基础布局 */
.auth-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  overflow: hidden;
  z-index: 9999;
}

.auth-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 500px;
  padding: 0 20px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.auth-container.is-animating {
  pointer-events: none;
}

/* 卡片样式 */
.auth-card {
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 32px 64px rgba(0, 0, 0, 0.4), 0 16px 32px rgba(0, 0, 0, 0.2);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 头部样式 */
.auth-header {
  padding: 72px 32px 32px;
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
  backdrop-filter: blur(10px);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.back-icon {
  font-size: 20px;
  color: #fff;
  font-weight: bold;
}

.logo {
  margin-bottom: 32px;
}

.logo-title {
  margin: 0 0 8px;
  font-size: 36px;
  font-weight: 900;
  background: linear-gradient(135deg, #e50914, #ff6b6b, #ffd93d, #4ecdc4);
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 4s ease-in-out infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  25% { background-position: 100% 50%; }
  50% { background-position: 50% 100%; }
  75% { background-position: 50% 0%; }
}

.logo-subtitle {
  margin: 0;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
  letter-spacing: 1px;
}

.page-title {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 700;
  color: #fff;
}

.page-subtitle {
  margin: 0;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

/* Tab样式 */
.auth-tabs {
  display: flex;
  gap: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 8px;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-btn {
  flex: 1;
  padding: 16px 24px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.tab-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #e50914, #ff6b6b);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.tab-btn.active {
  color: #fff;
  transform: scale(1.02);
  box-shadow: 0 8px 24px rgba(229, 9, 20, 0.3);
}

.tab-btn.active::before {
  opacity: 1;
}

.tab-btn span {
  position: relative;
  z-index: 1;
}

.tab-btn:hover:not(.active):not(:disabled) {
  background: rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
}

.tab-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* 主体内容 */
.auth-body {
  padding: 40px 32px;
}

.auth-title {
  margin: 0 0 12px;
  font-size: 32px;
  font-weight: 800;
  color: #fff;
  text-align: center;
  letter-spacing: -0.5px;
}

.auth-desc {
  margin: 0 0 40px;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  text-align: center;
}

/* 消息样式 */
.message {
  margin: 0 0 24px;
  padding: 16px 20px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 12px;
  backdrop-filter: blur(20px);
  animation: messageSlide 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.message-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.message--info {
  background: rgba(52, 211, 153, 0.2);
  border: 1px solid rgba(52, 211, 153, 0.4);
  color: #34d399;
}

.message--error {
  background: rgba(248, 113, 113, 0.2);
  border: 1px solid rgba(248, 113, 113, 0.4);
  color: #f87171;
}

/* 表单样式 */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  position: relative;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input {
  width: 100%;
  padding: 20px 24px;
  padding-right: 60px;
  background: rgba(255, 255, 255, 0.08);
  border: 2px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  color: #fff;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(20px);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-input:focus {
  outline: none;
  border-color: #e50914;
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 0 0 6px rgba(229, 9, 20, 0.15), 0 8px 32px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-icon {
  position: absolute;
  right: 20px;
  font-size: 20px;
  color: rgba(255, 255, 255, 0.4);
  pointer-events: none;
  z-index: 1;
}

.email-verifying {
  position: absolute;
  right: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.password-toggle {
  position: absolute;
  right: 16px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-size: 18px;
  z-index: 2;
}

.password-toggle:hover {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
  transform: scale(1.1);
}

/* 用户信息确认 */
.user-info {
  text-align: center;
  padding: 32px 0;
}

.user-avatar {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #e50914, #ff6b6b);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: bold;
  color: white;
}

.user-name {
  margin: 0 0 8px;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
}

.user-email {
  margin: 0 0 20px;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
}

.confirm-text {
  margin: 0;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
}

.confirm-actions {
  display: flex;
  gap: 16px;
  margin-top: 32px;
}

.cancel-btn,
.confirm-btn {
  flex: 1;
  padding: 16px 24px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.confirm-btn {
  background: linear-gradient(135deg, #e50914, #ff6b6b);
  color: #fff;
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #f40612, #ff7979);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(229, 9, 20, 0.4);
}

/* 其他选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 8px 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.checkbox-label:hover {
  color: rgba(255, 255, 255, 0.9);
}

.checkbox-text {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.forgot-link {
  background: none;
  border: none;
  color: #e50914;
  font-size: 14px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s ease;
  font-weight: 600;
}

.forgot-link:hover {
  color: #ff6b6b;
  background: rgba(229, 9, 20, 0.1);
  transform: scale(1.05);
}

.agreement-label {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  margin: 16px 0;
  transition: all 0.2s ease;
}

.agreement-label:hover {
  color: rgba(255, 255, 255, 0.9);
}

.agreement-text {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
}

/* 提交按钮 */
.submit-btn {
  padding: 20px 32px;
  background: linear-gradient(135deg, #e50914, #ff6b6b);
  border: none;
  border-radius: 16px;
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-top: 16px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.submit-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.submit-btn:hover:not(:disabled)::before {
  transform: translateX(100%);
}

.submit-btn--register {
  background: linear-gradient(135deg, #34d399, #22d3ee);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 16px 40px rgba(229, 9, 20, 0.4);
}

.submit-btn--register:hover:not(:disabled) {
  background: linear-gradient(135deg, #10b981, #06b6d4);
  box-shadow: 0 16px 40px rgba(52, 211, 153, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top: 2px solid #e50914;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 验证码样式 */
.verify-content {
  text-align: center;
}

.verify-icon {
  font-size: 64px;
  margin-bottom: 24px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-12px); }
  60% { transform: translateY(-6px); }
}

/* 内容淡入淡出动画，用于注册步骤主体 */
.fade-enter-active, .fade-leave-active { transition: opacity .25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.verify-subtitle {
  margin: 0 0 16px;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
}

.verify-desc {
  margin: 0 0 40px;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
}

.code-input-group {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 32px;
}

/* 隐藏的验证码真实输入框（可聚焦、不可见） */
.hidden-code-input {
  position: absolute;
  left: -9999px;
  top: 0;
  width: 0;
  height: 0;
  opacity: 0;
}

.code-input-wrapper {
  position: relative;
}

.code-input {
  width: 60px;
  height: 72px;
  text-align: center;
  font-size: 28px;
  font-weight: 800;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  color: #fff;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(20px);
}

.code-input:focus {
  outline: none;
  border-color: #e50914;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 4px rgba(229, 9, 20, 0.2);
  transform: scale(1.1);
}

.code-input--filled {
  border-color: #34d399;
  background: rgba(52, 211, 153, 0.2);
  color: #34d399;
  transform: scale(1.05);
}

.code-input--loading {
  border-color: #fbbf24;
  background: rgba(251, 191, 36, 0.2);
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.verify-status {
  margin: 20px 0;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.verifying-status {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 600;
}

.resend-section {
  margin: 24px 0;
  text-align: center;
}

.resend-btn {
  background: none;
  border: none;
  color: #e50914;
  font-size: 14px;
  cursor: pointer;
  padding: 12px 20px;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-weight: 600;
}

.resend-btn:hover:not(.disabled) {
  background: rgba(229, 9, 20, 0.1);
  color: #ff6b6b;
  transform: scale(1.05);
}

.resend-btn.disabled {
  color: rgba(255, 255, 255, 0.4);
  cursor: not-allowed;
}

/* 过渡动画 */
.auth-card-enter-active,
.auth-card-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.auth-card-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(40px);
}

.auth-card-leave-to {
  opacity: 0;
  transform: scale(1.1) translateY(-40px);
}

.message-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

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

/* 响应式设计 */
@media (max-width: 640px) {
  .auth-header,
  .auth-body {
    padding: 32px 24px;
  }
  
  .logo-title {
    font-size: 32px;
  }
  
  .auth-title {
    font-size: 28px;
  }
  
  .form-input {
    padding: 18px 20px;
    font-size: 15px;
  }
  
  .code-input-group {
    gap: 12px;
  }
  
  .code-input {
    width: 50px;
    height: 64px;
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .auth-page {
    padding: 12px;
  }
  
  .logo-title {
    font-size: 28px;
  }
  
  .auth-title {
    font-size: 24px;
  }
  
  .tab-btn {
    padding: 14px 20px;
    font-size: 15px;
  }
  
  .code-input {
    width: 45px;
    height: 58px;
    font-size: 20px;
  }
  
  .code-input-group {
    gap: 8px;
  }
}

/* 忘记密码和重置密码页面样式 */
.forgot-content,
.reset-content {
  text-align: center;
}

.forgot-icon,
.reset-icon {
  font-size: 48px;
  margin-bottom: 16px;
  animation: bounce 2s ease-in-out infinite;
}

.forgot-title,
.reset-title {
  margin: 0 0 16px;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
}

.forgot-desc,
.reset-desc {
  margin-bottom: 32px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
}

.auth-footer {
  margin-top: 32px;
  text-align: center;
}

.auth-footer p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

/* 多步骤注册样式 */
.step-indicator {
  margin-bottom: 24px;
}

.step-progress {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.5s ease;
}

.step-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  text-align: center;
  margin: 0;
}

.password-requirements {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  margin-top: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.requirements-title {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 12px;
}

.requirement-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.requirement-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  transition: color 0.3s ease;
}

.requirement-item.met {
  color: #4ade80;
}

.requirement-icon {
  font-size: 16px;
}

.form-desc {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  margin-top: 4px;
  line-height: 1.4;
}

.form-label {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  display: block;
}

.date-inputs {
  display: flex;
  gap: 12px;
}

.date-select {
  flex: 1;
  padding: 16px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 16px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.date-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.date-select option {
  background: #1a1a2e;
  color: #fff;
}

.gender-options {
  display: flex;
  gap: 24px;
  margin-top: 8px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.radio-option input[type="radio"] {
  width: 20px;
  height: 20px;
  accent-color: #667eea;
  cursor: pointer;
}

.radio-label {
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.terms-container {
  max-height: 280px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.terms-container::-webkit-scrollbar {
  width: 8px;
}

.terms-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.terms-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.terms-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

.terms-content {
  line-height: 1.6;
}

.terms-content h3 {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px;
}

.terms-content h4 {
  color: #667eea;
  font-size: 16px;
  font-weight: 600;
  margin: 20px 0 8px;
}

.terms-content p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  margin: 0 0 16px;
}

.terms-footer {
  text-align: center;
  font-weight: 600;
  color: #667eea !important;
  margin-top: 24px !important;
}

.loading-dots {
  display: inline-flex;
  gap: 4px;
  margin-right: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  background: currentColor;
  border-radius: 50%;
  animation: bounce-dot 1.4s ease-in-out infinite both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
.dot:nth-child(3) { animation-delay: 0s; }

@keyframes bounce-dot {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.back-button {
  position: absolute;
  top: 24px;
  left: 24px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 20px;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(-4px);
}
</style>
