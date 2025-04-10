// 获取注册按钮元素
const signUpButton = document.getElementById('signUp');
// 获取登录按钮元素
const signInButton = document.getElementById('signIn');
// 获取容器元素
const container = document.getElementById('container');

// 为注册按钮添加点击事件监听器
signUpButton.addEventListener('click', () => {
    // 为容器添加 right-panel-active 类，切换到注册界面
    container.classList.add("right-panel-active");
});

// 为登录按钮添加点击事件监听器
signInButton.addEventListener('click', () => {
    // 从容器中移除 right-panel-active 类，切换到登录界面
    container.classList.remove("right-panel-active");
});