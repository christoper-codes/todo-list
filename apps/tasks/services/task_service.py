from typing import List, Optional
from django.core.exceptions import ValidationError
from ..repositories.task_repository import TaskRepository


class TaskService:
    
    def __init__(self, task_repository = None):
        self.task_repository = task_repository or TaskRepository()
    
    def list(self) -> List:
        return self.task_repository.list()
    
    def show(self, task_id: int) -> Optional:
        return self.task_repository.show(task_id)
    
    def store(self, task_data: dict):
        return self.task_repository.store(task_data)
    
    def update(self, task_id: int, task_data: dict) -> Optional:
        return self.task_repository.update(task_id, task_data)
    
    def destroy(self, task_id: int) -> bool:
        return self.task_repository.destroy(task_id)