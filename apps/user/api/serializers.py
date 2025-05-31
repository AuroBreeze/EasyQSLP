import imghdr # 验证图片格式
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from ..models import *
from PIL import Image
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import markdown
import markdown



class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        token['is_active'] = user.is_active
        return token

# 用户登录序列化器
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,error_messages={"required":"邮箱不能为空","invalid":"邮箱格式不正确"})
    password = serializers.CharField(required=True,write_only=True,error_messages={"required":"密码不能为空","blank":"密码不能为空"})

    # 验证邮箱和密码
    def validate(self, data):#使用中文注释
        email = data.get('email')
        password = data.get('password')
        #print(email,password)
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active: # 判断用户是否激活
                    data['user'] = user
                else:
                    raise ValidationError({"ValidationError":"用户已被禁用"})
            else:
                raise ValidationError({"ValidationError":"邮箱或密码错误"})
        else:
            raise ValidationError({"ValidationError":"邮箱或密码不能为空"})
        return data
    class Meta:
        model = User_Login
        fields = ['email','join_date','username']

# 用户注册序列化器
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50,required=True)
    password = serializers.CharField(max_length=255,required=True,write_only=True)
    username = serializers.CharField(max_length=20,validators=[MinLengthValidator(2)],required=True)
    code = serializers.CharField(max_length=6,min_length=6,required=True,write_only=True,error_messages={"required":"验证码不能为空","min_length":"验证码长度为6位","max_length":"验证码长度为6位"})
    # 验证码用途，防止一码多用(注册和重置密码)
    #usage = serializers.CharField(max_length=25,required=False,write_only=True,error_messages={"required":"用途不能为空"})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        code = data.get('code')
        #usage = data.get('usage')
        #if usage != "Register": # 注册方式错误
            #raise ValidationError({"ValidationError":"注册方式错误"})
        if email and password and username and code: # 验证数据
            if User_Login.objects.filter(email=email).exists(): # 邮箱已被注册
                raise ValidationError({"ValidationError":"邮箱已被注册"})
            if User_Login.objects.filter(username=username).exists():
                raise ValidationError({"ValidationError":"用户名已被注册"})
        else:
            raise ValidationError({"ValidationError":"邮箱、密码、用户名、验证码不能为空"})
        if Email_Verify_Code.objects.filter(email=email).exists() and Email_Verify_Code.objects.filter(email=email).first().usage == "Register":
            if Email_Verify_Code.objects.filter(email=email).first().is_expired():
                raise ValidationError({"ValidationError":"验证码已过期"})
            if Email_Verify_Code.objects.filter(email=email).first().code != code:
                raise ValidationError({"ValidationError":"验证码错误"})
        else:
            raise ValidationError({"ValidationError":"邮箱未发送验证码"})
        return data

    def create(self, validated_data):

        user = User_Login.objects.create_user(email=validated_data['email'], username=validated_data['username'],
                                              password=validated_data['password'])
        user.save() # 创建用户

        user_profile = User_Profile.objects.create(
            user_Login=user,
        )
        user_profile.save() # 创建用户资料
        return user

    class Meta:
        model = User_Login
        fields = ['email','password','username','code']


# 重置密码序列化器

class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50,required=True)
    code = serializers.CharField(min_length=6,max_length=6,required=True,write_only=True,error_messages={"min_length":"验证码长度为6位","max_length":"验证码长度为6位"})
    password = serializers.CharField(min_length=8,max_length=255,required=True,write_only=True,error_messages={"required":"密码不能为空","min_length":"密码长度不能小于8位","max_length":"密码长度不能大于255位"})
    password_confirm = serializers.CharField(min_length=8,max_length=255,required=True,write_only=True,error_messages={"required":"密码不能为空","min_length":"密码长度不能小于8位","max_length":"密码长度不能大于255位"})
    
    class Meta:
        model = Email_Verify_Code
        fields = ['email','code','password','password_confirm']
        
    def validate(self,data):
        email = data.get('email')
        code = data.get('code')
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        
        if User_Login.objects.filter(email=email).exists() == False:
            raise ValidationError({"ValidationError":"邮箱未注册"})
        if password != password_confirm:
            raise ValidationError({"ValidationError":"两次密码不一致"})
        
        if Email_Verify_Code.objects.filter(email=email).exists() and Email_Verify_Code.objects.filter(email=email).first().usage == "ResetPassword":
            if Email_Verify_Code.objects.filter(email=email).first().is_expired():
                raise ValidationError({"ValidationError":"验证码已过期"})
            if Email_Verify_Code.objects.filter(email=email).first().code != code:
                raise ValidationError({"ValidationError":"验证码错误"})
        else:
            raise ValidationError({"ValidationError":"邮箱未发送验证码"})
        
        return data
    
    def update(self,instance,validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        
        user = User_Login.objects.get(email=email)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    toc = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()
    toc = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()
    def validate_avatar(self, value):
        # 图片类型
        image_type = imghdr.what(value)
        if image_type not in ['jpeg','png','jpg']:
            raise ValidationError({"ValidationError":"图片格式错误,仅允许 jpeg,png,jpg"})
        # 图片大小
        if value.size > 4 * 1024 * 1024:
            raise ValidationError({"ValidationError":"图片大小不能超过 4M"})

        # 图片尺寸
        image = Image.open(value)
        width, height = image.size
        if width > 1024 or height > 1024:
            raise ValidationError({"ValidationError":"图片尺寸不能超过 1024x1024"})
        return value
    def get_toc(self, obj):
        """
        生成目录
        """
        md = markdown.Markdown(extensions=['markdown.extensions.toc'])
        md.convert(obj.content_md)
        return md.toc

    def get_word_count(self, obj):
        return len(obj.content_md.split())
    class Meta:
        model = User_Profile
        fields = ['avatar','userprofile_md','userprofile_html','content_hash','create_time','update_time','user_Login']
