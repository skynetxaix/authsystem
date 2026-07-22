from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    username=serializers.CharField(required=True)
    class Meta:
        model=User
        fields=['username','email','password']

    def create(self,validated_data):
        user= User.objects.create_user(

            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False

        )
       
        return user
    

    def validate_password(self, value):
        validate_password(value)
        return value
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)