from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from .serializers import *
from django_ratelimit.decorators import ratelimit
# Create your views here.

class RegisterAPI(APIView):
    @method_decorator(ratelimit(key='ip', rate='3/hour'))  # 同一 IP 每小时最多注册5次
    def post(self, request):
        # user = User_Login(username="AuroBreeze", password="123123123",email="123@qq.com")
        # user.save()
        serialize = UserRegisterSerializer(data=request.data)
        #print(request.data)
        if serialize.is_valid():
            serialize.save()
            return Response({"message": "User registered successfully!"},status=status.HTTP_201_CREATED)
        else:
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response({"message": "User registered successfully!"})

class LoginAPI(APIView):
    @method_decorator(ratelimit(key='ip', rate='3/hour'))  # 同一 IP 每小时最多登录5次
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            # 这里可以添加生成 token 或 session 的逻辑
            return Response({"success": True,"message": "Login successful", "uuid_user": user.uuid_user,"username": user.username}, status=status.HTTP_200_OK)
        else:
            errors = serializer.errors
            error_dict = {}
            # 提取错误信息并转换为字符串
            for field, error_list in errors.items():
                if error_list:
                    error_dict[field] = error_list[0]  # 取第一个错误
            return Response({
                "success": False,
                "message": "Invalid credentials",
                "errors": error_dict  # 仅包含有错误的字段
            }, status=status.HTTP_400_BAD_REQUEST)
class EmailCodeSendAPI(APIView):
    #@method_decorator(ratelimit(key="ip", rate='1/minute'))
    def post(self,request):
        serializer = EmailCodeSendSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            error_dict = {}
            # 提取错误信息并转换为字符串
            for field, error_list in errors.items():
                if error_list:
                    error_dict[field] = error_list[0] 
            return Response({
                "success": False,
                "message": "Invalid email",
                "errors": error_dict  # 仅包含有错误的字段
            }, status=status.HTTP_400_BAD_REQUEST)
        
        #print(serializer.instance)
        serializer.save()
        #print(serializer.data['code'])
        #send_email(email, serializer.data['code'])
        return Response({"success": True, "message": "Email code sent successfully!","code":serializer.data['code']},status=status.HTTP_201_CREATED)
            

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
        # users = User_Login.objects.get(username__exact=1) #获取id为1的用户,'__exact'是精确匹配，'__iexact'是忽略大小写的匹配
        # users = User_Login.objects.filter(username__contains='123').all() #获取用户名包含'123'的用户,'__contains'是包含匹配,'__icontains'是忽略大小写的包含匹配
        # users = User_Login.objects.filter(username__in=['123','456','789']).all() #获取用户名为'123'、'456'、'789'的用户,'__in'是范围匹配
        # users = User_Login.objects.filter(username__startswith='123') #获取用户名以'123'开头的用户,'__startswith'是前缀匹配,'__istartswith'是忽略大小写的前缀匹配
        # users = User_Login.objects.filter(username__endswith='123') #获取用户名以'123'结尾的用户,'__endswith'是后缀匹配,'__iendswith'是忽略大小写的后缀匹配
        # users = User_Login.objects.filter(join_date__range=('2021-01-01','2021-12-31')) #获取2021年1月1日到2021年12月31日创建的用户,'__range'是范围匹配
        # users = User_Login.objects.filter(id__gt=1) #获取id大于1的用户,'__gt'是大于匹配,'__gte'是大于等于匹配
        # users = User_Login.objects.filter(id__lt=1) #获取id小于1的用户,'__lt'是小于匹配,'__lte'是小于等于匹配
        # users = User_Login.objects.filter(id__isnull=True) #获取id为空的用户,'__isnull'是为空匹配
        # users = User_Login.objects.filter(username__regex=r'^123') #获取用户名以'123'开头的用户,'__regex'是正则匹配,'__iregex'是忽略大小写的正则匹配
        
        # users = User_Login.objects.filter(articles__title__icontains="Article") #使用根据关联表进行查询，获取作者名包含'Article'的文章
        users = [user.password for user in users]
        
        # F表达式
        # 查找用户名和密码都相同的用户
        # from django.db.models import F
        # users = User_Login.objects.filter(username=F('password')).all()
        
        # Q表达式
        # 查找用户加入时间大于2021年1月1日的用户
        # from django.db.models import Q
        # users = User_Login.objects.filter(Q(join_date__gte="2021") |  Q(join_date__lte="2022")).all()
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

class ArticleListAPI(APIView): #一对多关系
    def post(self, request):
        user = User_Login.objects.first()
        #筛选出title包含'Article'的文章
        #articles = user.articles.filter(title__contains="Article").all()
        articles = user.articles.all() 
        #正常应该是user.article_set.all() 'article'是模型的名字(小写)，加上'_set'固定写法
        #因为Article模型使用了related_name='articles'，所以可以这样写
        #这是两种写法
        articles = [article.title for article in articles]
        
        return Response({"message": f"Articles:{articles}"})