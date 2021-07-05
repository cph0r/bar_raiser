from rest_framework import serializers
from .models import videos

class videos_serializer(serializers.ModelSerializer):
    class Meta:
        model = videos
        fields = '__all__'
