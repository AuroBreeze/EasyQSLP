from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(user_email,message:str):
    send_mail(
        subject="欢迎注册",
        message=message,
        from_email="noreply@qq.com",
        recipient_list=[user_email],
        fail_silently=False,
    )
