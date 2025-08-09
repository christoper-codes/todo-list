from abc import ABC, abstractmethod
from typing import List, Optional


class TaskRepositoryInterface(ABC):
    
    @abstractmethod
    def list(self) -> List:
        pass
    
    @abstractmethod
    def show(self, task_id: int) -> Optional:
        pass
    
    @abstractmethod
    def store(self, task_data: dict):
        pass
    
    @abstractmethod
    def update(self, task_id: int, task_data: dict) -> Optional:
        pass
    
    @abstractmethod
    def destroy(self, task_id: int) -> bool:
        pass