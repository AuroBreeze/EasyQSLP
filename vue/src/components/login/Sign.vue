<template>
  <div class="page-container">
    <!-- 波浪背景容器 -->
    <WaveBackground />
    <div class="content-wrapper">
      <h2>欢迎来到EasyQSLP</h2>
      <div class="container" id="container">
      <!-- 容器，包含注册和登录表单及切换面板 -->
      <!-- 注册表单部分 -->
      <div class="form-container sign-up-container">
        <form @submit.prevent="handleSignUp">
          <!-- 注册表单 -->
          <h1>创建账户😀</h1>
          <!-- 注册表单标题 -->
          <span>使用邮箱注册</span>
          <!-- 提示用户使用邮箱注册 -->
          <!-- 错误提示区域 -->
          <div v-if="signUpErrorMessage" class="error-message">
            {{ signUpErrorMessage }}
          </div>
          <!-- 姓名输入框 -->
          <div class="input-group">
            <input type="text" placeholder="姓名" id="nameInput" v-model="signUpData.name" />
            <label for="nameInput">姓名</label>
          </div>
          
          <!-- 邮箱输入框和验证码按钮 -->
          <EmailCode 
            v-model="signUpData.email"
            input-id="signupEmail"
            button-id="signupGetCode"
            usage="Register"
            @code-sent="handleCodeSent"
          />
          <!-- 验证码输入框 -->
          <div class="input-group">
            <input type="text" placeholder="验证码" id="signupCode" v-model="signUpData.code" />
            <label for="signupCode">验证码</label>
          </div>
          
          <!-- 密码输入框 -->
          <div class="input-group">
            <input type="password" placeholder="密码" id="signupPassword" v-model="signUpData.password" />
            <label for="signupPassword">密码</label>
          </div>
          <button>注册</button>
          <!-- 提交注册表单的按钮 -->
        </form>
      </div>
      <!-- 登录表单部分 -->
      <div class="form-container sign-in-container">
        <form @submit.prevent="handleSignIn">
          <!-- 登录表单 -->
          <h1>登录😃</h1>
          <!-- 登录表单标题 -->
          <span>账户密码登录</span>
          <!-- 提示用户使用账户密码登录 -->
          <!-- 错误提示区域 -->
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
          
          <!-- 邮箱输入框 -->
          <div class="input-group">
            <input type="email" placeholder="邮箱" id="signinEmail" v-model="signInData.email" />
            <label for="signinEmail">邮箱</label>
          </div>
          
          <!-- 密码输入框 -->
          <div class="input-group">
            <input type="password" placeholder="密码" id="signinPassword" v-model="signInData.password" />
            <label for="signinPassword">密码</label>
          </div>
          <a href="#" class="forgot-password" @click.prevent="handleForgotPassword">忘记密码?</a>
          <!-- 忘记密码的链接 -->
          <button>登录</button>
          <!-- 提交登录表单的按钮 -->
        </form>
      </div>
      <!-- 忘记密码表单部分 -->
      <div class="form-container forgot-password-container">
        <form @submit.prevent="handleResetPassword">
          <h1>重置密码</h1>
          <span>请输入您的邮箱和验证码</span>
          
          <div v-if="forgotPasswordError" class="error-message">
            {{ forgotPasswordError }}
          </div>

          <!-- 邮箱输入框和验证码按钮 -->
          <EmailCode 
            v-model="forgotPasswordData.email"
            input-id="forgotEmail"
            button-id="forgotGetCode"
            usage="ResetPassword"
            @code-sent="handleCodeSent"
          />

          <!-- 验证码输入框 -->
          <div class="input-group">
            <input type="text" placeholder="验证码" id="forgotCode" v-model="forgotPasswordData.code" />
            <label for="forgotCode">验证码</label>
          </div>

          <!-- 新密码输入框 -->
          <div class="input-group">
            <input type="password" placeholder="新密码" id="newPassword" v-model="forgotPasswordData.password" />
            <label for="newPassword">新密码</label>
          </div>

          <!-- 确认新密码输入框 -->
          <div class="input-group">
            <input type="password" placeholder="确认新密码" id="confirmPassword" v-model="forgotPasswordData.password_confirm" />
            <label for="confirmPassword">确认新密码</label>
          </div>

          <button type="submit">重置密码</button>
          <a href="#" class="back-to-login" @click.prevent="handleBackToLogin">返回登录</a>
        </form>
      </div>

      <div class="overlay-container">
        <!-- 覆盖层容器，用于切换注册和登录界面 -->
        <div class="overlay">
          <div class="overlay-panel overlay-left">
            <!-- 左侧覆盖层面板 -->
            <h1>欢迎回来！😊</h1>
            <!-- 左侧覆盖层面板标题 -->
            <p>请使用您的个人信息登录以保持与我们的联系</p>
            <!-- 左侧覆盖层面板提示信息 -->
            <button class="ghost" id="signIn" @click="togglePanel(false)">登录</button>
            <!-- 切换到登录界面的按钮 -->
          </div>
          <div class="overlay-panel overlay-right">
            <!-- 右侧覆盖层面板 -->
            <h1>欢迎🎉</h1>
            <!-- 右侧覆盖层面板标题 -->
            <p>注册账户，并加入我们的大家庭</p>
            <!-- 右侧覆盖层面板提示信息 -->
            <button class="ghost" id="signUp" @click="togglePanel(true)">注册</button>
            <!-- 切换到注册界面的按钮 -->
          </div>
        </div>
      </div>
    </div>

      <!-- 登录成功后的界面 -->
      <div v-if="isLoginSuccess" class="success-page">
        <div class="success-container">
          <div class="success-content">
            <h1>登录成功🎉</h1>
            <p>您已成功登录，欢迎回来！</p>
            <p>页面将在 <span class="countdown">{{ countdown }}</span> 秒后自动跳转...</p>
            <button class="success-button" @click="goToSupport">联系支持</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import WaveBackground from '@/components/background/WaveBackground.vue';
import EmailCode from '@/components/login/EmailCode.vue';

const router = useRouter();

const signUpData = reactive({
  name: '',
  email: '',
  code: '',
  password: ''
});

const signInData = reactive({
  email: '',
  password: ''
});

const isLoginSuccess = ref(false);
const countdown = ref(3);
const errorMessage = ref('');
const signUpErrorMessage = ref('');
const handleCodeSent = (success: boolean) => {
  if (!success) {
    showSignUpError("验证码发送失败");
  }
};

const togglePanel = (isRightPanelActive:boolean) => {
  const container = document.getElementById('container');
  if (container) {
    // 如果当前是忘记密码面板且要切换到注册面板
    if (isForgotPasswordActive.value && isRightPanelActive) {
      container.classList.remove("forgot-panel-active");
      isForgotPasswordActive.value = false;
    }
    
    if (isRightPanelActive) {
      container.classList.add("right-panel-active");
    } else {
      container.classList.remove("right-panel-active");
    }
    // 切换面板时清除所有提示信息
    signUpErrorMessage.value = '';
    errorMessage.value = '';
  }
};

const handleSignIn = async () => {
  const { email, password } = signInData;
  if (!email || !password) {
    showError('邮箱和密码不能为空');
    return;
  }

  // 检查URL参数是否有mock=true
  const urlParams = new URLSearchParams(window.location.search);
  const mockMode = urlParams.get('mock') === 'true';

  if (mockMode) {
    // Mock模式 - 直接模拟成功登录
    console.log('Running in mock mode - simulating successful login');
    isLoginSuccess.value = true;
    localStorage.setItem('user_id', 'mock-user-123');
    startCountdown();
    return;
  }

  try {
    // 1. 先调用登录接口
    const loginResponse = await fetch('http://localhost:8000/api/v1/user/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });

    const loginData = await loginResponse.json();
    
    if (!loginResponse.ok) {
      // 处理400/401错误
      if (loginData.errors) {
        if (loginData.errors.ValidationError) {
          showError(loginData.errors.ValidationError);
        } else if (loginData.errors.email) {
          showError(`邮箱错误: ${loginData.errors.email}`);
        } else if (loginData.errors.password) {
          showError(`密码错误: ${loginData.errors.password}`);
        } else {
          showError(loginData.message || '登录失败');
        }
      } else {
        showError(loginData.message || '登录失败');
      }
      return;
    }

    if (loginData.success) {
      // 2. 登录成功后再获取JWT token
      const tokenResponse = await fetch('http://localhost:8000/api/v1/user/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      const tokenData = await tokenResponse.json();
      
      if (tokenData.access) {
        // 存储token和用户信息
        localStorage.setItem('access_token', tokenData.access);
        localStorage.setItem('refresh_token', tokenData.refresh);
        localStorage.setItem('user_id', loginData.user_id);
        localStorage.setItem('username', loginData.username);
        
        isLoginSuccess.value = true;
        startCountdown();
      } else {
        showError(tokenData.detail || '获取token失败');
      }
    }
  } catch (error) {
    console.error('登录请求失败:', error);
    showError('网络错误，请检查连接后重试');
  }
};

// 刷新token方法
const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) return null;

  try {
    const response = await fetch('http://localhost:8000/api/v1/user/token/refresh/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        refresh: refreshToken
      })
    });

    const data = await response.json();
    if (data.access) {
      localStorage.setItem('access_token', data.access);
      return data.access;
    }
    return null;
  } catch (error) {
    console.error('刷新token失败:', error);
    return null;
  }
};

// 验证token方法
const verifyToken = async (token: string) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/user/token/verify/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        token: token
      })
    });

    return response.ok;
  } catch (error) {
    console.error('验证token失败:', error);
    return false;
  }
};

const handleSignUp = async () => {
  const { name, email, code, password } = signUpData;
  //console.log(name, email, code, password);
  if (!name || !email || !code || !password) {
    showSignUpError('请填写所有必填项');
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/api/v1/user/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        password: password,
        username: name,
        code: code,
        usage: 'Register'
      })
    });

    const data = await response.json();
    console.log(data);
    
    if (!response.ok) {
      // 处理400/401错误
      if (data.errors) {
        if (data.errors.ValidationError) {
          showSignUpError(data.errors.ValidationError[0]);
        } else if (data.errors.email) {
          showSignUpError(`邮箱错误: ${data.errors.email}`);
        } else if (data.errors.password) {
          showSignUpError(`密码错误: ${data.errors.password}`);
        } else if (data.errors.code) {
          showSignUpError(`验证码错误: ${data.errors.code}`);
        } else {
          showSignUpError(data.message || '注册失败');
        }
      } else {
        showSignUpError(data.message || '注册失败');
      }
      return;
    }

    if (data.success) {
      // 显示成功消息
      signUpErrorMessage.value = '注册成功，正在跳转到登录页面...';
      
      // 2秒后平滑切换到登录界面并保留成功提示
      setTimeout(() => {
        togglePanel(false);
        signUpData.name = '';
        signUpData.email = '';
        signUpData.code = '';
        signUpData.password = '';
        signUpErrorMessage.value = '注册成功，请登录';
      }, 2000);

    }
  } catch (error) {
    console.error('注册请求失败:', error);
    showSignUpError('网络错误，请检查连接后重试');
  }
};



const forgotPasswordData = reactive({
  email: '',
  code: '',
  password: '',
  password_confirm: ''
});
const forgotPasswordError = ref('');
const isForgotPasswordActive = ref(false);

const handleForgotPassword = () => {
  const container = document.getElementById('container');
  if (container) {
    container.classList.remove("right-panel-active");
    container.classList.add("forgot-panel-active");
    isForgotPasswordActive.value = true;
    errorMessage.value = '';
    signUpErrorMessage.value = '';
  }
};

const handleBackToLogin = () => {
  const container = document.getElementById('container');
  if (container) {
    container.classList.remove("forgot-panel-active");
    isForgotPasswordActive.value = false;
    forgotPasswordData.email = '';
    forgotPasswordData.code = '';
    forgotPasswordData.password = '';
    forgotPasswordData.password_confirm = '';
    forgotPasswordError.value = '';
  }
};

const handleResetPassword = async () => {
  const { email, code, password, password_confirm } = forgotPasswordData;
  
  //console.log(email, code, password, password_confirm);
  if (!email || !code || !password || !password_confirm) {
    forgotPasswordError.value = '请填写所有必填项';
    return;
  }

  if (password !== password_confirm) {
    forgotPasswordError.value = '两次输入的密码不一致';
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/api/v1/user/resetpassword/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        code: code,
        password: password,
        password_confirm: password_confirm
      })
    });

    const data = await response.json();
    
    if (!response.ok) {
      if (data.errors) {
        if (data.errors.ValidationError) {
          forgotPasswordError.value = data.errors.ValidationError[0];
        } else if (data.errors.email) {
          forgotPasswordError.value = `邮箱错误: ${data.errors.email}`;
        } else if (data.errors.code) {
          forgotPasswordError.value = `验证码错误: ${data.errors.code}`;
        } else if (data.errors.password) {
          forgotPasswordError.value = `密码错误: ${data.errors.password}`;
        } else {
          forgotPasswordError.value = data.message || '密码重置失败';
        }
      } else {
        forgotPasswordError.value = data.message || '密码重置失败';
      }
      return;
    }

    if (data.success) {
      forgotPasswordError.value = '';
      const successMessage = '密码重置成功！2秒后将自动返回登录页面';
      showResetPasswordSuccess(successMessage);
      
      setTimeout(() => {
        handleBackToLogin();
        forgotPasswordData.email = '';
        forgotPasswordData.code = '';
        forgotPasswordData.password = '';
        forgotPasswordData.password_confirm = '';
      }, 2000);
    }
  } catch (error) {
    console.error('密码重置请求失败:', error);
    forgotPasswordError.value = '网络错误，请检查连接后重试';
  }
};

const showError = (message: string) => {
    errorMessage.value = message;
    // 5秒后自动清除错误信息
    setTimeout(() => {
        errorMessage.value = '';
    }, 5000);
};

const showResetPasswordSuccess = (message: string) => {
    forgotPasswordError.value = message;
    // 修改样式为成功提示
    const errorEl = document.querySelector('.forgot-password-container .error-message');
    if (errorEl) {
        errorEl.classList.add('success-message');
    }
    // 5秒后自动清除
    setTimeout(() => {
        forgotPasswordError.value = '';
        if (errorEl) {
            errorEl.classList.remove('success-message');
        }
    }, 5000);
};

const showSignUpError = (message: string) => {
    signUpErrorMessage.value = message;
    // 5秒后自动清除错误信息
    setTimeout(() => {
        signUpErrorMessage.value = '';
    }, 5000);
};


const startCountdown = () => {
  const interval = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      clearInterval(interval);
      router.push('/start/');
    }
  }, 1000);
};

const goToSupport = () => {
  router.push('/support');
};
</script>

<style scoped>
/* 页面容器样式 */
.page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  overflow-y: auto;
  padding: 20px;
}

/* 内容包装器样式 */
.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 800px;
  padding: 20px;
}

/* 引入外部字体 */
/* @import url('https://fonts.googleapis.com/css?family=Montserrat:400,800'); */

/* 全局设置，将所有元素的盒模型设置为 border-box */
* {
    box-sizing: border-box;
}

/* 页面主体样式 */
body {
    /* 设置背景颜色 */
    background: #f6f5f7;
    /* 使用 Flexbox 布局，水平和垂直居中内容 */
    display: flex;
    justify-content: center;
    align-items: center;
    /* 设置主轴方向为垂直 */
    flex-direction: column;
    /* 设置字体 */
    font-family: 'Montserrat', sans-serif;
    /* 设置高度为视口高度 */
    height: 100vh;
    /* 设置上下外边距 */
    margin: 0; /* 去除默认的 margin */
    /* 防止滚动条出现 */
    overflow: hidden;
    font-family: Arial, sans-serif;
}

/* 容器样式 */
.container {
    /* 设置背景颜色 */
    background-color: #fff;
    /* 设置圆角 */
    border-radius: 10px;
    /* 设置阴影 */
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25),
        0 10px 10px rgba(0, 0, 0, 0.22);
    /* 设置定位方式为相对定位 */
    position: relative;
    /* 隐藏溢出内容 */
    overflow: hidden;
    /* 设置宽度 */
    width: 768px;
    /* 设置最大宽度 */
    max-width: 100%;
    /* 设置最小高度 */
    min-height: 480px;
    /* 居中显示 */
    margin: 20px 0;
}

/* 一级标题样式 */
h1 {
    /* 设置字体加粗 */
    font-weight: bold;
    /* 去除外边距 */
    margin: 0;
}

/* 二级标题样式 */
h2 {
    /* 文本居中 */
    text-align: center;
    /* 设置字体大小 */
    font-size: 30px;
    /* 设置字体颜色 */
    color: #333;
    /* 设置字体粗细 */
    font-weight: 700;
    /* 设置字体样式 */
    font-style: italic;
}

/* 段落样式 */
p {
    /* 设置字体大小 */
    font-size: 14px;
    /* 设置字体粗细 */
    font-weight: 100;
    /* 设置行高 */
    line-height: 20px;
    /* 设置字母间距 */
    letter-spacing: 0.5px;
    /* 设置上下外边距 */
    margin: 20px 0 30px;
}

/* 行内元素样式 */
span {
    /* 设置字体大小 */
    font-size: 12px;
}

/* 链接样式 */
a {
    /* 设置文本颜色 */
    color: #333;
    /* 设置字体大小 */
    font-size: 14px;
    /* 去除下划线 */
    text-decoration: none;
    /* 设置上下外边距 */
    margin: 15px 0;
}

/* 按钮样式 */
button {
    /* 设置圆角 */
    border-radius: 20px;
    /* 设置边框 */
    border: 1px solid #FF4B2B;
    /* 设置背景颜色 */
    background-color: #FF4B2B;
    /* 设置文本颜色 */
    color: #FFFFFF;
    /* 设置字体大小 */
    font-size: 12px;
    /* 设置字体加粗 */
    font-weight: bold;
    /* 设置内边距 */
    padding: 12px 20px;
    /* 设置字母间距 */
    letter-spacing: 1px;
    /* 文本大写 */
    text-transform: uppercase;
    /* 设置过渡效果 */
    transition: transform 80ms ease-in;
    /* 设置左外边距 */
    margin-left: 10px;
}

/* 注册获取验证码按钮样式 */
#signupGetCode {
    /* 设置字体大小 */
    font-size: 10px;
    /* 设置内边距 */
    padding: 10px 15px;
}

/* 按钮点击效果 */
button:active {
    /* 缩小按钮 */
    transform: scale(0.95);
}

/* 按钮聚焦效果 */
button:focus {
    /* 去除聚焦时的轮廓 */
    outline: none;
}

/* 幽灵按钮样式 */
button.ghost {
    /* 设置透明背景 */
    background-color: transparent;
    /* 设置边框颜色 */
    border-color: #FFFFFF;
}

/* 表单样式 */
form {
    /* 设置背景颜色 */
    background-color: #FFFFFF;
    /* 使用 Flexbox 布局，水平和垂直居中内容 */
    display: flex;
    align-items: center;
    /* 设置主轴方向为垂直 */
    justify-content: center;
    flex-direction: column;
    /* 设置内边距 */
    padding: 0 50px;
    /* 设置高度为 100% */
    height: 100%;
    /* 文本居中 */
    text-align: center;
}

/* 输入框样式 */
input {
    /* 设置背景颜色 */
    background-color: #eee;
    /* 去除边框 */
    border: none;
    /* 设置内边距 */
    padding: 12px 15px;
    /* 设置上下外边距 */
    margin: 8px 0;
    /* 设置宽度为 100% */
    width: 100%;
}

/* 表单容器样式 */
.form-container {
    /* 设置定位方式为绝对定位 */
    position: absolute;
    /* 设置顶部位置 */
    top: 0;
    /* 设置高度为 100% */
    height: 100%;
    /* 设置过渡效果 */
    transition: all 0.6s ease-in-out;
}

/* 登录表单容器样式 */
.sign-in-container {
    /* 设置左侧位置 */
    left: 0;
    /* 设置宽度 */
    width: 50%;
    /* 设置层级 */
    z-index: 2;
}

/* 容器右侧面板激活时登录表单容器样式 */
.container.right-panel-active .sign-in-container {
    /* 向右平移 100% */
    transform: translateX(100%);
}

/* 忘记密码表单容器样式 */
.forgot-password-container {
  right: 0;
  width: 50%;
  opacity: 0;
  z-index: 1;
}

.container.forgot-panel-active .forgot-password-container {
  transform: translateX(-100%);
  opacity: 1;
  z-index: 5;
  animation: show 0.6s;
}

/* 注册表单容器样式 */
.sign-up-container {
    /* 设置左侧位置 */
    left: 0;
    /* 设置宽度 */
    width: 50%;
    /* 设置透明度为 0 */
    opacity: 0;
    /* 设置层级 */
    z-index: 1;
}

/* 容器右侧面板激活时注册表单容器样式 */
.container.right-panel-active .sign-up-container {
    /* 向右平移 100% */
    transform: translateX(100%);
    /* 设置透明度为 1 */
    opacity: 1;
    /* 设置层级 */
    z-index: 5;
    /* 应用动画 */
    animation: show 0.6s;
}

/* 显示动画 */
@keyframes show {
    /* 动画开始和 49.99% 时的状态 */
    0%,
    49.99% {
        /* 设置透明度为 0 */
        opacity: 0;
        /* 设置层级 */
        z-index: 1;
    }

    /* 动画 50% 到结束时的状态 */
    50%,
    100% {
        /* 设置透明度为 1 */
        opacity: 1;
        /* 设置层级 */
        z-index: 5;
    }
}

/* 覆盖层容器样式 */
.overlay-container {
    /* 设置定位方式为绝对定位 */
    position: absolute;
    /* 设置顶部位置 */
    top: 0;
    /* 设置左侧位置 */
    left: 50%;
    /* 设置宽度 */
    width: 50%;
    /* 设置高度 */
    height: 100%;
    /* 隐藏溢出内容 */
    overflow: hidden;
    /* 设置过渡效果 */
    transition: transform 0.6s ease-in-out;
    /* 设置层级 */
    z-index: 100;
}

/* 容器右侧面板激活时覆盖层容器样式 */
.container.right-panel-active .overlay-container {
    /* 向左平移 100% */
    transform: translateX(-100%);
}

/* 覆盖层样式 */
.overlay {
    /* 设置背景渐变 */
    background: linear-gradient(to right, #FF4B2B, #FF416C);
    /* 设置背景不重复 */
    background-repeat: no-repeat;
    /* 设置背景大小 */
    background-size: cover;
    /* 设置背景位置 */
    background-position: 0 0;
    /* 设置文本颜色 */
    color: #FFFFFF;
    /* 设置定位方式为相对定位 */
    position: relative;
    /* 设置左侧位置 */
    left: -100%;
    /* 设置高度 */
    height: 100%;
    /* 设置宽度 */
    width: 200%;
    /* 平移 0 */
    transform: translateX(0);
    /* 设置过渡效果 */
    transition: transform 0.6s ease-in-out;
}

/* 容器右侧面板激活时覆盖层样式 */
.container.right-panel-active .overlay {
    /* 向右平移 50% */
    transform: translateX(50%);
}

/* 覆盖层面板样式 */
.overlay-panel {
    /* 设置定位方式为绝对定位 */
    position: absolute;
    /* 使用 Flexbox 布局，水平和垂直居中内容 */
    display: flex;
    align-items: center;
    justify-content: center;
    /* 设置主轴方向为垂直 */
    flex-direction: column;
    /* 设置内边距 */
    padding: 0 40px;
    /* 文本居中 */
    text-align: center;
    /* 设置顶部位置 */
    top: 0;
    /* 设置高度 */
    height: 100%;
    /* 设置宽度 */
    width: 50%;
    /* 平移 0 */
    transform: translateX(0);
    /* 设置过渡效果 */
    transition: transform 0.6s ease-in-out;
}

/* 左侧覆盖层面板样式 */
.overlay-left {
    /* 向左平移 20% */
    transform: translateX(-20%);
}

/* 容器右侧面板激活时左侧覆盖层面板样式 */
.container.right-panel-active .overlay-left {
    /* 平移 0 */
    transform: translateX(0);
}

/* 右侧覆盖层面板样式 */
.overlay-right {
    /* 设置右侧位置 */
    right: 0;
    /* 平移 0 */
    transform: translateX(0);
}

/* 容器右侧面板激活时右侧覆盖层面板样式 */
.container.right-panel-active .overlay-right {
    /* 向右平移 20% */
    transform: translateX(20%);
}

/* 页脚样式 */
footer {
    /* 设置背景颜色 */
    background-color: #222;
    /* 设置文本颜色 */
    color: #fff;
    /* 设置字体大小 */
    font-size: 14px;
    /* 设置底部位置 */
    bottom: 0;
    /* 设置定位方式为固定定位 */
    position: fixed;
    /* 设置左侧位置 */
    left: 0;
    /* 设置右侧位置 */
    right: 0;
    /* 文本居中 */
    text-align: center;
    /* 设置层级 */
    z-index: 999;
}

/* 页脚段落样式 */
footer p {
    /* 设置上下外边距 */
    margin: 10px 0;
}

/* 页脚图标样式 */
footer i {
    /* 设置文本颜色 */
    color: red;
}

/* 页脚链接样式 */
footer a {
    /* 设置文本颜色 */
    color: #3c97bf;
    /* 去除下划线 */
    text-decoration: none;
}

/* 输入框组样式 */
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
    color: #999;
    transition: opacity 0.2s ease;
}


.input-group input:focus::placeholder,
.input-group input:not(:placeholder-shown)::placeholder {
    opacity: 0;
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

/* 保持原有输入框样式 */
input {
    background-color: #eee;
    border: none;
    padding: 12px 15px;
    margin: 0;
    width: 100%;
}

/* 在文件末尾添加以下样式 */

.back-to-login {
    display: block;
    text-align: center;
    margin-top: 15px;
    color: #333;
    font-size: 14px;
    text-decoration: none;
}

.back-to-login:hover {
    text-decoration: underline;
}

/* 确保获取验证码按钮样式一致 */
#forgotGetCode {
    font-size: 10px;
    padding: 10px 15px;
    margin-left: 10px;
}

/* 添加错误提示样式 */
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

.success-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.success-container {
  background: linear-gradient(135deg, #ffffff 0%, #f9f9f9 100%);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  width: 500px;
  max-width: 90%;
  padding: 50px;
  text-align: center;
  position: relative;
  overflow: hidden;
  animation: slideUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.success-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,75,43,0.1) 0%, rgba(255,75,43,0) 70%);
  z-index: -1;
}

.success-content h1 {
  color: #FF4B2B;
  margin-bottom: 25px;
  font-size: 2.2rem;
  font-weight: 700;
  position: relative;
  display: inline-block;
}

.success-content h1::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(to right, #FF4B2B, #FF416C);
  border-radius: 3px;
}

.success-content p {
  margin: 15px 0;
  color: #555;
  font-size: 1.1rem;
  line-height: 1.6;
}

.countdown {
  color: #FF4B2B;
  font-weight: bold;
  font-size: 1.3rem;
  display: inline-block;
  min-width: 30px;
}

.success-button {
  margin-top: 30px;
  background: linear-gradient(to right, #FF4B2B, #FF416C);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 30px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(255, 75, 43, 0.4);
  position: relative;
  overflow: hidden;
}

.success-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(255, 75, 43, 0.6);
}

.success-button:active {
  transform: translateY(1px);
}

.success-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.5);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%);
  transform-origin: 50% 50%;
}

.success-button:focus:not(:active)::after {
  animation: ripple 1s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    transform: translateY(50px);
    opacity: 0;
  }
  to { 
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes ripple {
  0% {
    transform: scale(0, 0);
    opacity: 1;
  }
  20% {
    transform: scale(25, 25);
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: scale(40, 40);
  }
}
</style>
