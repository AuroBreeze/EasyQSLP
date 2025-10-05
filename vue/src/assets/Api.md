登录
/api/v1/user/login/
    传入：  {
    "email": "test@test.com", （必须）
    "password": "12345678"  （必须）
    }
    返回： 200 ：{
    "success": true,
    "message": "Login successful",
    "username": "tester",
    "user_id": 2
    }
            400：{
    "success": false,
    "message": "Invalid credentials",
    "errors": {
        "ValidationError": "邮箱或密码错误"
        }
    }

邮箱是否存在
/api/v1/user/account/exist/
    传入：  {
    "email": "string"   必须
    }
    返回：  200：   {
    "success": true,
    "message": "string",
    "data": {
        "by": "string",
        "value": "string",
        "exists": true
        }
    }

注册
/api/v1/user/register/
    传入：  {
    "email": "string",  必须
    "password": "string",   必须
    "username": "string",   必须
    "code": "string"    必须
    }
    返回： 200： {}

验证码获取
/api/v1/user/emailsendcode/
    传入：  {
    "email": "lnf13@soh.com",   必须
    "usage": "Register/ResetPassword"   必须
    }
    返回： 201：   {
    "success": true,
    "message": "Email code sent successfully!",
    "code": "330510"
    }
            429：  {
    "success": false,
    "message": "发送频率过快，请稍后再试"
    } 
            400：   {
    "success": false,
    "message": "usage参数错误"
    }

JWT 获取
/api/v1/user/token/
    传入：  {
    "email": "k1zsbt6@126.com", （必须）
    "password": "fOiA_4PkN61v4Sh"   （必须）
    }
    返回：  200：   {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1OTQ3Mzk5NywiaWF0IjoxNzU5NDcwMzk3LCJqdGkiOiI1NjNjZmRkMDUxYWQ0NzIzOGUzNThmMDYzMTdlNjM4YiIsInVzZXJfaWQiOjIsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSIsInVzZXJuYW1lIjoidGVzdGVyIiwiaXNfYWN0aXZlIjp0cnVlfQ.7tDDYegbeznEYkDnRWCqGRNfTM64rpyqXkZ3SDNHO70",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5NDcyMTk3LCJpYXQiOjE3NTk0NzAzOTcsImp0aSI6IjEwMzgxNDA2M2E1YjRiZjc4YTYxYjk4ZGFmOWIxYTUyIiwidXNlcl9pZCI6MiwiZW1haWwiOiJ0ZXN0QHRlc3QuY29tIiwidXNlcm5hbWUiOiJ0ZXN0ZXIiLCJpc19hY3RpdmUiOnRydWV9.bRVQ4cZoQD4fiErmUJb56PPAuqKmN3AYL8RLnmOqSeg"
    }
            400：   {
    "success": false,
    "message": "Invalid credentials",
    "errors": {
        "ValidationError": "邮箱或密码错误"
        }
    }

JWT 刷新
/api/v1/user/token/refresh/
    传入：  {
    "refresh": "qui laborum tempor" （必须）
    }
    返回：  200：   {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5NDcxODA5LCJpYXQiOjE3NTk0NzAwMDksImp0aSI6ImM1MTU3NmEzZGJhMTQ3Y2U4MjAwNjZjN2NkZjhiY2U1IiwidXNlcl9pZCI6MiwiZW1haWwiOiJ0ZXN0QHRlc3QuY29tIiwidXNlcm5hbWUiOiJ0ZXN0ZXIiLCJpc19hY3RpdmUiOnRydWV9.vz4Bx0378kmsJApFFYjZA42KU-zqgCgd9eDa3nSVcew",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1OTQ3MzYwOSwiaWF0IjoxNzU5NDcwMDA5LCJqdGkiOiI0NDE2OWJlOTdmMTU0Yjg4YTNmZDY1Y2JjZDI5ZjBjMiIsInVzZXJfaWQiOjIsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSIsInVzZXJuYW1lIjoidGVzdGVyIiwiaXNfYWN0aXZlIjp0cnVlfQ.bLEEI6-YVnaHJx_yW8_KywpNO-skSdz5p12QxuPjWoc"
    }
            400：   {
    "success": false,
    "message": "Invalid credentials",
    "errors": {
        "ValidationError": "令牌错误"
        }
    }

JWT 验证
/api/v1/user/token/verify/
    传入： {
    "token": "Excepteur Lorem"  必须
    }
    返回： 200：    {}
            400：   {
    "success": false,
    "message": "Invalid credentials",
    "errors": {
        "ValidationError": "令牌错误"
        }
    }
