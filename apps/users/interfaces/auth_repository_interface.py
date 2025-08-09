from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..models.user import User

class AuthRepositoryInterface(ABC):
    
    @abstractmethod
    def register(self, data: Dict[str, Any]) -> User:
        pass
    
    @abstractmethod
    def authenticate(self, email: str, password: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
