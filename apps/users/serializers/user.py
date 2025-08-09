from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from ..models import User


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'is_active', 'created_at']


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'full_name', 'is_active', 'created_at', 'updated_at']


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate_email(self, value):
        user = getattr(self, 'instance', None)
        if user:
            if User.objects.filter(email=value).exclude(pk=user.pk).exists():
                raise serializers.ValidationError("This email is already registered")
        else:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already registered")
        return value.lower().strip()
    
    def validate_username(self, value):
        user = getattr(self, 'instance', None)
        if user:
            if User.objects.filter(username=value).exclude(pk=user.pk).exists():
                raise serializers.ValidationError("This username is already taken")
        else:
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("This username is already taken")
        return value.strip()
    
    def validate_first_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long")
        return value.strip().title()
    
    def validate_last_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long")
        return value.strip().title()
    
    def validate_password(self, value):
        if value:
            validate_password(value)
        return value
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise serializers.ValidationError({
                    'password_confirm': 'Passwords do not match'
                })
        elif password and not password_confirm:
            raise serializers.ValidationError({
                'password_confirm': 'Password confirmation is required'
            })
        elif not password and password_confirm:
            raise serializers.ValidationError({
                'password': 'Password is required'
            })
        
        if 'password_confirm' in attrs:
            attrs.pop('password_confirm')
        
        return attrs
