import signService from "@/utils/api/signService"
import { reactive,ref } from "vue"
import router from "@/router"

const signInData = reactive({
  email: '',
  password: ''
});

const errorMessage = ref('');
const isLoginSuccess = ref(false);
const countdown = ref(3);
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
    const result = await signService.Login(email, password);
    //console.log("API123123 response:",result);

    if (!result.success) {
      // 处理错误
      console.log("API798 response:", result.errors);
      showError(result.errors.ValidationError || result.errors.email || '登录失败');
      return;
    }
    if (result.success && 'user_id' in result && 'username' in result) {
      localStorage.setItem('user_id', result.user_id.toString());
      localStorage.setItem('username', result.username);
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

const showError = (message: string) => {
  errorMessage.value = message;
  // 5秒后自动清除错误信息
  setTimeout(() => {
    errorMessage.value = '';
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


export default function useSignIn() {
  return {
    signInData,
    errorMessage,
    isLoginSuccess,
    countdown,
    handleSignIn,
    showError,
    startCountdown
  };
}

