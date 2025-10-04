from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Email_Verify_Code

@shared_task
def send_email_task(user_email,code:str):
    message_html = f"""
        <html>
            <body>
                <h1>EasyQFLP System Notification🚀</h1>
                <span>
                <p>感谢您加入 EasyQFLP，这是一个基于项目的知识分享型网站，致力于打破信息差，提供更多的其他领域的<strong>从零开始</strong>的学习项目，让更多的人可以接触到更多的知识，以便寻找到属于自己的方向。🌍</p>
                <p>您的验证码为：<strong>{code}</strong></p>
                <p>验证码将在 5 分钟后过期。</p>
                <p>请使用此验证码完成注册流程。</p>
                <p>期待您的加入，一起探索知识的海洋！</p>
                </span>
                
                <p>如果本操作不是您本人所发起的，请注意您的个人信息安全，及时修改密码。</p>
                <a href="https://easyqflp.top/">重置密码</a>
                
                <p>此邮件为系统自动发送，请勿回复。</p>
                <p>Best regards,<br>EasyQFLP Team</p>
            </body>
        </html>
        """
    send_mail(
        subject="欢迎注册EasyQFLP",
        message=None, # 纯文本邮件
        html_message=message_html,
        from_email="easyqflp@nvc0qfnu.top",
        recipient_list=[user_email],
        fail_silently=False,
    )

@shared_task
def clear_expired_codes_task():
    # 获取当前时间
    now = timezone.now()
    
    # 查询所有过期的验证码
    expired_codes = Email_Verify_Code.objects.filter(expire_time__lte=now)
    
    # 获取过期验证码的数量
    count_num = expired_codes.count()
    
    # 删除所有过期的验证码
    expired_codes.delete()
    
    return f"已删除{count_num} 个过期验证码(当前时间：{now})"
