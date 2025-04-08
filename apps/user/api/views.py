from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

def user_login(request):
    return HttpResponse("user_login")

class RegisterAPI(APIView):
    def post(self, request):
        return Response({"message": "User registered successfully!"})

class LoginAPI(APIView):
    def post(self, request):
        return Response({"message": "User logged in successfully!"})
    