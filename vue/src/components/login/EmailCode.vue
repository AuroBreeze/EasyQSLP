<template>
  <div style="display: flex; align-items: center; gap: 10px;">
    <div class="input-group" style="flex-grow: 1;">
      <input 
        type="email" 
        :placeholder="placeholder" 
        :id="inputId" 
        v-model="email" 
        @input="clearError"
      />
      <label :for="inputId">{{ label }}</label>
    </div>
    <button 
      type="button" 
      :id="buttonId" 
      @click="handleGetCode"
      :disabled="!canGetCode"
    >
      {{ canGetCode ? buttonText : `${countdown}秒后重试` }}
    </button>
  </div>
  <div v-if="errorMessage" class="error-message">
    {{ errorMessage }}
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '邮箱'
  },
  label: {
    type: String,
    default: '邮箱'
  },
  inputId: {
    type: String,
    default: 'emailInput'
  },
  buttonId: {
    type: String,
    default: 'getCodeBtn'
  },
  buttonText: {
    type: String,
    default: '获取验证码'
  },
  usage: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['update:modelValue', 'codeSent']);

const email = ref(props.modelValue);

watch(email, (newVal: string) => {
  //console.log('EmailCode emitting update:', newVal);
  emit('update:modelValue', newVal);
});

watch(() => props.modelValue, (newVal: string) => {
  email.value = newVal;
});
const errorMessage = ref('');
const countdown = ref(0);
const canGetCode = ref(true);

const clearError = () => {
  errorMessage.value = '';
};

const showError = (message: string) => {
  errorMessage.value = message;
  setTimeout(() => {
    errorMessage.value = '';
  }, 5000);
};

const handleGetCode = async () => {
  if (!canGetCode.value) return;
  
  if (!email.value) {
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
        email: email.value,
        usage: props.usage
      })
    });

    const data = await response.json();
    if (data.success) {
      // 开始倒计时
      canGetCode.value = false;
      countdown.value = 60;
      const timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
          canGetCode.value = true;
        }
      }, 1000);
      emit('codeSent', true);
    } else {
      showError(data.message);
      emit('codeSent', false);
    }
  } catch (error) {
    console.error('验证码请求失败:', error);
    showError('验证码请求失败，请检查网络连接');
    emit('codeSent', false);
  }
};

defineExpose({
  email,
  clearError
});
</script>

<style scoped>
button {
  border-radius: 20px;
  border: 1px solid #FF4B2B;
  background-color: #FF4B2B;
  color: #FFFFFF;
  font-size: 10px;
  font-weight: bold;
  padding: 10px 15px;
  letter-spacing: 1px;
  transition: transform 80ms ease-in;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  color: red;
  font-size: 14px;
  margin: 8px 0;
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
