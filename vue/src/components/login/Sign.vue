<template>
  <div>
    <!-- 波浪背景容器 -->
    <!-- <div class="wave-background"></div> -->
    <WaveBackground />
    <h2>欢迎来到EasyQFLP</h2>
    <!-- 显示欢迎标题 -->
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
          <!-- 姓名输入框 -->
          <div class="input-group">
            <input type="text" placeholder="姓名" id="nameInput" v-model="signUpData.name" />
            <label for="nameInput">姓名</label>
          </div>
          
          <!-- 邮箱输入框 -->
          <div style="display: flex; align-items: center;">
            <div class="input-group" style="flex-grow: 1;">
              <input type="email" placeholder="邮箱" id="signupEmail" v-model="signUpData.email" />
              <label for="signupEmail">邮箱</label>
            </div>
            <button type="button" id="signupGetCode" @click="handleGetSignUpCode">获取验证码</button>
          </div>
          
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
          <a href="#" @click.prevent="handleForgotPassword">忘记密码?</a>
          <!-- 忘记密码的链接 -->
          <button>登录</button>
          <!-- 提交登录表单的按钮 -->
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
    <div class="container" id="successContainer" v-if="isLoginSuccess">
      <div class="form-container">
        <form>
          <h1>登录成功🎉</h1>
          <p>您已成功登录，欢迎回来！</p>
          <p>页面将在 <span id="countdown">{{ countdown }}</span> 秒后自动跳转...</p>
        </form>
      </div>
      <!-- 新增右边框内容 -->
      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-panel overlay-right">
            <h1><strong>欢迎回来！😊</strong></h1>
            <p>您已成功登录，可以开始使用我们的服务了。</p>
            <p>如果您有任何问题，请随时联系我们的支持团队。</p>
            <button class="ghost" id="goToSupport" @click="goToSupport">联系支持</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import WaveBackground from '@/components/background/WaveBackground.vue';

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

const togglePanel = (isRightPanelActive:boolean) => {
  const container = document.getElementById('container');
  if (container) {
  if (isRightPanelActive) {
    container.classList.add("right-panel-active");
  } else {
    container.classList.remove("right-panel-active");
  }
}
};

const handleSignIn = async () => {
  const { email, password } = signInData;
  if (!email || !password) {
    showError('邮箱和密码不能为空');
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/api/v1/user/login/', {
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
    
    const data = await response.json();
    
    if (data.success) {
      isLoginSuccess.value = true;
      localStorage.setItem('user_id', data.user_id);
      startCountdown();
    } else {
      showError(data.message);
    }
  } catch (error) {
    console.error('登录请求失败:', error);
    showError('登录请求失败，请检查网络连接');
  }
};

const handleSignUp = async () => {
  const { name, email, code, password } = signUpData;
  if (!name || !email || !code || !password) {
    showError('请填写所有必填项');
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
    
    if (data.success) {
      alert('注册成功，请登录');
      location.reload();
    } else {
      showError(data.message);
    }
  } catch (error) {
    console.error('注册请求失败:', error);
    showError('注册请求失败，请检查网络连接');
  }
};

const handleGetSignUpCode = async () => {
  const { email } = signUpData;
  if (!email) {
    showError('请输入邮箱地址');
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/api/v1/user/emailsendcode/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        usage: 'Register'
      })
    });

    const data = await response.json();
    if (data.success) {
      alert('验证码已发送到您的邮箱');
    } else {
      showError(data.message);
    }
  } catch (error) {
    console.error('验证码请求失败:', error);
    showError('验证码请求失败，请检查网络连接');
  }
};

const handleForgotPassword = () => {
  // 忘记密码逻辑
};

const showError = (message:string) => {
  alert(message);
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
/* 引入外部字体 */
@import url('https://fonts.googleapis.com/css?family=Montserrat:400,800');

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
    margin: -20px 0 50px;
    /* 防止滚动条出现 */
    overflow: hidden; /* 防止滚动条出现 */
    font-family: Arial, sans-serif;
}

.wave-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    --animation-duration: 10s;
    --animation-direction: -1;
    background: linear-gradient(to right, #FF4B2B, #FF416C);
    overflow: hidden;
}

.wave-background::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 200%;
    height: 100%;
    background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255, 255, 255, 0.2)" fill-opacity="1" d="M0,256L48,261.3C96,267,192,277,288,256C384,235,480,181,576,181.3C672,181,768,235,864,250.7C960,267,1056,245,1152,213.3C1248,181,1344,139,1392,117.3L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
    background-repeat: repeat-x;
    background-size: 50% 100%;
    animation: wave var(--animation-duration) linear infinite;
}

@keyframes wave {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-50%);
    }
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

#successContainer {
    background: linear-gradient(to right, #FF4B2B, #FF416C);
    border-radius: 10px;
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
    color: #FFFFFF;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 480px;
    width: 768px;
    max-width: 100%;
    position: relative;
    overflow: hidden;
}

#successContainer .form-container {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 40px;
    text-align: center;
    width: 100%;
    max-width: 400px;
}

#successContainer h1 {
    font-size: 32px;
    margin-bottom: 20px;
    color: #FF4B2B;
}

#successContainer p {
    font-size: 16px;
    margin-bottom: 20px;
    color: #333;
}

#successContainer #countdown {
    color: #FF4B2B;
    font-weight: bold;
}

#successContainer button {
    background-color: #FF4B2B;
    border: none;
    border-radius: 20px;
    color: #FFFFFF;
    font-size: 14px;
    font-weight: bold;
    padding: 12px 20px;
    margin-top: 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

#successContainer button:hover {
    background-color: #FF416C;
}

#successContainer .overlay-container {
    position: absolute;
    top: 0;
    left: 50%;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: transform 0.6s ease-in-out;
    z-index: 100;
}

#successContainer .overlay {
    background: linear-gradient(to right, #FF4B2B, #FF416C);
    background-repeat: no-repeat;
    background-size: cover;
    background-position: 0 0;
    color: #FFFFFF;
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
    transform: translateX(0);
    transition: transform 0.6s ease-in-out;
}

#successContainer .overlay-panel {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 0 40px;
    text-align: center;
    top: 0;
    height: 100%;
    width: 50%;
    transform: translateX(0);
    transition: transform 0.6s ease-in-out;
}

#successContainer .overlay-panel h1,
#successContainer .overlay-panel p {
    color: #000; /* 将字体颜色改为黑色 */
}

#successContainer .overlay-right {
    right: 0;
    transform: translateX(0);
}
</style>