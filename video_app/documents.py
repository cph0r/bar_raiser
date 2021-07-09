from typing import Text
from django_elasticsearch_dsl import Document , fields ,Index
from .models import videos

PUBLISHER_INDEX = Index('videos')

PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
)

@PUBLISHER_INDEX.doc_type
class video_document(Document):
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword'
            }
        }
    )

    description = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword'
            }
        }
    )

    video_id = fields.TextField(
        fields={
            'raw':{
                'type': 'text'
            }
        }
    )

    date = fields.DateField(
        fields={
            'raw':{
                'type': 'date'
            }
        }
    )

    photo = fields.TextField(
        fields={
            'raw':{
                'type': 'text'
            }
        }
    )

    url = fields.TextField(
        fields={
            'raw':{
                'type': 'text'
            }
        }
    )

    class Django(object):
        model = videos