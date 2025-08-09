from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from ..models.user import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered")
        return value.lower().strip()
    
    def validate_first_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long")
        return value.strip().title()
    
    def validate_last_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long")
        return value.strip().title()
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match'
            })
        
        email = attrs['email']
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        attrs['username'] = username
        attrs.pop('password_confirm')
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate_email(self, value):
        return value.lower().strip()


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'is_active', 'created_at']
