from video_app.constants import GET
from django.urls import path

from . import views


app_name = 'video_app'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/',views.add,name='add'),
    path('view',views.view,name='view'),
    # elasticsearch with sharding for optimization
    # path('search/',views.search.as_view({'get':'list'}),name='search')]
    #normal search 
    path(r'search/',views.search ,name='search')]
    