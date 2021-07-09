# from video_app.constants import VIDEOS
# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl import Document, Text, Date
# from elasticsearch_dsl.field import Integer
# from elasticsearch.helpers import bulk
# from elasticsearch import Elasticsearch
# from . import models

# connections.create_connection(hosts=['localhost'])

# class video_index(Document):   
#     id = Integer() 
#     videoId = Text()
#     title = Text()    
#     date = Date()    
#     description = Text()    
#     photo = Text()
#     url = Text()    
#     class Index:        
#         name = 'video_index'

# def bulk_indexing():
#     video_index.init()
#     es = Elasticsearch()
#     bulk(client=es, actions=(b.indexing() for b in getattr(models,VIDEOS).objects.all().iterator()))