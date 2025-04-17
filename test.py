import requests

url_register = "http://127.0.0.1:8000/api/v1/user/register/"
url_querr = "http://127.0.0.1:8000/api/v1/user/querr/"
url_login = "http://127.0.0.1:8000/api/v1/user/login/"
url_article = "http://127.0.0.1:8000/api/v1/user/article/"
url_articlelist = "http://127.0.0.1:8000/api/v1/user/articlelist/"
url_codesend = "http://127.0.0.1:8000/api/v1/user/emailsendcode/"
url_resetpwd = "http://127.0.0.1:8000/api/v1/user/resetpassword/"
# 登录测试
login_data = {
    "email": "123@qq.com",
    "password": "123123123"
}
login_data1={
    "email": "123123@qq.com",
    "password": "123456789"
}
register_data = {
    "email": "123123@qq.com",
    "password": "123123123",
    "username": "AuroBreeze",
    "code": "738963",#572741
    "usage": "Register"
}

email_data = {
    "email": "123123@qq.com",
    "usage": "ResetPassword"#Register or ResetPassword
}


#res = requests.post(url_register, json=register_data).json()
res = requests.post(url_login, json=login_data1).json()
# code_data = requests.post(url_codesend, json=email_data).json()
# print(code_data)
# code = code_data["code"]
# print(code)
# resetpwd_data = {
#     "email": "123123@qq.com",
#     "code": "896281",
#     "password": "123456789",
#     "password_confirm": "123456789"
# }
# res = requests.post(url_resetpwd, json=resetpwd_data).json()
print(res)