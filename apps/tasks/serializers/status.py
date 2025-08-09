from rest_framework import serializers
from ..models import Status

class StatusSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Status
        fields = '__all__'


class StatusListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Status
        fields = ['id', 'name']