from typing import Dict, Any, Optional
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from ..interfaces.auth_repository_interface import AuthRepositoryInterface
from ..models.user import User

class AuthRepository(AuthRepositoryInterface):
    
    def register(self, data: Dict[str, Any]) -> User:
        data['password'] = make_password(data['password'])
        return User.objects.create(**data)
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = authenticate(username=email, password=password)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
