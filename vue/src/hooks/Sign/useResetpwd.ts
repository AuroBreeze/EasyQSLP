import { ref, reactive } from 'vue';


const forgotPasswordData = reactive({
    email: '',
    code: '',
    password: '',
    password_confirm: ''
});
const forgotPasswordError = ref('');
const isForgotPasswordActive = ref(false);

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



const handleForgotPassword = () => {
    const container = document.getElementById('container');
    if (container) {
        container.classList.remove("right-panel-active");
        container.classList.add("forgot-panel-active");
        isForgotPasswordActive.value = true;
        // errorMessage.value = '';
        // signUpErrorMessage.value = '';
    }
};

export default function useResetpwd(emit?:(event: 'handleBackToLogin')=>void) {
    const handleBackToLogin = () => {
        if (emit) {
            emit('handleBackToLogin');
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
                        forgotPasswordError.value = data.errors.ValidationError;
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

    return {
        forgotPasswordData,
        forgotPasswordError,
        isForgotPasswordActive,
        handleResetPassword,
        handleForgotPassword,
        showResetPasswordSuccess
    };
}