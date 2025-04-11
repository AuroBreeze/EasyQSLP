from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from ..models import User_Login

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        print(email,password)

        if email and password:
            # 只有使用hash保存的密码才能使用authenticate验证
            user = authenticate(email=email, password=password)
            print(user)
            # ee = User_Login.objects.get(email=email)
            # print(ee)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise ValidationError("User account is disabled.")
            else:
                raise ValidationError("Unable to log in with provided credentials.")
        else:
            raise ValidationError("Must provide email and password.")

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