from elasticsearch_dsl import document
from rest_framework import serializers
from .models import videos
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *

class videos_serializer(DocumentSerializer):
    class Meta:
        model = videos
        document = video_document
        fields = '__all__'
        ordering = '-date'