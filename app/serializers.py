from rest_framework import serializers
from .models import user

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'
        ordering = '-date'