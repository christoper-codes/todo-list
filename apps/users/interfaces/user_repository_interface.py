from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..models.user import User

class UserRepositoryInterface(ABC):
    
    @abstractmethod
    def list(self) -> List[User]:
        pass
    
    @abstractmethod
    def show(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def store(self, data: Dict[str, Any]) -> User:
        pass
    
    @abstractmethod
    def update(self, user_id: int, data: Dict[str, Any]) -> Optional[User]:
        pass
    
    @abstractmethod
    def destroy(self, user_id: int) -> bool:
        pass
