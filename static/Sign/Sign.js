// 获取注册按钮元素
const signUpButton = document.getElementById('signUp');
// 获取登录按钮元素
const signInButton = document.getElementById('signIn');
// 获取容器元素
const container = document.getElementById('container');

// 为注册按钮添加点击事件监听器
signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

// 为登录按钮添加点击事件监听器
signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});

// 登录表单提交处理
document.querySelector('.sign-in-container form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('signinEmail').value;
    const password = document.getElementById('signinPassword').value;
    
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
            // 隐藏登录界面，显示登录成功界面
            document.getElementById('container').style.display = 'none';
            document.getElementById('successContainer').style.display = 'block';
            
            // 存储用户ID到本地存储
            localStorage.setItem('user_id', data.user_id);
        } else {
            let errorMsg = data.message;
            if (data.errors) {
                if (data.errors.email) errorMsg += `\n${data.errors.email}`;
                if (data.errors.password) errorMsg += `\n${data.errors.password}`;
                if (data.errors.ValidationError) errorMsg += `\n${data.errors.ValidationError}`;
            }
            alert(errorMsg);
        }
    } catch (error) {
        console.error('登录请求失败:', error);
        alert('登录请求失败，请检查网络连接');
    }
});

// 前往仪表盘按钮点击事件
document.getElementById('goToDashboard')?.addEventListener('click', () => {
    window.location.href = '/dashboard';
});

// 忘记密码链接点击事件
document.querySelector('.sign-in-container a').addEventListener('click', (e) => {
    e.preventDefault();
    // 创建忘记密码表单
    const forgotPasswordHTML = `
        <form id="forgotPasswordForm">
            <h1>重置密码🔑</h1>
            <span>通过邮箱验证重置密码</span>
            
            <div style="display: flex; align-items: center;">
                <div class="input-group" style="flex-grow: 1;">
                    <input type="email" placeholder="邮箱" id="forgotEmail" required />
                    <label for="forgotEmail">邮箱</label>
                </div>
                <button type="button" id="forgotGetCode">获取验证码</button>
            </div>
            
            <div class="input-group">
                <input type="text" placeholder="验证码" id="forgotCode" required />
                <label for="forgotCode">验证码</label>
            </div>
            
            <div class="input-group">
                <input type="password" placeholder="新密码" id="newPassword" required />
                <label for="newPassword">新密码</label>
            </div>
            
            <div class="input-group">
                <input type="password" placeholder="确认新密码" id="confirmPassword" required />
                <label for="confirmPassword">确认新密码</label>
            </div>
            
            <button type="submit">重置密码</button>
            <a href="#" class="back-to-login">返回登录</a>
        </form>
    `;
    
    // 替换登录表单内容
    const signInContainer = document.querySelector('.sign-in-container');
    signInContainer.innerHTML = forgotPasswordHTML;
    
    // 添加返回登录事件
    document.querySelector('.back-to-login').addEventListener('click', (e) => {
        e.preventDefault();
        location.reload();
    });
    
    // 获取验证码事件
    document.getElementById('forgotGetCode').addEventListener('click', async () => {
        const email = document.getElementById('forgotEmail').value;
        if (!email) {
            alert('请输入邮箱地址');
            return;
        }
        // 这里添加发送验证码的逻辑
        alert('验证码已发送到您的邮箱');
    });
    
    // 表单提交事件
    document.getElementById('forgotPasswordForm').addEventListener('submit', (e) => {
        e.preventDefault();
        
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (newPassword !== confirmPassword) {
            alert('两次输入的密码不一致，请重新输入');
            return;
        }
        
        // 这里添加重置密码的逻辑
        alert('密码重置成功，请使用新密码登录');
        location.reload();
    });
});