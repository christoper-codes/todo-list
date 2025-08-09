from typing import List, Optional, Dict, Any
from ..interfaces.user_repository_interface import UserRepositoryInterface
from ..repositories.user_repository import UserRepository
from ..models.user import User

class UserService:
    
    def __init__(self, user_repository: UserRepositoryInterface = None):
        self.user_repository = user_repository or UserRepository()
    
    def list(self) -> List[User]:
        return self.user_repository.list()
    
    def show(self, user_id: int) -> Optional[User]:
        return self.user_repository.show(user_id)
    
    def store(self, data: Dict[str, Any]) -> User:
        return self.user_repository.store(data)
    
    def update(self, user_id: int, data: Dict[str, Any]) -> Optional[User]:
        return self.user_repository.update(user_id, data)
    
    def destroy(self, user_id: int) -> bool:
        return self.user_repository.destroy(user_id)
