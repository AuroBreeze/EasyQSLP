import requests
url = "http://127.0.0.1:8000/user/login/"

res = requests.post(url).text
print(res)