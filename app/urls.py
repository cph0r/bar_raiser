from .constants import GET
from django.urls import path

from . import views


app_name = 'app'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create', views.create, name='create'),
    path('update', views.update, name='update'),
    path('delete', views.delete, name='delete'),
    path('claim', views.claim, name='claim')]
    