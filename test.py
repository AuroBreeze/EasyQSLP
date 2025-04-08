import requests
url = "http://127.0.0.1:8000/api/v1/user/querr/"

res = requests.post(url).json()
print(res)