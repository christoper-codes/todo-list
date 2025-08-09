from typing import List, Optional, Dict, Any
from django.contrib.auth.hashers import make_password
from ..interfaces.user_repository_interface import UserRepositoryInterface
from ..models.user import User

class UserRepository(UserRepositoryInterface):
    
    def list(self) -> List[User]:
        return User.objects.all().order_by('-created_at')
    
    def show(self, user_id: int) -> Optional[User]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    def store(self, data: Dict[str, Any]) -> User:
        if 'password' in data:
            data['password'] = make_password(data['password'])
        return User.objects.create(**data)
    
    def update(self, user_id: int, data: Dict[str, Any]) -> Optional[User]:
        try:
            user = User.objects.get(id=user_id)
            
            if 'password' in data:
                data['password'] = make_password(data['password'])
            
            for key, value in data.items():
                setattr(user, key, value)
            
            user.save()
            return user
        except User.DoesNotExist:
            return None
    
    def destroy(self, user_id: int) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
