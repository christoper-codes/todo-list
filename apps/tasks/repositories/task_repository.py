from typing import List, Optional
from ..models.task import Task
from ..interfaces.task_repository_interface import TaskRepositoryInterface


class TaskRepository(TaskRepositoryInterface):

    def list(self) -> List:
        return Task.objects.select_related('status').all()
    
    def show(self, task_id: int) -> Optional:
        try:
            return Task.objects.select_related('status').get(id=task_id)
        except Task.DoesNotExist:
            return None
    
    def store(self, task_data: dict):
        return Task.objects.create(**task_data)

    def update(self, task_id: int, task_data: dict) -> Optional:
        try:
            task = Task.objects.get(id=task_id)
            for field, value in task_data.items():
                setattr(task, field, value)
            task.save()
            return task
        except Task.DoesNotExist:
            return None
    
    def destroy(self, task_id: int) -> bool:
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return True
        except Task.DoesNotExist:
            return False
