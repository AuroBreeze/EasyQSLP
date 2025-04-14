import requests

url_register = "http://127.0.0.1:8000/api/v1/user/register/"
url_querr = "http://127.0.0.1:8000/api/v1/user/querr/"
url_login = "http://127.0.0.1:8000/api/v1/user/login/"
url_article = "http://127.0.0.1:8000/api/v1/user/article/"
url_articlelist = "http://127.0.0.1:8000/api/v1/user/articlelist/"

# 登录测试
login_data = {
    "email": "123@qq.com",
    "password": "123123123"
}
login_data1={
    "email": "123123@qq.com",
    "password": "123123123"
}
register_data = {
    "email": "123123@qq.com",
    "password": "123123123",
    "username": "AuroBreeze111"
}
#res = requests.post(url_register, json=register_data).json()
#res = requests.post(url_login, json=login_data1).json()
res = requests.post(url_querr).json()
print(res)