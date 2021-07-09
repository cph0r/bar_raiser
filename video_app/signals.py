from .models import videos
from django.db.models.signals import post_save

from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

@receiver(post_save, sender=videos)
def index_post(sender, instance, **kwargs):
    instances = instance.videos.all()
    print("Synced es")
    for _instance in instances:
        registry.update(_instance)