from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from ..models import *
# Create your views here.

def user_login(request):
    return HttpResponse("user_login")

class RegisterAPI(APIView):
    def post(self, request):
        user = User_Login(username="123456", password="1234567890")
        user.save()
        return Response({"message": "User registered successfully!"})

class LoginAPI(APIView):
    def post(self, request):
        user = User_Login.objects.get(username="123456")
        return Response({"message": f"User {user.username} logged in successfully!"})

class DeletAPI(APIView):
    def post(self, request):
        user = User_Login.objects.get(username="123456")
        user.delete()
        return Response({"message": "User deleted successfully!"})
class ChangeAPI(APIView):
    def post(self, request):
        user = User_Login.objects.get(username="123456")
        user.password = "9876543210"
        user.save()
        return Response({"message": "User password changed successfully!"})


class Querr(APIView):
    def post(self, request):
        users = User_Login.objects.all()
        users = [user.username for user in users]
        return Response({"message": f"Users:{users}"})

class ArticleAPI(APIView):
    def post(self, request):
        # user = User_Login(username="fhajsdhflk", password="1234567890",email="123@123.com")
        # user.save()
        # article = Article(title="Article1", content="This is the content of the article", author=user)
        # article.save()
        article = Article.objects.first()
        print(article)
        return Response({"message": f"Article {article.author.username} created successfully!"})

class ArticleListAPI(APIView):
    def post(self, request):
        user = User_Login.objects.first()
        articles = user.articles.all() 
        #正常应该是user.article_set.all() 'article'是模型的名字(小写)，加上'_set'固定写法
        #因为Article模型使用了related_name='articles'，所以可以这样写
        #这是两种写法
        articles = [article.title for article in articles]
        return Response({"message": f"Articles:{articles}"})