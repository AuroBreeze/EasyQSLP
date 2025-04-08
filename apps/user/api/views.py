from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
# Create your views here.

def user_login(request):
    return HttpResponse("user_login")

class RegisterAPI(APIView):
    def post(self, request):
        return Response({"message": "User registered successfully!"})

class LoginAPI(APIView):
    def post(self, request):
        return Response({"message": "User logged in successfully!"})

class Querr(APIView):
    def post(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM test_demo")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return Response(rows)
        #return Response({"message": "User logged in successfully!"})