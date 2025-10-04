import { ref, reactive } from 'vue';

const signUpData = reactive({
    name: '',
    email: '',
    code: '',
    password: ''
});

const signUpErrorMessage = ref('');


const showSignUpError = (message: string) => {
    signUpErrorMessage.value = message;
    // 5秒后自动清除错误信息
    setTimeout(() => {
        signUpErrorMessage.value = '';
    }, 5000);
};

const handleCodeSent = (success: boolean) => {
    if (!success) {
        showSignUpError("验证码发送失败");
    }
};


export default function useSignUp(emit?: (event: 'toggle-panel', isRightPanelActive: boolean) => void) {
    const togglePanel = (isRightPanelActive: boolean) => {
        if (emit) {
            emit('toggle-panel', isRightPanelActive);
        }
    };
    const handleSignUp = async () => {
        const { name, email, code, password } = signUpData;
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
                })
            });

            const data = await response.json();
            console.log(data);

            if (!response.ok) {
                if (data.errors) {
                    if (data.errors.ValidationError) {
                        showSignUpError(data.errors.ValidationError);
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
                signUpErrorMessage.value = '注册成功，正在跳转到登录页面...';

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

    return {
        signUpData,
        signUpErrorMessage,
        handleSignUp,
        handleCodeSent,
        togglePanel
    };
}
