from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from core.mixins.error_handler_mixin import ErrorHandlerMixin
from ..services.auth_service import AuthService
from ..serializers.auth import (
    RegisterSerializer, 
    LoginSerializer, 
    TokenRefreshSerializer,
    UserProfileSerializer
)

class RegisterView(ErrorHandlerMixin, APIView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()
    
    def post(self, request):
        try:
            with transaction.atomic():
                serializer = RegisterSerializer(data=request.data)
                validated_data = self.validate_serializer(serializer)
                
                result = self.auth_service.register(validated_data)
                user_serializer = UserProfileSerializer(result['user'])
                
                return self.success_response(
                    data={'user': user_serializer.data, 'tokens': result['tokens']},
                    message='User registered successfully',
                    status_code=status.HTTP_201_CREATED
                )
        except Exception as e:
            return self.handle_error(e, 'Error registering user')

class LoginView(ErrorHandlerMixin, APIView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()
    
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            validated_data = self.validate_serializer(serializer)
            
            result = self.auth_service.login(email=validated_data['email'], password=validated_data['password'])
            if not result:
                return Response({'errors': {'general': ['Invalid credentials']}}, status=status.HTTP_401_UNAUTHORIZED)

            user_serializer = UserProfileSerializer(result['user'])
            return self.success_response(data={'user': user_serializer.data, 'tokens': result['tokens']}, message='Login successful')
        except Exception as e:
            return self.handle_error(e, 'Error during login')

class LogoutView(ErrorHandlerMixin, APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            
            if refresh_token:
                from rest_framework_simplejwt.tokens import RefreshToken
                token = RefreshToken(refresh_token)
                token.blacklist()

            return self.success_response(message='Logout successful', status_code=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return self.handle_error(e, 'Error during logout')

