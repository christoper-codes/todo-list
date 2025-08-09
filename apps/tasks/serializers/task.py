from rest_framework import serializers
from ..models import Task


class TaskListSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    status_id = serializers.IntegerField(source='status.id', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status_id', 'status_name', 'user_id', 'user_name', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    status_id = serializers.IntegerField(source='status.id', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status_id', 'status_name', 
                 'user_id', 'user_name', 'created_at', 'updated_at']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    status_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'user_id', 'status_id']
    
    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value.strip()
    
    def validate_status_id(self, value):
        from ..models.status import Status
        if not Status.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected status does not exist")
        return value
    
    def validate_user_id(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected user does not exist")
        return value
    
    def create(self, validated_data):
        status_id = validated_data.pop('status_id')
        user_id = validated_data.pop('user_id')
        validated_data['status_id'] = status_id
        validated_data['user_id'] = user_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'status_id' in validated_data:
            status_id = validated_data.pop('status_id')
            validated_data['status_id'] = status_id
        if 'user_id' in validated_data:
            user_id = validated_data.pop('user_id')
            validated_data['user_id'] = user_id
        return super().update(instance, validated_data)