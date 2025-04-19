from django.core.validators import MinLengthValidator
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from ..models import *
from django.utils import timezone

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,error_messages={"required":"邮箱不能为空","invalid":"邮箱格式不正确"})
    password = serializers.CharField(required=True,write_only=True,error_messages={"required":"密码不能为空","blank":"密码不能为空"})
    def validate(self, data):#使用中文注释
        email = data.get('email')
        password = data.get('password')
        #print(email,password)
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise ValidationError({"ValidationError":"用户已被禁用"})
            else:
                raise ValidationError({"ValidationError":"邮箱或密码错误"})
        else:
            raise ValidationError({"ValidationError":"邮箱或密码不能为空"})
        return data
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50,required=True)
    password = serializers.CharField(max_length=255,required=True,write_only=True)
    username = serializers.CharField(max_length=20,validators=[MinLengthValidator(2)],required=True)
    code = serializers.CharField(max_length=6,min_length=6,required=True,write_only=True)
    usage = serializers.CharField(max_length=25,required=False,write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        code = data.get('code')
        usage = data.get('usage')
        if usage != "Register":
            raise ValidationError({"ValidationError":"注册方式错误"})
        if email and password and username and code:
            if User_Login.objects.filter(email=email).exists():
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

        user = User_Login.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            is_active=True,
            )
        user.save()
        return user

    class Meta:
        model = User_Login
        fields = ['email','password','username','code',"usage"]
class EmailCodeSendSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50,required=True)
    code = serializers.CharField(max_length=6,required=True,write_only=True)
    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        if User_Login.objects.filter(email=email).exists():
            raise ValidationError({"ValidationError":"邮箱已被注册"})
        try:
            record = Email_Verify_Code.objects.get(email=email)
        except Email_Verify_Code.DoesNotExist:
            raise ValidationError({"ValidationError":"验证码无效或已过期"})
        if record.code != code:
            raise ValidationError({"ValidationError":"验证码错误"})
        if record.is_expired():
            raise ValidationError({"ValidationError":"验证码已过期"})
        if record.send_limit():
            raise ValidationError({"ValidationError":"验证码发送太频繁"})
        return data
    class Meta:
        model = Email_Verify_Code
        fields = ['email',"code"]
class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50,required=True)
    code = serializers.CharField(min_length=6,max_length=6,required=True,write_only=True)
    password = serializers.CharField(min_length=8,max_length=255,required=True,write_only=True)
    password_confirm = serializers.CharField(min_length=8,max_length=255,required=True,write_only=True)
    
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

        
        
        