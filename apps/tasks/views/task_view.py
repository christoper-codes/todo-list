from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.core.exceptions import ValidationError
from core.mixins.error_handler_mixin import ErrorHandlerMixin
from ..services.task_service import TaskService
from ..serializers.task import TaskListSerializer, TaskDetailSerializer, TaskCreateUpdateSerializer

class TaskViewSet(ErrorHandlerMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_service = TaskService()
    
    def list(self, request):
        try:
            tasks = self.task_service.list()
            serializer = TaskListSerializer(tasks, many=True)
            return self.success_response(data=serializer.data, message='Tasks retrieved')
        except Exception as e:
            return Response({'errors': {'general': [f'Error retrieving tasks: {str(e)}']}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            with transaction.atomic():
                serializer = TaskCreateUpdateSerializer(data=request.data)
                validated_data = self.validate_serializer(serializer) 

                task = self.task_service.store(validated_data)
                response_serializer = TaskDetailSerializer(task)
                return self.success_response(data=response_serializer.data, message='Task created', status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return self.handle_error(e, 'Error creating task')

    def update(self, request, pk=None):
        try:
            with transaction.atomic():
                serializer = TaskCreateUpdateSerializer(data=request.data, partial=True)
                validated_data = self.validate_serializer(serializer) 

                task = self.task_service.update(int(pk), validated_data)
                if not task:
                    return Response({'errors': {'general': ['Task not found']}}, status=status.HTTP_404_NOT_FOUND)

                response_serializer = TaskDetailSerializer(task)
                return self.success_response(data=response_serializer.data, message='Task updated')
        except Exception as e:
            return self.handle_error(e, 'Error updating task')

    def destroy(self, request, pk=None):
        try:
            with transaction.atomic():
                deleted = self.task_service.destroy(int(pk))
                if not deleted:
                    return Response({'errors': {'general': ['Task not found']}}, status=status.HTTP_404_NOT_FOUND)
                
                return self.success_response(message='Task deleted', status_code=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return self.handle_error(e, 'Error deleting task')
