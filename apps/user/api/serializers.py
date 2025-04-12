from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from ..models import User_Login

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

    print(email,password,username)

    class Meta:
        model = User_Login
        fields = ['email','password','username']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)