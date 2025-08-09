from django.urls import path
from .views.task_view import TaskViewSet

task_viewset = TaskViewSet.as_view({'get': 'list', 'post': 'create'})
task_detail_viewset = TaskViewSet.as_view({'put': 'update', 'patch': 'update', 'delete': 'destroy'})

urlpatterns = [
    path('api/tasks', task_viewset, name='tasks-list'),
    path('api/tasks/<int:pk>', task_detail_viewset, name='tasks-detail'),
]
