from typing import Dict, Any, Optional
from rest_framework_simplejwt.tokens import RefreshToken
from ..interfaces.auth_repository_interface import AuthRepositoryInterface
from ..repositories.auth_repository import AuthRepository
from ..models.user import User

class AuthService:
    
    def __init__(self, auth_repository: AuthRepositoryInterface = None):
        self.auth_repository = auth_repository or AuthRepository()
    
    def register(self, data: Dict[str, Any]) -> Dict[str, Any]:
        user = self.auth_repository.register(data)
        tokens = self._generate_tokens(user)

        return {'user': user, 'tokens': tokens}

    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        user = self.auth_repository.authenticate(email, password)
        
        if user and user.is_active:
            tokens = self._generate_tokens(user)
            return {'user': user, 'tokens': tokens}

        return None
    
    def refresh_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        try:
            refresh = RefreshToken(refresh_token)
            return {'access': str(refresh.access_token)}
        except Exception:
            return None
    
    def _generate_tokens(self, user: User) -> Dict[str, str]:
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
